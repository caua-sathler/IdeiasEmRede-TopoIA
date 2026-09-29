"""Initialise the PublicHearingBR data hub: download + phrases + embeddings + metrics.

This single script turns ``dataset/`` into the reproducible *data hub* of the
project (it merges the former ``download_dataset.py`` and
``generate_embeddings_and_standard_metrics.py``). It produces:

    dataset/
    |-- LDS/  NLI/                                 (raw HuggingFace datasets)
    |-- phrasal_data/
    |   `-- data_XXX/
    |       `-- phrases_XXX.csv                    (columns: transcript, article)
    |-- opinions_data/                             (gold key-opinions from the NLI split)
    |   `-- data_XXX/
    |       `-- opinions_XXX.csv                   (columns: opiniao, envolvido, cargo,
    |                                               alucinacao_manual, juiz_p{1..3}_{...})
    |-- <MODEL>_embeddings_phrasal_data/           (one dir per embedding model)
    |   `-- data_XXX/
    |       |-- transcript_embeddings_XXX.npy      (n_phrases, dim) float32
    |       `-- article_embeddings_XXX.npy         (n_phrases, dim) float32
    |-- <MODEL>_opinion_embeddings/                (gold-opinion embeddings, per model)
    |   `-- data_XXX/
    |       `-- opinion_embeddings_XXX.npy         (n_opinions, dim) float32
    |-- windowed_data_<CFG>/                       (sliding-window chunks; opt-in --windows)
    |   `-- data_XXX/
    |       `-- windows_XXX.csv                    (columns: transcript, article)
    |-- <MODEL>_embeddings_windowed_data_<CFG>/    (window embeddings, per model & config)
    |   `-- data_XXX/
    |       |-- transcript_embeddings_XXX.npy      (n_windows, dim) float32
    |       `-- article_embeddings_XXX.npy         (n_windows, dim) float32
    `-- metrics_<MODEL>.csv                        (one metrics file PER model)

``XXX`` is the LDS ``id`` zero-padded to 3 digits (``data_001`` ... ``data_206``).
``<CFG>`` tags a sliding-window config as ``w<size>s<stride>`` (e.g. ``w3s1`` =
windows of 3 phrases, stride 1). Windows are **additive and opt-in** (``--windows``):
they never touch ``phrasal_data`` or any existing artifact, and are fully
regenerable from the phrase CSVs, so the friend's Bottleneck (same phrases) is
unaffected.

**Multiple embedding models.** Embeddings for each model live in their own
directory ``<MODEL>_embeddings_phrasal_data`` and their standard metrics in their
own file ``metrics_<MODEL>.csv`` (e.g. ``metrics_BERT.csv``, ``metrics_MPNET.csv``).
The available models are in the ``MODELS`` registry below; add an entry and run
with ``--models <KEY>`` to add one. Each ``metrics_<MODEL>.csv`` is self-contained
(ROUGE is lexical/model-independent; the cosine columns use that model's
embeddings) and is updated **incrementally** -- re-running refreshes only the
columns this script owns and never deletes columns added elsewhere (e.g. the
``mapper_*`` columns written by the analysis notebook).

**Hallucination labels (gold).** Each opinion of the NLI split carries
``verificacao_alucinacao``: a **human** verdict ``verificacao_manual`` (True =
the extracted opinion is NOT supported by the transcript -- a confirmed
hallucination; 504 of the 4238 opinions) plus the stored verdicts of **12
LLM judges** (3 prompts x gpt-4o-mini / gpt-4o / deepseek-chat / sabia-3.1).
``generate_opinions`` propagates all of them into ``opinions_XXX.csv``
(columns ``alucinacao_manual`` and ``juiz_p<prompt>_<model>``), so the analysis
notebooks can benchmark hallucination detectors against the human labels and
the LLM judges without any API call. Existing CSVs from an older schema are
upgraded in place on the next run (row order is unchanged, so the per-model
opinion embeddings stay aligned).

Usage
-----
    python init_data.py                       # download (if missing) + BERT + metrics_BERT.csv
    python init_data.py --models all          # every model in the registry
    python init_data.py --models MPNET        # a single specific model
    python init_data.py --models BERT,MPNET
    python init_data.py --list-models         # show the registry and exit
    python init_data.py --redownload          # re-fetch the raw datasets
    python init_data.py --force               # regenerate phrases + embeddings
    python init_data.py --metrics-only        # only (re)compute metrics_<MODEL>.csv
    python init_data.py --limit 3             # first 3 records (smoke test)
    python init_data.py --windows --models all       # also build sliding-window chunks + embeddings
    python init_data.py --windows --window-configs w3s1   # a single window config
    python init_data.py --phrasal-sides article      # embed only the article side (quick partial run)
"""

from __future__ import annotations

import argparse
import os
import re
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
from datasets import load_dataset, load_from_disk

# ---------------------------------------------------------------------------
# Paths -- always resolved relative to this file so the script is CWD-independent
# ---------------------------------------------------------------------------
DATASET_DIR = Path(__file__).resolve().parent
LDS_DIR = DATASET_DIR / "LDS"
NLI_DIR = DATASET_DIR / "NLI"
PHRASAL_DIR = DATASET_DIR / "phrasal_data"
OPINIONS_DIR = DATASET_DIR / "opinions_data"

# Key column shared with the notebooks' CSVs (bottleneck_distances.csv, ...).
KEY = "data_reference"

# Sliding-window configs to build under --windows, as (size, stride) in phrases.
# Each becomes its own artifact tagged w<size>s<stride>. Kept as a list so the
# analysis notebook can *compare* granularities (premise+conclusion context for
# the NLI retriever, and coverage) rather than committing to one up front.
WINDOW_CONFIGS = [(3, 1), (4, 2), (3, 2)]

# ---------------------------------------------------------------------------
# Embedding models registry.
#
# Every model is a local mean-pooling sentence encoder via ``AutoModel`` (the
# ``hf`` field is the model id, ``dim`` its width). Embeddings are saved per
# model under ``dataset/<KEY>_embeddings_phrasal_data`` and metrics under
# ``dataset/metrics_<KEY>.csv``. Add a model with a new entry and run
# ``--models <KEY>``.
#
#   BERT   -- project baseline (anisotropic; cosine distances compressed)
#   MPNET  -- multilingual sentence-transformer, contrastively trained
#   MINILM -- lighter multilingual sentence-transformer
# ---------------------------------------------------------------------------
MODELS = {
    "BERT":   {"hf": "neuralmind/bert-base-portuguese-cased",                       "dim": 768},
    "MPNET":  {"hf": "sentence-transformers/paraphrase-multilingual-mpnet-base-v2", "dim": 768},
    "MINILM": {"hf": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2", "dim": 384},
}
DEFAULT_MODELS = ["BERT"]     # used when --models is omitted

# ---------------------------------------------------------------------------
# Hallucination-verification labels (NLI split -> opinions_data columns).
#
# Each gold opinion ships ``verificacao_alucinacao``:
#   - ``verificacao_manual``: the HUMAN verdict. True = the extracted opinion is
#     NOT supported by the transcript (a confirmed hallucination). This is the
#     ground truth used to benchmark hallucination detectors.
#   - ``prompt_<p>_<model>``: stored verdicts of 12 LLM judges (3 prompts x 4
#     models), each ``{alucinacao: bool, explicacao: str}``. We propagate only
#     the boolean verdict; the explanations stay in the NLI split.
# ``HALLUC_JUDGES`` maps the short CSV column name to the key inside
# ``verificacao_alucinacao`` (kept short so the CSVs stay readable).
# ---------------------------------------------------------------------------
_JUDGE_MODELS = [
    ("gpt4omini", "gpt-4o-mini-2024-07-18"),
    ("gpt4o",     "gpt-4o-2024-08-06"),
    ("deepseek",  "deepseek-chat"),
    ("sabia",     "sabia-3.1-2025-05-08"),
]
HALLUC_JUDGES = {
    f"juiz_p{p}_{short}": f"prompt_{p}_{full}"
    for p in (1, 2, 3)
    for short, full in _JUDGE_MODELS
}
OPINION_COLS = ["opiniao", "envolvido", "cargo", "alucinacao_manual", *HALLUC_JUDGES]


def embeddings_dir_for(model_key: str) -> Path:
    """Directory that holds ``<model_key>`` embeddings, e.g. BERT_embeddings_phrasal_data."""
    return DATASET_DIR / f"{model_key}_embeddings_phrasal_data"


def opinion_embeddings_dir_for(model_key: str) -> Path:
    """Directory that holds ``<model_key>`` gold-opinion embeddings, e.g. BERT_opinion_embeddings."""
    return DATASET_DIR / f"{model_key}_opinion_embeddings"


def metrics_csv_for(model_key: str) -> Path:
    """Metrics file for ``<model_key>``, e.g. metrics_BERT.csv."""
    return DATASET_DIR / f"metrics_{model_key}.csv"


def _cfg_tag(size: int, stride: int) -> str:
    """Compact tag for a sliding-window config, e.g. (3, 1) -> ``w3s1``."""
    return f"w{size}s{stride}"


def windows_dir_for(size: int, stride: int) -> Path:
    """Directory holding the window-text CSVs of one config, e.g. windowed_data_w3s1."""
    return DATASET_DIR / f"windowed_data_{_cfg_tag(size, stride)}"


def window_embeddings_dir_for(model_key: str, size: int, stride: int) -> Path:
    """Directory holding a model's window embeddings for one config,
    e.g. BERT_embeddings_windowed_data_w3s1."""
    return DATASET_DIR / f"{model_key}_embeddings_windowed_data_{_cfg_tag(size, stride)}"


# ---------------------------------------------------------------------------
# 0. Download the raw HuggingFace datasets (LDS + NLI)
# ---------------------------------------------------------------------------
def download_datasets(force: bool = False):
    """Fetch the PublicHearingBR LDS and NLI splits into dataset/ (skip if present)."""
    for name, out_dir, data_file in [
        ("LDS", LDS_DIR, "PublicHearingBR_LDS.jsonl"),
        ("NLI", NLI_DIR, "PublicHearingBR_NLI.jsonl"),
    ]:
        if out_dir.exists() and not force:
            print(f"{name} already present at {out_dir.relative_to(DATASET_DIR.parent)}/ -- skipping download.")
            continue
        print(f"Downloading {name} dataset...")
        ds = load_dataset("unicamp-dl/PublicHearingBR", data_files=data_file)
        ds.save_to_disk(out_dir)
        print(f"{name} saved to {out_dir.relative_to(DATASET_DIR.parent)}/.")


# ---------------------------------------------------------------------------
# 1. Phrase splitting
#
# Sentence segmentation for transcripts and articles. Besides splitting on
# sentence-final punctuation it (a) protects abbreviations / legislative
# honorifics (Sr., art., V.Sa., V.Exas., S.Exa., ...) so their dots don't force
# a split, (b) keeps a trailing-off reticence ("...") joined to a lowercase
# continuation, and (c) for articles (split_on_newlines=True) treats line breaks
# as boundaries so the headline / dek / dateline / byline become their own
# phrases instead of gluing into the first sentence.
#
# NOTE: changing this shifts every downstream .npy, the standard metrics AND the
# friend's Bottleneck (same phrases) -- regenerate with --force and align with
# the team.
# ---------------------------------------------------------------------------
def split_into_phrases(text, split_on_newlines=False):
    # Abbreviations / legislative honorifics whose trailing dot must NOT start a
    # new sentence. The honorifics (V.Sa., V.Exas., S.Exa., ...) never end a
    # sentence, so protecting them only removes false splits.
    abbrevs = [
        'sr', 'sra', 'srs', 'sras', 'dr', 'dra', 'drs', 'dras',
        'art', 'arts', 'v.exa', 'v.exas', 'exa', 's.exa', 's.exas',
        'v.sa', 'v.sas', 'dep', 'deps', 'nº', 'no',
        'reg', 'cap', 'pág', 'págs', 'vol', 'vols', 'prof', 'profa'
    ]

    temp_text = text
    # Replace the dots in abbreviations with a temporary token
    for ab in abbrevs:
        pattern = r'\b' + re.escape(ab) + r'\.'

        def repl(match):
            return match.group(0).replace('.', '___DOT___')
        temp_text = re.sub(pattern, repl, temp_text, flags=re.IGNORECASE)

    # Split pattern: matches whitespace preceded by:
    # 1. Punctuation (.!?) -> (?<=[.!?])\s+
    # 2. Punctuation followed by quotes (.!" or .!' etc.) -> (?<=[.!?]["'])\s+
    # 3. Punctuation followed by closing parenthesis (.!) or .?) etc.) -> (?<=[.!?]\))\s+
    split_pattern = r'(?<=[.!?])\s+|(?<=[.!?]["\'])\s+|(?<=[.!?]\))\s+'
    # Articles only: also break on line breaks. Headlines, deks, datelines and
    # bylines sit on their own newline-separated lines with no terminal
    # punctuation; in this corpus a newline is never followed by a lowercase
    # letter (verified), so this isolates that scaffolding without ever cutting a
    # sentence that wraps across lines.
    if split_on_newlines:
        split_pattern += r'|\s*\n\s*'
    raw_splits = re.split(split_pattern, temp_text)

    # Reassemble, keeping (a) parenthesised/bracketed asides whole and (b) a
    # trailing-off reticence joined to its lowercase continuation.
    phrases = []
    current_phrase = ""
    n_parts = len(raw_splits)

    for i, part in enumerate(raw_splits):
        part = part.strip()
        if not part:
            continue

        if current_phrase:
            current_phrase += " " + part
        else:
            current_phrase = part

        # Count parentheses and brackets in the accumulated phrase
        open_p = current_phrase.count('(')
        close_p = current_phrase.count(')')
        open_b = current_phrase.count('[')
        close_b = current_phrase.count(']')
        balanced = (open_p == close_p and open_b == close_b)

        # Reticence ("..." / "…") followed by a lowercase start = hesitation /
        # interrupted speech that was split from its own continuation -> keep
        # merging instead of emitting a truncated fragment.
        nxt = ""
        for j in range(i + 1, n_parts):
            cand = raw_splits[j].strip()
            if cand:
                nxt = cand
                break
        hold_reticence = current_phrase.endswith(('...', '…')) and nxt[:1].islower()

        # Split if balanced (and not holding a reticence) OR if the accumulated
        # phrase gets too long (> 1000 chars). The length cap keeps a single
        # unmatched parenthesis/bracket from merging the rest of the text, and it
        # only ever flushes at a sentence boundary -- it never cuts a sentence.
        if (balanced and not hold_reticence) or len(current_phrase) > 1000:
            # Restore the protected dots
            final_phrase = current_phrase.replace('___DOT___', '.')
            # Replace internal consecutive whitespaces/newlines with a single space
            final_phrase = re.sub(r'\s+', ' ', final_phrase)
            phrases.append(final_phrase)
            current_phrase = ""

    if current_phrase:
        final_phrase = current_phrase.replace('___DOT___', '.')
        final_phrase = re.sub(r'\s+', ' ', final_phrase)
        phrases.append(final_phrase)

    return phrases


def generate_phrases(dataset, force: bool):
    """Split every transcript/article into phrases and save one CSV per record."""
    PHRASAL_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Splitting {len(dataset)} records into phrases...")

    for row in dataset:
        ref = f"data_{int(row['id']):03d}"
        subfolder = PHRASAL_DIR / ref
        csv_path = subfolder / f"phrases_{ref.split('_')[-1]}.csv"

        if csv_path.exists() and not force:
            continue

        subfolder.mkdir(parents=True, exist_ok=True)
        transcript_phrases = split_into_phrases(row['transcricao']) if row.get('transcricao') else []
        # Article: also break on line breaks so the headline / dek / dateline /
        # byline (newline-separated, no terminal punctuation) become their own
        # phrases instead of gluing into the first sentence.
        article_phrases = split_into_phrases(row['materia'], split_on_newlines=True) if row.get('materia') else []

        df = pd.DataFrame({
            "transcript": pd.Series(transcript_phrases, dtype="object"),
            "article": pd.Series(article_phrases, dtype="object"),
        })
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")

    print(f"Phrases saved in '{PHRASAL_DIR.relative_to(DATASET_DIR.parent)}/'.")


# ---------------------------------------------------------------------------
# 1a. Sliding-window chunks  (opt-in --windows; additive, derived from phrases)
#
# A phrase carries a claim; a *window* of a few consecutive phrases carries the
# claim WITH its premise/conclusion. Multi-phrase context makes better premises
# for the NLI retriever (fewer "unsupported" false positives) and a richer
# coverage manifold. Built per (size, stride) config into its own folder, so the
# notebook can compare granularities. Purely derived from phrasal_data -- it does
# not alter the phrases the friend's Bottleneck relies on.
# ---------------------------------------------------------------------------
def make_windows(phrases, size, stride):
    """Sliding windows of ``size`` consecutive phrases advancing by ``stride``.

    Windows overlap when ``stride < size`` and always cover the tail: the final
    window is clamped to end on the last phrase, so no phrase is dropped and no
    undersized fragment is emitted. Each window is its phrases joined by a space.
    """
    phrases = [str(p) for p in phrases if str(p).strip()]
    n = len(phrases)
    if n == 0:
        return []
    if n <= size:
        return [" ".join(phrases)]
    starts = list(range(0, n - size + 1, stride))
    if starts[-1] != n - size:           # clamp a final window onto the tail
        starts.append(n - size)
    return [" ".join(phrases[s:s + size]) for s in starts]


def generate_windows(force: bool, configs):
    """Build sliding-window chunk CSVs (one folder per config) from the phrases.

    Reads ``phrasal_data/**/phrases_XXX.csv`` and writes, per config,
    ``windowed_data_<CFG>/data_XXX/windows_XXX.csv`` with the same
    ``transcript``/``article`` columns. Model-independent and skip-if-present.
    """
    csv_files = sorted(PHRASAL_DIR.glob("**/phrases_*.csv"))
    if not csv_files:
        print("No phrasal data found -- run phrase generation first.")
        return

    for size, stride in configs:
        out_dir = windows_dir_for(size, stride)
        out_dir.mkdir(parents=True, exist_ok=True)
        n_new = 0
        for csv_path in csv_files:
            idx = re.search(r'phrases_(\d+)\.csv', csv_path.name).group(1)
            subfolder = out_dir / f"data_{idx}"
            w_path = subfolder / f"windows_{idx}.csv"
            if w_path.exists() and not force:
                continue

            df = pd.read_csv(csv_path)
            t_src = df['transcript'].dropna().tolist() if 'transcript' in df.columns else []
            a_src = df['article'].dropna().tolist() if 'article' in df.columns else []
            transcript_windows = make_windows(t_src, size, stride)
            article_windows = make_windows(a_src, size, stride)

            subfolder.mkdir(parents=True, exist_ok=True)
            pd.DataFrame({
                "transcript": pd.Series(transcript_windows, dtype="object"),
                "article": pd.Series(article_windows, dtype="object"),
            }).to_csv(w_path, index=False, encoding="utf-8-sig")
            n_new += 1

        print(f"[windows {_cfg_tag(size, stride)}] '{out_dir.name}/': {n_new} record(s) written "
              f"({len(csv_files) - n_new} already present).")


# ---------------------------------------------------------------------------
# 1b. Gold key-opinions (from the NLI split)
#
# The PublicHearingBR ``NLI`` split ships a curated per-hearing extraction
# ``metadados_extraidos = {assunto, envolvidos[].opinioes[].{opiniao,
# chunks_proximos, verificacao_alucinacao}, tl_dr}``. We persist the key
# *opinions* -- one row each, in a deterministic ``envolvidos -> opinioes``
# order (empty ones skipped) -- so they can be embedded per model (see
# generate_opinion_embeddings) and used as a gold "importance" reference for
# coverage in the analysis notebook. Each row also carries the hallucination
# labels (``alucinacao_manual`` + the 12 ``juiz_*`` verdicts; see HALLUC_JUDGES)
# so the notebooks can benchmark detectors with zero API calls. Model-independent
# and parallel to phrasal_data; keyed by the same ``data_XXX`` (LDS/NLI id).
#
# Schema upgrade: a CSV written by an older version (without the label columns)
# is regenerated in place even without --force. The row set and order never
# change (same deterministic extraction), so the per-model opinion embeddings
# stay row-aligned -- verified against the old CSV, with a loud warning if the
# opinion texts ever differ.
# ---------------------------------------------------------------------------
def generate_opinions(dataset, force: bool):
    """Extract the gold key-opinions (text + hallucination labels) per record."""
    OPINIONS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Extracting gold opinions from {len(dataset)} NLI records...")

    n_upgraded = 0
    for row in dataset:
        ref = f"data_{int(row['id']):03d}"
        subfolder = OPINIONS_DIR / ref
        csv_path = subfolder / f"opinions_{ref.split('_')[-1]}.csv"
        old_df = None
        if csv_path.exists() and not force:
            old_df = pd.read_csv(csv_path)
            if all(c in old_df.columns for c in OPINION_COLS):
                continue          # schema already current
            n_upgraded += 1       # old schema -> regenerate in place (adds labels)

        meta = row.get('metadados_extraidos') or {}
        recs = []
        for env in (meta.get('envolvidos') or []):
            nome = (env.get('nome') or '').strip()
            cargo = (env.get('cargo') or '').strip()
            for op in (env.get('opinioes') or []):
                texto = (op.get('opiniao') or '').strip()
                if not texto:
                    continue
                ver = op.get('verificacao_alucinacao') or {}
                rec = {"opiniao": texto, "envolvido": nome, "cargo": cargo,
                       # True = human-confirmed hallucination (opinion NOT
                       # supported by the transcript).
                       "alucinacao_manual": bool(ver.get('verificacao_manual'))}
                for col, key in HALLUC_JUDGES.items():
                    j = ver.get(key) or {}
                    rec[col] = bool(j.get('alucinacao')) if isinstance(j, dict) else False
                recs.append(rec)

        new_df = pd.DataFrame(recs, columns=OPINION_COLS)
        # Alignment guard: the opinion embeddings on disk are row-aligned with the
        # old CSV; if the texts changed, they must be regenerated.
        if old_df is not None and "opiniao" in old_df.columns:
            old_txt = old_df["opiniao"].astype(str).tolist()
            if old_txt != new_df["opiniao"].astype(str).tolist():
                print(f"  [WARN] {ref}: opinion texts changed vs the old CSV -- "
                      f"regenerate <MODEL>_opinion_embeddings with --force.")

        subfolder.mkdir(parents=True, exist_ok=True)
        # Keep the columns even when a hearing has no opinions (empty CSV), so the
        # per-record structure is uniform and the notebook never KeyErrors.
        new_df.to_csv(csv_path, index=False, encoding="utf-8-sig")

    extra = f" ({n_upgraded} CSV(s) upgraded to the labeled schema)" if n_upgraded else ""
    print(f"Gold opinions saved in '{OPINIONS_DIR.relative_to(DATASET_DIR.parent)}/'{extra}.")


# ---------------------------------------------------------------------------
# 2. Sentence embeddings  (mean pooling -- one path for every registered model)
# ---------------------------------------------------------------------------
def _load_model(model_key):
    import torch
    from transformers import AutoModel, AutoTokenizer

    hf = MODELS[model_key]["hf"]
    print(f"Loading model {model_key} ({hf})...")
    tokenizer = AutoTokenizer.from_pretrained(hf)
    model = AutoModel.from_pretrained(hf)
    device = torch.device(
        "cuda" if torch.cuda.is_available()
        else "mps" if torch.backends.mps.is_available()
        else "cpu"
    )
    model = model.to(device)
    model.eval()
    print(f"  device: {device}")
    return tokenizer, model, device


def _get_embeddings(phrases, tokenizer, model, device, dim, batch_size=32):
    import torch

    if not phrases:
        return np.empty((0, dim), dtype=np.float32)

    all_embeddings = []
    for i in range(0, len(phrases), batch_size):
        batch = phrases[i: i + batch_size]
        inputs = tokenizer(batch, padding=True, truncation=True, max_length=512, return_tensors="pt")
        inputs = {k: v.to(device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = model(**inputs)

        last_hidden = outputs.last_hidden_state
        attention_mask = inputs['attention_mask'].unsqueeze(-1)

        # Mean pooling, ignoring padding tokens
        token_embeddings = last_hidden * attention_mask
        sum_embeddings = torch.sum(token_embeddings, dim=1)
        sum_mask = torch.clamp(attention_mask.sum(dim=1), min=1e-9)

        batch_embeddings = (sum_embeddings / sum_mask).cpu().numpy()
        all_embeddings.append(batch_embeddings)

    return np.vstack(all_embeddings).astype(np.float32)


def _make_embedder(model_key):
    """Return ``embed(list[str]) -> (n, dim) float32`` for this model.

    Loads the model once and mean-pools; every generate_* function goes through
    this single path.
    """
    spec = MODELS[model_key]
    dim = spec["dim"]
    tokenizer, model, device = _load_model(model_key)
    return lambda texts: _get_embeddings(texts, tokenizer, model, device, dim)


def generate_embeddings(model_key, force: bool, sides=("transcript", "article")):
    """Read every phrases_XXX.csv and save this model's transcript/article embeddings.

    ``sides`` restricts which sides to embed -- e.g. ``("article",)`` skips the huge
    transcript side (quick partial run, enough for gold-surjectivity).
    """
    emb_dir = embeddings_dir_for(model_key)
    emb_dir.mkdir(parents=True, exist_ok=True)

    csv_files = sorted(PHRASAL_DIR.glob("**/phrases_*.csv"))
    if not csv_files:
        print("No phrasal data found -- run phrase generation first.")
        return

    # Figure out which records/sides still need embeddings before loading the model.
    pending = []
    for csv_path in csv_files:
        idx = re.search(r'phrases_(\d+)\.csv', csv_path.name).group(1)
        subfolder = emb_dir / f"data_{idx}"
        paths = {s: subfolder / f"{s}_embeddings_{idx}.npy" for s in ("transcript", "article")}
        need = [s for s in sides if force or not paths[s].exists()]
        if need:
            pending.append((idx, csv_path, subfolder, paths, need))

    if not pending:
        print(f"[{model_key}] All embeddings already present -- nothing to do (use --force to regenerate).")
        return

    embed = _make_embedder(model_key)
    print(f"[{model_key}] Generating embeddings for {len(pending)} record(s) (sides: {', '.join(sides)})...")

    for idx, csv_path, subfolder, paths, need in pending:
        df = pd.read_csv(csv_path)
        subfolder.mkdir(parents=True, exist_ok=True)
        for s in need:
            texts = df[s].dropna().tolist() if s in df.columns else []
            np.save(paths[s], embed(texts))

    print(f"[{model_key}] Embeddings saved in '{emb_dir.relative_to(DATASET_DIR.parent)}/'.")


def generate_opinion_embeddings(model_key, force: bool):
    """Embed each hearing's gold opinions (opinions_data) with this model.

    Mirrors generate_embeddings: one npy per record under
    ``<model_key>_opinion_embeddings/data_XXX/opinion_embeddings_XXX.npy``, aligned
    row-for-row with ``opinions_data/data_XXX/opinions_XXX.csv``. Saved unnormalised
    (like transcript/article embeddings); the notebook L2-normalises on load.
    """
    if not OPINIONS_DIR.exists():
        print(f"[{model_key}] No opinions_data found -- run opinion extraction first.")
        return

    emb_dir = opinion_embeddings_dir_for(model_key)
    emb_dir.mkdir(parents=True, exist_ok=True)

    csv_files = sorted(OPINIONS_DIR.glob("**/opinions_*.csv"))
    if not csv_files:
        print(f"[{model_key}] No opinions CSVs found -- nothing to embed.")
        return

    pending = []
    for csv_path in csv_files:
        idx = re.search(r'opinions_(\d+)\.csv', csv_path.name).group(1)
        subfolder = emb_dir / f"data_{idx}"
        o_path = subfolder / f"opinion_embeddings_{idx}.npy"
        if force or not o_path.exists():
            pending.append((idx, csv_path, subfolder, o_path))

    if not pending:
        print(f"[{model_key}] All opinion embeddings already present -- nothing to do (use --force to regenerate).")
        return

    embed = _make_embedder(model_key)
    print(f"[{model_key}] Generating opinion embeddings for {len(pending)} record(s)...")

    for idx, csv_path, subfolder, o_path in pending:
        df = pd.read_csv(csv_path)
        opinions = df["opiniao"].dropna().astype(str).tolist() if "opiniao" in df.columns else []
        subfolder.mkdir(parents=True, exist_ok=True)
        np.save(o_path, embed(opinions))

    print(f"[{model_key}] Opinion embeddings saved in '{emb_dir.relative_to(DATASET_DIR.parent)}/'.")


def generate_window_embeddings(model_key, force: bool, configs, sides=("transcript", "article")):
    """Embed each config's sliding-window chunks with ``model_key``.

    Mirrors generate_embeddings: one npy per record under
    ``<model_key>_embeddings_windowed_data_<CFG>/data_XXX/{transcript,article}_embeddings_XXX.npy``,
    row-aligned with that config's ``windows_XXX.csv``. Saved unnormalised (the
    notebook L2-normalises on load). ``sides`` restricts which sides to embed.
    Builds the embedder once and reuses it across every pending (config, record).
    """
    pending = []   # (size, stride, idx, w_csv, subfolder, paths, need)
    for size, stride in configs:
        w_src = windows_dir_for(size, stride)
        if not w_src.exists():
            print(f"[{model_key}] windows '{w_src.name}/' not found -- run --windows first for {_cfg_tag(size, stride)}.")
            continue
        emb_dir = window_embeddings_dir_for(model_key, size, stride)
        for w_csv in sorted(w_src.glob("**/windows_*.csv")):
            idx = re.search(r'windows_(\d+)\.csv', w_csv.name).group(1)
            subfolder = emb_dir / f"data_{idx}"
            paths = {s: subfolder / f"{s}_embeddings_{idx}.npy" for s in ("transcript", "article")}
            need = [s for s in sides if force or not paths[s].exists()]
            if need:
                pending.append((size, stride, idx, w_csv, subfolder, paths, need))

    if not pending:
        print(f"[{model_key}] All window embeddings already present -- nothing to do (use --force to regenerate).")
        return

    embed = _make_embedder(model_key)
    print(f"[{model_key}] Generating window embeddings for {len(pending)} (config,record)(s) (sides: {', '.join(sides)})...")

    for size, stride, idx, w_csv, subfolder, paths, need in pending:
        df = pd.read_csv(w_csv)
        subfolder.mkdir(parents=True, exist_ok=True)
        for s in need:
            texts = df[s].dropna().astype(str).tolist() if s in df.columns else []
            np.save(paths[s], embed(texts))

    tags = ', '.join(_cfg_tag(s, t) for s, t in configs)
    print(f"[{model_key}] Window embeddings saved (configs: {tags}).")


# ---------------------------------------------------------------------------
# 3. Standard metrics  (ROUGE from phrases, cosine from each model's embeddings)
# ---------------------------------------------------------------------------
_WORD_RE = re.compile(r"\w+", re.UNICODE)


def _tokenize(text: str):
    return _WORD_RE.findall(text.lower())


def _ngram_counts(tokens, n):
    if len(tokens) < n:
        return Counter()
    return Counter(tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1))


def rouge_n_f(reference_tokens, candidate_tokens, n):
    """ROUGE-N F1 (self-contained, no external dependency).

    reference = full hearing transcript, candidate = news article. Measures the
    lexical n-gram overlap between the article and the hearing it summarises.
    Only ROUGE-1/2 are exposed: they are Counter-based (O(n+m)), whereas ROUGE-L
    would be O(n*m) LCS over ~20k-word transcripts and prohibitively slow.
    """
    ref = _ngram_counts(reference_tokens, n)
    cand = _ngram_counts(candidate_tokens, n)
    if not ref or not cand:
        return np.nan
    overlap = sum((ref & cand).values())
    if overlap == 0:
        return 0.0
    precision = overlap / sum(cand.values())
    recall = overlap / sum(ref.values())
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def cosine_centroid(transcript_emb, article_emb):
    """Cosine similarity between the mean (document-level) embeddings."""
    if len(transcript_emb) == 0 or len(article_emb) == 0:
        return np.nan
    tc = transcript_emb.mean(axis=0)
    ac = article_emb.mean(axis=0)
    denom = np.linalg.norm(tc) * np.linalg.norm(ac)
    if denom == 0:
        return np.nan
    return float(np.dot(tc, ac) / denom)


def article_grounding_cosine(transcript_emb, article_emb):
    """Mean over article phrases of the max cosine similarity to any transcript
    phrase -- how well each sentence of the news is grounded in the hearing."""
    if len(transcript_emb) == 0 or len(article_emb) == 0:
        return np.nan
    from sklearn.preprocessing import normalize
    tn = normalize(transcript_emb)
    an = normalize(article_emb)
    sims = an @ tn.T  # (n_article, n_transcript)
    return float(sims.max(axis=1).mean())


def compute_metrics(model_key):
    """Standard baseline metrics for one model: ROUGE (lexical) + cosine (this model)."""
    csv_files = sorted(PHRASAL_DIR.glob("**/phrases_*.csv"))
    if not csv_files:
        print("No phrasal data found -- nothing to compute metrics for.")
        return None

    emb_dir = embeddings_dir_for(model_key)
    if not emb_dir.exists():
        print(f"[{model_key}] embeddings not found at '{emb_dir.name}/' -- "
              f"cosine columns will be NaN (ROUGE still computed).")

    rows = []
    for csv_path in csv_files:
        idx = re.search(r'phrases_(\d+)\.csv', csv_path.name).group(1)
        ref = f"data_{idx}"

        df = pd.read_csv(csv_path)
        transcript_phrases = df['transcript'].dropna().astype(str).tolist()
        article_phrases = df['article'].dropna().astype(str).tolist()

        # --- ROUGE (lexical, from the phrases; model-independent) ---
        transcript_tokens = _tokenize(" ".join(transcript_phrases))
        article_tokens = _tokenize(" ".join(article_phrases))
        rouge1 = rouge_n_f(transcript_tokens, article_tokens, 1)
        rouge2 = rouge_n_f(transcript_tokens, article_tokens, 2)

        # --- Cosine (semantic, from this model's embeddings) ---
        t_path = emb_dir / ref / f"transcript_embeddings_{idx}.npy"
        a_path = emb_dir / ref / f"article_embeddings_{idx}.npy"
        if t_path.exists() and a_path.exists():
            transcript_emb = np.load(t_path)
            article_emb = np.load(a_path)
            cos_centroid = cosine_centroid(transcript_emb, article_emb)
            grounding = article_grounding_cosine(transcript_emb, article_emb)
        else:
            cos_centroid = grounding = np.nan

        rows.append({
            KEY: ref,
            "n_transcript_phrases": len(transcript_phrases),
            "n_article_phrases": len(article_phrases),
            "rouge1_f": rouge1,
            "rouge2_f": rouge2,
            "cosine_centroid": cos_centroid,
            "article_grounding_cosine": grounding,
        })

    return pd.DataFrame(rows)


def update_metrics_csv(new_df, metrics_csv):
    """Write ``metrics_csv``, updating only this script's columns.

    Columns added by other scripts/people (e.g. the notebook's ``mapper_*``) are
    preserved; only the columns present in ``new_df`` are (re)written, and only
    for the rows processed in this run. New records are appended.
    """
    if new_df is None or new_df.empty:
        return

    new_df = new_df.set_index(KEY)

    if Path(metrics_csv).exists():
        merged = pd.read_csv(metrics_csv).set_index(KEY)
    else:
        merged = pd.DataFrame(index=pd.Index([], name=KEY))

    # Make sure every processed record has a row.
    merged = merged.reindex(merged.index.union(new_df.index))

    # Overwrite / insert only this script's columns, only for processed rows.
    for col in new_df.columns:
        if col not in merged.columns:
            merged[col] = np.nan
        merged.loc[new_df.index, col] = new_df[col].values

    merged = merged.sort_index().reset_index()
    # Plain utf-8 (no BOM) to match bottleneck_distances.csv so the KEY column
    # stays clean when the notebooks merge on it.
    merged.to_csv(metrics_csv, index=False, encoding="utf-8")
    print(f"{Path(metrics_csv).name} updated ({len(merged)} rows, {len(merged.columns) - 1} metric columns).")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def _resolve_models(arg):
    """Turn the --models argument into a validated list of registry keys."""
    if arg is None:
        return list(DEFAULT_MODELS)
    if arg.strip().lower() == "all":
        return list(MODELS)
    keys = [k.strip() for k in arg.split(",") if k.strip()]
    unknown = [k for k in keys if k not in MODELS]
    if unknown:
        raise SystemExit(f"Unknown model(s): {unknown}. Available: {list(MODELS)}")
    return keys


def _resolve_window_configs(arg):
    """Turn --window-configs into a list of (size, stride). None/'all' = every config."""
    if arg is None or arg.strip().lower() == "all":
        return list(WINDOW_CONFIGS)
    out = []
    for tag in arg.split(","):
        tag = tag.strip().lower()
        m = re.fullmatch(r"w(\d+)s(\d+)", tag)
        if not m:
            known = ", ".join(_cfg_tag(*c) for c in WINDOW_CONFIGS)
            raise SystemExit(f"Bad window config '{tag}'. Use e.g. w3s1,w4s2 or 'all'. Known: {known}.")
        out.append((int(m.group(1)), int(m.group(2))))
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--models", default=None,
                        help="Comma-separated model keys or 'all'. Default: BERT. "
                             f"Available: {', '.join(MODELS)}.")
    parser.add_argument("--list-models", action="store_true",
                        help="Print the embedding-model registry and exit.")
    parser.add_argument("--redownload", action="store_true",
                        help="Re-fetch the raw LDS/NLI datasets even if already present.")
    parser.add_argument("--force", action="store_true",
                        help="Regenerate phrases and embeddings even if they already exist.")
    parser.add_argument("--metrics-only", action="store_true",
                        help="Skip download/phrase/embedding generation; only (re)compute metrics_<MODEL>.csv.")
    parser.add_argument("--windows", action="store_true",
                        help="Also build sliding-window chunks + their per-model embeddings (additive).")
    parser.add_argument("--window-configs", default=None,
                        help="Comma-separated window configs (e.g. w3s1,w4s2) or 'all'. Default: all. "
                             f"Known: {', '.join(_cfg_tag(*c) for c in WINDOW_CONFIGS)}.")
    parser.add_argument("--phrasal-sides", choices=["both", "transcript", "article"], default="both",
                        help="Which phrasal/window sides to embed. 'article' skips the huge transcript "
                             "side (quick partial run; enough for gold-surjectivity).")
    parser.add_argument("--limit", type=int, default=None,
                        help="Process only the first N records (useful for smoke tests).")
    args = parser.parse_args()

    if args.list_models:
        print("Available embedding models (dir = <KEY>_embeddings_phrasal_data, metrics = metrics_<KEY>.csv):")
        for k, v in MODELS.items():
            print(f"  {k:8} -> {v['hf']}  (dim={v['dim']})")
        return

    models = _resolve_models(args.models)
    window_configs = _resolve_window_configs(args.window_configs)
    sides = ("transcript", "article") if args.phrasal_sides == "both" else (args.phrasal_sides,)

    if not args.metrics_only:
        download_datasets(force=args.redownload)
        if not LDS_DIR.exists():
            raise SystemExit(f"LDS dataset not found at {LDS_DIR}. Download step failed?")
        dataset = load_from_disk(str(LDS_DIR))["train"]
        if args.limit is not None:
            dataset = dataset.select(range(min(args.limit, len(dataset))))

        generate_phrases(dataset, force=args.force)

        # Gold key-opinions from the NLI split (aligned to LDS by id -> data_XXX).
        if NLI_DIR.exists():
            nli_dataset = load_from_disk(str(NLI_DIR))["train"]
            if args.limit is not None:
                nli_dataset = nli_dataset.select(range(min(args.limit, len(nli_dataset))))
            generate_opinions(nli_dataset, force=args.force)
        else:
            print(f"NLI split not found at {NLI_DIR} -- skipping gold-opinion extraction.")

        # Sliding-window chunks (opt-in, additive): derived from the phrases above.
        if args.windows:
            print(f"Window configs: {', '.join(_cfg_tag(*c) for c in window_configs)}")
            generate_windows(force=args.force, configs=window_configs)

        print(f"Models to embed: {', '.join(models)} (sides: {', '.join(sides)})")
        for model_key in models:
            generate_embeddings(model_key, force=args.force, sides=sides)
            if OPINIONS_DIR.exists():
                generate_opinion_embeddings(model_key, force=args.force)
            if args.windows:
                generate_window_embeddings(model_key, force=args.force, configs=window_configs, sides=sides)

    # One metrics file per model, each self-contained.
    for model_key in models:
        metrics_df = compute_metrics(model_key)
        if args.limit is not None and metrics_df is not None:
            keep = {f"data_{int(i) + 1:03d}" for i in range(args.limit)}
            metrics_df = metrics_df[metrics_df[KEY].isin(keep)]
        update_metrics_csv(metrics_df, metrics_csv_for(model_key))

    print("Done.")


if __name__ == "__main__":
    main()

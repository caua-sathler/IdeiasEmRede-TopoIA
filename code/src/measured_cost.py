"""Measured cost of the cheap detector (CPU time per opinion) and of a judge call (tokens).

Measured on the same machine (CPU only): speaker parsing + name matching, incidence
features over precomputed embeddings, embedding of a transcript (once per hearing), NLI
on short sentence pairs (10 per opinion in the full detector), and the number of tokens
a judge reads (4 retrieved chunks + opinion; XLM-R tokenizer as a proxy) against the
tokens of a whole transcript. Monetary cost is NOT measured: provider prices change.

    python measured_cost.py            # writes results/measured_cost.csv
"""
from __future__ import annotations

import os
import platform
import sys
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import common as E0            # noqa: E402
import dataset_readers as R             # noqa: E402
import speaker_incidence as H6        # noqa: E402
import official_chunks as M0     # noqa: E402

warnings.filterwarnings("ignore")


def main() -> None:
    E0.banner("M4 — custo medido")
    hw = f"{platform.machine()}, {os.cpu_count()} vCPU, sem GPU"
    rows = []

    def add(comp, unidade, valor, nota=""):
        rows.append(dict(componente=comp, unidade=unidade, valor=valor, nota=nota, hardware=hw))
        print(f"  {comp:55s} {valor:>12.3f} {unidade:14s} {nota}")

    refs = R.refs_ok()
    # (a)+(b): parsing de oradores, casamento e features de incidência (0 chamadas de modelo)
    n_op = n_fr = 0
    t_parse = t_feat = 0.0
    for ref in refs[:60]:
        g, ge = R.opinions(ref), R.op_emb(ref)
        Tm = R.emb(ref, "transcript", "MPNET")
        if ge is None or not len(Tm):
            continue
        fr = (R.phrases(ref, "transcript") + [""] * len(Tm))[:len(Tm)]
        t0 = time.perf_counter()
        spk = H6.speakers(fr)
        cands = sorted({s for s in spk if s})
        idx = {c: np.where(spk == c)[0] for c in cands}
        ms = [H6.match_gold(g.envolvido.iloc[i], cands) for i in range(len(g))]
        t_parse += time.perf_counter() - t0
        t0 = time.perf_counter()
        S = ge @ Tm.T
        for i, m in enumerate(ms):
            cg = S[i].max()
            if m is not None:
                js = idx[m]
                cs = S[i, js].max()
                _ = (cg - cs, (S[i] > cs).mean(), np.sort(S[i])[::-1][:10])
        t_feat += time.perf_counter() - t0
        n_op += len(g)
        n_fr += len(Tm)
    add("parsing de oradores + casamento por nome", "ms/opiniao", 1000 * t_parse / n_op,
        f"{n_op} opinioes, 60 audiencias")
    add("features de incidencia (cosseno, sobre embeddings prontos)", "ms/opiniao",
        1000 * t_feat / n_op, "matriz opiniao x frases + maximos por orador")

    # (c) embedding das frases da transcricao (feito uma vez por audiencia)
    tot_fr = sum(len(R.emb(r, "transcript", "MPNET")) for r in refs)
    add("frases de transcricao por audiencia (media)", "frases", tot_fr / len(refs))
    add("frases de transcricao no corpus (206 audiencias)", "frases", tot_fr)
    import torch
    from transformers import AutoModel, AutoModelForSequenceClassification, AutoTokenizer
    MPNET = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    torch.set_num_threads(os.cpu_count() or 4)
    tk_e = AutoTokenizer.from_pretrained(MPNET)
    mp = AutoModel.from_pretrained(MPNET).eval()
    sents = [f for r_ in refs[:5] for f in R.phrases(r_, "transcript")][:96]
    tmed = []
    for _ in range(3):
        t0 = time.perf_counter()
        for s_ in range(0, len(sents), 32):
            enc = tk_e(sents[s_:s_ + 32], padding=True, truncation=True, max_length=128,
                       return_tensors="pt")
            with torch.inference_mode():
                mp(**enc)
        tmed.append(time.perf_counter() - t0)
    fr_ms = 1000 * float(np.median(tmed)) / len(sents)
    add("embedding MPNet de uma frase de transcricao", "ms/frase", fr_ms,
        f"{len(sents)} frases, bs=32, mediana de 3 repeticoes")
    add("embedding MPNet de todas as frases de uma audiencia (media)", "s/audiencia",
        fr_ms * tot_fr / len(refs) / 1000, "feito uma vez; nao depende do numero de opinioes")

    # (d2) NLI sobre pares CURTOS (frase da transcricao -> opiniao), como nas features nli_s/nli_g
    tkn = AutoTokenizer.from_pretrained("MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7")
    mn = AutoModelForSequenceClassification.from_pretrained(
        "MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7").eval()
    rng = np.random.default_rng(42)
    pares = []
    for ref in refs[:40]:
        fr = [f for f in R.phrases(ref, "transcript") if 60 < len(f) < 400]
        g = R.opinions(ref)
        for _ in range(5):
            pares.append((fr[int(rng.integers(len(fr)))], g.opiniao.iloc[int(rng.integers(len(g)))]))
    t0 = time.perf_counter()
    for s in range(0, len(pares), 16):
        enc = tkn(pares[s:s + 16], padding=True, truncation=True, max_length=256,
                  return_tensors="pt")
        with torch.inference_mode():
            mn(**enc)
    add("NLI mDeBERTa, par curto (frase -> opiniao)", "ms/par",
        1000 * (time.perf_counter() - t0) / len(pares), f"{len(pares)} pares")

    # (e) o que um juiz LLM le

    tk = AutoTokenizer.from_pretrained("sentence-transformers/paraphrase-multilingual-mpnet-base-v2")
    D = M0.carregar()
    amostra = D.sample(600, random_state=42)
    nt = [len(tk(" ".join(r.chunks) + " " + r.opiniao, add_special_tokens=False)["input_ids"])
          for _, r in amostra.iterrows()]
    add("tokens lidos por uma chamada de juiz (4 chunks + opiniao)", "tokens (mediana)",
        float(np.median(nt)), f"tokenizador XLM-R como proxy; media {np.mean(nt):.0f}, p95 "
        f"{np.percentile(nt, 95):.0f}; sem o texto fixo do prompt")
    # transcricao inteira, para contraste
    tt = []
    for ref in refs[:40]:
        fr = R.phrases(ref, "transcript")
        tt.append(sum(len(tk(s, add_special_tokens=False)["input_ids"]) for s in fr[:4000]))
    add("tokens de uma transcricao inteira (media, 40 audiencias)", "tokens", float(np.mean(tt)),
        "para contraste: os juizes do dataset NAO leem isto")
    pd.DataFrame(rows).to_csv(E0.OUT / "measured_cost.csv", index=False)


if __name__ == "__main__":
    main()

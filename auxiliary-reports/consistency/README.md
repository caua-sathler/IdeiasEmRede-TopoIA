# Consistency report

**When Does Answer Diversity Mean Disagreement? Possible Worlds and the Scope of Semantic Entropy** —
[`report/consistency_report.pdf`](report/consistency_report.pdf) (source: `report/consistency_report.tex`, class `desafiokunumi`).

Companion to the paper ([`../../paper/main.tex`](../../paper/main.tex)), which cites it once, in *Negative Results*:
contradictions in the retrieved evidence do **not** indicate hallucination in PublicHearingBR (report Section 7).

## Layout

| Path | Content |
|---|---|
| `report/` | LaTeX source, compiled PDF, `references.bib`, template class and figures (compiles on its own) |
| `code/run_all.sh` | Reproduces every number in the report (see below) |
| `code/src/` | The scripts |
| `code/cache/` | Precomputed generations and NLI scores (2.3 MB) — the reason everything runs offline |
| `code/results/` | `opinions_meta.csv` and `incoherent_support.csv` (inputs shipped); the other tables are regenerated |
| `code/expected_outputs/` | Reference output of each script, used by `./run_all.sh --check` |

## Reproduce

```bash
cd code
python -m venv .venv && source .venv/bin/activate      # Python 3.11
pip install -r requirements.txt                        # pinned: the reference outputs match only with these versions
./run_all.sh            # all analyses, offline, from cache/ (~1 min, CPU only)
./run_all.sh --check    # same, then diff every log against expected_outputs/ (exit 1 on any difference)
./run_all.sh --pdf      # same, then compile report/consistency_report.pdf (pdflatex + bibtex, TeX Live with newtx)
```

Logs go to `code/results/logs/`. No LLM or NLI call is made unless a cache file is deleted.

**Table 8 needs the processed PublicHearingBR.** `incoherent_support.py` runs only if `dataset/phrasal_data/` exists
(generate it at the repository root with `python dataset/init_data.py --models MPNET`, see
[`../../dataset/README.md`](../../dataset/README.md)) or `PHBR_DATA=/path/to/dataset` is set; otherwise `run_all.sh` skips it and
`intervals.py` uses the shipped `results/incoherent_support.csv`.

## Script ↔ report

| Script (`code/src/`) | Reproduces |
|---|---|
| `event_structure.py` | Worlds library and numerical check of Proposition 3; Table 2; topology (Section 4) |
| `triviaqa_worlds.py` | Sections 6.1–6.2; Table 4 (strata) and Table 5 (AUROC on TriviaQA) |
| `domain_conflict.py` | Table 6 (conflation by domain); evidence swap (Section 7) |
| `conflation_intervention.py` | Table 7 (entity → sentence intervention) |
| `incoherent_support.py` | Table 8 (PublicHearingBR support coherence) — needs the dataset |
| `intervals.py` | Intervals, controls and every number the logs above do not print: Wilson and clustered intervals, P4/P5/P6, worked example (Section 3.4), sample inventory (Table 3). Run after the three scripts before it |
| `common.py`, `finite_space.py`, `triviaqa_collect.py`, `llm.py`, `nli_runner.py` | Shared paths and AUROC; finite-space/homotopy library; TriviaQA collection helpers; LLM client and mDeBERTa NLI runner (only used to regenerate a deleted cache) |

## Caches (`code/cache/`)

| File | Content | Read by |
|---|---|---|
| `f11_triviaqa.jsonl`, `f12_nli.npz` | TriviaQA samples (233 questions) and their NLI entailment/contradiction matrices | `triviaqa_worlds`, `conflation_intervention`, `intervals` |
| `h5_longas.jsonl`, `h5_nli.npz` | Sentence-mode answers for the intervention and their NLI scores | `conflation_intervention`, `intervals` |
| `f4_geracoes.jsonl`, `f4_llama.jsonl`, `f7_intervencao.jsonl`, `h3_nli.npz` | Sampled claims about hearings (Qwen, Llama), the paired with/without-evidence intervention samples, and their NLI scores | `domain_conflict`, `intervals` |
| `f2_matrizes.npz`, `h4_nli.npz` | Entailment/similarity matrices between the 837 PublicHearingBR opinions and their retrieved transcript sentences, and the NLI scores for the support cones | `incoherent_support` |

Regenerating a cache: delete the file and rerun its script (needs `torch` and `transformers`, commented out in
`requirements.txt`). Generations need the LLM proxy described in `src/llm.py` and are not needed to reproduce anything.

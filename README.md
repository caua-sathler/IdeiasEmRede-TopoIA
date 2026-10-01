# Who Said It? Speaker-Conditioned Verification and Lexicographic Tie-Breaking

Submission repository — *Ideias em Rede, 1st edition (TopoAI)*.  
Low-cost screening of possible hallucinations for summaries of Brazilian Chamber of Deputies hearings (PublicHearingBR):
(1) verify an attributed opinion against the turns of the **attributed speaker**;
(2) use that cheap signal **only to break ties** of a 12-judge LLM committee.

## Layout

| Path | Content |
|---|---|
| `paper/` | LaTeX source (`main.tex`, `references.bib`, template class), figures and compiled `main.pdf` (15 pages) |
| `dashboard/` | Interactive dashboard, pseudonymised: `pt-br-dashboard.html` and `en-dashboard.html` (open either file in any browser); templates, data and `build.py` in `dashboard/src/` |
| `code/` | Everything needed to reproduce the paper's numbers: `run_all.sh`, `src/`, `results/`, `requirements.txt` (see `code/README.md`) |
| `dataset/` | How to obtain/process PublicHearingBR (`init_data.py`, see `dataset/README.md`) |
| `auxiliary-reports/` | Companion report(s) (item 8.2 of the call): `consistency/` has the PDF, LaTeX source and its own `code/run_all.sh` |

## Quick reproduction

```bash
cd code
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt          # pinned: results match the paper exactly only with these versions
./run_all.sh                             # all tables/numbers from the shipped intermediate tables (minutes, CPU only)
./run_all.sh --from-scratch              # rebuild the tables from the processed dataset (needs dataset/, torch, transformers)
./run_all.sh --cost                      # re-measure the CPU cost table
```

Logs go to `code/results/logs/`.

## Data, privacy and ethics

Public data only. Parliamentarians are pseudonymised ("Deputy A/B") in the paper and in every shipped
artifact; the audit sheets that contain names are **not** versioned (LGPD). The detector flags
*opinions* for human review; it does not classify or profile individuals.

## Evaluation scope and supporting material

The target is the official four-chunk NLI annotation, not a new exhaustive judgement
of each transcript. Main results use 3,630 matched-speaker opinions (408 positives).
The judges are four models with three prompts each, using released votes.

- [Feature and metric definitions](code/FEATURES.md)
- [Exploratory audit protocol](code/AUDIT_PROTOCOL.md)
- [Five-minute pitch script and recording guide](video/pitch_script.md)

For feature extraction / timing: `pip install -r code/requirements-full.txt`.
The dashboards demonstrate precomputed benchmark results; they do not run live
inference on newly supplied hearings.

## Authors

| Author | Affiliation | Contact |
|---|---|---|
| Gabriel Ribeiro | DMAT-UFMG | gabriel.ribeiro@dcc.ufmg.br |
| Cauã Sathler | DCC-UFMG | cauasathler@ufmg.br |
| Arthur Gonçalves | DCC-UFMG | afariag72@gmail.com |
| Jordan Elias | DGEO-UFC | jordanelias@alu.ufc.br |

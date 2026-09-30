# Who Said It? Speaker-Conditioned Verification and Lexicographic Tie-Breaking

Submission repository — *Ideias em Rede, 1st edition (TopoAI)*.
Low-cost hallucination detection for summaries of Brazilian Chamber of Deputies hearings
(PublicHearingBR): (1) verify an attributed opinion against the turns of the **attributed speaker**;
(2) use that cheap signal **only to break ties** of a 12-judge LLM committee.

## Layout

| Path | Content |
|---|---|
| `paper/` | LaTeX source (`main.tex`, `references.bib`, template class), figures and compiled `main.pdf` (15 pages) |
| `code/` | Everything needed to reproduce the paper's numbers: `run_all.sh`, `src/`, `results/`, `predictions/`, `requirements.txt` (see `code/README.md`) |
| `dataset/` | How to obtain/process PublicHearingBR (`init_data.py`) |
| `video/` | Pitch script (< 5 min) and recording checklist |
| `docs/` | Call for submissions and rules |

## Quick reproduction

```bash
cd code
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt          # pinned: results match the paper exactly only with these versions
./run_all.sh                             # all tables/numbers from the shipped intermediate tables (minutes, CPU only)
./run_all.sh --from-scratch              # rebuild the tables from the processed dataset (needs dataset/, torch, transformers)
./run_all.sh --cost                      # re-measure the CPU cost table
```

Logs go to `code/results/logs/`; printed tables/summaries are also stored in `code/predictions/`.

## Data, privacy and ethics

Public data only. Parliamentarians are pseudonymised ("Deputy A/B") in the paper and in every shipped
artifact; the audit sheets that contain names are **not** versioned (LGPD). The detector flags
*opinions* for human review; it does not classify or profile individuals.

## Authors

| Author | Affiliation | Contact |
|---|---|---|
| Gabriel Ribeiro | DCC-UFMG | gabriel.ribeiro@dcc.ufmg.br |
| Cauã Sathler | DCC-UFMG | cauasathler@ufmg.br |
| Arthur Gonçalves | DCC-UFMG | afariag72@gmail.com |
| Jordan Elias | UFC | jordanelias@alu.ufc.br |

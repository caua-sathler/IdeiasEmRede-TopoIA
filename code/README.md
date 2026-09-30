# Code

```bash
pip install -r requirements.txt     # numpy 2.4.6, pandas 3.0.5, scipy 1.17.1, scikit-learn 1.9.0
./run_all.sh [--from-scratch] [--cost]
```

Pinned versions matter: stacking/tree results reproduce to the 4th decimal only with them.
`torch`, `transformers`, `datasets`, `huggingface_hub` are needed only for `--from-scratch` and `--cost`.

## Modes

| Mode | Runs | Needs |
|---|---|---|
| default | the analysis scripts below, reading `results/` | CPU, pinned requirements |
| `--from-scratch` | `opinion_table`, `speaker_incidence`, `speaker_controls`, `incidence_features`, `nli_features`, `audit_sample`, then the analysis | processed dataset (`../dataset/README.md`), torch/transformers |
| `--cost` | `official_chunks`, `measured_cost` | same as above |

## Script ↔ paper claim

| Script (`src/`) | What it does / reproduces |
|---|---|
| `audit_agreement.py` | 50-opinion audit: two-pass agreement (κ = 0.81), share of misattributions (12/50) |
| `lexicographic_combination.py` | committee 0.926 → 0.930 with lexicographic tie-breaking; 20 fold partitions; gain = τ(α−½) |
| `tiebreak_controls.py` | controls for the tie-break (conditional join vs. stacking/sum) |
| `fold_stability.py` | stability across fold partitions; stacking below committee in 19/20 |
| `pair_decomposition.py` | pair-level mechanism: tied fraction τ, in-tie accuracy α, where the committee is wrong |
| `committee_histogram.py` | 13-level vote histogram (figure data) |
| `secondary_detector_attempts.py --full` | six attempts to improve the tie-breaker; none beats the baseline (α 0.489–0.520) |
| `judge_budget.py --robustez` | judge-budget ladder (1…12 judges), per-judge gains, 8 judges non-inferior, worst case, fold variance |
| `gamma_sweep.py` | f_γ gate family |
| `review_queue.py` | review-queue recall (top 10%: 40.5% → 52.2%) |
| `gain_forecast.py` | forecasting the gain on held-out hearings (≈5% error) |
| `measured_cost.py`, `official_chunks.py` | measured CPU cost table and token counts |
| `opinion_table.py`, `speaker_incidence.py`, `speaker_controls.py`, `incidence_features.py`, `nli_features.py`, `nli_runner.py` | feature construction (cosine global/in-speaker, incidence family, NLI) |
| `audit_sample.py` | draws the audit sample (output with names stays local, not versioned) |
| `common.py`, `dataset_readers.py` | shared paths, metrics, dataset readers |

## Intermediate tables (`results/`)

`opinion_table.csv` (one row per labelled opinion), `incidence_features.csv`, `nli_features.csv`,
`speaker_controls.csv`, `audit_labels.csv`, `official_chunks.csv`, `measured_cost.csv`, `gain_forecast.csv`.
`cache/nli_pairs.npz` caches NLI pair scores.

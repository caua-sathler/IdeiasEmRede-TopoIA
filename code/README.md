# Code & Replication Package

This directory contains the complete implementation, intermediate data tables, and analysis pipeline to reproduce every experimental finding and statistical claim reported in the paper.

## Directory Structure

```
code/
├── src/            # Python scripts (feature construction and statistical analyses)
├── results/        # Precomputed intermediate tables (.csv) and execution logs
├── cache/          # High-cost inference cache (compressed .npz)
├── run_all.sh      # Master reproduction runner script
└── requirements.txt # Pinned Python dependencies
```

- **`src/`**: Source code for all data processing and paper experiments:
  - *Data & Feature Construction*: `opinion_table.py`, `nli_features.py`, `nli_runner.py`, `incidence_features.py`, `speaker_incidence.py`, `speaker_controls.py`, `dataset_readers.py`, `common.py`.
  - *Analyses & Hypothesis Testing*: `lexicographic_combination.py`, `tiebreak_controls.py`, `fold_stability.py`, `pair_decomposition.py`, `committee_histogram.py`, `secondary_detector_attempts.py`, `judge_budget.py`, `gamma_sweep.py`, `review_queue.py`, `gain_forecast.py`, `audit_agreement.py`, `audit_sample.py`, `measured_cost.py`, `official_chunks.py`.
- **`results/`**: Intermediate precomputed `.csv` tables. These tables decouple lightweight statistical evaluations from expensive deep-learning inferences (allowing analyses to run on a standard laptop CPU in minutes).
  - Also hosts `results/logs/`, where stdout/stderr from each script is logged during execution.
- **`cache/`**: Persisted artifacts from computationally heavy operations. Contains `cache/nli_pairs.npz`, caching the mDeBERTa natural language inference scores for ~29,000 sentence–opinion pairs.

## Environment & Requirements

Pinned dependency versions are essential: stacking and tree-based results replicate to the 4th decimal place only with these exact versions (tested on Python 3.11).

```bash
pip install -r requirements.txt
```
*(Packages: `numpy==2.4.6`, `pandas==3.0.5`, `scipy==1.17.1`, `scikit-learn==1.9.0`)*

> [!NOTE]
> Deep learning dependencies (`torch`, `transformers`, `datasets`, `huggingface_hub`) are only required for the `--from-scratch` and `--cost` execution modes.

## How to Run & Reproduce

### 1. Automated Execution (`run_all.sh`)

Use `run_all.sh` to run the analysis pipeline or rebuild intermediate data from scratch:

```bash
./run_all.sh [--from-scratch] [--cost]
```

| Mode | Command | What it does | Requirements & Runtime |
|---|---|---|---|
| **Default** (Recommended) | `./run_all.sh` | Executes all 11 core paper analyses reading precomputed tables in `results/` | Laptop CPU, pinned requirements (~15 min) |
| **From Scratch** | `./run_all.sh --from-scratch` | Downloads dataset and mDeBERTa model, reconstructs all feature tables in `results/`, then runs the analyses | PyTorch, Transformers, `../dataset` initialized (~1–2 h on CPU) |
| **With Cost Measurement** | `./run_all.sh --cost` | Additionally computes token counts and CPU inference benchmarks | Same as `--from-scratch` |

Execution logs for every script are written to `results/logs/<script_name>.txt` and echoed to the terminal.

### 2. Running Individual Scripts

You can also run any analysis script individually from the `src/` directory:

```bash
cd src
python lexicographic_combination.py
python fold_stability.py
python secondary_detector_attempts.py --full
python judge_budget.py --robustez
```

## Script ↔ Paper Claim Mapping

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

## Intermediate Tables & Cache

The `results/` and `cache/` directories contain the following key files:

- **`results/opinion_table.csv`**: Main dataset containing one row per labelled opinion with ground truth, embeddings, and judge predictions.
- **`results/incidence_features.csv`**: Speaker-level and sentence-level incidence features.
- **`results/speaker_controls.csv`**: Controls for speaker size, identity, and clustered inference.
- **`results/nli_features.csv`**: Features derived from natural language inference models.
- **`results/audit_labels.csv`**: Human annotation labels for the 50-opinion audit sample.
- **`results/official_chunks.csv`**: Official text chunks read by judges for NLI splitting.
- **`results/measured_cost.csv`**: CPU inference runtime benchmarks and token counts.
- **`results/gain_forecast.csv`**: Projected gains on held-out public hearings.
- **`cache/nli_pairs.npz`**: Compressed binary array caching mDeBERTa pair-level scores.

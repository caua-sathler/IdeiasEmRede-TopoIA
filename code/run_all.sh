#!/usr/bin/env bash
# Reproduce every number reported in the paper.
#
#   ./run_all.sh                 analysis only, from the precomputed tables in results/
#                                (no dataset, no model download; ~15 min on a laptop CPU)
#   ./run_all.sh --from-scratch  first rebuild the tables from the PublicHearingBR dataset
#                                (downloads the dataset and mDeBERTa; ~1-2 h on CPU), then
#                                run the analysis
#   ./run_all.sh --cost          additionally measure CPU time and tokens (Table "Measured
#                                cost"); needs the dataset, the NLI split and the models
#
# Every script prints to the terminal and is also logged to results/logs/<script>.txt.
# The paper's numbers were produced with the versions in requirements.txt (Python 3.11).
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE/src"
export PYTHONDONTWRITEBYTECODE=1
LOGS="$HERE/results/logs"
mkdir -p "$LOGS"

run() {                       # run <script.py> [args...]  -> terminal + log
    local name="${1%.py}"
    echo
    echo "################ $* ################"
    python "$@" 2>&1 | tee "$LOGS/$name.txt"
}

MODE="${1:-}"

if [[ "$MODE" == "--from-scratch" ]]; then
    # 1. data: download and embed PublicHearingBR (MPNet embeddings of sentences and opinions)
    (cd "$HERE/../dataset" && python init_data.py --models MPNET)
    # 2. tables the analyses read
    run opinion_table.py          # results/opinion_table.csv
    run speaker_incidence.py      # AUROC of cos_g, cos_s, Delta and of the 12 judges
    run speaker_controls.py       # size / identity / clustered-inference controls
    run incidence_features.py     # results/incidence_features.csv
    run nli_features.py           # results/nli_features.csv (mDeBERTa, ~29k pairs)
    run audit_sample.py "$HERE/results/audit_local"   # blind sheet for the 50-positive audit
fi

if [[ "$MODE" == "--cost" ]]; then
    run official_chunks.py        # the 4 chunks a judge reads (official NLI split)
    run measured_cost.py          # results/measured_cost.csv
fi

# ---- analyses (read only results/*.csv) --------------------------------------------------
run audit_agreement.py                          # audit: agreement and kappa
run lexicographic_combination.py                # tau, ceiling, rule vs sum, vs the committee
run tiebreak_controls.py                        # random tie-break null, controls
run fold_stability.py                           # 20 fold partitions (stability table)
run pair_decomposition.py                       # exact AUROC decomposition by type of pair
run committee_histogram.py                      # committee vote levels (figure data)
run secondary_detector_attempts.py --full       # six attempts to raise alpha (all fail)
run judge_budget.py --robustez                  # gap analysis, judge-call ladder, non-inferiority
run gamma_sweep.py                              # f_gamma family: overruling the committee
run review_queue.py                             # human review queue (figure data)
run gain_forecast.py                            # forecast of the gain on unseen hearings

echo
echo "Done. Logs in $LOGS"

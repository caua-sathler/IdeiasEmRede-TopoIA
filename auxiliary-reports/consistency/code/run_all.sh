#!/usr/bin/env bash
# Reproduce every number in the consistency report (report/consistency_report.pdf).
#
#   ./run_all.sh           run all analyses offline, from the shipped caches in cache/
#                          (no LLM, no NLI model, no network; ~1 min on a laptop CPU).
#                          incoherent_support.py (Table 8) also needs the processed
#                          PublicHearingBR dataset; if dataset/phrasal_data/ is not found
#                          it is skipped and the shipped results/incoherent_support.csv is used.
#   ./run_all.sh --check   same, then diff every log against expected_outputs/
#                          (exit code 1 on any difference)
#   ./run_all.sh --pdf     same, then compile ../report/consistency_report.pdf
#                          (needs pdflatex + bibtex, TeX Live with newtx)
#
# Flags can be combined. Every script prints to the terminal and is logged to
# results/logs/<script>.txt. Numbers in the report were produced with the versions in
# requirements.txt (Python 3.11).
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE/src"
export PYTHONDONTWRITEBYTECODE=1
LOGS="$HERE/results/logs"
mkdir -p "$LOGS"

CHECK=0; PDF=0
for arg in "$@"; do
    case "$arg" in
        --check) CHECK=1 ;;
        --pdf)   PDF=1 ;;
        *) echo "unknown option: $arg (use --check and/or --pdf)" >&2; exit 2 ;;
    esac
done

run() {                       # run <script.py> -> terminal + log
    local name="${1%.py}"
    echo
    echo "################ $* ################"
    python "$@" 2>&1 | tee "$LOGS/$name.txt"
}

# ---- analyses (order matters: intervals reads the tables of the three before it) ------------
run event_structure.py            # Table 2: worlds = maximal independent sets (numerical check of Prop. 3)
run triviaqa_worlds.py            # Sec. 6.1-6.2, Tables 4-5: strata and AUROC on TriviaQA
run domain_conflict.py            # Table 6: conflation rate by domain, evidence swap
run conflation_intervention.py    # Table 7: entity -> sentence intervention
run intervals.py                  # intervals, controls, worked example, sample inventory

# Table 8 (PublicHearingBR) needs the processed dataset; the shipped
# results/incoherent_support.csv already lets intervals.py run without it.
if [[ -n "${PHBR_DATA:-}" && -d "$PHBR_DATA/phrasal_data" ]] || [[ -d "$HERE/../../../dataset/phrasal_data" ]]; then
    run incoherent_support.py
else
    echo
    echo "[skip] incoherent_support.py: dataset/phrasal_data/ not found (run"
    echo "       'python dataset/init_data.py --models MPNET' at the repo root, or set PHBR_DATA)."
    rm -f "$LOGS/incoherent_support.txt"
fi

# ---- optional: compare with the reference outputs --------------------------------------------
STATUS=0
if [[ "$CHECK" == 1 ]]; then
    echo
    echo "################ check against expected_outputs/ ################"
    for exp in "$HERE"/expected_outputs/*.txt; do
        name="$(basename "$exp")"
        if [[ ! -f "$LOGS/$name" ]]; then
            echo "SKIPPED   $name (not run)"; continue
        fi
        if diff -q <(grep -v '^gravado:' "$exp") <(grep -v '^gravado:' "$LOGS/$name") >/dev/null; then
            echo "IDENTICAL $name"
        else
            echo "DIFFERS   $name"; STATUS=1
            diff <(grep -v '^gravado:' "$exp") <(grep -v '^gravado:' "$LOGS/$name") | head -20
        fi
    done
fi

# ---- optional: compile the report ------------------------------------------------------------
if [[ "$PDF" == 1 ]]; then
    echo
    echo "################ compile report ################"
    (cd "$HERE/../report" \
        && pdflatex -interaction=nonstopmode consistency_report >/dev/null \
        && bibtex consistency_report >/dev/null \
        && pdflatex -interaction=nonstopmode consistency_report >/dev/null \
        && pdflatex -interaction=nonstopmode consistency_report >/dev/null \
        && echo "wrote report/consistency_report.pdf")
fi

echo
echo "Done. Logs in $LOGS"
exit "$STATUS"

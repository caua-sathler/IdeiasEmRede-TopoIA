"""Inter-annotator agreement for the 50-positive audit (Section 'What kind of error are the positives?').

Reads results/audit_labels.csv: for each of the 50 sampled positives, the category
assigned by each of the two independent LLM-assisted passes (M = misattributed to
another participant, S = supported/discussed by the attributed speaker, ...) and the
speaker-incidence features of the opinion (cos_s, best_other, delta). The sheet with
opinion texts is NOT versioned (it contains named individuals); `audit_sample.py`
regenerates it locally.

    python audit_agreement.py
"""
from pathlib import Path

import pandas as pd
from sklearn.metrics import cohen_kappa_score

D = Path(__file__).resolve().parent.parent / "results" / "audit_labels.csv"


def main() -> None:
    m = pd.read_csv(D).rename(columns={"category_annotator_a": "categoria_a",
                                       "category_annotator_b": "categoria_b"})
    print(pd.crosstab(m.categoria_a, m.categoria_b, margins=True))
    agree = (m.categoria_a == m.categoria_b).mean()
    kappa = cohen_kappa_score(m.categoria_a, m.categoria_b)
    print(f"\nagreement {agree:.2f} · Cohen's kappa {kappa:.3f} · n = {len(m)}")
    m["consenso"] = m.categoria_a.where(m.categoria_a == m.categoria_b, "disc")
    print("\nconsensus counts:\n", m.consenso.value_counts().to_string())
    print("\nmean features by consensus category:")
    print(m.groupby("consenso")[["cos_s", "best_other", "delta"]].mean().round(3))
    print("\nshare with delta > 0:")
    print(m.assign(pos=m.delta > 0).groupby("consenso").pos.mean().round(2))


if __name__ == "__main__":
    main()

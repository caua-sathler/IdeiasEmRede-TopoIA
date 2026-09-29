"""K2 — Label audit: agreement between the two annotation passes.

Reads out/k1_auditoria/{anotador_A,anotador_B,planilha}.csv (the sheet is built
by k1_auditoria_planilha.py) and prints the confusion table, raw agreement,
Cohen's kappa, the consensus counts per category, and the mean speaker
features per consensus category.

Categories: M = misattribution, D = distortion, F = fabrication,
S = apparently supported, I = undecidable.

    python k2_auditoria_concordancia.py
"""
from pathlib import Path

import pandas as pd
from sklearn.metrics import cohen_kappa_score

D = Path(__file__).resolve().parent / "out" / "k1_auditoria"


def main() -> None:
    a = pd.read_csv(D / "anotador_A.csv")[["item", "categoria"]]
    b = pd.read_csv(D / "anotador_B.csv")[["item", "categoria"]]
    p = pd.read_csv(D / "planilha.csv")[["item", "cos_s", "best_other", "delta"]]
    m = a.merge(b, on="item", suffixes=("_a", "_b")).merge(p, on="item")
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

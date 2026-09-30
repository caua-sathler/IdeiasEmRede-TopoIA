"""Lexicographic combination of a coarse detector and a fine one (the paper's rule).

A detector induces a preorder on opinions. A committee of binary judges takes
few distinct values, so many (positive, negative) pairs are TIED. With tau the
fraction of tied pairs, AUROC = P(correct separation) + tau/2, hence
AUROC <= 1 - tau/2 (Lemma in Background).

A weighted sum can reverse a strict decision of the reliable detector; the
LEXICOGRAPHIC rule (`join`) ranks by the committee and uses the fine score only
inside each class of tied opinions, so it never reverses a committee decision.

This module provides `deficit` (tau, ceiling, AUROC) and `join` (the rule) to the
other scripts, and when run directly prints: the tie structure of each judge and
of the committee, the rule versus a fitted sum for each single judge, and the
main comparison against the twelve-judge committee (incl. paired cluster-bootstrap CIs
and the random-tie-break / global-cosine controls).

    python lexicographic_combination.py
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import common as E0            # noqa: E402
import speaker_incidence as H6            # noqa: E402

warnings.filterwarnings("ignore")
SEED = 42


def deficit(y: np.ndarray, s: np.ndarray) -> tuple[float, float, float]:
    """(tau, teto, AUROC): tau = fracao dos pares (pos,neg) EMPATADOS; o teto
    1 - tau/2 e exato e e o maximo que qualquer desempatador pode alcancar."""
    sp, sn = s[y], s[~y]
    tot = len(sp) * len(sn)
    if tot == 0:
        return np.nan, np.nan, np.nan
    vp, cp = np.unique(sp, return_counts=True)
    vn, cn = np.unique(sn, return_counts=True)
    com = np.intersect1d(vp, vn)
    emp = sum(int(cp[vp == v][0]) * int(cn[vn == v][0]) for v in com)
    tau = emp / tot
    return tau, 1.0 - tau / 2.0, E0.auc(y, s)


def join(prim: np.ndarray, sec: np.ndarray) -> np.ndarray:
    """O JOIN no reticulado: refina `prim` por `sec` DENTRO das suas classes de
    equivalencia, sem nunca reordenar atraves delas."""
    import pandas as pd
    niv = pd.Series(prim).rank(method="dense").to_numpy()
    r = pd.Series(sec).rank(method="average").to_numpy()
    r = (r - r.min()) / max(r.max() - r.min(), 1e-9)
    return niv + 0.999 * r / (niv.max() + 1.0)


def main() -> None:
    import pandas as pd
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import GroupKFold
    from sklearn.preprocessing import StandardScaler

    Di = pd.read_csv(E0.OUT / "opinion_table.csv")
    h7 = pd.read_csv(E0.OUT / "nli_features.csv")
    Mk = Di.sem_turno.to_numpy() == 0
    sub = Di[Mk].reset_index(drop=True)
    assert len(h7) == len(sub) and np.allclose(h7.cos_s, sub.cos_s, atol=1e-6)
    print("  [ok] alinhamento verificado linha a linha")
    y = sub.hall.to_numpy().astype(bool)
    gm = sub.ref.to_numpy()
    rng = np.random.default_rng(SEED)

    def dcl(a, b, nb=5000):
        us = np.unique(gm)
        mp = {u: np.where(gm == u)[0] for u in us}
        d = []
        for _ in range(nb):
            s = np.concatenate([mp[u] for u in
                                us[rng.integers(0, len(us), len(us))]])
            if len(np.unique(y[s])) < 2:
                continue
            d.append(E0.auc(y[s], a[s]) - E0.auc(y[s], b[s]))
        d = np.array(d)
        return d.mean(), *np.percentile(d, [2.5, 97.5])

    def oof(X):
        z = np.zeros(len(y))
        for tr, te in GroupKFold(5).split(X, y, gm):
            sc = StandardScaler().fit(X[tr])
            c = LogisticRegression(max_iter=3000, class_weight="balanced")
            c.fit(sc.transform(X[tr]), y[tr])
            z[te] = c.predict_proba(sc.transform(X[te]))[:, 1]
        return z

    FAM = ["cos_s", "best_other", "share_attr", "n_spk_sup", "attr_in_sup",
           "rank_spk", "nli_s", "nli_g", "delta_n"]
    Xf = np.hstack([h7[FAM].fillna(0).to_numpy(float),
                    sub[["n_irm"]].fillna(0).to_numpy(float)])
    JU = [j for j in H6.JUIZES if j in sub and sub[j].notna().sum() > 3000]
    V = sub[JU].fillna(0).to_numpy(float)
    fino = oof(Xf)

    E0.banner("(2) O DEFICIT DE RESOLUCAO: AUROC <= 1 - tau/2, exato")
    print(f"  {'detector':30s} {'niveis':>7s} {'tau':>8s} {'teto':>8s} "
          f"{'AUROC':>8s} {'folga':>8s}")
    print("  " + "-" * 74)
    dets = [(j, sub[j].fillna(0).to_numpy(float)) for j in JU[:4]]
    dets += [("comite: soma de votos", V.sum(1)),
             ("comite: pesos OOF", oof(V)),
             ("nosso escore fino", fino)]
    for nome, s in dets:
        tau, teto, a = deficit(y, s)
        print(f"  {nome:30s} {len(np.unique(s)):7d} {tau:8.1%} {teto:8.4f} "
              f"{a:8.4f} {teto-a:8.4f}")
    print("\n  Um juiz emite um VOTO BINARIO: 2 niveis, tau ~ 100%, teto ~ 0,75.")
    print("  O teto e da GROSSURA da ordem induzida, nao da qualidade do julgamento.")

    E0.banner("(3)/(4) JOIN vs SOMA — cada juiz sozinho")
    print(f"  {'juiz':24s} {'so':>7s} {'teto':>7s} {'SOMA':>8s} {'JOIN':>8s} "
          f"{'JOIN - SOMA (IC95)':>24s}")
    print("  " + "-" * 82)
    for j in JU:
        v = sub[j].fillna(0).to_numpy(float)
        tau, teto, a0 = deficit(y, v)
        z_som = oof(np.hstack([v.reshape(-1, 1), Xf]))
        z_joi = join(v, fino)
        mu, lo, hi = dcl(z_joi, z_som)
        st = "*" if (lo > 0 or hi < 0) else " "
        print(f"  {j:24s} {a0:7.4f} {teto:7.4f} {E0.auc(y, z_som):8.4f} "
              f"{E0.auc(y, z_joi):8.4f}  {mu:+.4f} [{lo:+.4f},{hi:+.4f}]{st}")

    E0.banner("O RESULTADO — CONTRA O COMITE DOS 12")
    base = V.sum(1)
    tau, teto, a_base = deficit(y, base)
    z_add = oof(np.hstack([V, Xf]))
    cands = {
        "comite (soma de votos)": base,
        "comite (pesos OOF)": oof(V),
        "comite + familia, SOMA ADITIVA": z_add,
        "JOIN(comite, familia)": join(base, fino),
        "CONTROLE JOIN(comite, ruido)": join(base, rng.random(len(y))),
        "CONTROLE JOIN(comite, cos_g)": join(base, -sub.cos_g.to_numpy(float)),
    }
    # ATENCAO: o orcamento de um DESEMPATADOR e tau/2, nao (1 - tau/2) - AUROC.
    # A diferenca entre as duas e a lacuna de JULGAMENTO do comite (pares que ele
    # separa e ordena errado), e o Teorema (i) garante que o join nunca a toca.
    # Dividir o ganho por (teto - AUROC) subestima a captura por um fator ~2.
    orc = tau / 2.0
    print(f"  tau = {tau:.1%}  ·  orcamento do desempate (tau/2) = {orc:.4f}")
    print(f"  teto de um desempatador perfeito = {a_base + orc:.4f}   "
          f"(1 - tau/2 = {teto:.4f} inclui a lacuna de julgamento)")
    print(f"  {'metodo':36s} {'AUROC':>8s} {'% do orcamento tau/2':>23s}")
    print("  " + "-" * 70)
    for nome, s in cands.items():
        a = E0.auc(y, s)
        rec = (a - a_base) / orc * 100 if orc > 1e-9 else np.nan
        print(f"  {nome:36s} {a:8.4f} {rec:22.1f}%")
    print()
    z_best = cands["JOIN(comite, familia)"]
    for nome, a, b in [
            ("JOIN vs comite (soma de votos)", z_best, base),
            ("JOIN vs comite (pesos OOF)", z_best, cands["comite (pesos OOF)"]),
            ("JOIN vs SOMA ADITIVA", z_best, z_add),
            ("JOIN vs CONTROLE(ruido)", z_best, cands["CONTROLE JOIN(comite, ruido)"]),
            ("JOIN vs CONTROLE(cos_g)", z_best, cands["CONTROLE JOIN(comite, cos_g)"])]:
        mu, lo, hi = dcl(a, b)
        st = "  *" if (lo > 0 or hi < 0) else ""
        print(f"  {nome:38s} {mu:+.4f} [{lo:+.4f},{hi:+.4f}]{st}")


if __name__ == "__main__":
    main()

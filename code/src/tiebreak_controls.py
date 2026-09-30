"""J5 — O JOIN CONDICIONAL e a distribuição nula do desempate.

Duas correções que a teoria exige e que o j4 deixou em aberto.

(a) A DISTRIBUIÇÃO NULA. Um desempatador ALEATÓRIO tem AUROC esperado igual ao do
    detector original (empate conta ½), mas VARIÂNCIA alta: no j3 uma realização
    deu 0,9236 e no j4 outra deu 0,9278. Comparar contra UMA realização não
    decide nada. O controle correto é a distribuição sobre muitos sorteios.

(b) O SECUNDÁRIO CERTO. O join usa o escore fino apenas DENTRO das classes de
    equivalência do detector confiável. Logo o que importa é a discriminação
    INTRA-CLASSE, e um modelo treinado globalmente não é treinado para isso —
    ele gasta capacidade separando o que o primário já separa. A teoria pede um
    secundário CONDICIONAL: ajustado dentro de cada classe.

    join_cond(prim, X) = refina cada classe de `prim` por um modelo OOF ajustado
                         SÓ naquela classe (com recuo ao modelo global se n for
                         pequeno).

    python tiebreak_controls.py
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
from lexicographic_combination import deficit, join   # noqa: E402

warnings.filterwarnings("ignore")
SEED = 42
N_MIN = 150          # n minimo por classe para ajustar um modelo proprio


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

    def oof(X, mask=None):
        """OOF com GroupKFold por audiencia; se `mask`, ajusta so nessas linhas."""
        m = np.ones(len(y), bool) if mask is None else mask
        z = np.full(len(y), np.nan)
        yy, gg, XX = y[m], gm[m], X[m]
        idx = np.where(m)[0]
        if len(np.unique(yy)) < 2 or yy.sum() < 5 or (~yy).sum() < 5:
            return z
        k = min(5, len(np.unique(gg)))
        if k < 2:
            return z
        for tr, te in GroupKFold(k).split(XX, yy, gg):
            if len(np.unique(yy[tr])) < 2:
                continue
            sc = StandardScaler().fit(XX[tr])
            c = LogisticRegression(max_iter=3000, class_weight="balanced")
            c.fit(sc.transform(XX[tr]), yy[tr])
            z[idx[te]] = c.predict_proba(sc.transform(XX[te]))[:, 1]
        return z

    FAM = ["cos_s", "best_other", "share_attr", "n_spk_sup", "attr_in_sup",
           "rank_spk", "nli_s", "nli_g", "delta_n"]
    Xf = np.hstack([h7[FAM].fillna(0).to_numpy(float),
                    sub[["n_irm"]].fillna(0).to_numpy(float)])
    JU = [j for j in H6.JUIZES if j in sub and sub[j].notna().sum() > 3000]
    V = sub[JU].fillna(0).to_numpy(float)
    base = V.sum(1)

    def join_cond(prim, X):
        """O JOIN CONDICIONAL: dentro de cada classe de `prim`, um modelo OOF
        ajustado SO naquela classe (recuo ao global se n < N_MIN)."""
        glob = oof(X)
        sec = glob.copy()
        for v in np.unique(prim):
            m = prim == v
            if m.sum() >= N_MIN:
                loc = oof(X, m)
                ok = ~np.isnan(loc[m])
                if ok.mean() > 0.9:
                    sec[m] = np.where(np.isnan(loc[m]), glob[m], loc[m])
        return join(prim, sec), sec

    E0.banner("(a) A DISTRIBUICAO NULA DO DESEMPATE (200 sorteios)")
    a_base = E0.auc(y, base)
    nul = np.array([E0.auc(y, join(base, rng.random(len(y))))
                    for _ in range(200)])
    print(f"  comite (soma de votos) ......... {a_base:.4f}")
    print(f"  desempatador ALEATORIO ......... media {nul.mean():.4f} · "
          f"dp {nul.std():.4f} · p95 {np.percentile(nul, 95):.4f} · "
          f"max {nul.max():.4f}")

    E0.banner("(b) O JOIN CONDICIONAL")
    z_gf = join(base, oof(Xf))
    z_cf, _ = join_cond(base, Xf)
    tau, teto, _ = deficit(y, base)
    # o orcamento de um desempatador e tau/2 (ver a nota no j4): (1 - tau/2) - AUROC
    # inclui a lacuna de julgamento, que o Teorema (i) impede o join de tocar.
    orc = tau / 2.0
    linhas = [("comite (soma de votos)", base),
              ("JOIN global,  familia", z_gf),
              ("JOIN CONDICIONAL, familia", z_cf)]
    print(f"  tau {tau:.1%} · orcamento tau/2 = {orc:.4f} · teto de um "
          f"desempatador perfeito {a_base + orc:.4f}")
    print(f"  {'metodo':34s} {'AUROC':>8s} {'% orcam.':>9s} {'p vs nulo':>11s}")
    print("  " + "-" * 66)
    for nome, s in linhas:
        a = E0.auc(y, s)
        p = (nul >= a).mean()
        print(f"  {nome:34s} {a:8.4f} {(a-a_base)/orc*100:8.1f}% "
              f"{p:11.3f}")

    melhor = max(linhas[1:], key=lambda t: E0.auc(y, t[1]))
    E0.banner(f"O CONFRONTO — {melhor[0]}")
    z_add = oof(np.hstack([V, Xf]))
    z_oof = oof(V)
    for nome, b in [("comite (soma de votos)", base),
                    ("comite (pesos OOF)", z_oof),
                    ("comite + familia, SOMA ADITIVA", z_add),
                    ("JOIN global (lexicographic_combination.py)", z_gf)]:
        mu, lo, hi = dcl(melhor[1], b)
        st = "  *" if (lo > 0 or hi < 0) else ""
        print(f"  vs {nome:34s} {mu:+.4f} [{lo:+.4f},{hi:+.4f}]{st}")

    E0.banner("O MESMO, POR JUIZ INDIVIDUAL (1 chamada)")
    print(f"  {'juiz':24s} {'so':>7s} {'SOMA':>8s} {'JOIN cond':>10s} "
          f"{'JOIN - SOMA (IC95)':>24s}")
    print("  " + "-" * 76)
    top = ("", 0.0)
    for j in JU:
        v = sub[j].fillna(0).to_numpy(float)
        z_s = oof(np.hstack([v.reshape(-1, 1), Xf]))
        z_j, _ = join_cond(v, Xf)
        a_j = E0.auc(y, z_j)
        if a_j > top[1]:
            top = (j, a_j)
        mu, lo, hi = dcl(z_j, z_s)
        st = "*" if (lo > 0 or hi < 0) else " "
        print(f"  {j:24s} {E0.auc(y, v):7.4f} {E0.auc(y, z_s):8.4f} "
              f"{a_j:10.4f}  {mu:+.4f} [{lo:+.4f},{hi:+.4f}]{st}")
    print(f"\n  melhor a 1 chamada: {top[0]} = {top[1]:.4f}")


if __name__ == "__main__":
    main()

"""I4 — A GUARDA CONTRA O COMITÊ, a volume igualado e em teste pareado.

O i3 mediu que, entre as opiniões que o comitê dos 12 juízes APROVA, a camada
conjunta concentra os erros restantes (lift 1,76–1,87×, IC excluindo 1,0). Mas o
escore usado ali contém a família H6/H7 — então o lift pode ser da família, não da
camada conjunta.

Este script roda o protocolo que a E26 estabeleceu e que decidiu o veredito da
guarda de nervo: cada candidata sinaliza EXATAMENTE o mesmo número de itens, e o
IC é o da DIFERENÇA de lifts nas mesmas reamostras (não IC sobrepostos).

Candidatas:
    conj   camada CONJUNTA pura (Hodge + duplicação), sem a família
    fam    família H6/H7 + n_irm (o melhor sinal por-opinião que temos)
    tudo   família + camada conjunta
    triv   guardas triviais: cos_s baixo, delta_n alto, n_irm alto

    python i4_guarda_comite.py
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import comum as E0            # noqa: E402
import h6_orador as H6            # noqa: E402

warnings.filterwarnings("ignore")
SEED = 42
FAM = ["cos_s", "best_other", "share_attr", "n_spk_sup", "attr_in_sup",
       "rank_spk", "nli_s", "nli_g", "delta_n"]
HOD = ["h_att", "g_att", "phi_spk", "r_spk", "h_norm", "phi_op"]


def main() -> None:
    import pandas as pd
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import GroupKFold
    from sklearn.preprocessing import StandardScaler

    Di = pd.read_csv(E0.OUT / "i2_hodge.csv")
    Dd = pd.read_csv(E0.OUT / "i3_dup.csv")
    h7 = pd.read_csv(E0.OUT / "h7_nli_orador.csv")
    assert len(Dd) == len(Di) and (Dd.hall == Di.hall).all(), "desalinhado"
    Mk = Di.sem_turno.to_numpy() == 0
    sub, dup = Di[Mk].reset_index(drop=True), Dd[Mk].reset_index(drop=True)
    assert len(h7) == len(sub) and (h7.hall.to_numpy() == sub.hall.to_numpy()).all()
    print("  [ok] alinhamento verificado linha a linha")
    y = sub.hall.to_numpy().astype(bool)
    gm = sub.ref.to_numpy()
    rng = np.random.default_rng(SEED)

    def oof(X):
        z = np.zeros(len(y))
        for tr, te in GroupKFold(5).split(X, y, gm):
            sc = StandardScaler().fit(X[tr])
            c = LogisticRegression(max_iter=3000, class_weight="balanced")
            c.fit(sc.transform(X[tr]), y[tr])
            z[te] = c.predict_proba(sc.transform(X[te]))[:, 1]
        return z

    Xf = np.hstack([h7[FAM].fillna(0).to_numpy(float),
                    sub[["n_irm"]].fillna(0).to_numpy(float)])
    Xc = np.hstack([sub[HOD].fillna(0).to_numpy(float),
                    dup[["dup"]].to_numpy(float)])
    Xcs = np.hstack([sub[[c + "_sh" for c in HOD]].fillna(0).to_numpy(float),
                     dup[["dup_sh"]].to_numpy(float)])
    JU = [j for j in H6.JUIZES if j in sub and sub[j].notna().sum() > 3000]
    z_com = oof(sub[JU].fillna(0).to_numpy(float))

    cand = {
        "CONJUNTA pura (Hodge+dup)": oof(Xc),
        "CONJUNTA embaralhada": oof(Xcs),
        "familia H6/H7 (+n_irm)": oof(Xf),
        "familia + CONJUNTA": oof(np.hstack([Xf, Xc])),
        "trivial: cos_s baixo": -sub.cos_s.to_numpy(float),
        "trivial: delta_n alto": h7.delta_n.fillna(0).to_numpy(float),
    }

    def lifts(sel_ap, esc, frac):
        """lift a volume igualado: sinaliza os `frac` piores dos aprovados."""
        yy = y[sel_ap]
        s = esc[sel_ap]
        k = max(int(round(frac * len(s))), 5)
        thr = np.sort(s)[-k]
        m = s >= thr
        if yy.mean() <= 0 or m.sum() == 0:
            return np.nan, m
        return yy[m].mean() / yy.mean(), m

    for q in [0.90, 0.80, 0.70]:
        ap = z_com <= np.quantile(z_com, q)
        yy, gg = y[ap], gm[ap]
        if yy.sum() < 5:
            continue
        E0.banner(f"APROVADOS PELO COMITE — cobertura {1-q:.0%} mais segura "
                  f"(n={ap.sum()}, risco {yy.mean():.1%})")
        res = {}
        for nome, esc in cand.items():
            lf, m = lifts(ap, esc, 0.25)
            res[nome] = (lf, m, yy[m].sum() / max(yy.sum(), 1))
        print(f"  {'guarda (25% dos aprovados)':30s} {'lift':>6s} {'captura':>8s}")
        print("  " + "-" * 48)
        for nome, (lf, m, cap) in res.items():
            print(f"  {nome:30s} {lf:6.2f} {cap:8.1%}")
        # teste PAREADO da diferenca de lifts, nas mesmas reamostras
        us = np.unique(gg)
        mp = {u: np.where(gg == u)[0] for u in us}
        print(f"\n  {'diferenca pareada de lifts':44s} {'media':>7s} {'IC95':>18s}")
        print("  " + "-" * 72)
        for a, b in [("familia + CONJUNTA", "familia H6/H7 (+n_irm)"),
                     ("CONJUNTA pura (Hodge+dup)", "CONJUNTA embaralhada"),
                     ("CONJUNTA pura (Hodge+dup)", "trivial: cos_s baixo"),
                     ("CONJUNTA pura (Hodge+dup)", "trivial: delta_n alto")]:
            ma, mb = res[a][1], res[b][1]
            d = []
            for _ in range(3000):
                sel = np.concatenate([mp[u] for u in
                                      us[rng.integers(0, len(us), len(us))]])
                ys = yy[sel]
                if ys.mean() <= 0:
                    continue
                A, B = ma[sel], mb[sel]
                if A.sum() < 3 or B.sum() < 3:
                    continue
                d.append(ys[A].mean() / ys.mean() - ys[B].mean() / ys.mean())
            d = np.array(d)
            lo, hi = np.percentile(d, [2.5, 97.5])
            st = "  *" if (lo > 0 or hi < 0) else ""
            print(f"  {a[:20]:22s} vs {b[:20]:20s} {d.mean():+7.2f} "
                  f"[{lo:+6.2f},{hi:+6.2f}]{st}")


if __name__ == "__main__":
    main()

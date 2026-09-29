"""J3 — O COMITÊ É LIMITADO POR RESOLUÇÃO, NÃO POR INFORMAÇÃO.

O ACHADO que orienta este script (j2): `cos_s` e `h_att` preveem ONDE o comitê
erra com AUROC 0,64 — e mesmo assim não somam a ele numa regressão logística. A
explicação é medível e é estrutural:

    o comitê são 12 VOTOS BINÁRIOS -> 13 níveis -> 31,3% DOS PARES EMPATADOS

Um par empatado conta 0,5 no AUROC, ganhe ou perca. Toda a informação contínua do
mundo, somada aditivamente a um escore de 13 níveis, é diluída pelos pesos; o que
falta não é sinal novo, é RESOLUÇÃO dentro dos níveis.

A combinação certa é LEXICOGRÁFICA: o comitê ordena, e o nosso escore desempata
DENTRO de cada nível, sem nunca reordenar através dos níveis. É a operação que
respeita a natureza dos dois sinais — um voto grosseiro e confiável, um escore
fino e barato.

    python j3_desempate.py
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


def main() -> None:
    import pandas as pd
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import GroupKFold
    from sklearn.preprocessing import StandardScaler

    Di = pd.read_csv(E0.OUT / "i2_hodge.csv")
    Dj = pd.read_csv(E0.OUT / "j1_continuidade.csv")
    Dd = pd.read_csv(E0.OUT / "i3_dup.csv")
    h7 = pd.read_csv(E0.OUT / "h7_nli_orador.csv")
    Mk = Di.sem_turno.to_numpy() == 0
    sub, jj, dup = (Di[Mk].reset_index(drop=True), Dj[Mk].reset_index(drop=True),
                    Dd[Mk].reset_index(drop=True))
    assert len(h7) == len(sub) and np.allclose(h7.cos_s, sub.cos_s, atol=1e-6)
    assert (Dj.hall.to_numpy() == Di.hall.to_numpy()).all()
    print("  [ok] alinhamento verificado linha a linha")
    y = sub.hall.to_numpy().astype(bool)
    gm = sub.ref.to_numpy()
    rng = np.random.default_rng(SEED)

    def dcl(a, b, nb=4000):
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
    HOD = ["h_att", "g_att", "phi_spk", "r_spk", "h_norm", "phi_op"]
    CON = ["g", "mu", "d", "omega"]
    Xf = np.hstack([h7[FAM].fillna(0).to_numpy(float),
                    sub[["n_irm"]].fillna(0).to_numpy(float)])
    Xh = np.hstack([sub[HOD].fillna(0).to_numpy(float),
                    dup[["dup"]].to_numpy(float)])
    Xc = jj[CON].fillna(0).to_numpy(float)
    JU = [j for j in H6.JUIZES if j in sub and sub[j].notna().sum() > 3000]
    V = sub[JU].fillna(0).to_numpy(float)

    nosso = {"familia H6/H7": oof(Xf),
             "familia + Hodge": oof(np.hstack([Xf, Xh])),
             "familia + Hodge + cont": oof(np.hstack([Xf, Xh, Xc]))}
    comite = {"soma de votos (crua)": V.sum(1),
              "comite OOF (pesos aprendidos)": oof(V)}

    def lex(prim, sec):
        """Ordena por `prim`; DENTRO de cada empate, ordena por `sec`.
        Nunca reordena atraves dos niveis: o comite manda, nos desempatamos."""
        r = pd.Series(sec).rank(method="average").to_numpy()
        r = (r - r.min()) / max(r.max() - r.min(), 1e-9)
        niv = pd.Series(prim).rank(method="dense").to_numpy()
        return niv + 0.999 * r / (niv.max() + 1.0)

    E0.banner("O DIAGNOSTICO — quanto do AUROC do comite e perdido em EMPATE?")
    for nome, c in comite.items():
        n = len(c)
        cnt = np.bincount(pd.Series(c).rank(method="dense").astype(int))
        emp = sum(k * (k - 1) / 2 for k in cnt) / (n * (n - 1) / 2)
        print(f"  {nome:34s} niveis {len(np.unique(c)):5d} · "
              f"pares empatados {emp:6.1%} · AUROC {E0.auc(y, c):.4f}")

    E0.banner("A COMBINACAO LEXICOGRAFICA (o comite ordena, nos desempatamos)")
    base_n, base = "soma de votos (crua)", comite["soma de votos (crua)"]
    a_base = E0.auc(y, base)
    print(f"  referencia: {base_n} = {a_base:.4f}\n")
    print(f"  {'desempatador':34s} {'AUROC':>8s} {'ganho pareado (IC95 agrupado)':>34s}")
    print("  " + "-" * 78)
    melhor = ("", 0.0, None)
    for nome, s in nosso.items():
        z = lex(base, s)
        a = E0.auc(y, z)
        mu, lo, hi = dcl(z, base)
        st = "  *" if lo > 0 else ""
        if a > melhor[1]:
            melhor = (nome, a, z)
        print(f"  {nome:34s} {a:8.4f}   {mu:+.4f} [{lo:+.4f},{hi:+.4f}]{st}")
    # controles: desempatar por ruido e por um escalar trivial
    for nome, s in [("CONTROLE: ruido aleatorio", rng.random(len(y))),
                    ("CONTROLE: cos_g global (o piso)",
                     -sub.cos_g.to_numpy(float))]:
        z = lex(base, s)
        mu, lo, hi = dcl(z, base)
        st = "  *" if lo > 0 else ""
        print(f"  {nome:34s} {E0.auc(y, z):8.4f}   {mu:+.4f} "
              f"[{lo:+.4f},{hi:+.4f}]{st}")

    E0.banner("CONTRA O MELHOR COMITE DISPONIVEL (pesos OOF) e vs SOMA ADITIVA")
    com_oof = comite["comite OOF (pesos aprendidos)"]
    z_lex = melhor[2]
    z_add = oof(np.hstack([V, Xf, Xh, Xc]))
    print(f"  comite OOF (pesos aprendidos) ......... {E0.auc(y, com_oof):.4f}")
    print(f"  comite + tudo, SOMA ADITIVA (logistica) {E0.auc(y, z_add):.4f}")
    print(f"  comite + tudo, LEXICOGRAFICA .......... {E0.auc(y, z_lex):.4f}"
          f"   <- {melhor[0]}")
    print()
    for nome, a, b in [("lexicografica vs soma de votos", z_lex, base),
                       ("lexicografica vs comite OOF", z_lex, com_oof),
                       ("lexicografica vs soma aditiva", z_lex, z_add)]:
        mu, lo, hi = dcl(a, b)
        st = "  *" if (lo > 0 or hi < 0) else ""
        print(f"  {nome:36s} {mu:+.4f} [{lo:+.4f},{hi:+.4f}]{st}")

    E0.banner("ONDE O GANHO VEM — decomposicao por nivel de voto")
    vs = V.sum(1)
    print(f"  {'votos':>6s} {'n':>6s} {'alucin.':>8s} {'AUROC do desempatador':>22s}")
    print("  " + "-" * 46)
    s = nosso[melhor[0]]
    for v in range(13):
        m = vs == v
        if m.sum() < 40 or y[m].sum() < 3 or (~y[m]).sum() < 3:
            continue
        print(f"  {v:6.0f} {m.sum():6d} {y[m].mean():7.1%} "
              f"{E0.auc(y[m], s[m]):22.4f}")


if __name__ == "__main__":
    main()

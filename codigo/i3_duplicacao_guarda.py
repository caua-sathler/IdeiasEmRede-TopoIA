"""I3 — A terceira obstrução (DUPLICAÇÃO) e a leitura de GUARDA.

P12/P13 — DUPLICAÇÃO. O resumo afirma um mapa α : O → A. As opiniões carregam uma
estrutura de similaridade entre si que NADA neste projeto jamais computou. Se o₁ e
o₂ são quase idênticas e atribuídas a oradores diferentes, ou os dois disseram o
mesmo (possível num debate), ou uma é duplicata má-atribuída — e a EVIDÊNCIA decide:

    dup(o) = max_{o' ≠ o, α(o') ≠ α(o)}  sim(o,o') · [ M[o, α(o')] - M[o, α(o)] ]_+

"existe uma opinião quase idêntica à minha, atribuída a OUTRO orador, e a minha
evidência está nos turnos DAQUELE orador, não nos do meu". É função de α restrita
às outras opiniões — o mesmo teorema de cegueira conjunta do i1.

P14 — GUARDA. A E26 estabeleceu que um sinal pode falhar como classificador e
funcionar como guarda com explicação. Entre as opiniões que o comitê dos 12
APROVA, a camada conjunta concentra os erros restantes?

    python i3_duplicacao_guarda.py
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import comum as E0            # noqa: E402
import dados as R           # noqa: E402
import h6_orador as H6            # noqa: E402

warnings.filterwarnings("ignore")
SEED = 42


def coletar():
    import pandas as pd
    linhas = []
    rng = np.random.default_rng(SEED)
    for ri, r in enumerate(R.refs_ok()):
        Tm = R.emb(r, "transcript", R.GEOM)
        g, ge = R.opinions(r), R.op_emb(r)
        if not len(Tm) or ge is None or len(g) != len(ge):
            continue
        fr = R.phrases(r, "transcript")[:len(Tm)]
        if len(fr) < len(Tm):
            fr = fr + [""] * (len(Tm) - len(fr))
        spk = H6.speakers(fr)
        cands = sorted({s for s in spk if s})
        if len(cands) < 2:
            continue
        S = ge @ Tm.T
        idx = {c: np.where(spk == c)[0] for c in cands}
        rot = np.array([not pd.isna(v) for v in g.alucinacao_manual])
        gi = np.where(rot)[0]
        if len(gi) < 3:
            continue
        M = np.array([[float(S[i, idx[c]].max()) for c in cands] for i in gi])
        quem = (g.envolvido.to_numpy()[gi] if "envolvido" in g
                else np.array([None] * len(gi)))
        atr = np.array([cands.index(m) if (m := H6.match_gold(q_, cands))
                        else -1 for q_ in quem])
        casado = atr >= 0
        if casado.sum() < 3:
            continue
        # similaridade OPINIÃO x OPINIÃO — a estrutura nunca computada
        Go = ge[gi]
        SS = Go @ Go.T
        np.fill_diagonal(SS, -1.0)

        def dup_de(av):
            out = np.zeros(len(gi))
            viz = np.zeros(len(gi))
            for o in range(len(gi)):
                if av[o] < 0:
                    continue
                melhor, vz = 0.0, 0.0
                for o2 in range(len(gi)):
                    if o2 == o or av[o2] < 0 or av[o2] == av[o]:
                        continue
                    s = float(SS[o, o2])
                    if s <= 0:
                        continue
                    vz = max(vz, s)
                    ganho = M[o, av[o2]] - M[o, av[o]]
                    melhor = max(melhor, s * max(ganho, 0.0))
                out[o], viz[o] = melhor, vz
            return out, viz

        d_re, viz = dup_de(atr)
        a_sh = atr.copy()
        vs = np.where(casado)[0]
        a_sh[vs] = atr[rng.permutation(vs)]
        d_sh, _ = dup_de(a_sh)
        for kk, o in enumerate(gi):
            linhas.append({"ref": r, "hall": int(bool(g.alucinacao_manual.iloc[o])),
                           "sem_turno": int(not casado[kk]),
                           "dup": d_re[kk], "dup_sh": d_sh[kk],
                           "viz_max": viz[kk]})
        if (ri + 1) % 50 == 0:
            print(f"  {ri+1}/206 · {len(linhas)} opinioes", flush=True)
    D = pd.DataFrame(linhas)
    D.to_csv(E0.OUT / "i3_dup.csv", index=False)
    return D


def main() -> None:
    import pandas as pd
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import GroupKFold
    from sklearn.preprocessing import StandardScaler

    cam = E0.OUT / "i3_dup.csv"
    Dd = pd.read_csv(cam) if cam.exists() else coletar()
    Di = pd.read_csv(E0.OUT / "i2_hodge.csv")
    h7 = pd.read_csv(E0.OUT / "h7_nli_orador.csv")
    assert len(Dd) == len(Di), f"alinhamento i3={len(Dd)} vs i2={len(Di)}"
    assert (Dd.hall.to_numpy() == Di.hall.to_numpy()).all(), "rotulos desalinhados"
    print("  [ok] alinhamento i3 <-> i2 verificado linha a linha")

    Mk = Di.sem_turno.to_numpy() == 0
    sub, dup = Di[Mk].reset_index(drop=True), Dd[Mk].reset_index(drop=True)
    assert len(h7) == len(sub), "alinhamento h7"
    y = sub.hall.to_numpy().astype(bool)
    gm = sub.ref.to_numpy()
    rng = np.random.default_rng(SEED)

    def dauc_cl(a, b, nb=3000):
        us = np.unique(gm)
        mp = {u: np.where(gm == u)[0] for u in us}
        d = []
        for _ in range(nb):
            sel = np.concatenate([mp[u] for u in
                                  us[rng.integers(0, len(us), len(us))]])
            if len(np.unique(y[sel])) < 2:
                continue
            d.append(E0.auc(y[sel], a[sel]) - E0.auc(y[sel], b[sel]))
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

    E0.banner("P12 — A DUPLICACAO CARREGA SINAL?")
    for c, nome in [("dup", "dup   (real)"), ("dup_sh", "dup   EMBARALHADO"),
                    ("viz_max", "viz_max (controle: so a similaridade)")]:
        print(f"  {nome:38s} {E0.auc(y, dup[c].to_numpy(float)):7.4f}")
    mu, lo, hi = dauc_cl(dup.dup.to_numpy(float), dup.dup_sh.to_numpy(float))
    st = "  *" if (lo > 0 or hi < 0) else ""
    print(f"\n  dup real vs EMBARALHADO: {mu:+.4f} [{lo:+.4f},{hi:+.4f}]{st}")
    print(f"  dup > 0 em {(dup.dup > 1e-9).mean():.1%} das opinioes")

    E0.banner("P13 — SOMA A BASE? (OOF, GroupKFold por audiencia)")
    FAM = ["cos_s", "best_other", "share_attr", "n_spk_sup", "attr_in_sup",
           "rank_spk", "nli_s", "nli_g", "delta_n"]
    HOD = ["h_att", "g_att", "phi_spk", "r_spk", "h_norm", "phi_op"]
    Xf = np.hstack([h7[FAM].fillna(0).to_numpy(float),
                    sub[["n_irm"]].fillna(0).to_numpy(float)])
    Xh = sub[HOD].fillna(0).to_numpy(float)
    Xd = dup[["dup"]].to_numpy(float)
    Xds = dup[["dup_sh"]].to_numpy(float)
    z_b = oof(Xf)
    z_bh = oof(np.hstack([Xf, Xh]))
    z_bd = oof(np.hstack([Xf, Xd]))
    z_all = oof(np.hstack([Xf, Xh, Xd]))
    z_alls = oof(np.hstack([Xf, sub[[c + "_sh" for c in HOD]].fillna(0)
                            .to_numpy(float), Xds]))
    print(f"  base (familia + n_irm) ............ {E0.auc(y, z_b):.4f}")
    print(f"  base + Hodge ...................... {E0.auc(y, z_bh):.4f}")
    print(f"  base + duplicacao ................. {E0.auc(y, z_bd):.4f}")
    print(f"  base + Hodge + duplicacao (TUDO) .. {E0.auc(y, z_all):.4f}")
    print(f"  base + tudo EMBARALHADO (controle). {E0.auc(y, z_alls):.4f}")
    print()
    for nome, a, b in [("base+dup vs base", z_bd, z_b),
                       ("TUDO vs base", z_all, z_b),
                       ("TUDO vs base+Hodge", z_all, z_bh),
                       ("TUDO vs EMBARALHADO (o controle)", z_all, z_alls)]:
        mu, lo, hi = dauc_cl(a, b)
        st = "  *" if (lo > 0 or hi < 0) else ""
        print(f"  {nome:36s} {mu:+.4f} [{lo:+.4f},{hi:+.4f}]{st}")

    E0.banner("P14 — A LEITURA DE GUARDA (a moldura da E26)")
    JU = [j for j in H6.JUIZES if j in sub and sub[j].notna().sum() > 3000]
    votos = sub[JU].fillna(0).to_numpy(float).sum(1)
    z_com = oof(sub[JU].fillna(0).to_numpy(float))
    conj = z_all
    print(f"  comite dos 12 (OOF) = {E0.auc(y, z_com):.4f}")
    print(f"\n  {'aprovados pelo comite':28s} {'n':>6s} {'risco':>7s} "
          f"{'sinaliz.':>9s} {'lift':>6s} {'IC95':>18s} {'captura':>8s}")
    print("  " + "-" * 82)
    for q in [0.90, 0.80, 0.70, 0.60, 0.50]:
        thr = np.quantile(z_com, q)
        ap = z_com <= thr                     # o comite APROVA (baixo risco)
        if ap.sum() < 50 or y[ap].sum() < 5:
            continue
        s = conj[ap]
        yy = y[ap]
        gg = gm[ap]
        marca = s >= np.quantile(s, 0.75)      # o quartil mais suspeito
        if marca.sum() < 10 or yy[marca].sum() < 2:
            continue
        lift = (yy[marca].mean() / yy.mean()) if yy.mean() > 0 else np.nan
        us = np.unique(gg)
        mp = {u: np.where(gg == u)[0] for u in us}
        bs = []
        for _ in range(3000):
            sel = np.concatenate([mp[u] for u in
                                  us[rng.integers(0, len(us), len(us))]])
            ys, ms = yy[sel], marca[sel]
            if ys.mean() <= 0 or ms.sum() < 3:
                continue
            bs.append(ys[ms].mean() / ys.mean())
        lo, hi = np.percentile(bs, [2.5, 97.5])
        st = "*" if lo > 1.0 else " "
        cap = yy[marca].sum() / max(yy.sum(), 1)
        print(f"  cobertura {1-q:4.0%} mais segura {ap.sum():6d} "
              f"{yy.mean():6.1%} {marca.sum():9d} {lift:6.2f} "
              f"[{lo:5.2f},{hi:5.2f}]{st} {cap:7.1%}")
    print(f"\ngravado: {E0.OUT / 'i3_dup.csv'}")


if __name__ == "__main__":
    main()

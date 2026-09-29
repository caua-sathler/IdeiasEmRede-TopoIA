"""I2 — A corrente de atribuição nas 206 audiências: P1–P8 do `i0_predicoes.md`.

Custo: ZERO chamadas de modelo (a matriz M sai dos embeddings que o h6 já usa;
a decomposição é álgebra linear em grafos de ~30 vértices).

Confrontos primários declarados: P4 (soma à família de incidência) e P5 (soma ao
comitê dos 12 juízes). Todo o resto é secundário/exploratório.

    python i2_hodge_audiencias.py
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
import i1_corrente_atribuicao as I1   # noqa: E402

warnings.filterwarnings("ignore")
SEED = 42
K_TOP = 5
JUIZES = H6.JUIZES


def coletar() -> "object":
    import pandas as pd

    linhas = []
    refs = R.refs_ok()
    rng = np.random.default_rng(SEED)
    for ri, r in enumerate(refs):
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
        cos_g = np.array([float(S[i].max()) for i in gi])
        quem = (g.envolvido.to_numpy()[gi] if "envolvido" in g
                else np.array([None] * len(gi)))
        atr = np.array([cands.index(m) if (m := H6.match_gold(q_, cands))
                        else -1 for q_ in quem])
        casado = atr >= 0
        if casado.sum() < 3:
            continue

        P = I1.perfil(M, atr, k=K_TOP)
        # CONTROLE (P6): mesma M, mesmo grafo, atribuição EMBARALHADA entre as
        # opiniões casadas da audiência (preserva o multiconjunto de oradores).
        atr_sh = atr.copy()
        vs = np.where(casado)[0]
        atr_sh[vs] = atr[rng.permutation(vs)]
        Psh = I1.perfil(M, atr_sh, k=K_TOP)

        # ---- superlotação (P9–P11) e defeito de Hall (P8), por orador
        def camada_exclusiva(av: np.ndarray) -> tuple:
            """(preço-sombra por opinião, lacuna do orador, nº de irmãs)."""
            dl = np.zeros(len(gi))
            gap = np.zeros(len(gi))
            nir = np.zeros(len(gi))
            for a in np.unique(av[av >= 0]):
                ops = np.where(av == a)[0]
                js = idx[cands[a]]
                nir[ops] = len(ops)
                if len(ops) < 2 or len(js) < 1:
                    continue
                # frases candidatas: união dos top-5 de cada opinião irmã
                cs = sorted({int(j) for o in ops
                             for j in js[np.argsort(-S[gi[o], js])[:5]]})
                N = np.array([[float(S[gi[o], j]) for j in cs] for o in ops])
                g_, d_ = I1.superlotacao(N)
                dl[ops] = d_
                gap[ops] = g_
            return dl, gap, nir

        d_lot, g_lot, n_irm = camada_exclusiva(atr)
        d_lot_sh, g_lot_sh, _ = camada_exclusiva(atr_sh)

        defs = np.zeros(len(gi))
        for a in np.unique(atr[casado]):
            ops = np.where(atr == a)[0]
            js = idx[cands[a]]
            if len(ops) < 2 or len(js) < 1:
                continue
            sup = np.array([[S[gi[o], j] >= 0.55 for j in js] for o in ops])
            defs[ops] = I1.defeito_hall(sup)

        for kk, o in enumerate(gi):
            row = {
                "ref": r, "hall": int(bool(g.alucinacao_manual.iloc[o])),
                "cos_g": cos_g[kk],
                "cos_s": M[kk, atr[kk]] if casado[kk] else np.nan,
                "sem_turno": int(not casado[kk]),
                "h_att": P["h_att"][kk], "g_att": P["g_att"][kk],
                "phi_spk": P["phi_spk"][kk], "r_spk": P["r_spk"][kk],
                "h_norm": P["h_norm"][kk], "phi_op": P["phi_op"][kk],
                # controle P6: TODAS as seis features recomputadas no perfil
                # embaralhado (um controle parcial nao e controle)
                "h_att_sh": Psh["h_att"][kk], "g_att_sh": Psh["g_att"][kk],
                "phi_spk_sh": Psh["phi_spk"][kk], "r_spk_sh": Psh["r_spk"][kk],
                "h_norm_sh": Psh["h_norm"][kk], "phi_op_sh": Psh["phi_op"][kk],
                "rho": P["rho"], "rho_sh": Psh["rho"],
                "dim_ciclo": P["dim_ciclo"], "n_op": len(gi),
                "n_spk": len(cands), "hall_def": defs[kk],
                "d_lot": d_lot[kk], "g_lot": g_lot[kk], "n_irm": n_irm[kk],
                "d_lot_sh": d_lot_sh[kk], "g_lot_sh": g_lot_sh[kk],
            }
            for j in JUIZES:
                if j in g:
                    v = g[j].iloc[o]
                    if not pd.isna(v):
                        row[j] = int(bool(v))
            linhas.append(row)
        if (ri + 1) % 50 == 0:
            print(f"  {ri+1}/{len(refs)} · {len(linhas)} opinioes", flush=True)
    D = pd.DataFrame(linhas)
    D.to_csv(E0.OUT / "i2_hodge.csv", index=False)
    return D


def main() -> None:
    import pandas as pd
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import GroupKFold
    from sklearn.preprocessing import StandardScaler

    cam = E0.OUT / "i2_hodge.csv"
    D = pd.read_csv(cam) if cam.exists() else coletar()
    y = D.hall.to_numpy().astype(bool)
    grp = D.ref.to_numpy()
    rng = np.random.default_rng(SEED)

    def dauc_cl(a, b, yy, gg, nb=3000):
        """Bootstrap AGRUPADO por audiência (o i.i.d. por linha é otimista)."""
        us = np.unique(gg)
        mp = {u: np.where(gg == u)[0] for u in us}
        d = []
        for _ in range(nb):
            sel = np.concatenate([mp[u] for u in
                                  us[rng.integers(0, len(us), len(us))]])
            if len(np.unique(yy[sel])) < 2:
                continue
            d.append(E0.auc(yy[sel], a[sel]) - E0.auc(yy[sel], b[sel]))
        d = np.array(d)
        return d.mean(), *np.percentile(d, [2.5, 97.5])

    def oof(X, yy, gg):
        z = np.zeros(len(yy))
        for tr, te in GroupKFold(5).split(X, yy, gg):
            sc = StandardScaler().fit(X[tr])
            c = LogisticRegression(max_iter=3000, class_weight="balanced")
            c.fit(sc.transform(X[tr]), yy[tr])
            z[te] = c.predict_proba(sc.transform(X[te]))[:, 1]
        return z

    # ------------------------------------------------------------------ P1
    E0.banner("P1 — SANIDADE (tem de reproduzir o h6 exatamente)")
    print(f"  n={len(D)} · alucinadas={int(y.sum())} ({y.mean():.1%}) · "
          f"audiencias={D.ref.nunique()}")
    print(f"  cos_g global (todos) ........... "
          f"{E0.auc(y, -D.cos_g.to_numpy(float)):.4f}   (h6: 0.5628)")
    Mk = D.sem_turno.to_numpy() == 0
    ym, gm = y[Mk], grp[Mk]
    sub = D[Mk].reset_index(drop=True)
    print(f"  casados: n={Mk.sum()} ({int(ym.sum())} alucinadas)")
    print(f"  cos_g (casados) ................ "
          f"{E0.auc(ym, -sub.cos_g.to_numpy(float)):.4f}   (h6: 0.5676)")
    print(f"  cos_s (casados) ................ "
          f"{E0.auc(ym, -sub.cos_s.to_numpy(float)):.4f}   (h6: 0.7455)")

    # ------------------------------------------------------------------ P2
    E0.banner("P2 — O OBJETO EXISTE?")
    au = D.drop_duplicates("ref")
    print(f"  dim Z_1 (espaco de ciclos) ..... mediana {au.dim_ciclo.median():.0f}"
          f" · media {au.dim_ciclo.mean():.1f}")
    print(f"  fracao harmonica rho ........... media {au.rho.mean():.3f} · "
          f"mediana {au.rho.median():.3f}   (predicao: >= 0,10)")
    print(f"  rho EMBARALHADO ................ media {au.rho_sh.mean():.3f}")
    dr = au.rho_sh.to_numpy() - au.rho.to_numpy()
    b = np.array([np.mean(dr[rng.integers(0, len(dr), len(dr))])
                  for _ in range(3000)])
    st = "  *" if (np.percentile(b, 2.5) > 0 or np.percentile(b, 97.5) < 0) else ""
    print(f"  P6(a) embaralhado - real ....... {dr.mean():+.4f} "
          f"[{np.percentile(b,2.5):+.4f},{np.percentile(b,97.5):+.4f}]{st}")

    # ------------------------------------------------------------------ P3/P7
    E0.banner("P3 / P7 — O SINAL ISOLADO, e HARMONICO vs GRADIENTE")
    feats = [("cos_s", -1, "cos_s (a familia H6, referencia)"),
             ("h_att", +1, "h_att   HARMONICO na aresta atribuida"),
             ("g_att", +1, "g_att   GRADIENTE na aresta atribuida"),
             ("phi_spk", +1, "phi_spk potencial do orador"),
             ("r_spk", +1, "r_spk   residuo de credito do orador"),
             ("h_norm", +1, "h_norm  norma harmonica da opiniao"),
             ("hall_def", +1, "def. de Hall do orador (P8, explorat.)"),
             ("d_lot", +1, "d_lot   PRECO-SOMBRA de superlotacao (P9)"),
             ("g_lot", +1, "g_lot   lacuna de superlotacao do orador"),
             ("n_irm", +1, "n_irm   nº de opinioes do orador (controle)"),
             ("h_att_sh", +1, "h_att EMBARALHADO  (P6b: tem de cair)"),
             ("d_lot_sh", +1, "d_lot EMBARALHADO (P11: tem de cair)")]
    print(f"  {'feature':42s} {'AUROC':>7s}")
    print("  " + "-" * 52)
    for c, sg, nome in feats:
        v = sub[c].to_numpy(float) * sg
        print(f"  {nome:42s} {E0.auc(ym, v):7.4f}")

    for nome, a, b_ in [("P6(b)  h_att real vs EMBARALHADO", "h_att", "h_att_sh"),
                        ("P11    d_lot real vs EMBARALHADO", "d_lot", "d_lot_sh")]:
        mu, lo, hi = dauc_cl(sub[a].to_numpy(float), sub[b_].to_numpy(float),
                             ym, gm)
        st = "  *" if (lo > 0 or hi < 0) else ""
        print(f"\n  {nome}: {mu:+.4f} [{lo:+.4f},{hi:+.4f}]{st}")

    # ------------------------------------------------------------------ P4
    E0.banner("P4 — SOMA A FAMILIA DE INCIDENCIA? (OOF, GroupKFold por audiencia)")
    h7 = pd.read_csv(E0.OUT / "h7_nli_orador.csv")
    assert len(h7) == len(sub), f"alinhamento: h7={len(h7)} vs sub={len(sub)}"
    assert (h7.hall.to_numpy() == sub.hall.to_numpy()).all(), "rotulos desalinhados"
    assert np.allclose(h7.cos_s.to_numpy(), sub.cos_s.to_numpy(), atol=1e-6), \
        "cos_s desalinhado entre h7 e i2"
    print("  [ok] alinhamento h7 <-> i2 verificado linha a linha")

    FAM = ["cos_s", "best_other", "share_attr", "n_spk_sup", "attr_in_sup",
           "rank_spk", "nli_s", "nli_g", "delta_n"]
    HOD = ["h_att", "g_att", "phi_spk", "r_spk", "h_norm", "phi_op"]
    LOT = ["d_lot", "g_lot"]
    Xf = h7[FAM].fillna(0).to_numpy(float)
    Xn = sub[["n_irm"]].fillna(0).to_numpy(float)      # o contador trivial
    Xh = sub[HOD].fillna(0).to_numpy(float)
    Xl = sub[LOT].fillna(0).to_numpy(float)
    Xhs = sub[[c + "_sh" for c in HOD]].fillna(0).to_numpy(float)
    Xls = sub[[c + "_sh" for c in LOT]].fillna(0).to_numpy(float)
    # baseline ESTENDIDO: a familia mais o contador trivial de opinioes-irmas.
    # A camada conjunta tem de bater ISTO, nao a familia crua (o controle da E26:
    # a guarda topologica tem de bater a guarda trivial da mesma decomposicao).
    z_f = oof(Xf, ym, gm)
    z_fn = oof(np.hstack([Xf, Xn]), ym, gm)
    z_j = oof(np.hstack([Xh, Xl]), ym, gm)
    z_fh = oof(np.hstack([Xf, Xn, Xh]), ym, gm)
    z_fl = oof(np.hstack([Xf, Xn, Xl]), ym, gm)
    z_ful = oof(np.hstack([Xf, Xn, Xh, Xl]), ym, gm)
    z_sh = oof(np.hstack([Xf, Xn, Xhs, Xls]), ym, gm)
    print(f"  familia H6+H7 (referencia) ........ {E0.auc(ym, z_f):.4f}  (h7: 0.7792)")
    print(f"  familia + n_irm (baseline trivial). {E0.auc(ym, z_fn):.4f}")
    print(f"  so a camada CONJUNTA (Hodge+lotac.) {E0.auc(ym, z_j):.4f}")
    print(f"  base + HODGE ...................... {E0.auc(ym, z_fh):.4f}")
    print(f"  base + SUPERLOTACAO ............... {E0.auc(ym, z_fl):.4f}")
    print(f"  base + HODGE + SUPERLOTACAO ....... {E0.auc(ym, z_ful):.4f}")
    print(f"  base + tudo EMBARALHADO (controle). {E0.auc(ym, z_sh):.4f}")
    print()
    for nome, a, b_ in [
            ("base(+n_irm) vs familia crua", z_fn, z_f),
            ("P4   base+Hodge vs base", z_fh, z_fn),
            ("P10a base+lotacao vs base", z_fl, z_fn),
            ("P10b base+Hodge+lotacao vs base", z_ful, z_fn),
            ("P11  base+conjunta vs base+EMBARALHADO", z_ful, z_sh)]:
        mu, lo, hi = dauc_cl(a, b_, ym, gm)
        st = "  *" if (lo > 0 or hi < 0) else ""
        print(f"  {nome:40s} {mu:+.4f} [{lo:+.4f},{hi:+.4f}]{st}")
    Xh = np.hstack([Xh, Xl, Xn])        # a camada CONJUNTA completa, para o P5
    Xf = np.hstack([Xf, Xn])

    # ------------------------------------------------------------------ P5
    E0.banner("P5 — SOMA AOS JUIZES E AO COMITE? (a aposta forte)")
    jj = [j for j in JUIZES if j in sub and sub[j].notna().sum() > 3000]
    Xj = sub[jj].fillna(0).to_numpy(float)
    z_com = oof(Xj, ym, gm)
    z_com_f = oof(np.hstack([Xj, Xf]), ym, gm)
    z_com_h = oof(np.hstack([Xj, Xh]), ym, gm)
    z_com_fh = oof(np.hstack([Xj, Xf, Xh]), ym, gm)
    print(f"  comite dos 12 (pesos OOF) ...... {E0.auc(ym, z_com):.4f}   (h6c: 0.9245)")
    print(f"  comite + familia H6/H7 ......... {E0.auc(ym, z_com_f):.4f}")
    print(f"  comite + HODGE ................. {E0.auc(ym, z_com_h):.4f}")
    print(f"  comite + familia + HODGE ....... {E0.auc(ym, z_com_fh):.4f}")
    for nome, a, b_ in [("comite+familia vs comite", z_com_f, z_com),
                        ("comite+Hodge  vs comite", z_com_h, z_com),
                        ("comite+fam+Hodge vs comite", z_com_fh, z_com),
                        ("comite+fam+Hodge vs comite+fam", z_com_fh, z_com_f)]:
        mu, lo, hi = dauc_cl(a, b_, ym, gm)
        st = "  *" if (lo > 0 or hi < 0) else ""
        print(f"  {nome:34s} {mu:+.4f} [{lo:+.4f},{hi:+.4f}]{st}")

    print()
    print(f"  {'juiz':24s} {'sozinho':>8s} {'+fam':>8s} {'+fam+Hodge':>11s}")
    print("  " + "-" * 54)
    melhor = (None, 0.0)
    for j in jj:
        vj = sub[j].fillna(0).to_numpy(float).reshape(-1, 1)
        a0 = E0.auc(ym, vj.ravel())
        a1 = E0.auc(ym, oof(np.hstack([vj, Xf]), ym, gm))
        z2 = oof(np.hstack([vj, Xf, Xh]), ym, gm)
        a2 = E0.auc(ym, z2)
        if a2 > melhor[1]:
            melhor = (j, a2, z2, np.hstack([vj, Xf]))
        print(f"  {j:24s} {a0:8.4f} {a1:8.4f} {a2:11.4f}")
    if melhor[0]:
        mu, lo, hi = dauc_cl(melhor[2], oof(melhor[3], ym, gm), ym, gm)
        st = "  *" if (lo > 0 or hi < 0) else ""
        print(f"\n  melhor 1-chamada: {melhor[0]} + fam + Hodge = {melhor[1]:.4f}")
        print(f"  ganho do Hodge sobre juiz+familia: {mu:+.4f} "
              f"[{lo:+.4f},{hi:+.4f}]{st}")
    print(f"\ngravado: {E0.OUT / 'i2_hodge.csv'}")


if __name__ == "__main__":
    main()

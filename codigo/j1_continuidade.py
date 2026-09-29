"""J1 — FIDELIDADE É CONTINUIDADE: a obstrução de alinhamento monótono.

Por Alexandrov, um mapa entre ordens totais finitas é CONTÍNUO sse é MONÓTONO. O
resumo afirma um mapa ρ : (O, ordem do resumo) -> (T, ordem do tempo). Um resumo
fiel é um mapa contínuo; uma opinião ALUCINADA não tem posição verdadeira, é
inserida onde o sumarizador quis, e quebra a monotonicidade — é literalmente uma
DESCONTINUIDADE.

    V_livre = Σ_i max_t N[i,t]                       (o que cos_s computa)
    V_mono  = max_{t_1 ≤ … ≤ t_k} Σ_i N[i,t_i]       (a melhor leitura CONTÍNUA)
    Ω       = V_livre − V_mono ≥ 0                   a OBSTRUÇÃO

Por opinião: preço-sombra g_i, deslocamento d_i, e o marginal deixando-um-fora
μ_i = (V_mono^{-i} + max_t N[i,t]) − V_mono — a obstrução a ESTENDER a seção
monótona de O∖{o_i} para O, no sentido literal de teoria de obstrução.

É a fonte EXÓGENA que o diagnóstico da fase I pedia: t_i* depende da ORDEM DO
RESUMO, que não está em M. Nenhum juiz LLM que leia uma opinião por vez tem acesso
a ela.

Predições registradas em `j0_predicoes.md`. Custo: zero chamadas de modelo.

    python j1_continuidade.py
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


def alinha_monotono(N: np.ndarray) -> tuple[float, np.ndarray]:
    """Melhor alinhamento FRACAMENTE MONÓTONO: escolhe t_1 ≤ … ≤ t_k maximizando
    Σ_i N[i,t_i]. DP com máximo-prefixo, O(k·m).

    Devolve (valor, posições escolhidas). É o análogo discreto de exigir que o mapa
    ρ seja contínuo (= monótono, por Alexandrov)."""
    k, m = N.shape
    if k == 0 or m == 0:
        return 0.0, np.zeros(k, int)
    V = np.full((k, m), -np.inf)
    BP = np.zeros((k, m), int)
    V[0] = N[0]
    for i in range(1, k):
        melhor, arg = -np.inf, 0
        for t in range(m):
            if V[i - 1, t] > melhor:
                melhor, arg = V[i - 1, t], t
            V[i, t] = melhor + N[i, t]
            BP[i, t] = arg
    t = int(np.argmax(V[k - 1]))
    pos = np.zeros(k, int)
    for i in range(k - 1, -1, -1):
        pos[i] = t
        t = BP[i, t]
    return float(V[k - 1].max()), pos


def perfil_continuidade(N: np.ndarray) -> dict:
    """Todas as features de continuidade de UM orador, de uma vez."""
    k, m = N.shape
    livre = N.max(1)
    if k == 0 or m == 0:
        return {"g": np.zeros(k), "d": np.zeros(k), "mu": np.zeros(k),
                "omega": 0.0}
    Vm, pos = alinha_monotono(N)
    g = livre - N[np.arange(k), pos]
    d = np.abs(pos - N.argmax(1)) / max(m - 1, 1)
    mu = np.zeros(k)
    if k >= 2:
        for i in range(k):
            keep = [j for j in range(k) if j != i]
            Vi, _ = alinha_monotono(N[keep])
            mu[i] = (Vi + livre[i]) - Vm
    return {"g": g, "d": d, "mu": mu, "omega": float(livre.sum() - Vm)}


def coletar():
    import pandas as pd
    rng = np.random.default_rng(SEED)
    linhas, taus = [], []
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
        quem = (g.envolvido.to_numpy()[gi] if "envolvido" in g
                else np.array([None] * len(gi)))
        atr = [H6.match_gold(q_, cands) for q_ in quem]

        cols = {c: np.full(len(gi), np.nan) for c in
                ("g", "d", "mu", "omega", "g_p", "d_p", "mu_p", "omega_p",
                 "k_spk")}
        for a in {x for x in atr if x}:
            ops = [i for i in range(len(gi)) if atr[i] == a]
            js = idx[a]
            if len(ops) < 2 or len(js) < 2:
                continue
            N = np.array([[float(S[gi[o], j]) for j in js] for o in ops])
            P = perfil_continuidade(N)
            # CONTROLE (P3): a MESMA N com a ordem do resumo PERMUTADA. Mesma
            # matriz, mesmas opiniões, mesmos turnos — só a ordem destruída.
            pm = rng.permutation(len(ops))
            Pp = perfil_continuidade(N[pm])
            inv = np.argsort(pm)
            for kk, o in enumerate(ops):
                cols["g"][o], cols["d"][o], cols["mu"][o] = \
                    P["g"][kk], P["d"][kk], P["mu"][kk]
                cols["g_p"][o], cols["d_p"][o], cols["mu_p"][o] = \
                    Pp["g"][inv[kk]], Pp["d"][inv[kk]], Pp["mu"][inv[kk]]
                cols["omega"][o] = P["omega"]
                cols["omega_p"][o] = Pp["omega"]
                cols["k_spk"][o] = len(ops)
            # tau de sanidade
            pg = np.array([int(js[int(np.argmax(S[gi[o], js]))]) for o in ops],
                          float)
            oo = np.arange(len(ops), dtype=float)
            c = d_ = 0
            for i in range(len(ops)):
                for j in range(i + 1, len(ops)):
                    s = np.sign(oo[i] - oo[j]) * np.sign(pg[i] - pg[j])
                    c += s > 0
                    d_ += s < 0
            if c + d_:
                taus.append((c - d_) / (c + d_))

        for kk, o in enumerate(gi):
            row = {"ref": r, "hall": int(bool(g.alucinacao_manual.iloc[o])),
                   "sem_turno": int(atr[kk] is None),
                   "cos_s": (float(S[o, idx[atr[kk]]].max())
                             if atr[kk] else np.nan)}
            for c in cols:
                row[c] = cols[c][kk]
            linhas.append(row)
        if (ri + 1) % 50 == 0:
            print(f"  {ri+1}/206 · {len(linhas)} opinioes", flush=True)
    D = pd.DataFrame(linhas)
    D.to_csv(E0.OUT / "j1_continuidade.csv", index=False)
    print(f"  tau medio dentro do orador: {np.mean(taus):+.4f} "
          f"(j0: +0.5982)", flush=True)
    return D


def main() -> None:
    import pandas as pd
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import GroupKFold
    from sklearn.preprocessing import StandardScaler

    cam = E0.OUT / "j1_continuidade.csv"
    Dj = pd.read_csv(cam) if cam.exists() else coletar()
    Di = pd.read_csv(E0.OUT / "i2_hodge.csv")
    Dd = pd.read_csv(E0.OUT / "i3_dup.csv")
    h7 = pd.read_csv(E0.OUT / "h7_nli_orador.csv")
    assert len(Dj) == len(Di) == len(Dd), "desalinhado"
    assert (Dj.hall.to_numpy() == Di.hall.to_numpy()).all(), "rotulos desalinhados"
    Mk = Di.sem_turno.to_numpy() == 0
    jj, sub, dup = (Dj[Mk].reset_index(drop=True), Di[Mk].reset_index(drop=True),
                    Dd[Mk].reset_index(drop=True))
    assert len(h7) == len(sub) and np.allclose(h7.cos_s, sub.cos_s, atol=1e-6)
    print("  [ok] alinhamento j1 <-> i2 <-> i3 <-> h7 verificado linha a linha")
    y = sub.hall.to_numpy().astype(bool)
    gm = sub.ref.to_numpy()
    rng = np.random.default_rng(SEED)

    def dcl(a, b, nb=3000):
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

    E0.banner("P1/P2 — O SINAL ISOLADO DA CONTINUIDADE")
    print(f"  n={len(sub)} · alucinadas={int(y.sum())} · "
          f"cos_s={E0.auc(y, -sub.cos_s.to_numpy(float)):.4f} (h6: 0.7455)")
    print(f"  opinioes com >= 2 irmas no orador: "
          f"{(jj.k_spk.fillna(0) >= 2).mean():.1%}")
    print(f"\n  {'feature':44s} {'AUROC':>7s}")
    print("  " + "-" * 54)
    for c, nome in [("g", "g   preco-sombra da monotonicidade"),
                    ("mu", "mu  marginal deixando-um-fora (obstrucao)"),
                    ("d", "d   deslocamento no alinhamento"),
                    ("omega", "omega  obstrucao total do orador"),
                    ("g_p", "g   ORDEM PERMUTADA  (P3: tem de cair)"),
                    ("mu_p", "mu  ORDEM PERMUTADA  (P3: tem de cair)"),
                    ("d_p", "d   ORDEM PERMUTADA  (P3: tem de cair)")]:
        v = jj[c].fillna(0).to_numpy(float)
        print(f"  {nome:44s} {E0.auc(y, v):7.4f}")
    print("\n  P3 — pareado real vs ORDEM PERMUTADA:")
    for c in ("g", "mu", "d"):
        mu_, lo, hi = dcl(jj[c].fillna(0).to_numpy(float),
                          jj[c + "_p"].fillna(0).to_numpy(float))
        st = "  *" if (lo > 0 or hi < 0) else ""
        print(f"    {c:6s} {mu_:+.4f} [{lo:+.4f},{hi:+.4f}]{st}")

    E0.banner("P4 — SOMA A BASE? (OOF, GroupKFold por audiencia)")
    FAM = ["cos_s", "best_other", "share_attr", "n_spk_sup", "attr_in_sup",
           "rank_spk", "nli_s", "nli_g", "delta_n"]
    HOD = ["h_att", "g_att", "phi_spk", "r_spk", "h_norm", "phi_op"]
    CON = ["g", "mu", "d", "omega"]
    Xf = np.hstack([h7[FAM].fillna(0).to_numpy(float),
                    sub[["n_irm"]].fillna(0).to_numpy(float)])
    Xh = np.hstack([sub[HOD].fillna(0).to_numpy(float),
                    dup[["dup"]].to_numpy(float)])
    Xc = jj[CON].fillna(0).to_numpy(float)
    Xcp = jj[[c + "_p" for c in ("g", "mu", "d")] + ["omega_p"]] \
        .fillna(0).to_numpy(float)
    z_b = oof(Xf)
    z_bh = oof(np.hstack([Xf, Xh]))
    z_c = oof(Xc)
    z_bc = oof(np.hstack([Xf, Xc]))
    z_all = oof(np.hstack([Xf, Xh, Xc]))
    z_allp = oof(np.hstack([Xf, Xh, Xcp]))
    print(f"  base (familia H6/H7 + n_irm) ...... {E0.auc(y, z_b):.4f}")
    print(f"  base + Hodge/dup (fase I) ......... {E0.auc(y, z_bh):.4f}")
    print(f"  so a camada de CONTINUIDADE ....... {E0.auc(y, z_c):.4f}")
    print(f"  base + CONTINUIDADE ............... {E0.auc(y, z_bc):.4f}")
    print(f"  base + Hodge + CONTINUIDADE ....... {E0.auc(y, z_all):.4f}")
    print(f"  ... com a ordem PERMUTADA (contr.). {E0.auc(y, z_allp):.4f}")
    print()
    for nome, a, b in [("base+cont vs base", z_bc, z_b),
                       ("TUDO vs base", z_all, z_b),
                       ("TUDO vs base+Hodge", z_all, z_bh),
                       ("P3' TUDO vs ORDEM PERMUTADA", z_all, z_allp)]:
        mu_, lo, hi = dcl(a, b)
        st = "  *" if (lo > 0 or hi < 0) else ""
        print(f"  {nome:34s} {mu_:+.4f} [{lo:+.4f},{hi:+.4f}]{st}")

    E0.banner("P5 — SOMA AO COMITE DOS 12? (a aposta)")
    JU = [j for j in H6.JUIZES if j in sub and sub[j].notna().sum() > 3000]
    Xj = sub[JU].fillna(0).to_numpy(float)
    z_com = oof(Xj)
    z_cc = oof(np.hstack([Xj, Xc]))
    z_cf = oof(np.hstack([Xj, Xf]))
    z_cfc = oof(np.hstack([Xj, Xf, Xc]))
    z_cfhc = oof(np.hstack([Xj, Xf, Xh, Xc]))
    z_cfcp = oof(np.hstack([Xj, Xf, Xcp]))
    print(f"  comite dos 12 (pesos OOF) ......... {E0.auc(y, z_com):.4f}  (h6c: 0.9245)")
    print(f"  comite + CONTINUIDADE ............. {E0.auc(y, z_cc):.4f}")
    print(f"  comite + familia .................. {E0.auc(y, z_cf):.4f}")
    print(f"  comite + familia + CONTINUIDADE ... {E0.auc(y, z_cfc):.4f}")
    print(f"  comite + familia + Hodge + cont ... {E0.auc(y, z_cfhc):.4f}")
    print(f"  ... com a ordem PERMUTADA (contr.). {E0.auc(y, z_cfcp):.4f}")
    print()
    for nome, a, b in [("comite+cont vs comite", z_cc, z_com),
                       ("comite+fam vs comite", z_cf, z_com),
                       ("comite+fam+cont vs comite", z_cfc, z_com),
                       ("comite+fam+cont vs comite+fam", z_cfc, z_cf),
                       ("comite+tudo vs comite", z_cfhc, z_com),
                       ("P3'' comite+fam+cont vs PERMUTADA", z_cfc, z_cfcp)]:
        mu_, lo, hi = dcl(a, b)
        st = "  *" if (lo > 0 or hi < 0) else ""
        print(f"  {nome:36s} {mu_:+.4f} [{lo:+.4f},{hi:+.4f}]{st}")

    print()
    print(f"  {'juiz':24s} {'sozinho':>8s} {'+fam':>8s} {'+fam+cont':>10s}")
    print("  " + "-" * 54)
    melhor = ("", 0.0)
    for j in JU:
        vj = sub[j].fillna(0).to_numpy(float).reshape(-1, 1)
        a0 = E0.auc(y, vj.ravel())
        a1 = E0.auc(y, oof(np.hstack([vj, Xf])))
        a2 = E0.auc(y, oof(np.hstack([vj, Xf, Xc])))
        if a2 > melhor[1]:
            melhor = (j, a2)
        print(f"  {j:24s} {a0:8.4f} {a1:8.4f} {a2:10.4f}")
    print(f"\n  melhor a 1 chamada: {melhor[0]} + fam + cont = {melhor[1]:.4f}")
    print(f"\ngravado: {E0.OUT / 'j1_continuidade.csv'}")


if __name__ == "__main__":
    main()

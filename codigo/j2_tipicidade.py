"""J2 — TIPICIDADE ENTRE AUDIÊNCIAS: a fonte que o juiz NÃO PODE ver.

O diagnóstico das fases I e J1: toda estrutura testada era função da matriz M da
PRÓPRIA audiência — e os juízes LLM também leem a própria audiência. Acoplamento
novo, informação nenhuma.

A fonte exógena que resta é de outra natureza: **o corpus**. Um juiz recebe
(uma opinião, uma transcrição). Ele NÃO PODE saber que a mesma formulação aparece
no resumo de outras 30 audiências. Nós podemos: são 4.238 opiniões e 206
audiências, e a comparação custa um produto de matrizes.

A HIPÓTESE. Quando o sumarizador tem conteúdo, ele escreve o específico daquela
audiência. Quando não tem, ele recua para a formulação genérica que serve a
qualquer audiência ("destacou a importância do debate", "defendeu a necessidade de
maior fiscalização"). Alucinação é, em parte, REGRESSÃO AO TEMPLATE — e o template
é visível apenas de fora da audiência.

O OBJETO, e é topológico de verdade: seja π : O → H o mapa opinião → audiência
sobre a nuvem das 4.238 opiniões. Uma opinião FUNDAMENTADA tem vizinhança
concentrada na PRÓPRIA fibra π⁻¹(h) — o mapa é localmente separado ali. Uma
opinião GENÉRICA tem vizinhança atravessando muitas fibras. A fração da vizinhança
que sai da própria fibra é exatamente a falha de separação local do recobrimento
por audiências.

Também caracteriza ONDE O COMITÊ ERRA, para saber se sobrou informação.

    python j2_tipicidade.py
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
KS = (1, 5, 20, 50)


def coletar():
    import pandas as pd
    embs, metas = [], []
    for ri, r in enumerate(R.refs_ok()):
        g, ge = R.opinions(r), R.op_emb(r)
        if ge is None or len(g) != len(ge):
            continue
        rot = np.array([not pd.isna(v) for v in g.alucinacao_manual])
        gi = np.where(rot)[0]
        if not len(gi):
            continue
        embs.append(ge[gi])
        for i in gi:
            metas.append({"ref": r, "hall": int(bool(g.alucinacao_manual.iloc[i])),
                          "envolvido": (g.envolvido.iloc[i]
                                        if "envolvido" in g else None)})
        if (ri + 1) % 50 == 0:
            print(f"  {ri+1}/206 · {len(metas)} opinioes", flush=True)
    E = np.vstack(embs).astype(np.float32)
    E /= np.linalg.norm(E, axis=1, keepdims=True) + 1e-9
    Mt = pd.DataFrame(metas)
    print(f"  nuvem: {E.shape}", flush=True)

    aud = Mt.ref.to_numpy()
    S = E @ E.T
    np.fill_diagonal(S, -1.0)
    mesma = aud[:, None] == aud[None, :]
    fora = S.copy()
    fora[mesma] = -1.0                    # so vizinhos de OUTRAS audiencias
    dentro = S.copy()
    dentro[~mesma] = -1.0                 # so vizinhos da PROPRIA audiencia

    for k in KS:
        Mt[f"tip{k}"] = np.sort(fora, axis=1)[:, -k:].mean(1)
    Mt["tip_dentro"] = np.sort(dentro, axis=1)[:, -5:].mean(1)
    # separacao local da fibra: fracao dos K vizinhos GLOBAIS que sao da propria
    # audiencia. Alta = a opiniao e especifica daquela audiencia.
    for k in (10, 30):
        viz = np.argsort(-S, axis=1)[:, :k]
        Mt[f"fibra{k}"] = np.array([mesma[i, viz[i]].mean()
                                    for i in range(len(S))])
    Mt["margem"] = Mt.tip_dentro - Mt.tip5
    Mt.to_csv(E0.OUT / "j2_tipicidade.csv", index=False)
    return Mt


def main() -> None:
    import pandas as pd
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import GroupKFold
    from sklearn.preprocessing import StandardScaler

    cam = E0.OUT / "j2_tipicidade.csv"
    Mt = pd.read_csv(cam) if cam.exists() else coletar()
    Di = pd.read_csv(E0.OUT / "i2_hodge.csv")
    Dj = pd.read_csv(E0.OUT / "j1_continuidade.csv")
    Dd = pd.read_csv(E0.OUT / "i3_dup.csv")
    h7 = pd.read_csv(E0.OUT / "h7_nli_orador.csv")
    assert len(Mt) == len(Di), f"j2={len(Mt)} vs i2={len(Di)}"
    assert (Mt.hall.to_numpy() == Di.hall.to_numpy()).all(), "rotulos desalinhados"
    assert (Mt.ref.to_numpy() == Di.ref.to_numpy()).all(), "refs desalinhadas"
    print("  [ok] alinhamento verificado linha a linha")

    yall = Mt.hall.to_numpy().astype(bool)
    gall = Mt.ref.to_numpy()
    rng = np.random.default_rng(SEED)

    E0.banner("A TIPICIDADE CARREGA SINAL? (n=4238, TODAS as opinioes)")
    print(f"  {'feature':46s} {'AUROC':>7s}")
    print("  " + "-" * 56)
    tipf = [(f"tip{k}", +1, f"tip{k}   sim. media aos {k} vizinhos DE FORA")
            for k in KS]
    tipf += [("tip_dentro", -1, "tip_dentro  sim. aos 5 vizinhos DE DENTRO"),
             ("fibra10", -1, "fibra10  fracao dos 10 vizinhos na propria aud."),
             ("fibra30", -1, "fibra30  fracao dos 30 vizinhos na propria aud."),
             ("margem", -1, "margem = dentro - fora (especificidade)")]
    for c, sg, nome in tipf:
        print(f"  {nome:46s} {E0.auc(yall, Mt[c].to_numpy(float)*sg):7.4f}")
    print()
    print(f"  alucinada:     tip5 {Mt[Mt.hall==1].tip5.mean():.4f} · "
          f"fibra10 {Mt[Mt.hall==1].fibra10.mean():.3f}")
    print(f"  nao-alucinada: tip5 {Mt[Mt.hall==0].tip5.mean():.4f} · "
          f"fibra10 {Mt[Mt.hall==0].fibra10.mean():.3f}")

    # ---------------- combinacoes no subconjunto casado
    Mk = Di.sem_turno.to_numpy() == 0
    sub, jj, dup, tp = (Di[Mk].reset_index(drop=True), Dj[Mk].reset_index(drop=True),
                        Dd[Mk].reset_index(drop=True), Mt[Mk].reset_index(drop=True))
    y = sub.hall.to_numpy().astype(bool)
    gm = sub.ref.to_numpy()

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

    def oof(X, yy=None, gg=None):
        yy = y if yy is None else yy
        gg = gm if gg is None else gg
        z = np.zeros(len(yy))
        for tr, te in GroupKFold(5).split(X, yy, gg):
            sc = StandardScaler().fit(X[tr])
            c = LogisticRegression(max_iter=3000, class_weight="balanced")
            c.fit(sc.transform(X[tr]), yy[tr])
            z[te] = c.predict_proba(sc.transform(X[te]))[:, 1]
        return z

    FAM = ["cos_s", "best_other", "share_attr", "n_spk_sup", "attr_in_sup",
           "rank_spk", "nli_s", "nli_g", "delta_n"]
    HOD = ["h_att", "g_att", "phi_spk", "r_spk", "h_norm", "phi_op"]
    CON = ["g", "mu", "d", "omega"]
    TIP = [f"tip{k}" for k in KS] + ["tip_dentro", "fibra10", "fibra30", "margem"]
    Xf = np.hstack([h7[FAM].fillna(0).to_numpy(float),
                    sub[["n_irm"]].fillna(0).to_numpy(float)])
    Xh = np.hstack([sub[HOD].fillna(0).to_numpy(float),
                    dup[["dup"]].to_numpy(float)])
    Xc = jj[CON].fillna(0).to_numpy(float)
    Xt = tp[TIP].fillna(0).to_numpy(float)

    E0.banner("SOMA A BASE? (OOF, GroupKFold por audiencia, n=3630)")
    z_b = oof(Xf)
    z_t = oof(Xt)
    z_bt = oof(np.hstack([Xf, Xt]))
    z_all = oof(np.hstack([Xf, Xh, Xc, Xt]))
    print(f"  base (familia H6/H7 + n_irm) ...... {E0.auc(y, z_b):.4f}")
    print(f"  so TIPICIDADE ..................... {E0.auc(y, z_t):.4f}")
    print(f"  base + TIPICIDADE ................. {E0.auc(y, z_bt):.4f}")
    print(f"  base + Hodge + cont + TIPICIDADE .. {E0.auc(y, z_all):.4f}")
    for nome, a, b in [("base+tip vs base", z_bt, z_b),
                       ("TUDO vs base", z_all, z_b)]:
        mu_, lo, hi = dcl(a, b)
        st = "  *" if (lo > 0 or hi < 0) else ""
        print(f"  {nome:34s} {mu_:+.4f} [{lo:+.4f},{hi:+.4f}]{st}")

    E0.banner("A APOSTA — SOMA AO COMITE DOS 12?")
    JU = [j for j in H6.JUIZES if j in sub and sub[j].notna().sum() > 3000]
    Xj = sub[JU].fillna(0).to_numpy(float)
    z_com = oof(Xj)
    z_ct = oof(np.hstack([Xj, Xt]))
    z_cf = oof(np.hstack([Xj, Xf]))
    z_cft = oof(np.hstack([Xj, Xf, Xt]))
    z_call = oof(np.hstack([Xj, Xf, Xh, Xc, Xt]))
    print(f"  comite dos 12 (pesos OOF) ......... {E0.auc(y, z_com):.4f}")
    print(f"  comite + TIPICIDADE ............... {E0.auc(y, z_ct):.4f}")
    print(f"  comite + familia .................. {E0.auc(y, z_cf):.4f}")
    print(f"  comite + familia + TIPICIDADE ..... {E0.auc(y, z_cft):.4f}")
    print(f"  comite + TUDO ..................... {E0.auc(y, z_call):.4f}")
    print()
    for nome, a, b in [("comite+tip vs comite", z_ct, z_com),
                       ("comite+fam+tip vs comite", z_cft, z_com),
                       ("comite+fam+tip vs comite+fam", z_cft, z_cf),
                       ("comite+TUDO vs comite", z_call, z_com)]:
        mu_, lo, hi = dcl(a, b)
        st = "  *" if (lo > 0 or hi < 0) else ""
        print(f"  {nome:36s} {mu_:+.4f} [{lo:+.4f},{hi:+.4f}]{st}")

    E0.banner("ONDE O COMITE ERRA — sobrou informacao?")
    err = (z_com > np.quantile(z_com, 1 - y.mean())) != y
    print(f"  taxa de erro do comite (no limiar da prevalencia): {err.mean():.1%}")
    print(f"  {'feature':30s} {'AUROC de prever o ERRO do comite':>34s}")
    print("  " + "-" * 66)
    for nome, v in [("tip5", tp.tip5.to_numpy(float)),
                    ("fibra10", -tp.fibra10.to_numpy(float)),
                    ("cos_s", -sub.cos_s.to_numpy(float)),
                    ("h_att", sub.h_att.to_numpy(float)),
                    ("mu (continuidade)", jj.mu.fillna(0).to_numpy(float)),
                    ("dup", dup.dup.to_numpy(float))]:
        print(f"  {nome:30s} {E0.auc(err, v):34.4f}")
    print(f"\ngravado: {E0.OUT / 'j2_tipicidade.csv'}")


if __name__ == "__main__":
    main()

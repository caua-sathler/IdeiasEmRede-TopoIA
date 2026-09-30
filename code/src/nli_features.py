"""H7 — NLI NOS TURNOS DO ORADOR: trocar o pareador fraco pelo forte.

O h6 estabeleceu a incidência por orador com o COSSENO (0,7455/0,7605). O NLI é
pareador melhor (global: 0,598–0,676 contra 0,563 do cosseno). Este script mede a
família condicionada com mDeBERTa:

    nli_s    max P(entail) frase->opiniao nas top-5 frases DO ORADOR
    nli_g    max P(entail) nas top-5 frases GLOBAIS (mesmo orçamento)
    delta_n  nli_g - nli_s (má-atribuição em NLI)

PREDIÇÕES REGISTRADAS: (i) nli_s > cos_s (0,7455); (ii) nli_s > nli_g pareado;
(iii) a família completa (cosseno + NLI) supera 0,7605; (iv) o ensemble com juízes
sobe junto. Inferência agrupada por audiência; combinações OOF.

    python nli_features.py     # retomável (checkpoint por lote)
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import common as E0            # noqa: E402
import dataset_readers as R           # noqa: E402
import speaker_incidence as H6            # noqa: E402

warnings.filterwarnings("ignore")
NPZ = E0.CACHE / "nli_pairs.npz"
CHARS = 280
TOPK = 5
SEED = 42


def main() -> None:
    import pandas as pd

    linhas = []
    pares: list[tuple[str, str]] = []
    pidx: dict[tuple[str, str], int] = {}

    def pid(a: str, b: str) -> int:
        k = (a, b)
        if k not in pidx:
            pidx[k] = len(pares)
            pares.append(k)
        return pidx[k]

    refs = R.refs_ok()
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
        idx_spk = {c: np.where(spk == c)[0] for c in cands}
        S = ge @ Tm.T
        for i in range(len(g)):
            lab = g.alucinacao_manual.iloc[i]
            if pd.isna(lab):
                continue
            quem = g.envolvido.iloc[i] if "envolvido" in g else None
            m = H6.match_gold(quem, cands) if quem is not None else None
            if m is None:
                continue
            op = str(g.opiniao.iloc[i])[:CHARS]
            js = idx_spk[m]
            top_s = js[np.argsort(-S[i, js])[:TOPK]]
            top_g = np.argsort(-S[i])[:TOPK]
            row = {"ref": r, "hall": int(bool(lab)),
                   "ps": [pid(str(fr[c])[:CHARS], op) for c in top_s],
                   "pg": [pid(str(fr[c])[:CHARS], op) for c in top_g]}
            for j in H6.JUIZES:
                if j in g and not pd.isna(g[j].iloc[i]):
                    row[j] = int(bool(g[j].iloc[i]))
            linhas.append(row)
        if (ri + 1) % 60 == 0:
            print(f"  {ri+1}/{len(refs)} · pares unicos {len(pares)}",
                  flush=True)
    print(f"opinioes: {len(linhas)} · pares NLI unicos: {len(pares)}",
          flush=True)

    # ---- NLI retomável
    ent = np.full(len(pares), -1.0, np.float32)
    feito = 0
    if NPZ.exists():
        z = np.load(NPZ)
        if int(z["k"]) == len(pares):
            ent = z["ent"].copy()
            feito = int(z["feito"])
            print(f"cache nli_pairs.npz: {feito}/{len(pares)}", flush=True)
    if feito < len(pares):
        import nli_runner
        nli_runner.NLI_BATCH = 64
        nli = nli_runner.make_nli()
        if nli is None:
            print("[ERRO] NLI indisponivel."); return
        LOTE = 4096
        for s in range(feito, len(pares), LOTE):
            pr = nli(pares[s:s + LOTE])
            ent[s:s + len(pr)] = pr[:, 0]
            feito = s + len(pr)
            np.savez(NPZ, ent=ent, k=len(pares), feito=feito)
            print(f"  NLI {feito}/{len(pares)}", flush=True)

    D = pd.DataFrame([{**{k: v for k, v in r.items()
                          if k not in ("ps", "pg")},
                       "nli_s": float(ent[r["ps"]].max()),
                       "nli_g": float(ent[r["pg"]].max())}
                      for r in linhas])
    D["delta_n"] = D.nli_g - D.nli_s
    # junta as features do incidence_features.py (mesma ordem de construcao)
    C6 = pd.read_csv(E0.OUT / "incidence_features.csv")
    assert len(C6) == len(D) and (C6.ref.to_numpy() == D.ref.to_numpy()).all()
    for c in ["cos_s", "best_other", "share_attr", "n_spk_sup",
              "attr_in_sup", "rank_spk"]:
        D[c] = C6[c]
    D.to_csv(E0.OUT / "nli_features.csv", index=False)

    y = D.hall.to_numpy().astype(bool)
    grupos = D.ref.to_numpy()
    rng = np.random.default_rng(SEED)

    def dauc(a, b, yy, gg, nb=3000):
        uref = np.unique(gg)
        out = []
        for _ in range(nb):
            sel = uref[rng.integers(0, len(uref), len(uref))]
            idx = np.concatenate([np.where(gg == u)[0] for u in sel])
            if len(np.unique(yy[idx])) < 2:
                continue
            out.append(E0.auc(yy[idx], a[idx]) - E0.auc(yy[idx], b[idx]))
        out = np.array(out)
        return out.mean(), *np.percentile(out, [2.5, 97.5])

    E0.banner("(i)/(ii) — NLI CONDICIONADO vs COSSENO E vs GLOBAL")
    print(f"  {'feature':30s} {'AUROC':>7s}")
    print("  " + "-" * 40)
    for c, sg in [("cos_s", -1), ("nli_g", -1), ("nli_s", -1), ("delta_n", +1)]:
        print(f"  {c:30s} {E0.auc(y, sg * D[c].to_numpy(float)):7.4f}")
    for nome, a, b in [("nli_s vs cos_s", -D.nli_s, -D.cos_s),
                       ("nli_s vs nli_g", -D.nli_s, -D.nli_g)]:
        mu, lo, hi = dauc(a.to_numpy(float), b.to_numpy(float), y, grupos)
        st = "  *" if lo > 0 else ""
        print(f"  pareado {nome:24s} {mu:+.4f} [{lo:+.4f},{hi:+.4f}]{st}")

    E0.banner("(iii) — A FAMILIA COMPLETA (OOF por audiencia)")
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import GroupKFold
    from sklearn.preprocessing import StandardScaler

    def oof(cols):
        X = D[cols].to_numpy(float)
        o = np.zeros(len(D))
        for tr, te in GroupKFold(5).split(X, y, grupos):
            sc = StandardScaler().fit(X[tr])
            clf = LogisticRegression(max_iter=2000, class_weight="balanced")
            clf.fit(sc.transform(X[tr]), y[tr])
            o[te] = clf.predict_proba(sc.transform(X[te]))[:, 1]
        return o

    C6F = ["cos_s", "best_other", "share_attr", "n_spk_sup",
           "attr_in_sup", "rank_spk"]
    o_h6 = oof(C6F)
    o_h7 = oof(C6F + ["nli_s", "nli_g", "delta_n"])
    a6, a7 = E0.auc(y, o_h6), E0.auc(y, o_h7)
    mu, lo, hi = dauc(o_h7, o_h6, y, grupos)
    st = "  *" if lo > 0 else ""
    print(f"  familia (cosseno) (cosseno) ........ {a6:.4f}")
    print(f"  familia (cosseno) + NLI orador ..... {a7:.4f}")
    print(f"  pareado: {mu:+.4f} [{lo:+.4f},{hi:+.4f}]{st}")

    E0.banner("(iv) — ENSEMBLE COM OS JUIZES (postos, agrupado)")
    import scipy.stats as sst
    ganhos = []
    for j in H6.JUIZES:
        if j not in D or D[j].notna().sum() < 3000:
            continue
        Jm = D[j].notna().to_numpy()
        yj, gj = y[Jm], grupos[Jm]
        juiz = D[j][Jm].to_numpy(float)
        ens = sst.rankdata(juiz) + sst.rankdata(o_h7[Jm])
        a_j, a_e = E0.auc(yj, juiz), E0.auc(yj, ens)
        mu, lo, hi = dauc(ens, juiz, yj, gj, nb=1200)
        ganhos.append((j, a_j, a_e, mu, lo, hi))
    melhor = max(ganhos, key=lambda t: t[2])
    n_sig = sum(1 for t in ganhos if t[4] > 0)
    for j, a_j, a_e, mu, lo, hi in ganhos[:4]:
        print(f"  {j:26s} {a_j:.4f} -> {a_e:.4f}  {mu:+.4f} "
              f"[{lo:+.4f},{hi:+.4f}]")
    print(f"  ... ({n_sig}/{len(ganhos)} juizes com IC excluindo zero)")
    print(f"  MELHOR ENSEMBLE: {melhor[0]} -> {melhor[2]:.4f} "
          f"(sem a camada estrutural)")

    E0.banner("COMITE DOS 12 (pesos OOF) + familia h7")
    J12 = [j for j in H6.JUIZES if j in D]
    M12 = D[J12].notna().all(axis=1).to_numpy()
    Dm = D[M12].reset_index(drop=True)
    yj, gj = y[M12], grupos[M12]

    def oof_m(cols):
        X = Dm[cols].to_numpy(float)
        o = np.zeros(len(Dm))
        for tr, te in GroupKFold(5).split(X, yj, gj):
            sc = StandardScaler().fit(X[tr])
            clf = LogisticRegression(max_iter=2000, class_weight="balanced")
            clf.fit(sc.transform(X[tr]), yj[tr])
            o[te] = clf.predict_proba(sc.transform(X[te]))[:, 1]
        return o

    o_c = oof_m(J12)
    o_ct = oof_m(J12 + C6F + ["nli_s", "nli_g", "delta_n"])
    mu, lo, hi = dauc(o_ct, o_c, yj, gj)
    st = "  *" if lo > 0 else ""
    print(f"  comite: {E0.auc(yj, o_c):.4f} · comite + familia h7: "
          f"{E0.auc(yj, o_ct):.4f} · pareado {mu:+.4f} "
          f"[{lo:+.4f},{hi:+.4f}]{st}")
    print(f"\ngravado: {E0.OUT / 'nli_features.csv'}")


if __name__ == "__main__":
    main()

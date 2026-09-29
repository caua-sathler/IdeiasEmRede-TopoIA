"""H6c — A CAMADA ESTRUTURAL: a relação de Dowker oradores × opiniões.

O h6/h6b estabeleceram o ESCALAR (cos no orador atribuído, 0,7455; controles ok).
Este script pergunta se a ESTRUTURA da relação de suporte — quem mais sustenta a
opinião, quanto do suporte pertence ao orador atribuído, quão longe o atribuído
está do topo — soma além do escalar. E fecha o placar: o ensemble soma a CADA um
dos 12 juízes LLM, ou só ao melhor?

Features da relação R ⊆ oradores × opiniões (suporte a nível de turno):
    cos_s        max cos nos turnos do atribuído (o escalar do h6)
    best_other   max cos nos turnos de QUALQUER outro orador
    share_attr   fração da massa de suporte (top-10 frases) no atribuído
    n_spk_sup    nº de oradores com alguma frase >= 0,65 (largura do coro)
    attr_in_sup  o atribuído pertence ao recobrimento de suporte? (Dowker)
    rank_spk     posto do atribuído entre oradores (por melhor frase)

    python h6c_dowker_oradores.py
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
TAU_SUP = 0.65


def main() -> None:
    import pandas as pd

    linhas = []
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
            best_por_spk = {c: float(S[i, j].max()) for c, j in idx_spk.items()
                            if len(j)}
            cos_s = best_por_spk[m]
            outros = [v for c, v in best_por_spk.items() if c != m]
            best_other = max(outros) if outros else 0.0
            # massa de suporte: top-10 frases globais, fração no atribuído
            top = np.argsort(-S[i])[:10]
            massa = S[i, top]
            e_attr = np.isin(top, idx_spk[m])
            share = float(massa[e_attr].sum() / max(massa.sum(), 1e-9))
            sup = [c for c, v in best_por_spk.items() if v >= TAU_SUP]
            ordem = sorted(best_por_spk.values(), reverse=True)
            rank_spk = ordem.index(cos_s) / max(len(ordem) - 1, 1)
            row = {"ref": r, "hall": int(bool(lab)),
                   "cos_s": cos_s, "best_other": best_other,
                   "delta2": best_other - cos_s,
                   "share_attr": share,
                   "n_spk_sup": len(sup),
                   "attr_in_sup": int(m in sup),
                   "rank_spk": rank_spk}
            for j in H6.JUIZES:
                if j in g and not pd.isna(g[j].iloc[i]):
                    row[j] = int(bool(g[j].iloc[i]))
            linhas.append(row)
        if (ri + 1) % 60 == 0:
            print(f"  {ri+1}/{len(refs)}", flush=True)

    D = pd.DataFrame(linhas)
    D.to_csv(E0.OUT / "h6c_dowker.csv", index=False)
    y = D.hall.to_numpy().astype(bool)
    grupos = D.ref.to_numpy()
    rng = np.random.default_rng(SEED)
    print(f"\nopinioes: {len(D)} · alucinadas: {int(y.sum())}")

    E0.banner("FEATURES ESTRUTURAIS — sozinhas")
    for c, sg in [("cos_s", -1), ("best_other", -1), ("delta2", +1),
                  ("share_attr", -1), ("n_spk_sup", -1), ("attr_in_sup", -1),
                  ("rank_spk", +1)]:
        print(f"  {c:14s} {E0.auc(y, sg * D[c].to_numpy(float)):7.4f}")

    def dauc_cluster(a, b, yy, gg, nb=3000):
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

    E0.banner("ESTRUTURA SOMA AO ESCALAR? (OOF, GroupKFold por audiencia)")
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

    o_esc = oof(["cos_s"])
    o_tudo = oof(["cos_s", "best_other", "share_attr", "n_spk_sup",
                  "attr_in_sup", "rank_spk"])
    a1, a2 = E0.auc(y, o_esc), E0.auc(y, o_tudo)
    mu, lo, hi = dauc_cluster(o_tudo, o_esc, y, grupos)
    st = "  *" if lo > 0 else ""
    print(f"  so o escalar (cos_s) ......... {a1:.4f}")
    print(f"  escalar + estrutura Dowker ... {a2:.4f}")
    print(f"  pareado: {mu:+.4f} [{lo:+.4f},{hi:+.4f}]{st}")

    E0.banner("O PLACAR COMPLETO — ensemble com CADA juiz (postos, agrupado)")
    import scipy.stats as sst
    ganhos = []
    print(f"  {'juiz':26s} {'sozinho':>8s} {'+orador':>8s} "
          f"{'delta':>8s} {'IC95':>20s}")
    print("  " + "-" * 76)
    for j in H6.JUIZES:
        if j not in D or D[j].notna().sum() < 3000:
            continue
        J = D[j].notna().to_numpy()
        yj, gj = y[J], grupos[J]
        juiz = D[j][J].to_numpy(float)
        feat = o_tudo[J]
        ens = sst.rankdata(juiz) + sst.rankdata(feat)
        a_j, a_e = E0.auc(yj, juiz), E0.auc(yj, ens)
        mu, lo, hi = dauc_cluster(ens, juiz, yj, gj, nb=1500)
        st = "*" if lo > 0 else " "
        ganhos.append((a_j, a_e, lo > 0))
        print(f"  {j:26s} {a_j:8.4f} {a_e:8.4f} {mu:+8.4f} "
              f"[{lo:+.4f},{hi:+.4f}] {st}")
    n_sig = sum(1 for _, _, s in ganhos if s)
    print(f"\n  soma com IC excluindo zero em {n_sig}/{len(ganhos)} juizes · "
          f"melhor ensemble: {max(a for _, a, _ in ganhos):.4f} "
          f"(melhor juiz sozinho: {max(a for a, _, _ in ganhos):.4f})")
    print(f"\ngravado: {E0.OUT / 'h6c_dowker.csv'}")


if __name__ == "__main__":
    main()

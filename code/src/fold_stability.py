"""J6 — ESTABILIDADE do join e o placar final.

O ganho do join é pequeno (+0,004 sobre o comitê). A regra desta linha de trabalho
é desconfiar de ganho pequeno: três regressões à média na fase F, todas na direção
favorável. Aqui n=3630 e o IC é agrupado, mas falta a fonte de variância que o IC
bootstrap NÃO captura: a atribuição de dobras do GroupKFold.

Este script repete todo o pipeline com 20 particionamentos diferentes e reporta a
DISTRIBUIÇÃO do ganho, não um ponto. Se a mediana do ganho cruzar zero, o resultado
não se sustenta.

    python fold_stability.py
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
N_REP = 20


def main() -> None:
    import pandas as pd
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import GroupKFold
    from sklearn.preprocessing import StandardScaler

    Di = pd.read_csv(E0.OUT / "opinion_table.csv")
    h7 = pd.read_csv(E0.OUT / "nli_features.csv")
    Mk = Di.sem_turno.to_numpy() == 0
    sub = Di[Mk].reset_index(drop=True)
    y = sub.hall.to_numpy().astype(bool)
    gm = sub.ref.to_numpy()
    rng = np.random.default_rng(SEED)

    FAM = ["cos_s", "best_other", "share_attr", "n_spk_sup", "attr_in_sup",
           "rank_spk", "nli_s", "nli_g", "delta_n"]
    Xf = np.hstack([h7[FAM].fillna(0).to_numpy(float),
                    sub[["n_irm"]].fillna(0).to_numpy(float)])
    JU = [j for j in H6.JUIZES if j in sub and sub[j].notna().sum() > 3000]
    V = sub[JU].fillna(0).to_numpy(float)
    base = V.sum(1)
    a_base = E0.auc(y, base)

    def oof(X, perm):
        """OOF com as audiências reatribuídas a dobras por `perm`."""
        us = np.unique(gm)
        gid = {u: i for i, u in enumerate(us[perm])}
        gg = np.array([gid[u] for u in gm])
        z = np.zeros(len(y))
        for tr, te in GroupKFold(5).split(X, y, gg):
            sc = StandardScaler().fit(X[tr])
            c = LogisticRegression(max_iter=3000, class_weight="balanced")
            c.fit(sc.transform(X[tr]), y[tr])
            z[te] = c.predict_proba(sc.transform(X[te]))[:, 1]
        return z

    E0.banner(f"ESTABILIDADE EM {N_REP} PARTICIONAMENTOS DE DOBRA")
    nus = len(np.unique(gm))
    # As quatro linhas da tabela de estabilidade do artigo. O braco
    # SOMA ADITIVA(comite, FAMILIA) e o pareado que importa: mesma informacao
    # que JOIN(comite, familia), so muda a OPERACAO. Sem ele a tabela compara
    # operacoes E conjuntos de features ao mesmo tempo.
    res = {"SOMA ADITIVA(comite, familia)": [],
           "JOIN(comite, familia)": [],
           "comite pesos OOF": []}
    for rep in range(N_REP):
        pm = rng.permutation(nus)
        zf, zv = oof(Xf, pm), oof(V, pm)
        res["SOMA ADITIVA(comite, familia)"].append(
            E0.auc(y, oof(np.hstack([V, Xf]), pm)))
        res["JOIN(comite, familia)"].append(E0.auc(y, join(base, zf)))
        res["comite pesos OOF"].append(E0.auc(y, zv))
        if (rep + 1) % 5 == 0:
            print(f"  {rep+1}/{N_REP}", flush=True)

    print(f"\n  referencia: comite (soma de votos) = {a_base:.4f}")
    print(f"  {'metodo':32s} {'mediana':>9s} {'min':>8s} {'max':>8s} "
          f"{'ganho med.':>11s} {'>base':>7s}")
    print("  " + "-" * 80)
    for nome, v in res.items():
        v = np.array(v)
        print(f"  {nome:32s} {np.median(v):9.4f} {v.min():8.4f} {v.max():8.4f} "
              f"{np.median(v)-a_base:+11.4f} {(v > a_base).mean():6.0%}")

    E0.banner("O PLACAR FINAL")
    tau, teto, _ = deficit(y, base)
    pm = np.arange(nus)
    zf = oof(Xf, pm)
    lin = [
        ("familia de incidencia H6 (custo zero)", "0", E0.auc(y, oof(
            np.hstack([h7[[c for c in FAM if not c.startswith('nli')]]
                       .fillna(0).to_numpy(float),
                       sub[["n_irm"]].to_numpy(float)]), pm))),
        ("familia H6/H7 completa", "~10 NLI", E0.auc(y, zf)),
        ("melhor juiz LLM individual", "1 LLM", max(
            E0.auc(y, sub[j].fillna(0).to_numpy(float)) for j in JU)),
        ("melhor juiz + familia, SOMA", "1 LLM", None),
        ("melhor juiz + familia, JOIN", "1 LLM", None),
        ("comite dos 12 (soma de votos)", "12 LLM", a_base),
        ("comite dos 12 (pesos OOF)", "12 LLM", E0.auc(y, oof(V, pm))),
        ("comite + familia, SOMA ADITIVA", "12 LLM", E0.auc(
            y, oof(np.hstack([V, Xf]), pm))),
        ("comite + familia, JOIN", "12 LLM", E0.auc(y, join(base, zf))),
    ]
    # os dois de 1 chamada
    melhor_j, melhor_s, melhor_i = "", 0.0, 0.0
    for j in JU:
        v = sub[j].fillna(0).to_numpy(float)
        s = E0.auc(y, oof(np.hstack([v.reshape(-1, 1), Xf]), pm))
        i_ = E0.auc(y, join(v, zf))
        if i_ > melhor_i:
            melhor_j, melhor_s, melhor_i = j, s, i_
    print(f"  {'metodo':50s} {'custo':>9s} {'AUROC':>8s}")
    print("  " + "-" * 70)
    for nome, custo, a in lin:
        if a is None:
            if "SOMA" in nome and "juiz" in nome:
                a = melhor_s
            elif "JOIN" in nome and "juiz" in nome:
                a = melhor_i
            else:
                a = float("nan")
        print(f"  {nome:50s} {custo:>9s} {a:8.4f}")
    print(f"\n  (melhor juiz para o par 1-chamada: {melhor_j})")
    # O orcamento do desempate e tau/2, NAO (1 - tau/2) - AUROC. A segunda
    # quantidade e a lacuna de JULGAMENTO do comite, e o Teorema (i) garante
    # que o lexicografico nunca a toca. Um desempatador perfeito chega a
    # AUROC + tau/2, nao a 1 - tau/2.
    print(f"  tau = {tau:.1%} · orcamento do desempate (tau/2) = {tau/2:.4f}")
    print(f"  teto de um desempatador perfeito = {a_base + tau/2:.4f} "
          f"(o limite {teto:.4f} = 1 - tau/2 inclui a lacuna de julgamento,")
    print("   que o lexicografico nao pode tocar)")


if __name__ == "__main__":
    main()

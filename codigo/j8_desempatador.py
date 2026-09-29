"""J8 — SUBIR `a2`: quanto do orçamento `τ/2` dá para capturar de fato.

O Teorema 15(iii) reduz a fusão lexicográfica a UM número:

    AUROC(lex) = AUROC(s1) + tau·(a2 - ½)        captura = 2·a2 - 1

com `a2` = AUROC do secundário RESTRITO aos pares que o primário empata. O AUROC
global do secundário não aparece. Então "melhorar a fusão" é, exatamente,
"subir `a2`" — e é só isso que este script tenta.

Baseline (j7): a2 = 0,5856, captura 17,1%, lex = 0,9300.

Duas hipóteses concorrentes, com predições diferentes (ver `j8_predicoes.md`):

  H-ajuste  o sinal existe nos estratos que detêm o orçamento, mas o modelo é
            ajustado globalmente e gasta capacidade separando o que o comitê já
            separa. Condicionar/reponderar sobe `a2`.
  H-sinal   não há sinal ali. Nada feito com as MESMAS features sobe `a2`, e o
            17% é propriedade dos dados.

O `j5` já matou a versão ingênua de H-ajuste (um modelo por classe: 0,9237,
pior — é o negativo N do artigo). Aqui vão as versões que NÃO fragmentam a
amostra, mais o diagnóstico que decide entre as duas hipóteses: o `a2` de cada
feature CRUA, sozinha, no conjunto empatado.

    python j8_desempatador.py            # dobra fixa + diagnóstico
    python j8_desempatador.py --full     # + as 20 partições e os IC pareados
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import comum as E0                          # noqa: E402
import h6_orador as H6                      # noqa: E402
from j4_reticulado import deficit, join     # noqa: E402
from j7_mecanismo import a2_global, a2_restrito   # noqa: E402

warnings.filterwarnings("ignore")
SEED = 42
N_REP = 20

FAM = ["cos_s", "best_other", "share_attr", "n_spk_sup", "attr_in_sup",
       "rank_spk", "nli_s", "nli_g", "delta_n"]


def buckets(v: np.ndarray) -> np.ndarray:
    """Estratos grossos do comitê: {0}, {1,2}, {3..11}, {12}. Escolhidos pela
    massa de pares empatados (58% / 22% / 18% / 2%), nao pelo resultado."""
    b = np.zeros(len(v), int)
    b[(v >= 1) & (v <= 2)] = 1
    b[(v >= 3) & (v <= 11)] = 2
    b[v >= 12] = 3
    return b


def massa_empate(y: np.ndarray, prim: np.ndarray) -> np.ndarray:
    """Peso do item = numero de pares empatados de que ele participa.

    Um positivo na classe c pareia com todos os negativos de c, e vice-versa.
    Somado sobre os itens, isto da 2x o numero de pares empatados: e a medida
    que a identidade do Teorema 15(iii) integra."""
    w = np.zeros(len(y))
    for c in np.unique(prim):
        m = prim == c
        npos, nneg = int(y[m].sum()), int((~y[m]).sum())
        w[m & y] = nneg
        w[m & ~y] = npos
    return w


def main() -> None:
    import pandas as pd
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import GroupKFold
    from sklearn.preprocessing import StandardScaler

    full = "--full" in sys.argv

    Di = pd.read_csv(E0.OUT / "i2_hodge.csv")
    Dd = pd.read_csv(E0.OUT / "i3_dup.csv")
    h7 = pd.read_csv(E0.OUT / "h7_nli_orador.csv")
    Mk = Di.sem_turno.to_numpy() == 0
    sub, dup = Di[Mk].reset_index(drop=True), Dd[Mk].reset_index(drop=True)
    assert len(h7) == len(sub) and np.allclose(h7.cos_s, sub.cos_s, atol=1e-6)
    print("  [ok] alinhamento verificado linha a linha")
    y = sub.hall.to_numpy().astype(bool)
    gm = sub.ref.to_numpy()
    rng = np.random.default_rng(SEED)

    NOMES = FAM + ["n_irm"]
    Xf = np.hstack([h7[FAM].fillna(0).to_numpy(float),
                    sub[["n_irm"]].fillna(0).to_numpy(float)])
    JU = [j for j in H6.JUIZES if j in sub and sub[j].notna().sum() > 3000]
    V = sub[JU].fillna(0).to_numpy(float)
    base = V.sum(1)
    a_base = E0.auc(y, base)
    tau, _, _ = deficit(y, base)

    # ------------------------------------------------------------- utilidades
    def folds(perm=None):
        """Indices (treino, teste) de 5 dobras agrupadas por audiencia."""
        g = gm
        if perm is not None:
            us = np.unique(gm)
            gid = {u: i for i, u in enumerate(us[perm])}
            g = np.array([gid[u] for u in gm])
        return list(GroupKFold(5).split(Xf, y, g))

    def oof(X, perm=None, w=None, balanced=True):
        """OOF por audiencia. `balanced=False` quando `w` ja equilibra as
        classes por si (e o caso do peso de massa-de-empate: dentro de cada
        estrato os positivos e os negativos recebem massa total identica, entao
        `class_weight` por cima reponderaria duas vezes)."""
        z = np.zeros(len(y))
        for tr, te in folds(perm):
            sc = StandardScaler().fit(X[tr])
            c = LogisticRegression(max_iter=5000,
                                   class_weight="balanced" if balanced else None)
            c.fit(sc.transform(X[tr]), y[tr], sample_weight=None if w is None
                  else w[tr])
            z[te] = c.predict_proba(sc.transform(X[te]))[:, 1]
        return z

    C_GRID = (0.003, 0.03, 0.3, 3.0)

    def _pares(Xs, idx, prim):
        """Vetores-diferenca x_p - x_n de todos os pares (pos,neg) EMPATADOS
        dentro de `idx`."""
        D = []
        for c in np.unique(prim[idx]):
            ip = idx[(prim[idx] == c) & y[idx]]
            ineg = idx[(prim[idx] == c) & ~y[idx]]
            if len(ip) and len(ineg):
                D.append((Xs[ip][:, None, :] - Xs[ineg][None, :, :])
                         .reshape(-1, Xs.shape[1]))
        return np.vstack(D) if D else None

    def _ajusta_par(D, C):
        """RankNet = logistica SEM intercepto sobre as diferencas, simetrizada
        (+D rotulado 1, -D rotulado 0). Devolve o vetor de pesos."""
        XX = np.vstack([D, -D])
        yy = np.r_[np.ones(len(D)), np.zeros(len(D))]
        m = LogisticRegression(max_iter=5000, fit_intercept=False, C=C)
        m.fit(XX, yy)
        return m.coef_.ravel()

    def oof_pares(X, prim, perm=None):
        """VARIANTE E — RankNet sobre os pares EMPATADOS: a unica variante cuja
        funcao objetivo E a quantidade do Teorema 15(iii).

        `C` e escolhido por CV INTERNA (3 dobras agrupadas, dentro do treino),
        pontuada pelo proprio `a2` — nunca no conjunto de teste. Os pares de
        treino saem so das audiencias de treino (controle 3 do registro):
        nenhum par cruza a fronteira de dobra."""
        z = np.zeros(len(y))
        for tr, te in folds(perm):
            sc = StandardScaler().fit(X[tr])
            Xs = sc.transform(X)
            # --- selecao interna de C
            gi = gm[tr]
            melhor, melhor_a2 = C_GRID[0], -1.0
            for C in C_GRID:
                vals = []
                for itr, ite in GroupKFold(min(3, len(np.unique(gi)))).split(
                        tr, y[tr], gi):
                    D = _pares(Xs, tr[itr], prim)
                    if D is None:
                        continue
                    s = Xs @ _ajusta_par(D, C)
                    msk = np.zeros(len(y), bool)
                    msk[tr[ite]] = True
                    a2v, k = 0.0, 0
                    for c in np.unique(prim[tr[ite]]):
                        a, kk = a2_restrito(y, s, msk & (prim == c))
                        if kk:
                            a2v, k = a2v + a * kk, k + kk
                    if k:
                        vals.append(a2v / k)
                if vals and np.mean(vals) > melhor_a2:
                    melhor, melhor_a2 = C, float(np.mean(vals))
            D = _pares(Xs, tr, prim)
            if D is None:
                continue
            z[te] = Xs[te] @ _ajusta_par(D, melhor)
        return z

    def resumo(nome, s, mostrar=True):
        a2, _ = a2_global(y, base, s)
        lex = E0.auc(y, join(base, s))
        if mostrar:
            print(f"  {nome:34s} {E0.auc(y, s):8.4f} {a2:8.4f} {lex:9.4f} "
                  f"{2*a2-1:9.1%}")
        return a2, lex

    # ============================================================ P1 sanidade
    E0.banner("P1 — SANIDADE: o baseline do j7")
    z_base = oof(Xf)
    print(f"  comite = {a_base:.4f} · tau = {tau:.4%} · "
          f"tau/2 = {tau/2:.4f} · teto = {a_base + tau/2:.4f}")
    print(f"\n  {'secundario':34s} {'AUROC':>8s} {'a2':>8s} {'lex':>9s} "
          f"{'captura':>9s}")
    print("  " + "-" * 74)
    a2_0, lex_0 = resumo("familia (baseline)", z_base)

    # ================================================ o diagnostico que decide
    E0.banner("O DIAGNOSTICO — `a2` de cada feature CRUA (H-ajuste vs H-sinal)")
    print("  Se alguma feature crua bater o escore ajustado (0,5856) com folga,")
    print("  o problema e de AJUSTE. Se todas ficarem em ~0,5-0,6, e de SINAL.")
    print(f"\n  {'feature':16s} {'a2 (todos empates)':>19s} "
          f"{'a2 (nivel 0)':>14s} {'a2 (nivel 1)':>14s}")
    print("  " + "-" * 68)
    m0, m1 = base == 0, base == 1
    diag = []
    for k, nome in enumerate(NOMES):
        col = Xf[:, k]
        # o sinal da feature e desconhecido a priori; reportamos a orientacao
        # que a logistica escolheria (a que da a2 >= 0,5), e marcamos qual e
        a_all, _ = a2_global(y, base, col)
        flip = a_all < 0.5
        col = -col if flip else col
        a_all, _ = a2_global(y, base, col)
        a_n0, _ = a2_restrito(y, col, m0)
        a_n1, _ = a2_restrito(y, col, m1)
        diag.append((nome, a_all, a_n0, a_n1))
        print(f"  {nome:16s}{'*' if flip else ' '} {a_all:18.4f} "
              f"{a_n0:14.4f} {a_n1:14.4f}")
    print("  (* = feature usada com sinal invertido)")
    melhor = max(diag, key=lambda t: t[1])
    print(f"\n  melhor feature crua: {melhor[0]} com a2 = {melhor[1]:.4f} "
          f"(ajustado: {a2_0:.4f})")

    # ========================================================= as 5 variantes
    E0.banner("AS VARIANTES (dobra fixa) — P2..P5")
    v = base.reshape(-1, 1)
    B = buckets(base)
    Xb = np.hstack([Xf] + [Xf * (B == b).reshape(-1, 1) for b in (1, 2, 3)])
    w_emp = massa_empate(y, base)
    print(f"  {'variante':34s} {'AUROC':>8s} {'a2':>8s} {'lex':>9s} "
          f"{'captura':>9s}")
    print("  " + "-" * 74)
    res = {"familia (baseline)": z_base}
    resumo("familia (baseline)", z_base)
    res["A  [Xf, v]"] = oof(np.hstack([Xf, v]))
    resumo("A  [Xf, v]", res["A  [Xf, v]"])
    res["B  [Xf, v, Xf*v]"] = oof(np.hstack([Xf, v, Xf * v]))
    resumo("B  [Xf, v, Xf*v]", res["B  [Xf, v, Xf*v]"])
    res["C  [Xf, Xf*bucket]"] = oof(Xb)
    resumo("C  [Xf, Xf*bucket]", res["C  [Xf, Xf*bucket]"])
    res["D  Xf, peso=massa empate"] = oof(Xf, w=w_emp, balanced=False)
    resumo("D  Xf, peso=massa empate", res["D  Xf, peso=massa empate"])
    res["D2 idem, dupla ponderacao"] = oof(Xf, w=w_emp)
    resumo("D2 idem, dupla ponderacao", res["D2 idem, dupla ponderacao"])
    res["E  par a par nos empates"] = oof_pares(Xf, base)
    resumo("E  par a par nos empates", res["E  par a par nos empates"])

    d_a = abs(a2_global(y, base, res["A  [Xf, v]"])[0] - a2_0)
    print(f"\n  P2 (inercia de A): |dA2| = {d_a:.4f} "
          f"{'-> CONFIRMADA (< 0,005)' if d_a < 0.005 else '-> FALHOU'}")

    # --- por que A machuca: o voto absorve o sinal e GIRA a direcao restante.
    # Dentro de uma classe de empate `v` e constante, entao o termo b_v·v e um
    # deslocamento constante do logito e nao reordena nada — a predicao P2 estava
    # certa quanto ao CANAL. O que ela errou foi a magnitude: o unico canal
    # disponivel (o reajuste dos outros coeficientes) e forte, e prejudicial.
    def coefs(X):
        sc = StandardScaler().fit(X)
        m = LogisticRegression(max_iter=5000, class_weight="balanced")
        m.fit(sc.transform(X), y)
        return m.coef_.ravel()

    c0, c1 = coefs(Xf), coefs(np.hstack([Xf, v]))
    n0, n1 = np.linalg.norm(c0), np.linalg.norm(c1[:-1])
    print(f"\n  o mecanismo de A, medido (ajuste em toda a amostra):")
    print(f"    ||coef(Xf)||         {n0:.3f}  ->  {n1:.3f}  ao acrescentar v")
    print(f"    |coef(v)|            {abs(c1[-1]):.3f}  "
          f"({abs(c1[-1])/n1:.1f}x a norma de toda a familia)")
    print(f"    cosseno entre as duas direcoes de Xf: {c0 @ c1[:-1]/(n0*n1):.3f}")
    print("    -> v absorve o sinal, a familia encolhe e a direcao GIRA; como v")
    print("       e constante dentro do empate, so a direcao girada ordena la.")
    print(f"  nulo do j5: um desempatador aleatorio chega a 0,9308 em 200")
    print(f"  sorteios. Qualquer lex abaixo disso numa dobra nao decide nada.")

    if not full:
        print("\n  (rode com --full para as 20 particoes e os IC pareados)")
        return

    # ==================================================== P7: o teste que vale
    E0.banner(f"P7 — O CONFRONTO: {N_REP} PARTICIONAMENTOS DE DOBRA")
    nus = len(np.unique(gm))
    variantes = {
        "familia (baseline)": lambda pm: oof(Xf, pm),
        "A  [Xf, v]": lambda pm: oof(np.hstack([Xf, v]), pm),
        "B  [Xf, v, Xf*v]": lambda pm: oof(np.hstack([Xf, v, Xf * v]), pm),
        "C  [Xf, Xf*bucket]": lambda pm: oof(Xb, pm),
        "D  Xf, peso=massa empate": lambda pm: oof(Xf, pm, w=w_emp, balanced=False),
        "E  par a par nos empates": lambda pm: oof_pares(Xf, base, pm),
    }
    acc = {k: {"a2": [], "lex": []} for k in variantes}
    guarda = {k: None for k in variantes}
    for rep in range(N_REP):
        pm = rng.permutation(nus)
        for k, f in variantes.items():
            z = f(pm)
            a2, _ = a2_global(y, base, z)
            acc[k]["a2"].append(a2)
            acc[k]["lex"].append(E0.auc(y, join(base, z)))
            if rep == 0:
                guarda[k] = z
        if (rep + 1) % 5 == 0:
            print(f"  {rep+1}/{N_REP}", flush=True)

    print(f"\n  referencia: comite = {a_base:.4f} · "
          f"teto de um desempatador perfeito = {a_base + tau/2:.4f}")
    print(f"\n  {'variante':28s} {'a2 med':>8s} {'lex med':>9s} {'min':>8s} "
          f"{'max':>8s} {'capt.':>7s} {'>base':>7s}")
    print("  " + "-" * 82)
    med_base = float(np.median(acc["familia (baseline)"]["lex"]))
    for k in variantes:
        a2v = np.array(acc[k]["a2"])
        lx = np.array(acc[k]["lex"])
        print(f"  {k:28s} {np.median(a2v):8.4f} {np.median(lx):9.4f} "
              f"{lx.min():8.4f} {lx.max():8.4f} "
              f"{2*np.median(a2v)-1:6.1%} "
              f"{(lx > med_base).mean():6.0%}")

    E0.banner("IC PAREADO (bootstrap agrupado por audiencia, 5000 reamostras)")

    def dcl(a, b, nb=5000):
        us = np.unique(gm)
        mp = {u: np.where(gm == u)[0] for u in us}
        r2 = np.random.default_rng(SEED)
        d = []
        for _ in range(nb):
            s = np.concatenate([mp[u] for u in
                                us[r2.integers(0, len(us), len(us))]])
            if len(np.unique(y[s])) < 2:
                continue
            d.append(E0.auc(y[s], a[s]) - E0.auc(y[s], b[s]))
        d = np.array(d)
        return d.mean(), *np.percentile(d, [2.5, 97.5])

    ref = join(base, guarda["familia (baseline)"])
    print(f"  {'variante':28s} {'vs baseline lex':>22s} "
          f"{'vs comite':>22s}")
    print("  " + "-" * 76)
    for k in variantes:
        if k == "familia (baseline)":
            continue
        z = join(base, guarda[k])
        m1_, l1, h1 = dcl(z, ref)
        m2_, l2, h2 = dcl(z, base)
        s1 = "*" if (l1 > 0 or h1 < 0) else " "
        s2 = "*" if (l2 > 0 or h2 < 0) else " "
        print(f"  {k:28s} {m1_:+.4f} [{l1:+.4f},{h1:+.4f}]{s1} "
              f"{m2_:+.4f} [{l2:+.4f},{h2:+.4f}]{s2}")

    E0.banner("VEREDITO")
    vencedor, ganho = None, 0.0
    for k in variantes:
        if k == "familia (baseline)":
            continue
        g = float(np.median(acc[k]["lex"])) - med_base
        if g > ganho:
            vencedor, ganho = k, g
    if vencedor is None:
        print("  Nenhuma variante bate a mediana do baseline. P7 FALHOU:")
        print("  o veredito e H-SINAL — a captura de 17% e limite de sinal e")
        print("  de tamanho de amostra, nao da operacao de fusao.")
    else:
        print(f"  Melhor: {vencedor} (+{ganho:.4f} na mediana). Confira o IC")
        print("  pareado acima: sem ele excluindo zero, P7 nao passa.")


if __name__ == "__main__":
    main()

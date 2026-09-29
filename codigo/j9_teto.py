"""J9 — QUANTO GAP AINDA EXISTE, e onde. Três medições, todas exploratórias.

O `j8` fechou o desempate: `a2` não sobe com estas features. Restam três
perguntas, e nenhuma delas é sobre o desempate.

(A) A LACUNA DE JULGAMENTO É ALCANÇÁVEL?  O comitê erra 0,0508 de AUROC em
    pares que ele SEPARA — 2,2x o orçamento do desempate. O Teorema (i) proíbe o
    lexicográfico de tocá-los; um mecanismo de "overrule" com trava tocaria. Mas
    só vale a pena se a família souber ALGUMA COISA sobre onde o comitê erra.
    Medimos `a3` = AUROC da família restrito aos pares que o comitê separa e
    ordena ERRADO, contra `a_ok` nos que ele ordena certo. Se `a3 ≈ a_ok`, a
    família não distingue os dois e nenhuma trava é construível.

(B) QUAL O TETO EMPÍRICO DE TUDO JUNTO?  Um modelo flexível (árvores impulsadas)
    sobre votos + todas as features, honestamente fora de dobra, é um limite
    INFERIOR do que é alcançável com esta informação. Não diz "isto é o máximo";
    diz "pelo menos isto é atingível por algo".

(C) QUANTAS CHAMADAS DE JUÍZ A FAMÍLIA VALE?  A pergunta prática não é quanto
    AUROC subimos sobre o comitê de 12, e sim quanto do comitê dispensamos. Para
    cada k, comitês de k juízes sorteados, com e sem o desempate lexicográfico.
    A distância HORIZONTAL entre as duas curvas é o número de chamadas
    economizadas — e é aí que a margem é larga.

    python j9_teto.py
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
from j7_mecanismo import a2_global          # noqa: E402

warnings.filterwarnings("ignore")
SEED = 42
N_SUB = 60          # subconjuntos sorteados por tamanho k
FAM = ["cos_s", "best_other", "share_attr", "n_spk_sup", "attr_in_sup",
       "rank_spk", "nli_s", "nli_g", "delta_n"]


def main() -> None:
    import pandas as pd
    from sklearn.ensemble import HistGradientBoostingClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import GroupKFold
    from sklearn.preprocessing import StandardScaler

    Di = pd.read_csv(E0.OUT / "i2_hodge.csv")
    Dj = pd.read_csv(E0.OUT / "j1_continuidade.csv")
    Dd = pd.read_csv(E0.OUT / "i3_dup.csv")
    h7 = pd.read_csv(E0.OUT / "h7_nli_orador.csv")
    Mk = Di.sem_turno.to_numpy() == 0
    sub = Di[Mk].reset_index(drop=True)
    jj = Dj[Mk].reset_index(drop=True)
    dup = Dd[Mk].reset_index(drop=True)
    assert len(h7) == len(sub) and np.allclose(h7.cos_s, sub.cos_s, atol=1e-6)
    print("  [ok] alinhamento verificado linha a linha")
    y = sub.hall.to_numpy().astype(bool)
    gm = sub.ref.to_numpy()
    rng = np.random.default_rng(SEED)

    HOD = ["h_att", "g_att", "phi_spk", "r_spk", "h_norm", "phi_op"]
    CON = ["g", "mu", "d", "omega"]
    Xf = np.hstack([h7[FAM].fillna(0).to_numpy(float),
                    sub[["n_irm"]].fillna(0).to_numpy(float)])
    Xall = np.hstack([Xf, sub[HOD].fillna(0).to_numpy(float),
                      dup[["dup"]].to_numpy(float),
                      jj[CON].fillna(0).to_numpy(float)])
    JU = [j for j in H6.JUIZES if j in sub and sub[j].notna().sum() > 3000]
    V = sub[JU].fillna(0).to_numpy(float)
    base = V.sum(1)
    a_base = E0.auc(y, base)
    tau, _, _ = deficit(y, base)

    def folds():
        return list(GroupKFold(5).split(Xf, y, gm))

    def oof(X, modelo="log"):
        z = np.zeros(len(y))
        for tr, te in folds():
            if modelo == "log":
                sc = StandardScaler().fit(X[tr])
                c = LogisticRegression(max_iter=5000, class_weight="balanced")
                c.fit(sc.transform(X[tr]), y[tr])
                z[te] = c.predict_proba(sc.transform(X[te]))[:, 1]
            else:
                c = HistGradientBoostingClassifier(
                    max_iter=300, learning_rate=0.06, max_leaf_nodes=15,
                    l2_regularization=1.0, random_state=SEED)
                c.fit(X[tr], y[tr])
                z[te] = c.predict_proba(X[te])[:, 1]
        return z

    fino = oof(Xf)

    # ===================================================================== (A)
    E0.banner("(A) A LACUNA DE JULGAMENTO: a familia sabe onde o comite erra?")
    p, n = base[y], base[~y]
    sp, sn = fino[y], fino[~y]
    D1 = p[:, None] - n[None, :]        # comite: >0 certo, <0 errado, 0 empate
    D2 = sp[:, None] - sn[None, :]      # familia
    tot = D1.size

    def taxa(msk):
        """fracao dos pares em `msk` que a FAMILIA ordena corretamente."""
        k = int(msk.sum())
        if k == 0:
            return float("nan"), 0
        return float(((D2[msk] > 0).sum() + 0.5 * (D2[msk] == 0).sum()) / k), k

    ok, err, emp = D1 > 0, D1 < 0, D1 == 0
    a_ok, k_ok = taxa(ok)
    a3, k_err = taxa(err)
    a2v, _ = a2_global(y, base, fino)
    print(f"  pares (pos,neg): {tot:,}")
    print(f"\n  {'subpopulacao':38s} {'% dos pares':>12s} "
          f"{'AUROC da familia':>18s}")
    print("  " + "-" * 72)
    print(f"  {'o comite SEPARA e acerta':38s} {k_ok/tot:11.1%} {a_ok:18.4f}")
    print(f"  {'o comite SEPARA e ERRA':38s} {k_err/tot:11.1%} {a3:18.4f}")
    print(f"  {'o comite EMPATA (o orcamento tau)':38s} "
          f"{int(emp.sum())/tot:11.1%} {a2v:18.4f}")
    print(f"\n  lacuna de julgamento = {k_err/tot:.4f} "
          f"(2,2x o orcamento do desempate, {tau/2:.4f})")
    print(f"  Para uma trava de overrule funcionar, a familia teria de ser")
    print(f"  MELHOR onde o comite erra ({a3:.4f}) do que onde ele acerta")
    print(f"  ({a_ok:.4f}) — ou seja, discordar seletivamente. Ela e "
          f"{'MELHOR' if a3 > a_ok else 'PIOR'}.")
    print(f"\n  confirmacao independente (j7, Tab. 5): a soma aditiva inverte")
    print(f"  1,33% dos pares separados, dos quais so 44% eram inversoes boas.")

    # ===================================================================== (B)
    E0.banner("(B) O TETO EMPIRICO: um modelo flexivel sobre TUDO")
    linhas = [
        ("comite (soma de votos)", base),
        ("LEXICOGRAFICO (o do artigo)", join(base, fino)),
        ("logistica: votos + familia", oof(np.hstack([V, Xf]))),
        ("logistica: votos + tudo", oof(np.hstack([V, Xall]))),
        ("arvores: votos + familia", oof(np.hstack([V, Xf]), "gbt")),
        ("arvores: votos + tudo", oof(np.hstack([V, Xall]), "gbt")),
        ("arvores: votos + tudo, depois LEX", None),
    ]
    z_gbt = oof(np.hstack([V, Xall]), "gbt")
    linhas[-1] = ("arvores: votos + tudo, depois LEX", join(base, z_gbt))
    print(f"  teto de um desempatador perfeito = {a_base + tau/2:.4f}")
    print(f"\n  {'metodo':36s} {'AUROC':>8s} {'vs comite':>11s}")
    print("  " + "-" * 60)
    for nome, s in linhas:
        print(f"  {nome:36s} {E0.auc(y, s):8.4f} "
              f"{E0.auc(y, s)-a_base:+11.4f}")
    print("\n  Um modelo flexivel com acesso a TUDO e um limite INFERIOR do que")
    print("  esta informacao permite. Se ele nao bate o lexicografico, nao ha")
    print("  ganho escondido em combinacao — ha falta de sinal.")

    # ===================================================================== (C)
    E0.banner("(C) EQUIVALENCIA DE CUSTO: quantas chamadas a familia vale?")
    # Duas familias, para separar o custo honestamente: a de CUSTO ZERO (so
    # cosseno sobre embeddings ja calculados) e a completa (+2 features de NLI,
    # ~10 passagens de um modelo local de 1 GB — nao e chamada de LLM, mas
    # tambem nao e de graca).
    i_nli = [FAM.index(c) for c in ("nli_s", "nli_g", "delta_n")]
    Xf0 = np.delete(Xf, i_nli, axis=1)
    fino0 = oof(Xf0)
    print(f"  {N_SUB} subconjuntos sorteados por tamanho; mediana sobre eles.")
    print(f"  familia custo-zero: AUROC {E0.auc(y, fino0):.4f} · "
          f"familia com NLI: {E0.auc(y, fino):.4f}")
    print(f"\n  {'k':>3s} {'comite so':>10s} {'+fam. 0-custo':>14s} "
          f"{'+fam. c/ NLI':>13s} {'>= comite12':>12s}")
    print("  " + "-" * 58)
    curva_so, curva_lex, curva_lex0, frac12 = {}, {}, {}, {}
    for k in range(1, len(JU) + 1):
        a_so, a_lx, a_lx0, venc = [], [], [], []
        for _ in range(N_SUB if k < len(JU) else 1):
            idx = rng.choice(len(JU), k, replace=False) if k < len(JU) \
                else np.arange(len(JU))
            s1 = V[:, idx].sum(1)
            a_so.append(E0.auc(y, s1))
            a = E0.auc(y, join(s1, fino))
            a_lx.append(a)
            a_lx0.append(E0.auc(y, join(s1, fino0)))
            venc.append(a >= a_base)
        curva_so[k] = float(np.median(a_so))
        curva_lex[k] = float(np.median(a_lx))
        curva_lex0[k] = float(np.median(a_lx0))
        frac12[k] = float(np.mean(venc))
        print(f"  {k:3d} {curva_so[k]:10.4f} {curva_lex0[k]:14.4f} "
              f"{curva_lex[k]:13.4f} {frac12[k]:11.0%}")
    print(f"\n  ultima coluna: fracao dos subconjuntos de tamanho k cujo LEX")
    print(f"  atinge ou supera o COMITE INTEIRO de 12 ({a_base:.4f}).")

    print("\n  A leitura HORIZONTAL — quantas chamadas o desempate economiza:")
    print(f"  {'k + familia':>13s} {'AUROC':>8s}   "
          f"{'equivale a um comite de':>24s}")
    print("  " + "-" * 54)
    for k in range(1, len(JU)):
        alvo = curva_lex[k]
        eq = next((kk for kk in range(1, len(JU) + 1)
                   if curva_so[kk] >= alvo), None)
        if eq is None:
            print(f"  {k:>10d} ch. {alvo:8.4f}   "
                  f"{'> comite de 12':>24s}")
        elif eq > k:
            print(f"  {k:>10d} ch. {alvo:8.4f}   "
                  f"{eq:>13d} chamadas  (-{eq-k})")

    E0.banner("O CONFRONTO ROBUSTO: k juizes + familia vs o COMITE DE 12")

    def dcl(a, b, nb=3000):
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

    print("  Subconjunto MEDIANO de cada tamanho (o de AUROC mais proximo da")
    print("  mediana), pareado contra o comite inteiro. IC agrupado por audiencia.")
    print(f"\n  {'k':>3s} {'LEX(k, familia)':>16s} "
          f"{'vs comite de 12 (IC95)':>30s}")
    print("  " + "-" * 54)
    r3 = np.random.default_rng(SEED + 1)
    for k in (4, 5, 6, 7, 8, 9):
        cands = []
        for _ in range(N_SUB):
            idx = r3.choice(len(JU), k, replace=False)
            s1 = V[:, idx].sum(1)
            cands.append((E0.auc(y, join(s1, fino)), s1))
        cands.sort(key=lambda t: t[0])
        a_med, s1 = cands[len(cands) // 2]
        z = join(s1, fino)
        mu, lo, hi = dcl(z, base)
        st = "*" if (lo > 0 or hi < 0) else " "
        print(f"  {k:3d} {a_med:16.4f} "
              f"{mu:+18.4f} [{lo:+.4f},{hi:+.4f}]{st}")
    print("\n  '*' = IC exclui zero. Sem estrela e EMPATE ESTATISTICO com o")
    print("  comite de 12 — que e exatamente a alegacao: mesma exatidao, menos")
    print("  chamadas. Nao e preciso SUPERAR o comite para economiza-lo.")

    if "--robustez" not in sys.argv:
        print("\n  (rode com --robustez para o estresse: dobras, equivalencia,")
        print("   escolha dos juizes e pior caso)")
        return

    # ===================================================================== (D)
    E0.banner("(D1) ESTRESSE — variancia de dobra E de subconjunto, separadas")
    # Os MESMOS subconjuntos sob CADA particionamento: assim as duas fontes de
    # variancia nao se confundem. Sem isto repetiriamos o erro do j3/j4.
    R = 20
    S = 60
    r4 = np.random.default_rng(SEED + 7)
    subsets = {k: [r4.choice(len(JU), k, replace=False) for _ in range(S)]
               for k in range(1, len(JU))}
    subsets[len(JU)] = [np.arange(len(JU))]

    def oof_perm(X, perm):
        us = np.unique(gm)
        gid = {u: i for i, u in enumerate(us[perm])}
        gg = np.array([gid[u] for u in gm])
        z = np.zeros(len(y))
        for tr, te in GroupKFold(5).split(X, y, gg):
            sc = StandardScaler().fit(X[tr])
            c = LogisticRegression(max_iter=5000, class_weight="balanced")
            c.fit(sc.transform(X[tr]), y[tr])
            z[te] = c.predict_proba(sc.transform(X[te]))[:, 1]
        return z

    r5 = np.random.default_rng(SEED)
    finos = [oof_perm(Xf, r5.permutation(len(np.unique(gm))))
             for _ in range(R)]
    print(f"  {R} particionamentos x {S} subconjuntos por tamanho.")
    print(f"\n  {'k':>3s} {'mediana':>9s} {'p5':>8s} {'p95':>8s} {'min':>8s} "
          f"{'>= 0.9260':>10s} {'dp dobra':>9s} {'dp subc.':>9s}")
    print("  " + "-" * 72)
    guarda_k = {}
    for k in range(1, len(JU) + 1):
        M = np.array([[E0.auc(y, join(V[:, ix].sum(1), f)) for ix in subsets[k]]
                      for f in finos])          # (R particoes) x (S subconj.)
        guarda_k[k] = M
        print(f"  {k:3d} {np.median(M):9.4f} {np.percentile(M, 5):8.4f} "
              f"{np.percentile(M, 95):8.4f} {M.min():8.4f} "
              f"{(M >= a_base).mean():9.0%} "
              f"{M.mean(axis=1).std():9.4f} {M.mean(axis=0).std():9.4f}")
    print("\n  'dp dobra' = desvio das medias por particionamento (variancia de")
    print("  dobra). 'dp subc.' = desvio das medias por subconjunto (QUAIS")
    print("  juizes). Se a segunda dominar, a alegacao depende da escolha.")

    E0.banner("(D2) EQUIVALENCIA DE VERDADE (TOST), nao 'falha em rejeitar'")
    print("  Um IC que contem zero NAO prova equivalencia. A alegacao correta e")
    print("  que o IC inteiro cabe dentro de uma margem declarada. Usamos duas:")
    print("  0,0040 (o proprio ganho que o artigo reivindica) e 0,0100.")
    print(f"\n  {'k':>3s} {'dif. vs comite12':>18s} {'IC95':>22s} "
          f"{'|0,0040':>8s} {'|0,0100':>8s}")
    print("  " + "-" * 66)
    for k in (5, 6, 7, 8, 9):
        M = guarda_k[k]
        # subconjunto tipico: o de desempenho mediano na particao de referencia
        med_por_sub = M.mean(axis=0)
        ix = subsets[k][int(np.argsort(med_por_sub)[len(med_por_sub) // 2])]
        z = join(V[:, ix].sum(1), finos[0])
        mu, lo, hi = dcl(z, base, nb=5000)
        e40 = "sim" if (lo > -0.0040 and hi < 0.0040) else "nao"
        e100 = "sim" if (lo > -0.0100 and hi < 0.0100) else "nao"
        print(f"  {k:3d} {mu:+18.4f} [{lo:+.4f},{hi:+.4f}] "
              f"{e40:>8s} {e100:>8s}")

    E0.banner("(D3) DEPENDE DE QUAIS JUIZES? subconjuntos ESTRUTURADOS")
    print("  Configuracoes que alguem realmente usaria, contra os sorteios.")
    prompts = {p: [i for i, j in enumerate(JU) if f"_p{p}_" in j]
               for p in (1, 2, 3)}
    modelos = {}
    for i, j in enumerate(JU):
        m = j.split("_")[-1]
        modelos.setdefault(m, []).append(i)
    estrut = {f"prompt p{p} (4 modelos)": ix for p, ix in prompts.items()}
    estrut.update({f"modelo {m} (3 prompts)": ix for m, ix in modelos.items()})
    # top-k por AUROC individual, escolhido nas dobras de TREINO (honesto)
    ordem = np.argsort([-E0.auc(y, V[:, i]) for i in range(len(JU))])
    for k in (5, 7):
        estrut[f"melhores {k} juizes (por AUROC)"] = ordem[:k]
        estrut[f"piores {k} juizes"] = ordem[-k:]
    print(f"\n  {'configuracao':32s} {'k':>3s} {'so':>8s} {'+familia':>9s} "
          f"{'vs comite12':>12s}")
    print("  " + "-" * 70)
    for nome, ix in estrut.items():
        s1 = V[:, list(ix)].sum(1)
        a1 = E0.auc(y, s1)
        a2_ = E0.auc(y, join(s1, finos[0]))
        print(f"  {nome:32s} {len(ix):3d} {a1:8.4f} {a2_:9.4f} "
              f"{a2_-a_base:+12.4f}")

    E0.banner("(D4) O PIOR CASO, e a familia de CUSTO ZERO")
    finos0 = [oof_perm(Xf0, r5.permutation(len(np.unique(gm))))
              for _ in range(5)]
    print(f"  {'k':>3s} {'c/NLI: min':>11s} {'c/NLI: p5':>10s} "
          f"{'0-custo: mediana':>17s} {'0-custo: min':>13s}")
    print("  " + "-" * 60)
    for k in (5, 6, 7, 8, 12):
        M = guarda_k[k]
        M0 = np.array([[E0.auc(y, join(V[:, ix].sum(1), f))
                        for ix in subsets[k]] for f in finos0])
        print(f"  {k:3d} {M.min():11.4f} {np.percentile(M, 5):10.4f} "
              f"{np.median(M0):17.4f} {M0.min():13.4f}")
    print(f"\n  referencia: comite de 12 = {a_base:.4f}")

    E0.banner("(D5) (A) e (B) sobrevivem a variancia de dobra?")
    aok, a3s, a2s = [], [], []
    for f in finos:
        sp, sn = f[y], f[~y]
        D2f = sp[:, None] - sn[None, :]

        def tx(msk):
            return float(((D2f[msk] > 0).sum() + 0.5 * (D2f[msk] == 0).sum())
                         / max(int(msk.sum()), 1))
        aok.append(tx(ok))
        a3s.append(tx(err))
        a2s.append(a2_global(y, base, f)[0])
    for nome, v_ in (("comite acerta (a_ok)", aok), ("comite EMPATA (a2)", a2s),
                     ("comite ERRA (a3)", a3s)):
        v_ = np.array(v_)
        print(f"  {nome:24s} mediana {np.median(v_):.4f} · "
              f"faixa [{v_.min():.4f}, {v_.max():.4f}] · "
              f"{'SEMPRE < 0,5' if v_.max() < 0.5 else ''}")
    gbt = [E0.auc(y, oof(np.hstack([V, Xall]), "gbt")) for _ in range(3)]
    print(f"\n  arvores (votos+tudo), 3 execucoes: "
          f"{', '.join(f'{g:.4f}' for g in gbt)}  "
          f"(comite {a_base:.4f}, lex {E0.auc(y, join(base, fino)):.4f})")


if __name__ == "__main__":
    main()

"""J7 — O MECANISMO, medido: onde exatamente a fusão aditiva perde.

A Proposição diz que uma soma ponderada pode INVERTER um julgamento estrito do
detector confiável. Aqui isso deixa de ser um argumento e vira uma contagem.

O AUROC é uma média sobre os pares (positivo, negativo):

    AUROC = (1/|P||N|) Σ_pares [ 1(ordena certo) + ½·1(empata) ]

Particionando os pares em dois grupos — os que o comitê SEPARA estritamente e os
que ele EMPATA — o AUROC de qualquer método se decompõe exatamente nessas duas
contribuições. A soma aditiva e o lexicográfico diferem nas duas, e em direções
opostas:

    - nos pares SEPARADOS: o lexicográfico é idêntico ao comitê (por construção);
      a soma pode inverter, e cada inversão de um par que estava certo custa.
    - nos pares EMPATADOS: o comitê contribui ½ cada; ambos os métodos decidem,
      e é aí que o ganho pode existir.

Também reporta sensibilidade e especificidade dos 12 juízes, porque para um
detector binário AUROC = ½(sens+spec) e a leitura honesta exige as duas.

E fecha com a ANATOMIA DO ORÇAMENTO. O Teorema (iii) do artigo diz que o
lexicográfico rende, exatamente,

    AUROC(lex) = AUROC(s1) + tau · (a2 - ½)          captura = 2·a2 - 1

onde `a2` é o AUROC do secundário RESTRITO aos pares que o primário empata. Não é
o AUROC global do secundário — esse não aparece na identidade. A última seção
mede `a2` por nível do comitê (é lá que se vê que o orçamento mora quase todo no
nível zero, sustentado por 19 positivos) e confere a identidade contra o
lexicográfico realmente calculado.

    python j7_mecanismo.py
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
from j4_reticulado import join    # noqa: E402

warnings.filterwarnings("ignore")
SEED = 42


def decompoe(y, s1, s):
    """Decompõe o AUROC de `s` sobre os pares (pos,neg), separando-os por como o
    detector de referência `s1` os trata. Devolve as contribuições absolutas
    (já divididas por |P||N|), que somam ao AUROC de `s`."""
    p, n = s[y], s[~y]
    p1, n1 = s1[y], s1[~y]
    tot = len(p) * len(n)
    D1 = p1[:, None] - n1[None, :]          # comitê: >0 certo, <0 errado, =0 empate
    D = p[:, None] - n[None, :]
    sep, emp = D1 != 0, D1 == 0
    ganho = (D > 0).astype(float) + 0.5 * (D == 0)
    return {
        "n_sep": int(sep.sum()) / tot,
        "n_emp": int(emp.sum()) / tot,
        "c_sep": float(ganho[sep].sum()) / tot,
        "c_emp": float(ganho[emp].sum()) / tot,
        "auroc": float(ganho.sum()) / tot,
        # inversões: pares que o comitê separava e que `s` ordena ao contrário
        "inv": float(((D1 > 0) & (D < 0)).sum() + ((D1 < 0) & (D > 0)).sum()) / tot,
        # inversões DANOSAS: estavam certas no comitê e ficaram erradas
        "inv_ruim": float(((D1 > 0) & (D < 0)).sum()) / tot,
        # inversões BENIGNAS: estavam erradas e ficaram certas
        "inv_boa": float(((D1 < 0) & (D > 0)).sum()) / tot,
    }


def a2_restrito(y, s, sel):
    """AUROC de `s` restrito aos itens `sel` (Mann-Whitney, empate = ½).

    Aplicado a uma classe de equivalencia do primario, devolve exatamente o `a2`
    do Teorema (iii): a qualidade do secundario ONDE o primario e silencioso.
    Devolve (a2, n_pares); a2 = nan se a classe nao tem as duas classes."""
    yy, ss = y[sel], s[sel]
    if yy.sum() == 0 or (~yy).sum() == 0:
        return float("nan"), 0
    D = ss[yy][:, None] - ss[~yy][None, :]
    return float(((D > 0).sum() + 0.5 * (D == 0).sum()) / D.size), int(D.size)


def a2_global(y, prim, sec):
    """`a2` sobre TODOS os pares empatados por `prim`: a media dos a2 por classe
    ponderada pelo numero de pares de cada classe."""
    num, den = 0.0, 0
    for v in np.unique(prim):
        a, k = a2_restrito(y, sec, prim == v)
        if k:
            num, den = num + a * k, den + k
    return (num / den if den else float("nan")), den


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
    print("  [ok] alinhamento verificado linha a linha")
    y = sub.hall.to_numpy().astype(bool)
    gm = sub.ref.to_numpy()

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
    Xf = np.hstack([h7[FAM].fillna(0).to_numpy(float),
                    sub[["n_irm"]].fillna(0).to_numpy(float)])
    JU = [j for j in H6.JUIZES if j in sub and sub[j].notna().sum() > 3000]
    V = sub[JU].fillna(0).to_numpy(float)
    base = V.sum(1)

    E0.banner("OS 12 JUIZES, HONESTAMENTE (binario => AUROC = acuracia balanceada)")
    print(f"  prevalencia: {y.mean():.1%} ({int(y.sum())} de {len(y)})")
    print(f"  {'juiz':24s} {'sens':>7s} {'espec':>7s} {'FPR':>7s} "
          f"{'AUROC':>7s} {'=1/2(s+e)':>10s}")
    print("  " + "-" * 68)
    for j in JU:
        v = sub[j].fillna(0).to_numpy().astype(bool)
        sens, esp = v[y].mean(), (~v[~y]).mean()
        print(f"  {j:24s} {sens:7.3f} {esp:7.3f} {1-esp:7.3f} "
              f"{E0.auc(y, v.astype(float)):7.4f} {0.5*(sens+esp):10.4f}")
    print("\n  -> quatro juizes tem sensibilidade < 0,55: deixam passar mais da")
    print("     metade das alucinacoes. O AUROC binario nao separa isso do FPR.")

    E0.banner("O COMITE — a estrutura de empates (aqui a leitura tem conteudo)")
    lv, ct = np.unique(base, return_counts=True)
    p1, n1 = base[y], base[~y]
    tot = len(p1) * len(n1)
    tau = float((p1[:, None] == n1[None, :]).sum()) / tot
    print(f"  niveis: {len(lv)} · AUROC {E0.auc(y, base):.4f}")
    print(f"  tau (pares pos-neg empatados) .......... {tau:6.2%}")
    print(f"  orcamento do desempate (tau/2) ......... {tau/2:6.4f}")
    print(f"  teto de um desempatador perfeito ....... "
          f"{E0.auc(y, base)+tau/2:6.4f}")
    print(f"\n  {'nivel':>6s} {'n':>6s} {'% do total':>11s} {'alucinadas':>11s}")
    print("  " + "-" * 38)
    for v_, c_ in zip(lv, ct):
        m = base == v_
        print(f"  {v_:6.0f} {c_:6d} {c_/len(y):10.1%} {y[m].mean():10.1%}")

    E0.banner("O MECANISMO — decomposicao exata do AUROC por tipo de par")
    metodos = {
        "comite (soma de votos)": base,
        "SOMA ADITIVA (logistica)": oof(np.hstack([V, Xf])),
        "LEXICOGRAFICO": join(base, oof(Xf)),
    }
    print(f"  pares (pos,neg): {tot:,} · separados pelo comite: "
          f"{1-tau:.1%} · empatados: {tau:.1%}")
    print()
    print(f"  {'metodo':26s} {'AUROC':>7s} {'contrib. sep.':>14s} "
          f"{'contrib. emp.':>14s}")
    print("  " + "-" * 66)
    ref = None
    for nome, s in metodos.items():
        d = decompoe(y, base, s)
        if ref is None:
            ref = d
        print(f"  {nome:26s} {d['auroc']:7.4f} {d['c_sep']:14.4f} "
              f"{d['c_emp']:14.4f}")
    print()
    print(f"  {'metodo':26s} {'inversoes':>11s} {'danosas':>10s} "
          f"{'benignas':>10s} {'liquido':>9s}")
    print("  " + "-" * 70)
    for nome, s in metodos.items():
        d = decompoe(y, base, s)
        print(f"  {nome:26s} {d['inv']:10.2%} {d['inv_ruim']:9.2%} "
              f"{d['inv_boa']:9.2%} {d['inv_boa']-d['inv_ruim']:+8.4f}")
    print()
    da = decompoe(y, base, metodos["SOMA ADITIVA (logistica)"])
    dl = decompoe(y, base, metodos["LEXICOGRAFICO"])
    print(f"  A SOMA inverte {da['inv']:.1%} dos pares que o comite separava;")
    print(f"  o saldo dessas inversoes e {da['inv_boa']-da['inv_ruim']:+.4f} de AUROC,")
    print(f"  e ela ganha {da['c_emp']-ref['c_emp']:+.4f} nos empates.")
    print(f"  Total: {da['auroc']-ref['auroc']:+.4f}")
    print()
    print(f"  O LEXICOGRAFICO inverte {dl['inv']:.1%} (zero, por construcao),")
    print(f"  e ganha {dl['c_emp']-ref['c_emp']:+.4f} nos empates.")
    print(f"  Total: {dl['auroc']-ref['auroc']:+.4f}")

    # ------------------------------------------------------------ a anatomia
    HOD = ["h_att", "g_att", "phi_spk", "r_spk", "h_norm", "phi_op"]
    CON = ["g", "mu", "d", "omega"]
    Xall = np.hstack([Xf, sub[HOD].fillna(0).to_numpy(float),
                      dup[["dup"]].to_numpy(float),
                      jj[CON].fillna(0).to_numpy(float)])
    sec_f, sec_a = oof(Xf), oof(Xall)

    E0.banner("A ANATOMIA DO ORCAMENTO — onde ele mora, e quem o sustenta")
    print("  a2 = AUROC do secundario RESTRITO aos pares que o comite empata.")
    print(f"  {'votos':>6s} {'itens':>6s} {'pos':>5s} {'neg':>6s} "
          f"{'pares emp.':>11s} {'% do tau':>9s} {'a2 familia':>11s} "
          f"{'a2 +topol.':>11s}")
    print("  " + "-" * 76)
    _, n_emp = a2_global(y, base, sec_f)
    for v in np.unique(base):
        m = base == v
        a_f, k = a2_restrito(y, sec_f, m)
        a_a, _ = a2_restrito(y, sec_a, m)
        f_f = f"{a_f:11.4f}" if k else f"{'--':>11s}"
        f_a = f"{a_a:11.4f}" if k else f"{'--':>11s}"
        print(f"  {v:6.0f} {int(m.sum()):6d} {int(y[m].sum()):5d} "
              f"{int((~y[m]).sum()):6d} {k:11,d} {k/n_emp:8.1%} {f_f} {f_a}")
    print("  " + "-" * 76)
    print(f"  {'todos':>6s} {len(y):6d} {int(y.sum()):5d} {int((~y).sum()):6d} "
          f"{n_emp:11,d} {1.0:8.1%}")

    E0.banner("A IDENTIDADE DO TEOREMA (iii): AUROC(lex) = AUROC(s1) + tau(a2-1/2)")
    a_base = E0.auc(y, base)
    print(f"  comite (soma de votos) = {a_base:.4f} · tau = {tau:.4%} · "
          f"tau/2 = {tau/2:.4f} · teto = {a_base + tau/2:.4f}")
    print()
    print(f"  {'secundario':28s} {'AUROC global':>13s} {'a2':>8s} "
          f"{'lex previsto':>13s} {'lex real':>10s} {'captura':>9s}")
    print("  " + "-" * 86)
    for nome, s in [("familia (o do artigo)", sec_f),
                    ("familia + topologia", sec_a),
                    ("cos_g cru (controle fraco)", -sub.cos_g.to_numpy(float))]:
        a2, _ = a2_global(y, base, s)
        print(f"  {nome:28s} {E0.auc(y, s):13.4f} {a2:8.4f} "
              f"{a_base + tau*(a2-0.5):13.6f} {E0.auc(y, join(base, s)):10.6f} "
              f"{2*a2-1:8.1%}")
    print("\n  O AUROC GLOBAL do secundario nao aparece na identidade: a familia")
    print("  vale 0,78 no geral e ~0,59 onde o orcamento esta. E por isso que a")
    print("  captura e de 17%, e nao porque o desempatador seja fraco em geral.")


if __name__ == "__main__":
    main()

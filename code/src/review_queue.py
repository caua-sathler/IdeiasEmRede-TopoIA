"""J11 — A FILA DE REVISAO: o que a AUROC nao diz a um auditor.

AUROC e uma afirmacao sobre PARES. Um auditor revisa uma FILA, de cima para
baixo, ate o orcamento acabar. Este script traduz o resultado do artigo para
essa leitura, e mede uma consequencia do Teorema 15 que so aparece aqui:

    Um comite de 12 votos binarios tem 13 NIVEIS. Uma fila exige uma ordem
    TOTAL. Na fronteira de qualquer orcamento existe uma classe de empate que
    o comite nao ordena, entao A FILA NAO ESTA DEFINIDA: dois operadores com
    o mesmo comite e o mesmo orcamento revisam conjuntos diferentes.

O recall alcancavel num orcamento e portanto um INTERVALO EXATO (contagem, nao
estimativa), e um desempatador escolhe um ponto nele. A largura do intervalo e
quanto da decisao o comite simplesmente nao toma.

Predicoes em j11_predicoes.md, escritas antes de rodar.

    python review_queue.py
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import common as E0            # noqa: E402
import speaker_incidence as H6        # noqa: E402
from lexicographic_combination import join, deficit   # noqa: E402

warnings.filterwarnings("ignore")
SEED = 42
ORCAMENTOS = (0.05, 0.10, 0.20, 0.50)
N_SORTEIOS = 200


# ---------------------------------------------------------------------------
# O intervalo de ambiguidade, exato
# ---------------------------------------------------------------------------
def intervalo_recall(y: np.ndarray, s: np.ndarray, k: int) -> tuple[float, float]:
    """Recall pessimista e otimista ao revisar os `k` itens de maior `s`.

    Todos os itens com s > t entram (t = valor de corte); restam r vagas para
    a classe de empate s == t. O melhor caso preenche com positivos, o pior
    com negativos. Ambos sao contagens, nao estimativas.
    """
    P = int(y.sum())
    if P == 0 or k <= 0:
        return 0.0, 0.0
    ordem = np.sort(np.unique(s))[::-1]
    acima = 0
    for t in ordem:
        n_t = int((s == t).sum())
        if acima + n_t >= k:
            r = k - acima
            pos_acima = int(y[s > t].sum())
            pos_t = int(y[s == t].sum())
            neg_t = n_t - pos_t
            pess = (pos_acima + max(0, r - neg_t)) / P
            otim = (pos_acima + min(r, pos_t)) / P
            return pess, otim
        acima += n_t
    return 1.0, 1.0


def recall_em(y: np.ndarray, s: np.ndarray, k: int, rng) -> float:
    """Recall de UMA fila concreta: ordena por s, empates quebrados ao acaso."""
    chave = s + rng.random(len(s)) * 1e-12 * (np.ptp(s) + 1.0)
    idx = np.argsort(-chave, kind="stable")[:k]
    return float(y[idx].sum()) / max(int(y.sum()), 1)


def recall_det(y: np.ndarray, s: np.ndarray, k: int) -> float:
    """Recall de uma fila TOTALMENTE ordenada (sem empates a resolver)."""
    idx = np.argsort(-s, kind="stable")[:k]
    return float(y[idx].sum()) / max(int(y.sum()), 1)


def main() -> None:
    import pandas as pd
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import GroupKFold
    from sklearn.preprocessing import StandardScaler

    Di = pd.read_csv(E0.OUT / "opinion_table.csv")
    h7 = pd.read_csv(E0.OUT / "nli_features.csv")
    Mk = Di.sem_turno.to_numpy() == 0
    sub = Di[Mk].reset_index(drop=True)
    assert len(h7) == len(sub) and np.allclose(h7.cos_s, sub.cos_s, atol=1e-6)
    y = sub.hall.to_numpy().astype(bool)
    gm = sub.ref.to_numpy()
    rng = np.random.default_rng(SEED)
    n, P = len(y), int(y.sum())

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

    familia = oof(Xf)
    comite = V.sum(1)
    lex = join(comite, familia)
    cos_g = -sub.cos_g.to_numpy(float)

    # ---- controle 1: os numeros do artigo -------------------------------
    E0.banner("(0) CONTROLE — os numeros do artigo devem sair primeiro")
    tau, teto, a_com = deficit(y, comite)
    a_lex = E0.auc(y, lex)
    print(f"  n = {n}   positivos = {P} ({P/n:.1%})")
    print(f"  AUROC(comite, soma de votos) = {a_com:.4f}   (artigo: 0,9260)")
    print(f"  AUROC(lexicografico)         = {a_lex:.4f}   (artigo: 0,9300)")
    print(f"  AUROC(familia, OOF)          = {E0.auc(y, familia):.4f}")
    print(f"  tau = {tau:.2%}   orcamento tau/2 = {tau/2:.4f}")
    ok = abs(a_com - 0.9260) < 5e-4 and abs(a_lex - 0.9300) < 1e-3
    print(f"  [{'ok' if ok else 'FALHA'}] reproducao da base")
    if not ok:
        print("  ABORTANDO: sem a base reproduzida nada abaixo vale.")
        return

    # ---- P1: a fila do comite nao esta definida -------------------------
    E0.banner("(1) P1 — o comite NAO define uma fila: intervalo exato de recall")
    print(f"  {'orcam.':>7s} {'itens':>6s} | {'pessimista':>11s} {'otimista':>9s}"
          f" {'largura':>8s} | {'aleatorio (200x)':>22s}")
    print("  " + "-" * 78)
    larguras = {}
    aleat = {}
    for b in ORCAMENTOS:
        k = int(round(b * n))
        pess, otim = intervalo_recall(y, comite, k)
        draws = np.array([recall_em(y, comite, k, rng) for _ in range(N_SORTEIOS)])
        larguras[b] = otim - pess
        aleat[b] = (draws.mean(), draws.std())
        print(f"  {b:6.0%} {k:6d} | {pess:10.1%} {otim:9.1%} "
              f"{otim-pess:8.1%} | {draws.mean():8.1%} (dp {draws.std():.1%})")
    p1 = max(larguras.values()) >= 0.05
    print(f"\n  P1 (largura >= 5 pp em algum orcamento): "
          f"{'CONFIRMADA' if p1 else 'REFUTADA'} "
          f"(maior largura = {max(larguras.values()):.1%})")

    # ---- P2/P3: o desempate escolhe um ponto no intervalo ---------------
    E0.banner("(2) P2/P3 — onde o desempatador cai dentro do intervalo")
    print(f"  {'orcam.':>7s} | {'aleatorio':>10s} {'LEXICOGR.':>10s} "
          f"{'ganho':>8s} | {'posicao no intervalo':>21s}")
    print("  " + "-" * 72)
    ganhos = {}
    for b in ORCAMENTOS:
        k = int(round(b * n))
        pess, otim = intervalo_recall(y, comite, k)
        r_lex = recall_det(y, lex, k)
        mu = aleat[b][0]
        ganhos[b] = r_lex - mu
        pos = (r_lex - pess) / (otim - pess) if otim > pess else float("nan")
        print(f"  {b:6.0%} | {mu:9.1%} {r_lex:10.1%} {r_lex-mu:+8.1%} | "
              f"{pos:20.0%}")
    p2 = all(g >= -1e-9 for b, g in ganhos.items() if b < 0.5)
    print(f"\n  P2 (lex >= media aleatoria nos orcamentos operacionais): "
          f"{'CONFIRMADA' if p2 else 'REFUTADA'}")
    rel_auroc = (a_lex - a_com) / a_com
    print(f"  P3: ganho relativo em AUROC = {rel_auroc:+.2%}")
    for b in (0.05, 0.10, 0.20):
        mu = aleat[b][0]
        print(f"      ganho relativo em recall@{b:.0%} = "
              f"{ganhos[b]/mu if mu > 0 else float('nan'):+.2%}")

    # ---- IC agrupado do ganho de recall ---------------------------------
    E0.banner("(3) IC95 agrupado por audiencia do ganho de recall (lex - aleatorio)")
    us = np.unique(gm)
    mp = {u: np.where(gm == u)[0] for u in us}
    rb = np.random.default_rng(SEED)
    for b in (0.05, 0.10, 0.20):
        d = []
        for _ in range(2000):
            s_idx = np.concatenate([mp[u] for u in
                                    us[rb.integers(0, len(us), len(us))]])
            if y[s_idx].sum() < 2:
                continue
            kk = int(round(b * len(s_idx)))
            d.append(recall_det(y[s_idx], lex[s_idx], kk)
                     - recall_em(y[s_idx], comite[s_idx], kk, rb))
        d = np.array(d)
        lo, hi = np.percentile(d, [2.5, 97.5])
        st = "*" if (lo > 0 or hi < 0) else " "
        print(f"  recall@{b:>4.0%}:  {d.mean():+.1%}  [{lo:+.1%}, {hi:+.1%}]{st}")

    # ---- P4: a escada de custo, na leitura operacional ------------------
    E0.banner("(4) P4 — a escada de orcamento, lida como carga de revisao")
    melhor_j = max(JU, key=lambda j: E0.auc(y, sub[j].fillna(0).to_numpy(float)))
    vj = sub[melhor_j].fillna(0).to_numpy(float)
    escada = [
        ("cosseno global (programa anterior)", 0, cos_g, False),
        ("familia de incidencia", 0, familia, True),
        (f"melhor juiz sozinho ({melhor_j.replace('juiz_', '')})", 1, vj, False),
        ("melhor juiz + familia, lexicografico", 1, join(vj, familia), True),
        ("comite de 12 juizes", 12, comite, False),
        ("comite + familia, lexicografico", 12, lex, True),
    ]
    print(f"  {'metodo':40s} {'cham.':>5s} {'AUROC':>7s} " +
          " ".join(f"{'r@'+format(b, '.0%'):>8s}" for b in ORCAMENTOS))
    print("  " + "-" * 88)
    linhas = []
    for nome, custo, s, total in escada:
        rs = []
        for b in ORCAMENTOS:
            k = int(round(b * n))
            if total:
                rs.append(recall_det(y, s, k))
            else:
                rs.append(np.mean([recall_em(y, s, k, rng) for _ in range(50)]))
        linhas.append((nome, custo, E0.auc(y, s), rs))
        print(f"  {nome:40s} {custo:5d} {E0.auc(y, s):7.4f} " +
              " ".join(f"{r:8.1%}" for r in rs))
    r_fam = dict(zip(ORCAMENTOS, linhas[1][3]))[0.10]
    r_cos = dict(zip(ORCAMENTOS, linhas[0][3]))[0.10]
    print(f"\n  P4 (familia >= 2x cosseno global em r@10%): "
          f"{'CONFIRMADA' if r_fam >= 2 * r_cos else 'REFUTADA'} "
          f"({r_fam:.1%} vs {r_cos:.1%}, fator {r_fam/max(r_cos,1e-9):.2f}x)")

    # ---- P5: e onde o desempate NAO ajuda -------------------------------
    E0.banner("(5) P5 — onde o desempate nao ajuda (orcamentos grandes)")
    k50 = int(round(0.50 * n))
    pess, otim = intervalo_recall(y, comite, k50)
    print(f"  em 50%: intervalo [{pess:.1%}, {otim:.1%}], largura {otim-pess:.1%}; "
          f"ganho do lex = {ganhos[0.50]:+.1%}")
    print(f"  P5 (ganho em 50% menor que em 10%): "
          f"{'CONFIRMADA' if abs(ganhos[0.50]) < abs(ganhos[0.10]) else 'REFUTADA'}")

    # ---- material para a figura do artigo -------------------------------
    E0.banner("(6) COORDENADAS PARA A FIGURA (nao editar a mao no .tex)")
    print(f"  comite      = {a_com:.4f}")
    print(f"  lex         = {a_lex:.4f}")
    print(f"  teto_desemp = {a_com + tau/2:.4f}   (comite + tau/2)")
    print(f"  tau_meio    = {tau/2:.4f}")
    print(f"  captura     = {(a_lex - a_com)/(tau/2):.1%}")
    for b in (0.05, 0.10, 0.20):
        k = int(round(b * n))
        pess, otim = intervalo_recall(y, comite, k)
        print(f"  r@{b:.0%}: pess={pess:.4f} otim={otim:.4f} "
              f"aleat={aleat[b][0]:.4f} lex={recall_det(y, lex, k):.4f}")

    E0.banner("(7) CURVAS DENSAS — coordenadas TikZ para a Figura 2 do artigo")
    grade = [0.02, 0.04, 0.06, 0.08, 0.10, 0.13, 0.16, 0.20,
             0.25, 0.30, 0.40, 0.50]
    curvas = [
        ("cosg", cos_g, False),
        ("familia", familia, True),
        ("juiz", vj, False),
        ("juizlex", join(vj, familia), True),
        ("comite", comite, False),
        ("comitelex", lex, True),
    ]
    print("  % gerado por review_queue.py secao (7) — nao editar a mao")
    for nome, s, total in curvas:
        pts = []
        for b in grade:
            k = int(round(b * n))
            r = (recall_det(y, s, k) if total
                 else float(np.mean([recall_em(y, s, k, rng) for _ in range(200)])))
            pts.append(f"({b*100:.0f},{r*100:.1f})")
        print(f"  \\def\\{nome}{{{' '.join(pts)}}}")
    print()


if __name__ == "__main__":
    main()

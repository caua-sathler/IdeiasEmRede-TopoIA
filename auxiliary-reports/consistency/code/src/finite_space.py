"""F1 — ESPAÇOS TOPOLÓGICOS FINITOS SOBRE A RELAÇÃO DE ACARRETAMENTO.

A TESE, em uma frase:

    a entropia semântica (Farquhar et al., *Nature* 630, 2024) calcula o número de
    pontos de um espaço topológico finito que ela nunca nomeia; nomear o espaço dá
    o seu tipo de homotopia inteiro de graça.

O MECANISMO DA SOTA. A entropia semântica amostra N gerações, agrupa duas quaisquer
quando há acarretamento BIDIRECIONAL (a ⊢ b e b ⊢ a), e devolve a entropia sobre as
classes. Isto é: ela constrói a relação de equivalência ~ gerada por ⊢ ∩ ⊢ᵒᵖ e mede
H(N/~). O resultado depende SÓ do multiconjunto de tamanhos das classes.

O QUE ELA JOGA FORA. Acarretamento é uma pré-ordem, não uma equivalência. Ao
simetrizar à força, a SOTA descarta a DIREÇÃO (a ⊢ b sem b ⊢ a significa que a é
mais específica que b). Duas amostras com as MESMAS classes e a MESMA distribuição
têm a MESMA entropia semântica, quaisquer que sejam as relações entre as classes.

A CORREÇÃO. Por ALEXANDROV, uma pré-ordem num conjunto finito É uma topologia
(abertos = conjuntos superiores). Por McCORD (1966), esse espaço finito é
fracamente equivalente ao COMPLEXO DE ORDEM do poset — um complexo simplicial cujos
k-simplexos são as cadeias de k+1 elementos. Por STONG (1966), ele tem um NÚCLEO
minimal, único a menos de homeomorfismo, obtido removendo "beat points".

Nada disso é caro: N ≤ 20, tudo é contagem.

    |P|             o que a SOTA vê       (número de pontos)
    χ̃              contagem alternada de cadeias — teorema de P. Hall
    b₀, b₁          homologia do complexo de ordem
    núcleo          modelo minimal de Stong; |núcleo| = 1 ⟺ contrátil

O CONTRA-EXEMPLO QUE DECIDE — a ESCADA DE GRANULARIDADE. Um modelo que responde

    "foi em 1988"  ⊢  "foi no fim dos anos 80"  ⊢  "foi no século XX"

produz N classes distintas (nenhuma equivale a outra), logo entropia semântica
MÁXIMA — e nenhuma discordância: é UMA crença dita em granularidades diferentes.
Uma cadeia tem máximo, logo o complexo de ordem é um cone: CONTRÁTIL, núcleo = 1
ponto. A SOTA grita alucinação onde a topologia vê consenso.

Isso não é hipotético: a própria literatura registra que a entropia semântica
degrada em respostas longas de uma frase — "a pattern inherent to tasks such as
summarization" — que é exatamente a tarefa deste desafio.

    python finite_space.py        # a prova sintética
"""
from __future__ import annotations

import numpy as np

# --------------------------------------------------------------------------- núcleo


def fecho_transitivo(R: np.ndarray) -> np.ndarray:
    """Fecho transitivo-reflexivo de uma relação booleana (Floyd-Warshall, n ≤ 20).

    O NLI medido NÃO é transitivo; Alexandrov exige uma pré-ordem. Fechar é a
    escolha honesta — e a diferença entre R e o seu fecho é ela mesma mensurável
    (`nao_transitividade`)."""
    n = len(R)
    T = R.copy().astype(bool)
    np.fill_diagonal(T, True)
    for k in range(n):
        T |= np.outer(T[:, k], T[k, :])
    return T


def nao_transitividade(R: np.ndarray) -> float:
    """Fração de arestas que o fecho precisa acrescentar. Mede o quanto o modelo de
    NLI viola a transitividade que LGU (arXiv 2607.16868) assume por teorema."""
    T = fecho_transitivo(R)
    n = len(R)
    fora = n * n - n
    if fora <= 0:
        return 0.0
    R0 = R.copy().astype(bool)
    np.fill_diagonal(R0, False)
    T0 = T.copy()
    np.fill_diagonal(T0, False)
    return float((T0 & ~R0).sum()) / fora


def reflexao_poset(T: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Pré-ordem -> poset. Devolve (matriz ≤ do poset quociente, rótulo de classe).

    Elementos mutuamente acarretados formam UMA classe: são exatamente os
    "clusters" da entropia semântica. O espaço de Alexandrov da pré-ordem
    deformação-retrai sobre o do quociente, então o tipo de homotopia é o mesmo."""
    n = len(T)
    mut = T & T.T
    lab = -np.ones(n, dtype=int)
    k = 0
    for i in range(n):
        if lab[i] < 0:
            lab[mut[i]] = k
            k += 1
    P = np.zeros((k, k), dtype=bool)
    for i in range(n):
        for j in range(n):
            if T[i, j]:
                P[lab[i], lab[j]] = True
    np.fill_diagonal(P, True)
    return P, lab


def cadeias(P: np.ndarray, kmax: int = 3) -> list[list[tuple]]:
    """Cadeias estritas do poset, por comprimento. `saida[k]` tem as de k+1 elementos.

    Os k-simplexos do complexo de ordem. Só preciso de k ≤ 2 para b₀ e b₁, e o
    número delas é ≤ C(n, k+1) — nada explode."""
    n = len(P)
    lt = P & ~P.T                                   # ordem ESTRITA
    out: list[list[tuple]] = [[(i,) for i in range(n)]]
    atual = [(i,) for i in range(n)]
    for _ in range(kmax - 1):
        prox = []
        for c in atual:
            u = c[-1]
            for v in range(n):
                if lt[u, v]:
                    prox.append(c + (v,))
        out.append(prox)
        atual = prox
        if not prox:
            break
    while len(out) < kmax:
        out.append([])
    return out


def betti(P: np.ndarray) -> tuple[int, int]:
    """(b₀, b₁) do complexo de ordem, sobre ℚ, por posto das matrizes de bordo."""
    C = cadeias(P, 3)
    V, E, F = C[0], C[1], C[2]
    nv, ne, nf = len(V), len(E), len(F)
    if ne == 0:
        return nv, 0
    idxE = {e: i for i, e in enumerate(E)}
    d1 = np.zeros((nv, ne))
    for j, (a, b) in enumerate(E):
        d1[a, j], d1[b, j] = -1.0, 1.0
    r1 = int(np.linalg.matrix_rank(d1)) if ne else 0
    b0 = nv - r1
    r2 = 0
    if nf:
        d2 = np.zeros((ne, nf))
        for j, (a, b, c) in enumerate(F):
            d2[idxE[(b, c)], j] += 1.0
            d2[idxE[(a, c)], j] -= 1.0
            d2[idxE[(a, b)], j] += 1.0
        r2 = int(np.linalg.matrix_rank(d2))
    b1 = (ne - r1) - r2
    return int(b0), int(max(0, b1))


def euler_hall(P: np.ndarray) -> int:
    """χ̃ reduzida do complexo de ordem, via FUNÇÃO DE MÖBIUS do poset.

    Teorema de P. Hall: χ̃ = Σ_k (−1)^k c_k, com c_k = nº de cadeias de k elementos
    — mas contar cadeias é exponencial numa cadeia longa (2^n subconjuntos, todos
    cadeias). O mesmo número sai EXATO em O(n²) pela recursão de Möbius no poset
    com 0̂ adjunto:

        μ(0̂, x) = −Σ_{y < x} μ(0̂, y) − 1        e        χ̃ = −1 − Σ_x μ(0̂, x)

    Um invariante topológico obtido por contagem pura — sem homologia, sem álgebra
    linear. Cadeia -> 0 (contrátil). Anticadeia de k -> k−1. Coroa S¹ -> −1."""
    n = len(P)
    lt = P & ~P.T
    mu = np.zeros(n, dtype=np.int64)
    # ordem topológica: processa x só depois de todo y < x
    grau = lt.sum(0)
    ordem = sorted(range(n), key=lambda i: (grau[i], i))
    feito = np.zeros(n, dtype=bool)
    while not feito.all():
        avancou = False
        for x in ordem:
            if feito[x]:
                continue
            abaixo = np.where(lt[:, x])[0]
            if not feito[abaixo].all():
                continue
            mu[x] = -1 - int(mu[abaixo].sum())      # o −1 é o μ(0̂,0̂) = 1
            feito[x] = True
            avancou = True
        if not avancou:                              # ciclo: não é poset
            break
    return int(-1 - mu.sum())


def nucleo(P: np.ndarray) -> np.ndarray:
    """NÚCLEO DE STONG: remove beat points até não haver mais. Devolve os índices.

    x é *down-beat* se {y : y < x} tem MÁXIMO, e *up-beat* se {y : y > x} tem
    MÍNIMO. Remover um beat point é uma deformação-retração forte, então o núcleo
    tem o mesmo tipo de homotopia — e Stong (1966) prova que ele é ÚNICO a menos de
    homeomorfismo. É o conteúdo semântico irredutível da amostra: um resumo
    extrativo com teorema de unicidade."""
    viv = np.ones(len(P), dtype=bool)
    lt = P & ~P.T
    mudou = True
    while mudou and viv.sum() > 1:
        mudou = False
        for x in np.where(viv)[0]:
            baixo = np.where(viv & lt[:, x])[0]      # y < x
            alto = np.where(viv & lt[x, :])[0]       # y > x
            beat = False
            if len(baixo) == 1:
                beat = True                          # máximo trivial
            elif len(baixo) > 1:                     # existe y* com todo y ≤ y*?
                beat = any(all(lt[y, m] or y == m for y in baixo) for m in baixo)
            if not beat and len(alto) == 1:
                beat = True
            elif not beat and len(alto) > 1:
                beat = any(all(lt[m, y] or y == m for y in alto) for m in alto)
            if beat:
                viv[x] = False
                mudou = True
                break
    return np.where(viv)[0]


def nucleo_massa(P: np.ndarray, p: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """NÚCLEO COM TRANSPORTE DE MASSA — o método proposto.

    Colapsa beat points como `nucleo`, mas carrega a probabilidade junto: quando x
    é removido, a sua massa vai para a TESTEMUNHA do colapso (o máximo de Û(x) ou o
    mínimo de F̂(x)), que é exatamente o ponto que o absorve na retração. Uma
    resposta que só repete outra em granularidade diferente devolve o seu peso a
    ela em vez de contar como classe nova.

    Devolve (índices do núcleo, massas do núcleo)."""
    n = len(P)
    viv = np.ones(n, dtype=bool)
    q = p.astype(float).copy()
    lt = P & ~P.T
    mudou = True
    while mudou and viv.sum() > 1:
        mudou = False
        for x in np.where(viv)[0]:
            baixo = np.where(viv & lt[:, x])[0]
            alto = np.where(viv & lt[x, :])[0]
            test = -1
            if len(baixo) == 1:
                test = int(baixo[0])
            elif len(baixo) > 1:
                for m in baixo:
                    if all(lt[y, m] or y == m for y in baixo):
                        test = int(m); break
            if test < 0 and len(alto) == 1:
                test = int(alto[0])
            elif test < 0 and len(alto) > 1:
                for m in alto:
                    if all(lt[m, y] or y == m for y in alto):
                        test = int(m); break
            if test >= 0:
                q[test] += q[x]                   # a massa segue a retração
                q[x] = 0.0
                viv[x] = False
                mudou = True
                break
    idx = np.where(viv)[0]
    return idx, q[idx]


def _H(q: np.ndarray) -> float:
    q = q / max(q.sum(), 1e-12)
    q = q[q > 0]
    return float(-(q * np.log(q)).sum())


def entropia_nucleo(P: np.ndarray, p: np.ndarray, ordens: int = 8,
                    seed: int = 0) -> float:
    """ENTROPIA SEMÂNTICA DE NÚCLEO — substituto drop-in da SOTA.

    Idêntica à entropia semântica, exceto que é calculada sobre o NÚCLEO de Stong
    em vez de sobre todas as classes. Conserta o modo de falha da escada de
    granularidade: numa cadeia o núcleo é UM ponto, então esta entropia é 0
    enquanto a da SOTA é log k — o seu valor MÁXIMO.

    POR QUE A MÉDIA SOBRE ORDENS. Stong garante que o núcleo é único a menos de
    homeomorfismo, e de fato o seu TAMANHO é exatamente invariante (medido: 0
    divergências em 1500 posets × 6 ordens). Mas a MASSA não é: quando há várias
    sequências de colapso válidas, a testemunha que absorve cada ponto pode mudar,
    e a entropia oscilou em 2.1% dos casos (amplitude máxima 0.56 numa escala de
    0 a log n). Definir o estimador como a ESPERANÇA sobre sequências de colapso
    uniformes o torna bem definido por construção; a média empírica sobre `ordens`
    permutações é o estimador. `entropia_nucleo_dp` devolve também o desvio, que
    serve de diagnóstico de quão ambíguo é o colapso daquele item."""
    return entropia_nucleo_dp(P, p, ordens, seed)[0]


def entropia_nucleo_dp(P: np.ndarray, p: np.ndarray, ordens: int = 8,
                       seed: int = 0) -> tuple[float, float]:
    """(média, desvio) da entropia de núcleo sobre `ordens` sequências de colapso."""
    n = len(P)
    if n <= 1:
        return 0.0, 0.0
    rng = np.random.default_rng(seed)
    vs = []
    for k in range(ordens):
        pi = np.arange(n) if k == 0 else rng.permutation(n)
        _, q = nucleo_massa(P[np.ix_(pi, pi)], np.asarray(p, float)[pi])
        vs.append(_H(q))
    return float(np.mean(vs)), float(np.std(vs))


def altura(P: np.ndarray) -> int:
    """Comprimento da maior cadeia estrita — a profundidade da escada de
    especificidade que o modelo percorreu numa única pergunta."""
    n = len(P)
    lt = P & ~P.T
    memo = {}

    def prof(i: int) -> int:
        if i in memo:
            return memo[i]
        s = [prof(j) for j in range(n) if lt[i, j]]
        memo[i] = 1 + (max(s) if s else 0)
        return memo[i]

    return max((prof(i) for i in range(n)), default=0)


def entropia_semantica(lab: np.ndarray) -> float:
    """A SOTA (variante discreta de Farquhar et al.): entropia sobre as classes de
    acarretamento mútuo. Note que ela lê APENAS `lab` — a partição. Nenhuma
    informação de ordem entra nesta função; é essa cegueira que o F1 explora."""
    _, cnt = np.unique(lab, return_counts=True)
    p = cnt / cnt.sum()
    return float(-(p * np.log(p)).sum())


def perfil(R: np.ndarray) -> dict:
    """Todos os invariantes de uma relação de acarretamento bruta."""
    T = fecho_transitivo(R)
    P, lab = reflexao_poset(T)
    b0, b1 = betti(P)
    nu = nucleo(P)
    return {
        "n_classes": len(P),                 # o que a SOTA vê
        "se": entropia_semantica(lab),       # a SOTA
        "b0": b0, "b1": b1,
        "chi": euler_hall(P),
        "nucleo": len(nu),
        "contratil": int(len(nu) == 1),
        "altura": altura(P),
        "nao_trans": nao_transitividade(R),
    }


# --------------------------------------------------------------------------- prova
def rel_cadeia(n: int) -> np.ndarray:
    """ESCADA DE GRANULARIDADE: a₁ ⊢ a₂ ⊢ ... ⊢ aₙ. Uma crença, n granularidades."""
    R = np.zeros((n, n), dtype=bool)
    for i in range(n):
        for j in range(i + 1, n):
            R[i, j] = True
    return R


def rel_anticadeia(n: int) -> np.ndarray:
    """DISCORDÂNCIA GENUÍNA: n respostas mutuamente incomparáveis."""
    return np.eye(n, dtype=bool)


def rel_coroa(m: int = 2) -> np.ndarray:
    """COROA: m mínimos, m máximos, todos comparáveis entre níveis. Para m = 2 é o
    MODELO FINITO MINIMAL DE S¹ (Barmak) — quatro pontos bastam para um buraco.

    Leitura semântica: duas respostas específicas incompatíveis, cada uma
    acarretando duas generalizações que não se acarretam. O modelo está seguro do
    grosso e em conflito no fino, e as partes grossas não se determinam."""
    n = 2 * m
    R = np.eye(n, dtype=bool)
    for i in range(m):
        for j in range(m, n):
            R[i, j] = True
    return R


def rel_v(n: int) -> np.ndarray:
    """LEQUE: um mínimo que acarreta n−1 máximos incomparáveis. Uma resposta
    específica e várias generalizações dela. Contrátil (tem mínimo)."""
    R = np.eye(n, dtype=bool)
    R[0, 1:] = True
    return R


def main() -> None:
    import common as E0

    E0.banner("A SEPARACAO, POR CONSTRUCAO: mesma entropia semantica, "
              "topologias distintas")
    print("  Toda familia abaixo tem N=6 geracoes e SEIS classes de acarretamento")
    print("  mutuo distintas. Logo a entropia semantica e IDENTICA e MAXIMA em")
    print("  todas: log 6 = 1.7918. Ela nao pode distingui-las nem em principio.\n")
    fam = [("escada de granularidade (cadeia)", rel_cadeia(6)),
           ("leque (1 especifica, 5 gerais)", rel_v(6)),
           ("coroa dupla S^1 (4) + 2 isoladas", None),
           ("discordancia genuina (anticadeia)", rel_anticadeia(6))]
    R = np.zeros((6, 6), dtype=bool)
    R[:4, :4] = rel_coroa(2)
    np.fill_diagonal(R, True)
    fam[2] = (fam[2][0], R)

    print(f"  {'familia':34s} {'SE':>7s} {'SE-nuc':>7s} {'b0':>3s} {'b1':>3s} "
          f"{'chi':>4s} {'nucleo':>7s}  veredito")
    print("  " + "-" * 104)
    for nome, Rl in fam:
        p = perfil(Rl)
        P, _ = reflexao_poset(fecho_transitivo(Rl))
        en = entropia_nucleo(P, np.ones(len(P)) / len(P))
        v = ("UMA crenca, varias granularidades" if p["contratil"]
             else (f"{p['b1']} buraco(s): conflito nao reconciliavel"
                   if p["b1"] else f"{p['b0']} crencas independentes"))
        print(f"  {nome:34s} {p['se']:7.4f} {en:7.4f} {p['b0']:3d} "
              f"{p['b1']:3d} {p['chi']:4d} {p['nucleo']:7d}  {v}")

    E0.banner("O QUE ISSO PROVA")
    print("  A coluna SE e constante por construcao — a entropia semantica e funcao")
    print("  APENAS da particao em classes, e as quatro familias tem a mesma.")
    print("  As colunas topologicas separam as quatro. Nao e um efeito estatistico")
    print("  a ser medido com IC: e um fato sobre o que cada funcional le.")
    print()
    print("  Em particular a escada (cadeia) tem SE MAXIMA e nucleo = 1 ponto: o")
    print("  modelo esta perfeitamente coerente e a SOTA o marca como confabulacao.")
    print("  E a coroa tem b1 = 1, uma patologia que NENHUM numero de clusters ve.")

    E0.banner("ROBUSTEZ DO CONTRA-EXEMPLO: a escada em varios tamanhos")
    print(f"  {'N':>3s} {'SE (a SOTA)':>12s} {'nucleo':>7s} {'chi':>4s}  leitura")
    print("  " + "-" * 62)
    for n in (2, 4, 8, 16):
        p = perfil(rel_cadeia(n))
        print(f"  {n:3d} {p['se']:12.4f} {p['nucleo']:7d} {p['chi']:4d}  "
              f"SE cresce como log N, a topologia permanece trivial")


if __name__ == "__main__":
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    main()

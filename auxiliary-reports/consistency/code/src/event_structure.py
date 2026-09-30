"""H1 — ESTRUTURAS DE EVENTOS SEMÂNTICAS: a topologia da CONSISTÊNCIA.

A TESE, em uma frase:

    a entropia semântica descarta a ORDEM do acarretamento (fase F) e descarta
    também a distinção entre CONTRADIÇÃO e NEUTRALIDADE; o objeto que carrega as
    duas é uma estrutura de eventos (Winskel), cujas configurações maximais são
    os MUNDOS POSSÍVEIS que o conjunto de respostas sustenta.

O QUE A SOTA E OS SUCESSORES FAZEM COM O CONFLITO:

    SE  (Nature 2024)      contradição = neutro = "não equivalente"  (cega)
    KLE (NeurIPS 2024)     peso w = (1, 0.5, 0): conflito é um NÚMERO, não uma
                           obstrução — e neutro vira "meio parecido"
    LGU (jul/2026)         densidade escalar de contradição entre raízes
    DEG (2407.00994)       grafo dirigido de acarretamento; contradição ignorada
    fase F (nossa)         poset/topologia da ordem; contradição ignorada

O OBJETO. Sobre as classes do poset de acarretamento P (a reflexão da fase F),
uma relação de conflito C lida do NLI. A semântica exige HERANÇA: quem contradiz
o geral contradiz todo refinamento dele —

    u ⊑ v,  w ⊑ v',  v # v'   ⟹   u # w        (fecho:  C* = bool(P·C·Pᵀ))

Isto é exatamente o axioma de estrutura de eventos (com causalidade = generali-
zação). As CONFIGURAÇÕES (conjuntos sem conflito interno, fechados para generali-
zação) são estados de crença consistentes; as maximais são os MUNDOS.

A FORMA TOPOLÓGICA. Os conjuntos livres de conflito formam o COMPLEXO DE
INDEPENDÊNCIA Ind(C*) do grafo de conflito — um complexo de bandeira clássico da
topologia combinatória. Os mundos são as FACETAS de Ind(C*). Pela dualidade de
Dowker aplicada à relação de pertinência classe×mundo, o NERVO do recobrimento
por mundos tem o mesmo tipo de homotopia de Ind(C*): a homologia do conflito pode
ser computada de qualquer um dos lados.

POR QUE OS MUNDOS SÃO MIS. Após o fecho de herança, o fechamento-para-cima de um
conjunto livre de conflito é livre de conflito (se uma generalização v ⊒ u
conflitasse com w, então u conflitaria com w pelo fecho). Logo todo conjunto
independente MAXIMAL já contém as generalizações de seus membros, e

    mundos  =  conjuntos independentes maximais de C*      (verificado no main)

O CONTRA-EXEMPLO QUE DECIDE — o Λ (hedge). Duas respostas específicas em
conflito sob UMA generalização comum:

    "foi Paris"  #  "foi Roma",   ambas ⊑ "foi uma capital europeia"

O núcleo de Stong COLAPSA o Λ (as específicas são up-beat points; o geral absorve
tudo): SE-núcleo = 0, exatamente o mecanismo pelo qual a fase F perdeu −0,015 no
TriviaQA — colapsar o hedge destrói o sinal de incerteza. Os mundos PRESERVAM o
conflito ({Paris, capital} e {Roma, capital}: 2 mundos) enquanto colapsam a
elaboração (cadeia sem conflito: 1 mundo). E as duas anticadeias — compossível
(tudo neutro) e conflitante (tudo contradiz) — têm TODOS os invariantes da fase F
idênticos e mundos 1 contra n: a cegueira ao conflito é por construção.

    python event_structure.py     # prova sintética + validação
"""
from __future__ import annotations

import numpy as np

# ----------------------------------------------------------------- construção


def simetrizar(Craw: np.ndarray) -> np.ndarray:
    """Conflito é semanticamente simétrico; a assimetria medida é ruído do
    verificador. `a # b` se QUALQUER direção passa do limiar (a escolha do f12)."""
    C = Craw.astype(bool)
    C = C | C.T
    np.fill_diagonal(C, False)
    return C


def fechar_conflito(P: np.ndarray, C: np.ndarray) -> np.ndarray:
    """Fecho de HERANÇA do conflito:  u ⊑ v, w ⊑ v', v # v'  ⟹  u # w.

    Em matrizes booleanas (P[u,v] = u ⊑ v, reflexiva):  C* = bool(P · C · Pᵀ).
    É o axioma de estrutura de eventos na direção semântica: contradizer o geral
    é contradizer todo refinamento dele. A fração de arestas acrescentadas é o
    análogo exato da não-transitividade da fase F — reportá-la, não escondê-la."""
    Pi = P.astype(np.int64)
    Cs = (Pi @ simetrizar(C).astype(np.int64) @ Pi.T) > 0
    return Cs


def custo_fecho(C: np.ndarray, Cs: np.ndarray) -> float:
    """Fração de pares (não ordenados, fora da diagonal) que o fecho acrescenta."""
    n = len(C)
    if n < 2:
        return 0.0
    C0 = simetrizar(C)
    C1 = Cs.copy()
    np.fill_diagonal(C1, False)
    tot = n * (n - 1) / 2
    novo = (C1 & ~C0).sum() / 2
    return float(novo) / tot


def autoconflito(Cs: np.ndarray) -> np.ndarray:
    """Classes que conflitam consigo mesmas após o fecho (conflitam com um
    ancestral): eventos IMPOSSÍVEIS na leitura de estrutura de eventos —
    incoerência do verificador. Ficam fora de todo mundo; a taxa é diagnóstico."""
    return np.diag(Cs).copy()


def mundos(Cs: np.ndarray) -> list[list[int]]:
    """MUNDOS = conjuntos independentes maximais do grafo de conflito fechado
    (= cliques maximais do grafo de consistência), entre as classes possíveis
    (sem autoconflito). Bron–Kerbosch com pivô; n ≤ 20, custo irrelevante."""
    n = len(Cs)
    vivos = [i for i in range(n) if not Cs[i, i]]
    if not vivos:
        return []
    # adjacência de CONSISTÊNCIA entre os vivos
    adj = {v: {u for u in vivos if u != v and not Cs[v, u]} for v in vivos}
    out: list[list[int]] = []

    def bk(R: set, Pv: set, X: set) -> None:
        if not Pv and not X:
            out.append(sorted(R))
            return
        u = max(Pv | X, key=lambda w: len(adj[w] & Pv))
        for v in list(Pv - adj[u]):
            bk(R | {v}, Pv & adj[v], X & adj[v])
            Pv.discard(v)
            X.add(v)

    bk(set(), set(vivos), set())
    return out


def massa_mundos(Ws: list[list[int]], p: np.ndarray) -> np.ndarray:
    """Massa de cada mundo: a massa de cada classe é rateada igualmente entre os
    mundos que a contêm (conserva massa; classes impossíveis perdem a sua)."""
    if not Ws:
        return np.array([])
    m = np.zeros(len(p))
    for W in Ws:
        for u in W:
            m[u] += 1.0
    q = np.array([sum(p[u] / m[u] for u in W) for W in Ws], float)
    s = q.sum()
    return q / s if s > 0 else q


def _H(q: np.ndarray) -> float:
    q = q[q > 0]
    if len(q) == 0:
        return 0.0
    q = q / q.sum()
    return float(-(q * np.log(q)).sum())


def entropia_mundos(P: np.ndarray, C: np.ndarray, p: np.ndarray) -> float:
    """WE — ENTROPIA DE MUNDOS: a entropia sobre os mundos possíveis, com massa
    rateada. Colapsa elaboração e compossibilidade (1 mundo ⟹ 0) e preserva
    conflito (k mundos equiprováveis ⟹ log k). Substituto drop-in: mesma entrada
    da SE mais a coluna de contradição que o NLI já produz e todos descartam."""
    Cs = fechar_conflito(P, C)
    return _H(massa_mundos(mundos(Cs), p))


def b0_consistencia(Cs: np.ndarray) -> int:
    """Componentes conexas do grafo de consistência (1-esqueleto de Ind):
    blocos de classes mutuamente irreconciliáveis entre blocos."""
    n = len(Cs)
    vivos = [i for i in range(n) if not Cs[i, i]]
    if not vivos:
        return 0
    pai = {v: v for v in vivos}

    def find(a):
        while pai[a] != a:
            pai[a] = pai[pai[a]]
            a = pai[a]
        return a

    for i in vivos:
        for j in vivos:
            if i < j and not Cs[i, j]:
                pai[find(i)] = find(j)
    return len({find(v) for v in vivos})


def b1_independencia(Cs: np.ndarray) -> int:
    """b₁ do complexo de independência Ind(C*).
    Ind é complexo de bandeira (o complexo de cliques do grafo de CONSISTÊNCIA):
    faces = conjuntos SEM conflito interno; bastam as dimensões 0–2 para b₁
    (posto de ∂₁ e ∂₂ sobre ℚ, como em f1.betti).
    Condição necessária para b₁ > 0: um ciclo induzido de comprimento ≥ 4 no
    grafo de consistência. O menor exemplo são dois conflitos disjuntos
    (a#b, c#d: 4 mundos, b₁ = 1), sem nenhum ciclo de conflito; o pentágono é
    só o menor exemplo entre grafos de conflito que são ciclos (correção
    registrada em 2026-08-03; ver o relatório, Seção 4)."""
    n = len(Cs)
    vivos = [i for i in range(n) if not Cs[i, i]]
    nv = len(vivos)
    if nv == 0:
        return 0
    idx = {v: k for k, v in enumerate(vivos)}
    E = [(a, b) for i, a in enumerate(vivos) for b in vivos[i + 1:]
         if not Cs[a, b]]
    if not E:
        return 0
    T = [(a, b, c)
         for i, a in enumerate(vivos)
         for j, b in enumerate(vivos[i + 1:], i + 1)
         if not Cs[a, b]
         for c in vivos[j + 1:]
         if not Cs[a, c] and not Cs[b, c]]
    ne, nf = len(E), len(T)
    iE = {e: k for k, e in enumerate(E)}
    d1 = np.zeros((nv, ne))
    for k, (a, b) in enumerate(E):
        d1[idx[a], k], d1[idx[b], k] = -1.0, 1.0
    r1 = int(np.linalg.matrix_rank(d1))
    r2 = 0
    if nf:
        d2 = np.zeros((ne, nf))
        for k, (a, b, c) in enumerate(T):
            d2[iE[(b, c)], k] += 1.0
            d2[iE[(a, c)], k] -= 1.0
            d2[iE[(a, b)], k] += 1.0
        r2 = int(np.linalg.matrix_rank(d2))
    return int(max(0, (ne - r1) - r2))


def perfil_mundos(P: np.ndarray, C: np.ndarray, p: np.ndarray) -> dict:
    """Todos os invariantes de conflito de um par (poset, conflito bruto)."""
    Cs = fechar_conflito(P, C)
    Ws = mundos(Cs)
    q = massa_mundos(Ws, p)
    n = len(P)
    viv = ~np.diag(Cs)
    npar = n * (n - 1) / 2 if n > 1 else 1
    Cnd = Cs.copy()
    np.fill_diagonal(Cnd, False)
    # conflito "sob teto comum": aresta de conflito entre classes com majorante
    # comum no poset — a assinatura do hedge (Λ)
    teto = 0
    for i in range(n):
        for j in range(i + 1, n):
            if Cnd[i, j] and (P[i] & P[j]).any():
                teto += 1
    return {
        "n_mundos": len(Ws),
        "we": _H(q),
        "b0_cons": b0_consistencia(Cs),
        "b1_ind": b1_independencia(Cs),
        "dens_c": float(Cnd.sum() / 2) / npar,
        "custo_fecho": custo_fecho(C, Cs),
        "frac_autoc": float((~viv).sum()) / n,
        "conflito_teto": teto,
        "massa_viva": float(p[viv].sum() / max(p.sum(), 1e-12)),
    }


# ----------------------------------------------------------- prova e validação


def _poset_aleatorio(rng, n: int, dens: float) -> np.ndarray:
    """Poset aleatório: relação esparsa sobre ordem topológica fixa + fecho."""
    R = np.eye(n, dtype=bool)
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < dens:
                R[i, j] = True
    for k in range(n):
        R |= np.outer(R[:, k], R[k, :])
    return R


def _mis_bruto(Cs: np.ndarray) -> list[list[int]]:
    """Referência independente: enumeração de TODOS os subconjuntos (n ≤ 14)."""
    n = len(Cs)
    vivos = [i for i in range(n) if not Cs[i, i]]
    out = []
    for m in range(1, 2 ** len(vivos)):
        S = [vivos[k] for k in range(len(vivos)) if m >> k & 1]
        if any(Cs[a, b] for i, a in enumerate(S) for b in S[i + 1:]):
            continue
        if any(all(not Cs[v, s] for s in S) for v in vivos if v not in S):
            continue                      # não maximal
        out.append(S)
    return out


def _ciclo(n: int) -> np.ndarray:
    C = np.zeros((n, n), bool)
    for i in range(n):
        C[i, (i + 1) % n] = C[(i + 1) % n, i] = True
    return C


def main() -> None:
    import common as E0
    import finite_space as F

    rng = np.random.default_rng(42)

    # ---------------------------------------------------------------- validação
    E0.banner("VALIDACAO 1 — mundos = MIS, contra enumeracao por forca bruta")
    dis = 0
    for t in range(400):
        n = int(rng.integers(3, 11))
        C = np.zeros((n, n), bool)
        for i in range(n):
            for j in range(i + 1, n):
                if rng.random() < 0.35:
                    C[i, j] = C[j, i] = True
        a = {tuple(w) for w in mundos(C)}
        b = {tuple(w) for w in _mis_bruto(C)}
        if a != b:
            dis += 1
    print(f"  400 grafos aleatorios (n 3-10): {dis} discordancias")

    E0.banner("VALIDACAO 2 — b1(Ind) contra os tipos de homotopia CONHECIDOS")
    print("  Ind(C_n): S^0 disjunto (n=4), S^1 (n=5), S^1 v S^1 (n=6), S^1 (n=7)")
    esperado = {4: (2, 0), 5: (1, 1), 6: (1, 2), 7: (1, 1)}
    ok = True
    for n, (b0e, b1e) in esperado.items():
        C = _ciclo(n)
        b0m, b1m = b0_consistencia(C), b1_independencia(C)
        st = "ok" if (b0m, b1m) == (b0e, b1e) else "ERRO"
        ok &= st == "ok"
        print(f"  Ind(C_{n}): esperado (b0={b0e}, b1={b1e})  medido "
              f"(b0={b0m}, b1={b1m})  {st}")
    Kn = np.ones((6, 6), bool)
    np.fill_diagonal(Kn, False)
    print(f"  Ind(K_6) = 6 pontos: b0 medido = {b0_consistencia(Kn)} "
          f"(esperado 6)")
    Z = np.zeros((6, 6), bool)
    print(f"  Ind(vazio) = simplexo: (b0, b1) medido = "
          f"({b0_consistencia(Z)}, {b1_independencia(Z)}) (esperado (1, 0))")

    E0.banner("VALIDACAO 3 — apos o fecho, todo mundo e fechado p/ generalizacao")
    viol = 0
    casos = 0
    for t in range(400):
        n = int(rng.integers(4, 11))
        P = _poset_aleatorio(rng, n, 0.25)
        C = np.zeros((n, n), bool)
        for i in range(n):
            for j in range(i + 1, n):
                if rng.random() < 0.25:
                    C[i, j] = True
        Cs = fechar_conflito(P, C)
        for W in mundos(Cs):
            Sw = set(W)
            casos += 1
            for u in W:
                acima = np.where(P[u] & ~Cs.diagonal())[0]
                if any(v not in Sw for v in acima):
                    viol += 1
                    break
    print(f"  400 posets x conflitos aleatorios, {casos} mundos: "
          f"{viol} violacoes de fechamento")
    print("  (a proposicao 'mundo = MIS' depende disto; o fecho de heranca e o")
    print("   que a garante — sem ele, MIS nao seriam configuracoes)")

    # ------------------------------------------------------------------- prova
    E0.banner("A SEPARACAO NOVA, POR CONSTRUCAO: conflito e invisivel a TUDO "
              "da fase F")
    print("  Duas anticadeias de 6 classes: TODOS os invariantes do artigo 1")
    print("  (SE, SE-nucleo, |P|, nucleo, b0, b1, chi, altura) sao IDENTICOS.")
    print("  So difere a relacao de conflito — que nenhum deles recebe.\n")

    n = 6
    A = F.rel_anticadeia(n)
    P, lab = F.reflexao_poset(F.fecho_transitivo(A))
    p = np.ones(len(P)) / len(P)
    C_comp = np.zeros((len(P), len(P)), bool)                 # tudo neutro
    C_conf = np.ones((len(P), len(P)), bool)                  # tudo conflita
    np.fill_diagonal(C_conf, False)

    cadeia = F.rel_cadeia(n)
    Pc, _ = F.reflexao_poset(F.fecho_transitivo(cadeia))
    pc = np.ones(len(Pc)) / len(Pc)
    C0c = np.zeros((len(Pc), len(Pc)), bool)

    # coroa (4 pts) + 2 isoladas; conflito entre as 2 especificas (minimos 0,1)
    R = np.zeros((6, 6), dtype=bool)
    R[:4, :4] = F.rel_coroa(2)
    np.fill_diagonal(R, True)
    Pk, labk = F.reflexao_poset(F.fecho_transitivo(R))
    pk = np.ones(len(Pk)) / len(Pk)
    Ck = np.zeros((len(Pk), len(Pk)), bool)
    Ck[labk[0], labk[1]] = Ck[labk[1], labk[0]] = True

    # Lambda (hedge): 2+2+2 amostras -> 3 classes: s1 # s2, ambas ⊑ g
    Rl = np.eye(6, dtype=bool)
    for a in (0, 1):                       # amostras 0,1 = s1
        for b in (4, 5):                   # amostras 4,5 = g
            Rl[a, b] = True
    for a in (2, 3):                       # amostras 2,3 = s2
        for b in (4, 5):
            Rl[a, b] = True
    Rl[0, 1] = Rl[1, 0] = Rl[2, 3] = Rl[3, 2] = Rl[4, 5] = Rl[5, 4] = True
    Pl, labl = F.reflexao_poset(F.fecho_transitivo(Rl))
    pl = np.array([(labl == c).sum() for c in range(len(Pl))], float)
    pl /= pl.sum()
    Cl = np.zeros((len(Pl), len(Pl)), bool)
    Cl[labl[0], labl[2]] = Cl[labl[2], labl[0]] = True        # s1 # s2

    fams = [
        ("escada (cadeia, sem conflito)", Pc, C0c, pc, cadeia),
        ("anticadeia COMPOSSIVEL (neutra)", P, C_comp, p, A),
        ("anticadeia CONFLITANTE", P, C_conf, p, A),
        ("coroa S^1 + 2 isoladas (s1#s2)", Pk, Ck, pk, R),
        ("LAMBDA/hedge: s1#s2 sob g", Pl, Cl, pl, Rl),
    ]
    print(f"  {'familia':34s} {'SE':>7s} {'SE-nuc':>7s} {'mundos':>7s} "
          f"{'WE':>7s} {'b0c':>4s} {'b1i':>4s}")
    print("  " + "-" * 78)
    for nome, Pf, Cf, pf, Rf in fams:
        _, labf = F.reflexao_poset(F.fecho_transitivo(Rf))
        se = F.entropia_semantica(labf)
        sen = F.entropia_nucleo(Pf, pf, ordens=8)
        prf = perfil_mundos(Pf, Cf, pf)
        print(f"  {nome:34s} {se:7.4f} {sen:7.4f} {prf['n_mundos']:7d} "
              f"{prf['we']:7.4f} {prf['b0_cons']:4d} {prf['b1_ind']:4d}")

    E0.banner("O QUE ISSO PROVA")
    print("  1. As duas anticadeias: SE, SE-nucleo e toda a fase F IDENTICOS;")
    print("     mundos 1 contra 6. Cegueira ao conflito, por construcao.")
    print("  2. O LAMBDA e o mecanismo da derrota do nucleo no TriviaQA: o")
    print("     nucleo colapsa o hedge (SE-nuc = 0) e destroi o sinal; os")
    print("     mundos preservam (2 mundos, WE > 0) e colapsam a elaboracao.")
    print("  3. A coroa: nucleo NAO distingue de anticadeia (6 = 6); mundos")
    print("     distinguem (2 contra 6).")

    E0.banner("CICLO DE CONFLITO: o b1 que a fase F nao podia ver — e seu limite")
    # CORRECAO REGISTRADA (2026-08-03). A versao anterior deste bloco afirmava
    # que b1(Ind) > 0 exigia >= 5 classes em ciclo induzido, com o pentagono
    # como witness minimo. E FALSO. Ind(C*) e o complexo de cliques do grafo de
    # CONSISTENCIA (o complemento), entao basta um ciclo induzido de 4 la —
    # equivalentemente, dois conflitos DISJUNTOS em C*. Witness minimo: quatro
    # classes com a#b e c#d, Ind = 4-ciclo a-c-b-d sem triangulo, b1 = 1, e
    # nenhum ciclo de conflito. Leitura semantica: duas incertezas binarias
    # independentes. Verificado por varredura exaustiva de todos os grafos com
    # n <= 5. O pentagono continua sendo o menor witness ENTRE CICLOS.
    n8 = 4
    P8 = np.eye(n8, dtype=bool)
    C8 = np.zeros((n8, n8), bool)
    C8[0, 1] = C8[1, 0] = C8[2, 3] = C8[3, 2] = True      # a#b, c#d (2K2)
    pr8 = perfil_mundos(P8, C8, np.ones(n8) / n8)
    print(f"  MINIMO — dois conflitos disjuntos (a#b, c#d): mundos = "
          f"{pr8['n_mundos']}  b0 = {pr8['b0_cons']}  b1(Ind) = {pr8['b1_ind']}")
    print("  (esperado: 4 mundos, b0 = 1, b1 = 1 — e ZERO ciclos de conflito)")
    n9 = 5
    P9 = np.eye(n9, dtype=bool)                    # anticadeia (sem ordem)
    C9 = _ciclo(5)
    pr9 = perfil_mundos(P9, C9, np.ones(n9) / n9)
    print(f"  pentagono de conflito (anticadeia): mundos = {pr9['n_mundos']}  "
          f"b0 = {pr9['b0_cons']}  b1(Ind) = {pr9['b1_ind']}")
    print("  (esperado: 5 mundos — os pares {i, i+2} —, b0 = 1, b1 = 1)")
    print("  Limite CORRETO: b1(Ind) > 0 exige um ciclo induzido >= 4 no grafo")
    print("  de CONSISTENCIA; entre ciclos de CONFLITO, o pentagono e o menor.")


if __name__ == "__main__":
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    main()

"""I1 — A CORRENTE DE ATRIBUIÇÃO e sua decomposição de Hodge.

A TESE, em uma frase:

    a família H6/H7 lê a incidência orador–frase mas ainda pontua UMA OPINIÃO POR
    VEZ; o resumo de uma audiência é um objeto CONJUNTO (~20 opiniões, ~6 oradores
    atribuídos, mediana 3 opiniões por orador), e a falha característica de um
    sumarizador — dar a Y o que X disse — CONSERVA as marginais, logo é uma
    CIRCULAÇÃO, logo é invisível a todo pontuador por-opinião.

O OBJETO. Por audiência, o grafo bipartido G = (O ⊔ A, E) com E = top-k oradores de
cada opinião mais a aresta atribuída. Duas correntes de arestas:

    J_α(o,a) = 1[a = α(o)]          o que o resumo AFIRMA
    J_ε(o,a) = π_o(a)               o que a transcrição SUSTENTA

e a discrepância D = J_α − J_ε. Por construção ∂D se anula em toda opinião (as duas
correntes emitem 1 unidade por opinião) e vale r(a) = crédito afirmado − crédito
merecido em cada orador.

A DECOMPOSIÇÃO (Hodge combinatório; Jiang, Lim, Yao & Ye 2011):

    D = grad φ  ⊕  h,     L_w φ = div_w D,     div_w h = 0

    grad φ  "este orador é sobre-creditado no geral"   — um potencial por vértice,
            visível a um detector por-opinião com contexto de orador
    h       "o crédito deveria CIRCULAR entre oradores, conservando os totais"
            — uma REATRIBUIÇÃO COERENTE, função do conjunto, e de mais nada

FATO ESTRUTURAL. G é bipartido ⟹ sem triângulos ⟹ o espaço de curl é trivial e
Z₁ = ker ∂ é inteiramente HARMÔNICO. Toda inconsistência cíclica aqui é global,
nunca local. (Em HodgeRank a decomposição tem três peças; a bipartição a reduz a
duas — simplificação, não perda.)

POR QUE ESCAPA DAS CINCO IMPOSSIBILIDADES: ver `i0_predicoes.md` §2. Em resumo:
sem métrica (E16); base com p≈12 e q≈20, não 2 partes (E24); fluxo, não sinal
(E25); dim Z₁ mediana 142 medida (F3); e o objeto é PONDERADO, não o complexo
binário cujo b₁ o i0 mediu ser 0 em 100% (I0 — a quinta, achado desta fase).

    python i1_corrente_atribuicao.py    # prova sintética + validação
"""
from __future__ import annotations

import numpy as np

# ------------------------------------------------------------------ construção


def grafo(M: np.ndarray, atr: np.ndarray, k: int = 5) -> list[tuple[int, int]]:
    """Arestas (o, a): os top-k oradores de cada opinião mais a aresta atribuída.

    Manter a atribuída mesmo fora do top-k é essencial: é exatamente o caso de
    má-atribuição que queremos ver, e podá-la apagaria o sinal."""
    q, p = M.shape
    E = set()
    kk = min(k, p)
    for o in range(q):
        for a in np.argsort(-M[o])[:kk]:
            E.add((o, int(a)))
        if atr[o] >= 0:
            E.add((o, int(atr[o])))
    return sorted(E)


def correntes(M: np.ndarray, atr: np.ndarray, E: list[tuple[int, int]],
              kappa: float = 1.5, modo: str = "posto") -> tuple:
    """(J_α, J_ε, w). π_o por POSTO — invariante a qualquer reparametrização
    monótona da similaridade (a única família com sinal na E15). `modo='softmax'`
    fica disponível como variante secundária, reportada mas não primária."""
    q = M.shape[0]
    por_o: dict[int, list[int]] = {}
    for i, (o, _) in enumerate(E):
        por_o.setdefault(o, []).append(i)
    Ja = np.zeros(len(E))
    Je = np.zeros(len(E))
    w = np.zeros(len(E))
    for o, idx in por_o.items():
        vals = np.array([M[o, E[i][1]] for i in idx])
        if modo == "posto":
            r = np.argsort(np.argsort(-vals))          # 0 = melhor
            pes = np.exp(-r / kappa)
        else:
            pes = np.exp((vals - vals.max()) / 0.05)
        pes = pes / pes.sum()
        for j, i in enumerate(idx):
            Je[i] = pes[j]
            Ja[i] = 1.0 if E[i][1] == atr[o] else 0.0
            # peso da aresta: confiança de que ela é comparável. Usamos o próprio
            # peso da evidência, com piso, para que arestas plausíveis dominem o
            # produto interno sem que as implausíveis saiam do espaço.
            w[i] = pes[j] + 0.05
        if atr[o] < 0:                                  # opinião sem orador casado
            Ja[idx] = Je[idx]                           # discrepância nula
    return Ja / max(q, 1), Je / max(q, 1), w


def hodge(E: list[tuple[int, int]], nq: int, npk: int, D: np.ndarray,
          w: np.ndarray) -> dict:
    """Decomposição de Hodge ponderada de D no grafo bipartido.

    B  = matriz de incidência (∂₁), orientação o → a
    L_w = B diag(w) Bᵀ            (laplaciano ponderado)
    φ   = L_w⁺ (B diag(w) D)      (potencial; L_w é singular — pseudo-inversa)
    grad = Bᵀ φ                   h = D − grad

    Garantias verificadas no `validar()`: div_w(h) = 0 e ⟨grad, h⟩_w = 0."""
    nv, ne = nq + npk, len(E)
    B = np.zeros((nv, ne))
    for i, (o, a) in enumerate(E):
        B[o, i] = -1.0
        B[nq + a, i] = +1.0
    L = B @ np.diag(w) @ B.T
    div = B @ (w * D)
    phi = np.linalg.pinv(L) @ div
    g = B.T @ phi
    h = D - g
    return {"B": B, "phi": phi, "grad": g, "h": h, "div": div,
            "dim_ciclo": ne - np.linalg.matrix_rank(B)}


def perfil(M: np.ndarray, atr: np.ndarray, k: int = 5,
           modo: str = "posto") -> dict:
    """Todas as features, por opinião e por audiência, de uma vez."""
    q, p = M.shape
    E = grafo(M, atr, k)
    Ja, Je, w = correntes(M, atr, E, modo=modo)
    D = Ja - Je
    H = hodge(E, q, p, D, w)
    h, g, phi = H["h"], H["grad"], H["phi"]
    idx_att = {}
    h_o = np.zeros(q)
    for i, (o, a) in enumerate(E):
        h_o[o] += h[i] ** 2
        if a == atr[o]:
            idx_att[o] = i
    nh = float(w @ (h ** 2))
    nd = float(w @ (D ** 2))
    return {
        "h_att": np.array([h[idx_att[o]] if o in idx_att else 0.0
                           for o in range(q)]),
        "g_att": np.array([g[idx_att[o]] if o in idx_att else 0.0
                           for o in range(q)]),
        "phi_spk": np.array([phi[q + atr[o]] if atr[o] >= 0 else 0.0
                             for o in range(q)]),
        "phi_op": phi[:q].copy(),
        "h_norm": np.sqrt(h_o),
        "r_spk": np.array([H["div"][q + atr[o]] if atr[o] >= 0 else 0.0
                           for o in range(q)]),
        "rho": nh / nd if nd > 1e-12 else 0.0,
        "dim_ciclo": int(H["dim_ciclo"]),
        "n_arestas": len(E),
    }


def superlotacao(N: np.ndarray) -> tuple[float, np.ndarray]:
    """A LACUNA DE SUPERLOTAÇÃO e os preços-sombra por opinião.

    `N[o,s]` = escore da opinião `o` contra a frase `s` (só as opiniões atribuídas
    a UM orador, contra as frases dos turnos dele).

        U = Σ_o max_s N[o,s]                   irrestrito — o que `cos_s` computa
        C = max_{σ injetiva} Σ_o N[o,σ(o)]     exclusivo — designação linear
        Δ = U − C ≥ 0                          a lacuna
        δ_o = max_s N[o,s] − N[o,σ*(o)]        preço-sombra: quem perde a disputa

    Δ = 0 sse cada opinião pode possuir uma frase distinta no seu próprio ótimo.
    Duas opiniões distintas não podem ambas ser *a* paráfrase da mesma frase — a
    impossibilidade é conjunta, e todo escore por-opinião a aprova."""
    from scipy.optimize import linear_sum_assignment
    q, t = N.shape
    if q == 0 or t == 0:
        return 0.0, np.zeros(q)
    melhor = N.max(1)
    if q == 1:
        return 0.0, np.zeros(1)
    if t < q:                       # menos frases que opiniões: impossível já aqui
        N = np.hstack([N, np.full((q, q - t), N.min() - 1.0)])
    li, co = linear_sum_assignment(-N)
    esc = N[li, co]
    delta = np.zeros(q)
    delta[li] = melhor[li] - esc
    return float(melhor.sum() - esc.sum()), delta


def defeito_hall(sup: np.ndarray) -> int:
    """Defeito de emparelhamento de Hall no bipartido opiniões × turnos de UM
    orador: max_S (|S| − |N(S)|). Por König–Egerváry, def = |O| − emparelhamento
    máximo; calculamos o emparelhamento por Hopcroft–Karp ingênuo (n pequeno).

    Leitura: um orador creditado com 4 opiniões cujos turnos só sustentam 2
    conteúdos distintos tem 2 opiniões que NÃO podem ser realizadas juntas."""
    q, t = sup.shape
    if q == 0 or t == 0:
        return q
    par = [-1] * t

    def tenta(o, vis):
        for j in range(t):
            if sup[o, j] and not vis[j]:
                vis[j] = True
                if par[j] < 0 or tenta(par[j], vis):
                    par[j] = o
                    return True
        return False

    m = sum(tenta(o, [False] * t) for o in range(q))
    return q - m


# ------------------------------------------------------- prova sintética + testes


def _cenario(q, p, M, atr):
    return perfil(np.asarray(M, float), np.asarray(atr, int), k=p)


def prova_sintetica() -> None:
    print("=" * 74)
    print("A SEPARAÇÃO CONSTRUTIVA — o que cada funcional lê")
    print("=" * 74)
    # 2 opiniões x 2 oradores, M SIMÉTRICA sob a troca de a1/a2:
    # toda feature por-opinião é idêntica nas duas configurações.
    M = np.array([[0.80, 0.80],
                  [0.80, 0.80]])
    for nome, atr in [("α = (a1, a2)  [diagonal]", [0, 1]),
                      ("α = (a2, a1)  [trocada] ", [1, 0]),
                      ("α = (a1, a1)  [ambas a1]", [0, 0])]:
        P = _cenario(2, 2, M, atr)
        print(f"  {nome}  cos_s=(0.80,0.80)  h_att = "
              f"({P['h_att'][0]:+.4f}, {P['h_att'][1]:+.4f})   "
              f"ρ = {P['rho']:.3f}")
    print("  -> M idêntica, cos_s idêntico, features por-opinião idênticas;")
    print("     h_att SEPARA a configuração 'ambas em a1' das simétricas.\n")

    # a testemunha do teorema: mudar α da OUTRA opinião muda h da primeira
    M2 = np.array([[0.90, 0.30],
                   [0.55, 0.55]])
    P1 = _cenario(2, 2, M2, [0, 0])
    P2 = _cenario(2, 2, M2, [0, 1])
    print("TESTEMUNHA DO TEOREMA (cegueira conjunta):")
    print("  opinião 1 fixa em a1 nas duas configurações; muda só α(o2).")
    print(f"    α(o2)=a1 :  h_att(o1) = {P1['h_att'][0]:+.5f}")
    print(f"    α(o2)=a2 :  h_att(o1) = {P2['h_att'][0]:+.5f}")
    dif = abs(P1["h_att"][0] - P2["h_att"][0])
    print(f"  |Δ| = {dif:.5f}  -> todo F(o1) = f(o1, α(o1), T) é IGUAL nas duas;")
    print("     h_att(o1) NÃO é. A cegueira é por construção.\n")

    # circulação pura: 3 oradores, troca cíclica
    M3 = np.array([[0.90, 0.40, 0.35],
                   [0.35, 0.90, 0.40],
                   [0.40, 0.35, 0.90]])
    for nome, atr in [("atribuição CORRETA (identidade)", [0, 1, 2]),
                      ("rotação cíclica (swap de 3)   ", [1, 2, 0]),
                      ("uma opinião fora do lugar     ", [1, 1, 2])]:
        P = _cenario(3, 3, M3, atr)
        print(f"  {nome}  ρ={P['rho']:.3f}  "
              f"‖h_att‖={np.linalg.norm(P['h_att']):.4f}  "
              f"‖g_att‖={np.linalg.norm(P['g_att']):.4f}")
    print("  -> a rotação cíclica é PURA circulação: conserva o crédito de todo")
    print("     orador (‖g‖≈0) e vive inteira na parte harmônica.\n")


def validar() -> None:
    print("=" * 74)
    print("VALIDAÇÃO — cada garantia contra uma referência independente")
    print("=" * 74)
    rng = np.random.default_rng(42)
    err_div, err_ort, err_som, err_dim, err_hall = [], [], [], [], []
    for _ in range(400):
        q = int(rng.integers(3, 14))
        p = int(rng.integers(2, 9))
        M = rng.random((q, p))
        atr = rng.integers(0, p, q)
        E = grafo(M, atr, k=int(rng.integers(2, p + 1)))
        Ja, Je, w = correntes(M, atr, E)
        D = Ja - Je
        H = hodge(E, q, p, D, w)
        B, h, g = H["B"], H["h"], H["grad"]
        err_div.append(np.abs(B @ (w * h)).max())          # div_w(h) = 0
        err_ort.append(abs(float((w * g) @ h)))            # <grad,h>_w = 0
        err_som.append(np.abs(g + h - D).max())            # soma exata
        # dim do espaço de ciclos por referência independente: |E|-|V|+b0
        nv = len({o for o, _ in E}) + len({a for _, a in E})
        pai = {}

        def ach(x):
            while pai.get(x, x) != x:
                pai[x] = pai.get(pai[x], pai[x])
                x = pai[x]
            return x
        for o, a in E:
            u, v = ach(("o", o)), ach(("a", a))
            pai.setdefault(u, u)
            pai.setdefault(v, v)
            if u != v:
                pai[u] = v
        b0 = len({ach(x) for x in
                  [("o", o) for o, _ in E] + [("a", a) for _, a in E]})
        err_dim.append(abs(H["dim_ciclo"] - (len(E) - nv + b0)))
        # Hall: def = |O| - emparelhamento, contra busca exaustiva de max_S
        if q <= 7 and p <= 6:
            sup = M[:, :p] > 0.5
            d1 = defeito_hall(sup)
            d2 = 0
            for msk in range(1, 1 << q):
                S = [i for i in range(q) if msk >> i & 1]
                N = set()
                for i in S:
                    N |= set(np.where(sup[i])[0].tolist())
                d2 = max(d2, len(S) - len(N))
            err_hall.append(abs(d1 - d2))
    lin = [
        ("div_w(h) = 0", "definição de harmônico (livre de divergência)",
         len(err_div), max(err_div)),
        ("<grad, h>_w = 0", "ortogonalidade do teorema de Hodge",
         len(err_ort), max(err_ort)),
        ("grad + h = D", "a decomposição é exata, não aproximada",
         len(err_som), max(err_som)),
        ("dim Z_1", "|E| - |V| + b0 por union-find independente",
         len(err_dim), max(err_dim)),
        ("defeito de Hall", "max_S (|S|-|N(S)|) por força bruta em 2^q",
         len(err_hall), max(err_hall) if err_hall else 0),
    ]
    print(f"  {'garantia':18s} {'referência independente':44s} {'casos':>6s} "
          f"{'erro máx':>10s}")
    print("  " + "-" * 82)
    for a, b, c, d in lin:
        print(f"  {a:18s} {b:44s} {c:6d} {d:10.2e}")
    print()
    # curl trivial: um grafo bipartido não tem triângulos
    print("  fato estrutural: G bipartido ⟹ 0 triângulos ⟹ curl trivial ⟹")
    print("  Z_1 é INTEIRAMENTE harmônico (toda inconsistência é global).")
    print()


if __name__ == "__main__":
    prova_sintetica()
    validar()

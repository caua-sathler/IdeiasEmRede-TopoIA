# J0 — Registro de predições: fidelidade é CONTINUIDADE

**Data: 2026-08-03.** Escrito ANTES de qualquer AUROC do invariante novo.

---

## 1. A tese, em três frases

A fase I fechou com um diagnóstico: os invariantes conjuntos eram funcionais da
**mesma matriz `M`** que a família por-opinião já resume — acoplamento novo,
informação nenhuma. Para bater o comitê é preciso uma **fonte exógena**.

Existe uma, e ela estava no enunciado da tarefa o tempo todo: **o resumo é uma
SEQUÊNCIA e a transcrição é uma SEQUÊNCIA**. Nenhum método deste projeto, nenhum
método da literatura, e — decisivamente — **nenhum juiz LLM que leia uma opinião por
vez** tem acesso à posição de uma opinião relativa às outras.

E a estrutura é real: medido no j0, o τ de Kendall entre a ordem do resumo e a
posição do suporte é **+0,3376** global e **+0,5982 (mediana +0,7471)** restrito aos
turnos do orador atribuído, contra **−0,0010** sob permutação.

## 2. A forma topológica: alucinação é uma descontinuidade

Por **Alexandrov**, uma ordem total finita é um espaço topológico, e um mapa entre
ordens totais finitas é **contínuo se e só se é monótono**. O resumo afirma um mapa

    ρ : (O, ordem do resumo)  ⟶  (T, ordem do tempo)

que leva cada opinião à posição do trecho que a sustenta. **Um resumo fiel é um mapa
contínuo.** Uma opinião alucinada não tem posição verdadeira: ela é inserida onde o
sumarizador quis, e **quebra a monotonicidade localmente** — é literalmente um ponto
de descontinuidade.

Isto é o teorema da fase F com a ordem **exógena** (o tempo do debate) no lugar da
**endógena** (o acarretamento lido pelo próprio NLI). A fase F provou que um
sumarizador é contínuo sse preserva especificidade e mediu ganho nulo; o diagnóstico
da fase I explica por quê — a ordem de acarretamento vem do mesmo verificador que já
era o baseline. A ordem do tempo não vem de verificador nenhum.

## 3. O invariante: a obstrução de alinhamento monótono

Para o orador `a` com opiniões atribuídas `o_1 < … < o_k` (ordem do resumo) e frases
`j_1 < … < j_m` (ordem do tempo), com `N[i,t] = cos(o_i, s_{j_t})`:

```
V_livre  = Σ_i max_t N[i,t]                            cada opinião no seu ótimo
V_mono   = max_{t_1 ≤ t_2 ≤ … ≤ t_k} Σ_i N[i,t_i]      o melhor alinhamento CONTÍNUO
Ω_a      = V_livre − V_mono ≥ 0                        a OBSTRUÇÃO do orador
```

`V_livre` é exatamente o que `cos_s` computa, por opinião. `V_mono` é o que uma
leitura **contínua** do turno consegue sustentar. A diferença é a obstrução a
estender a atribuição a um mapa contínuo — e é **zero se e só se** as opiniões de `a`
podem todas ser lidas na ordem em que o resumo as apresenta.

Por opinião, três leituras, todas funções de `α` e da ordem nas **outras** opiniões:

- **preço-sombra** `g_i = max_t N[i,t] − N[i, t_i*]` — quanto `o_i` perde para caber;
- **deslocamento** `d_i = |t_i* − argmax_t N[i,t]| / m` — quanto teve de se mover;
- **marginal deixando-um-fora** `μ_i = (V_mono^{-i} + max_t N[i,t]) − V_mono` — o
  custo de **incluir** `o_i` na cadeia contínua. É a obstrução a estender a seção
  monótona de `O∖{o_i}` para `O`, no sentido literal de teoria de obstrução.

Custo: DP em `O(k·m)` com máximo-prefixo, e `k+1` execuções para os marginais. **Zero
chamadas de modelo.**

**Teorema (cegueira à ordem, mesma forma do i1).** Todo pontuador
`F(o) = f(o, α(o), T)` — o que inclui todo escore agregado, toda a família H6/H7/I, e
**todo juiz LLM que leia uma opinião por vez** — é invariante a qualquer permutação
da ordem em que o resumo apresenta as outras opiniões. `g_i`, `d_i` e `μ_i` não são.
Testemunha: duas opiniões do mesmo orador com posições de suporte trocadas.

## 4. Por que escapa das SEIS impossibilidades medidas

| impossibilidade | por que não morde |
|---|---|
| E16 concentração de medida | nenhum predicado métrico em ℝ⁷⁶⁸; só a ORDEM das posições |
| E24 limite de Dowker | não é nervo de 2 partes |
| E25 balanço vacuoso | não é grafo com sinal |
| F3 esparsidade | não é `b₁` de poset esparso |
| I0 densidade | não é o complexo de incidência binária |
| **I-exclusividade** | a restrição de **injetividade** não mordia (`g_lot=0` em 86,8%); a de **monotonicidade** é muito mais forte — τ dentro do orador é 0,75, então a ordem realmente restringe |

E, crucialmente, escapa do **diagnóstico da fase I**: `t_i*` depende da ordem do
resumo, que **não está em `M`**. É informação exógena, não um funcional novo de `M`.

## 5. Predições registradas

**P1 (sanidade).** Reproduzir `cos_s = 0,7455` e o τ do j0 (+0,5982 dentro do orador).

**P2 (o sinal isolado).** `g_i` ou `μ_i` tem AUROC contra o rótulo humano **≥ 0,60**.
(As features cruas do j0 deram 0,52–0,57; a predição é que o alinhamento monótono
completo é estritamente mais informativo que o deslocamento de posto.)

**P3 (o controle que decide).** Sob **permutação da ordem do resumo dentro do
orador** — mesma `M`, mesmas opiniões, mesmos turnos, só a ordem destruída — todas as
features caem para o acaso. Se não caírem, o sinal é do alinhamento e não da ordem,
e o veredito é nulo.

**P4 (complementaridade).** A camada de continuidade soma à base
(família H6/H7 + n_irm + Hodge) fora da amostra, com IC agrupado por audiência
excluindo zero, **e** sobrevive ao braço com ordem permutada.

**P5 (a aposta — o estado da arte).** A camada de continuidade **soma ao comitê dos
12 juízes** (0,9245), onde a família de incidência (+0,0013 ns) e a camada de Hodge
(−0,0021 ns, e −0,0039\* em combinação) **falharam**. A justificativa mecanística é
específica e forte: os juízes leem uma opinião por vez e **não têm como saber onde
ela está em relação às outras** — a informação é literalmente inacessível a eles, ao
contrário de tudo que testamos antes, que era função da mesma `M` que eles também
leem. Se falhar, entra em `RESULTADOS_J.md` com o mesmo destaque.

## 6. Controles fixados

1. Reprodução do H6 antes de qualquer número novo.
2. **Ordem permutada dentro do orador** (P3) — o análogo do orador aleatório do h6b.
3. Baseline trivial declarado: `desloc`, `n_tur` e `disp` do j0 (0,52–0,57). A camada
   monótona tem de bater **isso**, não só o acaso.
4. Inferência agrupada por audiência em tudo; combinações sempre OOF (GroupKFold).
5. Confronto primário declarado: **P5**. P4 é secundário; o resto é diagnóstico.

## 7. O que decide continuar ou parar

- P3 falha → o sinal não é da ordem; escrever o nulo e parar.
- P5 passa → **é o resultado**: a primeira coisa neste projeto que soma ao comitê.
- P5 falha e P4 passa → ganho no orçamento barato, sem estado da arte; reportar assim.

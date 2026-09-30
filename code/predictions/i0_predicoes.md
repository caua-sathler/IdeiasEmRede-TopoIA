# I0 — Registro de predições: a corrente de atribuição e sua decomposição de Hodge

**Data de registro: 2026-08-03.** Escrito ANTES de qualquer AUROC do invariante novo.
Predições imutáveis; o que os dados disserem entra em `RESULTADOS_I.md`, não aqui.
(Regra herdada das fases F e H: predição registrada → medição → veredito.)

---

## 1. A tese, em três frases

A fase H mostrou que a agregação global destrói a **incidência orador–frase**, e que
lê-la vale +0,18 de AUROC. Mas a família H6/H7 ainda pontua **uma opinião por vez**:
toda feature é função da linha `o` da matriz de suporte. Esta fase parte da observação
de que o resumo estruturado de uma audiência é um **objeto conjunto** — ~20 opiniões
distribuídas entre ~6 oradores atribuídos, mediana de **3 opiniões por orador** — e que
a falha característica de um sumarizador não é errar uma opinião isolada, é
**redistribuir crédito**: dar a Y o que X disse.

Redistribuição que conserva os totais é, literalmente, uma **circulação** — um ciclo no
grafo bipartido opiniões × oradores. É invisível a qualquer pontuador por-opinião
porque as marginais não mudam. O objeto que a isola é clássico e nunca foi importado
para verificação factual: a **decomposição de Hodge combinatória** de um fluxo de
arestas (Jiang, Lim, Yao & Ye, *Math. Programming* 2011).

## 2. Por que escapa das CINCO impossibilidades medidas

| impossibilidade | mecanismo medido | por que não morde aqui |
|---|---|---|
| E16 concentração de medida | `opp8=0,000`; `dim8≈6,2/8` | nenhum predicado métrico em ℝ⁷⁶⁸: só uma matriz de escores virando fluxo; com pesos por **posto**, invariante a reparametrização monótona |
| E24 limite de Dowker | mediana 2 partes ⟹ `H¹≡0` | o espaço base tem `p≈12` oradores e `q≈20` opiniões, não 2 partes |
| E25 balanço vacuoso | 0/55 arestas negativas (corpus curado) | audiência é **debate**; e o invariante não é de sinal, é de fluxo |
| F3 esparsidade do poset | `b₁>0` em 0,31–1,7% | **medido no I0: `dim Z₁` mediana 142 por audiência, em 100% delas** |
| **I0 densidade (nova)** | **`b₁(Dowker)=0` em 100%; grau médio 9 de 12** | a rota **combinatória binária** morre aqui; a construção usa o objeto **ponderado**, para o qual densidade é a favor (mais ciclos), não contra |

A quinta é achado desta fase e **é reportada como impossibilidade**, não escondida: a
homologia do complexo de incidência binária é vazia por densidade. O que sobrevive é o
fluxo.

## 3. Definições (fixadas antes de medir)

Por audiência, com `O` = opiniões com rótulo, `A` = oradores com turno, `α : O → A` a
atribuição que o resumo afirma, e `M[o,a] = max_{s ∈ T_a} cos(o, s)` (a matriz que o
h6 já computa):

- **Grafo base** `G`: bipartido, arestas = (top-`k` oradores de cada opinião) ∪ (aresta
  atribuída). Orientação `o → a`. Sem triângulos por bipartição.
- **Corrente afirmada** `J_α(o,a) = 1[a = α(o)]`.
- **Corrente da evidência** `J_ε(o,a) = π_o(a)`, com `π_o` distribuição sobre oradores.
  Primária: **por posto**, `π_o(a) ∝ exp(−rank_o(a)/κ)` — invariante a qualquer
  reparametrização monótona da similaridade (a única família com sinal na E15).
  Secundária: softmax em `M` (reportada, não primária).
- **Discrepância** `D = J_α − J_ε ∈ C₁(G)`. Por construção `∂D` se anula em toda
  opinião (cada uma emite exatamente 1 unidade nas duas correntes) e vale
  `r(a) = |α⁻¹(a)| − Σ_o π_o(a)` em cada orador: o **resíduo de crédito**.
- **Decomposição de Hodge** com produto interno ponderado por `w(o,a)`:
  `D = grad φ + h`, onde `L_w φ = ∂D` e `∂h = 0`.
  - `grad φ` — a parte explicável por um **potencial por vértice**: "este orador é
    sistematicamente sobre-creditado". Um detector por-opinião com contexto de orador
    pode vê-la.
  - `h` — a parte **livre de divergência**: circulação pura, uma **reatribuição
    coerente que conserva os totais de todo orador**.
- **Fato estrutural**: `G` é bipartido, logo **sem triângulos**, logo o espaço de curl
  é trivial e `Z₁ = ker ∂` é inteiramente **harmônico**. Toda inconsistência cíclica
  aqui é global, nunca local. (Em HodgeRank, curl e harmônico se separam; aqui a
  bipartição colapsa a decomposição de três para duas peças — simplificação, não perda.)
- **Features por opinião**: `h_att = h(o, α(o))`, `g_att = grad φ(o, α(o))`,
  `phi_spk = φ(α(o))`, `r_spk = r(α(o))`, `h_norm_o = ‖h|_{arestas de o}‖`.
- **Feature por audiência**: fração harmônica `ρ = ‖h‖²/‖D‖²`.
- **Defeito de emparelhamento (companheiro, exploratório)**: para cada orador `a`, o
  defeito de Hall `def(a) = max_{S ⊆ α⁻¹(a)} (|S| − |N(S)|)` no grafo bipartido entre
  as opiniões atribuídas a `a` e os seus turnos. Conta quantas opiniões de `a` **não
  podem ser simultaneamente realizadas** por turnos distintos.

## 4. O teorema que o desenho aposta (a ser provado no i1)

> **Cegueira conjunta.** Seja `F` qualquer pontuador que atribua a cada opinião um valor
> função apenas de `(o, α(o), transcrição)` — o que inclui todo escore agregado de
> similaridade/NLI, toda a família H6/H7, e **todo juiz LLM que leia uma opinião por
> vez**. Então existem duas audiências com o mesmo `M`, os mesmos valores de `F` em
> todas as opiniões, e componentes harmônicas `h` distintas. Testemunha: 2 opiniões × 2
> oradores com atribuição trocada e `M` simétrica sob a troca.

É o argumento §2.4 do `REPORT_GUARDA_NERVO` um nível acima do H6: lá a permutação
destruía orador↔frase; aqui a pontuação independente destrói opinião↔opinião.

**Contraponto declarado na literatura**: MACI (arXiv 2602.01285) mede que pontuar as
afirmações de um resumo *em conjunto* empata com pontuá-las independentemente. Eles
testaram "conjunto" = dar todas ao LLM. O teorema acima diz que isso não decide nada:
um LLM que recebe o conjunto ainda emite decisões por afirmação. A questão é se existe
um **funcional conjunto** que nenhuma decisão por afirmação computa — e `h` é um.

## 5. Predições registradas

**P1 (sanidade).** A matriz `M` reconstruída reproduz `cos_s = 0,7455` e
`cos_g = 0,5676` no subconjunto casado (n=3630). Se não reproduzir, há bug e nada
abaixo conta.

**P2 (o objeto existe).** Fração harmônica média `ρ ≥ 0,10`; `dim Z₁` mediana ≥ 50.
(O I0 já mediu `dim Z₁` = 142; esta predição é sobre a discrepância REAL viver
fora do espaço de gradientes.)

**P3 (o sinal isolado).** `h_att` sozinha tem AUROC contra o rótulo humano
**entre 0,60 e 0,72** — abaixo de `cos_s` (0,7455), porque é um resíduo depois de
remover a parte forte. Se der ≥ 0,7455 sozinha, desconfiar de vazamento e checar.

**P4 (complementaridade — a alegação principal).** As features de Hodge somam à
família de incidência fora da amostra: **0,7792 → ≥ 0,79**, pareado com IC excluindo
zero (bootstrap agrupado por audiência).

**P5 (a aposta forte — o estado da arte).** As features de Hodge somam ao **comitê dos
12 juízes**, onde a família H6/H7 falhou (+0,0015 ns). Predição registrada:
**Δ > 0 com IC excluindo zero**. É a predição com maior chance de falhar e a única que
justificaria "novo estado da arte" sem qualificação de orçamento. Se falhar, entra em
`RESULTADOS_I.md` com o mesmo destaque das que passarem.

**P6 (o controle que decide — a lição da E22).** Atribuição **embaralhada** dentro da
audiência (mesma `M`, mesmo grafo, `α` permutada):
(a) a energia harmônica sobe — resumos reais são mais consistentes que aleatórios;
(b) o AUROC de `h_att` colapsa para o acaso.
Se real e embaralhado forem indistinguíveis, a estrutura não carrega e o veredito é
nulo — sétima vez do padrão, se ocorrer.

**P7 (estrutura vs escalar — a segunda lição da E22).** `h_att` bate ou soma sobre a
sua própria sombra escalar: o resíduo por-orador (`cos_s` menos a média dos `cos_s` do
mesmo orador na audiência), que é exatamente a parte de gradiente. Se o gradiente
sozinho fizer o mesmo trabalho, a homologia não está pagando.

**P8 (defeito de emparelhamento — exploratório).** `def(a) > 0` concentra alucinação
entre as opiniões de `a`. Rotulado exploratório: o defeito é por orador, não por
opinião, e a atribuição do rótulo dentro do conjunto violador é ambígua.

## 6. Controles fixados

1. **Reprodução do H6 antes de qualquer número novo** (P1).
2. **Atribuição embaralhada** (P6) — o análogo do grafo aleatório da E22 e do orador
   aleatório do H6b.
3. **Gradiente vs harmônico** (P7): a decomposição é ortogonal por construção, então a
   comparação é limpa; reportar as duas metades sempre juntas.
4. **Inferência agrupada por audiência** em tudo (o bootstrap i.i.d. por linha é
   otimista; lição do h6b).
5. **Combinações sempre fora da amostra** (GroupKFold por audiência).
6. **Regra do n**: nada abaixo de n≈500 vira manchete; `n=3630` aqui, então o problema
   é multiplicidade, não poder. Confrontos primários declarados: **P4 e P5**. Todo o
   resto é secundário/exploratório e será rotulado assim.

## 6-bis. ADENDO REGISTRADO (mesmo dia, APÓS a primeira rodada do i2)

A primeira rodada mediu: P1 exata; P2 folgada (ρ=0,64; dim Z₁=70); P3 dentro da
faixa (`h_att` 0,6555); **P7 passou de forma limpa** (harmônico 0,6555 contra
gradiente 0,4476 — *abaixo* do acaso); **P6 passou** (embaralhado 0,5349;
pareado +0,1208 [+0,0809, +0,1608]); e **P5 falhou** (comitê 0,9245 → 0,9235, ns).
A P4 teve o seu controle **invalidado por erro meu** (o braço embaralhado
reaproveitava 4 das 6 colunas do perfil real) e foi refeita.

O adendo é uma extensão declarada da mesma teoria, motivada por um modo de falha
**distinto** do que a parte harmônica captura, com predição escrita antes de medir.

**O modo de falha.** A componente harmônica vê *troca* — crédito no orador errado,
totais conservados. Não vê **superlotação**: creditar 4 opiniões a um orador que fez
2 pontos. Aí cada opinião tem, isoladamente, um bom casamento (o mesmo!), e todo
escore por-opinião aprova. A impossibilidade é conjunta e **exclusiva**: duas
opiniões distintas não podem ambas ser *a* paráfrase da mesma frase.

**O objeto.** Para o orador `a` com opiniões atribuídas `O_a` e frases `T_a`, seja
`N[o,s] = cos(o,s)`. Duas avaliações:

- **irrestrita** `U = Σ_o max_s N[o,s]` — exatamente o que `cos_s` computa, por opinião;
- **exclusiva** `C = max_{σ injetiva} Σ_o N[o,σ(o)]` — o problema de designação linear.

A **lacuna de superlotação** `Δ_a = U − C ≥ 0` é zero se e só se cada opinião pode
possuir uma frase distinta no seu ótimo. Por opinião, o **preço-sombra**
`δ_o = max_s N[o,s] − N[o,σ*(o)]` localiza quem perde a disputa. É o dual do
politopo de transporte — a geometria do mesmo objeto de fluxo, uma dimensão acima
do grafo bipartido.

`Δ_a` e `δ_o` são funções de `α` restrita às **outras** opiniões: o mesmo teorema de
cegueira conjunta se aplica, com a mesma testemunha.

**P9 (superlotação, isolada).** `δ_o` tem AUROC contra o rótulo humano **≥ 0,58**.
**P10 (superlotação, complementaridade — confronto primário do adendo).** A camada
de superlotação soma à família H6/H7 **mais** Hodge, fora da amostra, com IC
agrupado excluindo zero.
**P11 (o controle).** Sob atribuição embaralhada `δ_o` cai para o acaso, e o ganho
da P10 desaparece contra o braço embaralhado. Se não cair, é artefato de contagem
(quantas opiniões o orador tem) e não de identidade — e nesse caso o controle
correto é o número de opiniões por orador sozinho, que também será reportado.

## 6-ter. SEGUNDO ADENDO (mesmo dia, após a segunda rodada do i2)

A segunda rodada, com o controle corrigido: P4 **passou** (+0,0091 [+0,0013,
+0,0167]); P6(b) **passou decisivamente** (h_att 0,6555 contra 0,5349 embaralhado;
+0,1208 [+0,0809, +0,1608]); P7 **passou de forma limpa** (harmônico 0,6555 contra
gradiente 0,4476, *abaixo* do acaso); **P9/P10 falharam** e o mecanismo está medido
(`g_lot = 0` em **86,8%** — turnos são longos, a restrição de exclusividade não
morde); **P11 no nível do modelo empatou** (+0,0036 [−0,0055, +0,0117]); **P5
falhou** e chega a diluir (−0,0039* sobre comitê+família).

### A moldura que emergiu, e a terceira obstrução

O resumo afirma um **mapa** `α : O → A`. Fidelidade é a afirmação de que `α` é
**induzido pela evidência**. As obstruções a isso são de três tipos, e cada uma é
invisível a qualquer pontuador por-opinião:

| obstrução | falha de `α` como | invariante | status |
|---|---|---|---|
| circulação | fluxo consistente | componente **harmônica** | real (0,6555; controle 0,5349) |
| superlotação | injetividade suficiente | lacuna de **designação** | **refutada**: não morde (86,8% zero) |
| **duplicação** | **morfismo (preserva estrutura em `O`)** | **discrepância `O`↔`A`** | a testar |

A terceira: opiniões carregam uma estrutura de similaridade entre si, que **nada
neste projeto jamais computou**. Se `o₁` e `o₂` são quase idênticas mas atribuídas a
oradores diferentes, ou os dois disseram a mesma coisa (possível num debate), ou uma
é duplicata má-atribuída — e a **evidência decide**: se o suporte das duas vem dos
turnos do MESMO orador, a segunda atribuição é infundada. É o modo de falha que a
literatura nomeia como *"summarization models merge viewpoints"*.

**P12 (duplicação, isolada).** `dup = max_{o'≠o} [ sim(o,o') · 1(α(o')≠α(o)) ·
concordância das evidências ]` tem AUROC ≥ 0,58 contra o rótulo humano.
**P13 (duplicação, complementaridade).** Soma à base (família + n_irm + Hodge) com
IC agrupado excluindo zero, e sobrevive ao braço com atribuição embaralhada.
**P14 (guarda — a moldura da E26).** Entre as opiniões que o **comitê dos 12
aprova**, a camada conjunta concentra os erros restantes com *lift* > 1, IC
excluindo 1,0. Esta é a leitura que a E26 validou para um sinal que não vence como
classificador; declarada exploratória e reportada com o *lift* e a captura, não só
com AUROC.

## 7. O que decide continuar ou parar

- P1 falha → bug; consertar antes de tudo.
- P6 falha (embaralhado indistinguível) → a corrente não carrega informação de
  atribuição; escrever o nulo com mecanismo e parar.
- P4 e P5 falham ambas → a decomposição é real mas não paga; reportar como
  **decomposição diagnóstica** (o gênero da lei de conflação), não como detector.
- P4 passa e P5 falha → ganho dentro do orçamento barato, sem estado da arte absoluto;
  reportar exatamente assim, como a fase H fez.
- **P5 passa → é o resultado.**

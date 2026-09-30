# H0 — Registro de predições: a topologia da consistência (estruturas de eventos semânticas)

**Data de registro: 2026-08-03.** Este documento é escrito ANTES de qualquer AUROC ser
computado sobre os invariantes novos. As predições abaixo são imutáveis; o que os dados
disserem depois entra nos documentos de resultados, não aqui. (Regra herdada da fase F:
predição registrada → medição → veredito, nunca o contrário.)

---

## 1. A tese, em três frases

O artigo dos espaços finitos provou que a entropia semântica descarta a **ordem** do
acarretamento. Esta fase parte da observação de que ela — e todos os sucessores —
descartam uma **segunda** estrutura: a distinção entre **contradição** (não há mundo em
que ambas valham) e **neutralidade** (podem ser ambas verdadeiras). Para a SE, os dois
casos são o mesmo "não equivalente"; para o KLE, contradição é um **número** (peso 0,
contra 0,5 do neutro) e não uma **obstrução**; para o LGU, é um escalar de densidade.

O objeto que carrega (ordem + conflito + herança de conflito) é clássico e nunca foi
importado para PLN/UQ: **estrutura de eventos** (Winskel, teoria da concorrência), cujas
**configurações** (conjuntos fechados-para-cima sem conflito interno) são exatamente
**estados de crença consistentes**, e cujas configurações maximais são os **mundos
possíveis** que o conjunto de respostas sustenta.

A forma topológica: os conjuntos livres de conflito formam o **complexo de independência**
`Ind(C*)` do grafo de conflito fechado; os **mundos são as suas facetas**; por dualidade
de Dowker, o **nervo do recobrimento por mundos** tem o mesmo tipo de homotopia de
`Ind(C*)`. A homologia desse complexo — não a do complexo de ordem — é onde mora o
conflito.

## 2. Por que escapa das quatro impossibilidades medidas

| impossibilidade | por que não morde aqui |
|---|---|
| E16 concentração de medida | nenhuma métrica: só as relações ⊑ e # do NLI |
| E24 limite de dimensão de Dowker | o nervo aqui é sobre **mundos** (2–6+ vértices), não sobre 2 partes de claim |
| E25 balanço vacuoso (corpus curado) | amostras de um modelo **não são curadas** — conflitos existem (30% dos pares no TriviaQA) |
| F3 esparsidade (b₁ do poset) | conflito é um padrão de **2 pontos** (uma aresta), não um ciclo de 4 |

## 3. Definições (fixadas antes de medir)

Sobre as classes do poset `P` (reflexão da pré-ordem de acarretamento, como na fase F):

- **Conflito bruto** `C[u,v]` = 1 se `max(P_con(u→v), P_con(v→u)) ≥ TAU_CON = 0,50`
  (mesmo limiar do f12; simétrico por construção).
- **Fecho de herança** `C* = bool(P·C·Pᵀ)`: se `u ⊑ v`, `w ⊑ v'` e `v # v'`, então
  `u # w` (quem contradiz o geral contradiz todo refinamento dele). É o axioma de
  estrutura de eventos, na direção semântica correta. A fração de arestas acrescentadas
  é o **custo do fecho de conflito** — diagnóstico análogo à não-transitividade.
- **Autoconflito** `diag(C*)`: classe que conflita com um ancestral próprio. É
  incoerência do verificador (evento impossível); excluída dos mundos, taxa reportada.
- **Grafo de consistência** = complemento de `C*`. **Mundos** = conjuntos independentes
  maximais de `C*` (= cliques maximais da consistência). Proposição (provada no h1 por
  teste): após o fecho, todo mundo é automaticamente fechado para generalização — o
  fecho é exatamente o que torna "mundo = MIS" bem definido.
- **Massa de mundo**: `q(W) ∝ Σ_{u∈W} p(u)/m(u)`, onde `m(u)` = nº de mundos que contêm
  `u` (rateio igual; conserva massa). **Entropia de mundos** `WE = H(q)`.
- **Invariantes topológicos**: `b₀(cons)` = componentes do grafo de consistência
  (blocos mutuamente irreconciliáveis); `b₁(Ind)` = ciclos do complexo de independência
  (conflito cíclico: específicos mutuamente exclusivos, reconciliáveis dois a dois em
  generalidade intermediária, sem reconciliação comum).
- **Densidade de conflito** `dens_c` = fração de pares de classes em `C*` — o escalar
  à la LGU-InS, que serve de **controle**: se mundos ≈ densidade em toda parte, a
  estrutura não paga (lição da E22: o ganho tem de sobreviver ao controle de grafo).

## 4. A separação sintética (o que o h1 tem de exibir)

Com N=6 e seis classes, a coluna nova separa o que TODAS as colunas do artigo 1 não
separam:

| família | SE | SE-núcleo | mundos | WE |
|---|---|---|---|---|
| escada (cadeia, sem conflito) | log 6 | 0 | **1** | **0** |
| anticadeia **compossível** (tudo neutro) | log 6 | log 6 | **1** | **0** |
| anticadeia **conflitante** (tudo conflita) | log 6 | log 6 | **6** | **log 6** |
| coroa (2 específicas em conflito) | log 6 | log 6 | **2** | baixo |
| **Λ (hedge)**: 2 específicas conflitantes sob 1 geral | log 3 | **0** ← colapsa! | **2** | **> 0** |

A linha Λ é o mecanismo exato da derrota do SE-núcleo no TriviaQA (−0,015): o núcleo de
Stong colapsa o hedge (o geral absorve as específicas em conflito), destruindo o sinal
de incerteza. Os mundos **preservam** o conflito enquanto colapsam a elaboração. As duas
anticadeias são o caso em que **toda** a maquinaria do artigo 1 (SE, núcleo, b₀, b₁, χ̃,
altura) é constante e os mundos vão de 1 a 6 — cegueira ao conflito, por construção.

## 5. Predições registradas

**P1 (sanidade, TriviaQA n=233, cache f12).** A reprodução da SE a partir do cache dá
AUROC ≈ 0,811 (o número do f12). Se não der, há bug no meu pipeline e nada abaixo conta.

**P2 (estrutura, TriviaQA).** Conflitos vivem fora da ordem: a maioria esmagadora das
arestas de `C*` liga classes ⊑-incomparáveis. O custo do fecho de herança é < 10%
(mesma ordem da não-transitividade já medida, 0,37% em QA curta) e a taxa de
autoconflito é < 5%.

**P3 (o confronto principal, TriviaQA).** Pareado contra a SE:
`Δ(WE − SE) > Δ(SE-núcleo − SE) = −0,0149`. Isto é, a correção sensível a conflito
**não perde** como a correção cega a conflito perdeu. Predição forte (registrada como
esperança, não como aposta): `Δ(WE − SE) ≥ 0`, porque o WE colapsa elaboração e
compossibilidade (raras aqui) e preserva hedging (frequente aqui). Um empate
(IC contendo 0, sem a perda sistemática do núcleo) já falsifica "colapsar sempre
destrói sinal" e confirma o mecanismo Λ.

**P4 (estrutura > escalar, TriviaQA).** `WE` e/ou `|mundos|` batem `dens_c` (a densidade
à la InS) em AUROC pareado, OU somam sobre ela em combinação. Se a densidade empatar com
os mundos em tudo, a topologia da consistência não está pagando — reportar como nulo
estrutural (sétima vez do padrão, se ocorrer).

**P5 (estrato de escada, TriviaQA, n≈28 — EXPLORATÓRIO, abaixo da regra n≈500).** Entre
itens com escada, os errados têm mais mundos que os certos (hedge = específicas
conflitantes sob o vago). Reportar como direção com IC, jamais como manchete.

**P6 (o nulo herdado, F8/intervenção — quando houver contradição computada).** Nenhum
invariante de mundos separa o braço A do braço B. O limite da F8 é do paradigma de
auto-consistência inteiro e os mundos continuam sendo auto-consistência. Se separar,
é notícia grande — mas a predição registrada é o nulo.

**P7 (sumarização, f4 — requer passada nova de NLI de contradição).** Conjuntos reais
de sumarização são majoritariamente **1 mundo** (elaboração compossível); o nulo
embaralhado também é ≈1 mundo (não-relacionados não conflitam — compossibilidade
trivial). Ou seja: mundos NÃO substituem a SE como detector de dispersão; eles medem o
eixo ortogonal (conflito). A alegação é de **decomposição**, não de dominância:
SE conflita três multiplicidades (refinamento, complementaridade, conflito); a tripla
`(SE, SE-núcleo, WE)` as separa.

**P8 (lado da verificação, S3 — requer NLI de contradição nos cones).** Suporte
incoerente — frases que acarretam a opinião mas conflitam entre si (o cone Û(o) atravessa
≥ 2 mundos) — existe em taxa mensurável e concentra alucinação. Exploratório; 62
positivos apenas; qualquer resultado vai com a ressalva de n.

## 6. Controles fixados

1. **Reprodução da SOTA antes de qualquer número novo** (P1).
2. **Escalar vs estrutura** (P4) — o análogo do controle de grafo aleatório da E22.
3. **Validade de construto sem rede neural**: pares de amostras em mundos diferentes
   devem ser enriquecidos em "status de acerto misto" (uma bate o alias do ouro, a outra
   não) em relação a pares no mesmo mundo. Usa o rótulo só como validação, nunca como
   feature.
4. **Multiplicidade declarada**: os confrontos primários são P3 e P4; todo o resto é
   secundário/exploratório e será rotulado assim.
5. **Regra do n**: nada abaixo de n≈200 vira manchete; estratos pequenos são direção.

## 7. O que decide continuar ou parar

- P1 falha → bug; consertar antes de tudo.
- P3 e P4 falham ambos → a topologia da consistência não paga em QA curta; escrever o
  nulo com mecanismo e testar apenas P7/P8 (os domínios de geração longa) antes de
  arquivar.
- P3 ou P4 passam → coletar contradição para f4/f6/f8 (custo: ~23k/66k/9k pares de NLI,
  um script por vez) e fechar o quadro completo.

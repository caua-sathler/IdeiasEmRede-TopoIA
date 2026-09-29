# J8 — Registro de predições: capturar mais do orçamento `τ/2`

**Data: 2026-08-09.** Escrito ANTES de rodar `j8_desempatador.py`. O baseline
(`a₂ = 0,5856`, captura 17,1%) já é conhecido do `j7`; tudo o que vem abaixo é
sobre variantes que ainda não foram medidas.

---

## 1. O alvo, agora exato

O Teorema 15(iii) dá a identidade

```
AUROC(lex) = AUROC(s₁) + τ·(a₂ − ½)          captura = 2·a₂ − 1
```

com `a₂` = AUROC do secundário **restrito aos pares (pos,neg) que o primário
empata**. O AUROC global do secundário **não aparece**. Logo o problema deixou
de ser "melhorar o desempatador" e passou a ser uma coisa só: **subir `a₂`**.

Baseline medido (`j7`): `a₂ = 0,5856`, captura 17,1%, `lex = 0,9300`.
Teto: `a₂ = 1` ⟹ captura 100% ⟹ `0,9492`.

## 2. Por que o baseline é fraco, e onde

A anatomia (`j7`, Tab. 8 do artigo) mostra que o orçamento é concentrado:

| nível | pares empatados | % do τ | `a₂` |
|---|---|---|---|
| 0 votos | 35.682 | **58,4%** | 0,5608 |
| 1 voto | 10.350 | 16,9% | 0,6784 |
| 2–11 | 13.674 | 22,4% | 0,30–0,65 |
| 12 votos | 1.413 | 2,3% | 0,8733 |

**75% do orçamento é decidido por 37 positivos** (19 no nível 0, 18 no nível 1).
São, por construção, as alucinações mais difíceis do dataset: onze ou doze
juízes independentes deixaram passar cada uma.

Isto sugere duas hipóteses concorrentes, e **elas fazem predições diferentes**:

- **(H-ajuste)** o sinal existe nesses estratos, mas o modelo é ajustado
  globalmente e gasta capacidade separando o que o comitê já separa. Então
  reponderar/condicionar o ajuste sobe `a₂`.
- **(H-sinal)** não há sinal nesses estratos: a família é quase cega justamente
  onde o comitê é. Então nada que se faça com **as mesmas features** sobe `a₂`,
  e o 17% é uma propriedade dos dados, não do ajuste.

O `j5` já matou a versão ingênua de H-ajuste (um modelo por classe, N do artigo:
`0,9237`, pior). O `j8` testa as versões que **não fragmentam** a amostra.

## 3. O diagnóstico que decide entre H-ajuste e H-sinal

Antes de qualquer variante: medir `a₂` de **cada feature crua**, sozinha, no
conjunto empatado e dentro do nível 0.

Se alguma feature crua tiver `a₂` claramente acima do escore ajustado
(0,5856), H-ajuste ganha e a correção é trivial. Se todas ficarem em torno de
0,5–0,6, H-sinal ganha e as variantes 2/3 estão condenadas antes de rodar.
**Este é o resultado mais informativo do j8, independente do resto.**

## 4. As variantes

Todas OOF por audiência (`GroupKFold` 5, agrupado por `ref`), como todo o resto
do pacote. `Xf` é a família de incidência (9 features + `n_irm`); `v` é a
contagem de votos do comitê (0…12).

| # | variante | ideia |
|---|---|---|
| A | `[Xf, v]` | contagem de votos como feature aditiva |
| B | `[Xf, v, Xf⊗v]` | interação linear: coeficientes variam com o estrato |
| C | `[Xf, Xf⊗onehot(bucket)]`, buckets {0}, {1–2}, {3–11}, {12} | interação por estrato grosso |
| D | `Xf` com **peso amostral** ∝ massa de pares empatados do item | reponderar sem fragmentar |
| E | **par a par nos empates**: logística sem intercepto sobre as diferenças `x_p − x_n` de pares empatados | otimiza `a₂` diretamente |

A variante E merece nota: a perda de ranqueamento par a par (RankNet) sobre os
pares empatados **é** uma regressão logística sobre os vetores-diferença, então
não precisa de otimizador novo — e é o único item da lista cuja função objetivo
é literalmente a quantidade do Teorema 15(iii).

## 5. Predições registradas

**P1 (sanidade).** Reproduzir `a₂ = 0,5856` e `lex = 0,9300` do `j7`.

**P2 (a inércia, predição teórica).** A variante **A não muda `a₂`** em mais de
`0,005` em valor absoluto. Razão: dentro de uma classe de empate `v` é
constante, então o termo `β_v·v` é um deslocamento constante do logito e **não
reordena nada**; o único canal é o reajuste dos outros coeficientes. Se A mudar
muito, a minha leitura da geometria do problema está errada.

**P3 (interações).** B e C **sobem `a₂`** numa dobra fixa, mas **não sobrevivem**
à mediana de 20 particionamentos. Confiança: média. A heterogeneidade entre
estratos é real (`a₂` vai de 0,30 a 0,87), mas há 19 positivos no estrato que
detém 58% do orçamento, e interações custam parâmetros.

**P4 (reponderação).** D sobe `a₂` acima de `0,5856`. Confiança: baixa-média
(~45%). É a variante mais barata e a que menos arrisca variância.

**P5 (par a par).** E dá o maior `a₂` **dentro da amostra de treino** e o mais
instável fora dela. Confiança: média-alta. 35.682 dos 61.119 pares de treino
saem de 19 positivos: o tamanho de amostra efetivo é o número de positivos
únicos, não o de pares.

**P6 (o teto realista).** **Nenhuma** variante chega a captura ≥ 50%
(`a₂ ≥ 0,75`). Confiança: alta (~90%).

**P7 (a aposta).** Alguma variante bate o baseline com mediana de 20
particionamentos acima de `0,9301` **e** IC pareado agrupado excluindo zero.
Confiança: baixa (~30%). Se falhar, o veredito é H-sinal e entra no artigo como
negativo, com o mesmo destaque dos outros.

## 6. Controles fixados

1. Reproduzir o baseline antes de qualquer número novo (P1).
2. Tudo OOF por audiência; nenhum ajuste vê a própria linha.
3. **A variante E não pode formar pares cruzando a fronteira de dobra** — os
   pares de treino saem só das audiências de treino.
4. Confronto primário declarado: **P7**, medido como no `j6` (mediana e faixa
   sobre 20 particionamentos) e no `j5` (IC pareado, bootstrap agrupado por
   audiência). Uma dobra só não decide nada — essa lição já custou caro no j3/j4.
5. O nulo do `j5` continua valendo: um desempatador aleatório tem média `0,9259`
   e máximo `0,9308` em 200 sorteios. **Qualquer variante abaixo de `0,9308`
   numa dobra única é indistinguível de sorte.**

## 7. O que decide continuar ou parar

- Diagnóstico da §3 mostra feature crua com `a₂` alto → H-ajuste; perseguir.
- P2 falha → parar e entender a geometria antes de qualquer outra coisa.
- P7 passa → o número do artigo sobe, e a §8.4 ganha o mecanismo.
- P7 falha → **escrever o negativo**: a captura de 17% é limite de sinal e de
  tamanho de amostra, não de operação, e o `τ/2` restante não é alcançável com
  estas features. Isso fecha a §8.4 com honestidade em vez de deixá-la em aberto.

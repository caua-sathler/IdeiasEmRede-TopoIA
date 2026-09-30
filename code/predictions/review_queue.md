# J11 — Registro de predições: a fila de revisão

**Data: 2026-08-09.** Escrito ANTES de rodar `j11_operacao.py`.

---

## 1. O que falta medir

O artigo inteiro é medido em AUROC, que é uma afirmação sobre **pares**. Um
auditor não revisa pares: ele revisa uma **fila**, de cima para baixo, até o
orçamento acabar. A pergunta operacional é

> revisando as `k%` opiniões mais suspeitas, que fração das alucinações eu pego?

Isso é *risk–coverage* clássico \citep{elyaniv2010foundations}, e o artigo já
cita a linhagem (Chow) sem nunca instanciá-la. Um ganho de `+0,0040` de AUROC
não diz nada sobre isso, nem para melhor nem para pior.

## 2. A observação que motiva

Um comitê de 12 votos binários tem **13 níveis** para 3.630 itens. Uma fila
exige uma ordem **total**. Logo, na fronteira do orçamento existe uma classe de
empate inteira que o comitê não ordena, e **a fila não está definida**: dois
operadores usando o mesmo comitê, com o mesmo orçamento, revisam conjuntos
diferentes e obtêm recalls diferentes.

Isso é o Teorema 15 lido do lado operacional, e é a razão pela qual o
desempate pode valer mais na prática do que o `+0,0040` sugere: a AUROC média
sobre todos os pares dilui um efeito que, na fila, está concentrado exatamente
onde o corte cai.

## 3. O objeto: o intervalo de ambiguidade

Para um escore `s` e um orçamento de `k` itens, seja `t` o valor de corte.
Todos os itens com `s > t` entram; restam `r` vagas para a classe `s = t`.
Então o recall alcançável é **exatamente** um intervalo:

```
recall_pess = [pos(s>t) + max(0, r − neg(s=t))] / P
recall_otim = [pos(s>t) + min(r, pos(s=t))]     / P
```

Não é estimativa: são as escolhas pior e melhor dentro do que o comitê deixa
indeterminado. Um desempatador escolhe **um ponto** nesse intervalo. Reportar
a largura `recall_otim − recall_pess` é reportar quanto da decisão o comitê
simplesmente não toma.

## 4. Predições registradas

**P1 (a ambiguidade é material).** Em orçamentos operacionais
(`k ∈ {5%, 10%, 20%}`) a largura do intervalo do comitê é `≥ 5` pontos
percentuais de recall em pelo menos um orçamento. Confiança: média-alta. Se
for `≈0`, a fila do comitê já é essencialmente determinada e este experimento
não tem objeto.

**P2 (o desempate fica acima da média).** O recall do lexicográfico é `≥` a
média do desempate aleatório em **todos** os três orçamentos. Implicado pelo
Teorema 15(iii) com `a₂ > ½`, mas só em média sobre pares — na fila é uma
predição genuína, porque um orçamento específico amostra uma região específica
da ordem. Confiança: média.

**P3 (o ganho relativo é maior que em AUROC).** O ganho do lexicográfico
sobre a média aleatória, em pontos de recall, é relativamente **maior** que o
ganho em AUROC (`+0,43%` relativo). Razão: a AUROC dilui sobre 1,3 milhão de
pares; o recall@k é local. Confiança: média-baixa — depende de o corte cair
perto de uma classe grande, o que eu não controlo.

**P4 (o barato sozinho é útil).** A família de incidência a **zero chamadas**
pega mais que o dobro das alucinações que o cosseno global no mesmo orçamento
de 10%. Confiança: alta (AUROC 0,7605 vs 0,5676).

**P5 (o que NÃO vai acontecer).** O desempate **não** melhora o recall em
orçamentos muito grandes (`k ≥ 50%`), porque aí o corte cai dentro da classe
de zero votos, que é 52,3% dos itens e onde `a₂ ≈ 0,56` — quase nada.
Confiança: média. Se o ganho for grande lá, minha leitura da concentração do
orçamento (§8.4 do artigo) está errada.

## 5. Controles fixados

1. Reproduzir `AUROC(comitê) = 0,9260` e `AUROC(lex) = 0,9300` antes de tudo;
   se não baterem, o resto não vale.
2. O secundário é o mesmo escore OOF da fase J — nada é reajustado aqui.
3. O desempate aleatório é mediado sobre **200 sorteios** com semente fixa, e
   reporto média e desvio, não uma realização.
4. Os intervalos `[pess, otim]` são **exatos** (contagem), não bootstrap.
5. O intervalo de confiança do ganho de recall é bootstrap **agrupado por
   audiência**, como todo o resto do artigo.

## 6. O que decide o veredito

- P1 falha → não há resultado operacional a reportar; registro o negativo e
  o experimento morre aqui.
- P1 passa e P2 falha → o desempate é ruim na fila apesar de bom em AUROC;
  isso seria uma **ressalva séria** ao artigo e entra nas Ameaças.
- P1 e P2 passam → entra no artigo como a leitura operacional, com a largura
  do intervalo como a medida de quanto o comitê sozinho não decide.

# J10 — Registro de predições: o portão, e o que ele custa

**Data: 2026-08-09.** Escrito ANTES de rodar `j10_portao.py`.

---

## 1. A lacuna que sobrou, e por que ninguém a tocou ainda

O comitê erra `0,0508` de AUROC em pares que ele **separa** — 2,2× o orçamento
do desempate. O Teorema 15(i) proíbe o lexicográfico de encostar neles: é
exatamente essa proibição que o torna seguro. A soma aditiva pode encostar, e
foi isso que a afundou (inverte 1,33% dos separados, saldo −0,0014).

Faltava a coisa entre as duas: um operador que **às vezes** pode contrariar o
primário, com um limite *provado* de quanto pode perder.

## 2. O operador: uma discagem, não um terceiro método

Sejam `r₁(x)` o nível de `x` sob o primário (posto denso, 1…13) e `r₂(x)` o
posto normalizado do secundário em [0,1]. Defina

```
f_γ(x) = r₁(x) + γ · r₂(x)
```

Isto **não é** um método novo: é a família de um parâmetro que liga os dois
métodos que o artigo já compara.

- `γ < 1`: nenhuma inversão é possível (se `r₁(x) < r₁(y)` então
  `f_γ(x) < r₁(x)+1 ≤ r₁(y) ≤ f_γ(y)`). É **exatamente o lexicográfico**.
- `γ ≥ 1`: o secundário pode mover um item por até `⌊γ⌋` níveis do comitê.
- `γ → ∞`: a ordem tende à do secundário puro.

E o parâmetro é interpretável: **γ é quantos níveis do comitê o escore barato
tem licença para mover um item.** A soma aditiva é o caso em que essa licença
é ilimitada e não declarada.

**A cota (o que se prova).** Nenhum par separado por `g ≥ γ` níveis pode ser
invertido. Logo, definindo `τ_γ = Pr[0 < g < γ]` sobre os pares (pos,neg), a
perda em pares separados é no máximo `τ_γ`, e

```
AUROC(s₁) − τ/2 − τ_γ  ≤  AUROC(f_γ)  ≤  AUROC(s₁) + τ/2 + τ_γ
```

`τ_γ` é computável **do comitê apenas**, antes de olhar o secundário — a mesma
propriedade que faz `τ/2` útil. Em `γ<1`, `τ_γ = 0` e recuperamos o Teorema 15.

## 3. O desenho que separa MECANISMO de SINAL

O `j9` mediu `a₃ = 0,473`: a família é **pior que o acaso** nos pares que o
comitê erra. Isso prevê que abrir o portão perde. Mas um resultado negativo
sozinho não distingue "o operador é ruim" de "o detector é cego". Então rodamos
a mesma discagem com secundários de qualidade **controlada**:

- o secundário real (a família);
- um **clarividente**: `s₂ = y` (o rótulo), o melhor detector concebível;
- clarividentes **corrompidos** a taxa `p`: o rótulo trocado com probabilidade
  `p`, varrendo `p` para achar **quão bom um detector precisaria ser** para o
  portão passar a compensar.

O último é a pergunta prática que sobra depois do `j8`/`j9`: se as features
acabaram, *que qualidade* uma feature nova precisaria ter para valer a pena?

## 4. Predições registradas

**P1 (sanidade/teoria).** Todo `γ ∈ (0,1)` devolve exatamente o AUROC do
lexicográfico, `0,9300`, e **zero** inversões.

**P2 (a cota).** Em nenhum `γ` existe par invertido com separação `g ≥ γ`
níveis. Zero violações. Se falhar, a álgebra da §2 está errada.

**P3 (a direção).** Com a família real, `AUROC(f_γ)` é **monótona decrescente**
em `γ` para `γ ≥ 1`. Razão: `a₃ = 0,473 < ½`, então cada par recém-alcançado é,
em média, revertido para pior. Confiança: alta.

**P4 (o clarividente).** Com `s₂ = y`: em `γ<1` dá exatamente `0,9492`
(`AUROC + τ/2`, o teto do desempate); e cresce monotonamente com `γ`, tendendo a
`1,0`. Isto prova que **o mecanismo funciona** — o que falta é o detector.

**P5 (nenhum γ ganha).** Com a família real, nenhum `γ` supera o lexicográfico.
Confiança: alta (~90%), e é implicado por P3.

**P6 (o limiar).** Existe uma taxa de corrupção `p*` abaixo da qual o portão
aberto bate o lexicográfico. Predição: `p* < 0,35`, isto é, o detector novo
precisaria acertar **acima de ~65%** nos pares relevantes — muito acima dos
`0,473` de hoje e mesmo dos `0,589` de `a₂`. Confiança: média; é o número que
eu mais quero medir e o que menos consigo prever.

## 5. Controles fixados

1. Reproduzir o lexicográfico (`0,9300`) e a soma aditiva antes de tudo (P1).
2. O secundário é o mesmo escore OOF do resto da fase — nada é reajustado aqui.
3. O clarividente corrompido é sorteado com semente fixa e **mediado sobre 20
   sorteios** por `p`: uma realização não decide nada (lição do j3/j4/j5).
4. Confronto primário: **P5**, contra o lexicográfico, na mesma partição.
5. `τ_γ` é reportado junto de cada `γ`, porque é a cota que dá sentido ao valor.

## 6. O que decide o veredito

- P2 falha → a cota está errada; parar e refazer a álgebra.
- P4 falha → o mecanismo é ruim, e aí o negativo é sobre o operador.
- P3 e P5 confirmam com P4 confirmado → o veredito é **"mecanismo certo,
  detector ausente"**, e o `p*` de P6 vira a especificação do que procurar.

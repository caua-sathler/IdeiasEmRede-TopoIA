# Roteiro do Vídeo (até 5 minutos)

> **Competição:** Ideias em Rede — 1ª Edição (Instituto Kunumi)
> **Artigo:** *Speaker-Conditioned Verification and Lexicographic Tie-Breaking for Hallucination Detection in Legislative Hearings*
> **Duração prevista:** cerca de 4 min 40 s (margem de 20 s antes do limite).
> **Formato:** slides (`slides.pdf`) intercalados com gravação de tela do **painel interativo** (`dashboard/index.html`), que serve de demonstração prática.

Todos os números abaixo estão no artigo e no painel. Não arredonde para cima nem acrescente afirmações que não estejam lá.

---

## Estrutura

```
00:00 – 00:35  Bloco 1 — O problema                         slides 1–2
00:35 – 01:25  Bloco 2 — Quem disse? (ideia 1)              slide 3 → painel, etapa 1 → slide 4
01:25 – 02:30  Bloco 3 — Empates e o desempate (ideia 2)    painel, etapas 2 e 3 → slide 7
02:30 – 03:35  Bloco 4 — O resultado: custo e fila          painel, etapas 4 e 5 (slides 8–9 de apoio)
03:35 – 04:05  Bloco 5 — O ganho é previsível               painel, etapa 6
04:05 – 04:40  Bloco 6 — Limites e encerramento             slides 11–12
```

---

## Bloco 1 — O problema (00:00 – 00:35)

**Tela:** slide 1 (capa) → slide 2 (206 audiências, 4.238 opiniões, 11,9%, 12 juízes).

> "Olá! Resumos de audiências públicas dizem coisas como: o deputado X defendeu Y. Quando X não disse Y, temos uma alucinação que coloca palavras na boca de uma pessoa real.
>
> O PublicHearingBR tem 206 audiências da Câmara dos Deputados e 4.238 opiniões atribuídas, das quais 11,9% foram marcadas por anotadores humanos como não suportadas. Ele também traz os votos de doze juízes LLM. Juntos, esses doze juízes chegam a 0,926 de AUROC, mas cada chamada custa. A nossa pergunta é: dá para chegar perto disso gastando muito menos?"

---

## Bloco 2 — Quem disse? (00:35 – 01:25)

**Tela:** slide 3 (exemplo de Chinaglia) → **painel, etapa 1**: clicar em *Arlindo Chinaglia*, passar o mouse sobre a barra de *Marcel van Hattem* para mostrar a frase; depois clicar em *Bruna Rafaela* (frase quase literal de outra pessoa, 0,90 contra 0,56) → slide 4 (tabela de AUROC).

> "Detectores baratos comparam a opinião com cada frase da transcrição e ficam com a melhor. Mas veja este caso real: a opinião atribuída ao deputado Arlindo Chinaglia encontra uma frase muito parecida na audiência, com similaridade 0,78. Só que essa frase é do deputado Marcel van Hattem. Nas falas do próprio Chinaglia, o melhor que existe é 0,39.
>
> Qualquer nota que pega o máximo ou a média das frases não sabe quem falou cada uma. Por isso esses detectores ficam perto de 0,57. A nossa primeira ideia é simples: comparar a opinião com as falas de quem supostamente a disse, e com as dos outros oradores. Só isso leva a AUROC de 0,57 para 0,76, sem chamar nenhum modelo de linguagem. E o controle confirma: usando um orador sorteado da mesma audiência, o sinal cai para o acaso."

---

## Bloco 3 — Empates e o desempate (01:25 – 02:30)

**Tela:** **painel, etapa 2**: começar com o controle em 1 juiz, arrastar até 12 e mostrar τ caindo → **etapa 3**: alternar entre *Soma ponderada* e *Desempate lexicográfico* → slide 7 (a fórmula).

> "Agora, como juntar esse sinal barato com os juízes? Cada juiz vota sim ou não. Com um juiz, a nota só tem dois valores, e muitos pares de opiniões ficam empatados. Com doze, ainda são só treze valores possíveis.
>
> O caminho usual é ajustar um modelo com os votos e o sinal barato juntos. Isso piora o comitê. Veja o motivo: numa soma, uma opinião com quatro votos pode passar à frente de uma com cinco, só porque o sinal barato discordou. Nos 1,3 milhão de pares, a soma ganha um pouco nos empates e perde quase tudo invertendo decisões dos juízes.
>
> A nossa regra é o desempate lexicográfico: ordenamos pelos votos e usamos o sinal barato só entre opiniões com o mesmo número de votos. Ela nunca contraria os juízes, e o ganho sai de uma conta simples: a fração de pares empatados vezes o quanto o sinal acerta dentro desses empates."

---

## Bloco 4 — O resultado: custo e fila (02:30 – 03:35)

**Tela:** **painel, etapa 4**: passar o mouse de 1 a 12 juízes → **etapa 5**: mover o orçamento para 10% (slides 8 e 9 servem de apoio se preferir não gravar o painel).

> "Este é o resultado principal. O desempate melhora comitês de todos os tamanhos, e ganha mais onde há menos juízes. Um juiz típico sobe de 0,81 para 0,88. Isso vale para cada um dos doze juízes, com intervalos de confiança acima de zero. E, numa análise exploratória, sete juízes com o desempate ficam estatisticamente empatados com o comitê completo de doze. Com todos os doze, a AUROC vai de 0,926 para 0,930, acima do comitê em todas as vinte partições que testamos.
>
> Na prática, um auditor revisa uma fila, da opinião mais suspeita para a menos suspeita. Revisando só 10% das opiniões, o melhor juiz sozinho encontra 40,5% das alucinações. Com o desempate, 52,2%, com a mesma única chamada."

---

## Bloco 5 — O ganho é previsível (03:35 – 04:05)

**Tela:** **painel, etapa 6**: mostrar os pontos sobre a diagonal; clicar em *Com AUROC global* para mostrar os pontos subindo acima da diagonal.

> "E dá para saber o ganho antes de usar a regra. Dividimos as audiências ao meio cinquenta vezes: medimos o sinal numa metade e previmos o ganho na outra, que o modelo nunca viu. A previsão acerta sem viés. Já usar a AUROC global do sinal, em vez da medida dentro dos empates, superestima o ganho de 1,4 a 3 vezes."

---

## Bloco 6 — Limites e encerramento (04:05 – 04:40)

**Tela:** slide 11 (o que não funcionou) → slide 12 (encerramento).

> "Também reportamos o que não funcionou: features topológicas e seis tentativas de melhorar o sinal não ajudaram, e onde os juízes erram o sinal barato erra junto. Usamos os rótulos do dataset como dados, e o ganho sobre os doze juízes é pequeno, embora consistente.
>
> A mensagem é: detecção confiável de atribuições falsas não precisa de um comitê grande. O artigo, o código e este painel estão no repositório. Muito obrigado ao Instituto Kunumi e à organização do Ideias em Rede!"

---

## Dicas de gravação

1. **Ritmo:** o texto tem cerca de 600 palavras; a 130 palavras por minuto, dá cerca de 4 min 35 s. Faça um ensaio cronometrado.
2. **Painel:** abra o painel em tela cheia, com zoom de 110–125% para legibilidade em 1080p. Os controles têm dados reais e respondem na hora; ensaie os movimentos de cada etapa uma vez.
3. **Honestidade dos números:** "sete juízes empatam com doze" é **exploratório**; "cada juiz melhora" tem intervalo de confiança; o ganho com doze juízes é **pequeno**. Diga assim.
4. **Margem:** terminar por volta de 4 min 40 s evita o risco de penalização pelo limite de 5 minutos.

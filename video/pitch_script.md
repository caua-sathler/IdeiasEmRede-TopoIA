# Roteiro do vídeo de pitch (alvo: 4 min 30 s, limite: 5 min)

**Artigo:** *Who Said It? Speaker-Conditioned Verification and Lexicographic Tie-Breaking for Low-Cost Hallucination Detection in Legislative Hearings*
**Formato:** fala em português, ~130 palavras/minuto (≈ 580 palavras faladas). Tela: figuras e tabelas do artigo (`paper/main.pdf`) e uma execução curta do código no terminal.
**Regra de ouro:** só números que estão no artigo. Nunca citar nomes de parlamentares: usar "Deputado A" e "Deputado B" (LGPD; é o que o artigo faz).

| Bloco | Tempo | Tela |
|---|---|---|
| 1. O problema | 0:00 – 0:30 | título do artigo; depois a Fig. 1 (só a frase atribuída) |
| 2. Ideia 1: quem disse? | 0:30 – 1:20 | Fig. 1 completa; tabela de AUROC das features |
| 3. Ideia 2: desempatar, não somar | 1:20 – 2:20 | Fig. 2 (visão geral do método); Fig. do histograma do comitê |
| 4. Resultado | 2:20 – 3:25 | tabela da escada de custo; fig. da fila de revisão |
| 5. Custo e previsibilidade | 3:25 – 3:55 | tabela *Measured cost*; tabela de previsão |
| 6. Limites e ética | 3:55 – 4:15 | seção *Ethics* / *Threats* |
| 7. Fechamento e reprodução | 4:15 – 4:35 | terminal: `./run_all.sh`; repositório |

---

## Bloco 1 — O problema (0:00 – 0:30)

> "Resumos de audiências públicas dizem coisas como: *o Deputado A defendeu tal ponto*. Se ele não disse isso, o resumo colocou palavras na boca de uma pessoa real.
>
> O PublicHearingBR reúne 206 audiências da Câmara dos Deputados e 4.238 opiniões atribuídas, cada uma com veredito humano: 11,9% foram marcadas como possível alucinação. O dataset traz ainda os votos de doze juízes LLM. Juntos, eles chegam a 0,926 de AUROC, mas cada chamada custa. Nossa pergunta: como chegar perto disso gastando muito menos?"

## Bloco 2 — Ideia 1: quem disse? (0:30 – 1:20)

**Tela:** Fig. 1; depois a tabela de AUROC (cos global 0,57 → cos no orador 0,75 → conjunto de features 0,76).

> "Os detectores baratos comparam a opinião com todas as frases da transcrição e ficam com a melhor. Só que a melhor frase pode ser de outra pessoa. Neste caso real, anonimizado, a opinião atribuída ao Deputado A tem similaridade 0,78 com uma frase… do Deputado B. Dentro das falas do próprio Deputado A, o melhor casamento é 0,39.
>
> Qualquer nota que tira o máximo ou a média sobre a transcrição inteira não sabe *quem* falou. Por isso esses detectores ficam em 0,57 de AUROC.
>
> A nossa primeira ideia é simples: comparar a opinião com as falas de quem supostamente a disse. Isso leva o AUROC de 0,57 para 0,76, sem nenhuma chamada de LLM. E uma auditoria de 50 casos mostra que cerca de um quarto das alucinações são exatamente isso: algo que foi dito, mas por outra pessoa."

## Bloco 3 — Ideia 2: desempatar, não somar (1:20 – 2:20)

**Tela:** Fig. 2 (visão geral) → histograma dos 13 níveis de voto.

> "Como juntar esse sinal barato com os juízes? Cada juiz vota sim ou não. Doze votos binários dão só treze notas possíveis, então muitas opiniões ficam empatadas.
>
> O jeito usual é ajustar um modelo sobre votos e features juntos. Mas uma soma pode inverter uma decisão correta do comitê: uma opinião com quatro votos passa à frente de uma com cinco só porque o sinal barato discordou. Resultado: esse modelo fica abaixo do comitê em 19 de 20 partições.
>
> A nossa regra é lexicográfica: ordenar pelos votos e usar o sinal barato *apenas entre opiniões com o mesmo número de votos*. Ela nunca contraria os juízes. E o ganho tem fórmula exata: a fração de pares empatados, vezes o quanto o detector acerta dentro desses empates, acima do acaso."

## Bloco 4 — Resultado (2:20 – 3:25)

**Tela:** tabela da escada de custo (1, 3, 5, 8, 12 juízes); depois a figura da fila de revisão.

> "No comitê completo, a regra sobe o AUROC de 0,926 para 0,930, nas vinte partições. O ganho é pequeno, porque o comitê já empata pouco.
>
> Onde ela paga é quando há poucos juízes. Cada um dos doze juízes melhora, de 0,046 a 0,101 de AUROC. Um juiz típico sobe de 0,81 para 0,88 — com uma chamada de LLM em vez de doze. E, em análise exploratória, oito juízes com a regra são não-inferiores aos doze: um terço a menos de chamadas.
>
> Na prática, um auditor revisa uma fila. Com o melhor juiz sozinho, revisar os 10% mais suspeitos acha 40,5% das alucinações. Com a regra, 52,2%."

## Bloco 5 — Custo e previsibilidade (3:25 – 3:55)

**Tela:** tabela *Measured cost*; tabela de previsão do ganho.

> "Baixo custo precisa de medida. Em CPU, sem GPU: montar as features leva menos de um milésimo de segundo por opinião; embutir a transcrição custa cerca de 2 segundos por opinião, pagos uma vez por audiência; e dez chamadas de NLI pequeno somam cerca de 5 segundos. Nenhuma chamada de LLM. Um juiz lê cerca de 600 tokens; a transcrição inteira tem mais de 27 mil.
>
> E dá para prever o ganho antes de implantar: estimando os empates e o acerto do detector numa metade das audiências, o ganho na outra metade sai dentro de cerca de 5%."

## Bloco 6 — Limites e ética (3:55 – 4:15)

**Tela:** seção *Ethics, Data Use and Limits of Use*.

> "Limites: o ganho sobre o comitê completo é pequeno. E as features não ajudam onde o comitê erra — ali estão abaixo do acaso. Sobre ética: usamos só dados públicos da Câmara, pseudonimizamos as pessoas e o detector sinaliza *opiniões* para revisão humana. Ele não classifica nem perfila indivíduos."

## Bloco 7 — Fechamento e reprodução (4:15 – 4:35)

**Tela:** terminal com `cd code && ./run_all.sh` (mostrar as primeiras linhas e o resultado de `lexicographic_combination.py`: `0.9260 → 0.9300`); depois a página do repositório.

> "Tudo é reproduzível com um único script: `run_all.sh` refaz todos os números do artigo. Resumindo: condicione ao orador, e use o sinal barato só para desempatar. Menos chamadas de LLM, mesma confiabilidade, ganho previsível. Obrigado!"

---

## Versão de emergência (se passar de 4:45)

Cortar o Bloco 5 para duas frases (*"em CPU, sem nenhuma chamada de LLM: cerca de 5 s por opinião; e o ganho é previsível dentro de ~5%"*) e o Bloco 6 para uma frase.

## Checklist de gravação

- [ ] 1080p, 16:9, áudio limpo; exportar `.mp4` ou link não listado.
- [ ] Ensaio cronometrado: a fala deve ficar entre 4:15 e 4:45 (o limite é 5:00).
- [ ] Nenhum nome de parlamentar na tela (conferir a Fig. 1 e o terminal).
- [ ] Deixar o terminal com fonte grande; rodar antes uma vez para aquecer o cache.
- [ ] Conferir os números na tela contra `paper/main.pdf`.

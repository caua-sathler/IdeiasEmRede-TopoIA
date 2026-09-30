# Roteiro Oficial do Vídeo de Pitch (Apresentação Baseada no Dashboard)

**Duração Alvo:** 4 minutos e 30 segundos (Teto regulamentar: **5 minutos estritos**).  
**Formato Visual:** Gravação de tela do [**`dashboard/pt-br-dashboard.html#slides`**](../dashboard/pt-br-dashboard.html) no modo apresentação (ver tabela abaixo) (com corte rápido de 10s no terminal mostrando `./run_all.sh`).  
**Estratégia de Pitch:** Alinhamento explícito e agressivo com os **4 Critérios Oficiais de Avaliação**:
- **Inovação e Originalidade (40%)**: Verificação condicionada ao orador + desempate lexicográfico não destrutivo.
- **Rigor Metodológico (30%)**: Identidade matemática analítica $\tau(\alpha - 1/2)$, 20 partições GroupKFold, erro de previsão out-of-sample < 5%.
- **Impacto e Aplicabilidade (10%)**: Aplicação direta na esfera pública (Câmara dos Deputados, TCU, checagem), viável em CPU comum com > 95% de economia de custo.
- **Qualidade da Apresentação e Código (20%)**: Dashboard interativo auto-contido, clareza visual, conformidade com a LGPD e código 100% reproduzível via `./run_all.sh`.

---

## Mapa de Cenas e Navegação no Dashboard

| Bloco | Tempo | Seção no Dashboard | Ação do Apresentador na Tela | Critério Destacado |
|---|---|---|---|---|
| **1. Abertura & Inovação 1** | 0:00 – 0:45 | Topo + `#quem` | Exibir KPIs do cabeçalho; descer para Seção 1; clicar nos botões dos exemplos reais (Orador A vs Orador B). | **Inovação (40%) & Problema** |
| **2. Inovação 2: A Regra** | 0:45 – 1:45 | `#empates` + `#regra` | Mostrar o histograma dos 13 níveis de voto; alternar os botões *"Empilhamento"* vs *"Desempate lexicográfico"*. | **Inovação (40%) & Rigor (30%)** |
| **3. Rigor Teórico & Previsão** | 1:45 – 2:30 | `#previsao` | Descer para Seção 7; destacar a fórmula exata e a tabela comparativa entre previsto e observado. | **Rigor Metodológico (30%)** |
| **4. Eficiência & Menos Juízes** | 2:30 – 3:30 | `#juizes` + `#custo` | Mostrar a curva da escada de juízes (1 a 12) e a tabela de custos em CPU sem GPU. | **Eficiência (Trilha D) & Impacto** |
| **5. Impacto Real & Fila Cívica** | 3:30 – 4:15 | `#fila` | Mover o slider interativo do orçamento do auditor humano de 10% para 20%; apontar conformidade LGPD. | **Impacto & Aplicabilidade (10%)** |
| **6. Reprodutibilidade & Fechamento** | 4:15 – 4:30 | Terminal / Rodapé | Cortar brevemente para o terminal rodando `./run_all.sh` com as saídas geradas; fechar no repositório. | **Qualidade de Código (20%)** |

### Gravação no modo apresentação

Abra `dashboard/pt-br-dashboard.html#slides` em tela cheia (`F`). A seta `→` (ou o passador de slides) primeiro executa as interações do slide e só depois passa para o próximo; os pontinhos no canto superior direito mostram quantas interações faltam. `←` volta e reinicia o slide, `H` esconde contador e barra de progresso, `C` mostra a área reservada para a câmera (canto inferior esquerdo) para alinhar o OBS.

| Slide | Bloco | O que cada `→` faz |
|---|---|---|
| 1 · Título e KPIs | 1 | — (os números contam na entrada) |
| 2 · Quem disse | 1 | Má-atribuição 1 → Má-atribuição 2 → Opinião suportada |
| 3 · Empates | 2 | comitê cresce de 1 para 12 juízes |
| 4 · Somar ou desempatar | 2 | troca soma ponderada → desempate lexicográfico (as linhas trocam de posição) |
| 5 · Previsão | 3 | previsão com AUROC global → volta para α |
| 6 · Menos juízes | 4 | marcador em 5 → 8 → 12 juízes |
| 7 · Custo medido | 4 | 12 → 8 juízes → 1 juiz |
| 8 · Fila de revisão | 5 | orçamento de 10% → 20% |
| 9 · Código aberto | 6 | — |

---

## Transcrição do Roteiro (Texto de Locução)

### Bloco 1 — Abertura, O Problema e Inovação 1 (0:00 – 0:45)
**Ação na tela:** Começar no topo do Dashboard (`Quem disse isso?`), passar o mouse pelos KPIs (206 audiências, 3.630 opiniões, 12 juízes) e descer até a Seção 1 (`#quem`). Clicar entre o Exemplo 1 e o Exemplo 2.

> *"Audiências públicas da Câmara dos Deputados duram até quatro horas. Quando um resumo legislativo afirma que o Deputado A defendeu determinado ponto, mas ele não disse aquilo, o sistema coloca palavras na boca de um representante público.*
> 
> *A forma mais comum de alucinação não é inventar um assunto do nada, mas trocar quem falou. Um RAG tradicional busca a maior similaridade na audiência inteira: ele acha a frase dita pelo Deputado B e dá nota alta, errando com AUROC de apenas 0,57.*
> 
> *Nossa primeira inovação ataca a raiz do problema: condicionamos a verificação estritamente aos turnos do orador atribuído. Como vemos aqui no painel, essa simples mudança eleva a AUROC de 0,57 para 0,76 — sem fazer nenhuma chamada cara a modelos de linguagem."*

---

### Bloco 2 — Inovação 2: A Armadilha do Stacking e a Regra Lexicográfica (0:45 – 1:45)
**Ação na tela:** Rolar para `#empates`, apontando as 13 barras do histograma de votos. Descer para `#regra` e alternar entre o botão *"Empilhamento (regressão logística)"* e o botão *"Desempate lexicográfico"*, mostrando visualmente as linhas trocando de posição.

> *"Para auditar essas audiências, o comitê de 12 juízes LLM atinge 0,926 de AUROC, mas gera apenas treze patamares de voto, acumulando milhares de empates.*
> 
> *Como combinar nosso sinal barato com esses juízes? A literatura convencional ajusta um modelo supervisionado — como uma regressão logística sobre votos e similaridades. Isso é uma armadilha metodológica: uma soma ponderada pode fazer uma opinião com 4 votos ultrapassar uma com 5 votos só porque o sinal barato discordou. Por isso, o stacking perde para o comitê em 19 de 20 partições.*
> 
> *Nossa segunda inovação é a Regra Lexicográfica: nós ordenamos rigorosamente pelos votos do comitê e usamos o verificador leve exclusivamente para desempatar opiniões no mesmo nível. Ela tem variabilidade sete vezes menor e nunca contraria uma decisão soberana dos juízes."*

---

### Bloco 3 — Rigor Metodológico e Previsibilidade Analítica (1:45 – 2:30)
**Ação na tela:** Rolar para `#previsao`. Apontar a fórmula analítica no texto e a tabela de previsão out-of-sample (*Previsão vs. Observado*).

> *"Nosso diferencial em rigor metodológico é que essa combinação não depende de tentativa e erro. Provamos formalmente uma identidade de decomposição de pares: o ganho de AUROC é exatamente igual à taxa de pares empatados vezes a vantagem do detector leve sobre o acaso nesses empates.*
> 
> *Isso confere previsibilidade analítica: estimando essa vantagem em metade das audiências, conseguimos prever com precisão matemática o ganho exato na outra metade dos dados, com erro relativo inferior a 5%. É ciência com garantias teóricas antes da implantação."*

---

### Bloco 4 — Eficiência Extrema e a Escada de Juízes (2:30 – 3:30)
**Ação na tela:** Rolar para `#juizes`, passando o mouse pelos pontos da curva (1, 3, 5, 8, 12 juízes). Em seguida, rolar para `#custo`, mostrando a tabela de latência e custo em CPU.

> *"Na Trilha de Eficiência e Otimização do edital, o ganho prático é transformador. Quando o orçamento é escasso, nossa regra brilha:*
> 
> *Cada um dos doze juízes individuais salta de 0,81 para 0,88 de AUROC com uma única chamada de LLM. Mais impressionante ainda: oito juízes com o nosso desempate são estatisticamente não-inferiores ao comitê completo de doze juízes, poupando um terço de todas as chamadas.*
> 
> *E o custo computacional medido é ínfimo: em CPU comum de notebook, sem qualquer acelerador gráfico, montar as features leva menos de 1 milissegundo por opinião. Uma economia superior a 95% de tokens comparada a pipelines tradicionais de LLM."*

---

### Bloco 5 — Impacto na Esfera Pública e Fila de Auditoria Cívica (3:30 – 4:15)
**Ação na tela:** Rolar para `#fila`. Mover o slider interativo do orçamento de revisão de 10% para 15% e depois 20%, mostrando o percentual de alucinações capturadas subindo em tempo real.

> *"Para a esfera pública — em órgãos de controle como TCU, controladorias ou agências de checagem —, o tempo do auditor humano é o recurso mais valioso.*
> 
> *Aqui no simulador da fila de revisão, vemos o impacto direto: com o melhor juiz sozinho, revisar os 10% mais suspeitos captura 40% dos erros. Com o nosso desempate lexicográfico, o mesmo auditor encontra mais da metade — 52,2% de todas as alucinações.*
> 
> *Tudo isso operando com estrita conformidade à LGPD: pseudonimizamos todos os parlamentares para 'Deputado A e B' e auditamos a fidedignidade da informação, sem perfilar indivíduos."*

---

### Bloco 6 — Reprodutibilidade e Conclusão (4:15 – 4:35)
**Ação na tela:** Cortar brevemente para uma janela de terminal limpo executando `./run_all.sh` (mostrando a execução rápida em CPU) e retornar ao rodapé do Dashboard ou página do repositório GitHub.

> *"Todo o pipeline é 100% aberto e reprodutível: basta clonar o repositório e executar `./run_all.sh` para reconstruir todas as tabelas em poucos minutos em CPU.*
> 
> *Aliamos inovação arquitetural, rigor analítico comprovado, custo quase nulo e alto impacto na transparência pública brasileira. Muito obrigado!"*

---

## Dicas Práticas para a Gravação

1. **Resolução e Janela:** Grave o navegador em janela cheia (1080p, 1920x1080).
2. **Cursor do Mouse:** Use o cursor do mouse como ponteiro laser: aponte para os KPIs, clique nos botões de exemplo e arraste o slider da fila suavemente durante a fala.
3. **Cronômetro:** Mantenha um cronômetro na sua frente. O texto tem ~630 palavras faladas. No ritmo de 140 palavras/min, a locução dura exatamente **4m30s**, garantindo 30 segundos de margem de segurança abaixo dos 5m00s do edital.
4. **Áudio:** Use microfone dedicado sem eco ambiente.

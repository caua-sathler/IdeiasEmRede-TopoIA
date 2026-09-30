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
| **5. Impacto Real & Fila Cívica** | 3:30 – 4:15 | `#fila` | Mover o slider interativo do orçamento do auditor humano de 10% para 20%; explicar a revisão humana e a pseudonimização. | **Impacto & Aplicabilidade (10%)** |
| **6. Reprodutibilidade & Fechamento** | 4:15 – 4:30 | Terminal / Rodapé | Cortar brevemente para o terminal rodando `./run_all.sh` com as saídas geradas; fechar no repositório. | **Qualidade da apresentação (20%)** |

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

## Transcrição do roteiro — versão alinhada ao artigo

Texto para aproximadamente 4 a 4min30s; confirmar com ensaio cronometrado. As telas mostram resultados pré-calculados do benchmark. As seis partes podem ser distribuídas entre os integrantes.

### 1 — Problema e evidência por orador (0:00–0:45)

> Em uma audiência pública, não basta um resumo falar sobre o assunto certo: ele precisa atribuir cada opinião à pessoa certa. Confundir quem disse o quê pode distorcer a leitura de um debate público.
>
> Avaliamos esse problema no PublicHearingBR. Os rótulos humanos indicam se uma opinião é sustentada por quatro trechos recuperados. Analisamos 3.630 opiniões com orador identificado, em 206 audiências.
>
> Comparar a opinião com a melhor frase de toda a audiência alcança AUROC de 0,57. Restringir a comparação ao orador eleva o resultado para 0,75; combinar características de similaridade chega a 0,76, sem chamadas a juízes LLM. A recuperação por orador já existe no protocolo original. Nossa contribuição é quantificar e aproveitar esses sinais baratos na triagem.

### 2 — A regra de combinação (0:45–1:40)

> O comitê de doze juízes alcança AUROC de 0,926. Mas doze votos binários produzem apenas treze notas possíveis: há muitos empates.
>
> Como aproveitar um sinal barato sem perder o que o comitê já faz bem? Nos nossos experimentos, uma regressão que mistura votos e características fica abaixo do comitê em dezenove de vinte particionamentos por audiência.
>
> A regra lexicográfica ordena primeiro pela quantidade de votos e usa o sinal secundário apenas nos empates. Assim, preserva toda ordem estrita do comitê. Com ela, a AUROC fica em torno de 0,930, acima do comitê nos vinte particionamentos.
>
> Há também uma versão especialmente simples: usar diretamente a diferença entre similaridade global e similaridade ao orador já alcança 0,9294. Esse desempate dispensa treinamento e NLI.

### 3 — Explicação e previsão (1:40–2:20)

> Além de medir, explicamos o ganho. Provamos que ele é exatamente a fração de pares empatados multiplicada pela vantagem do sinal secundário sobre o acaso nesses pares.
>
> A identidade descreve o resultado exato; a previsão em novos dados é uma estimativa. Em cinquenta divisões das audiências, estimamos os dois componentes em uma metade e avaliamos na outra. As previsões médias correspondem a 92 a 98 por cento dos ganhos médios observados. Isso ajuda a decidir onde vale investir em um desempate.

### 4 — Eficiência (2:20–3:10)

> O benefício cresce quando há poucos juízes: um juiz típico passa de 0,807 para 0,879 com o detector completo. Subconjuntos de oito juízes com desempate alcançam mediana de 0,9272, indicando potencial para reduzir chamadas. A escolha de quais juízes usar ainda precisa de validação prospectiva.
>
> Medimos também os componentes de custo em CPU. Com os embeddings prontos, as características de similaridade levam menos de um milissegundo por opinião no ambiente medido. Produzir embeddings e executar NLI têm custos próprios, documentados separadamente. A versão simples de desempate evita o NLI.

### 5 — Impacto e fila de revisão (3:10–3:55)

> O uso proposto é priorizar revisão humana. Neste benchmark, ao revisar dez por cento das opiniões, o melhor juiz sozinho recupera 40,5 por cento dos casos positivos. Com o desempate completo, recupera 52,2 por cento, mantendo uma chamada de juiz por opinião.
>
> É um resultado exploratório que mostra uma aplicação concreta: ajudar uma equipe com tempo limitado a encontrar mais casos que merecem conferência. O painel permite explorar essa fila e mostra exemplos com participantes pseudonimizados. O sinal serve para revisão, não para julgar pessoas.

### 6 — Entrega e fechamento (3:55–4:20)

> Entregamos o artigo, o código das análises, as tabelas, os registros da auditoria e este painel em português e inglês. Os experimentos separam audiências entre treino e teste, e as comparações principais incluem intervalos de confiança.
>
> Nossa proposta combina uma regra simples, uma explicação matemática e evidência experimental: aproveitar melhor os votos já disponíveis e sinais locais baratos para tornar a revisão de resumos públicos mais eficiente. Obrigado!

---

## Dicas Práticas para a Gravação

1. **Resolução e Janela:** Grave o navegador em janela cheia (1080p, 1920x1080).
2. **Cursor do Mouse:** Use o cursor do mouse como ponteiro laser: aponte para os KPIs, clique nos botões de exemplo e arraste o slider da fila suavemente durante a fala.
3. **Cronômetro:** Ensaiar a locução e as interações juntas. Buscar 4min30s e conferir que o arquivo final tem menos de 5 minutos; o tempo depende do ritmo e das pausas.
4. **Áudio:** Use microfone dedicado sem eco ambiente.

5. **Antes do envio:** conferir áudio, legibilidade, duração, acesso ao link do vídeo e correspondência dos números com `paper/main.pdf`. A gravação e o link final ainda estão pendentes.

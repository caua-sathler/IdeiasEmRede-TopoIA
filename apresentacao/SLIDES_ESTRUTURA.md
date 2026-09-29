# Estrutura dos Slides (`slides.tex`, 12 slides)

Os slides acompanham o [`ROTEIRO_VIDEO_5MIN.md`](ROTEIRO_VIDEO_5MIN.md) e usam as mesmas cores do painel interativo (azul = método, laranja = alucinação, cinza = baseline). Números conferidos com o artigo (`producao_de_artigos/artigo_unificado_sota/main.tex`).

| # | Título | Conteúdo | Bloco do roteiro |
|---|---|---|---|
| 1 | Capa | título, autor, logos | 1 |
| 2 | O problema | 206 audiências, 4.238 opiniões, 11,9%, 12 juízes (0,926); o que é AUROC | 1 |
| 3 | Por que detectores baratos falham | exemplo real (Chinaglia: 0,783 × 0,386) e a observação de cegueira de incidência | 2 |
| 4 | Ideia 1 | tabela de AUROC: 0,568 → 0,746 → 0,761 → 0,779; controle do orador aleatório; auditoria (1 em 4) | 2 |
| 5 | Os juízes empatam | histograma de votos (19 × 1.878 na classe de zero votos); τ = 4,65% | 3 |
| 6 | Somar ou desempatar | exemplo x, y, z; stacking +0,0017 −0,0014 vs lexicográfico +0,0040 | 3 |
| 7 | Ideia 2 | a regra e a decomposição AUROC + τ(α − ½); 0,9260 → 0,9300 | 3 |
| 8 | Resultado principal | curva por número de juízes (1 juiz 0,807 → 0,881; 7 ≈ 12) | 4 |
| 9 | Fila de revisão | curvas de recall; 40,5% → 52,2% a 10% | 4 |
| 10 | Previsão | observado × previsto com α × com AUROC global | 5 |
| 11 | O que não funcionou e limites | negativos e ressalvas | 6 |
| 12 | Encerramento | contribuições e materiais | 6 |

Compilação: `pdflatex slides` (duas vezes).

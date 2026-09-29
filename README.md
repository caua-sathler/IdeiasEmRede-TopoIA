# IdeiasEmRede-TopoIA

Submissão ao **Ideias em Rede — 1ª Edição** (Instituto Kunumi): *Speaker-Conditioned
Verification and Lexicographic Tie-Breaking for Hallucination Detection in
Legislative Hearings*.

O trabalho detecta opiniões atribuídas à pessoa errada em resumos de
audiências públicas do [PublicHearingBR](https://huggingface.co/datasets/unicamp-dl/PublicHearingBR).
Duas ideias, nessa ordem:

1. **Condicionar a verificação ao orador.** Um escore que compara uma opinião
   com a transcrição inteira e fica com o melhor casamento não enxerga *quem*
   disse cada frase — ele não consegue distinguir uma opinião apoiada pelo
   próprio orador atribuído de uma opinião apoiada só por outra pessoa
   (Fig. 1 do artigo). Restringir a comparação às falas do orador atribuído
   sobe o AUROC de 0,57 para 0,76, sem nenhuma chamada de modelo.
2. **Combinar esse detector barato com o comitê de 12 juízes LLM sem
   piorá-lo.** Somar os escores pode inverter decisões do comitê. Usar o
   detector barato só para desempatar opiniões que o comitê empatou nunca
   inverte uma decisão, e o ganho tem fórmula fechada (`τ·(α − ½)`). A regra
   melhora todo tamanho de comitê testado — um juiz típico sobe de 0,81 para
   0,88 — e sete juízes com a regra ficam estatisticamente indistinguíveis do
   comitê de doze.

## Estrutura

| diretório | conteúdo |
|---|---|
| [`artigo/`](artigo/) | o artigo (`main.tex`, versão de 15 páginas; `main_10p.tex`, versão de 10), bibliografia, classe da competição e figuras. |
| [`codigo/`](codigo/) | pacote de reprodução dos experimentos — todo número do artigo sai daqui. Tem README próprio com a ordem de execução e a correspondência seção → script. |
| [`dataset/`](dataset/) | script para baixar e processar o PublicHearingBR (`init_data.py`); os dados processados (~650MB) não são versionados, ver `dataset/README.md`. |
| [`apresentacao/`](apresentacao/) | slides, roteiro e painel interativo (`dashboard/`) para o vídeo de até 5 minutos. |
| [`documentos/`](documentos/) | chamada e regulamento oficiais da competição. |

## Reprodução rápida

O resultado de manchete (comitê `0,9260 → 0,9300`) não precisa do dataset —
os CSV intermediários já vêm em `codigo/out/`:

```bash
cd codigo
pip install -r requirements.txt
python j4_reticulado.py       # teto τ/2, join vs. soma, por juiz
python j6_estabilidade.py     # 20 particionamentos + placar final (Tab. 6)
python j7_mecanismo.py        # decomposição exata do AUROC (Tab. 5, 8)
```

Para regenerar do zero, inclusive as *features* de incidência por orador
(trilha A), veja `codigo/README.md` (ordem completa de execução, tempos e
correspondência artigo → script) e `dataset/README.md` (como obter o
PublicHearingBR processado).

## Compilar o artigo

```bash
cd artigo
pdflatex -interaction=nonstopmode main && bibtex main && \
  pdflatex -interaction=nonstopmode main && pdflatex -interaction=nonstopmode main
```

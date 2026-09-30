# IdeiasEmRede-TopoIA

Submissão ao **Ideias em Rede — 1ª Edição** (Instituto Kunumi): *Who Said It?
Speaker-Conditioned Verification and Lexicographic Tie-Breaking for Low-Cost
Hallucination Detection in Legislative Hearings*.

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
   0,88 — e, numa análise exploratória, oito juízes com a regra são
   não-inferiores ao comitê de doze (margem de 0,004 de AUROC), um terço a
   menos de chamadas de LLM. O ganho pode ser previsto antes de aplicar a
   regra: `τ` e `α` estimados numa amostra rotulada bastam.

## Autores

| autor | instituição | Colab | contato |
|---|---|---|---|
| Gabriel Ribeiro | Departamento de Ciência da Computação, Universidade Federal de Minas Gerais (DCC-UFMG) | Domain-Specific Foundation Models | gabriel.ribeiro@dcc.ufmg.br |
| Cauã Sathler | Departamento de Ciência da Computação, Universidade Federal de Minas Gerais (DCC-UFMG) | Agentic AutoML for Data Science | cauasathler@ufmg.br |
| Arthur Gonçalves | Departamento de Ciência da Computação, Universidade Federal de Minas Gerais (DCC-UFMG) | Domain-Specific Foundation Models | afariag72@gmail.com |
| Jordan Elias | Universidade Federal do Ceará (UFC) | SLMs for Process Automation | jordanelias@alu.ufc.br |

## Estrutura

| diretório | conteúdo |
|---|---|
| [`artigo/`](artigo/) | o artigo (`main.tex`), bibliografia, classe da competição e figuras. |
| [`codigo/`](codigo/) | pacote de reprodução dos experimentos — todo número do artigo sai daqui. Tem README próprio com a ordem de execução e a correspondência seção → script. |
| [`dataset/`](dataset/) | script para baixar e processar o PublicHearingBR (`init_data.py`); os dados processados (~650MB) não são versionados, ver `dataset/README.md`. |
| [`apresentacao/`](apresentacao/) | slides, roteiro e painel interativo (`dashboard/`) para o vídeo de até 5 minutos. |
| [`auxiliary-reports/`](auxiliary-reports/) | relatórios complementares (Regulamento, item 8.2): o estudo de consistência semântica (mundos possíveis e taxa de conflação), cortado do artigo por espaço, com código, dados e saídas de referência próprios. |
| [`documentos/`](documentos/) | chamada e regulamento oficiais da competição. |

## Reprodução rápida

O resultado de manchete (comitê `0,9260 → 0,9300`) não precisa do dataset —
os CSV intermediários já vêm em `codigo/out/`:

```bash
cd codigo
pip install -r requirements.txt
python j4_reticulado.py       # teto τ/2, join vs. soma, por juiz
python j6_estabilidade.py     # 20 particionamentos + placar final (Tabela 3)
python j7_mecanismo.py        # decomposição exata do AUROC (Tabelas 2 e 7)
python j13_previsao.py        # previsão do ganho em audiências não vistas (Tabela 6)
```

Os números do artigo foram gerados com as versões fixadas em
`codigo/requirements.txt` (Python 3.11); outras versões do scikit-learn mudam
a terceira casa decimal de alguns resultados fora de dobra.

Para regenerar do zero, inclusive as *features* de incidência por orador, veja
`codigo/README.md` (ordem completa de execução, tempos e correspondência
artigo → script) e `dataset/README.md` (como obter o PublicHearingBR
processado).

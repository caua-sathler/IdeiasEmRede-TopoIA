# `dataset/` — PublicHearingBR processado

Este diretório não vem com os dados prontos: os embeddings MPNet do corpus
inteiro somam ~650MB, e o resultado principal do artigo (trilha C, ver
`../codigo/README.md`) não precisa deles — os CSV intermediários que ele lê já
vêm versionados em `../codigo/out/`. Estes dados só são necessários para
regenerar as *features* de incidência por orador do zero (trilha A).

## Gerar

```bash
pip install -r ../codigo/requirements.txt   # numpy, pandas, torch, transformers, datasets
python init_data.py --models MPNET
```

Baixa o PublicHearingBR do Hugging Face (`unicamp-dl/PublicHearingBR`) e
escreve, dentro deste diretório:

```
phrasal_data/data_XXX/phrases_XXX.csv
opinions_data/data_XXX/opinions_XXX.csv
MPNET_embeddings_phrasal_data/data_XXX/{transcript,article}_embeddings_XXX.npy
MPNET_opinion_embeddings/data_XXX/opinion_embeddings_XXX.npy
metrics_MPNET.csv
```

`comum.py` (em `../codigo/`) encontra este diretório automaticamente por estar
no mesmo nível de `codigo/`; para apontar para uma cópia em outro lugar, use
`export PHBR_DATA=/caminho/para/dataset`.

`init_data.py` também sabe gerar embeddings para outros modelos (BERT,
MINILM, NOMIC — ver `--list-models`); nenhuma linha deste pacote de
reprodução os usa, então `--models MPNET` é suficiente e mais rápido.

Confira com `python ../codigo/dados.py` (deve imprimir `audiencias
utilizaveis: 206`).

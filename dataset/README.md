# `dataset/` — processed PublicHearingBR

The processed corpus is **not versioned** (the MPNet embeddings of the whole corpus are ~650 MB).
It is only needed to rebuild the speaker-incidence features from scratch
(`code/run_all.sh --from-scratch`); every table that the analyses read already ships in
`code/results/`.

## Build

```bash
pip install -r ../code/requirements.txt
python init_data.py --models MPNET
```

This downloads PublicHearingBR from the Hugging Face Hub (`unicamp-dl/PublicHearingBR`) and writes,
inside this directory:

```
phrasal_data/data_XXX/phrases_XXX.csv
opinions_data/data_XXX/opinions_XXX.csv
MPNET_embeddings_phrasal_data/data_XXX/{transcript,article}_embeddings_XXX.npy
MPNET_opinion_embeddings/data_XXX/opinion_embeddings_XXX.npy
metrics_MPNET.csv
```

The scripts in `code/src/` find this directory automatically (it is a sibling of `code/`). To use a copy
elsewhere: `export PHBR_DATA=/path/to/dataset`.

Check the build with `python ../code/src/dataset_readers.py` (it should print `audiencias utilizaveis: 206`).

## Source and use

PublicHearingBR is built from official public records of the Brazilian Chamber of Deputies
(Fernandes et al., 2024). We use it only for the research purpose of the challenge; see the
*Ethics, Data Use and Limits of Use* section of the paper (LGPD, Law 13.709/2018). The repository
does not redistribute transcripts or opinions: the tables in `code/results/` hold scores, verdicts and
judge votes only.

"""Leitores do PublicHearingBR ja processado por `dataset/init_data.py`.

Extraido de `diagnostico/e10_retrato.py`, que no repositorio de pesquisa e um
experimento inteiro da fase E (Mapper, lentes, negativos duros) do qual esta
linha usava apenas os seis leitores abaixo. Ficar com o arquivo original
arrastaria `ctm.py`, o algoritmo Mapper e o cache do acervo — nada disso e usado
aqui.

Layout esperado (`comum.DATA`):

    dataset/
      phrasal_data/data_XXX/phrases_XXX.csv          colunas `transcript`, `article`
      opinions_data/data_XXX/opinions_XXX.csv        opinioes + `alucinacao_manual` + juizes
      MPNET_embeddings_phrasal_data/data_XXX/transcript_embeddings_XXX.npy
      MPNET_opinion_embeddings/data_XXX/opinion_embeddings_XXX.npy

Todos os embeddings saem daqui ja L2-normalizados, entao `A @ B.T` e cosseno.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from comum import DATA, _unit, exigir_dados

# Espaco metrico usado como referencia em toda esta linha. O esqueleto do Mapper
# (fase E) usava BERT-pt; aqui nao ha esqueleto, e o MPNET e estritamente melhor
# como metrica (E1: cosseno medio entre pares aleatorios 0,202 contra 0,572 do
# BERT-pt, isto e, muito menos anisotropia).
GEOM = "MPNET"


def emb(ref: str, kind: str, mk: str = GEOM, unit: str = "frase") -> np.ndarray:
    """Embeddings das frases de `ref` (`kind` = transcript | article).

    Devolve `(0, 768)` quando o arquivo nao existe — os chamadores tratam isso
    como "audiencia sem esse artefato" e pulam.
    """
    i = ref.split("_")[-1]
    sub = (f"{mk}_embeddings_phrasal_data" if unit == "frase"
           else f"{mk}_embeddings_windowed_data_{unit}")
    p = DATA / sub / ref / f"{kind}_embeddings_{i}.npy"
    if not p.exists():
        return np.zeros((0, 768), np.float32)
    return _unit(np.load(p))


def phrases(ref: str, kind: str) -> list[str]:
    """As frases de `ref`, na mesma ordem dos embeddings de `emb(ref, kind)`."""
    i = ref.split("_")[-1]
    f = DATA / "phrasal_data" / ref / f"phrases_{i}.csv"
    df = pd.read_csv(f)
    return df[kind].dropna().astype(str).tolist() if kind in df.columns else []


def opinions(ref: str) -> pd.DataFrame | None:
    """As opinioes-ouro de `ref`, com `alucinacao_manual` coagido a booleano.

    Colunas relevantes: `envolvido` (a quem a opiniao e atribuida), `cargo`,
    `alucinacao_manual` (o veredito humano) e os 12 `juiz_p*_*` (votos binarios
    de LLM ja versionados no dataset).
    """
    i = ref.split("_")[-1]
    f = DATA / "opinions_data" / ref / f"opinions_{i}.csv"
    if not f.exists():
        return None
    g = pd.read_csv(f)
    g["alucinacao_manual"] = (g["alucinacao_manual"].astype(bool)
                              if "alucinacao_manual" in g.columns else False)
    return g


def op_emb(ref: str, mk: str = GEOM) -> np.ndarray | None:
    """Embeddings das opinioes-ouro de `ref`, alinhados linha a linha com
    `opinions(ref)`. Os chamadores conferem `len(g) == len(ge)` antes de usar —
    a assercao de alinhamento que a fase H documenta como obrigatoria."""
    i = ref.split("_")[-1]
    f = DATA / f"{mk}_opinion_embeddings" / ref / f"opinion_embeddings_{i}.npy"
    return _unit(np.load(f)) if f.exists() else None


def refs_ok() -> list[str]:
    """As audiencias com os tres artefatos presentes (embeddings de frase,
    opinioes e embeddings de opiniao). E a populacao de todos os experimentos."""
    exigir_dados()
    r = sorted(p.name for p in (DATA / f"{GEOM}_embeddings_phrasal_data").glob("data_*"))
    return [x for x in r if opinions(x) is not None and len(opinions(x))
            and op_emb(x) is not None]


if __name__ == "__main__":
    R = refs_ok()
    print(f"audiencias utilizaveis: {len(R)}")
    if R:
        g = opinions(R[0])
        print(f"exemplo {R[0]}: {len(g)} opinioes · "
              f"{len(phrases(R[0], 'transcript'))} frases de transcricao")

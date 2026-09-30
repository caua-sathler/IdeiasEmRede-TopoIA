"""Infraestrutura compartilhada dos experimentos deste artigo.

Substitui o `diagnostico/e0_common.py` do repositorio de pesquisa. Aquele modulo
tambem materializava o acervo de fontes confiaveis (60.407 frases, ~400 MB de
cache, dependencia de `init_sources.py` e de `ctm.py`) — e NENHUM script desta
linha usa isso. Aqui ficam so as quatro coisas de que os scripts precisam: onde
gravar, onde estao os dataset_readers, o AUROC e o banner.

Caminhos
--------
`OUT`   resultados (CSV) — criado ao lado deste arquivo.
`CACHE` caches reaproveitaveis (NLI, geracoes) — criado ao lado deste arquivo.
`DATA`  o diretorio `dataset/` do PublicHearingBR, resolvido nesta ordem:

    1. a variavel de ambiente `PHBR_DATA`, se definida;
    2. o primeiro `dataset/` que contenha `phrasal_data/`, subindo a partir
       deste arquivo (o layout do repositorio de pesquisa).

Se nada for encontrado, `DATA` recebe o candidato mais provavel e o erro so
aparece na primeira leitura — use `exigir_dados()` para falhar cedo e com uma
mensagem util.
"""
from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
CODE = HERE.parent
OUT = CODE / "results"
CACHE = CODE / "cache"
OUT.mkdir(exist_ok=True)
CACHE.mkdir(exist_ok=True)


# --------------------------------------------------------------------- caminhos
def _achar_dataset() -> Path:
    env = os.environ.get("PHBR_DATA")
    if env:
        return Path(env).expanduser().resolve()
    for base in [HERE, *HERE.parents]:
        cand = base / "dataset"
        if (cand / "phrasal_data").is_dir():
            return cand
    # Nothing generated yet: guess the sibling `dataset/` at the repo root
    # (`code/` and `dataset/` are siblings in this repository's layout).
    return CODE.parent / "dataset"


DATA = _achar_dataset()


def exigir_dados() -> Path:
    """Falha cedo, com instrucao, se o `dataset/` nao estiver no lugar."""
    if (DATA / "phrasal_data").is_dir():
        return DATA
    raise SystemExit(
        f"[dataset_readers] nao encontrei o dataset do PublicHearingBR.\n"
        f"  procurei em: {DATA}\n"
        f"  esperava:    {DATA}/phrasal_data/data_XXX/phrases_XXX.csv\n\n"
        f"  Gere-o com `python dataset/init_data.py --models MPNET` (ver\n"
        f"  dataset/README.md), ou aponte para uma copia existente:\n"
        f"      export PHBR_DATA=/caminho/para/dataset"
    )


# --------------------------------------------------------------------- metricas
def _unit(X):
    """L2-normaliza a ultima dimensao (todo cosseno do projeto assume isto)."""
    X = np.asarray(X, np.float32)
    return X / (np.linalg.norm(X, axis=-1, keepdims=True) + 1e-12)


def auc(y, s) -> float:
    """AUROC por ranking, com empates contando 1/2 — sem dependencia de sklearn.

    A convencao de empate importa: o artigo 3 mede exatamente essa meia-contagem
    (`AUROC = A + tau/2`), entao a implementacao precisa ser a estatistica de
    Mann-Whitney com postos medios, que e o que `pandas.rank()` devolve.
    """
    y = np.asarray(y, bool)
    s = np.asarray(s, float)
    if y.all() or not y.any():
        return float("nan")
    r = pd.Series(s).rank().values
    return float((r[y].sum() - y.sum() * (y.sum() + 1) / 2) / (y.sum() * (~y).sum()))


def auc_ci(y, s, groups, n_boot: int = 400, seed: int = 42):
    """AUROC + IC95 por bootstrap AGRUPADO e ESTRATIFICADO por classe.

    Reamostrar grupos sem estratificar explode o IC quando os positivos vivem em
    poucos grupos: um sorteio pode nao conter positivo nenhum. Reamostramos os
    grupos de cada classe separadamente, preservando o n de grupos por classe.
    """
    y = np.asarray(y, bool)
    s = np.asarray(s, float)
    g = np.asarray(groups)
    rng = np.random.default_rng(seed)
    pos_g, neg_g = np.unique(g[y]), np.unique(g[~y])
    where = {u: np.where(g == u)[0] for u in np.unique(g)}
    vals = []
    for _ in range(n_boot):
        sel = np.concatenate([where[u] for u in
                              np.r_[rng.choice(pos_g, len(pos_g), replace=True),
                                    rng.choice(neg_g, len(neg_g), replace=True)]])
        a = auc(y[sel], s[sel])
        if not np.isnan(a):
            vals.append(a)
    lo, hi = (np.percentile(vals, [2.5, 97.5]) if vals else (np.nan, np.nan))
    return auc(y, s), float(lo), float(hi)


def topk(sims: np.ndarray, k: int) -> np.ndarray:
    """Indices dos k maiores, ja ordenados por valor decrescente."""
    k = min(k, len(sims))
    idx = np.argpartition(-sims, k - 1)[:k]
    return idx[np.argsort(-sims[idx])]


def banner(t: str) -> None:
    print(f"\n{'=' * 74}\n{t}\n{'=' * 74}", flush=True)


if __name__ == "__main__":
    print(f"OUT   = {OUT}")
    print(f"CACHE = {CACHE}")
    print(f"DATA  = {DATA}   ({'ok' if (DATA / 'phrasal_data').is_dir() else 'NAO ENCONTRADO'})")

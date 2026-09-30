"""M0 — O QUE O RÓTULO HUMANO REALMENTE MEDE (protocolo de anotação do PublicHearingBR).

Descoberta que reorganiza o artigo. O artigo do dataset (Fernandes et al., 2024, §4.1.2
e §4.2.2) descreve o protocolo: (1) separa-se a fala de cada pessoa; (2) cada fala é
quebrada em *chunks* de 5 frases (1 de sobreposição); (3) cada pessoa ganha sua própria
base vetorial; (4) para cada opinião extraída, buscam-se na base da pessoa ATRIBUÍDA
os 4 chunks mais próximos; (5) o consultor da Câmara (humano) e os 12 juízes LLM
julgam se a opinião "pode ser inferida" desses 4 chunks. Logo:

  * `alucinacao_manual`  = "NÃO inferível dos 4 chunks recuperados da fala do orador
    atribuído" (limite superior de alucinação — o próprio artigo do dataset diz isso);
    NÃO é "não sustentada pela transcrição inteira";
  * os juízes recebem os MESMOS 4 chunks (chamada barata: ~500 tokens, não a transcrição).

O split NLI do dataset traz os 4 chunks (`chunks_proximos`). Este script (a) os
carrega alinhados ao `opinions_XXX.csv`, (b) verifica o alinhamento, (c) mede o tamanho
do que um juiz lê e (d) confere se os chunks realmente saem dos turnos do orador
atribuído (validando o casamento de oradores do artigo).

Saídas: `results/official_chunks.csv` (só números) e `scratch/official_chunks.jsonl` (textos do
dataset — NÃO versionado, regenerado a partir do split NLI oficial).

    python official_chunks.py                     # baixa PublicHearingBR_NLI.jsonl se preciso
    PHBR_NLI=/caminho/PublicHearingBR_NLI.jsonl python official_chunks.py
"""
from __future__ import annotations

import json
import os
import re
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import common as E0            # noqa: E402
import dataset_readers as R             # noqa: E402
import speaker_incidence as H6        # noqa: E402

warnings.filterwarnings("ignore")
SCRATCH = Path(os.environ.get("IER_SCRATCH", E0.CODE / "scratch"))
SCRATCH.mkdir(parents=True, exist_ok=True)
CHUNKS_JSONL = SCRATCH / "official_chunks.jsonl"


def nli_jsonl() -> Path:
    """Caminho do PublicHearingBR_NLI.jsonl (env PHBR_NLI, senão baixa do HF Hub)."""
    env = os.environ.get("PHBR_NLI")
    if env:
        return Path(env).expanduser()
    from huggingface_hub import hf_hub_download
    return Path(hf_hub_download("unicamp-dl/PublicHearingBR", "PublicHearingBR_NLI.jsonl",
                                repo_type="dataset"))


def carregar() -> pd.DataFrame:
    """Uma linha por opinião (4.238), na ordem de `opinions_XXX.csv`, com os 4 chunks.

    Colunas: ref, i (linha no CSV da audiência), opiniao, envolvido, hall (veredito
    humano), chunks (lista de 4 str). Falha alto se a ordem/texto divergir do CSV.
    """
    explicit_cache = os.environ.get("PHBR_CHUNKS")
    if explicit_cache:
        D = pd.read_json(Path(explicit_cache).expanduser(), lines=True)
    else:
        # Reuse the dataset prepared by init_data.py when available. An explicit
        # PHBR_NLI JSONL always takes precedence, making offline reproduction easy.
        if not os.environ.get("PHBR_NLI") and (R.DATA / "NLI").is_dir():
            from datasets import load_from_disk
            saved = load_from_disk(str(R.DATA / "NLI"))
            records = saved["train"] if hasattr(saved, "keys") and "train" in saved else saved
        else:
            with open(nli_jsonl(), encoding="utf-8") as stream:
                records = [json.loads(line) for line in stream if line.strip()]
        recs = []
        for row in records:
            ref = f"data_{int(row['id']):03d}"
            meta = row.get("metadados_extraidos") or {}
            k = 0
            for participant in (meta.get("envolvidos") or []):
                for op in (participant.get("opinioes") or []):
                    text = (op.get("opiniao") or "").strip()
                    if not text:
                        continue
                    verdict = op.get("verificacao_alucinacao") or {}
                    recs.append({"ref": ref, "i": k, "opiniao": text,
                                 "envolvido": (participant.get("nome") or "").strip(),
                                 "hall": int(bool(verdict.get("verificacao_manual"))),
                                 "chunks": [str(c) for c in (op.get("chunks_proximos") or [])]})
                    k += 1
        D = pd.DataFrame(recs)
    required = {"ref", "i", "opiniao", "envolvido", "hall", "chunks"}
    if not required.issubset(D.columns) or D.empty or D.duplicated(["ref", "i"]).any():
        raise ValueError("Invalid or duplicate official-chunk records")
    expected_refs = set(R.refs_ok())
    if set(D.ref) != expected_refs:
        raise ValueError("Chunk cache does not cover the processed corpus")
    D = D.sort_values(["ref", "i"]).reset_index(drop=True)
    # alinhamento com opinions_XXX.csv (fonte dos embeddings e dos votos dos juízes)
    bad = 0
    for ref, g in D.groupby("ref"):
        c = R.opinions(ref)
        if c is None or len(c) != len(g) or \
           [str(x).strip() for x in c.opiniao] != g.opiniao.tolist() or \
           [int(bool(x)) for x in c.alucinacao_manual] != g.hall.tolist():
            bad += 1
            print(f"[ALERTA] {ref}: desalinhado com opinions_XXX.csv")
    if bad:
        raise SystemExit(f"{bad} audiencias desalinhadas — nao prossiga.")
    D.to_json(CHUNKS_JSONL, orient="records", lines=True, force_ascii=False)
    return D


def _ws(s: str) -> str:
    return re.sub(r"\s+", " ", str(s)).strip().lower()


def main() -> None:
    E0.banner("M0 — PROTOCOLO DE ANOTAÇÃO: o que o rótulo mede")
    D = carregar()
    y = D.hall.to_numpy().astype(bool)
    print(f"  opinioes: {len(D)} · audiencias: {D.ref.nunique()} · "
          f"alucinacoes humanas: {int(y.sum())} ({y.mean():.2%})")
    print(f"  chunks por opiniao: {D.chunks.map(len).value_counts().to_dict()}")

    # ---- (c) o que um juiz lê
    ch_chars = D.chunks.map(lambda c: sum(len(x) for x in c))
    print(f"  caracteres lidos por um juiz (4 chunks): media {ch_chars.mean():.0f}, "
          f"mediana {ch_chars.median():.0f}, p95 {ch_chars.quantile(.95):.0f}")
    print(f"  caracteres da opiniao: media {D.opiniao.str.len().mean():.0f}")

    # ---- (d) os chunks saem dos turnos do orador atribuído?
    rows = []
    for ref, g in D.groupby("ref", sort=True):
        fr = R.phrases(ref, "transcript")
        spk = H6.speakers(fr)
        cands = sorted({s for s in spk if s})
        # texto normalizado e mapa posição -> índice de frase
        off, pos = [], 0
        partes = []
        for s in fr:
            t = _ws(s)
            off.append(pos)
            partes.append(t)
            pos += len(t) + 1
        txt = " ".join(partes)
        off = np.array(off)
        for _, r in g.iterrows():
            m = H6.match_gold(r.envolvido, cands)
            achou = dentro = 0
            for c in r.chunks:
                cc = _ws(c)
                # o chunk vem da fala do orador: sem o marcador "O SR. X -"; busca um
                # trecho do meio do chunk para não depender de limites de frase
                n = len(cc)
                if n < 40:
                    continue
                probe = cc[n // 4: n // 4 + 60]
                p = txt.find(probe)
                if p < 0:
                    continue
                achou += 1
                idx = int(np.searchsorted(off, p, side="right") - 1)
                if m is not None and spk[idx] == m:
                    dentro += 1
            rows.append({"ref": ref, "i": int(r.i), "hall": int(r.hall),
                         "match_orador": int(m is not None),
                         "chunks_achados": achou, "chunks_no_orador": dentro,
                         "chars_chunks": int(sum(len(x) for x in r.chunks)),
                         "chars_opiniao": len(r.opiniao)})
    P = pd.DataFrame(rows)
    P.to_csv(E0.OUT / "official_chunks.csv", index=False)
    mt = P.match_orador == 1
    tot = int(P.chunks_achados[mt].sum())
    print(f"\n  opinioes com orador casado por nome: {mt.sum()} ({mt.mean():.1%})")
    print(f"  chunks localizados na transcricao: {int(P.chunks_achados.sum())} de "
          f"{4 * len(P)} ({P.chunks_achados.sum() / (4 * len(P)):.1%})")
    if tot:
        print(f"  entre os localizados (opinioes casadas): "
              f"{P.chunks_no_orador[mt].sum() / tot:.1%} estao nos turnos do orador casado")
    full = P[mt & (P.chunks_achados == 4)]
    if len(full):
        print(f"  opinioes casadas com os 4 chunks localizados: {len(full)}; "
              f"com >=3 dos 4 no orador casado: "
              f"{(full.chunks_no_orador >= 3).mean():.1%}")


if __name__ == "__main__":
    main()

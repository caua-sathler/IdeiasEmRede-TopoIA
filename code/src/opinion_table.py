"""Opinion-level table: one row per labelled opinion, with the quantities shared by all analyses.

Columns: ref (hearing), hall (human verdict: 1 = possible hallucination), cos_g (best cosine
match in the whole transcript), cos_s (best match in the attributed speaker's turns; empty if
the speaker could not be matched), sem_turno (1 = attributed speaker not matched to a speaker
of the transcript), n_irm (number of labelled opinions of the hearing attributed to the same
speaker), and the votes of the 12 LLM judges (juiz_p{1,2,3}_{gpt4omini,gpt4o,deepseek,sabia}).

All analyses use the rows with sem_turno == 0 (3,630 opinions, 408 positive).

    python opinion_table.py        # needs the processed dataset (dataset/README.md)
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import common as E0            # noqa: E402
import dataset_readers as R    # noqa: E402
import speaker_incidence as H6   # noqa: E402

warnings.filterwarnings("ignore")


def build():
    import pandas as pd

    rows = []
    refs = R.refs_ok()
    for ri, r in enumerate(refs):
        Tm = R.emb(r, "transcript", R.GEOM)
        g, ge = R.opinions(r), R.op_emb(r)
        if not len(Tm) or ge is None or len(g) != len(ge):
            continue
        fr = R.phrases(r, "transcript")[:len(Tm)]
        if len(fr) < len(Tm):
            fr = fr + [""] * (len(Tm) - len(fr))
        spk = H6.speakers(fr)
        cands = sorted({s for s in spk if s})
        if len(cands) < 2:
            continue
        S = ge @ Tm.T
        idx = {c: np.where(spk == c)[0] for c in cands}
        labelled = np.array([not pd.isna(v) for v in g.alucinacao_manual])
        gi = np.where(labelled)[0]
        if len(gi) < 3:
            continue
        M = np.array([[float(S[i, idx[c]].max()) for c in cands] for i in gi])
        cos_g = np.array([float(S[i].max()) for i in gi])
        quem = (g.envolvido.to_numpy()[gi] if "envolvido" in g
                else np.array([None] * len(gi)))
        atr = np.array([cands.index(m) if (m := H6.match_gold(q_, cands)) else -1
                        for q_ in quem])
        matched = atr >= 0
        if matched.sum() < 3:
            continue
        n_irm = np.zeros(len(gi))
        for a in np.unique(atr[atr >= 0]):
            n_irm[atr == a] = int((atr == a).sum())
        for kk, o in enumerate(gi):
            row = {"ref": r, "hall": int(bool(g.alucinacao_manual.iloc[o])),
                   "cos_g": cos_g[kk],
                   "cos_s": M[kk, atr[kk]] if matched[kk] else np.nan,
                   "sem_turno": int(not matched[kk]), "n_irm": n_irm[kk]}
            for j in H6.JUIZES:
                if j in g:
                    v = g[j].iloc[o]
                    if not pd.isna(v):
                        row[j] = int(bool(v))
            rows.append(row)
        if (ri + 1) % 50 == 0:
            print(f"  {ri+1}/{len(refs)} · {len(rows)} opinions", flush=True)
    D = pd.DataFrame(rows)
    D.to_csv(E0.OUT / "opinion_table.csv", index=False)
    return D


if __name__ == "__main__":
    E0.exigir_dados()
    D = build()
    print(f"opinions: {len(D)} · matched: {int((D.sem_turno == 0).sum())} · "
          f"positives (matched): {int(D[D.sem_turno == 0].hall.sum())}")

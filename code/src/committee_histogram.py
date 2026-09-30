"""J12 - histogram of the committee's 13 vote levels, per class.

Computes pos/neg counts per vote level from nli_features.csv (votes = sum of
the 12 juiz_* columns), tau = sum_k pi+_k pi-_k, and prints TikZ coordinates
for the figure in Section 7.1 (paste, do not edit by hand).

    python committee_histogram.py [path/to/nli_features.csv]
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

HERE = Path(__file__).resolve().parent
default = HERE.parent / "results" / "nli_features.csv"
D = pd.read_csv(sys.argv[1] if len(sys.argv) > 1 else default)
J = [c for c in D.columns if c.startswith("juiz_")]
assert len(J) == 12
v = D[J].sum(axis=1).to_numpy(); y = D.hall.to_numpy().astype(bool)
P, N = int(y.sum()), int((~y).sum())
pos = np.bincount(v[y], minlength=13); neg = np.bincount(v[~y], minlength=13)
pp, pn = pos / P, neg / N
terms = pp * pn; tau = terms.sum()
print(f"n={len(D)} P={P} N={N}")
for k in range(13):
    print(f"votes {k:2d}: pos {pos[k]:4d}  neg {neg[k]:5d}  pi+={pp[k]:.4f} pi-={pn[k]:.4f}  tau_k={terms[k]:.5f}")
print(f"tau={tau:.5f}  tau/2={tau/2:.4f}")
print(f"level 0 share of tau={terms[0]/tau:.3f}; levels 0-1={terms[:2].sum()/tau:.3f}")
print(f"zero-vote share of opinions={(v==0).mean():.3f}; pos with 0-1 votes={pos[:2].sum()} ({pos[0]}+{pos[1]})")
print(f"neg share at 0={pn[0]:.3f}; pos share at 0={pp[0]:.3f}; pos share at 12={pp[12]:.3f}")
print("\n% TikZ coordinates (y in percent of class)")
print("neg:", " ".join(f"({k},{100*pn[k]:.1f})" for k in range(13)))
print("pos:", " ".join(f"({k},{100*pp[k]:.1f})" for k in range(13)))

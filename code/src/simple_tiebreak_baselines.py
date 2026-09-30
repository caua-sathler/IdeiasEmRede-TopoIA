"""Exploratory controls: break committee ties without training or NLI.

Uses shipped tables only. Saves AUROCs and paired hearing-bootstrap intervals;
the full secondary detector is fitted out of fold on the reference partition.
These controls were added during submission revision, not preregistered.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.preprocessing import StandardScaler

import common
from lexicographic_combination import join
from speaker_incidence import JUIZES


def main():
    d = pd.read_csv(common.OUT / "opinion_table.csv")
    d = d[d.sem_turno == 0].reset_index(drop=True)
    f = pd.read_csv(common.OUT / "incidence_features.csv")
    nli = pd.read_csv(common.OUT / "nli_features.csv")
    for other in (f, nli):
        assert len(other) == len(d)
        assert np.array_equal(other.ref, d.ref)
        assert np.array_equal(other.hall, d.hall)
        assert np.allclose(other.cos_s, d.cos_s)
    y, groups = d.hall.to_numpy(bool), d.ref.to_numpy()
    votes = d[JUIZES].to_numpy(float)
    assert np.isfinite(votes).all()
    base = votes.sum(axis=1)
    cols = ["cos_s", "best_other", "share_attr", "n_spk_sup", "attr_in_sup",
            "rank_spk", "nli_s", "nli_g", "delta_n"]
    X = np.column_stack([nli[cols].fillna(0).to_numpy(float), d.n_irm])
    fine = np.zeros(len(d))
    for tr, te in GroupKFold(5).split(X, y, groups):
        scaler = StandardScaler().fit(X[tr])
        model = LogisticRegression(max_iter=3000, class_weight="balanced")
        model.fit(scaler.transform(X[tr]), y[tr])
        fine[te] = model.predict_proba(scaler.transform(X[te]))[:, 1]
    scores = {
        "committee": base,
        "cos_s": join(base, -d.cos_s.to_numpy()),
        "delta": join(base, f.delta2.to_numpy()),
        "full_oof": join(base, fine),
    }
    rng = np.random.default_rng(20260930)
    hearings = np.unique(groups)
    rows = {h: np.flatnonzero(groups == h) for h in hearings}
    diffs = {name: [] for name in scores if name != "committee"}
    incremental = []
    for _ in range(3000):
        idx = np.concatenate([rows[h] for h in rng.choice(hearings, len(hearings), replace=True)])
        if not 0 < y[idx].sum() < len(idx):
            continue
        aucs = {name: common.auc(y[idx], s[idx]) for name, s in scores.items()}
        for name in diffs:
            diffs[name].append(aucs[name] - aucs["committee"])
        incremental.append(aucs["full_oof"] - aucs["delta"])
    results = []
    for name, score in scores.items():
        lo, hi = np.percentile(diffs[name], [2.5, 97.5]) if name in diffs else (0., 0.)
        results.append(dict(method=name, auroc=common.auc(y, score),
                            gain=common.auc(y, score)-common.auc(y, base),
                            ci_low=lo, ci_high=hi, nli_pairs=10 if name == "full_oof" else 0,
                            trained=name == "full_oof"))
    result = pd.DataFrame(results)
    result.to_csv(common.OUT / "simple_tiebreak_baselines.csv", index=False)
    print(result.to_string(index=False, float_format=lambda x: f"{x:.6f}"))
    lo, hi = np.percentile(incremental, [2.5, 97.5])
    print(f"Full OOF minus direct delta: {common.auc(y, scores['full_oof'])-common.auc(y, scores['delta']):+.6f}; "
          f"paired 95% CI [{lo:+.6f}, {hi:+.6f}]")
    print("Exploratory comparison; overlap with zero is not evidence of equivalence.")


if __name__ == "__main__":
    main()

"""J13 — Does Equation (3) PREDICT the gain on unseen hearings?

Equation (3) of the paper, AUROC(lex) = AUROC(s1) + tau * (a2 - 1/2), is an
exact identity when tau and a2 are measured on the same data. A reviewer
pointed out that this cannot "confirm" anything. This script turns it into a
genuine forecast:

    1. split the hearings at random into a DEV half and a TEST half;
    2. fit the secondary detector on DEV only, and measure a2 on DEV with
       out-of-fold scores (GroupKFold inside DEV);
    3. compute tau on TEST from the judges' votes alone (no secondary needed);
    4. predict the TEST gain as tau_test * (a2_dev - 1/2);
    5. compare with the gain actually observed on TEST, where the secondary
       detector was never fitted.

Repeated over R random splits and committee sizes k in {1, 3, 5, 8, 12}
(random judge subset per split). As a contrast, the same forecast is made with
the secondary detector's GLOBAL AUROC on DEV in place of a2: Remark 3 of the
paper says the global AUROC is the wrong quantity.

Part (B) gives hearing-clustered confidence intervals for the gain of the
lexicographic combination over each single judge (OOF secondary on the full
matched set, as in j6).

    python j13_previsao.py            # R = 50 splits, 2000 bootstrap resamples
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import comum as E0                        # noqa: E402
import h6_orador as H6                    # noqa: E402
from j4_reticulado import deficit, join   # noqa: E402

warnings.filterwarnings("ignore")
SEED = 20260925
R = 50
KS = (1, 3, 5, 8, 12)
N_BOOT = 2000


def a2_ties(y, prim, sec) -> float:
    """AUROC of `sec` restricted to the positive-negative pairs `prim` ties."""
    win = tot = 0.0
    for v in np.unique(prim):
        m = prim == v
        sp, sn = np.sort(sec[m & y]), np.sort(sec[m & ~y])
        if len(sp) == 0 or len(sn) == 0:
            continue
        lo = np.searchsorted(sn, sp, side="left")
        hi = np.searchsorted(sn, sp, side="right")
        win += lo.sum() + 0.5 * (hi - lo).sum()
        tot += len(sp) * len(sn)
    return win / tot if tot else np.nan


def main() -> None:
    import pandas as pd
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import GroupKFold
    from sklearn.preprocessing import StandardScaler

    # Same inputs and feature set as j6_estabilidade.py.
    Di = pd.read_csv(E0.OUT / "i2_hodge.csv")
    h7 = pd.read_csv(E0.OUT / "h7_nli_orador.csv")
    Mk = Di.sem_turno.to_numpy() == 0
    sub = Di[Mk].reset_index(drop=True)
    y = sub.hall.to_numpy().astype(bool)
    gm = sub.ref.to_numpy()
    FAM = ["cos_s", "best_other", "share_attr", "n_spk_sup", "attr_in_sup",
           "rank_spk", "nli_s", "nli_g", "delta_n"]
    X = np.hstack([h7[FAM].fillna(0).to_numpy(float),
                   sub[["n_irm"]].fillna(0).to_numpy(float)])
    JU = [j for j in H6.JUIZES if j in sub and sub[j].notna().sum() > 3000]
    V = sub[JU].fillna(0).to_numpy(float)
    print(f"n = {len(y)} · positives = {int(y.sum())} · judges = {len(JU)}")

    def fit(Xtr, ytr):
        sc = StandardScaler().fit(Xtr)
        c = LogisticRegression(max_iter=3000, class_weight="balanced")
        c.fit(sc.transform(Xtr), ytr)
        return lambda Z: c.predict_proba(sc.transform(Z))[:, 1]

    def oof(idx):
        z = np.zeros(len(idx))
        for tr, te in GroupKFold(5).split(X[idx], y[idx], gm[idx]):
            z[te] = fit(X[idx][tr], y[idx][tr])(X[idx][te])
        return z

    # ------------------------------------------------------------------ (A)
    E0.banner("(A) FORECASTING THE TEST GAIN FROM DEV-ONLY QUANTITIES")
    rng = np.random.default_rng(SEED)
    hs = np.unique(gm)
    rows = []
    for r in range(R):
        dev_h = set(rng.choice(hs, len(hs) // 2, replace=False))
        dev = np.array([g in dev_h for g in gm])
        di, ti = np.where(dev)[0], np.where(~dev)[0]
        s_dev = oof(di)                      # OOF inside DEV
        s_test = fit(X[di], y[di])(X[ti])    # fitted on DEV only
        for k in KS:
            J = (np.arange(len(JU)) if k == len(JU)
                 else rng.choice(len(JU), k, replace=False))
            p_dev, p_test = V[di][:, J].sum(1), V[ti][:, J].sum(1)
            a2 = a2_ties(y[di], p_dev, s_dev)
            ag = E0.auc(y[di], s_dev)
            tau_t = deficit(y[ti], p_test)[0]
            obs = E0.auc(y[ti], join(p_test, s_test)) - E0.auc(y[ti], p_test)
            rows.append(dict(r=r, k=k, tau=tau_t, a2=a2, aglob=ag, obs=obs,
                             pred=tau_t * (a2 - 0.5),
                             pred_glob=tau_t * (ag - 0.5)))
    D = pd.DataFrame(rows)
    D.to_csv(E0.OUT / "j13_previsao.csv", index=False)

    print(f"  {R} random dev/test splits of hearings; gains in AUROC on TEST.\n")
    print(f"  {'k':>3s} {'tau_test':>9s} {'a2_dev':>7s} {'observed':>9s} "
          f"{'pred(a2)':>9s} {'MAE(a2)':>8s} {'pred(glob)':>10s} "
          f"{'MAE(glob)':>9s}")
    print("  " + "-" * 72)
    for k, g in D.groupby("k"):
        print(f"  {k:3d} {g.tau.mean():9.4f} {g.a2.mean():7.3f} "
              f"{g.obs.mean():+9.4f} {g.pred.mean():+9.4f} "
              f"{(g.pred - g.obs).abs().mean():8.4f} "
              f"{g.pred_glob.mean():+10.4f} "
              f"{(g.pred_glob - g.obs).abs().mean():9.4f}")
    rho = np.corrcoef(D.pred, D.obs)[0, 1]
    rho_g = np.corrcoef(D.pred_glob, D.obs)[0, 1]
    print(f"\n  pooled correlation, predicted vs observed: a2 {rho:.3f} · "
          f"global AUROC {rho_g:.3f}")
    ok = (np.sign(D.pred) == np.sign(D.obs)).mean()
    print(f"  sign of the gain predicted correctly: {ok:.0%} of "
          f"{len(D)} (split, k) cases")

    # ------------------------------------------------------------------ (B)
    E0.banner("(B) GAIN OVER EACH SINGLE JUDGE, HEARING-CLUSTERED 95% CI")
    z = oof(np.arange(len(y)))
    us = np.unique(gm)
    mp = {u: np.where(gm == u)[0] for u in us}
    rb = np.random.default_rng(SEED)
    boots = [np.concatenate([mp[u] for u in us[rb.integers(0, len(us), len(us))]])
             for _ in range(N_BOOT)]
    gains = []
    print(f"  {'judge':22s} {'alone':>7s} {'+ rule':>7s} {'gain':>8s} "
          f"{'95% CI':>20s}")
    print("  " + "-" * 68)
    for i, j in enumerate(JU):
        a, b = V[:, i], join(V[:, i], z)
        d = [E0.auc(y[s], b[s]) - E0.auc(y[s], a[s]) for s in boots
             if 0 < y[s].sum() < len(s)]
        lo, hi = np.percentile(d, [2.5, 97.5])
        g = E0.auc(y, b) - E0.auc(y, a)
        gains.append((g, lo, hi))
        print(f"  {j:22s} {E0.auc(y, a):7.4f} {E0.auc(y, b):7.4f} "
              f"{g:+8.4f} [{lo:+.4f}, {hi:+.4f}]")
    G = np.array(gains)
    print(f"\n  median gain {np.median(G[:, 0]):+.4f} · range "
          f"[{G[:, 0].min():+.4f}, {G[:, 0].max():+.4f}] · "
          f"CI excludes zero for {(G[:, 1] > 0).sum()}/{len(G)} judges")


if __name__ == "__main__":
    main()

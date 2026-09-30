"""J10 — O PORTÃO: o lexicográfico e a soma aditiva são um só operador.

    f_γ(x) = r₁(x) + γ · r₂(x)          r₁ = nível do comitê, r₂ = posto ∈ [0,1]

γ é interpretável: **quantos níveis do comitê o escore barato tem licença para
mover um item**.

    γ < 1   nenhuma inversão é possível  ->  É o LEXICOGRÁFICO
    γ ≥ 1   o secundário move ate ⌊γ⌋ niveis
    γ -> ∞  a ordem tende a do secundario puro (a soma aditiva sem declarar)

A COTA (provada em `j10_predicoes.md` §2): nenhum par separado por g ≥ γ níveis
pode ser invertido. Com `τ_γ = Pr[0 < g < γ]`,

    AUROC(s1) − τ/2 − τ_γ  ≤  AUROC(f_γ)  ≤  AUROC(s1) + τ/2 + τ_γ

e `τ_γ` sai só do comitê, antes de olhar o secundário — a mesma propriedade que
torna `τ/2` útil. Em γ<1, τ_γ = 0 e recuperamos o Teorema 15.

O DESENHO QUE IMPORTA. O `j9` mediu `a3 = 0,473`: a família e pior que o acaso
onde o comite erra, logo abrir o portao deve perder. Mas isso sozinho nao separa
"o operador e ruim" de "o detector e cego". Entao a mesma discagem roda com
secundarios de qualidade CONTROLADA — a familia, um clarividente (s2 = y) e
clarividentes corrompidos a taxa p — para achar QUAO BOM um detector precisaria
ser para o portao compensar.

    python gamma_sweep.py
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import common as E0                          # noqa: E402
import speaker_incidence as H6                      # noqa: E402
from lexicographic_combination import deficit, join     # noqa: E402

warnings.filterwarnings("ignore")
SEED = 42
FAM = ["cos_s", "best_other", "share_attr", "n_spk_sup", "attr_in_sup",
       "rank_spk", "nli_s", "nli_g", "delta_n"]
GAMAS = (0.5, 1.0, 1.5, 2.0, 3.0, 5.0, 8.0, 13.0, 30.0)


def postos(s: np.ndarray) -> np.ndarray:
    """Posto medio normalizado em [0,1]."""
    import pandas as pd
    r = pd.Series(s).rank(method="average").to_numpy()
    return (r - r.min()) / max(r.max() - r.min(), 1e-9)


def niveis(s1: np.ndarray) -> np.ndarray:
    import pandas as pd
    return pd.Series(s1).rank(method="dense").to_numpy()


def portao(s1: np.ndarray, s2: np.ndarray, gama: float) -> np.ndarray:
    return niveis(s1) + gama * postos(s2)


def main() -> None:
    import pandas as pd
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import GroupKFold
    from sklearn.preprocessing import StandardScaler

    Di = pd.read_csv(E0.OUT / "opinion_table.csv")
    h7 = pd.read_csv(E0.OUT / "nli_features.csv")
    Mk = Di.sem_turno.to_numpy() == 0
    sub = Di[Mk].reset_index(drop=True)
    assert len(h7) == len(sub) and np.allclose(h7.cos_s, sub.cos_s, atol=1e-6)
    print("  [ok] alinhamento verificado linha a linha")
    y = sub.hall.to_numpy().astype(bool)
    gm = sub.ref.to_numpy()

    Xf = np.hstack([h7[FAM].fillna(0).to_numpy(float),
                    sub[["n_irm"]].fillna(0).to_numpy(float)])
    JU = [j for j in H6.JUIZES if j in sub and sub[j].notna().sum() > 3000]
    V = sub[JU].fillna(0).to_numpy(float)
    base = V.sum(1)
    a_base = E0.auc(y, base)
    tau, _, _ = deficit(y, base)

    z = np.zeros(len(y))
    for tr, te in GroupKFold(5).split(Xf, y, gm):
        sc = StandardScaler().fit(Xf[tr])
        c = LogisticRegression(max_iter=5000, class_weight="balanced")
        c.fit(sc.transform(Xf[tr]), y[tr])
        z[te] = c.predict_proba(sc.transform(Xf[te]))[:, 1]
    fino = z

    # --- geometria dos pares, computada uma vez
    nv = niveis(base)
    gap = nv[y][:, None] - nv[~y][None, :]      # niveis: >0 comite certo
    absg = np.abs(gap)
    tot = gap.size

    def tau_gama(g_):
        """massa de pares (pos,neg) recem-alcancavel: separados por 0 < g < γ."""
        return float(((absg > 0) & (absg < g_)).sum()) / tot

    def analisa(s, g_):
        """AUROC, inversoes e violacoes da cota, para f_γ com secundario s."""
        f = portao(base, s, g_)
        d = f[y][:, None] - f[~y][None, :]
        a = float(((d > 0).sum() + 0.5 * (d == 0).sum()) / tot)
        inv = (gap > 0) & (d < 0)
        inv |= (gap < 0) & (d > 0)
        # a cota: nenhum par com separacao >= γ pode inverter
        viol = int((inv & (absg >= g_)).sum())
        return a, float(inv.sum()) / tot, viol

    E0.banner("P1/P2 — A DISCAGEM COM A FAMILIA REAL, e a cota")
    print(f"  comite = {a_base:.4f} · tau = {tau:.4%} · tau/2 = {tau/2:.4f}")
    print(f"  lexicografico (join do artigo) = {E0.auc(y, join(base, fino)):.4f}")
    print(f"\n  {'gama':>6s} {'tau_gama':>9s} {'cota inf':>9s} {'cota sup':>9s} "
          f"{'AUROC':>8s} {'inversoes':>10s} {'violacoes':>10s}")
    print("  " + "-" * 70)
    for g_ in GAMAS:
        tg = tau_gama(g_)
        a, inv, viol = analisa(fino, g_)
        print(f"  {g_:6.1f} {tg:9.4f} {a_base-tau/2-tg:9.4f} "
              f"{a_base+tau/2+tg:9.4f} {a:8.4f} {inv:10.2%} "
              f"{viol:10d}")
    print("\n  'violacoes' = pares invertidos com separacao >= gama. A cota da")
    print("  §2 do registro diz que tem de ser ZERO em toda linha.")

    E0.banner("P4 — O MESMO PORTAO COM UM DETECTOR CLARIVIDENTE (s2 = y)")
    rng = np.random.default_rng(SEED)
    clar = y.astype(float) + rng.normal(0, 1e-6, len(y))   # desempata ties
    print(f"  {'gama':>6s} {'AUROC':>8s} {'ganho vs comite':>16s}")
    print("  " + "-" * 36)
    for g_ in GAMAS:
        a, _, _ = analisa(clar, g_)
        print(f"  {g_:6.1f} {a:8.4f} {a-a_base:+16.4f}")
    print(f"\n  em gama<1 isto tem de dar exatamente {a_base + tau/2:.4f} "
          f"(= AUROC + tau/2),")
    print("  o teto do desempate. Se cresce com gama, o MECANISMO funciona e o")
    print("  que falta e o detector.")

    E0.banner("P6 — QUAO BOM PRECISARIA SER? clarividente corrompido a taxa p")
    print("  s2 = y com o rotulo trocado com probabilidade p (20 sorteios por p).")
    a_lex = E0.auc(y, join(base, fino))
    print(f"  alvo a bater: o lexicografico com a familia = {a_lex:.4f}\n")
    print(f"  {'p':>5s} {'a3 do detector':>15s} {'melhor gama':>12s} "
          f"{'AUROC(melhor)':>14s} {'bate o lex?':>12s}")
    print("  " + "-" * 64)
    ok, sep = gap > 0, gap < 0
    for p in (0.0, 0.10, 0.20, 0.30, 0.40, 0.45, 0.50):
        melhor_a, melhor_g, a3s = -1.0, None, []
        for g_ in GAMAS:
            vals = []
            r2 = np.random.default_rng(SEED + 1)
            for _ in range(20):
                s2 = np.where(r2.random(len(y)) < p, ~y, y).astype(float)
                s2 = s2 + r2.normal(0, 1e-6, len(y))
                a, _, _ = analisa(s2, g_)
                vals.append(a)
                if g_ == GAMAS[0]:
                    d2 = s2[y][:, None] - s2[~y][None, :]
                    a3s.append(float(((d2[sep] > 0).sum()
                                      + 0.5 * (d2[sep] == 0).sum())
                                     / max(int(sep.sum()), 1)))
            m = float(np.median(vals))
            if m > melhor_a:
                melhor_a, melhor_g = m, g_
        print(f"  {p:5.2f} {np.mean(a3s):15.4f} {melhor_g:12.1f} "
              f"{melhor_a:14.4f} {'SIM' if melhor_a > a_lex else 'nao':>12s}")
    print("\n  'a3 do detector' = AUROC dele nos pares que o comite ERRA.")
    print(f"  A familia real tem a3 = 0,473 (j9). Compare com a coluna.")
    print("  Note tambem: quanto MELHOR o detector, mais LARGO o gama otimo.")

    # ------------------------------------------------------------------ P3/P5
    E0.banner("P3/P5 — A CORCOVA EM gama=2 SOBREVIVE? (o teste que decide)")
    print("  Varri 9 valores de gama numa particao e peguei o maximo: isso e")
    print("  exatamente a armadilha que o j6 existe para pegar. Aqui vao as 20")
    print("  particoes, o IC pareado, e o nulo do desempate aleatorio.")

    nus = len(np.unique(gm))
    r6 = np.random.default_rng(SEED)

    def oof_perm(perm):
        us = np.unique(gm)
        gid = {u: i for i, u in enumerate(us[perm])}
        gg = np.array([gid[u] for u in gm])
        zz = np.zeros(len(y))
        for tr, te in GroupKFold(5).split(Xf, y, gg):
            sc = StandardScaler().fit(Xf[tr])
            c = LogisticRegression(max_iter=5000, class_weight="balanced")
            c.fit(sc.transform(Xf[tr]), y[tr])
            zz[te] = c.predict_proba(sc.transform(Xf[te]))[:, 1]
        return zz

    alvos = (0.5, 1.5, 2.0, 3.0)
    acc = {g_: [] for g_ in alvos}
    for _ in range(20):
        f_ = oof_perm(r6.permutation(nus))
        for g_ in alvos:
            acc[g_].append(E0.auc(y, portao(base, f_, g_)))
    med_lex = float(np.median(acc[0.5]))
    print(f"\n  {'gama':>6s} {'mediana':>9s} {'min':>8s} {'max':>8s} "
          f"{'> lex':>7s}")
    print("  " + "-" * 44)
    for g_ in alvos:
        v = np.array(acc[g_])
        print(f"  {g_:6.1f} {np.median(v):9.4f} {v.min():8.4f} {v.max():8.4f} "
              f"{(v > med_lex).mean():6.0%}")

    def dcl(a, b, nb=5000):
        us = np.unique(gm)
        mp = {u: np.where(gm == u)[0] for u in us}
        r7 = np.random.default_rng(SEED)
        d = []
        for _ in range(nb):
            s = np.concatenate([mp[u] for u in
                                us[r7.integers(0, len(us), len(us))]])
            if len(np.unique(y[s])) < 2:
                continue
            d.append(E0.auc(y[s], a[s]) - E0.auc(y[s], b[s]))
        d = np.array(d)
        return d.mean(), *np.percentile(d, [2.5, 97.5])

    print("\n  Pareado, bootstrap agrupado por audiencia:")
    ref = portao(base, fino, 0.5)
    for g_ in (1.5, 2.0, 3.0):
        mu, lo, hi = dcl(portao(base, fino, g_), ref)
        st = "*" if (lo > 0 or hi < 0) else " "
        print(f"    gama={g_:.1f} vs lexicografico: {mu:+.4f} "
              f"[{lo:+.4f},{hi:+.4f}]{st}")

    nul = np.array([E0.auc(y, join(base, r6.random(len(y))))
                    for _ in range(200)])
    a2_ = E0.auc(y, portao(base, fino, 2.0))
    print(f"\n  nulo do desempate aleatorio (200 sorteios): media "
          f"{nul.mean():.4f}, max {nul.max():.4f}")
    print(f"  gama=2 na particao de referencia: {a2_:.4f} "
          f"-> p = {(nul >= a2_).mean():.3f}")
    print(f"  lexicografico: {E0.auc(y, ref):.4f} "
          f"-> p = {(nul >= E0.auc(y, ref)).mean():.3f}")


if __name__ == "__main__":
    main()

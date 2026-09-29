"""K3 — Data for the presentation dashboard (apresentacao/dashboard).

Writes out/dashboard_dados.json with everything the dashboard draws:

  exemplos   real opinions with the best-matching sentence of every speaker
             (the "who said it?" panel), from the same MPNet similarities as
             h6/h6c/k1;
  comite     for k = 1..12 judges, the vote-level counts of positives and
             negatives for a typical subset (the one with median AUROC among
             60 random subsets), its tie fraction tau, and its AUROC alone and
             with lexicographic tie-breaking;
  escada     medians over 60 random subsets per k (j9_teto.py, section C);
  previsao   the 250 (split, k) forecasts of j13_previsao.py;
  fila       review-queue curves of the paper's Figure 3 (j11_operacao.py);
  mecanismo  the pair decomposition of Table 3 (j7).

    python k3_dashboard_dados.py
"""
from __future__ import annotations

import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import comum as E0                        # noqa: E402
import h6_orador as H6                    # noqa: E402
from j4_reticulado import deficit, join   # noqa: E402
from k1_auditoria_planilha import carregar  # noqa: E402

warnings.filterwarnings("ignore")
SEED = 20260927

# (ref, fragment of the opinion text, why it is shown)
EXEMPLOS = [
    ("data_001", "jornalistas presentes", "exemplo do artigo (Figura 1)"),
    ("data_185", None, "má-atribuição (auditoria)"),
    ("data_155", None, "má-atribuição (auditoria)"),
    ("data_001", "__apoiada__", "opinião suportada (contraste)"),
]
AUDIT_IDX = {"data_185": 15, "data_155": 5}


def exemplo(ref, frag, nota):
    A = carregar(ref)
    g, S, spk = A["g"], A["S"], A["spk"]
    col = "opiniao"
    if frag == "__apoiada__":
        # the supported opinion of this hearing whose attributed speaker leads
        # the other speakers by the widest margin
        best_i, best_m = None, -9.0
        for k in range(len(g)):
            if pd.isna(g.alucinacao_manual.iloc[k]) or bool(g.alucinacao_manual.iloc[k]):
                continue
            mk = H6.match_gold(g.envolvido.iloc[k], A["cands"])
            if mk is None:
                continue
            bs = {c: float(S[k, js].max()) for c, js in A["idx_spk"].items() if len(js)}
            marg = bs[mk] - max(v for c, v in bs.items() if c != mk)
            if marg > best_m:
                best_i, best_m = k, marg
        i = best_i
    elif frag is not None:
        i = next(k for k, t in enumerate(g[col]) if frag in str(t))
    else:
        i = AUDIT_IDX[ref]
    quem = g.envolvido.iloc[i]
    m = H6.match_gold(quem, A["cands"])
    oradores = []
    for c, js in A["idx_spk"].items():
        if not len(js):
            continue
        j = js[np.argmax(S[i, js])]
        oradores.append(dict(nome=c, cos=round(float(S[i, j]), 3),
                             frase=A["fr"][j].strip()[:260],
                             n_frases=int(len(js))))
    oradores.sort(key=lambda d: -d["cos"])
    cos_s = next(d["cos"] for d in oradores if d["nome"] == m)
    outros = [d for d in oradores if d["nome"] != m]
    # turn strip: consecutive runs of the same speaker, with the run's best cos
    runs, cur, best, n = [], None, -1.0, 0
    for k, s in enumerate(spk):
        if s != cur and n:
            runs.append([cur or "", n, round(best, 3)])
            best, n = -1.0, 0
        cur = s
        best = max(best, float(S[i, k]))
        n += 1
    runs.append([cur or "", n, round(best, 3)])
    return dict(ref=ref, nota=nota, opiniao=str(g[col].iloc[i]).strip(),
                atribuido=str(quem), orador=m,
                rotulo="não suportada" if bool(g.alucinacao_manual.iloc[i])
                else "suportada",
                cos_s=cos_s, best_other=outros[0]["cos"],
                melhor_outro=outros[0]["nome"],
                delta=round(outros[0]["cos"] - cos_s, 3),
                oradores=(oradores[:7] if any(d["nome"] == m for d in oradores[:7])
                          else oradores[:6] + [d for d in oradores if d["nome"] == m]),
                turnos=runs)


def main() -> None:
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import GroupKFold
    from sklearn.preprocessing import StandardScaler

    out = {}
    out["exemplos"] = [exemplo(*e) for e in EXEMPLOS]
    for e in out["exemplos"]:
        print(f"  {e['ref']}: {e['atribuido']} -> best other {e['melhor_outro']}"
              f" | cos_s {e['cos_s']} best_other {e['best_other']} "
              f"| {e['rotulo']}")

    # ---- committee by k (same inputs as j6/j13)
    Di = pd.read_csv(E0.OUT / "i2_hodge.csv")
    h7 = pd.read_csv(E0.OUT / "h7_nli_orador.csv")
    sub = Di[Di.sem_turno.to_numpy() == 0].reset_index(drop=True)
    y = sub.hall.to_numpy().astype(bool)
    gm = sub.ref.to_numpy()
    FAM = ["cos_s", "best_other", "share_attr", "n_spk_sup", "attr_in_sup",
           "rank_spk", "nli_s", "nli_g", "delta_n"]
    X = np.hstack([h7[FAM].fillna(0).to_numpy(float),
                   sub[["n_irm"]].fillna(0).to_numpy(float)])
    JU = [j for j in H6.JUIZES if j in sub and sub[j].notna().sum() > 3000]
    V = sub[JU].fillna(0).to_numpy(float)
    z = np.zeros(len(y))
    for tr, te in GroupKFold(5).split(X, y, gm):
        sc = StandardScaler().fit(X[tr])
        c = LogisticRegression(max_iter=3000, class_weight="balanced")
        c.fit(sc.transform(X[tr]), y[tr])
        z[te] = c.predict_proba(sc.transform(X[te]))[:, 1]
    rng = np.random.default_rng(SEED)
    comite = []
    for k in range(1, len(JU) + 1):
        subs = ([np.arange(len(JU))] if k == len(JU) else
                [rng.choice(len(JU), k, replace=False) for _ in range(60)])
        aucs = [E0.auc(y, V[:, J].sum(1)) for J in subs]
        J = subs[int(np.argsort(aucs)[len(aucs) // 2])]
        v = V[:, J].sum(1)
        tau = deficit(y, v)[0]
        comite.append(dict(
            k=k, juizes=[JU[i].replace("juiz_", "") for i in J],
            pos=[int(((v == L) & y).sum()) for L in range(k + 1)],
            neg=[int(((v == L) & ~y).sum()) for L in range(k + 1)],
            tau=round(float(tau), 4), auc=round(E0.auc(y, v), 4),
            auc_lex=round(E0.auc(y, join(v, z)), 4)))
        print(f"  k={k:2d} tau={tau:.4f} auc={comite[-1]['auc']:.4f} "
              f"lex={comite[-1]['auc_lex']:.4f}")
    out["comite"] = comite
    out["totais"] = dict(n=int(len(y)), pos=int(y.sum()), neg=int((~y).sum()))

    # ---- ladder: j9_teto.py section (C), medians over 60 subsets per k
    out["escada"] = [
        dict(k=k, so=a, lex0=b, lex=c) for k, a, b, c in [
            (1, .8067, .8759, .8806), (2, .8746, .9017, .9035),
            (3, .8917, .9102, .9121), (4, .9030, .9160, .9180),
            (5, .9128, .9212, .9230), (6, .9148, .9221, .9241),
            (7, .9180, .9248, .9264), (8, .9205, .9255, .9272),
            (9, .9223, .9265, .9279), (10, .9239, .9276, .9291),
            (11, .9256, .9286, .9297), (12, .9260, .9290, .9301)]]

    # ---- forecast (j13)
    P = pd.read_csv(E0.OUT / "j13_previsao.csv")
    out["previsao"] = [dict(k=int(r.k), obs=round(r.obs, 5),
                            pred=round(r.pred, 5), glob=round(r.pred_glob, 5))
                       for r in P.itertuples()]

    # ---- review queue (paper Figure 3, j11_operacao.py section 7)
    xs = [2, 4, 6, 8, 10, 13, 16, 20, 25, 30, 40, 50]
    out["fila"] = dict(budget=xs, curvas=[
        dict(id="cos", nome="Similaridade global (0 chamadas)",
             y=[2.9, 6.6, 10.3, 12.3, 13.7, 17.6, 22.5, 28.2, 34.1, 38.5, 46.8, 57.4]),
        dict(id="fam", nome="Features de orador (0 chamadas)",
             y=[10.8, 19.1, 26.5, 33.6, 38.0, 45.1, 50.7, 56.1, 61.5, 65.9, 73.8, 81.1]),
        dict(id="juiz", nome="Melhor juiz sozinho (1 chamada)",
             y=[8.1, 16.3, 24.4, 32.3, 40.5, 52.9, 65.1, 81.4, 82.8, 83.9, 86.2, 88.4]),
        dict(id="lex", nome="Melhor juiz + desempate (1 chamada)",
             y=[15.0, 26.2, 37.0, 46.6, 52.2, 61.0, 71.1, 81.1, 85.0, 87.5, 90.4, 93.1]),
        dict(id="comite", nome="Comitê de 12 juízes",
             y=[16.9, 33.6, 48.0, 57.2, 64.7, 74.0, 80.0, 84.4, 88.4, 90.3, 93.3, 95.6]),
    ])
    out["mecanismo"] = dict(
        pares=1314576, separados=0.954, empatados=0.046,
        comite=dict(auc=.9260, sep=.9027, emp=.0232, inv=0.0),
        stacking=dict(auc=.9262, sep=.9013, emp=.0249, inv=1.33),
        lex=dict(auc=.9300, sep=.9027, emp=.0272, inv=0.0))

    f = E0.OUT / "dashboard_dados.json"
    f.write_text(json.dumps(out, ensure_ascii=False))
    print(f"\n  wrote {f} ({f.stat().st_size/1024:.0f} KB)")


if __name__ == "__main__":
    main()

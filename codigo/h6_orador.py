"""H6 — VERIFICAÇÃO CONDICIONADA AO ORADOR: a estrutura que ninguém usou no S3.

A OBSERVAÇÃO. Todo método barato testado (cos, NLI, Mapper, mundos) pontua a
opinião contra a transcrição INTEIRA. Mas o rótulo humano é "não sustentada pela
transcrição" — e uma opinião ATRIBUÍDA a um orador pode casar bem com a audiência
e não casar com OS TURNOS DAQUELE ORADOR. Má-atribuição é alucinação. O e13 provou
que a atribuição por cos_max funciona razoavelmente (0,622 de acurácia) — mas
nunca usamos o eixo orador como VERIFICADOR.

A RELAÇÃO NOVA é bipartida: opiniões × oradores (via marcadores de turno
`O SR. NOME -`), uma relação de Dowker que a agregação global destrói. Primeiro o
sinal escalar (este script); a topologia da relação só se o sinal existir.

PREDIÇÕES REGISTRADAS (antes de rodar):
    (i)   sanidade: cos_max global reproduz ~0,56 do d12 (n=4238, 504 pos);
    (ii)  o flag "envolvido sem turno na transcrição" concentra alucinação;
    (iii) cos_max condicionado ao orador > cos_max global como detector;
    (iv)  delta (global − orador) carrega o componente de má-atribuição.
COMPARAÇÃO: os 12 juízes LLM versionados, no MESMO conjunto de linhas.

Custo: zero chamadas de modelo (embeddings MPNET + regex de turnos, tudo local).

    python h6_orador.py
"""
from __future__ import annotations

import re
import sys
import unicodedata
import warnings
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import comum as E0            # noqa: E402
import dados as R           # noqa: E402

warnings.filterwarnings("ignore")
TURNO = re.compile(r"^\s*(?:O|A)\s+SRA?\.\s*([^-–—(]*)")
SEED = 42
JUIZES = ["juiz_p1_gpt4omini", "juiz_p1_gpt4o", "juiz_p1_deepseek",
          "juiz_p1_sabia", "juiz_p2_gpt4omini", "juiz_p2_gpt4o",
          "juiz_p2_deepseek", "juiz_p2_sabia", "juiz_p3_gpt4omini",
          "juiz_p3_gpt4o", "juiz_p3_deepseek", "juiz_p3_sabia"]


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z ]", " ", s.lower()).strip()


def toks(s: str) -> set:
    return {t for t in norm(s).split() if len(t) > 2}


def speakers(frases) -> np.ndarray:
    cur, out = None, []
    for s in frases:
        m = TURNO.match(str(s))
        if m and m.group(1).strip():
            cur = m.group(1).strip()
        out.append(cur)
    return np.array(out, dtype=object)


def match_gold(envolvido, cands):
    e = toks(envolvido)
    if not e:
        return None
    best, bs = None, 0
    for c in cands:
        ov = len(e & toks(c))
        if ov > bs:
            best, bs = c, ov
    need = 2 if len(e) >= 2 else 1
    return best if bs >= need else None


def main() -> None:
    import pandas as pd

    linhas = []
    refs = R.refs_ok()
    for ri, r in enumerate(refs):
        Tm = R.emb(r, "transcript", R.GEOM)
        g, ge = R.opinions(r), R.op_emb(r)
        if not len(Tm) or ge is None or len(g) != len(ge):
            continue
        fr = R.phrases(r, "transcript")[:len(Tm)]
        if len(fr) < len(Tm):
            fr = fr + [""] * (len(Tm) - len(fr))
        spk = speakers(fr)
        cands = sorted({s for s in spk if s})
        S = ge @ Tm.T                                 # opinioes x frases
        # mapa orador -> indices de frase (só turnos identificados)
        idx_spk = {c: np.where(spk == c)[0] for c in cands}
        for i in range(len(g)):
            lab = g.alucinacao_manual.iloc[i]
            if pd.isna(lab):
                continue
            row = {"ref": r, "hall": int(bool(lab)),
                   "cos_g": float(S[i].max())}
            quem = g.envolvido.iloc[i] if "envolvido" in g else None
            m = match_gold(quem, cands) if quem is not None else None
            row["sem_turno"] = int(m is None)
            if m is not None:
                js = idx_spk[m]
                cs = float(S[i, js].max())
                row["cos_s"] = cs
                row["delta"] = row["cos_g"] - cs
                # posto do melhor casamento do orador no ranking global
                row["rank_s"] = float((S[i] > cs).mean())
                row["n_frases_spk"] = int(len(js))
            for j in JUIZES:
                if j in g:
                    v = g[j].iloc[i]
                    if not pd.isna(v):
                        row[j] = int(bool(v))
            linhas.append(row)
        if (ri + 1) % 50 == 0:
            print(f"  {ri+1}/{len(refs)} audiencias · {len(linhas)} opinioes",
                  flush=True)

    D = pd.DataFrame(linhas)
    D.to_csv(E0.OUT / "h6_orador.csv", index=False)
    y = D.hall.to_numpy().astype(bool)
    rng = np.random.default_rng(SEED)
    print(f"\nopinioes com rotulo: {len(D)} · alucinadas: {int(y.sum())} "
          f"({y.mean():.1%}) · audiencias: {D.ref.nunique()}")

    E0.banner("(i) SANIDADE + (ii) O FLAG 'SEM TURNO'")
    print(f"  AUROC cos_max global ............ "
          f"{E0.auc(y, -D.cos_g.to_numpy(float)):.4f}   (d12: 0.5628)")
    st = D.sem_turno.to_numpy().astype(bool)
    print(f"  envolvido SEM turno ............. {st.mean():.1%} das opinioes")
    print(f"  taxa de alucinacao: sem turno {y[st].mean():.1%} "
          f"vs com turno {y[~st].mean():.1%}")
    print(f"  AUROC do flag sozinho ........... "
          f"{E0.auc(y, D.sem_turno.to_numpy(float)):.4f}")

    E0.banner("(iii)/(iv) — A FAMILIA CONDICIONADA AO ORADOR (so com turno casado)")
    M = ~st
    ym = y[M]
    sub = D[M]
    feats = [("cos_g", "cos_max global (baseline)", -1),
             ("cos_s", "cos_max NOS TURNOS DO ORADOR", -1),
             ("delta", "delta global - orador (ma-atribuicao)", +1),
             ("rank_s", "posto do orador no ranking global", +1)]
    print(f"  n={M.sum()} ({int(ym.sum())} alucinadas)")
    print(f"  {'feature':40s} {'AUROC':>7s}")
    print("  " + "-" * 50)
    for c, nome, sg in feats:
        v = sub[c].to_numpy(float) * sg
        print(f"  {nome:40s} {E0.auc(ym, v):7.4f}")

    def dauc(a, b, yy, nb=3000):
        d = []
        for _ in range(nb):
            i = rng.integers(0, len(yy), len(yy))
            if len(np.unique(yy[i])) < 2:
                continue
            d.append(E0.auc(yy[i], a[i]) - E0.auc(yy[i], b[i]))
        d = np.array(d)
        return d.mean(), *np.percentile(d, [2.5, 97.5])

    mu, lo, hi = dauc(-sub.cos_s.to_numpy(float), -sub.cos_g.to_numpy(float), ym)
    star = "  *" if (lo > 0 or hi < 0) else ""
    print(f"\n  pareado cos_orador vs cos_global: {mu:+.4f} "
          f"[{lo:+.4f},{hi:+.4f}]{star}")

    E0.banner("COMBINACAO OOF (GroupKFold por audiencia) + O PLACAR vs JUIZES LLM")
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import GroupKFold
    from sklearn.preprocessing import StandardScaler

    X = D[["cos_g", "sem_turno"]].copy()
    X["cos_s"] = D.cos_s.fillna(D.cos_s.median())
    X["delta"] = D.delta.fillna(0.0)
    X["rank_s"] = D.rank_s.fillna(D.rank_s.median())
    X = X.to_numpy(float)
    grp = D.ref.to_numpy()
    oof = np.zeros(len(D))
    for tr, te in GroupKFold(5).split(X, y, grp):
        sc = StandardScaler().fit(X[tr])
        clf = LogisticRegression(max_iter=2000, class_weight="balanced")
        clf.fit(sc.transform(X[tr]), y[tr])
        oof[te] = clf.predict_proba(sc.transform(X[te]))[:, 1]
    a_comb = E0.auc(y, oof)
    a_base = E0.auc(y, -D.cos_g.to_numpy(float))
    mu, lo, hi = dauc(oof, -D.cos_g.to_numpy(float), y)
    star = "  *" if lo > 0 else ""
    print(f"  combinacao orador (OOF, 5 folds) ....... {a_comb:.4f}")
    print(f"  vs cos_max global {a_base:.4f}: {mu:+.4f} [{lo:+.4f},{hi:+.4f}]{star}")
    print()
    print(f"  {'juiz LLM (voto binario, mesmo conjunto)':44s} {'AUROC':>7s}")
    print("  " + "-" * 54)
    ja = []
    for j in JUIZES:
        if j in D and D[j].notna().sum() > 3000:
            v = D[j].fillna(0).to_numpy(float)
            a = E0.auc(y, v)
            ja.append(a)
            print(f"  {j:44s} {a:7.4f}")
    if ja:
        print(f"\n  faixa dos juizes: {min(ja):.4f} – {max(ja):.4f} · "
              f"nossa combinacao barata: {a_comb:.4f}")
    print(f"\ngravado: {E0.OUT / 'h6_orador.csv'}")


if __name__ == "__main__":
    main()

"""H5 — A INTERVENÇÃO DE CONFLAÇÃO: as mesmas perguntas, mudando só o MODO.

A lei de conflação (RESULTADOS_H §3) prevê ONDE a entropia semântica tem de
falhar: onde a multiplicidade das respostas é compossível (elaboração), não
conflitual. Este experimento induz a mudança de regime NO MESMO dado: as mesmas
233 perguntas do TriviaQA (f11), o MESMO rótulo de corretude (o `ct` do modo
entidade — o conhecimento do modelo não muda com o formato), mudando só o modo:

    ENTIDADE (f11):  "David Seville"            -> conflação 12,6% (h2)
    FRASE (aqui):    uma frase completa com contexto breve

PREDIÇÕES REGISTRADAS (antes de rodar a análise):
    (i)   a conflação SOBE no modo frase (>= 40% contra 12,6%);
    (ii)  o AUROC da SE CAI no modo frase (contra 0,811 do modo entidade);
    (iii) WE >= SE no modo frase (pareado; o crossover que a lei prevê);
    (iv)  a QUEDA da SE entre modos é maior que a queda do WE (interação).

Uso:
    python conflation_intervention.py --gerar     # proxy, resumível
    python conflation_intervention.py             # NLI + análise
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import warnings
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

warnings.filterwarnings("ignore")
J_ENT = HERE.parent / "cache" / "f11_triviaqa.jsonl"
J_LON = HERE.parent / "cache" / "h5_longas.jsonl"
NPZ = HERE.parent / "cache" / "h5_nli.npz"
CJK = re.compile(r"[　-鿿가-힯]")
N = 8
TAU = 0.50
TAU_CON = 0.50
SEED = 42

PROMPT = """Answer the following trivia question with ONE complete sentence \
that states your answer and adds brief context. Answer in English.

Question: {q}
Answer:"""


def limpa(t: str) -> str:
    t = re.sub(r"\s+", " ", t.strip().strip('"'))
    t = re.sub(r"^(answer|resposta)\s*:\s*", "", t, flags=re.I)
    return t[:240]


def gerar() -> None:
    import llm
    itens = [json.loads(l) for l in J_ENT.read_text().splitlines() if l.strip()]
    itens = [d for d in itens if len(d["amostras"]) >= 6]
    feitos = set()
    if J_LON.exists():
        for ln in J_LON.read_text().splitlines():
            try:
                feitos.add(json.loads(ln)["qid"])
            except Exception:
                pass
    print(f"itens: {len(itens)} · ja gerados: {len(feitos)}", flush=True)
    fh = J_LON.open("a")
    for k, d in enumerate(itens):
        if d["qid"] in feitos:
            continue
        pr = PROMPT.format(q=d["pergunta"])
        am = []
        for s in range(N):
            try:
                t = limpa(llm.gen(pr, temp=1.0, seed=5000 + s))
            except Exception:
                t = ""
            if t and not CJK.search(t):
                am.append(t)
        if len(am) < N - 2:
            print(f"  [pula {d['qid']}] so {len(am)}", flush=True)
            continue
        fh.write(json.dumps({"qid": d["qid"], "amostras": am},
                            ensure_ascii=False) + "\n")
        fh.flush()
        if (k + 1) % 10 == 0:
            print(f"  {k+1}/{len(itens)}", flush=True)
    print("geracao concluida", flush=True)


def analisar() -> None:
    import pandas as pd
    import common as E0
    import finite_space as F
    import triviaqa_collect as F11
    import event_structure as H

    ent_itens = {d["qid"]: d for l in [None] for d in
                 (json.loads(x) for x in J_ENT.read_text().splitlines()
                  if x.strip()) if len(d["amostras"]) >= 6}
    # DEDUP por qid: o gerador foi retomado varias vezes e o jsonl acumulou
    # linhas repetidas (247 linhas / 202 qids). Sem isto, ~18% dos itens entram
    # DUAS vezes, inflando n e correlacionando erros. Mantem a primeira ocorrencia.
    lon, vistos = [], set()
    for l in J_LON.read_text().splitlines():
        if not l.strip():
            continue
        d = json.loads(l)
        if d["qid"] in vistos or d["qid"] not in ent_itens:
            continue
        if len(d["amostras"]) < 6:
            continue
        vistos.add(d["qid"])
        lon.append(d)
    print(f"itens pareados (entidade + frase): {len(lon)}", flush=True)

    # ---- NLI dos pares do modo frase (retomavel)
    chaves, pares = [], []
    for k, d in enumerate(lon):
        A = d["amostras"]
        for i in range(len(A)):
            for j in range(len(A)):
                if i != j:
                    chaves.append((k, i, j))
                    pares.append((A[i], A[j]))
    print(f"pares NLI: {len(pares)}", flush=True)
    ent = np.full(len(pares), -1.0, np.float32)
    con = np.full(len(pares), -1.0, np.float32)
    feito = 0
    if NPZ.exists():
        z = np.load(NPZ)
        if int(z["k"]) == len(pares):
            ent, con = z["ent"].copy(), z["con"].copy()
            feito = int(z["feito"])
            print(f"cache: {feito}/{len(pares)}", flush=True)
    if feito < len(pares):
        import nli_runner
        nli_runner.NLI_BATCH = 64
        nli = nli_runner.make_nli()
        if nli is None:
            print("[ERRO] NLI indisponivel."); return
        LOTE = 4096
        for s in range(feito, len(pares), LOTE):
            pr = nli(pares[s:s + LOTE])
            ent[s:s + len(pr)] = pr[:, 0]
            con[s:s + len(pr)] = pr[:, 2]
            feito = s + len(pr)
            np.savez(NPZ, ent=ent, con=con, k=len(pares), feito=feito)
            print(f"  NLI {feito}/{len(pares)}", flush=True)
    VE = {c: float(v) for c, v in zip(chaves, ent)}
    VC = {c: float(v) for c, v in zip(chaves, con)}

    # ---- perfis do modo FRASE
    linhas = []
    for k, d in enumerate(lon):
        A = d["amostras"]
        n = len(A)
        M = np.array([[1.0 if i == j else VE.get((k, i, j), 0.0)
                       for j in range(n)] for i in range(n)]) >= TAU
        Cm = np.array([[VC.get((k, i, j), 0.0) for j in range(n)]
                       for i in range(n)]) >= TAU_CON
        T = F.fecho_transitivo(M)
        P, lab = F.reflexao_poset(T)
        m = len(P)
        p = np.array([(lab == c).sum() for c in range(m)], float)
        p /= p.sum()
        Cc = np.zeros((m, m), bool)
        for i in range(n):
            for j in range(n):
                if Cm[i, j]:
                    Cc[lab[i], lab[j]] = True
        prf = H.perfil_mundos(P, Cc, p)
        e = ent_itens[d["qid"]]
        # validade: containment por AMOSTRA longa (alias dentro da frase)
        cts = [F11.acerta(a, e["aliases"])[1] for a in A]
        linhas.append({
            "qid": d["qid"], "ok": int(e["ct"]),
            "se": F.entropia_semantica(lab), "pts": m,
            "se_nuc": F.entropia_nucleo(P, p, ordens=8, seed=SEED),
            "we": prf["we"], "n_mundos": prf["n_mundos"],
            "dens_c": prf["dens_c"],
            "ct_amostras": float(np.mean(cts)),
        })
    D = pd.DataFrame(linhas)
    D.to_csv(E0.OUT / "sentence_intervention.csv", index=False)

    # ---- pareamento com o modo ENTIDADE (h2)
    H2 = pd.read_csv(E0.OUT / "triviaqa_worlds.csv",
                     float_precision="round_trip")   # leitura exata (2026-09-30)
    ent_j = [json.loads(x) for x in J_ENT.read_text().splitlines() if x.strip()]
    ent_j = [d for d in ent_j if len(d["amostras"]) >= 6]
    H2["qid"] = [d["qid"] for d in ent_j]
    ME = H2.set_index("qid").loc[D.qid]
    y = D.ok.to_numpy().astype(bool)
    rng = np.random.default_rng(SEED)

    E0.banner("(i) A CONFLACAO SOBE? (predicao: >= 40% contra 12,6%)")
    for nome, X in [("ENTIDADE (f11/h2)", ME), ("FRASE (h5)", D)]:
        multi = X.pts.to_numpy() > 1
        um = X.n_mundos.to_numpy() == 1
        confl = (multi & um).sum() / max(multi.sum(), 1)
        print(f"  {nome:20s} |P| {X.pts.mean():5.2f} · mundos "
              f"{X.n_mundos.mean():5.2f} · SE {X.se.mean():5.3f} · "
              f"WE {X.we.mean():5.3f} · conflacao {confl:6.1%}")

    E0.banner("(ii)/(iii) O CROSSOVER (AUROC; mesmo rotulo `ct` nos dois modos)")
    print(f"  acerto do rotulo: {y.mean():.1%} (n={len(y)})")
    print(f"  {'modo/metodo':34s} {'AUROC':>7s}")
    print("  " + "-" * 44)
    a_se_e = E0.auc(y, -ME.se.to_numpy(float))
    a_we_e = E0.auc(y, -ME.we.to_numpy(float))
    a_se_f = E0.auc(y, -D.se.to_numpy(float))
    a_we_f = E0.auc(y, -D.we.to_numpy(float))
    print(f"  {'ENTIDADE: SE (SOTA)':34s} {a_se_e:7.3f}")
    print(f"  {'ENTIDADE: WE':34s} {a_we_e:7.3f}")
    print(f"  {'FRASE:    SE (SOTA)':34s} {a_se_f:7.3f}")
    print(f"  {'FRASE:    WE (proposta)':34s} {a_we_f:7.3f}")
    print(f"  {'FRASE:    SE-nucleo':34s} "
          f"{E0.auc(y, -D.se_nuc.to_numpy(float)):7.3f}")
    print(f"  {'FRASE:    n_mundos':34s} "
          f"{E0.auc(y, -D.n_mundos.to_numpy(float)):7.3f}")

    def dauc(a, b, nb=5000):
        d_ = []
        for _ in range(nb):
            i = rng.integers(0, len(y), len(y))
            if len(np.unique(y[i])) < 2:
                continue
            d_.append(E0.auc(y[i], -a[i]) - E0.auc(y[i], -b[i]))
        d_ = np.array(d_)
        # estimativa PONTUAL da diferenca (ate 2026-09-30 imprimia a media das
        # reamostras, d_.mean(); o IC percentil nao muda)
        pt = E0.auc(y, -a) - E0.auc(y, -b)
        return pt, *np.percentile(d_, [2.5, 97.5])

    print()
    for nome, a, b in [
            ("FRASE: WE vs SE (o crossover, iii)", D.we, D.se),
            ("SE: FRASE vs ENTIDADE (a queda, ii)", D.se, ME.se),
            ("WE: FRASE vs ENTIDADE", D.we, ME.we),
            ("FRASE: WE vs SE-nucleo", D.we, D.se_nuc)]:
        mu, lo, hi = dauc(a.to_numpy(float), b.to_numpy(float))
        st = "  *" if (lo > 0 or hi < 0) else ""
        print(f"  {nome:38s} {mu:+.4f} [{lo:+.4f},{hi:+.4f}]{st}")

    E0.banner("VALIDADE — as frases longas ainda carregam a resposta?")
    print(f"  containment medio por amostra longa: {D.ct_amostras.mean():.1%}")
    print(f"  corr(ct_amostras, rotulo `ct`): "
          f"{np.corrcoef(D.ct_amostras, y.astype(float))[0,1]:+.3f}")
    print(f"\ngravado: {E0.OUT / 'sentence_intervention.csv'}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--gerar", action="store_true")
    args = ap.parse_args()
    if args.gerar:
        gerar()
    else:
        analisar()

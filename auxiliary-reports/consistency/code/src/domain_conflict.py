"""H3 — COLETA + ANÁLISE: a relação de conflito nos quatro domínios.

O QUE ESTÁ EM JOGO (predições registradas antes):

    P6  intervenção (f7): NENHUM invariante de mundos separa braço A de B —
        o limite da F8 é do paradigma de auto-consistência inteiro.
    P7  sumarização real: conjuntos majoritariamente COMPOSSÍVEIS (1 mundo,
        elaboração complementar) — a multiplicidade que a SE conta lá NÃO é
        conflito. O nulo embaralhado também ~1 mundo (não-relacionados não
        conflitam) — SE P7 falhar no nulo (conflito espúrio por template),
        reportar como está.

A LEI DE ESCOPO que este script mede (o número novo da teoria):

    taxa de conflação = fração dos conjuntos multi-classe cuja multiplicidade
    NÃO é conflito (1 mundo). A SE funciona onde a conflação é baixa (TriviaQA:
    12,6%, h2) e afunda onde é alta (predição: sumarização >> 50%).

Os scripts F guardaram só a coluna de entailment; este roda o NLI UMA vez
(3 classes) sobre os pares deduplicados de: f4 real (qwen), EMBARALHADO/0 e
MISTO/0 do f6 (reconstruídos com a MESMA seed), f4_llama, e os braços A/B do
f7. Cache em cache/h3_nli.npz. ~70k pares a ~57 pares/s ≈ 20 min. UM processo.

    python domain_conflict.py
"""
from __future__ import annotations

import json
import sys
import warnings
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import common as E0                # noqa: E402
import finite_space as F          # noqa: E402
import event_structure as H      # noqa: E402

warnings.filterwarnings("ignore")
J_QWEN = HERE.parent / "cache" / "f4_geracoes.jsonl"
J_LLAMA = HERE.parent / "cache" / "f4_llama.jsonl"
J_INTERV = HERE.parent / "cache" / "f7_intervencao.jsonl"
NPZ = HERE.parent / "cache" / "h3_nli.npz"
TAU = 0.50
TAU_CON = 0.50
SEED = 42
NREP = 2                      # igual ao f6 — necessário p/ reproduzir o rng


def conjuntos_f6() -> tuple[list[list[str]], dict[str, list[list[str]]]]:
    """Reconstrói EXATAMENTE os conjuntos do f6 (mesma seed, mesma ordem de
    sorteio). Devolve (frases_reais, {grupo: conjuntos de textos})."""
    itens = [json.loads(l) for l in J_QWEN.read_text().splitlines() if l.strip()]
    itens = [d for d in itens if len(d["amostras"]) >= 8]
    N = min(10, min(len(d["amostras"]) for d in itens))
    frases = [d["amostras"][:N] for d in itens]
    n = len(frases)
    rng = np.random.default_rng(SEED)
    plana = [(i, j) for i in range(n) for j in range(N)]

    grupos: dict[str, list[list[tuple]]] = {}
    grupos["REAL"] = [[(i, j) for j in range(N)] for i in range(n)]
    for r in range(NREP):
        emb = []
        for i in range(n):
            sel = [plana[k] for k in rng.choice(len(plana), N, replace=False)]
            emb.append(sel)
        grupos[f"EMBARALHADO/{r}"] = emb
    for r in range(NREP):
        mis = []
        for i in range(n):
            prop = [(i, j) for j in rng.choice(N, N // 2, replace=False)]
            alh = [plana[k] for k in rng.choice(len(plana), N - N // 2, replace=False)]
            mis.append(prop + alh)
        grupos[f"MISTO/{r}"] = mis
    usa = {"REAL": grupos["REAL"], "EMBARALHADO": grupos["EMBARALHADO/0"],
           "MISTO": grupos["MISTO/0"]}
    texto = {g: [[frases[a][b] for (a, b) in S] for S in G]
             for g, G in usa.items()}
    return frases, texto


def perfil_conjunto(A: list[str], VE: dict, VC: dict) -> dict:
    """Poset + conflito + mundos de um conjunto de textos, via caches de pares.

    CORRECAO (2026-09-30, revisao do relatorio auxiliar): os pares sao
    deduplicados POR TEXTO, e o par (s, s) de duas amostras identicas nunca
    entra no cache. A versao anterior lia esse par como acarretamento 0 e
    tratava duas amostras identicas como classes distintas (108 dos 259
    conjuntos REAL tem duplicatas). Agora texto identico acarreta texto
    identico, como na diagonal."""
    n = len(A)
    M = np.array([[1.0 if (i == j or A[i] == A[j]) else VE.get((A[i], A[j]), 0.0)
                   for j in range(n)] for i in range(n)]) >= TAU
    Cm = np.array([[0.0 if i == j else VC.get((A[i], A[j]), 0.0)
                    for j in range(n)] for i in range(n)]) >= TAU_CON
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
    prf.update({
        "pts": m, "se": F.entropia_semantica(lab),
        "se_nuc": F.entropia_nucleo(P, p, ordens=8, seed=SEED),
        "nuc": len(F.nucleo(P)), "alt": F.altura(P),
    })
    return prf


def main() -> None:
    import pandas as pd

    frases, gf6 = conjuntos_f6()
    itens_ll = [json.loads(l) for l in J_LLAMA.read_text().splitlines()
                if l.strip()]
    itens_ll = [d for d in itens_ll if len(d["amostras"]) >= 6]
    interv = [json.loads(l) for l in J_INTERV.read_text().splitlines()
              if l.strip()]

    conjuntos: list[tuple[str, list[str]]] = []
    for g, G in gf6.items():
        for S in G:
            conjuntos.append((g, S))
    for d in itens_ll:
        conjuntos.append(("LLAMA", d["amostras"]))
    for d in interv:
        conjuntos.append(("INTERV_A", d["com_evidencia"]))
        conjuntos.append(("INTERV_B", d["sem_evidencia"]))

    # ---- pares deduplicados (por texto, ordenados)
    need: set[tuple[str, str]] = set()
    for _, S in conjuntos:
        for a in S:
            for b in S:
                if a != b:
                    need.add((a, b))
    need_l = sorted(need)
    print(f"conjuntos: {len(conjuntos)} · pares NLI unicos: {len(need_l)}",
          flush=True)

    # coleta RETOMÁVEL: checkpoint a cada lote (rodar em 1º plano — background
    # no macOS leva QoS de eficiência, ~11x mais lento; armadilha #7 do handoff)
    ent = np.full(len(need_l), -1.0, np.float32)
    con = np.full(len(need_l), -1.0, np.float32)
    feito = 0
    if NPZ.exists():
        z = np.load(NPZ)
        if int(z["k"]) == len(need_l):
            ent, con = z["ent"].copy(), z["con"].copy()
            feito = int(z["feito"]) if "feito" in z else len(need_l)
            print(f"cache h3_nli.npz: {feito}/{len(need_l)} feitos", flush=True)
    if feito < len(need_l):
        import time
        import nli_runner
        nli_runner.NLI_BATCH = 64
        nli = nli_runner.make_nli()
        if nli is None:
            print("[ERRO] NLI indisponivel."); return
        LOTE = 4096
        t0 = time.time()
        for s in range(feito, len(need_l), LOTE):
            pr = nli(need_l[s:s + LOTE])
            ent[s:s + len(pr)] = pr[:, 0]
            con[s:s + len(pr)] = pr[:, 2]
            feito = s + len(pr)
            np.savez(NPZ, ent=ent, con=con, k=len(need_l), feito=feito)
            print(f"  NLI {feito}/{len(need_l)}  "
                  f"({feito / max(time.time() - t0, 1):.0f} pares/s)", flush=True)
    ent, con = ent, con
    VE = {par: float(v) for par, v in zip(need_l, ent)}
    VC = {par: float(v) for par, v in zip(need_l, con)}

    linhas = []
    for g, S in conjuntos:
        prf = perfil_conjunto(S, VE, VC)
        prf["grupo"] = g
        linhas.append(prf)
    D = pd.DataFrame(linhas)
    D.to_csv(E0.OUT / "domain_conflict.csv", index=False)

    # ------------------------------------------------- a tabela de escopo
    E0.banner("A LEI DE ESCOPO — estrutura de conflito por dominio")
    print(f"  {'dominio':16s} {'n':>4s} {'|P|':>5s} {'mundos':>7s} "
          f"{'>1 mundo':>9s} {'SE':>6s} {'WE':>6s} {'dens_c':>7s} "
          f"{'CONFLACAO':>10s}")
    print("  " + "-" * 78)
    ordem = ["REAL", "LLAMA", "MISTO", "EMBARALHADO", "INTERV_A", "INTERV_B"]
    for g in ordem:
        sub = D[D.grupo == g]
        if not len(sub):
            continue
        multi = sub.pts > 1
        confl = (multi & (sub.n_mundos == 1)).sum() / max(multi.sum(), 1)
        print(f"  {g:16s} {len(sub):4d} {sub.pts.mean():5.2f} "
              f"{sub.n_mundos.mean():7.2f} {(sub.n_mundos > 1).mean():9.1%} "
              f"{sub.se.mean():6.3f} {sub.we.mean():6.3f} "
              f"{sub.dens_c.mean():7.3f} {confl:10.1%}")
    print("\n  CONFLACAO = fracao dos conjuntos multi-classe com 1 mundo so")
    print("  (multiplicidade sem conflito: o que a SE conta e nao e discordancia).")
    print("  Referencia TriviaQA (h2): |P| 3.28 · mundos 2.63 · >1 mundo 53.6% ·")
    print("  conflacao 12.6% — e la a SE funciona (0.811).")

    E0.banner("DIAGNOSTICOS DO VERIFICADOR (fecho de heranca, autoconflito)")
    for g in ordem:
        sub = D[D.grupo == g]
        if not len(sub):
            continue
        print(f"  {g:16s} custo_fecho {sub.custo_fecho.mean():6.2%} · "
              f"autoconflito {sub.frac_autoc.mean():6.2%} · "
              f"b1(Ind)>0 {(sub.b1_ind > 0).mean():5.1%} · "
              f"b0_cons>1 {(sub.b0_cons > 1).mean():5.1%}")

    # ------------------------------------------------- P6: intervencao pareada
    E0.banner("P6 — INTERVENCAO PAREADA (predicao registrada: NULO)")
    A_ = D[D.grupo == "INTERV_A"].reset_index(drop=True)
    B_ = D[D.grupo == "INTERV_B"].reset_index(drop=True)
    rng = np.random.default_rng(SEED)
    print(f"  {'invariante':14s} {'A (evid.)':>10s} {'B (troc.)':>10s} "
          f"{'dif. pareada':>13s} {'IC95':>22s}")
    print("  " + "-" * 66)
    for c in ["n_mundos", "we", "dens_c", "pts", "se"]:
        d = A_[c].to_numpy(float) - B_[c].to_numpy(float)
        boots = [d[rng.integers(0, len(d), len(d))].mean() for _ in range(5000)]
        lo, hi = np.percentile(boots, [2.5, 97.5])
        st = "  *" if (lo > 0 or hi < 0) else ""
        print(f"  {c:14s} {A_[c].mean():10.3f} {B_[c].mean():10.3f} "
              f"{d.mean():+13.3f} [{lo:+.3f},{hi:+.3f}]{st}")
    print("\n  * = IC95 exclui zero (se aparecer, P6 foi FALSIFICADA — noticia)")

    # ------------------------------------------------- dose-resposta
    E0.banner("DOSE-RESPOSTA (real -> misto -> embaralhado)")
    for c in ["n_mundos", "we", "dens_c"]:
        v = [D[D.grupo == g][c].mean() for g in ["REAL", "MISTO", "EMBARALHADO"]]
        mono = "monotona" if (v[0] <= v[1] <= v[2] or v[0] >= v[1] >= v[2]) \
            else "NAO monotona"
        print(f"  {c:10s} REAL {v[0]:.3f} -> MISTO {v[1]:.3f} -> "
              f"EMB {v[2]:.3f}   ({mono})")
    print(f"\ngravado: {E0.OUT / 'domain_conflict.csv'}")


if __name__ == "__main__":
    main()

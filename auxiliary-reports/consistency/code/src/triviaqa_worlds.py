"""H2 — O PILOTO DECISIVO: mundos possíveis no TriviaQA, 100% offline do cache.

AS PREDIÇÕES ESTÃO REGISTRADAS EM predictions/registered_predictions.md (2026-08-03), ANTES desta
análise. Resumo do que está em jogo:

    P1  sanidade: reproduzir SE ~ 0,811 do f12 a partir do MESMO cache
    P2  conflitos vivem FORA da ordem; custo do fecho < 10%; autoconflito < 5%
    P3  pareado: delta(WE - SE) > delta(SE-nucleo - SE) = -0,0149; esperanca >= 0
    P4  estrutura > escalar: WE/|mundos| vs densidade de conflito (o controle
        da E22 — se empatar, a topologia da consistencia nao esta pagando)
    P5  exploratorio (n~28, ABAIXO da regra n=500): no estrato com escada, os
        errados tem mais mundos que os certos

Dados: cache/f11_triviaqa.jsonl (233 itens) + cache/f12_nli.npz (ent E con de
todos os pares ordenados). ZERO chamadas de modelo. Rótulo: alias matching, sem
rede neural (a mesma coluna `ct` do f12).

    python triviaqa_worlds.py
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
import triviaqa_collect as F11            # noqa: E402
import event_structure as H      # noqa: E402

warnings.filterwarnings("ignore")
JSONL = HERE.parent / "cache" / "f11_triviaqa.jsonl"
NPZ = HERE.parent / "cache" / "f12_nli.npz"
TAU = 0.50          # os MESMOS limiares do f12 — nada é tunado aqui
TAU_CON = 0.50
SEED = 42


def lgu(P: np.ndarray, p: np.ndarray, C: np.ndarray) -> tuple[float, float]:
    """Cópia exata do f12 (baseline LGU), para comparação no mesmo dado."""
    n = len(P)
    if n == 0:
        return 0.0, 0.0
    lt = P & ~np.eye(n, dtype=bool)
    raizes = [i for i in range(n) if not lt[:, i].any()]
    if not raizes:
        raizes = list(range(n))
    q = np.array([p[r] + p[lt[r]].sum() for r in raizes], float)
    q = q / max(q.sum(), 1e-12)
    q = q[q > 0]
    ige = float(-(q * np.log(q)).sum())
    k = len(raizes)
    if k > 1:
        sub = C[np.ix_(raizes, raizes)]
        ins = float((sub | sub.T).sum() - np.trace(sub | sub.T)) / (k * (k - 1))
    else:
        ins = 0.0
    return ige, (1.0 + ins) * ige


def main() -> None:
    import pandas as pd

    itens = [json.loads(l) for l in JSONL.read_text().splitlines() if l.strip()]
    itens = [d for d in itens if len(d["amostras"]) >= 6]
    z = np.load(NPZ)
    ent, con = z["ent"], z["con"]
    chaves = []
    for k, d in enumerate(itens):
        A = d["amostras"]
        for i in range(len(A)):
            for j in range(len(A)):
                if i != j:
                    chaves.append((k, i, j))
    assert len(chaves) == int(z["k"]), "cache nao corresponde aos itens"
    VE = {c: float(v) for c, v in zip(chaves, ent)}
    VC = {c: float(v) for c, v in zip(chaves, con)}

    linhas = []
    pares_par = []   # validade de construto: (conflito?, acerto misto?)
    for k, d in enumerate(itens):
        A = d["amostras"]
        n = len(A)
        M = np.array([[VE.get((k, i, j), 1.0 if i == j else 0.0)
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
        Cs = H.fechar_conflito(P, Cc)

        # P2: onde vivem os conflitos? (comparavel = u<=v ou v<=u no poset)
        n_cmp, n_inc = 0, 0
        Cnd = Cs.copy()
        np.fill_diagonal(Cnd, False)
        for a in range(m):
            for b in range(a + 1, m):
                if Cnd[a, b]:
                    if P[a, b] or P[b, a]:
                        n_cmp += 1
                    else:
                        n_inc += 1

        b0, b1 = F.betti(P)
        ige, lg = lgu(P, p, Cc)
        nuc = len(F.nucleo(P))
        linhas.append({
            "ok": int(d["ct"]), "em": int(d["em"]),
            "se": F.entropia_semantica(lab), "pts": m,
            "se_nuc": F.entropia_nucleo(P, p, ordens=8, seed=SEED),
            "nuc": nuc, "ige": ige, "lgu": lg,
            "alt": F.altura(P), "b1_poset": b1,
            "n_mundos": prf["n_mundos"], "we": prf["we"],
            "b0_cons": prf["b0_cons"], "b1_ind": prf["b1_ind"],
            "dens_c": prf["dens_c"], "custo_fecho": prf["custo_fecho"],
            "frac_autoc": prf["frac_autoc"],
            "conflito_teto": prf["conflito_teto"],
            "massa_viva": prf["massa_viva"],
            "conf_cmp": n_cmp, "conf_inc": n_inc,
        })

        # validade de construto (rotulo entra SO como validacao, nunca feature):
        # acerto POR AMOSTRA via alias matching, sem rede neural
        cts = [F11.acerta(a, d["aliases"])[1] for a in A]
        for i in range(n):
            for j in range(i + 1, n):
                confl = bool(Cm[i, j] or Cm[j, i])
                misto = int(cts[i] != cts[j])
                pares_par.append((confl, misto))

    D = pd.DataFrame(linhas)
    D.to_csv(E0.OUT / "triviaqa_worlds.csv", index=False)
    y = D.ok.to_numpy().astype(bool)
    rng = np.random.default_rng(SEED)

    E0.banner("P1 — SANIDADE: reproduz o f12 a partir do mesmo cache?")
    a_se = E0.auc(y, -D.se.to_numpy(float))
    a_nuc = E0.auc(y, -D.se_nuc.to_numpy(float))
    a_lgu = E0.auc(y, -D.lgu.to_numpy(float))
    print(f"  itens {len(D)} · acerto {y.mean():.1%}")
    print(f"  AUROC SE ........ {a_se:.3f}   (f12: 0.811)")
    print(f"  AUROC SE-nucleo . {a_nuc:.3f}   (f12: 0.796)")
    print(f"  AUROC LGU ....... {a_lgu:.3f}   (f12: 0.805)")

    E0.banner("P2 — ESTRUTURA DO CONFLITO NESTE DOMINIO")
    tem_c = (D.dens_c > 0)
    print(f"  itens com ALGUM conflito ......... {tem_c.mean():6.1%}")
    print(f"  mundos por item (media) .......... {D.n_mundos.mean():.2f}")
    print(f"  itens com > 1 mundo .............. {(D.n_mundos > 1).mean():6.1%}")
    print(f"  itens com b0_cons > 1 ............ {(D.b0_cons > 1).mean():6.1%}")
    print(f"  itens com b1(Ind) > 0 ............ {(D.b1_ind > 0).mean():6.1%}")
    tc = int(D.conf_cmp.sum() + D.conf_inc.sum())
    print(f"  arestas de conflito: {tc}  —  entre INCOMPARAVEIS "
          f"{D.conf_inc.sum() / max(tc, 1):6.1%}  (P2 preve >> 50%)")
    print(f"  custo do fecho de heranca ........ {D.custo_fecho.mean():6.2%}"
          f"   (P2 preve < 10%)")
    print(f"  taxa de autoconflito ............. {D.frac_autoc.mean():6.2%}"
          f"   (P2 preve < 5%)")
    print(f"  conflito sob teto comum (Λ) ...... "
          f"{(D.conflito_teto > 0).mean():6.1%} dos itens")

    E0.banner("P3/P4 — O CONFRONTO (AUROC; incerteza baixa -> resposta certa)")
    metodos = [("se", "entropia semantica (SOTA)"),
               ("se_nuc", "SE-nucleo (artigo 1)"),
               ("lgu", "LGU completo"),
               ("we", "ENTROPIA DE MUNDOS (proposta)"),
               ("n_mundos", "numero de mundos"),
               ("b0_cons", "b0 da consistencia"),
               ("dens_c", "densidade de conflito (escalar, controle)"),
               ("pts", "numero de classes")]
    print(f"  {'metodo':42s} {'AUROC':>7s}")
    print("  " + "-" * 52)
    for c, nome in metodos:
        print(f"  {nome:42s} {E0.auc(y, -D[c].to_numpy(float)):7.3f}")

    def dauc(a, b, nb=5000):
        d = []
        for _ in range(nb):
            i = rng.integers(0, len(y), len(y))
            if len(np.unique(y[i])) < 2:
                continue
            d.append(E0.auc(y[i], -a[i]) - E0.auc(y[i], -b[i]))
        d = np.array(d)
        # estimativa PONTUAL da diferenca (ate 2026-09-30 imprimia a media das
        # reamostras, d.mean(); o IC percentil nao muda)
        pt = E0.auc(y, -a) - E0.auc(y, -b)
        return pt, *np.percentile(d, [2.5, 97.5])

    print()
    comp = [("WE         vs  SE (P3 primario)", "we", "se"),
            ("SE-nucleo  vs  SE (ancora artigo 1)", "se_nuc", "se"),
            ("WE         vs  SE-nucleo", "we", "se_nuc"),
            ("WE         vs  dens_c (P4 primario)", "we", "dens_c"),
            ("n_mundos   vs  dens_c (P4)", "n_mundos", "dens_c"),
            ("WE         vs  LGU", "we", "lgu")]
    print(f"  {'comparacao pareada':38s} {'delta AUROC':>12s} {'IC95':>22s}")
    print("  " + "-" * 76)
    for nome, ca, cb in comp:
        mu, lo, hi = dauc(D[ca].to_numpy(float), D[cb].to_numpy(float))
        st = "  *" if (lo > 0 or hi < 0) else ""
        print(f"  {nome:38s} {mu:+12.4f} [{lo:+.4f},{hi:+.4f}]{st}")
    print("\n  * = IC95 exclui zero")

    E0.banner("P5 — EXPLORATORIO (estrato com escada; n PEQUENO, so direcao)")
    esc = (D.nuc < D.pts).to_numpy()
    for nome, msk in [("COM escada", esc), ("SEM escada", ~esc)]:
        if msk.sum() < 5:
            continue
        sub = D[msk]
        ys = y[msk]
        print(f"  {nome} (n={msk.sum()}): acerto {ys.mean():.1%} · "
              f"mundos medios {sub.n_mundos.mean():.2f} · "
              f">1 mundo: {(sub.n_mundos > 1).mean():.1%}")
        if len(np.unique(ys)) == 2:
            print(f"      AUROC no estrato — SE {E0.auc(ys, -sub.se.to_numpy(float)):.3f}"
                  f" · WE {E0.auc(ys, -sub.we.to_numpy(float)):.3f}"
                  f" · mundos {E0.auc(ys, -sub.n_mundos.to_numpy(float)):.3f}")
    cert = y
    print(f"\n  mundos medios: certos {D.n_mundos[cert].mean():.2f} "
          f"vs errados {D.n_mundos[~cert].mean():.2f}")

    E0.banner("VALIDADE DE CONSTRUTO (rotulo so como validacao, sem rede neural)")
    pares = np.array(pares_par, dtype=int)
    c1 = pares[pares[:, 0] == 1]
    c0 = pares[pares[:, 0] == 0]
    print("  pares de amostras com acerto MISTO (uma bate o alias, outra nao):")
    print(f"    entre pares em CONFLITO ......... {c1[:, 1].mean():6.1%}"
          f"   (n={len(c1)})")
    print(f"    entre pares COMPATIVEIS ......... {c0[:, 1].mean():6.1%}"
          f"   (n={len(c0)})")
    # IC bootstrap da diferenca (reamostrando pares)
    dd = []
    for _ in range(2000):
        i1 = rng.integers(0, len(c1), len(c1))
        i0 = rng.integers(0, len(c0), len(c0))
        dd.append(c1[i1, 1].mean() - c0[i0, 1].mean())
    lo, hi = np.percentile(dd, [2.5, 97.5])
    print(f"    diferenca: {c1[:, 1].mean() - c0[:, 1].mean():+.3f} "
          f"[{lo:+.3f}, {hi:+.3f}]")
    print(f"\ngravado: {E0.OUT / 'triviaqa_worlds.csv'}")


if __name__ == "__main__":
    main()

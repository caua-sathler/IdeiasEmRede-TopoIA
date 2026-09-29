"""I0 — VIABILIDADE ESTRUTURAL, antes de qualquer teoria.

A disciplina deste projeto (fase H, turno 2) é: olhar o que já está em disco e
medir se o OBJETO EXISTE antes de investir. Quatro impossibilidades foram
descobertas tarde demais porque essa checagem não foi feita.

A pergunta: a relação bipartida opiniões × oradores DE UMA AUDIÊNCIA tem
estrutura de dimensão 1? Isto é:

    dim H_1(G)  =  |E| - |V| + b_0        (posto do ciclo do grafo bipartido)
    dim H_1(D_O(R))                        (complexo de Dowker do lado opiniões)

Se ambos forem ~0, a teoria homológica morre aqui (5ª impossibilidade, por
esparsidade — o mecanismo da F3). Se dim H_1 for da ordem de dezenas, o espaço
existe e a construção é viável.

Também mede o que decide se a estrutura CONJUNTA vale a pena:
    - opiniões por audiência e por orador (há multiplicidade para emparelhar?)
    - concentração: quantos oradores sustentam cada opinião acima de τ?

    python i0_viabilidade.py
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import comum as E0            # noqa: E402
import dados as R           # noqa: E402
import h6_orador as H6            # noqa: E402

warnings.filterwarnings("ignore")


def betti_grafo(E: np.ndarray) -> tuple[int, int]:
    """(b0, b1) de um grafo bipartido dado pela matriz de incidência booleana
    E[o, a]. b1 = |arestas| - |vertices| + b0 (posto do espaco de ciclos)."""
    q, p = E.shape
    viz_o = [np.where(E[i])[0] for i in range(q)]
    viz_a = [np.where(E[:, j])[0] for j in range(p)]
    vis_o, vis_a = np.zeros(q, bool), np.zeros(p, bool)
    b0 = 0
    for i in range(q):
        if vis_o[i] or not len(viz_o[i]):
            continue
        b0 += 1
        pil = [("o", i)]
        vis_o[i] = True
        while pil:
            t, v = pil.pop()
            if t == "o":
                for a in viz_o[v]:
                    if not vis_a[a]:
                        vis_a[a] = True
                        pil.append(("a", a))
            else:
                for o in viz_a[v]:
                    if not vis_o[o]:
                        vis_o[o] = True
                        pil.append(("o", o))
    nv = int(vis_o.sum() + vis_a.sum())
    ne = int(E.sum())
    return b0, ne - nv + b0


def b1_dowker(E: np.ndarray) -> int:
    """b1 do complexo de Dowker D_O(R): vertices = opinioes com suporte;
    simplexos = conjuntos de opinioes com um orador comum. Como e um complexo
    de bandeira? NAO — e o nervo de {R(a)}_a. Calculamos b1 pelo 2-esqueleto:
    b1 = dim ker d1 - posto d2, com d1 sobre arestas (pares com orador comum) e
    d2 sobre triangulos (triplas com orador comum)."""
    q, p = E.shape
    viv = np.where(E.sum(1) > 0)[0]
    if len(viv) < 3:
        return 0
    idx = {o: k for k, o in enumerate(viv)}
    Es = E[viv]
    n = len(viv)
    # arestas: par (i,j) com algum orador em comum
    ares = [(i, j) for i in range(n) for j in range(i + 1, n)
            if np.any(Es[i] & Es[j])]
    if not ares:
        return 0
    ai = {e: k for k, e in enumerate(ares)}
    # triangulos: tripla com algum orador em comum
    tris = [(i, j, k) for i in range(n) for j in range(i + 1, n)
            for k in range(j + 1, n) if np.any(Es[i] & Es[j] & Es[k])]
    d1 = np.zeros((n, len(ares)))
    for (i, j), c in ai.items():
        d1[i, c], d1[j, c] = -1.0, 1.0
    r1 = np.linalg.matrix_rank(d1) if len(ares) else 0
    if tris:
        d2 = np.zeros((len(ares), len(tris)))
        for c, (i, j, k) in enumerate(tris):
            d2[ai[(i, j)], c] = 1.0
            d2[ai[(i, k)], c] = -1.0
            d2[ai[(j, k)], c] = 1.0
        r2 = np.linalg.matrix_rank(d2)
    else:
        r2 = 0
    return int(len(ares) - r1 - r2)


def main() -> None:
    import pandas as pd

    TAUS = [0.45, 0.50, 0.55, 0.60]
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
        spk = H6.speakers(fr)
        cands = sorted({s for s in spk if s})
        if len(cands) < 2:
            continue
        S = ge @ Tm.T
        idx = {c: np.where(spk == c)[0] for c in cands}
        # matriz de suporte opiniao x orador (max sobre os turnos do orador)
        M = np.array([[float(S[i, idx[c]].max()) for c in cands]
                      for i in range(len(g))])
        # so as opinioes com rotulo humano
        rot = np.array([not pd.isna(v) for v in g.alucinacao_manual])
        M = M[rot]
        if M.shape[0] < 3:
            continue
        # atribuicao
        atr = [H6.match_gold(q_, cands) for q_ in g.envolvido[rot]] \
            if "envolvido" in g else [None] * M.shape[0]
        row = {"ref": r, "n_op": M.shape[0], "n_spk": len(cands),
               "n_atr": sum(a is not None for a in atr),
               "n_spk_atr": len({a for a in atr if a})}
        for t in TAUS:
            E = M >= t
            b0, b1 = betti_grafo(E)
            row[f"gr_b1_{t}"] = b1
            row[f"deg_{t}"] = float(E.sum(1).mean())
            row[f"iso_{t}"] = float((E.sum(1) == 0).mean())
            if t == 0.50:
                row["dw_b1"] = b1_dowker(E)
        linhas.append(row)
        if (ri + 1) % 50 == 0:
            print(f"  {ri+1}/{len(refs)} · {len(linhas)} audiencias", flush=True)

    D = pd.DataFrame(linhas)
    D.to_csv(E0.OUT / "i0_viabilidade.csv", index=False)

    E0.banner("TAMANHO DO OBJETO CONJUNTO (por audiencia)")
    print(f"  audiencias utilizaveis .............. {len(D)}")
    for c, nome in [("n_op", "opinioes com rotulo"),
                    ("n_spk", "oradores com turno"),
                    ("n_atr", "opinioes com orador casado"),
                    ("n_spk_atr", "oradores distintos atribuidos")]:
        print(f"  {nome:34s} mediana {D[c].median():5.1f} · "
              f"media {D[c].mean():5.1f} · min {D[c].min():.0f} · "
              f"max {D[c].max():.0f}")
    mult = D.n_atr / D.n_spk_atr.clip(lower=1)
    print(f"  {'opinioes por orador atribuido':34s} mediana {mult.median():5.2f}"
          f" · max {mult.max():.1f}   <- multiplicidade p/ emparelhamento")

    E0.banner("O ESPACO DE CICLOS EXISTE? (a 5a impossibilidade seria b1 ~ 0)")
    print(f"  {'tau':>5s} {'grau medio':>11s} {'opin. isoladas':>15s} "
          f"{'b1(grafo) med':>15s} {'b1>0':>7s}")
    print("  " + "-" * 58)
    for t in TAUS:
        b = D[f"gr_b1_{t}"]
        print(f"  {t:5.2f} {D[f'deg_{t}'].mean():11.2f} "
              f"{D[f'iso_{t}'].mean():14.1%} {b.median():15.1f} "
              f"{(b > 0).mean():6.1%}")
    print()
    dw = D["dw_b1"]
    print(f"  b1 do complexo de DOWKER (tau=0,50): mediana {dw.median():.1f} · "
          f"media {dw.mean():.2f} · b1>0 em {(dw > 0).mean():.1%} das audiencias")
    print(f"\ngravado: {E0.OUT / 'i0_viabilidade.csv'}")


if __name__ == "__main__":
    main()

"""J0 — VIABILIDADE das fontes EXÓGENAS temporais, antes de qualquer teoria.

O diagnóstico da fase I: os invariantes conjuntos eram funcionais da MESMA matriz M
que a família por-opinião já resume — acoplamento novo, informação nenhuma. Para
bater o comitê é preciso uma FONTE EXÓGENA.

Três candidatas, nenhuma jamais tocada neste projeto, todas de custo zero:

  (A) A ORDEM DO RESUMO.  O resumo é uma SEQUÊNCIA o_1..o_q; a transcrição é uma
      SEQUÊNCIA s_1..s_m. Um resumo fiel é aproximadamente MONÓTONO: se o_i vem
      antes de o_j, o conteúdo que sustenta o_i tende a vir antes na transcrição.
      Uma opinião ALUCINADA não tem posição verdadeira — cai em qualquer lugar e
      quebra a monotonicidade localmente.
      Por Alexandrov, um mapa entre ordens totais finitas é CONTÍNUO sse é
      monótono: alucinação é literalmente uma DESCONTINUIDADE. É o teorema da
      fase F com a ordem EXÓGENA (tempo) no lugar da endógena (acarretamento).

  (B) LOCALIZAÇÃO EM TURNO.  `cos_s` toma o max sobre TODAS as frases do orador,
      que vêm de k turnos espalhados. Uma opinião realmente dita é um pico
      LOCALIZADO em um turno; uma sintetizada espalha-se por vários.

  (C) DISPERSÃO TEMPORAL do suporte dentro dos turnos do orador.

Este script só mede se o objeto EXISTE. Se a ordem do resumo não correlacionar com
a posição do suporte, (A) morre aqui e não se escreve teoria nenhuma.

    python j0_viabilidade_tempo.py
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
SEED = 42


def kendall(a: np.ndarray, b: np.ndarray) -> float:
    n = len(a)
    if n < 2:
        return np.nan
    c = d = 0
    for i in range(n):
        for j in range(i + 1, n):
            s = np.sign(a[i] - a[j]) * np.sign(b[i] - b[j])
            if s > 0:
                c += 1
            elif s < 0:
                d += 1
    return (c - d) / max(c + d, 1)


def main() -> None:
    import pandas as pd
    rng = np.random.default_rng(SEED)
    linhas, poraud = [], []
    for ri, r in enumerate(R.refs_ok()):
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
        # blocos de TURNO: trechos maximais contíguos com o mesmo orador
        turno = np.zeros(len(spk), int)
        t = 0
        for i in range(1, len(spk)):
            if spk[i] != spk[i - 1]:
                t += 1
            turno[i] = t
        rot = np.array([not pd.isna(v) for v in g.alucinacao_manual])
        gi = np.where(rot)[0]
        if len(gi) < 4:
            continue
        quem = (g.envolvido.to_numpy()[gi] if "envolvido" in g
                else np.array([None] * len(gi)))
        atr = [H6.match_gold(q_, cands) for q_ in quem]
        # posição do melhor suporte: global e restrita aos turnos do orador
        pos_g = np.array([int(np.argmax(S[i])) for i in gi], float)
        pos_s = np.full(len(gi), np.nan)
        disp = np.full(len(gi), np.nan)      # dispersão do top-5 entre turnos
        n_tur = np.full(len(gi), np.nan)
        for k, i in enumerate(gi):
            if atr[k] is None:
                continue
            js = idx[atr[k]]
            pos_s[k] = float(js[int(np.argmax(S[i, js]))])
            top = js[np.argsort(-S[i, js])[:5]]
            n_tur[k] = len(np.unique(turno[top]))
            disp[k] = float(np.std(top) / max(len(Tm), 1))
        ordem = np.arange(len(gi), dtype=float)
        ok = ~np.isnan(pos_s)
        tau_g = kendall(ordem, pos_g)
        tau_s = kendall(ordem[ok], pos_s[ok]) if ok.sum() >= 3 else np.nan
        tau_p = kendall(ordem, pos_g[rng.permutation(len(gi))])
        poraud.append({"ref": r, "n": len(gi), "tau_g": tau_g,
                       "tau_s": tau_s, "tau_perm": tau_p})
        # deslocamento por opinião: posto na ordem do resumo vs posto no tempo
        pr_o = np.argsort(np.argsort(ordem)) / max(len(gi) - 1, 1)
        pr_t = np.argsort(np.argsort(pos_g)) / max(len(gi) - 1, 1)
        for k, i in enumerate(gi):
            linhas.append({
                "ref": r, "hall": int(bool(g.alucinacao_manual.iloc[i])),
                "desloc": abs(pr_o[k] - pr_t[k]),
                "n_tur": n_tur[k], "disp": disp[k],
                "sem_turno": int(atr[k] is None)})
        if (ri + 1) % 50 == 0:
            print(f"  {ri+1}/206 · {len(linhas)} opinioes", flush=True)

    D = pd.DataFrame(linhas)
    A = pd.DataFrame(poraud)
    D.to_csv(E0.OUT / "j0_tempo.csv", index=False)
    y = D.hall.to_numpy().astype(bool)

    E0.banner("(A) A ORDEM DO RESUMO SEGUE O TEMPO DA TRANSCRICAO?")
    print(f"  audiencias: {len(A)} · opinioes: {len(D)}")
    print(f"  Kendall tau (ordem do resumo x posicao do suporte GLOBAL):")
    print(f"     media {A.tau_g.mean():+.4f} · mediana {A.tau_g.median():+.4f} · "
          f"tau>0 em {(A.tau_g > 0).mean():.1%} das audiencias")
    print(f"  Kendall tau (restrito aos TURNOS DO ORADOR):")
    print(f"     media {A.tau_s.mean():+.4f} · mediana {A.tau_s.median():+.4f}")
    print(f"  CONTROLE: ordem do resumo PERMUTADA:")
    print(f"     media {A.tau_perm.mean():+.4f}   <- tem de ser ~0")

    E0.banner("(B)/(C) LOCALIZACAO E DISPERSAO EM TURNO")
    M = D.sem_turno == 0
    print(f"  n_tur (turnos distintos no top-5): media {D[M].n_tur.mean():.2f} · "
          f"=1 em {(D[M].n_tur == 1).mean():.1%}")
    print(f"  alucinada:     n_tur {D[M & (D.hall == 1)].n_tur.mean():.2f} · "
          f"disp {D[M & (D.hall == 1)].disp.mean():.4f}")
    print(f"  nao-alucinada: n_tur {D[M & (D.hall == 0)].n_tur.mean():.2f} · "
          f"disp {D[M & (D.hall == 0)].disp.mean():.4f}")

    E0.banner("O SINAL ISOLADO (AUROC contra o rotulo humano)")
    for c, sg, nome in [("desloc", +1, "deslocamento de ordem (descontinuidade)"),
                        ("n_tur", +1, "nº de turnos distintos no top-5"),
                        ("disp", +1, "dispersao temporal do suporte")]:
        v = D[c].fillna(D[c].median()).to_numpy(float) * sg
        print(f"  {nome:42s} {E0.auc(y, v):7.4f}")
    ym = y[M.to_numpy()]
    sm = D[M]
    for c, sg, nome in [("n_tur", +1, "n_tur (so casados)"),
                        ("disp", +1, "disp  (so casados)")]:
        print(f"  {nome:42s} {E0.auc(ym, sm[c].to_numpy(float)*sg):7.4f}")
    print(f"\ngravado: {E0.OUT / 'j0_tempo.csv'}")


if __name__ == "__main__":
    main()

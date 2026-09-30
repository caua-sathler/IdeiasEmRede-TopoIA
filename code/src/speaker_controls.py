"""H6b — OS CONTROLES do sinal condicionado ao orador (antes de qualquer alegação).

TRES AMEACAS, cada uma com teste:

  (1) TAMANHO: cos_s é max sobre menos frases; orador que fala pouco da cos_s
      baixo por aritmética. Teste: AUROC de n_frases_spk sozinho, e correlação.
  (2) IDENTIDADE: o controle decisivo — cosseno nos turnos de um orador
      ALEATÓRIO (o mais próximo em nº de frases, excluindo o atribuído). Se
      cos_rand detectar igual, o sinal é tamanho/estrutura, não QUEM FALOU.
  (3) INFERÊNCIA: bootstrap AGRUPADO por audiência (o h6 usou i.i.d. por linha).

E O TESTE DA COMPETIÇÃO: o sinal soma ao MELHOR juiz LLM (juiz_p2_gpt4omini,
0,8501)? Ensemble por soma de postos, pareado, agrupado por audiência.

    python speaker_controls.py
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import common as E0            # noqa: E402
import dataset_readers as R           # noqa: E402
import speaker_incidence as H6            # noqa: E402

warnings.filterwarnings("ignore")
SEED = 42


def main() -> None:
    import pandas as pd

    rng = np.random.default_rng(SEED)
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
        idx_spk = {c: np.where(spk == c)[0] for c in cands}
        S = ge @ Tm.T
        for i in range(len(g)):
            lab = g.alucinacao_manual.iloc[i]
            if pd.isna(lab):
                continue
            quem = g.envolvido.iloc[i] if "envolvido" in g else None
            m = H6.match_gold(quem, cands) if quem is not None else None
            if m is None:
                continue
            js = idx_spk[m]
            outros = [c for c in cands if c != m]
            if not outros:
                continue
            # controle de IDENTIDADE pareado em tamanho: o outro orador com
            # nº de frases mais próximo (empate: sorteio com seed)
            tam = np.array([len(idx_spk[c]) for c in outros])
            d = np.abs(tam - len(js))
            cand_min = [outros[k] for k in np.where(d == d.min())[0]]
            alvo = cand_min[rng.integers(0, len(cand_min))]
            jr = idx_spk[alvo]
            linhas.append({
                "ref": r, "hall": int(bool(lab)),
                "cos_g": float(S[i].max()),
                "cos_s": float(S[i, js].max()),
                "cos_rand": float(S[i, jr].max()),
                "n_spk": int(len(js)), "n_rand": int(len(jr)),
                "juiz": (int(bool(g["juiz_p2_gpt4omini"].iloc[i]))
                         if "juiz_p2_gpt4omini" in g
                         and not pd.isna(g["juiz_p2_gpt4omini"].iloc[i])
                         else np.nan),
            })
        if (ri + 1) % 60 == 0:
            print(f"  {ri+1}/{len(refs)}", flush=True)

    D = pd.DataFrame(linhas)
    D.to_csv(E0.OUT / "speaker_controls.csv", index=False)
    y = D.hall.to_numpy().astype(bool)
    grupos = D.ref.to_numpy()
    print(f"\nopinioes: {len(D)} · alucinadas: {int(y.sum())} ({y.mean():.1%})")

    def dauc_cluster(a, b, nb=3000):
        """Bootstrap PAREADO agrupado por audiencia."""
        uref = np.unique(grupos)
        out = []
        for _ in range(nb):
            sel = uref[rng.integers(0, len(uref), len(uref))]
            idx = np.concatenate([np.where(grupos == u)[0] for u in sel])
            if len(np.unique(y[idx])) < 2:
                continue
            out.append(E0.auc(y[idx], a[idx]) - E0.auc(y[idx], b[idx]))
        out = np.array(out)
        return out.mean(), *np.percentile(out, [2.5, 97.5])

    E0.banner("(1) TAMANHO — o confundidor aritmético")
    print(f"  AUROC n_frases_spk sozinho ...... "
          f"{E0.auc(y, -D.n_spk.to_numpy(float)):.4f}")
    print(f"  corr(cos_s, log n_spk) .......... "
          f"{np.corrcoef(D.cos_s, np.log1p(D.n_spk))[0,1]:+.3f}")
    print(f"  tamanho casado no controle: n_spk {D.n_spk.median():.0f} "
          f"vs n_rand {D.n_rand.median():.0f} (medianas)")

    E0.banner("(2) IDENTIDADE — o controle decisivo")
    a_s = E0.auc(y, -D.cos_s.to_numpy(float))
    a_r = E0.auc(y, -D.cos_rand.to_numpy(float))
    a_g = E0.auc(y, -D.cos_g.to_numpy(float))
    print(f"  cos no ORADOR ATRIBUIDO ......... {a_s:.4f}")
    print(f"  cos em ORADOR ALEATORIO (casado)  {a_r:.4f}")
    print(f"  cos global (baseline) ........... {a_g:.4f}")
    mu, lo, hi = dauc_cluster(-D.cos_s.to_numpy(float),
                              -D.cos_rand.to_numpy(float))
    st = "  *" if lo > 0 else ""
    print(f"  pareado atribuido vs aleatorio: {mu:+.4f} [{lo:+.4f},{hi:+.4f}]{st}")

    E0.banner("(3) INFERENCIA AGRUPADA POR AUDIENCIA (o numero honesto)")
    mu, lo, hi = dauc_cluster(-D.cos_s.to_numpy(float),
                              -D.cos_g.to_numpy(float))
    st = "  *" if lo > 0 else ""
    print(f"  cos_orador vs cos_global: {mu:+.4f} [{lo:+.4f},{hi:+.4f}]{st}")

    E0.banner("O TESTE DA COMPETICAO — soma ao MELHOR juiz LLM?")
    import scipy.stats as sst
    J = D.juiz.notna().to_numpy()
    yj = y[J]
    gj = grupos[J]
    juiz = D.juiz[J].to_numpy(float)
    cos_s = -D.cos_s[J].to_numpy(float)
    a_j = E0.auc(yj, juiz)
    ens = sst.rankdata(juiz) + sst.rankdata(cos_s)
    a_e = E0.auc(yj, ens)

    def dauc_cl_j(a, b, nb=3000):
        uref = np.unique(gj)
        out = []
        for _ in range(nb):
            sel = uref[rng.integers(0, len(uref), len(uref))]
            idx = np.concatenate([np.where(gj == u)[0] for u in sel])
            if len(np.unique(yj[idx])) < 2:
                continue
            out.append(E0.auc(yj[idx], a[idx]) - E0.auc(yj[idx], b[idx]))
        out = np.array(out)
        return out.mean(), *np.percentile(out, [2.5, 97.5])

    print(f"  juiz_p2_gpt4omini sozinho ....... {a_j:.4f}  (n={int(J.sum())})")
    print(f"  juiz + cos_orador (postos) ...... {a_e:.4f}")
    mu, lo, hi = dauc_cl_j(ens, juiz)
    st = "  *" if lo > 0 else ""
    print(f"  pareado ensemble vs juiz: {mu:+.4f} [{lo:+.4f},{hi:+.4f}]{st}")
    print(f"\ngravado: {E0.OUT / 'speaker_controls.csv'}")


if __name__ == "__main__":
    main()

"""H4 — A INSTANCIAÇÃO NA TAREFA DO DESAFIO: suporte incoerente (P8, exploratório).

A PERGUNTA. Para uma opinião `o` e o cone de suporte Û(o) (frases da transcrição
que a acarretam), a fase F só olhou o TAMANHO e a ordem do cone. A relação de
conflito acrescenta duas perguntas que nada no pipeline via:

    1. SUPORTE INCOERENTE — as frases que sustentam `o` conflitam ENTRE SI?
       (o cone atravessa >= 2 mundos: `o` é uma síntese de vozes que não podem
       ser todas verdadeiras — numa audiência, tipicamente lados opostos do
       debate). Invisível a qualquer agregação por par (frase, o).
    2. CONTRADIÇÃO ATIVA — alguma frase recuperada CONTRADIZ `o`?
       (a direção de polaridade que a tricotomia da fase F não computava).

PREDIÇÃO REGISTRADA (h0, P8): taxa mensurável; concentração de alucinação nos
flags. EXPLORATÓRIO: 93 positivos em 837 — abaixo da regra n~500; nenhum número
daqui vira manchete sem réplica.

Custo: ~30k pares de NLI (contradição o<->top-14 + conflito dentro do cone
τ=0,20), cache em cache/h4_nli.npz. Rótulo: `alucinacao_manual` (humano).

    python incoherent_support.py
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import common as E0                # noqa: E402
import event_structure as H      # noqa: E402

warnings.filterwarnings("ignore")
OPI = E0.DATA /  "opinions_data"
EMB = E0.DATA /  "MPNET_embeddings_phrasal_data"
OEM = E0.DATA /  "MPNET_opinion_embeddings"
PHR = E0.DATA /  "phrasal_data"
F2NPZ = HERE.parent / "cache" / "f2_matrizes.npz"
NPZ = HERE.parent / "cache" / "h4_nli.npz"
K = 14
CHARS = 280
TAU_BASE = 0.20          # cone mais largo analisado (pares computados aqui)
TAU_CON = 0.50
SEED = 42
u = lambda X: X / (np.linalg.norm(X, axis=1, keepdims=True) + 1e-12)


def carrega_textos(refs: list[str]) -> list[dict]:
    """Refaz a recuperação DETERMINÍSTICA do f2 (mesmos argsort) para obter os
    TEXTOS das top-K frases de cada opinião, alinhados com opinions_meta.csv.
    `refs`: só as audiências que o f2 processou (o f2 foi interrompido no meio
    da coleta incremental — 837 de 4238 opiniões)."""
    import pandas as pd
    linhas = []
    for ref in refs:
        n = ref.split("_")[1]
        fo = OPI / ref / f"opinions_{n}.csv"
        fe = OEM / ref / f"opinion_embeddings_{n}.npy"
        ft = EMB / ref / f"transcript_embeddings_{n}.npy"
        fp = PHR / ref / f"phrases_{n}.csv"
        if not all(p.exists() for p in (fo, fe, ft, fp)):
            continue
        df = pd.read_csv(fo)
        O, T = u(np.load(fe).astype(np.float32)), u(np.load(ft).astype(np.float32))
        txt = pd.read_csv(fp)["transcript"].astype(str).tolist()
        if len(df) != len(O) or len(T) < K or len(txt) < len(T):
            continue
        S = O @ T.T
        for i in range(len(df)):
            sel = np.argsort(-S[i])[:K]
            linhas.append({
                "ref": ref, "op": i,
                "hall": bool(df.alucinacao_manual.iloc[i]),
                "o": str(df.opiniao.iloc[i])[:CHARS],
                "frases": [txt[c][:CHARS] for c in sel],
            })
    return linhas


def main() -> None:
    import pandas as pd

    meta = pd.read_csv(E0.OUT / "opinions_meta.csv")
    itens = carrega_textos(sorted(meta.ref.unique()))
    assert len(itens) == len(meta), (len(itens), len(meta))
    for a, b in zip(itens[:50], meta.itertuples()):
        assert a["ref"] == b.ref and a["op"] == b.op and a["hall"] == b.hall
    z = np.load(F2NPZ)
    EE, EO, OE, SI = z["ee"], z["eo"], z["oe"], z["sim"]
    assert len(EE) == len(itens)
    print(f"opinioes: {len(itens)} · alucinadas: "
          f"{sum(d['hall'] for d in itens)}", flush=True)

    # ---- pares novos: contradicao o<->top-14 (ambas direcoes) + pares do cone
    pares: list[tuple[str, str]] = []
    idx_oe, idx_eo, idx_cone = [], [], []
    for t, d in enumerate(itens):
        for j, f in enumerate(d["frases"]):
            idx_oe.append((t, j, len(pares))); pares.append((d["o"], f))
            idx_eo.append((t, j, len(pares))); pares.append((f, d["o"]))
        viz = [j for j in range(K) if EO[t, j] >= TAU_BASE]
        for a_ in range(len(viz)):
            for b_ in range(len(viz)):
                if a_ != b_:
                    idx_cone.append((t, viz[a_], viz[b_], len(pares)))
                    pares.append((d["frases"][viz[a_]], d["frases"][viz[b_]]))
    print(f"pares NLI: {len(pares)}", flush=True)

    # coleta retomável (checkpoint por lote; rodar em 1º plano — QoS do macOS)
    con = np.full(len(pares), -1.0, np.float32)
    ent2 = np.full(len(pares), -1.0, np.float32)
    feito = 0
    if NPZ.exists():
        zz = np.load(NPZ)
        if int(zz["k"]) == len(pares):
            con, ent2 = zz["con"].copy(), zz["ent"].copy()
            feito = int(zz["feito"]) if "feito" in zz else len(pares)
            print(f"cache h4_nli.npz: {feito}/{len(pares)} feitos", flush=True)
    if feito < len(pares):
        import nli_runner
        nli_runner.NLI_BATCH = 64
        nli = nli_runner.make_nli()
        if nli is None:
            print("[ERRO] NLI indisponivel."); return
        LOTE = 4096
        for s in range(feito, len(pares), LOTE):
            pr = nli(pares[s:s + LOTE])
            con[s:s + len(pr)] = pr[:, 2]
            ent2[s:s + len(pr)] = pr[:, 0]
            feito = s + len(pr)
            np.savez(NPZ, con=con, ent=ent2, k=len(pares), feito=feito)
            print(f"  NLI {feito}/{len(pares)}", flush=True)

    CON_OE = np.zeros((len(itens), K), np.float32)   # o->frase
    CON_EO = np.zeros((len(itens), K), np.float32)   # frase->o
    for t, j, k_ in idx_oe:
        CON_OE[t, j] = con[k_]
    for t, j, k_ in idx_eo:
        CON_EO[t, j] = con[k_]
    CONE_C: dict[tuple, float] = {}
    for t, a_, b_, k_ in idx_cone:
        CONE_C[(t, a_, b_)] = float(con[k_])

    # ---- features por opiniao
    linhas = []
    for t, d in enumerate(itens):
        row = {"hall": int(d["hall"]),
               "nli_max": float(EO[t].max()),
               "cos_max": float(SI[t].max()),
               "con_ativa": float(np.maximum(CON_OE[t], CON_EO[t]).max())}
        for tau in (0.50, 0.35, 0.20):
            viz = [j for j in range(K) if EO[t, j] >= tau]
            m = len(viz)
            row[f"nsup_{int(tau*100)}"] = m
            if m == 0:
                row[f"mundos_{int(tau*100)}"] = 0
                row[f"we_{int(tau*100)}"] = 0.0
                row[f"incoer_{int(tau*100)}"] = 0
                continue
            # poset do cone: ordem via EE (acarretamento frase->frase, cache f2)
            P = np.eye(m, dtype=bool)
            for a_ in range(m):
                for b_ in range(m):
                    if a_ != b_ and EE[t, viz[a_], viz[b_]] >= 0.50:
                        P[a_, b_] = True
            for kk in range(m):
                P |= np.outer(P[:, kk], P[kk, :])
            C = np.zeros((m, m), bool)
            for a_ in range(m):
                for b_ in range(m):
                    if a_ != b_ and CONE_C.get((t, viz[a_], viz[b_]), 0.0) >= TAU_CON:
                        C[a_, b_] = True
            prf = H.perfil_mundos(P, C, np.ones(m) / m)
            row[f"mundos_{int(tau*100)}"] = prf["n_mundos"]
            row[f"we_{int(tau*100)}"] = prf["we"]
            row[f"incoer_{int(tau*100)}"] = int(prf["n_mundos"] > 1)
        linhas.append(row)
    D = pd.DataFrame(linhas)
    D.to_csv(E0.OUT / "incoherent_support.csv", index=False)
    y = D.hall.to_numpy().astype(bool)
    rng = np.random.default_rng(SEED)

    E0.banner("P8 — ESTRUTURA (o que existe, antes de perguntar se preve)")
    for tau in (50, 35, 20):
        ns, mu = D[f"nsup_{tau}"], D[f"mundos_{tau}"]
        inc = D[f"incoer_{tau}"]
        print(f"  tau=0.{tau}: cone medio {ns.mean():.2f} · com suporte "
              f"{(ns > 0).mean():5.1%} · INCOERENTE {inc.mean():5.1%} "
              f"(mundos medios {mu[ns > 0].mean():.2f})")
    print(f"  contradicao ATIVA (max o<->frase): media "
          f"{D.con_ativa.mean():.3f} · >=0.5 em {(D.con_ativa >= .5).mean():.1%}")

    E0.banner("P8 — AUROC contra o rotulo humano (n=837, 93 pos) — EXPLORATORIO")
    feats = [("nli_max", "NLI max (baseline F3, la: 0.676)", -1),
             ("cos_max", "cosseno max", -1),
             ("con_ativa", "CONTRADICAO ATIVA (nova)", +1),
             ("nsup_35", "|cone| tau=0.35 (F3: 0.663)", -1),
             ("mundos_35", "mundos do cone (novo)", +1),
             ("we_35", "WE do cone (novo)", +1),
             ("incoer_35", "flag suporte incoerente (novo)", +1)]
    print(f"  {'feature':38s} {'AUROC':>7s}")
    print("  " + "-" * 48)
    for c, nome, sg in feats:
        s = D[c].to_numpy(float) * sg
        print(f"  {nome:38s} {E0.auc(y, s):7.3f}")

    def dauc(a, b, nb=5000):
        d = []
        for _ in range(nb):
            i = rng.integers(0, len(y), len(y))
            if len(np.unique(y[i])) < 2:
                continue
            d.append(E0.auc(y[i], a[i]) - E0.auc(y[i], b[i]))
        d = np.array(d)
        return d.mean(), *np.percentile(d, [2.5, 97.5])

    base = -D.nli_max.to_numpy(float)
    print("\n  combinacao por soma de postos (exploratorio):")
    import scipy.stats as st
    for extra, nome in [("con_ativa", "nli_max + con_ativa"),
                        ("we_35", "nli_max + WE cone"),
                        ("incoer_35", "nli_max + incoerente")]:
        comb = st.rankdata(base) + st.rankdata(D[extra].to_numpy(float))
        mu, lo, hi = dauc(comb, base)
        stt = "  *" if lo > 0 else ""
        print(f"    {nome:28s} AUROC {E0.auc(y, comb):.3f} · delta vs nli_max "
              f"{mu:+.4f} [{lo:+.4f},{hi:+.4f}]{stt}")

    E0.banner("GUARDA (estilo E19/E26): entre as opinioes que o NLI APROVA")
    for q in (0.5, 0.7):
        thr = np.quantile(D.nli_max, q)
        apr = D.nli_max >= thr
        fp = y[apr].mean()
        for c, nome in [("incoer_35", "suporte incoerente"),
                        ("con_ativa", "contradicao ativa >= 0.5")]:
            flag = (D[c] >= (1 if c == "incoer_35" else 0.5)) & apr
            if flag.sum() < 5:
                continue
            lift = y[flag].mean() / max(fp, 1e-9)
            boots = []
            ia = np.where(apr)[0]
            for _ in range(2000):
                ii = ia[rng.integers(0, len(ia), len(ia))]
                fl = flag.to_numpy()[ii]
                if fl.sum() < 3 or y[ii].mean() == 0:
                    continue
                boots.append(y[ii][fl].mean() / y[ii].mean())
            lo, hi = np.percentile(boots, [2.5, 97.5])
            print(f"  aprova q{int(q*100)} (risco base {fp:.1%}) · {nome}: "
                  f"lift {lift:.2f}x [{lo:.2f}, {hi:.2f}] "
                  f"(sinaliza {flag.sum()}/{apr.sum()})")
    print(f"\ngravado: {E0.OUT / 'incoherent_support.csv'}")


if __name__ == "__main__":
    main()

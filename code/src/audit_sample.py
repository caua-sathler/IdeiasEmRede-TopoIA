"""K1 — PLANILHA DA AUDITORIA DE ROTULOS (ma-atribuicao entre as alucinacoes).

Pergunta: das opinioes-ouro marcadas como NAO SUPORTADAS pelo rotulo humano do
PublicHearingBR, quantas sao MA-ATRIBUICOES (o conteudo foi dito na audiencia,
mas por outra pessoa)? Este script so MONTA a planilha cega para o auditor
humano; nao classifica nada.

Universo: exatamente o do incidence_features/nli_features — opinioes com rotulo e com o `envolvido`
casado a um orador da transcricao (`speaker_incidence.match_gold` sobre os marcadores
de turno `O SR./A SRA. NOME -`, com forward-fill). Esperado: n=3.630, 408
positivos (conferido contra `results/incidence_features.csv`, se existir).

Amostra: 50 positivos, `numpy.random.default_rng(20260923).choice(..., 50,
replace=False)` sobre os positivos na ordem de construcao do universo (ordem
das audiencias de `dataset_readers.refs_ok()`, depois ordem das linhas do CSV de
opinioes). Sem estratificacao.

Por item: id (ref + indice da linha em opinions_XXX.csv), audiencia (manchete da
materia como rotulo legivel), opiniao, participante atribuido (+ cargo), orador
casado; top-5 frases do orador atribuido e top-5 globais (com orador), cosseno
MPNet; 1 frase de contexto antes/depois da melhor global e da melhor do orador;
cos_s, best_other, Delta = best_other - cos_s (definicoes do incidence_features.py), cos_g.

Custo: zero chamadas de modelo (embeddings MPNET ja versionados em dataset/).

    python audit_sample.py [DIR_SAIDA]     # padrao: /tmp/audit
"""
from __future__ import annotations

import os
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
CODIGO = HERE if (HERE / "common.py").exists() else Path(
    os.environ.get("ARTIGO_CODIGO", HERE))
sys.path.insert(0, str(CODIGO))

import common as E0            # noqa: E402
import dataset_readers as R             # noqa: E402
import speaker_incidence as H6        # noqa: E402

warnings.filterwarnings("ignore")
SEED = 20260923
N_AMOSTRA = 50
TOPK = 5
OUTDIR = Path(sys.argv[1] if len(sys.argv) > 1
              else os.environ.get("AUDIT_OUT", "/tmp/audit"))


def carregar(ref: str):
    """Mesma montagem do h6/incidence_features/nli_features: frases alinhadas aos embeddings, orador por
    frase (forward-fill), candidatos, S = opinioes x frases (cosseno MPNet)."""
    Tm = R.emb(ref, "transcript", R.GEOM)
    g, ge = R.opinions(ref), R.op_emb(ref)
    if not len(Tm) or ge is None or len(g) != len(ge):
        return None
    fr = R.phrases(ref, "transcript")[:len(Tm)]
    if len(fr) < len(Tm):
        fr = fr + [""] * (len(Tm) - len(fr))
    spk = H6.speakers(fr)
    cands = sorted({s for s in spk if s})
    idx_spk = {c: np.where(spk == c)[0] for c in cands}
    return dict(g=g, fr=fr, spk=spk, cands=cands, idx_spk=idx_spk, S=ge @ Tm.T)


def universo() -> pd.DataFrame:
    linhas = []
    for r in R.refs_ok():
        A = carregar(r)
        if A is None:
            continue
        g, S = A["g"], A["S"]
        for i in range(len(g)):
            lab = g.alucinacao_manual.iloc[i]
            if pd.isna(lab):
                continue
            quem = g.envolvido.iloc[i] if "envolvido" in g else None
            m = H6.match_gold(quem, A["cands"]) if quem is not None else None
            if m is None:
                continue
            best = {c: float(S[i, j].max()) for c, j in A["idx_spk"].items()
                    if len(j)}
            cos_s = best[m]
            outros = [v for c, v in best.items() if c != m]
            bo = max(outros) if outros else 0.0
            linhas.append({"ref": r, "op_idx": i, "hall": int(bool(lab)),
                           "envolvido": quem, "orador_casado": m,
                           "cos_s": cos_s, "best_other": bo,
                           "delta": bo - cos_s, "cos_g": float(S[i].max())})
    return pd.DataFrame(linhas)


def conferir(U: pd.DataFrame) -> None:
    f = E0.OUT / "incidence_features.csv"
    if not f.exists():
        print(f"[aviso] {f} ausente; paridade com incidence_features nao conferida")
        return
    C = pd.read_csv(f)
    assert len(C) == len(U), (len(C), len(U))
    assert (C.ref.to_numpy() == U.ref.to_numpy()).all()
    assert (C.hall.to_numpy() == U.hall.to_numpy()).all()
    for c in ("cos_s", "best_other"):
        assert np.allclose(C[c].to_numpy(), U[c].to_numpy(), atol=1e-6), c
    print(f"[ok] paridade com {f.name}: ref, hall, cos_s, best_other")


def manchete(ref: str) -> str:
    a = R.phrases(ref, "article")
    return a[0].strip() if a else ""


def rotulo_orador(s) -> str:
    return s if s else "(antes do 1o marcador de turno)"


def bloco(row, A) -> dict:
    i, m = int(row.op_idx), row.orador_casado
    g, fr, spk, S = A["g"], A["fr"], A["spk"], A["S"][int(row.op_idx)]
    js = A["idx_spk"][m]
    top_s = js[np.argsort(-S[js], kind="stable")[:TOPK]]
    top_g = np.argsort(-S, kind="stable")[:TOPK]

    def ctx(k):
        prev = fr[k - 1] if k > 0 else ""
        nxt = fr[k + 1] if k + 1 < len(fr) else ""
        return (prev, rotulo_orador(spk[k - 1]) if k > 0 else "",
                nxt, rotulo_orador(spk[k + 1]) if k + 1 < len(fr) else "")

    d = {"item": None, "ref": row.ref, "op_idx": i,
         "id": f"{row.ref}#{i}",
         "audiencia": manchete(row.ref),
         "opiniao": str(g.opiniao.iloc[i]),
         "participante_atribuido": str(row.envolvido),
         "cargo": str(g.cargo.iloc[i]) if "cargo" in g else "",
         "orador_casado": m,
         "n_frases_orador": int(len(js)),
         "n_frases_transcricao": int(len(fr)),
         "n_oradores": int(len(A["cands"])),
         "cos_s": row.cos_s, "best_other": row.best_other,
         "delta": row.delta, "cos_g": row.cos_g}
    for n, k in enumerate(top_s, 1):
        d[f"orador_top{n}_idx"] = int(k)
        d[f"orador_top{n}_cos"] = float(S[k])
        d[f"orador_top{n}_texto"] = fr[k]
    for n, k in enumerate(top_g, 1):
        d[f"global_top{n}_idx"] = int(k)
        d[f"global_top{n}_cos"] = float(S[k])
        d[f"global_top{n}_orador"] = rotulo_orador(spk[k])
        d[f"global_top{n}_texto"] = fr[k]
    for nome, k in (("melhor_orador", int(top_s[0])),
                    ("melhor_global", int(top_g[0]))):
        p, ps, n_, ns = ctx(k)
        d[f"{nome}_ctx_antes"] = p
        d[f"{nome}_ctx_antes_orador"] = ps
        d[f"{nome}_ctx_depois"] = n_
        d[f"{nome}_ctx_depois_orador"] = ns
    # campos em branco para o auditor
    d["auditor_categoria"] = ""
    d["auditor_orador_real"] = ""
    d["auditor_notas"] = ""
    return d


def md(d: dict) -> str:
    q = lambda t: str(t).replace("\n", " ").strip()   # noqa: E731
    L = [f"## Item {d['item']:02d} — `{d['id']}`", "",
         f"- **Audiência ({d['ref']}):** {q(d['audiencia'])}",
         f"- **Participante atribuído:** {q(d['participante_atribuido'])}"
         f" — {q(d['cargo'])}",
         f"- **Orador casado na transcrição:** {q(d['orador_casado'])}"
         f" ({d['n_frases_orador']} frases de {d['n_frases_transcricao']};"
         f" {d['n_oradores']} oradores na audiência)",
         f"- **cos_s** = {d['cos_s']:.3f} · **best_other** = "
         f"{d['best_other']:.3f} · **Δ** = best_other − cos_s = "
         f"{d['delta']:+.3f} · cos_g = {d['cos_g']:.3f}", "",
         "**Opinião (PT original):**", "", f"> {q(d['opiniao'])}", "",
         "**Top-5 nos turnos do orador atribuído**", "",
         "| # | frase | cos | texto |", "|---|---|---|---|"]
    for n in range(1, TOPK + 1):
        if f"orador_top{n}_idx" in d:
            L.append(f"| {n} | {d[f'orador_top{n}_idx']} | "
                     f"{d[f'orador_top{n}_cos']:.3f} | "
                     f"{q(d[f'orador_top{n}_texto']).replace('|', '/')} |")
    L += ["", "**Top-5 globais**", "",
          "| # | frase | cos | orador | texto |", "|---|---|---|---|---|"]
    for n in range(1, TOPK + 1):
        L.append(f"| {n} | {d[f'global_top{n}_idx']} | "
                 f"{d[f'global_top{n}_cos']:.3f} | "
                 f"{q(d[f'global_top{n}_orador'])} | "
                 f"{q(d[f'global_top{n}_texto']).replace('|', '/')} |")
    for nome, tit, tk in (("melhor_orador", "Contexto da melhor frase do orador",
                           "orador_top1"),
                          ("melhor_global", "Contexto da melhor frase global",
                           "global_top1")):
        quem = (d["orador_casado"] if nome == "melhor_orador"
                else d["global_top1_orador"])
        L += ["", f"**{tit}** (frase {d[f'{tk}_idx']})", "",
              f"- antes [{q(d[f'{nome}_ctx_antes_orador'])}]: "
              f"{q(d[f'{nome}_ctx_antes'])}",
              f"- **frase [{q(quem)}]: {q(d[f'{tk}_texto'])}**",
              f"- depois [{q(d[f'{nome}_ctx_depois_orador'])}]: "
              f"{q(d[f'{nome}_ctx_depois'])}"]
    L += ["", "**Auditor** — categoria: ______ · orador real: ______ · "
          "notas: ______", "", "---", ""]
    return "\n".join(L)


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    E0.banner("K1 — universo com orador casado")
    U = universo()
    print(f"universo: n={len(U)} · positivos={int(U.hall.sum())} · "
          f"audiencias={U.ref.nunique()}")
    conferir(U)

    P = U[U.hall == 1].reset_index(drop=True)
    rng = np.random.default_rng(SEED)
    sel = np.sort(rng.choice(len(P), N_AMOSTRA, replace=False))
    A_ = P.iloc[sel].reset_index(drop=True)
    A_.insert(0, "item", np.arange(1, len(A_) + 1))
    A_[["item", "ref", "op_idx"]].assign(
        id=A_.ref + "#" + A_.op_idx.astype(str)).to_csv(
        OUTDIR / "ids_amostra.csv", index=False)
    print(f"amostra: {len(A_)} positivos em {A_.ref.nunique()} audiencias "
          f"(seed {SEED})")

    blocos, cache = [], {}
    for _, row in A_.iterrows():
        if row.ref not in cache:
            cache = {row.ref: carregar(row.ref)}   # uma audiencia por vez
        d = bloco(row, cache[row.ref])
        d["item"] = int(row["item"])
        blocos.append(d)
    D = pd.DataFrame(blocos)
    D.to_csv(OUTDIR / "planilha.csv", index=False, encoding="utf-8")

    cab = ["# Auditoria de rótulos — 50 opiniões marcadas como não suportadas",
           "",
           f"Universo: opiniões com rótulo humano e participante casado a um "
           f"orador da transcrição (n={len(U)}, {int(U.hall.sum())} marcadas). "
           f"Amostra aleatória de {N_AMOSTRA} (numpy default_rng, seed {SEED}).",
           "",
           "Cossenos no espaço MPNet (L2-normalizado). `cos_s` = maior cosseno "
           "nos turnos do orador atribuído; `best_other` = maior cosseno nos "
           "turnos de qualquer outro orador; Δ = best_other − cos_s; `cos_g` = "
           "maior cosseno na transcrição inteira. O orador de cada frase vem "
           "do último marcador `O SR./A SRA. NOME -` anterior (forward-fill). "
           "\"Audiência\" é a manchete da matéria da Agência Câmara pareada.",
           "", "---", ""]
    (OUTDIR / "planilha.md").write_text(
        "\n".join(cab) + "\n".join(md(d) for d in blocos), encoding="utf-8")

    vazio = (D.n_frases_orador <= 1).sum()
    print(f"itens com orador de <=1 frase: {vazio} · "
          f"Delta>0 (outro orador casa melhor): {(D.delta > 0).sum()}")
    print(f"gravado: {OUTDIR/'planilha.md'} · {OUTDIR/'planilha.csv'} · "
          f"{OUTDIR/'ids_amostra.csv'}")


if __name__ == "__main__":
    main()

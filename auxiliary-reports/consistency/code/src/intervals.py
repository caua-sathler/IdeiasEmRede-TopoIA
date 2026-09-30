"""R1 — OS NÚMEROS DO RELATÓRIO QUE NÃO SAEM DIRETO DOS LOGS h1–h5.

O relatório auxiliar (`../consistency_report.tex`) cita números que os scripts
h1–h5 não imprimem: intervalos de Wilson para proporções, bootstraps pareados a
mais no TriviaQA e no h5, intervalos agrupados por audiência no h4, o controle
do tamanho do suporte no h4, o exemplo trabalhado da Seção 3 e o contraexemplo
"WE pode exceder SE". Todos saem daqui, lendo só `results/*.csv` e `cache/` —
zero chamadas de modelo, zero dataset.

Pré-requisito: rodar h2, h3 e h5 antes (eles gravam `results/triviaqa_worlds.csv`,
`results/domain_conflict.csv` e `results/sentence_intervention.csv`). O `results/incoherent_support.csv` já vem no
pacote, porque regenerá-lo exige o dataset do PublicHearingBR (ver README).

Convenções: toda diferença é a estimativa PONTUAL; todo bootstrap usa 5.000
reamostras (semente 42) da unidade indicada na linha (pergunta, conjunto ou
audiência); os CSV são lidos com `float_precision="round_trip"`, para que a
leitura devolva exatamente os valores calculados (sem isso, o último bit muda e
empates exatos de AUROC deixam de ser empates).

    python intervals.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import common as E0                    # noqa: E402
import finite_space as F          # noqa: E402
import event_structure as H      # noqa: E402

SEED = 42
NB = 5000


def ler(nome: str) -> pd.DataFrame:
    return pd.read_csv(E0.OUT / nome, float_precision="round_trip")


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """Intervalo de Wilson para uma proporção k/n (IC95)."""
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return c - h, c + h


def conflacao(pts: np.ndarray, mundos: np.ndarray) -> tuple[int, int]:
    """(conjuntos multi-classe com UM mundo, conjuntos multi-classe)."""
    multi = pts > 1
    return int((multi & (mundos == 1)).sum()), int(multi.sum())


def um_mundo_com_conflito(X: pd.DataFrame) -> tuple[int, int]:
    """Dos conjuntos multi-classe com UM mundo, quantos ainda tem alguma aresta
    de conflito? So pode acontecer quando todo conflito envolve uma classe
    autoconflitante (fora de todos os mundos)."""
    um = (X.pts > 1) & (X.n_mundos == 1)
    return int((um & (X.dens_c > 0)).sum()), int(um.sum())


def ic(vals) -> tuple[float, float]:
    lo, hi = np.percentile(vals, [2.5, 97.5])
    return float(lo), float(hi)


def exemplo_trabalhado() -> None:
    E0.banner("EXEMPLO TRABALHADO (Secao 3 do relatorio)")
    # classes: 0 = "aprovou", 1 = "aprovou por ampla margem",
    #          2 = "rejeitou", 3 = "a sessao durou quatro horas"
    P = np.eye(4, dtype=bool)
    P[1, 0] = True                      # a2 acarreta a1 (a2 ⊑ a1)
    C = np.zeros((4, 4), bool)
    C[0, 2] = C[2, 0] = True            # a1 # a3 (coluna de contradicao)
    p = np.ones(4) / 4
    Cs = H.fechar_conflito(P, C)
    Ws = H.mundos(Cs)
    q = H.massa_mundos(Ws, p)
    se = F.entropia_semantica(np.arange(4))
    print(f"  SE = log 4 = {se:.4f}")
    print(f"  conflito herdado a2 # a3: {bool(Cs[1, 2])}")
    print(f"  mundos: {[[f'a{u + 1}' for u in W] for W in Ws]}  massas {np.round(q, 4)}")
    print(f"  WE = {H.entropia_mundos(P, C, p):.4f}   (log 2 = {np.log(2):.4f})")
    P3, C3 = P[np.ix_([0, 1, 3], [0, 1, 3])], np.zeros((3, 3), bool)
    print(f"  sem a3: SE = log 3 = {np.log(3):.4f} · mundos "
          f"{len(H.mundos(H.fechar_conflito(P3, C3)))} · WE "
          f"{H.entropia_mundos(P3, C3, np.ones(3) / 3):.4f}")

    E0.banner("WE NAO E UMA SE DESCONTADA: pode exceder a SE")
    n = 6
    P6 = np.eye(n, dtype=bool)                       # anticadeia de 6 classes
    C6 = np.zeros((n, n), bool)
    for a, b in [(0, 1), (2, 3), (4, 5)]:            # 3 incertezas binarias
        C6[a, b] = C6[b, a] = True
    Ws6 = H.mundos(H.fechar_conflito(P6, C6))
    print(f"  a#b, c#d, e#f: {len(Ws6)} mundos · WE = "
          f"{H.entropia_mundos(P6, C6, np.ones(n) / n):.4f} > SE = log 6 = "
          f"{np.log(6):.4f}")
    # e o caso "todo par em conflito" so da WE = SE numa ANTICADEIA: se u ⊑ v
    # e u # v, u e autoconflitante e sobra um mundo so
    P2 = np.array([[True, True], [False, True]])      # u ⊑ v
    C2 = np.array([[False, True], [True, False]])     # u # v
    print(f"  cadeia u ⊑ v com u # v: mundos "
          f"{len(H.mundos(H.fechar_conflito(P2, C2)))} · WE "
          f"{H.entropia_mundos(P2, C2, np.ones(2) / 2):.4f} (u e autoconflitante)")


def triviaqa() -> None:
    E0.banner("TRIVIAQA — pares em conflito, validade e estratos com intervalos")
    itens = [json.loads(l) for l in (HERE.parent / "cache" / "f11_triviaqa.jsonl")
             .read_text().splitlines() if l.strip()]
    itens = [d for d in itens if len(d["amostras"]) >= 6]
    z = np.load(HERE.parent / "cache" / "f12_nli.npz")
    chaves = [(k, i, j) for k, d in enumerate(itens)
              for i in range(len(d["amostras"]))
              for j in range(len(d["amostras"])) if i != j]
    VC = dict(zip(chaves, z["con"]))
    tot = hit = 0
    for k, d in enumerate(itens):
        n = len(d["amostras"])
        for i in range(n):
            for j in range(i + 1, n):
                tot += 1
                hit += max(VC[(k, i, j)], VC[(k, j, i)]) >= 0.5
    print(f"  pares nao ordenados com contradicao >= 0,5: {hit}/{tot} = "
          f"{hit / tot:.1%}")

    # VALIDADE DE CONSTRUTO com IC AGRUPADO POR PERGUNTA. O h2 reamostra
    # PARES, que nao sao independentes dentro de uma pergunta; aqui a unidade
    # reamostrada e a pergunta (a estimativa pontual e a mesma do h2).
    import triviaqa_collect as F11
    por_item = []
    for k, d in enumerate(itens):
        A = d["amostras"]
        cts = [F11.acerta(a, d["aliases"])[1] for a in A]
        pp = [(max(VC[(k, i, j)], VC[(k, j, i)]) >= 0.5, int(cts[i] != cts[j]))
              for i in range(len(A)) for j in range(i + 1, len(A))]
        por_item.append(np.array(pp, dtype=int))

    def dif(blocos):
        X = np.concatenate(blocos)
        return X[X[:, 0] == 1, 1].mean() - X[X[:, 0] == 0, 1].mean()

    rng = np.random.default_rng(SEED)
    bs = [dif([por_item[i] for i in rng.integers(0, len(por_item), len(por_item))])
          for _ in range(NB)]
    lo, hi = ic(bs)
    print(f"  validade de construto (acerto misto, conflito - compativel): "
          f"{dif(por_item):+.3f} [{lo:+.3f}, {hi:+.3f}] (IC agrupado por pergunta)")

    D = ler("triviaqa_worlds.csv")
    y = D.ok.to_numpy().astype(bool)
    estratos = [("uma classe (SE = 0)", D.pts == 1),
                ("multi-classe, 1 mundo", (D.pts > 1) & (D.n_mundos == 1)),
                ("multi-classe, >1 mundo", (D.pts > 1) & (D.n_mundos > 1))]
    print(f"\n  {'estrato':26s} {'n':>4s} {'acerto':>7s}   IC95 (Wilson)"
          f"      SE medio  WE medio")
    for nome, m in estratos:
        k, n = int(D.ok[m].sum()), int(m.sum())
        lo, hi = wilson(k, n)
        print(f"  {nome:26s} {n:4d} {k / n:7.1%}   [{lo:.1%}, {hi:.1%}]"
              f"   {D.se[m].mean():8.3f}  {D.we[m].mean():8.3f}")
    k, n = um_mundo_com_conflito(D)
    print(f"  dos {n} conjuntos multi-classe com 1 mundo, {k} contem conflito "
          f"(so com classes autoconflitantes)")
    oks = [D.ok[m].to_numpy() for _, m in estratos]
    for (a, b, rot) in [(0, 1, "uma classe - 1 mundo"),
                        (1, 2, "1 mundo - >1 mundo")]:
        x, w = oks[a], oks[b]
        ds = [rng.choice(x, len(x)).mean() - rng.choice(w, len(w)).mean()
              for _ in range(NB)]
        lo, hi = ic(ds)
        print(f"  diferenca de acerto, {rot:22s} {x.mean() - w.mean():+.3f} "
              f"[{lo:+.3f}, {hi:+.3f}]")

    # P5 (registrada como "direcao com IC"): no estrato com escada (nucleo
    # menor que |P|), os errados tem mais mundos? AUROC dos mundos + IC.
    esc = (D.nuc < D.pts).to_numpy()
    ye, se_ = y[esc], -D.n_mundos.to_numpy(float)[esc]
    vs = []
    for _ in range(NB):
        i = rng.integers(0, len(ye), len(ye))
        if len(np.unique(ye[i])) == 2:
            vs.append(E0.auc(ye[i], se_[i]))
    lo, hi = ic(vs)
    print(f"  P5, estrato com escada (n={esc.sum()}): AUROC dos mundos "
          f"{E0.auc(ye, se_):.3f} [{lo:.3f}, {hi:.3f}]")

    # P4, braco de COMBINACAO (registrado em h0, nao rodado em 2026-08-03;
    # rodado aqui em 2026-09-30): soma de postos densidade + WE (ou + mundos)
    # contra a densidade sozinha, pareado por pergunta.
    from scipy.stats import rankdata
    dens = D.dens_c.to_numpy(float)
    for col, rot in [("we", "densidade + WE"), ("n_mundos", "densidade + mundos")]:
        comb = rankdata(dens) + rankdata(D[col].to_numpy(float))
        pt = E0.auc(y, -comb) - E0.auc(y, -dens)
        vs = []
        for _ in range(NB):
            i = rng.integers(0, len(y), len(y))
            if len(np.unique(y[i])) == 2:
                vs.append(E0.auc(y[i], -comb[i]) - E0.auc(y[i], -dens[i]))
        lo, hi = ic(vs)
        print(f"  P4 combinacao, {rot:20s} AUROC {E0.auc(y, -comb):.3f} · "
              f"vs densidade {pt:+.4f} [{lo:+.4f}, {hi:+.4f}]")


def lei_de_conflacao() -> None:
    E0.banner("TAXA DE CONFLACAO — por dominio, com intervalos de Wilson")
    D3 = ler("domain_conflict.csv")
    D2 = ler("triviaqa_worlds.csv")
    linhas = [(g, D3[D3.grupo == g]) for g in
              ["REAL", "LLAMA", "MISTO", "EMBARALHADO", "INTERV_A", "INTERV_B"]]
    linhas.insert(2, ("TRIVIAQA", D2))
    print(f"  {'dominio':12s} {'n':>4s} {'|P|':>5s} {'mundos':>6s} {'>1 m.':>6s} "
          f"{'SE':>6s} {'WE':>6s} {'dens_c':>6s} {'multi':>5s} {'conflacao':>9s}"
          f"   IC95 (Wilson)   1 mundo c/ conflito   estrita")
    for g, X in linhas:
        k, n = conflacao(X.pts.to_numpy(), X.n_mundos.to_numpy())
        lo, hi = wilson(k, n)
        kc, nc = um_mundo_com_conflito(X)
        print(f"  {g:12s} {len(X):4d} {X.pts.mean():5.2f} {X.n_mundos.mean():6.2f} "
              f"{(X.n_mundos > 1).mean():6.1%} {X.se.mean():6.3f} {X.we.mean():6.3f} "
              f"{X.dens_c.mean():6.3f} {n:5d} {k / n:9.1%}   [{lo:.1%}, {hi:.1%}]"
              f"   {kc:4d}/{nc:<4d}            {(k - kc) / n:6.1%}")
    print("  (medias por conjunto; conflacao = multi-classe com 1 mundo; '1 mundo c/"
          "\n   conflito' = desses, quantos tem conflito envolvendo classe"
          "\n   autoconflitante; 'estrita' = multi-classe sem NENHUM conflito)")
    print(f"  conjuntos REAL com 1 mundo (todos, P7): "
          f"{(D3[D3.grupo == 'REAL'].n_mundos == 1).mean():.1%}")


def intervencao_h5() -> None:
    E0.banner("H5 — a subida da conflacao e a interacao (bootstrap pareado)")
    D = ler("sentence_intervention.csv")
    H2 = ler("triviaqa_worlds.csv")
    ent = [json.loads(x) for x in (HERE.parent / "cache" / "f11_triviaqa.jsonl")
           .read_text().splitlines() if x.strip()]
    H2["qid"] = [d["qid"] for d in ent if len(d["amostras"]) >= 6]
    ME = H2.set_index("qid").loc[D.qid].reset_index()
    y = D.ok.to_numpy().astype(bool)
    rng = np.random.default_rng(SEED)

    def taxa(X, i):
        k, n = conflacao(X.pts.to_numpy()[i], X.n_mundos.to_numpy()[i])
        return k / max(n, 1)

    todos = np.arange(len(D))
    ds = []
    for _ in range(NB):
        i = rng.integers(0, len(D), len(D))
        ds.append(taxa(D, i) - taxa(ME, i))
    lo, hi = ic(ds)
    for nome, X in [("ENTIDADE", ME), ("FRASE", D)]:
        k, n = conflacao(X.pts.to_numpy(), X.n_mundos.to_numpy())
        a, b = wilson(k, n)
        kc, nc = um_mundo_com_conflito(X)
        print(f"  {nome:9s} conflacao {k}/{n} = {k / n:.1%}  [{a:.1%}, {b:.1%}]"
              f"  · 1 mundo com conflito: {kc}/{nc} · estrita {(k - kc) / n:.1%}")
    print(f"  subida (frase - entidade, pareada): "
          f"{taxa(D, todos) - taxa(ME, todos):+.3f} [{lo:+.3f}, {hi:+.3f}]")

    s = {"se_f": -D.se.to_numpy(float), "se_e": -ME.se.to_numpy(float),
         "we_f": -D.we.to_numpy(float), "we_e": -ME.we.to_numpy(float)}
    print(f"  AUROC do SE-nucleo nas mesmas 202 perguntas: entidade "
          f"{E0.auc(y, -ME.se_nuc.to_numpy(float)):.3f} · frase "
          f"{E0.auc(y, -D.se_nuc.to_numpy(float)):.3f}")

    def inter(i):
        return ((E0.auc(y[i], s["se_f"][i]) - E0.auc(y[i], s["se_e"][i]))
                - (E0.auc(y[i], s["we_f"][i]) - E0.auc(y[i], s["we_e"][i])))

    vs = []
    for _ in range(NB):
        i = rng.integers(0, len(y), len(y))
        if len(np.unique(y[i])) == 2:
            vs.append(inter(i))
    lo, hi = ic(vs)
    print(f"  interacao (queda da SE - queda do WE): {inter(todos):+.4f} "
          f"[{lo:+.4f}, {hi:+.4f}]")

    # CONTROLE DO TAMANHO DA AMOSTRA. O modo frase tem ate 8 amostras por
    # pergunta; o modo entidade, ate 10. Menos amostras poderiam, por si so,
    # piorar a SE. Refazemos o modo entidade com as 8 PRIMEIRAS amostras, do
    # mesmo cache de NLI (f12), e repetimos a comparacao pareada.
    itens = [d for d in ent if len(d["amostras"]) >= 6]
    z = np.load(HERE.parent / "cache" / "f12_nli.npz")
    chaves = [(k, i, j) for k, d in enumerate(itens)
              for i in range(len(d["amostras"]))
              for j in range(len(d["amostras"])) if i != j]
    VE = dict(zip(chaves, z["ent"]))
    se8 = {}
    for k, d in enumerate(itens):
        n = min(8, len(d["amostras"]))
        M = np.array([[VE.get((k, i, j), 1.0 if i == j else 0.0)
                       for j in range(n)] for i in range(n)]) >= 0.5
        _, lab = F.reflexao_poset(F.fecho_transitivo(M))
        se8[d["qid"]] = F.entropia_semantica(lab)
    s8 = -np.array([se8[q] for q in D.qid], float)
    vs = []
    for _ in range(NB):
        i = rng.integers(0, len(y), len(y))
        if len(np.unique(y[i])) == 2:
            vs.append(E0.auc(y[i], s["se_f"][i]) - E0.auc(y[i], s8[i]))
    lo, hi = ic(vs)
    print(f"  controle: SE do modo entidade com 8 amostras, AUROC "
          f"{E0.auc(y, s8):.3f}; queda pareada da SE (frase - entidade/8) "
          f"{E0.auc(y, s['se_f']) - E0.auc(y, s8):+.4f} [{lo:+.4f}, {hi:+.4f}]")


STOP = set("de da do das dos e a o as os que em um uma para com no na nos nas por "
           "sobre ao aos se sua seu suas seus foi ser mais como durante audiencia "
           "publica afirmou destacou defendeu posicao contribuicao".split())


def _toks(s: str) -> set:
    import re
    import unicodedata
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return {w for w in re.findall(r"[a-z]{3,}", s) if w not in STOP}


def checagem_intervencao() -> None:
    """Checagem de manipulacao da troca de evidencia (a mesma do f8 da fase F):
    Jaccard de palavras de conteudo entre a opiniao-ouro e cada resposta, media
    por braco, diferenca pareada A - B por bootstrap sobre os 80 itens."""
    E0.banner("TROCA DE EVIDENCIA — checagem de manipulacao (sobreposicao lexical)")
    itens = [json.loads(l) for l in (HERE.parent / "cache" / "f7_intervencao.jsonl")
             .read_text().splitlines() if l.strip()]

    def jac(a: str, b: str) -> float:
        A, B = _toks(a), _toks(b)
        return len(A & B) / max(len(A | B), 1)

    A = np.array([np.mean([jac(d["ouro"], x) for x in d["com_evidencia"]])
                  for d in itens])
    B = np.array([np.mean([jac(d["ouro"], x) for x in d["sem_evidencia"]])
                  for d in itens])
    rng = np.random.default_rng(SEED)
    d = A - B
    lo, hi = ic([d[rng.integers(0, len(d), len(d))].mean() for _ in range(NB)])
    print(f"  itens {len(itens)} · A (evidencia certa) {A.mean():.4f} · "
          f"B (outra audiencia) {B.mean():.4f} · razao {A.mean() / B.mean():.1f}x")
    print(f"  diferenca pareada A - B: {d.mean():+.4f} [{lo:+.4f}, {hi:+.4f}]")


def _auc_estratificada(y, s, estrato) -> float:
    """AUROC que compara so pares (positivo, negativo) do MESMO estrato:
    soma dos U de Mann-Whitney por estrato / soma dos pares comparaveis."""
    num = den = 0.0
    for k in np.unique(estrato):
        m = estrato == k
        yk, sk = y[m], s[m]
        npos, nneg = int(yk.sum()), int((~yk).sum())
        if npos == 0 or nneg == 0:
            continue
        num += E0.auc(yk, sk) * npos * nneg
        den += npos * nneg
    return num / den if den else float("nan")


def verificacao_h4() -> None:
    E0.banner("H4 — AUROC com IC agrupado por AUDIENCIA (n=837, 40 audiencias)")
    meta = ler("opinions_meta.csv")
    D = ler("incoherent_support.csv")
    assert len(meta) == len(D) and (meta.hall.astype(int).to_numpy()
                                    == D.hall.to_numpy()).all()
    y = D.hall.to_numpy().astype(bool)
    g = meta.ref.to_numpy()
    grupos = {u: np.where(g == u)[0] for u in np.unique(g)}
    chaves = list(grupos)
    rng = np.random.default_rng(SEED)
    amostras = []
    for _ in range(NB):
        sel = rng.choice(len(chaves), len(chaves), replace=True)
        idx = np.concatenate([grupos[chaves[c]] for c in sel])
        if 0 < y[idx].sum() < len(idx):
            amostras.append(idx)
    feats = [("nli_max", -1, "NLI max (baseline)"),
             ("cos_max", -1, "cosseno max"),
             ("con_ativa", +1, "contradicao ativa"),
             ("nsup_35", -1, "|cone| tau=0,35"),
             ("mundos_35", +1, "mundos do cone"),
             ("we_35", +1, "WE do cone"),
             ("incoer_35", +1, "flag suporte incoerente")]
    print(f"  {'feature':28s} {'AUROC':>6s}   IC95 agrupado")
    for c, sg, nome in feats:
        s = D[c].to_numpy(float) * sg
        bs = [E0.auc(y[i], s[i]) for i in amostras]
        lo, hi = ic(bs)
        print(f"  {nome:28s} {E0.auc(y, s):6.3f}   [{lo:.3f}, {hi:.3f}]")
    print(f"  (reamostras validas: {len(amostras)})")

    # CONTROLE DO TAMANHO DO SUPORTE. O numero de mundos cresce com o numero de
    # frases do suporte (e e 0 quando o suporte e vazio), e o tamanho do
    # suporte sozinho ja separa as classes. A pergunta certa e se a coerencia
    # do suporte informa ALEM do tamanho: comparamos so opinioes com o mesmo
    # numero de frases de suporte (AUROC estratificada por |cone|).
    ns = D.nsup_35.to_numpy()
    print(f"\n  suporte vazio (|cone| = 0): {(ns == 0).mean():.1%} das opinioes"
          f" · corr(mundos, |cone|) = "
          f"{np.corrcoef(D.mundos_35, D.nsup_35)[0, 1]:+.2f}")
    # Com |cone| 0 ou 1 os tres tracos sao CONSTANTES (0 ou 1 mundo): esses
    # estratos so contribuem empates forcados, que puxam a AUROC para 0,5 e
    # estreitam o IC. A leitura correta usa so |cone| >= 2, onde ha incoerencia
    # possivel; a versao com todos os estratos fica como referencia.
    dois = ns >= 2
    print(f"  |cone| >= 2: {dois.sum()} opinioes, {int(y[dois].sum())} alucinadas")
    for c, rot in [("mundos_35", "mundos do cone"), ("we_35", "WE do cone"),
                   ("incoer_35", "flag suporte incoerente")]:
        s = D[c].to_numpy(float)
        bs_t = [_auc_estratificada(y[i], s[i], ns[i]) for i in amostras]
        bs_2 = [_auc_estratificada(y[i][dois[i]], s[i][dois[i]], ns[i][dois[i]])
                for i in amostras]
        lo_t, hi_t = ic(bs_t)
        lo_2, hi_2 = ic([b for b in bs_2 if not np.isnan(b)])
        print(f"  mesmo |cone|, {rot:24s} |cone|>=2: "
              f"{_auc_estratificada(y[dois], s[dois], ns[dois]):.3f} "
              f"[{lo_2:.3f}, {hi_2:.3f}] · todos os estratos: "
              f"{_auc_estratificada(y, s, ns):.3f} [{lo_t:.3f}, {hi_t:.3f}]")


def inventario() -> None:
    """Tabela 3 do relatorio: amostras por conjunto em cada montagem, e o
    maior numero de classes de um conjunto (para o custo da enumeracao)."""
    E0.banner("INVENTARIO — amostras por conjunto e maximo de classes")
    C = HERE.parent / "cache"

    def carrega(nome):
        return [json.loads(l) for l in (C / nome).read_text().splitlines()
                if l.strip()]

    def faixa(ns):
        return f"{min(ns)}-{max(ns)}" if min(ns) != max(ns) else f"{min(ns)}"

    ent = [d for d in carrega("f11_triviaqa.jsonl") if len(d["amostras"]) >= 6]
    D5 = ler("sentence_intervention.csv")
    lon, vistos = {}, set()
    for d in carrega("h5_longas.jsonl"):
        if d["qid"] not in vistos:
            vistos.add(d["qid"])
            lon[d["qid"]] = len(d["amostras"])
    qw = [d for d in carrega("f4_geracoes.jsonl") if len(d["amostras"]) >= 8]
    N = min(10, min(len(d["amostras"]) for d in qw))
    ll = [d for d in carrega("f4_llama.jsonl") if len(d["amostras"]) >= 6]
    iv = carrega("f7_intervencao.jsonl")
    print(f"  TriviaQA entidade: {len(ent)} conjuntos, "
          f"{faixa([len(d['amostras']) for d in ent])} amostras")
    print(f"  TriviaQA frase:    {len(D5)} conjuntos, "
          f"{faixa([lon[q] for q in D5.qid])} amostras")
    print(f"  audiencias, Qwen:  {len(qw)} conjuntos, {N} amostras (as {N} primeiras)")
    print(f"  audiencias, Llama: {len(ll)} conjuntos, "
          f"{faixa([len(d['amostras']) for d in ll])} amostras")
    print(f"  troca de evidencia: {len(iv)} pares, "
          f"{faixa([len(d['com_evidencia']) for d in iv] + [len(d['sem_evidencia']) for d in iv])}"
          f" amostras por braco")
    mx = max(int(ler("triviaqa_worlds.csv").pts.max()),
             int(ler("domain_conflict.csv").pts.max()), int(D5.pts.max()))
    print(f"  maior numero de classes num conjunto: {mx}")


def main() -> None:
    inventario()
    exemplo_trabalhado()
    triviaqa()
    lei_de_conflacao()
    intervencao_h5()
    checagem_intervencao()
    verificacao_h4()


if __name__ == "__main__":
    main()

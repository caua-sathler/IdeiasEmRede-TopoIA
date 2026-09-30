"""F11 — COLETA: TriviaQA de livro fechado, o cenário onde a SOTA comprovadamente funciona.

POR QUE ESTE EXPERIMENTO. As três montagens anteriores deram nulo para TODOS os
métodos, inclusive a entropia semântica, que ficou no acaso (0,462 / 0,491) ou
perdeu para um NLI simples. Registrei isso como falha de montagem: em audiências
obscuras o modelo nunca sabe, a corretude não varia, e não há o que prever. Uma
correção sensível à ordem só recupera acurácia onde HÁ acurácia a recuperar.

O LGU (arXiv 2607.16868) reporta +7,1% de AUROC sobre a entropia semântica em QA
padrão. O resultado deles e o meu nulo não se contradizem — eles avaliam onde a
SOTA funciona. Este script vai para lá.

PROTOCOLO, fiel a Farquhar et al. (Nature 630, 2024):

    1 resposta GULOSA (temp 0.1)   -> o rótulo de corretude
    N amostras a temp 1.0          -> as features de incerteza

O rótulo é EXATO e LIVRE DE MODELO: correspondência normalizada contra a lista de
apelidos do TriviaQA (minúsculas, sem pontuação, sem artigos). Nenhuma rede neural
entra no rótulo — a crítica de circularidade que derrubou a E14 não se aplica.

    python triviaqa_collect.py --itens 250 --n 10
"""
from __future__ import annotations

import argparse
import json
import re
import string
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import llm  # noqa: E402

SAIDA = HERE.parent / "cache" / "f11_triviaqa.jsonl"
CJK = re.compile(r"[　-鿿가-힯]")

PROMPT = """Answer the following trivia question. Give ONLY the answer \
-- no explanation, no full sentence, no punctuation at the end.

Question: {q}
Answer:"""


def normaliza(s: str) -> str:
    """Normalização padrão de SQuAD/TriviaQA: minúsculas, sem pontuação, sem
    artigos, espaços colapsados."""
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = "".join(" " if c in string.punctuation else c for c in s)
    s = re.sub(r"\b(a|an|the)\b", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def acerta(pred: str, aliases: list[str]) -> tuple[int, int]:
    """(exact match, containment). EM e o criterio estrito; containment e o
    padrao para modelos generativos, que respondem em frase mesmo instruidos."""
    p = normaliza(pred)
    A = {normaliza(a) for a in aliases if a.strip()}
    em = int(p in A)
    ct = int(any(a and a in p for a in A))
    return em, ct


def limpa(t: str) -> str:
    t = re.sub(r"\s+", " ", t.strip().strip('"').strip("."))
    # o modelo as vezes prefixa "Answer:" ou responde em frase
    t = re.sub(r"^(answer|resposta)\s*:\s*", "", t, flags=re.I)
    return t[:200]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--itens", type=int, default=250)
    ap.add_argument("--n", type=int, default=10)
    ap.add_argument("--modelo", default="qwen2.5:7b")
    args = ap.parse_args()

    feitos = set()
    if SAIDA.exists():
        for ln in SAIDA.read_text().splitlines():
            try:
                feitos.add(json.loads(ln)["qid"])
            except Exception:
                pass
    print(f"ja coletados: {len(feitos)}", flush=True)

    from datasets import load_dataset
    ds = load_dataset("mandarjoshi/trivia_qa", "rc.nocontext",
                      split=f"validation[:{args.itens * 2}]")

    fh = SAIDA.open("a")
    feito = 0
    for ex in ds:
        if feito >= args.itens:
            break
        qid = ex["question_id"]
        if qid in feitos:
            continue
        q = ex["question"].strip()
        aliases = list(ex["answer"]["aliases"]) + [ex["answer"]["value"]]
        pr = PROMPT.format(q=q)

        guloso = limpa(llm.gen(pr, model=args.modelo, temp=0.1, seed=7))
        if not guloso or CJK.search(guloso):
            continue
        amostras = []
        for s in range(args.n):
            t = limpa(llm.gen(pr, model=args.modelo, temp=1.0, seed=3000 + s))
            if t and not CJK.search(t):
                amostras.append(t)
        if len(amostras) < args.n - 2:
            print(f"  [pula {qid}] so {len(amostras)} amostras", flush=True)
            continue

        em, ct = acerta(guloso, aliases)
        fh.write(json.dumps({"qid": qid, "pergunta": q, "ouro": ex["answer"]["value"],
                             "aliases": aliases[:20], "guloso": guloso,
                             "em": em, "ct": ct, "amostras": amostras},
                            ensure_ascii=False) + "\n")
        fh.flush()
        feito += 1
        if feito % 10 == 0:
            print(f"  {feito} itens · acerto corrente "
                  f"{sum(1 for _ in open(SAIDA) if json.loads(_)['ct'])}/{feito+len(feitos)}",
                  flush=True)
    fh.close()
    print(f"\nfim: {feito} itens novos -> {SAIDA}")


if __name__ == "__main__":
    main()

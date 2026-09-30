"""Cliente minimo do proxy Ollama usado pelos coletores de geracao.

Diferenca em relacao ao `diagnostico/llm.py` do repositorio de pesquisa: aquele
lia a chave de um arquivo versionado, **no momento do import**, e portanto
quebrava qualquer script do pacote em uma maquina sem o segredo. Aqui a chave
vem do ambiente e so e exigida na primeira chamada de rede:

    export OLLAMA_BASE="https://<host-do-proxy>"     # obrigatorio
    export OLLAMA_KEY="<chave>"                      # ou OLLAMA_KEY_FILE=<caminho>

Somente os tres coletores precisam disto (`f4_geracoes`, `f7_intervencao`,
`triviaqa_collect`, e o `h5` no pacote da fase H). Todas as ANALISES rodam a partir
dos caches em `cache/*.jsonl`, sem rede — veja o README.

`MIN_GAP` serializa as chamadas: o proxy usado na pesquisa devolvia 429 para
qualquer concorrencia (testado com 1, 4 e 8 workers).
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path

import requests

MIN_GAP = 0.6            # s entre requisicoes
_LAST = [0.0]
_AUTH: dict = {}


def _cfg() -> tuple[str, dict]:
    """Resolve base e cabecalhos na primeira chamada, nao no import."""
    if not _AUTH:
        base = os.environ.get("OLLAMA_BASE", "").rstrip("/")
        key = os.environ.get("OLLAMA_KEY", "")
        if not key and os.environ.get("OLLAMA_KEY_FILE"):
            p = Path(os.environ["OLLAMA_KEY_FILE"]).expanduser()
            key = p.read_text().strip() if p.exists() else ""
        if not base or not key:
            raise SystemExit(
                "[llm] faltam credenciais do proxy de geracao.\n"
                "  export OLLAMA_BASE='https://<host>'\n"
                "  export OLLAMA_KEY='<chave>'      (ou OLLAMA_KEY_FILE=<caminho>)\n\n"
                "  So os coletores precisam disto. As analises rodam offline a\n"
                "  partir de cache/*.jsonl — veja o README."
            )
        _AUTH["base"] = base
        _AUTH["h"] = {"Content-Type": "application/json", "X-API-Key": key}
    return _AUTH["base"], _AUTH["h"]


def gen(prompt: str, model: str = "qwen2.5:7b", temp: float = 0.2,
        seed: int = 42, retries: int = 6, timeout: int = 240) -> str:
    """Uma geracao. Com `temp` baixa e `seed` fixa e reprodutivel; as coletas de
    amostragem multipla usam `temp=1.0` e seed variavel de proposito.

    Serializa as chamadas (`MIN_GAP`) e faz backoff exponencial no 429. Devolve
    string vazia apos esgotar `retries` — os coletores sao retomaveis e
    reprocessam o que ficou vazio.
    """
    base, headers = _cfg()
    body = {"model": model, "prompt": prompt, "stream": False,
            "options": {"temperature": temp, "seed": seed, "num_predict": 600}}
    for a in range(retries):
        gap = MIN_GAP - (time.time() - _LAST[0])
        if gap > 0:
            time.sleep(gap)
        try:
            r = requests.post(f"{base}/api/generate", headers=headers,
                              json=body, timeout=timeout)
            _LAST[0] = time.time()
            if r.status_code == 429:
                time.sleep(min(60, 3 * 2 ** a))
                continue
            r.raise_for_status()
            return r.json().get("response", "").strip()
        except Exception as e:
            _LAST[0] = time.time()
            if a == retries - 1:
                print(f"[llm] falha definitiva: {type(e).__name__}: {e}")
                return ""
            time.sleep(min(60, 3 * 2 ** a))
    return ""


def gen_json(prompt: str, **kw) -> dict | None:
    """Geracao esperando um objeto JSON; tolera cercas ```json e texto em volta."""
    t = gen(prompt, **kw)
    if not t:
        return None
    if "```" in t:
        t = t.split("```")[1]
        t = t[4:] if t.lower().startswith("json") else t
    i, j = t.find("{"), t.rfind("}")
    if i < 0 or j < i:
        return None
    try:
        return json.loads(t[i:j + 1])
    except json.JSONDecodeError:
        return None

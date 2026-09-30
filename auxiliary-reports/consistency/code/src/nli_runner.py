"""Reusable NLI wrapper for the CTM (WP-F): the mDeBERTa-xnli stance model loaded
once, returning **softmax probabilities** in the fixed column order
``[entailment, neutral, contradiction]`` (robust to the checkpoint's own label
ordering). This is the ``nli`` callable injected into ``ctm.verdict_nli`` /
``ctm.stance_node`` / ``ctm.profile_claim`` — the F.2 calibrator, the F.3 notebook
and the demo all import ``make_nli`` so the model wrapper lives in exactly one place.

Mirrors the proven "Aceleração" cell of ``mapper_ctm.ipynb`` (best device
mps→cuda→cpu, batched by length, heavy deps imported lazily). If torch/transformers
are unavailable, ``make_nli`` returns ``None`` and callers guard (the CTM critical
path degrades with a WARN, never crashes — reproducibility contract).
"""

from __future__ import annotations

NLI_MODEL = "MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7"
NLI_MAXLEN, NLI_BATCH = 192, 32
_STATE: dict = {}


def _device() -> str:
    try:
        import torch
        if torch.backends.mps.is_available():
            return "mps"
        if torch.cuda.is_available():
            return "cuda"
    except Exception:
        pass
    return "cpu"


def make_nli(return_probs: bool = True):
    """Return a callable ``nli(pairs) -> np.ndarray``. With ``return_probs`` (default)
    the shape is ``(N, 3)`` softmax probs ``[entail, neutral, contra]``; otherwise
    ``(N,)`` argmax labels (same order). ``pairs`` is a list of ``(premissa, hipótese)``.
    Returns ``None`` if the model can't be loaded (offline / no torch)."""
    if "fn" not in _STATE:
        try:
            import os
            import numpy as np
            import torch
            from transformers import (AutoTokenizer, AutoModelForSequenceClassification,
                                      logging as hf_logging)
            hf_logging.set_verbosity_error()
            torch.set_num_threads(min(16, os.cpu_count() or 4))
            dev = _device()
            tok = AutoTokenizer.from_pretrained(NLI_MODEL)
            mdl = AutoModelForSequenceClassification.from_pretrained(NLI_MODEL).eval().to(dev)
            # reorder logits to [entail, neutral, contra] regardless of the checkpoint's id2label
            lab = {str(v).lower(): int(k) for k, v in mdl.config.id2label.items()}
            perm = [lab.get("entailment", 0), lab.get("neutral", 1), lab.get("contradiction", 2)]

            def _fn(pairs):
                if not pairs:
                    return np.zeros((0, 3), dtype=np.float32)
                order = sorted(range(len(pairs)), key=lambda k: len(pairs[k][0]) + len(pairs[k][1]))
                out = np.zeros((len(pairs), 3), dtype=np.float32)
                for s in range(0, len(order), NLI_BATCH):
                    sel = order[s:s + NLI_BATCH]
                    enc = tok([tuple(pairs[k]) for k in sel], padding=True, truncation=True,
                              max_length=NLI_MAXLEN, return_tensors="pt")
                    enc = {k: v.to(dev) for k, v in enc.items()}
                    with torch.inference_mode():
                        pr = mdl(**enc).logits.float().softmax(-1).cpu().numpy()[:, perm]
                    for j, k in enumerate(sel):
                        out[k] = pr[j]
                return out

            _STATE["fn"] = _fn
        except Exception as e:                       # offline / deps missing -> guard
            print(f"[WARN] NLI indisponível ({type(e).__name__}: {e}). "
                  f"As células/scripts que dependem do NLI vão pular com aviso.")
            _STATE["fn"] = None

    fn = _STATE["fn"]
    if fn is None:
        return None
    return fn if return_probs else (lambda pairs: fn(pairs).argmax(1))

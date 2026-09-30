# `dataset/` — Processed PublicHearingBR Data Hub

The processed corpus is **not versioned** in git (the full MPNet embeddings occupy ~650 MB).
Rebuilding this data is **only necessary** if you intend to run feature extraction from scratch (`code/run_all.sh --from-scratch`). All downstream analysis scripts in `code/` can run immediately using the precomputed tables in `code/results/`.

---

## Generated Directory Structure

Running `init_data.py` populates this directory with:

```
dataset/
├── LDS/                                        # Raw HuggingFace LDS split (saved to disk)
├── NLI/                                        # Raw HuggingFace NLI split (saved to disk)
├── phrasal_data/
│   └── data_XXX/
│       └── phrases_XXX.csv                     # Split phrases (transcript, article)
├── opinions_data/
│   └── data_XXX/
│       └── opinions_XXX.csv                    # Key opinions, human audit & 12 LLM judge labels
├── MPNET_embeddings_phrasal_data/
│   └── data_XXX/
│       ├── transcript_embeddings_XXX.npy       # Sentence embeddings (n_phrases, 768)
│       └── article_embeddings_XXX.npy          # Article sentence embeddings
├── MPNET_opinion_embeddings/
│   └── data_XXX/
│       └── opinion_embeddings_XXX.npy          # Generated-opinion embeddings (n_opinions, 768)
├── windowed_data_<CFG>/                        # (Optional, --windows) Sliding-window text chunks
├── MPNET_embeddings_windowed_data_<CFG>/       # (Optional, --windows) Window embeddings
└── metrics_MPNET.csv                           # ROUGE & centroid/grounding cosine similarities
```

*Note: `XXX` represents the zero-padded hearing ID (`data_001` through `data_206`).*

---

## Build & Preparation

### 1. Requirements & Hardware Acceleration
Deep learning dependencies (`torch`, `transformers`, `datasets`, `huggingface_hub`) are required:

```bash
pip install -r ../code/requirements-full.txt
```

> [!NOTE]
> `init_data.py` automatically detects CUDA (NVIDIA) or MPS (Apple Silicon). On a laptop CPU, a full build takes ~1–2 hours; with GPU acceleration, it takes only a few minutes.

### 2. Execution

To build the full dataset required by the paper pipeline:

```bash
python init_data.py --models MPNET
```

> [!IMPORTANT]
> The default model if `--models` is omitted is `BERT`. You **must** specify `--models MPNET` for replication, as the geometric metrics in `code/src/` rely on contrastively trained multilingual MPNet embeddings.

### 3. Useful CLI Flags

* **Smoke test (fast check):**
  ```bash
  python init_data.py --models MPNET --limit 3
  ```
  *(Processes only the first 3 hearings in under a minute to verify environment setup).*
* **Force regeneration:**
  ```bash
  python init_data.py --models MPNET --force
  ```
* **Re-download raw splits:**
  ```bash
  python init_data.py --redownload
  ```
* **List available embedding models:**
  ```bash
  python init_data.py --list-models
  ```

---

## Build Verification

Verify that the processed corpus is ready and all 206 hearings are usable:

```bash
python ../code/src/dataset_readers.py
```
*Expected output:* `audiencias utilizaveis: 206`

The scripts in `code/src/` locate this directory automatically (as a sibling directory of `code/`). If you store the dataset in an alternative path, set:
```bash
export PHBR_DATA=/path/to/dataset
```

---

## Source and Data Governance

PublicHearingBR is constructed from official public records of the Brazilian Chamber of Deputies ([Fernandes et al., 2024](https://huggingface.co/datasets/unicamp-dl/PublicHearingBR)).

* **Purpose:** Exclusively used for academic research and hallucination detection benchmarking.
* **Privacy & LGPD:** In accordance with the *Ethics, Data Use and Limits of Use* statement of the paper and Brazilian General Data Protection Law (LGPD, Law 13.709/2018).
* **Redistribution:** The repository does not redistribute full raw transcripts; only the derived scores, verdicts, and LLM votes are versioned in `code/results/`.

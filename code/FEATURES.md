# Feature and evaluation map

All similarities use L2-normalised `sentence-transformers/paraphrase-multilingual-mpnet-base-v2`
embeddings. Larger detector scores mean more suspect. StandardScaler and balanced
logistic regression (`C=1`) are fitted on training hearings only in five-fold GroupKFold.

| Code column | Definition |
|---|---|
| `cos_g` | Maximum cosine similarity over the full transcript; use its negative for detection. |
| `cos_s` | Maximum over attributed-speaker sentences; use its negative for detection. |
| `best_other` | Maximum over all other matched transcript speakers. |
| `delta2` | `best_other - cos_s`; the untrained misattribution score Delta. |
| `share_attr` | Share of top-ten global cosine mass belonging to the attributed speaker. |
| `n_spk_sup` | Number of speakers with a sentence similarity at least 0.65. |
| `attr_in_sup` | Whether the attributed speaker meets the 0.65 threshold. |
| `rank_spk` | Descending rank of that speaker's best match, scaled to [0,1]. |
| `n_irm` | Number of labelled opinions attributed to that matched speaker in the hearing; no class labels enter the count. |
| `nli_s`, `nli_g` | Maximum entailment over the top-five cosine matches within speaker / globally. |
| `delta_n` | `nli_g - nli_s`; this is an NLI feature and must be excluded from zero-NLI controls. |

The feature-only cosine regression uses six columns: `cos_s`, `best_other`,
`share_attr`, `n_spk_sup`, `attr_in_sup`, `rank_spk`. The feature-only NLI model adds
`nli_s`, `nli_g`, `delta_n`. The combination/budget/queue models additionally use
`n_irm`. Differences between those model scores must not be attributed solely to
fold noise. The direct Delta control uses no fitted model and no NLI.

NLI checkpoint: `MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7`.
Feature generation truncates each text to 280 characters and the pair to 192 tokens,
with up to five sentence pairs per evidence pool. Overlapping pairs are cached once.

The CPU table is a component benchmark on the original four-vCPU machine, not
end-to-end latency or a current API price estimate. The timing script uses batches
of 32 / max length 128 for transcript embeddings and batches of 16 / max length 256
for the NLI timing probe. Opinion embedding, retrieval/index construction, fixed
LLM prompts and output tokens are outside the reported component totals. A local
remeasurement will vary with hardware and must not overwrite the reference table.

The evaluation target is the released four-chunk NLI verdict, not exhaustive
full-transcript verification. The 4,238 opinions are generated opinions in the NLI
experiment, distinct from the LDS reference-summary opinions. Main combination
results concern 3,630 matched-speaker opinions (408 positives).

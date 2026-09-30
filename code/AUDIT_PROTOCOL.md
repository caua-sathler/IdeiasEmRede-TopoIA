# Exploratory audit of 50 benchmark positives

## Population and sampling

The population is the 3,630 matched-speaker opinions, including 408 official NLI
positives. `audit_sample.py` draws 50 of those positives without replacement with
`numpy.random.default_rng(20260923)`, preserving the deterministic hearing/opinion
order. IDs have the form `data_XXX#i`, with a zero-based opinion row index.

## Evidence and annotation

The archived research record identifies two Claude annotation passes. Each received
an opinion, its attributed participant, the five most similar sentences from that
speaker, five global matches, speaker assignments, and neighbouring sentences around
the best matches. The generated sheet also contains similarity scores; this is not a
blinded human validation. The original research README explicitly records that no
human verification was performed in this audit. It is separate from the dataset's
original human labels, which remain the evaluation target.

The recorded categories are:

- **M:** content assigned to the wrong participant (misattribution).
- **S:** apparently supported/discussed by the attributed participant in the evidence.
- **D:** distortion of the content.
- **F:** fabrication (no item in the delivered passes received this category).

The preserved category/confidence fields from both passes are in
`results/audit_passes.csv`; their source-file SHA-256 hashes are in
`results/audit_provenance.json`. The original sheets contain named individuals and
verbatim evidence and remain outside the submission. `audit_sample.py` reconstructs
the evidence locally from PublicHearingBR. Exact model-version and generation-prompt
metadata are not stored in the category CSVs; the statistical reproduction below
reproduces the recorded annotations' agreement, not new model judgements.

## Aggregation and disagreements

No adjudicated category is imputed to disagreements. `audit_agreement.py` marks an
item as consensus only when the two recorded categories are identical. The resulting
counts are 12 M, 30 S, 3 D and 5 unresolved disagreements. Agreement is 45/50 and
Cohen's kappa is 0.807. This measures agreement between the model passes, not
inter-human reliability. The 12/50 consensus misattribution count is descriptive
of this exploratory sample, not an independently validated prevalence estimate.

## Reproduction

```bash
python src/audit_agreement.py
# To regenerate the local evidence sheet after preparing the dataset:
python src/audit_sample.py results/audit_local
```

The four-chunk NLI labels can differ from assessments using wider transcript context;
the audit does not replace, correct or filter the official evaluation labels.

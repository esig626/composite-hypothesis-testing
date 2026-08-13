# Codex project instructions

This repository contains research on finite blocklength minimax composite binary hypothesis testing.

## General rules

- Treat `manuscript/` as the authoritative source for notation, theorem statements, assumptions, and terminology.
- Do not silently alter theorem statements, quantifier order, assumptions, or notation.
- Preserve British English and the manuscript's information-theoretic terminology.
- Distinguish exact mathematical implications from heuristics, numerical evidence, and literature analogies.
- Do not claim novelty merely because a search fails to find an antecedent.
- Before editing the manuscript, identify the exact result or passage being changed and explain the mathematical reason.

## Literature and theorem search

When checking prior work:

1. Extract the mathematical claim independently of its prose wording.
2. Search several semantically distinct formulations.
3. Record serious candidates in `literature/literature_ledger.md`.
4. Record TheoremSearch queries in `literature/theoremsearch_queries.md`.
5. Inspect the source paper before asserting overlap or novelty.
6. Report assumptions, conclusion, theorem number where available, and the precise relation to the manuscript.

## Repository discipline

- Put theorem-level bookkeeping in `theory/`.
- Put literature-search records in `literature/`.
- Put numerical code and generated figures in `numerics/`.
- Put referee, collaborator, and external feedback in `reviews/`.
- Prefer small, reviewable commits.

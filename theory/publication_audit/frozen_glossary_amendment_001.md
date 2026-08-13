# Frozen glossary amendment 001 — error terminology

This amendment overrides any contrary wording in `frozen_glossary.md` and is frozen for the publication revision.

## Retired terminology

Do **not** use:

- `worst-case`;
- `worst case`;
- `worst-case Type I error`;
- `worst-case Type II error`.

## Canonical terminology

The Type I constraint is **uniform over the null class**. Preferred prose includes:

- `uniform Type I error probability constraint`;
- `the Type I error probability is bounded uniformly over the null class`.

The composite Type II criterion is defined by a supremum over the alternative class. Before attainment has been established, use:

- `supremum Type II error probability over the alternative class`;
- `Type II error probability, with the supremum taken over the alternative class`;
- where the surrounding definition makes the supremum clear, simply `composite Type II error probability` or `minimax Type II error probability`.

Use **maximum Type II error probability** only in a setting where the supremum is known to be attained. Do not silently replace a supremum by a maximum.

Likewise, use **maximum Type I error probability** only when attainment of the null-side supremum is known. In general, prefer `uniform Type I error probability`.

## Mathematical definitions

The definitions remain

\[
\alpha_n(\varphi_n;\mathcal P)
:=\sup_{P\in\mathcal P}\mathbb E_{P^n}[\varphi_n],
\]

and

\[
\beta_n(\varphi_n;\mathcal Q)
:=\sup_{Q\in\mathcal Q}\mathbb E_{Q^n}[1-\varphi_n].
\]

The terminology above must respect the distinction between `\sup` and `\max` throughout the manuscript.

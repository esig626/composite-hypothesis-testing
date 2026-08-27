# Frozen notation and terminology glossary

## Status

This glossary is the working notation and terminology standard for the publication revision of `manuscript/Manuscript.tex`.

The entries below are **frozen** for the theorem-by-theorem revision unless one of the following occurs:

1. a genuine mathematical inconsistency is found;
2. a later theorem requires an unavoidable distinction that the glossary does not support;
3. the notation creates a concrete ambiguity in a proof.

Changes should be made here first and only then propagated to the manuscript. Editorial preference alone is not sufficient to introduce a competing symbol later.

---

# 1. Hypothesis-testing notation

## Sample space and hypothesis classes

- `(\mathcal X,\mathcal F)`: measurable sample space.
- `\mathcal P`: null class of probability laws.
- `\mathcal Q`: alternative class of probability laws.
- `P\in\mathcal P`: generic null law.
- `Q\in\mathcal Q`: generic alternative law.
- `P^n:=P^{\otimes n}` and `Q^n:=Q^{\otimes n}`: product laws.
- `X^n=(X_1,\ldots,X_n)`: observed sample.

These symbols are canonical and are not to be renamed.

## Tests and errors

- `\mathsf T_n`: class of measurable randomised tests `\varphi_n:\mathcal X^n\to[0,1]`.
- `\varphi_n(x^n)`: probability of deciding the alternative after observing `x^n`.
- `\alpha_n(\varphi_n;\mathcal P)`: worst-case Type I error,
  \[
  \alpha_n(\varphi_n;\mathcal P)
  :=\sup_{P\in\mathcal P}\mathbb E_{P^n}[\varphi_n].
  \]
- `\beta_n(\varphi_n;\mathcal Q)`: worst-case Type II error,
  \[
  \beta_n(\varphi_n;\mathcal Q)
  :=\sup_{Q\in\mathcal Q}\mathbb E_{Q^n}[1-\varphi_n].
  \]

Use **Type I error** and **Type II error**. Use **worst-case** adjectivally and **worst case** as a noun phrase.

## Exponentially decaying Type I constraint

- `r>0`: exponential Type I rate.
- `\Phi_n(r;\mathcal P)`: admissible tests,
  \[
  \Phi_n(r;\mathcal P)
  :=\{\varphi_n\in\mathsf T_n:\alpha_n(\varphi_n;\mathcal P)\le e^{-nr}\}.
  \]
- `\beta_n^\star(r;\mathcal P,\mathcal Q)`: minimax Type II error,
  \[
  \beta_n^\star(r;\mathcal P,\mathcal Q)
  :=\inf_{\varphi_n\in\Phi_n(r;\mathcal P)}
  \beta_n(\varphi_n;\mathcal Q).
  \]

This is the central finite-blocklength quantity.

## Simple hypotheses

Do **not** use the subscript `\mathrm{sp}`.

For fixed laws `P,Q`, define the simple-hypothesis value by overloading the same symbol:

\[
\beta_n^\star(r;P,Q)
:=
\beta_n^\star(r;\{P\},\{Q\}).
\]

When needed explicitly,

\[
\beta_n^\star(r;P,Q)
=
\inf_{\substack{\varphi_n\in\mathsf T_n\\
\mathbb E_{P^n}[\varphi_n]\le e^{-nr}}}
\mathbb E_{Q^n}[1-\varphi_n].
\]

The argument types make the simple and composite cases unambiguous. Do not introduce a second symbol for the same optimisation problem.

## Fixed Type I level

- `\varepsilon\in(0,1)`: fixed Type I level.
- `\Phi_{n,\varepsilon}(\mathcal P)`: tests satisfying `\alpha_n\le\varepsilon`.
- `\beta_{n,\varepsilon}^\star(\mathcal P,\mathcal Q)`: corresponding minimax Type II error.
- For fixed `P,Q`, write `\beta_{n,\varepsilon}^\star(P,Q)` rather than introducing a simple-case subscript.

---

# 2. Rényi and Kullback--Leibler quantities

## Hellinger integral

For `\lambda>0`, `\lambda\neq1`, and laws `Q,P` dominated by `\mu` with densities `q,p`, define

\[
Z_\lambda(Q,P)
:=
\int q^\lambda p^{1-\lambda}\,d\mu.
\]

Canonical term: **order-`\lambda` Hellinger integral**.

Do not alternate among “Hellinger affinity”, “Chernoff functional”, “Rényi affinity”, or other names unless discussing an external source that uses that terminology.

## Rényi divergence

\[
D_\lambda(Q\|P)
:=
\frac{1}{\lambda-1}\log Z_\lambda(Q,P).
\]

The orientation is always written explicitly as `Q\|P`.

## KL divergence

- `D(Q\|P)`: Kullback--Leibler divergence from `Q` to `P`.

Use **KL divergence** in prose after the first definition.

## Classwise minima

The canonical notation is

\[
D_\lambda(\mathcal Q\|\mathcal P)
:=
\inf_{Q\in\mathcal Q}\inf_{P\in\mathcal P}
D_\lambda(Q\|P),
\]

and

\[
D(\mathcal Q\|\mathcal P)
:=
\inf_{Q\in\mathcal Q}\inf_{P\in\mathcal P}
D(Q\|P).
\]

Similarly,

\[
D(\mathcal P\|\mathcal Q)
:=
\inf_{P\in\mathcal P}\inf_{Q\in\mathcal Q}
D(P\|Q)
\]

when the reverse orientation is required in the fixed-level regime.

### Frozen rule

Do **not** introduce global aliases such as

- `d_\lambda`,
- `d_1`,
- `D_\lambda^\star`,

for these classwise minima.

Local one-line shorthand inside a proof is allowed only if it materially shortens the argument and is discarded at the end of the proof.

### Preferred prose

Use:

- “the minimum Rényi divergence from `\mathcal Q` to `\mathcal P`” when attainment is known;
- “the infimum Rényi divergence from `\mathcal Q` to `\mathcal P`” when attainment has not yet been established;
- “the minimum KL divergence from `\mathcal Q` to `\mathcal P`”; and
- “critical rate” after the value `D(\mathcal Q\|\mathcal P)` has been identified operationally.

Do not use:

- “directed composite Rényi separation”;
- “directed composite Kullback--Leibler separation”.

The divergence notation already records the direction.

## Critical rate

When a dedicated symbol is useful, use

\[
r_c:=D(\mathcal Q\|\mathcal P).
\]

Do not use `r_{\rm crit}` and `D(\mathcal Q\|\mathcal P)` as competing names throughout the paper. Introduce `r_c` only in sections where repeated use genuinely improves readability.

---

# 3. Laws versus densities

The law classes remain `\mathcal P` and `\mathcal Q` everywhere.

Do **not** distinguish law classes and density classes solely by changing `\mathcal` to `\mathscr`.

If a `\sigma`-finite measure `\mu` dominates the relevant laws, define the density representations locally by

\[
\mathcal D_\mu(\mathcal P)
:=
\left\{\frac{dP}{d\mu}:P\in\mathcal P\right\},
\qquad
\mathcal D_\mu(\mathcal Q)
:=
\left\{\frac{dQ}{d\mu}:Q\in\mathcal Q\right\}.
\]

Use lowercase `p,q` for individual densities.

- `\mu`: dominating measure.
- `\mathsf D_\mu`: all probability densities with respect to `\mu`, when that ambient set is actually needed.

`\mathsf D_\mu` and `\mathcal D_\mu(\mathcal P)`, `\mathcal D_\mu(\mathcal Q)` are local to the dominated-space section and proofs. They are not part of the paper-wide conceptual notation.

---

# 4. Rényi-minimising pair and likelihood-ratio statistic

For fixed `0<\lambda<1`, when the classwise infimum is attained, write

\[
P_\lambda^\star\in\mathcal P,
\qquad
Q_\lambda^\star\in\mathcal Q,
\]

with

\[
D_\lambda(Q_\lambda^\star\|P_\lambda^\star)
=
D_\lambda(\mathcal Q\|\mathcal P).
\]

Canonical prose:

- **Rényi-minimising pair** on first use;
- **selected pair** thereafter.

Use **Rényi projection** only when discussing projection geometry or external projection literature. Do not use **joint Rényi projection** as routine terminology for the selected pair.

## Single-sample score

The canonical symbol is

\[
\ell_\lambda
:=
\log\frac{dQ_\lambda^\star}{dP_\lambda^\star},
\]

with the appropriate extended-real definition when supports differ.

Canonical prose:

- **log-likelihood ratio of the selected pair**;
- **extended log-likelihood ratio** when the `\pm\infty` values matter.

Do not use `h_\lambda^\star` in the revised manuscript.

## Block score

Write

\[
L_{n,\lambda}
:=
\sum_{i=1}^n\ell_\lambda(X_i)
\]

whenever the ordinary sum is almost surely well defined. Any exceptional-set convention needed for the extended-real case is introduced locally in the measurable-space theorem/proof.

Do not use `S_{n,\lambda}^\star` in the revised manuscript.

## Hellinger value at the selected pair

Avoid carrying a global symbol `z_\lambda^\star` beyond the proof where it is useful.

When needed locally,

\[
z_\lambda
:=Z_\lambda(Q_\lambda^\star,P_\lambda^\star)
\]

is acceptable. The star on `z` is unnecessary because the selected pair is already starred.

---

# 5. Uniform inequalities and threshold tests

The two key inequalities generated by the selected pair are called

**uniform exponential-moment inequalities**.

Do not use **uniform Rényi inequalities** unless the context explicitly concerns their Rényi-divergence value.

## Analytical threshold

For the threshold obtained directly from the exponential-moment bound, use

\[
\tau_{n,\lambda}(r)
:=
\frac{n\left[r-(1-\lambda)D_\lambda(\mathcal Q\|\mathcal P)\right]}{\lambda}
\]

in the selected-pair application.

In an abstract theorem with a generic constant `D`, use the same pattern with `D` in place of the classwise minimum.

Do not use the superscript `\min`.

## Randomised threshold family

For a fixed selected score `L_{n,\lambda}`, define

\[
\psi_{n,\lambda;\tau,\eta}
:=
\mathbf 1\{L_{n,\lambda}>\tau\}
+
\eta\,\mathbf 1\{L_{n,\lambda}=\tau\},
\qquad 0\le\eta\le1.
\]

This is the canonical full notation.

Inside a subsection where `n` and `\lambda` have been fixed explicitly, shortening to `\psi_{\tau,\eta}` is allowed.

Do not use `\psi_{n,\tau,\eta}^{\lambda,\star}`.

## Calibrated threshold

Use

\[
\tau_{n,\lambda}^{\rm cal}(r),
\qquad
\eta_{n,\lambda}^{\rm cal}(r),
\]

for a calibrated representation when parameter notation is necessary.

The primary mathematical object is the induced test function, not the parameter pair.

---

# 6. Hoeffding exponent notation

## Hoeffding objective

Keep

\[
F_r(\lambda;P,Q)
:=
\frac{1-\lambda}{\lambda}
\left[D_\lambda(Q\|P)-r\right],
\qquad 0<\lambda<1.
\]

Canonical term: **Hoeffding objective**.

Do not repeatedly brand this as the “Rényi--Hoeffding functional”.

## Reparametrisation

The change of variables

\[
\rho=\frac{1-\lambda}{\lambda}
\]

and any corresponding `G_r(\rho;P,Q)` notation are **proof-local**. They are not global notation.

## Saddle point

At rate `r`, write

\[
\lambda_r^\star,\qquad P_r^\star,\qquad Q_r^\star
\]

for a saddle order and saddle pair.

Canonical prose:

- **saddle point of the Hoeffding objective**;
- **saddle pair** when only the distributions are being referenced.

Do not repeatedly use the phrase **Rényi--Hoeffding saddle point**.

## Tilted law

For a fixed pair `P,Q`, define

\[
R_\lambda^{P,Q}(x)
:=
\frac{Q(x)^\lambda P(x)^{1-\lambda}}
{Z_\lambda(Q,P)}.
\]

This is the canonical tilted-law notation.

At a saddle point, write

\[
R_r^\star
:=
R_{\lambda_r^\star}^{P_r^\star,Q_r^\star}.
\]

Do not use several interchangeable forms such as `R_s`, `R_\rho`, and `R_r^\star` for the same construction.

## Exact exponent

Keep

\[
E_{\rm H}(r;\mathcal P,\mathcal Q)
\]

for the exact subcritical Hoeffding Type II error exponent.

For simple hypotheses, overload the arguments:

\[
E_{\rm H}(r;P,Q)
:=
E_{\rm H}(r;\{P\},\{Q\}).
\]

Do not introduce `E_{\rm H}^{\rm sp}`.

---

# 7. Calibration notation

The calibration section is conceptually about the best test in the threshold family generated by a fixed score.

- `\beta_{n,\lambda}^{\rm cal}(r;\mathcal P,\mathcal Q)`: restricted minimax Type II error over randomised upper-threshold tests based on `L_{n,\lambda}`. Keep this symbol if the calibration result remains in the main paper.
- `\mathcal C_{n,\lambda}(r)`: **do not freeze as global notation**. Prefer defining the restricted optimisation directly. Retain a feasible-set symbol only if it materially shortens multiple proofs.
- `\Gamma_{n,\tau,\eta}^{\lambda}` and `\widetilde\Gamma_{n,\tau,\eta}^{\lambda}`: **not approved as frozen notation**. These quantities must be reconsidered theorem-by-theorem. If both survive, they require simpler names and a clear operational interpretation. They should not be propagated automatically during the publication revision.

Canonical prose:

- **calibrated threshold test**;
- **restricted optimum over threshold tests based on the selected log-likelihood ratio**.

Avoid:

- “direct calibration of the projected log--likelihood ratio”;
- “projected calibration”.

---

# 8. Exact reduction and robust-testing language

Use standard robust-testing terminology.

## Approved terms

- **least favourable pair**: only when the operational worst-case property is actually established.
- **exact reduction to a simple pair**: when the composite minimax value equals the simple-hypothesis value for a selected pair.
- **stochastic ordering of the selected log-likelihood ratio**: for the tail inequalities currently called “projected ordering”.
- **monotone likelihood ratio**: standard term for the one-parameter family section.
- **endpoint pair**: for the adjacent null/alternative endpoints in an ordered parametric family.

## Terms to remove

- “exact closure”;
- “projected ordering”;
- “projected score ordering”;
- “exact composite closure”.

If a selected pair has a special property, state that property directly rather than branding it with another manuscript-specific term.

---

# 9. Theorem, proposition, lemma, corollary, and naming policy

## Theorem titles

Default rule: **our own results are untitled**.

Use

```latex
\begin{theorem}
...
\end{theorem}
```

rather than

```latex
\begin{theorem}[Descriptive title]
...
\end{theorem}
```

The surrounding paragraph should explain what the result does.

A title is retained only when it is a genuinely standard named result being quoted or when the title is indispensable for navigation.

## Result hierarchy

- **Theorem**: a principal result on which later sections materially depend.
- **Proposition**: a substantial but secondary standalone result.
- **Lemma**: a technical statement used primarily to prove another result.
- **Corollary**: a direct consequence requiring little new argument.
- **Remark**: interpretation, limitation, comparison, or consequence that does not warrant a formal result.

Do not promote a result merely because it has a long proof.

---

# 10. Approved prose and banned jargon

## Preferred language

Use direct mathematical descriptions such as:

- “a pair minimising the order-`\lambda` Rényi divergence over the two classes”;
- “the log-likelihood ratio of the selected pair”;
- “the two uniform exponential-moment inequalities”;
- “a threshold test based on that log-likelihood ratio”;
- “the minimum KL divergence from `\mathcal Q` to `\mathcal P`”;
- “the critical rate”;
- “the exact Type II error exponent”;
- “a saddle point of the Hoeffding objective”;
- “calibration within the fixed threshold family”;
- “exact reduction to a simple pair”.

## Avoid unless required by an external source or a precise geometric discussion

- “directed composite Rényi separation”;
- “directed composite KL separation”;
- “joint Rényi projection”;
- “projected statistic”;
- “projected log--likelihood ratio”;
- “projected threshold”;
- “projected reverse Rényi construction”;
- “Rényi--Hoeffding saddle point” as a repeated label;
- “exact closure”;
- “projected ordering”;
- “analytical, threshold, and projection losses” unless those losses are formally defined quantities.

The editorial rule is: **if ordinary probability/statistics language says the same thing precisely, use the ordinary language.**

---

# 11. Orientation rules

Because the paper uses two different KL orientations in different operational regimes, the following is non-negotiable.

## Exponentially decaying Type I constraint

The critical rate is in the orientation

\[
D(\mathcal Q\|\mathcal P).
\]

## Fixed Type I level

The Chernoff--Stein exponent is in the orientation

\[
D(\mathcal P\|\mathcal Q).
\]

Never replace either by an unoriented phrase such as “the KL distance between the classes”.

Every theorem, proof, abstract sentence, and contribution statement must preserve the orientation explicitly.

---

# 12. Local-notation rule

A proof may introduce temporary notation when all three conditions hold:

1. the symbol materially shortens the proof;
2. its meaning is defined immediately before use;
3. it disappears at the end of that proof or subsection.

Temporary notation must not leak into later theorem statements without first being added to this glossary.

Examples of acceptable local notation include:

- `\xi=P_\lambda^\star+Q_\lambda^\star` in the variable-support proof;
- Radon--Nikodym densities relative to `\xi`;
- exceptional support sets;
- `\rho` and `G_r` inside the minimax reparametrisation;
- finite score levels `v_1<\cdots<v_m` inside the calibration proof.

---

# 13. Publication-revision protocol

For each theorem/proposition/lemma/corollary, the revision order is fixed:

1. explain the mathematical content in plain language;
2. identify its role in the paper;
3. rewrite the statement using this glossary;
4. audit every assumption and quantifier;
5. simplify the proof and remove disposable notation;
6. only then run an external theorem search;
7. external theorem search is restricted to the TheoremSearch archive/API unless explicitly reopened;
8. use archive results only to:
   - weaken assumptions,
   - strengthen conclusions,
   - replace bespoke arguments by standard theorems,
   - simplify proofs,
   - or derive worthwhile corollaries;
9. do not use theorem search as a novelty search during this publication pass;
10. do not modify the manuscript until the revised statement/proof has been approved.

---

# 14. Frozen decisions summary

The following choices are frozen:

1. `\mathcal P,\mathcal Q` denote law classes.
2. Density representations use `\mathcal D_\mu(\mathcal P)` and `\mathcal D_\mu(\mathcal Q)` locally; `\mathscr P,\mathscr Q` are retired.
3. `D_\lambda(\mathcal Q\|\mathcal P)` is the sole global notation for the classwise Rényi infimum; `d_\lambda` and `D_\lambda^\star` are retired as global aliases.
4. `D(\mathcal Q\|\mathcal P)` and `D(\mathcal P\|\mathcal Q)` retain their distinct orientations.
5. Simple-hypothesis quantities overload the composite notation by using `P,Q` as arguments; the subscript `\mathrm{sp}` is retired.
6. The selected order-`\lambda` pair is `(P_\lambda^\star,Q_\lambda^\star)`.
7. Its single-sample log-likelihood ratio is `\ell_\lambda`; `h_\lambda^\star` is retired.
8. The block score is `L_{n,\lambda}`; `S_{n,\lambda}^\star` is retired.
9. The analytical threshold is `\tau_{n,\lambda}(r)`; the superscript `\min` is retired.
10. The randomised threshold family is `\psi_{n,\lambda;\tau,\eta}`.
11. `F_r(\lambda;P,Q)` remains the Hoeffding objective.
12. Tilted laws use `R_\lambda^{P,Q}` and `R_r^\star` at a saddle point.
13. The exact exponent uses `E_{\rm H}` for both composite and simple cases, distinguished by its arguments.
14. The phrases “directed composite separation”, “exact closure”, and routine uses of “projected” as an adjective are retired.
15. Our own theorem environments are untitled by default.
16. TheoremSearch is the only external theorem archive used during theorem-by-theorem strengthening unless this rule is explicitly reopened.

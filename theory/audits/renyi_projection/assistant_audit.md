# Independent audit of Rényi projection strengthening candidates

This note records an independent mathematical audit of selected strengthening candidates from `theory/renyi_projection_strengthening_candidates.md`. It is intentionally separate from the Codex-generated search note.

## S1 — direct attainment and support condition

The direct-attainment part is a genuine simplification: once a positive joint maximiser `(q^*_lambda,p^*_lambda)` is assumed to exist, weak compactness is no longer needed in the variational part of the proof.

However, in the current dominated-density framework the proposed replacement

\[
R\{p^*_\lambda=q^*_\lambda=0\}=0
\]

for

\[
R\ll P^*_\lambda+Q^*_\lambda
\]

is not a strictly weaker support assumption. Since every class law is already dominated by `mu` and `P^*_lambda+Q^*_lambda` has density `p^*_lambda+q^*_lambda` with respect to `mu`, the null sets of the selected sum are precisely subsets of the joint-zero region, modulo `mu`-null sets. Thus, within the present framework,

\[
R\{p^*_\lambda=q^*_\lambda=0\}=0
\quad\Longleftrightarrow\quad
R\ll P^*_\lambda+Q^*_\lambda.
\]

So S1 should be described as weakening the **existence hypothesis** from weak compactness to direct attainment, while the support premise is best viewed as a proof-exact reformulation of the existing domination condition.

## S6 — order stability can likely drop full support

The proposed finite-alphabet continuity/stability result appears stronger than stated. For a finite alphabet and a compact interval `I \subset (0,1)`, the map

\[
(\lambda,Q,P)\mapsto Z_\lambda(Q,P)=\sum_x Q(x)^\lambda P(x)^{1-\lambda}
\]

is jointly continuous on `I x Delta x Delta`, including boundary points where some coordinates vanish, because both exponents remain strictly positive and bounded away from zero.

Therefore, for compact classes `P,Q`, Berge's maximum theorem should imply:

1. continuity of
   \[
   v(\lambda)=\max_{Q\in\mathcal Q,\,P\in\mathcal P} Z_\lambda(Q,P),
   \]
2. nonempty compact-valued upper hemicontinuity of the argmax correspondence,
3. continuity of the selected pair whenever the maximiser is unique.

A uniform positive lower bound on every coordinate is therefore probably unnecessary for S6 itself. Full support becomes relevant later for differentiability formulas involving logarithms, endpoint limits, and projected log-likelihood ratios, but not for continuity of the value/argmax on a compact subinterval of `(0,1)`.

This is worth proving in the strongest boundary-inclusive finite-alphabet form.

## S4 — simultaneous variational certificate

This is potentially the most substantive strengthening.

Under strict positivity of the selected pair, the weighted geometric mean is jointly concave and its tangent inequality gives, pointwise,

\[
q^\lambda p^{1-\lambda}
\le
(q^*)^\lambda(p^*)^{1-\lambda}
+\lambda(q-q^*)(q^*)^{\lambda-1}(p^*)^{1-\lambda}
+(1-\lambda)(p-p^*)(q^*)^\lambda(p^*)^{-\lambda}.
\]

After integration, if the two coordinatewise supporting inequalities hold for every feasible `Q` and `P`, the right-hand correction terms are nonpositive, giving global joint optimality of `(Q^*,P^*)`.

Thus, under conditions ensuring the displayed derivatives are integrable, the two one-sided moment/supporting inequalities should be not only necessary but jointly sufficient for optimality. This would convert the current first-order conditions into a clean variational characterisation.

The next proof task should be:

1. prove the full-support version rigorously;
2. identify the exact equality conditions;
3. determine whether the argument extends to boundary points using a supergradient formulation compatible with the existing varying-support derivative lemma.

## Current priority

1. **S4** — strongest candidate for a genuinely stronger structural theorem.
2. **Boundary-inclusive S6** — likely a clean and useful order-stability corollary.
3. **Corrected S1** — useful modularisation of existence, but the support hypothesis should not be advertised as weaker in the current dominated setting.

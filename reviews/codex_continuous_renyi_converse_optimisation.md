# Codex task: continuous Rényi-order optimisation for the numerical converse

Work on branch `codex/continuous-renyi-converse-optimisation`.

Read `AGENTS.md` first and obey it. Do not edit `manuscript/`.

## Objective

Refine the numerical converse curves by replacing the current finite Rényi-order search with a continuous one-dimensional optimisation over the Rényi order. Reuse the existing numerical results as aggressively as possible. Do not rerun the expensive finite-sample LPs or the calibrated achievability calculations unless a small diagnostic check is required.

The existing calculations are the starting point, not disposable intermediate data.

Relevant files include

- `numerics/scripts/nonordered_bruno_regimes.py`
- `numerics/scripts/affine_ternary_lp.py`
- `numerics/data/nonordered_bruno_regimes.csv`
- `numerics/data/nonordered_bruno_renyi_cache.json`
- `numerics/nonordered_bruno_regimes_audit.md`

The current converse cache already contains a dense deterministic mesh in
`a=(lambda-1)/lambda` with 167 finite orders greater than one, together with the order-infinity limit. Use those values to locate promising intervals. Do not recompute that mesh.

## Scope

1. Leave the existing minimax LP values unchanged.
2. Leave the existing calibrated achievability values unchanged.
3. Refine only the Rényi-order optimisation used by the converse.
4. Preserve the existing forward and reverse converse branches separately. Do not silently decide which branch belongs in the manuscript. Report both, together with their maximum, so the manuscript audit can make that decision separately.
5. Do not edit `manuscript/`.

## Numerical formulation

Use the bounded variable

`a=(lambda-1)/lambda`, so `a in (0,1)` and `lambda=1/(1-a)`.

For each blocklength `n`, Type I constraint `epsilon`, and converse branch, maximise the finite-sample converse exponent

`E(a) = a * [log(1/epsilon) - n D_lambda(class_1 || class_0)]_+`

with the appropriate directed composite Rényi divergence for that branch. Convert the optimised exponent to the corresponding Type II lower bound only after the optimisation.

Optimising in `a` rather than directly in `lambda` keeps the outer domain bounded and gives direct access to the order-infinity endpoint.

## Cost-control strategy

The continuous optimisation must use the existing cache as a warm start.

For each `(n, regime, branch)`:

1. Evaluate the converse objective on the already cached `a` mesh only. Do not recompute the cached composite divergences.
2. Identify every plausible local maximum from the cached objective values, including the best mesh point and neighbouring intervals. Include the endpoint limits `a downarrow 0` and `a uparrow 1` where relevant.
3. Refine only those candidate intervals with a bounded scalar optimisation in `a`.
4. At a new trial `a`, compute the required composite Rényi divergence using the nearest cached projected pair as the primary initial point for the inner `(s,t)` optimisation.
5. Also use the projected pairs at the adjacent cached orders as inexpensive secondary starts when available.
6. Use the existing full multistart `minimise_over_classes` routine only as a validation/polish step at the final candidate maximiser, or when the warm-started inner optimisation is demonstrably unstable. Do not invoke the full 13-by-13 scout search at every outer-function evaluation.
7. Cache every newly evaluated `(branch, lambda)` projection so that all blocklengths and both Type I regimes can reuse it. The composite Rényi divergence depends on `lambda` and the classes, not on `n` or `epsilon`.
8. Check whether many blocklengths select the same or nearby `lambda`. Reuse refined divergence evaluations across all rows.
9. Checkpoint new work incrementally so an interrupted run does not lose computed projections.

A feasible evaluated pair always gives a composite divergence no smaller than the true infimum, hence a conservative converse value. Nevertheless, the final selected order for each distinct local maximiser must be polished with the existing global-screening routine so that the reported refinement is numerically credible.

## Validation

Do not overwrite the existing CSV initially. Produce new columns or a separate comparison file containing at least

- legacy mesh converse
- continuous-refined converse
- legacy selected order
- continuous-refined selected order
- forward branch values and orders
- reverse branch values and orders
- absolute improvement from continuous refinement

Required checks:

1. The refined converse must be no smaller than the legacy mesh converse, up to numerical tolerance.
2. Each individual converse branch and their displayed maximum must remain below the stored numerical value of `beta_n^star` up to the established solver tolerance. Report any violation instead of clipping it.
3. Revalidate the final inner Rényi projections at every distinct refined maximising order with the existing multistart projection routine.
4. Compare the refined result against the nearest cached mesh points and verify that the scalar optimiser has not converged to an inferior local point.
5. Preserve the order-infinity candidate explicitly.

Do not rerun the 1--300 semi-infinite LP calculations merely to perform these checks. Use the committed CSV values.

## Figures

Trace which committed numerical figures use the converse values produced by `nonordered_bruno_regimes.py`. Regenerate only figures whose converse curve changes. Do not regenerate unrelated figures.

Keep the old figure/data outputs available for comparison until validation is complete.

## Audit report

Create `numerics/continuous_converse_optimisation_audit.md` containing

- the exact optimisation procedure
- how the cached mesh and cached projected pairs were reused
- the number of new Rényi orders/projections evaluated
- runtime for the refinement only
- maximum and median improvement in the converse bound
- the blocklength/regime with the largest improvement
- changes in the selected Rényi orders
- separate results for the forward and reverse branches
- any cases where the order-infinity endpoint is selected
- validation tolerances and the largest observed converse-minus-minimax violation
- whether the refined curves materially change any manuscript statement

The report must clearly distinguish mathematical validity from numerical evidence.

## Acceptance criteria

The task is complete only if

1. continuous refinement is implemented rather than merely using a denser fixed mesh;
2. existing cached projections and CSV results are reused as warm starts;
3. the expensive minimax LP and achievability calculations are not recomputed wholesale;
4. every refined final order is validated with the existing projection routine;
5. all numerical checks above pass or any failures are explicitly documented;
6. affected figures are regenerated only after validation;
7. `manuscript/` remains untouched.

Commit the implementation, comparison data, regenerated affected figures, and audit report in small reviewable commits. In the final response, report the numerical improvement over the old converse curves and identify any manuscript text that will need revision, but do not edit that text.
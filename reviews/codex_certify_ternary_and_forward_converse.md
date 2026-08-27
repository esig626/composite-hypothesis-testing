# Codex task

Work on branch `codex/certify-ternary-and-forward-converse`.

Read `AGENTS.md` first and obey it. Do not edit `manuscript/`.

## Objective

Produce a reproducible numerical certification for the manuscript's ternary calculations and for both finite sample converse branches. Reuse all existing calculations, caches, projections, LP outputs, and checkpoints as warm starts wherever possible. Do not rerun an expensive calculation merely because the old implementation used a discrete order mesh.

This task must cover all three numerical situations that are now relevant.

1. The existing nonordered ternary Hoeffding example in the manuscript, including its reported KL separation, saddle order, projected pair, exponent, and the blocklength 20 gap table.
2. The supercritical strong converse calculation for the same nonordered ternary classes under an exponentially decaying Type I constraint, including continuous optimisation of both the `Q||P` and `P||Q` converse branches.
3. The already computed fixed `epsilon=0.01` and subexponential `epsilon=1/n` nonordered affine ternary experiment, importing and preserving the validated continuous order optimisation from branch `codex/continuous-renyi-converse-optimisation` while preserving the Fano/data-processing additions now present on `main`.

The result must be an auditable numerical record suitable for a later Numerical Methods appendix.

## Repository state and reuse requirements

All open pull requests were merged before this branch was created. Treat the current branch base as authoritative.

A previous validated refinement exists on branch

`codex/continuous-renyi-converse-optimisation`

with remote head previously reported as `30654fb`.

That branch contains a continuous outer Reni order optimiser, a projection cache, comparison data, regenerated converse figures, and `numerics/continuous_converse_optimisation_audit.md`.

Do not blindly merge or cherry-pick that branch because `main` now also contains the Fano/data-processing curve from the formerly open PR. Selectively reuse the implementation and cached numerical data. Preserve the current Fano-aware plotting logic and current `main` outputs.

Before computing anything expensive, search the complete repository, branches, and reachable history for existing data or code for the exact ternary classes and rates below. If an existing result can be imported or used as a warm start, do so.

## Ternary classes

Use exactly

`P0 = [0.327, 0.418, 0.255]`

`P1 = [0.563, 0.266, 0.171]`

`Q0 = [0.143, 0.357, 0.500]`

`Q1 = [0.379, 0.205, 0.416]`

with

`P_s = (1-s) P0 + s P1`

`Q_t = (1-t) Q0 + t Q1`

for `s,t in [0,1]`.

The current manuscript reports the following values. Treat them as warm starts and values to certify, not as assumptions.

`D(Qclass || Pclass) ~= 0.094878`

For the subcritical choice

`r_minus = 0.35 * D(Qclass || Pclass) ~= 0.0332073`

it reports

`lambda_star ~= 0.601438`

`s_star = 0`

`t_star ~= 0.602843`

`E_H ~= 0.0153133`.

At `n=20` it reports

`beta_minimax ~= 0.026419`

`beta_calibrated_projected ~= 0.033633`

`beta_projected_at_tau_min ~= 0.236620`

`bound_slack_rejection ~= 0.399134`

`raw_projected_exponential_bound ~= 0.736191`.

For the supercritical strong converse calculation use

`r_plus = 1.5 * D(Qclass || Pclass)`.

Legacy calculations previously used values near

`lambda ~= 1.224`

`D_lambda(Qclass || Pclass) ~= 0.116`

and a reverse strong converse exponent near `0.00476`.

These are only warm starts. Recompute and certify the final values continuously.

## Part A

## Certify the subcritical ternary saddle calculation

Recompute the directed composite KL separation over the full square `(s,t) in [0,1]^2` using a global screen followed by local refinement. Use the existing reported minimiser as a warm start if available.

Then certify

`max_{0<lambda<1} min_{s,t} ((1-lambda)/lambda) * (D_lambda(Q_t||P_s) - r_minus)`.

Do not use a fixed order mesh as the final optimisation.

Use the existing manuscript values to locate the candidate region, then perform continuous one dimensional refinement in the order variable. At each new order, warm start the inner two parameter projection from the nearest validated projected pair. Cache every new projection.

Every final candidate maximising order must be rechecked using a full global projection screen over `(s,t)`, not only a local warm start. Repeat the outer optimisation if the global polish moves the inner minimum enough to move the outer maximiser.

Also numerically evaluate the equivalent min max form at the certified saddle pair sufficiently accurately to verify the saddle value and the stated pair. Report whether the pair is unique numerically. Do not convert numerical uniqueness into a theorem.

Recompute the complete `n=20` gap table from the actual test definitions. Reuse `affine_ternary_lp.py`, any existing LP checkpoint, and any existing projected-test code. Do not infer table entries from rounded manuscript values.

For every table entry store the unrounded numerical value, the Type I error actually attained, the class parameters attaining the Type I and Type II envelopes, and the numerical tolerance used.

## Part B

## Certify the strong converse ternary calculation

Use the same classes and

`epsilon_n = exp(-n r_plus)`.

For the reverse branch compute

`D_lambda(Qclass || Pclass) = min_{s,t} D_lambda(Q_t || P_s)`

and optimise continuously over `lambda>1`

`beta_reverse(n) = 1 - exp( - n * sup_{lambda>1} ((lambda-1)/lambda) * [r_plus - D_lambda(Qclass || Pclass)]_+ )`.

For the forward branch compute

`D_lambda(Pclass || Qclass) = min_{s,t} D_lambda(P_s || Q_t)`

and optimise the valid Bruno-style branch

`beta_forward(n) = sup_{lambda>1} (1-epsilon_n)^(lambda/(lambda-1)) * exp(-n D_lambda(Pclass || Qclass))`.

It is preferable to optimise in

`a=(lambda-1)/lambda in (0,1)`

with

`lambda=1/(1-a)`.

Then the forward log objective is

`log_beta_forward(a) = log(1-epsilon_n)/a - n D_lambda(Pclass || Qclass)`.

Keep the two branches separate and report their maximum as a third quantity. Never apply the reverse strong converse conversion to the forward divergence.

Use the legacy strong converse values listed above as warm starts. Search repository history and other branches for any previously computed strong converse ternary curve, selected orders, class projections, or minimax values before launching new work.

If exact minimax Type II values for this supercritical ternary example already exist anywhere in reachable history or another branch, reuse them and verify them rather than recomputing them.

If they do not exist, use the existing semi-infinite ternary LP solver with checkpointing and cross-blocklength warm starts. Before launching a full blocklength sweep, determine the blocklength range actually needed by the existing or intended figure and estimate the cost from representative values. Do not automatically run unnecessary blocklengths. The final certification must cover every blocklength that is plotted or quoted in the manuscript-facing output.

Validate each converse branch and their maximum against the independently computed minimax value whenever that value is available. Do not clip a converse to the minimax curve. Report any violation.

## Part C

## Bring forward the fixed and subexponential continuous converse certification

Reuse the validated work from `codex/continuous-renyi-converse-optimisation` rather than recomputing it.

The previous audit reported, among other checks,

- 600 saved rows
- continuous optimisation of both valid converse branches
- 167 committed finite starting orders plus the order infinity endpoint
- every distinct final candidate order globally revalidated
- two outer optimisation rounds until post-polish stability
- maximum displayed improvement about `2.879011353142e-04`
- median displayed improvement about `1.707118458233e-05`
- largest displayed converse minus stored minimax about `6.66e-16`.

Import the reusable continuous optimiser and validated cache or comparison data into this branch in a way that preserves the current main branch's Fano/data-processing curve and Fano-aware plotting script.

Do not recompute the 600 minimax LP values or the calibrated achievability values.

Confirm that the imported cache reproduces the previously certified fixed and `1/n` converse values before using it.

## Projection strategy and cost control

For every Reni projection in Parts A and B

1. Start from the nearest validated projection in order.
2. Use adjacent validated projections as secondary starts.
3. Cache every newly evaluated order and pair.
4. Share the cache across all blocklengths because the composite divergence depends on the order and class orientation, not on `n` or `epsilon`.
5. Use a coarse global parameter scout only when necessary during the outer search.
6. Re-run the full global parameter screen at every final distinct candidate maximising order.
7. Repeat the outer search after global polishing until the order and divergence are stable.
8. Include order one and order infinity limits explicitly where mathematically relevant without attempting an invalid projection at order one.
9. Check Reni monotonicity of the validated directed divergence values as a diagnostic.

Use existing caches from `nonordered_bruno_regimes.py`, `nonordered_bruno_renyi_cache.json`, the continuous optimisation branch, and any ternary-specific historical calculations as warm starts whenever the class endpoints and orientation match.

## Independent validation

The certification is not complete merely because an optimiser reports success.

Required checks include

1. Reproduce every legacy value from its stored data before refining it.
2. Verify each refined outer value is no worse than the legacy value in the mathematically appropriate direction.
3. Globally revalidate every selected inner class projection.
4. Verify the final selected order is no worse than both adjacent screening points.
5. Verify directed Reni divergence monotonicity on the validated values up to a stated tolerance.
6. For finite sample converse curves, verify each branch and their maximum remain below the independently computed minimax Type II error within the established LP tolerance.
7. For the subcritical `n=20` table, independently reevaluate Type I and Type II envelopes on a dense parameter grid in addition to the polynomial separator used by the LP solver.
8. Record all tolerances and the largest observed residual for each check.
9. Do not suppress, clip, or silently repair validation failures.

## Outputs

Create a unified audit

`numerics/ternary_and_converse_certification_audit.md`

containing

- exact class definitions and rates
- exact numerical formulations for the subcritical saddle, reverse converse branch, and forward converse branch
- the optimisation procedure
- all warm starts and caches reused
- number of new orders and projections actually evaluated
- continuous optimiser stopping conditions
- global projection validation procedure
- certified unrounded subcritical saddle values
- certified unrounded `n=20` table values
- certified supercritical ternary branch values and selected orders
- identification of which branch wins as a function of blocklength
- any order infinity selections
- all validation tolerances and largest residuals
- exact comparison with legacy values
- whether any manuscript-facing rounded number changes
- enough detail to write a Numerical Methods appendix without inspecting the code.

Create machine-readable data for the certified ternary calculations under `numerics/data/`. Keep legacy data intact for comparison.

If the strong converse ternary example has or needs a figure, regenerate only that affected figure after all validation passes.

For the fixed and `1/n` 2 by 2 figure, preserve the Fano/data-processing curve already on `main` while replacing only the Reni converse values with the validated continuous values from the previous branch if they are not already present.

Do not edit `manuscript/`.

## Acceptance criteria

The task is complete only if

1. The manuscript's existing ternary KL, saddle order, pair, exponent, and blocklength 20 table are independently certified or any discrepancy is explicitly reported.
2. The supercritical ternary reverse converse is continuously optimised and independently validated.
3. The supercritical ternary forward converse is computed with its correct functional form, continuously optimised, and independently validated.
4. The displayed maximum of the two branches is reported separately from each branch.
5. Existing fixed and `1/n` continuous converse work is reused, not recomputed wholesale.
6. Current Fano/data-processing additions on `main` are preserved.
7. Existing LP and achievability calculations are reused wherever possible.
8. Every final new projected pair is globally revalidated.
9. All plotted or quoted converse values are checked against an independent minimax value whenever available.
10. The unified audit gives enough numerical receipts for a publication appendix.
11. `manuscript/` remains untouched.

Commit the implementation, certified data, any necessary regenerated figures, and the audit in small reviewable commits. In the final response report all numerical discrepancies from the manuscript and legacy curves, the maximum improvement from continuous optimisation, and any remaining uncertified quantity.
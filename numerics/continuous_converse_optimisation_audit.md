# Audit: continuous Rényi-order optimisation of the numerical converse

## Outcome

Validation status: **PASS**.

The displayed maximum converse improved by at most
`2.879011353142e-04` and by a median of
`1.707118458233e-05` across the 600 saved rows.  The
largest improvement occurs at `n=277` in the
`linear` Type I regime: the bound moves from
`0.0297780115627` to
`0.030065912698`.

This is a numerical refinement of the saved experiment, not a new
mathematical converse.  The feasible projected pairs used during the outer
search give divergences no smaller than the exact composite infimum and hence
conservative lower bounds.  Mathematical validity comes from the two Hölder
inequalities described below; the optimiser and validation checks provide
numerical evidence that their suprema have been located accurately.

## Branch objectives and mathematical clarification

The reverse branch uses `D_lambda(Q||P)` and maximises

```text
E_reverse(a) = a [log(1/epsilon) - n D_lambda(Q||P)]_+,
beta_reverse = -expm1(-max_a E_reverse(a)).
```

The task directive displayed this exponent for “each” branch.  It cannot be
applied to the forward direction.  Hölder's inequality with `D_lambda(P||Q)`
instead gives

```text
ell_forward(a) = log(1-epsilon)/a - n D_lambda(P||Q),
beta_forward = exp(max_a ell_forward(a)).
```

The implementation therefore preserves and continuously refines the two
existing valid branches separately, then reports their maximum.  Applying the
reverse conversion to the forward divergence would exceed the saved minimax
value in 11 rows (by as much as about `5.3927e-3`) and is not used.

## Optimisation procedure and cache reuse

The bounded variable is `a=(lambda-1)/lambda`.  For every saved
`(n, regime, branch)` row, the scalar objective is first evaluated from the
167 committed finite orders and the committed order-infinity projection;
none of those divergences is recomputed.  Strict local mesh maxima, the best
mesh point and their neighbouring intervals define the candidate bounded
searches.  The limits `a downarrow 0` and `a=1` are checked
explicitly; no numerical projection is attempted at order one.

At each new scalar trial, L-BFGS-B starts first from the nearest cached
projected pair and then from pairs at adjacent cached orders.  A monotonicity
bracket against validated projections detects unstable inner evaluations;
only such evaluations invoke the 13-by-13 global screen immediately.  New
records are appended and fsynchronised to a JSON-lines journal, so interrupted
work can resume.  A successful run compacts the journal into
`numerics/data/nonordered_bruno_continuous_renyi_cache.json`.

The outer searches were repeated for 2 round(s), stopping only after
successive maximisers agreed within `5.0e-08` in
`a` and the final global screens improved divergence by at most
`1.0e-10`.  Every distinct new candidate
maximiser from each round was revalidated with the existing
13-by-13 multistart projection routine (using 6 worker processes).
The better feasible result between the warm point and global screen is retained;
their largest adverse disagreement was
`1.519e-14`.

The compact overlay contains 13511 projections: 13508
new branch/order projections at 13345 distinct new Rényi orders and
3 explicitly revalidated committed-mesh projections.
Of the new projections, 1313 are globally screened.  During this run there
were 13508 new warm evaluations,
165 instability-triggered global screens, and
1151 explicit final-candidate or base revalidation polishes.
There were 21222 exact projection-cache hits and
1865 unsuccessful local optimiser starts.
Divergence
evaluations are independent of `n` and `epsilon`, so all blocklengths and both
Type I regimes reuse this common store and nearby projected pairs.

Refinement-only runtime for the outer searches and projection validation,
excluding cache compaction, comparison/audit writing and figure rendering, was
`425.176` seconds for this invocation.  On a resumed run this
timer and the preceding evaluation counters exclude work already present in
the validated cache.

## Numerical changes by branch

| Branch | Maximum improvement | Median improvement | Rows with changed order | Distinct selected orders |
|---|---:|---:|---:|---:|
| Reverse (`Q||P`) | 2.879011353142e-04 | 1.837523719103e-05 | 559 | 558 |
| Forward (`P||Q`) | 1.875042550587e-04 | 9.679389878642e-06 | 599 | 599 |

Measured in the bounded variable `a`, the median/maximum absolute changes from
the legacy selected orders are
`2.170955e-03` /
`6.956246e-03` for the reverse branch and
`2.107454e-03` /
`6.988040e-03` for the forward branch.

The five largest displayed improvements are:

- `n=277`, `linear`: `0.0297780115627` to `0.030065912698` (gain `2.879011353142e-04`), winning order `1.0787864923` (reverse).
- `n=227`, `constant`: `0.0242319349024` to `0.0244448917681` (gain `2.129568657168e-04`), winning order `1.07836345209` (reverse).
- `n=276`, `linear`: `0.0309612592749` to `0.0311513910746` (gain `1.901317996766e-04`), winning order `1.08036231113` (reverse).
- `n=278`, `linear`: `0.0288128213804` to `0.0290001870988` (gain `1.873657184210e-04`), winning order `1.0772185701` (reverse).
- `n=286`, `linear`: `0.0210270162429` to `0.0211835357129` (gain `1.565194700206e-04`), winning order `1.06494596106` (reverse).

The identity of the branch giving the displayed maximum changes in
0 rows.  The order-infinity endpoint is selected by the
reverse branch in 4 rows and by the forward
branch in 0 rows.

Reverse order-infinity selections: n=1, constant, n=2, constant, n=3, constant, n=4, constant.

Forward order-infinity selections: none.

For flat zero-bound cases, the legacy smallest finite mesh order is retained;
such an order is not interpreted as an identified optimiser.

## Validation

The absolute tolerance for comparing a converse with the stored numerical
minimax value is `2.1e-09`, just above the established LP
alternative-envelope residual (about `2.0e-9`).  Scalar non-inferiority uses
`1.0e-11`; projection round trips use `5e-13`; global-screen
agreement and validated Rényi monotonicity use
`1.0e-10`.

- Largest error reconstructing every legacy branch and maximum from the committed cache: `2.220446e-16`.
- Largest decrease of the refined displayed converse relative to the legacy mesh: `0.000000e+00`.
- Largest reverse-branch decrease: `0.000000e+00`.
- Largest forward-branch decrease: `0.000000e+00`.
- Largest selected-bound inferiority to either adjacent committed mesh point: `0.000000e+00`.
- Largest selected projection divergence round-trip error: `0.000000e+00`.
- Selected projections with invalid parameters or divergence: `0`.
- Selected orders lacking the required global screen: `0`.
- Largest absolute divergence difference between a warm candidate and its global screen: `2.431388e-14`.
- Largest divergence improvement supplied by global screening: `2.431388e-14`.
- Largest validated decrease in directed divergence as Rényi order increases: `0.000000e+00`.
- Largest reverse converse minus stored minimax: `6.661338e-16`.
- Largest forward converse minus stored minimax: `0.000000e+00`.
- Largest displayed maximum converse minus stored minimax: `6.661338e-16`.

No value is clipped to the minimax result.  Validation failures:

None.

## Figures and manuscript impact

Only the two standalone converse panels and the combined 2-by-2 figure depend
on the refined maximum.  They are regenerated from saved CSV values only:
`nonordered_bruno_constant_converse.eps`,
`nonordered_bruno_linear_converse.eps`, `nonordered_bruno_2x2.eps`, and
`nonordered_bruno_2x2.png`.  The two achievability-only EPS files are left
unchanged.

The manuscript's nonordered ternary example uses different class endpoints,
an exponentially decaying Type I schedule, and a separate blocklength-20 gap
table.  Its plotted figures concern ordered endpoint families.  Consequently,
this refinement does not materially change an existing manuscript statement
or identify text requiring revision.  If these curves are later incorporated,
their caption should distinguish the reverse branch, forward branch and their
displayed maximum.

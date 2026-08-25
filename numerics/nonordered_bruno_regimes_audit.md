# Audit: non-ordered Bruno-style finite-blocklength experiment

## Affine ternary classes

The experiment uses

```text
P0 = [0.33, 0.33, 0.34]
P1 = [0.33, 0.35, 0.32]
Q0 = [0.20294716, 0.42818293, 0.36886991]
Q1 = [0.37047326, 0.45476373, 0.17476301]
```

and the affine segments `P_s=(1-s)P0+sP1` and
`Q_t=(1-t)Q0+tQ1`, with `s,t` in `[0,1]`.  The smallest endpoint
coordinate is 0.17476301,
so every law in both classes has full support.

The directed composite KL separations are
`D(Q||P)=0.01739678` and
`D(P||Q)=0.01697432`. At n=300 the computed minimax Type-II errors remain 0.185072 (epsilon=0.01) and 0.303775 (epsilon=1/n), so the selected separation remains visible throughout the requested range.

The within-class endpoint log-ratio rank signatures (in increasing order)
are `(2, 0, 1)` for the null segment and `(2, 1, 0)` for the
alternative segment.  They are incompatible.  In addition, the centred
two-dimensional log-odds coordinates of the four laws have singular values
`[1.1705117223077444, 0.3919281508748278]`; the nonzero second value rules out collinearity in a
common one-parameter ternary exponential family.  At order
0.5, the single-letter projected-score
ordering violations are
2.220446e-16 (null) and
9.323667e-02 (alternative),
so the manuscript's projected-ordering sufficient conditions fail.

The finite-block validation below is the operational non-ordering check.  At
`n=30, epsilon=0.01` and `n=40, epsilon=1/n`, the unrestricted composite LP
is strictly above the largest simple-pair value found by a seeded global
search over the complete `(s,t)` square.  The optimised calibrated projected
rule is also strictly above the unrestricted minimax value at every
representative check.  Thus the experiment is not evaluated by ordered
endpoint reduction or by treating a projected pair as least favourable.

## Numerical mesh and optimisation

The reported blocklength mesh is: all integers 1--300.  The CSV contains only
computed blocklengths.  Plotting joins those computed points by straight
line segments; no smoothed or fabricated numerical rows are introduced.
Projected-test calibration starts from 65 equally spaced
values of each class parameter before continuous refinement.

For each blocklength, ternary sequences are symmetrised into
`(n+1)(n+2)/2` exact types.  The minimax problem is a semi-infinite LP in
the type-wise randomisation probabilities.  Constraint generation starts
from seventeen deterministic values of each class parameter, solves with HiGHS,
then adds continuous worst-case null and alternative parameters until both
violations are at most `2e-9`; active parameters are deduplicated at
`2e-10`.  Each separating expectation is a polynomial of degree at most `n`;
it is represented at `n+1` Chebyshev nodes, trimmed at `5e-13`, and its
derivative is screened with oversampling factor 16 before root polishing.
Every candidate is re-evaluated from the original multinomial
probabilities.  LP rows and the objective are scaled by `1e4`; HiGHS primal
and dual feasibility tolerances are `1e-10`, the IPM optimality tolerance is
`1e-12`, and the small-matrix threshold is `1e-12`, to retain rare exact
types at large `n`.
Dual simplex is the default master solver, with a deterministic interior-point
fallback; `n=299` uses the same two methods in the opposite order because its
dual-simplex active set is reproducibly degenerate.

The tightened achievability calculation uses 27
orders in `(0,1)`, namely `0.001, 0.002, 0.005, 0.01, 0.02, 0.035, 0.05, 0.075, 0.1, 0.14, 0.18, 0.23, 0.28, 0.34, 0.4, 0.47, 0.5, 0.54, 0.61, 0.68, 0.75, 0.82, 0.88, 0.93, 0.96, 0.98, 0.99`.
For each order the joint composite Renyi projection is computed and cached,
the projected log-likelihood-ratio types are sorted, the threshold is
optimised, and a common boundary randomisation is adjusted until the
composite Type-I envelope exhausts the requested budget.  The smallest
maximal Type-II error over the order mesh is reported; the loose closed-form
exponential bound is not used.
Each joint projection uses a 13-by-13 scout grid followed by L-BFGS-B from
the twelve best starts (`ftol=1e-15`, `gtol=2e-10`, at most 500 iterations).
Continuous error envelopes use `xatol=2e-11`, `fatol=1e-13`, and at most 160
iterations.  Boundary calibration uses 60 bisection steps followed by ratio
minimisation with `xatol=2e-12`, `fatol=1e-13`, and at most 180 iterations.

For each Bruno converse branch, the script caches both directed composite
Renyi divergences on 167 finite orders greater than one,
plus the order-infinity limit.  The
order mesh is deterministic in `a=(lambda-1)/lambda`, with logarithmic
resolution near zero and one.  The displayed converse is the maximum of the
forward and reverse branches.  Restricting the order optimisation to this
mesh preserves converse validity (it can only weaken the displayed lower
bound).  The order-infinity projections are additionally polished by Powell
optimisation with `xtol=2e-11`, `ftol=1e-14`, and at most 1,000 iterations.

## Independent validation

Representative LP and projected tests were recomputed and evaluated on an
independent grid of 4,001 values for each class parameter.

Across all 600 CSV rows:

* Maximum LP Type-I violation: 9.514091e-15
* Maximum LP objective violation: 1.997726e-09
* Maximum absolute projected Type-I exhaustion error: 5.551115e-17
* Maximum violation of `achievability >= minimax`: 3.219647e-15
* Maximum violation of `converse <= minimax`: 6.661338e-16

On the independent 4,001-point representative grids, the maximum LP Type-I
violation is 2.074729e-15, the maximum LP
objective violation is 1.774797e-09, and
the maximum projected Type-I exhaustion error is
2.602085e-18.

* Smallest representative minimax gap above all four endpoint simple-pair values: 1.073637e-01
* Smallest designated minimax gap above the largest simple-product-pair value found: 9.057209e-05
* Smallest representative calibrated-projected gap above minimax: 9.076987e-04

At `n=30, epsilon=0.01` and `n=40, epsilon=1/n`, the largest simple-pair
value is sought by seeded differential evolution over
`(s,t) in [0,1]^2`; the search is not restricted to endpoints.  It uses
`tol=2e-9`, `atol=2e-11`, population multiplier 18, and at most 180
generations.  The positive search gaps numerically exclude least-favourable
simple-pair reduction at those checks to these optimisation tolerances.  The
other representative rows check endpoint-pair and projected-pair gaps.  Together,
the strict gaps numerically exclude endpoint reduction and verify that the
tightened projected test is not identically the composite minimax solution.
Individual validation rows are included below.

```json
[
  {
    "n": 30,
    "regime": "constant",
    "epsilon": 0.01,
    "lp_type_i_violation": 1.042568809062061e-15,
    "lp_type_ii_grid_violation": 1.0725645926967786e-09,
    "achievability_type_i_absolute_error": 0.0,
    "achievability_below_minimax_violation": 0.0,
    "converse_above_minimax_violation": 0.0,
    "endpoint_pair_lower_bound": 0.7952582946260408,
    "minimax_minus_endpoint_pair": 0.10736369389363887,
    "projected_pair_simple_value": 0.9021913902766592,
    "calibrated_projected_minus_minimax": 0.008772541088972186,
    "all_simple_pair_lower_bound": 0.9023088119601552,
    "all_simple_pair_s": 0.999999993754833,
    "all_simple_pair_t": 0.418035110388626,
    "minimax_minus_all_simple_pair": 0.0003131765595244529
  },
  {
    "n": 30,
    "regime": "linear",
    "epsilon": 0.03333333333333333,
    "lp_type_i_violation": 1.5681900222830336e-15,
    "lp_type_ii_grid_violation": 2.9723701278072667e-10,
    "achievability_type_i_absolute_error": 0.0,
    "achievability_below_minimax_violation": 0.0,
    "converse_above_minimax_violation": 0.0,
    "endpoint_pair_lower_bound": 0.616242175568481,
    "minimax_minus_endpoint_pair": 0.1729913446150848,
    "projected_pair_simple_value": 0.7889854401024204,
    "calibrated_projected_minus_minimax": 0.0025390017070968662,
    "all_simple_pair_lower_bound": null,
    "all_simple_pair_s": null,
    "all_simple_pair_t": null,
    "minimax_minus_all_simple_pair": null
  },
  {
    "n": 40,
    "regime": "constant",
    "epsilon": 0.01,
    "lp_type_i_violation": 2.0747292772682613e-15,
    "lp_type_ii_grid_violation": 1.7747966429837447e-09,
    "achievability_type_i_absolute_error": 1.734723475976807e-18,
    "achievability_below_minimax_violation": 0.0,
    "converse_above_minimax_violation": 0.0,
    "endpoint_pair_lower_bound": 0.7141665804624899,
    "minimax_minus_endpoint_pair": 0.15816850571190355,
    "projected_pair_simple_value": 0.8723212085866348,
    "calibrated_projected_minus_minimax": 0.0013471662792305938,
    "all_simple_pair_lower_bound": null,
    "all_simple_pair_s": null,
    "all_simple_pair_t": null,
    "minimax_minus_all_simple_pair": null
  },
  {
    "n": 40,
    "regime": "linear",
    "epsilon": 0.025,
    "lp_type_i_violation": 1.5751289161869408e-15,
    "lp_type_ii_grid_violation": 3.194178255228053e-11,
    "achievability_type_i_absolute_error": 0.0,
    "achievability_below_minimax_violation": 0.0,
    "converse_above_minimax_violation": 0.0,
    "endpoint_pair_lower_bound": 0.56919298008976,
    "minimax_minus_endpoint_pair": 0.2113972060442414,
    "projected_pair_simple_value": 0.780218155627376,
    "calibrated_projected_minus_minimax": 0.0030631770669221625,
    "all_simple_pair_lower_bound": 0.7804996140390134,
    "all_simple_pair_s": 0.9999999996866937,
    "all_simple_pair_t": 0.4825958470357,
    "minimax_minus_all_simple_pair": 9.057209498808394e-05
  },
  {
    "n": 150,
    "regime": "constant",
    "epsilon": 0.01,
    "lp_type_i_violation": 0.0,
    "lp_type_ii_grid_violation": 1.2621086398212356e-09,
    "achievability_type_i_absolute_error": 1.734723475976807e-18,
    "achievability_below_minimax_violation": 0.0,
    "converse_above_minimax_violation": 0.0,
    "endpoint_pair_lower_bound": 0.11322208007154799,
    "minimax_minus_endpoint_pair": 0.4028594185080694,
    "projected_pair_simple_value": 0.5160647173830646,
    "calibrated_projected_minus_minimax": 0.0018737270171996778,
    "all_simple_pair_lower_bound": null,
    "all_simple_pair_s": null,
    "all_simple_pair_t": null,
    "minimax_minus_all_simple_pair": null
  },
  {
    "n": 150,
    "regime": "linear",
    "epsilon": 0.006666666666666667,
    "lp_type_i_violation": 0.0,
    "lp_type_ii_grid_violation": 7.682287028742962e-10,
    "achievability_type_i_absolute_error": 2.6020852139652106e-18,
    "achievability_below_minimax_violation": 0.0,
    "converse_above_minimax_violation": 0.0,
    "endpoint_pair_lower_bound": 0.14618796665825717,
    "minimax_minus_endpoint_pair": 0.42812446030443096,
    "projected_pair_simple_value": 0.5742929752508681,
    "calibrated_projected_minus_minimax": 0.004155612476113513,
    "all_simple_pair_lower_bound": null,
    "all_simple_pair_s": null,
    "all_simple_pair_t": null,
    "minimax_minus_all_simple_pair": null
  },
  {
    "n": 300,
    "regime": "constant",
    "epsilon": 0.01,
    "lp_type_i_violation": 0.0,
    "lp_type_ii_grid_violation": 5.216196641288917e-10,
    "achievability_type_i_absolute_error": 0.0,
    "achievability_below_minimax_violation": 0.0,
    "converse_above_minimax_violation": 0.0,
    "endpoint_pair_lower_bound": 0.0032210090751872977,
    "minimax_minus_endpoint_pair": 0.18185056709811342,
    "projected_pair_simple_value": 0.18506943726367575,
    "calibrated_projected_minus_minimax": 0.0012291530739101941,
    "all_simple_pair_lower_bound": null,
    "all_simple_pair_s": null,
    "all_simple_pair_t": null,
    "minimax_minus_all_simple_pair": null
  },
  {
    "n": 300,
    "regime": "linear",
    "epsilon": 0.0033333333333333335,
    "lp_type_i_violation": 0.0,
    "lp_type_ii_grid_violation": 4.810142284483732e-10,
    "achievability_type_i_absolute_error": 0.0,
    "achievability_below_minimax_violation": 0.0,
    "converse_above_minimax_violation": 0.0,
    "endpoint_pair_lower_bound": 0.010239220401278892,
    "minimax_minus_endpoint_pair": 0.2935362084862032,
    "projected_pair_simple_value": 0.303774243638424,
    "calibrated_projected_minus_minimax": 0.0009076986896274786,
    "all_simple_pair_lower_bound": null,
    "all_simple_pair_s": null,
    "all_simple_pair_t": null,
    "minimax_minus_all_simple_pair": null
  }
]
```

## Checkpointing and runtime

The Renyi projections/divergences are independent of `n` and stored in
`numerics/data/nonordered_bruno_renyi_cache.json`.  Each completed
blocklength has an atomic JSON checkpoint under
`numerics/checkpoints/nonordered_bruno_regimes/`; reruns resume by default.
Checkpoint identity covers the endpoints and Renyi meshes, epsilon schedules,
operating-grid size, both numerical source files, and the Python, NumPy, and
SciPy versions, so a changed run configuration is not silently reused.
Blocklengths were evaluated with 4 worker process(es) and one BLAS
thread per worker.

Blocklength-stage wall time for the current resumed run (checkpoint loading
only; excluding plotting and independent validation): 0.042
seconds.  Sum of recorded per-blocklength worker times:
2949.928 seconds.  Elapsed span from the first to last
completed blocklength checkpoint: 1105.717 seconds.  The
n-independent Renyi cache took 27.269 seconds.
Platform: `Linux-6.18.35-x86_64-with-glibc2.39`;
Python: `3.12.13`.

The committed outputs are reproduced by running
`python numerics/scripts/nonordered_bruno_regimes.py --jobs 4` from the
repository root.

# Audit: ternary saddle and finite-sample converse certification

## Outcome and scope

Validation status: **PASS** for every task-required numerical quantity.

This audit distinguishes exact formulae and analytic implications from numerical
certification.  The class endpoints and rates below are exact decimal inputs.
The displayed optimisation values are numerical certificates with the stated
screens, residuals, and tolerances.  Claims of uniqueness are deliberately
limited to numerical evidence.

No file under `manuscript/` was changed.  The manuscript-facing rounded values
for the subcritical example all remain unchanged.  The legacy supercritical
values are valid rounded warm starts, and the fixed-`epsilon`/`1/n` continuous
refinement changes only the saved Rényi converse overlay.

## Exact classes, divergences, and rates

For $s,t\in[0,1]$,

\[
P_s=(1-s)P_0+sP_1,\qquad Q_t=(1-t)Q_0+tQ_1,
\]

with

\[
\begin{aligned}
P_0&=(0.327,0.418,0.255),&P_1&=(0.563,0.266,0.171),\\
Q_0&=(0.143,0.357,0.500),&Q_1&=(0.379,0.205,0.416).
\end{aligned}
\]

For finite $\lambda\ne1$,

\[
D_\lambda(R\Vert S)=\frac{1}{\lambda-1}
 \log\sum_i R_i^\lambda S_i^{1-\lambda},
\]

with the KL limit at order one and
$D_\infty(R\Vert S)=\max_i\log(R_i/S_i)$.  A directed composite
divergence is the minimum over the full $(s,t)$ square in the displayed
orientation; the two orientations are never interchanged.

The 80-decimal-digit KL solve gives

\[
D(\mathcal Q\Vert\mathcal P)
=0.09487789505284773533969740751800984369642240401234415824868574945431528,
\]

at $s=0$ and
$t=0.6391372739017507520723578414962444399045241512529054938101533502353730$.
Therefore

\[
\begin{aligned}
r_-&=0.35D(\mathcal Q\Vert\mathcal P)\\
&=0.03320726326849670736889409263130344529374784140432045538704001230901035,\\
r_+&=1.5D(\mathcal Q\Vert\mathcal P)\\
&=0.1423168425792716030095461112770147655446336060185162373730286241814729.
\end{aligned}
\]

## Numerical formulations

The subcritical profile is

\[
E_{\rm H}=\max_{0<\lambda<1}\frac{1-\lambda}{\lambda}
\left[\min_{s,t}D_\lambda(Q_t\Vert P_s)-r_-\right].
\]

The numerical saddle check also evaluates the reverse order of optimisation,

\[
\min_{s,t}\max_{0<\lambda<1}\frac{1-\lambda}{\lambda}
\left[D_\lambda(Q_t\Vert P_s)-r_-\right].
\]

For the supercritical schedule
$\varepsilon_n=\exp(-nr_+)$, let
$a=(\lambda-1)/\lambda\in(0,1]$ and
$\lambda=1/(1-a)$.  The reverse branch is

\[
\beta_{\rm reverse}(n)=1-\exp\left\{-n\sup_{0<a\le1}
a\left[r_+-D_{1/(1-a)}(\mathcal Q\Vert\mathcal P)\right]_+\right\}.
\]

The separately valid forward Hölder/Bruno branch is

\[
\beta_{\rm forward}(n)=\sup_{0<a\le1}\exp\left\{
\frac{\log(1-\varepsilon_n)}{a}
-nD_{1/(1-a)}(\mathcal P\Vert\mathcal Q)\right\}.
\]

The reported combined converse is
$\max\{\beta_{\rm reverse},\beta_{\rm forward}\}$.  The reverse
positive-part conversion is not applied to the forward divergence, and no
branch is clipped to a minimax LP value.

## Repository search and reuse

The history search covered all 12 branches, 94 unique reachable commits,
recursive trees, 61 unique historical text blobs, PRs 1--8, relevant workflow
runs, and available tags/releases.  It searched exact endpoints and reported
values as well as rates, orders, class parameters, cache/checkpoint names,
minimax outputs, and figure names.

For the exact manuscript family, history contained only the rounded manuscript
record and the reusable semi-infinite solver
`numerics/scripts/affine_ternary_lp.py` (blob
`14ec9ef16af93611ed2522a2650ba1278e9b7790`).  No exact-family projection
cache, unrounded $n=20$ receipt, tracked LP checkpoint, selected-order
strong-converse curve, supercritical minimax sweep, or strong-converse figure
was present.  Parts A and B consequently used the reported numbers only as
warm starts, reused the generic LP/projection/calibration machinery, and made
new orientation-specific caches.  The Part B LP used new per-blocklength NPZ
checkpoints and cross-$n$ active-set warm starts.

The older 600-row experiment uses different endpoints,

\[
\begin{aligned}
P_0&=(0.33,0.33,0.34),&P_1&=(0.33,0.35,0.32),\\
Q_0&=(0.20294716,0.42818293,0.36886991),&
Q_1&=(0.37047326,0.45476373,0.17476301),
\end{aligned}
\]

so its projections were not used to seed Parts A or B.  Apparent matches such
as order `1.224477`, cache coordinate `0.026419002...`, and schedule value
`0.0047619` were rejected as different-family false positives.

Part C was selectively imported from
`codex/continuous-renyi-converse-optimisation` at
`30654fb4c33d8fd4a453faa10aec4eb432cf705c`; no merge or cherry-pick brought
in the pre-Fano figures.  Provenance is:

| Artifact | Source commit | Git blob |
|---|---|---|
| `continuous_renyi_converse_optimisation.py` | `1230066b76eb28c7e3b43c6a140bef6a6d0bc47d` | `a8058eb81c34df6645a0ea3d8c5f1326e02fe96a` |
| Continuous comparison CSV | `2557318bf7cc2ccf7801be69ecc1704fc3a77ee5` | `17251d63383a1386f41e804c393bf4c6bf47f4f6` |
| Continuous projection cache | `2557318bf7cc2ccf7801be69ecc1704fc3a77ee5` | `c29640e3a6b4760970a70c8ef2239fa52f0a18b2` |
| Source optimisation audit | `30654fb4c33d8fd4a453faa10aec4eb432cf705c` | `1cdf28b2f191a58d9816994ddffcbaeeaac0c1fb` |

The unchanged inputs are `nonordered_bruno_regimes.csv` (blob `122843b6...`),
the legacy Rényi cache (blob `141a7288...`), and
`nonordered_bruno_regimes.py` (blob `246e5dc2...`).  Thus none of the 600
stored minimax LP or calibrated-achievability rows was recomputed.

## Part A: subcritical saddle

### Continuous optimisation and global validation

The manuscript warm start first seeds an 82-order scout.  The final order is
not selected from this mesh: each of two rounds uses bounded continuous scalar
refinement (`xatol=2e-13`, at most 1000 iterations).  Each new order uses the
nearest cached projected pair plus the adjacent cached pairs as starts.  Every
new order/pair is stored in
`numerics/data/ternary_subcritical_projection_cache.json`.

The run made 99 projection evaluations at 97 distinct new orders, with 95
cache hits.  Both round maximisers received a full $1001\times1001$ square
screen, differential-evolution scout, and local polish.  The two selected
orders were `0.6014375128904821` and `0.6014375307321356`; their separation
was `1.784165348794886e-08`, below the `5e-8` stopping tolerance.  Their
objective values differed by `5.551115123125783e-17`; the largest improvement
in $D_\lambda$ from global polishing was `5.759281940243e-16`, below
`1e-10`, and adjacent-screen inferiority was zero in both rounds.  The
order-one objective limit is zero; the order-zero limit is minus infinity for
these full-support classes and $r_->0$.

An independent 80-digit Newton solve of the projection-stationarity and
rate-matching equations stopped below a `1e-70` step.  It gives the certified
values

\[
\begin{aligned}
\lambda^\star&=0.6014375179592104010745884902326253591211417323746723933162593844596322,\\
s^\star&=0,\\
t^\star&=0.6028434550414398235869833511967816142498355238124404665546321466025728,\\
D_{\lambda^\star}(Q_{t^\star}\Vert P_0)
&=0.05631531434719570227200996249589105946380528467769558445386435688921715,\\
E_{\rm H}&=0.01531331504609634421557320402252651645022066467016784549782652189126677.
\end{aligned}
\]

The tilted law is

\[
R^\star=(0.30806070855063189277522440960738428136,
0.32526968829636585142525809946982068778,
0.36666960315300225579951749092279503086),
\]

and the 80-digit calculation returns
$D(R^\star\Vert P_0)=r_-$ and
$D(R^\star\Vert Q_{t^\star})=E_{\rm H}$.

The separate min--max computation used 3150 global pair candidates and a
continuous inner order optimisation.  It returned
`0.015313315046096287` at
$(\lambda,s,t)=(0.6014375634199242,0,0.6028434545555168)$, differing from
the max--min result by `-1.6653345369377348e-16`.  This supplies the numerical
saddle sandwich.

The selected KL and Rényi projections also received independent
$1001\times1001$ screens.  Differential-evolution polish returned
`0.09487789505284785` for KL and `0.056315314347196464` for Rényi, within
about `1.2e-16` and `7.7e-16` of the high-precision values.  A 100-order
monotonicity diagnostic, with 11 separate global cross-checks, found no
decrease; its largest profile/global discrepancy was
`5.551670234638095e-13`.

Numerical evidence supports a single basin but is not a uniqueness theorem.
The KL boundary derivative and $t$-curvature are
`+0.029446487966042326` and `+0.2942696529792243`; the selected-order Rényi
values are `+0.016733891795991204` and `+0.1986945041128699`; the outer
curvature is `-0.31636090159585056`.

### Complete $n=20$ gap table

Here $\varepsilon_{20}=0.5147132830103597$.  The `actual Type II` column
records the test's class envelope even for a looser analytical bound.

| Quantity | Certified value | Attained Type I | Worst $s$ | Actual Type II | Worst $t$ | Analytical $t$/relaxation |
|---|---:|---:|---:|---:|---:|---|
| Minimax Type II | 0.02641940284167423 | 0.5147132830103595 | 0 | 0.02641940284167423 | 0.55520929386513 | -- |
| Calibrated projected Type II | 0.03363265793899399 | 0.5147132830103593 | 0 | 0.03363265793899399 | 0 | -- |
| Projected Type II at `tau_min` | 0.23662009551315674 | 0.11022303340222175 | 0 | 0.23662009551315674 | 0.42370245164748604 | -- |
| Slack/rejection bound | 0.3991336822252006 | 0.11022303340222175 | 0 | 0.23662009551315674 | 0.42370245164748604 | 0.15887535598996355 |
| Raw projected exponential bound | 0.7361905451289885 | 0.11022303340222175 | 0 | 0.23662009551315674 | 0.42370245164748604 | uniform moment relaxation |

The minimax LP used all 231 ternary types, 33 initial parameter values per
class, and 14 constraint-generation iterations.  Its constraint tolerance was
`3e-14`, parameter deduplication tolerance `3e-15`, row/objective scale `1e4`,
separator trim tolerance `5e-13`, and derivative oversampling 64.  The master
value was `0.026419402841650595`; the validated Type-II envelope exceeded it by
`2.363387263670802e-14`.  Independent 500001-point dense checks returned Type I
`0.5147132830103595` at $s=0$ and Type II
`0.026419402841671043` at $t=0.55521$; separator-minus-dense residuals were
zero and `3.184952301893418e-15`.

Projected-test envelopes used a 100001-point dense check.  The largest
separator-minus-dense residual was `1.6006640457533194e-12` for the weighted
alternative envelope; the remaining relevant residuals were at most
`2.1210810885463616e-13`.  Calibration used
`tau_cal=-2.0081922439519904`, randomisation
`eta=0.028812013487143885`, and unique boundary type `(3,11,6)`.
The deterministic threshold was `tau_min=0.357878964448005`.

### Manuscript comparison

| Quantity | Printed | Certified | Certified minus printed | Display change? |
|---|---:|---:|---:|:---|
| KL separation | 0.094878 | 0.09487789505284773534 | -1.049471522646603e-7 | No |
| $r_-$ | 0.0332073 | 0.03320726326849670737 | -3.673150329263111e-8 | No |
| $\lambda^\star$ | 0.601438 | 0.60143751795921040107 | -4.820407895989254e-7 | No |
| $s^\star$ | 0 | 0 | 0 | No |
| $t^\star$ | 0.602843 | 0.60284345504143982359 | +4.550414398235870e-7 | No |
| $E_{\rm H}$ | 0.0153133 | 0.01531331504609634422 | +1.504609634421558e-8 | No |
| Minimax | 0.026419 | 0.02641940284167423 | +4.0284167423e-7 | No |
| Calibrated projected | 0.033633 | 0.03363265793899399 | -3.4206100601e-7 | No |
| At `tau_min` | 0.236620 | 0.23662009551315674 | +9.551315674e-8 | No |
| Slack/rejection bound | 0.399134 | 0.3991336822252006 | -3.177747994e-7 | No |
| Raw exponential bound | 0.736191 | 0.7361905451289885 | -4.548710115e-7 | No |

## Part B: supercritical converse

### Continuous reverse optimum

The reverse order is independent of $n$.  The 80-digit stationary solve is

\[
\begin{aligned}
a^\star&=0.1830498050623437152621508569750834164527671080564084366987093855592479,\\
\lambda^\star&=1.224064828182472921878207891899561604014753266807545110718415502743732,\\
(s^\star,t^\star)&=(0,0.6621510951167712320216953866751879071283127256638735684451948442600128),\\
D_{\lambda^\star}&=0.1163247940723476130332525360901459194311601994346729749069796656247348,\\
E_{\rm reverse}&=0.004757839412363418386178176109082145607385806908249459085820604709092668.
\end{aligned}
\]

The boundary-$s$ derivative is positive
(`0.0366238580363429341...`), and the Decimal inner/outer stationarity
residuals are below `3e-80`.  The legacy values
$(1.224,0.116,0.00476)$ differ by approximately

\[
\left(+6.4828182473\times10^{-5},+3.2479407235\times10^{-4},
-2.1605876366\times10^{-6}\right).
\]

At exactly $\lambda=1.224$, continuous
refinement improves the exponent by only `3.214356405e-10`; the legacy values
are therefore validated as rounded warm starts.

### Forward endpoint and branch winners

The forward KL separation is

\[
D(\mathcal P\Vert\mathcal Q)
=0.08972493185378859004955554055689691258674262868960856752259719273702243,
\]

at $s=0$, $t=0.55863736426012709205\ldots$.  At order infinity,

\[
D_\infty(\mathcal P\Vert\mathcal Q)
=0.3362619481207925202615293617469193491930997152320413753455786805970784.
\]

The infinity minimiser is not unique.  The entire minimising face is

\[
s=1.3997056270521191078235271917575574593\,t
-0.5374665056421481677171000490621579801,
\]

with
$0.3839853861087144089732528041415012942\le t\le1$ and
$0\le s\le0.8622391214099709401064271426953994792$.
The first two coordinate ratios are active; the third is slack.  No arbitrary
point on this face is reported as a unique projection.

The forward branch selects order infinity for $n=1,2,3$, and a finite order
from $n=4$.  The full directly validated range is:

| $n$ | Reverse | Forward | Forward $\lambda$ | Maximum | Winner | Minimax LP |
|---:|---:|---:|---:|---:|:---|---:|
| 1 | 0.00474653882365902 | 0.0947724984180341 | infinity | 0.0947724984180341 | forward | 0.0947724984180341 |
| 2 | 0.00947054801651354 | 0.126435930801080 | infinity | 0.126435930801080 | forward | 0.126435930801080 |
| 3 | 0.0141721345163309 | 0.126721379622188 | infinity | 0.126721379622188 | forward | 0.130159101010658 |
| 4 | 0.0188514047532940 | 0.126251357375672 | 3.6963783888794435 | 0.126251357375672 | forward | 0.164544118712625 |
| 5 | 0.0235084646524110 | 0.128745065565158 | 2.7828071712355693 | 0.128745065565158 | forward | 0.176349644999191 |
| 6 | 0.0281434196359127 | 0.130024312095183 | 2.3462050089165656 | 0.130024312095183 | forward | 0.196752025262360 |
| 7 | 0.0327563746256394 | 0.130102949349881 | 2.0759408602375050 | 0.130102949349881 | forward | 0.210641072111776 |
| 8 | 0.0373474340454155 | 0.129165301528964 | 1.8884253134979438 | 0.129165301528964 | forward | 0.225361259602009 |
| 9 | 0.0419167018234139 | 0.127394509247442 | 1.7494441386070292 | 0.127394509247442 | forward | 0.239540583002956 |
| 10 | 0.0464642813945083 | 0.124948617212849 | 1.6418691946150632 | 0.124948617212849 | forward | 0.251464023255393 |
| 11 | 0.0509902757026149 | 0.121960411635706 | 1.5560049340215318 | 0.121960411635706 | forward | 0.264692270703949 |
| 12 | 0.0554947872030224 | 0.118541315183778 | 1.4858821059742935 | 0.118541315183778 | forward | 0.276998007447146 |
| 13 | 0.0599779178647116 | 0.114785332952905 | 1.4275926715533810 | 0.114785332952905 | forward | 0.286110724332692 |
| 14 | 0.0644397691726635 | 0.110772290335325 | 1.3784542861274927 | 0.110772290335325 | forward | 0.297994402913537 |
| 15 | 0.0688804421301569 | 0.106570349118915 | 1.3365557830432740 | 0.106570349118915 | forward | 0.309035654529288 |
| 16 | 0.0733000372610543 | 0.102237940043849 | 1.3004931974881075 | 0.102237940043849 | forward | 0.317346812236809 |
| 17 | 0.0776986546120780 | 0.0978252547015219 | 1.2692087631409730 | 0.0978252547015219 | forward | 0.326714332054408 |
| 18 | 0.0820763937550748 | 0.0933754124964157 | 1.2418882118400372 | 0.0933754124964157 | forward | 0.337074179657648 |
| 19 | 0.0864333537892694 | 0.0889253896605886 | 1.2178933066572764 | 0.0889253896605886 | forward | 0.345139355971904 |
| 20 | 0.0907696333435086 | 0.0845067738768845 | 1.1967156067126652 | 0.0907696333435086 | reverse | 0.351865984134603 |
| 21 | 0.0950853305784934 | 0.0801463904018612 | 1.1779446105573141 | 0.0950853305784934 | reverse | 0.361903455957961 |
| 22 | 0.0993805431890011 | 0.0758668326458796 | 1.1612446670397296 | 0.0993805431890011 | reverse | 0.369951327057679 |
| 23 | 0.103655368406097 | 0.0716869207996942 | 1.1463386143621457 | 0.103655368406097 | reverse | 0.375944884189907 |
| 24 | 0.107909902999336 | 0.0676221053358417 | 1.1329950669273920 | 0.107909902999336 | reverse | 0.384047972572633 |
| 25 | 0.112144243278951 | 0.0636848273406966 | 1.1210194320672373 | 0.112144243278951 | reverse | 0.392207446906940 |

Thus forward wins for integer $1\le n\le19$, while reverse wins from
$n=20$.  Direct calculation covers through $n=25$.  For all later $n$,

\[
\beta_{\rm forward}(n)\le\exp\{-nD(\mathcal P\Vert\mathcal Q)\},
\]

whereas the reverse branch is increasing.  At $n=25$, the reverse value
`0.11214424327895142` already exceeds the forward KL envelope
`0.10612652163178594` by `0.006017721647165478`; hence there is no later
recrossing.

### Optimisation and independent validation

The orientation-aware in-memory cache was shared across all 25 blocklengths.
It contains 2575 projection evaluations at 2552 distinct orientation/order
keys (2545 distinct orders across the two orientations): 2187 records for
$P\Vert Q$ and 388 for $Q\Vert P$.  Nearest and adjacent cached orders
seed every local solve.  The selected/end-point set contains 28 globally
screened orientation/order projections.

Each branch used a hybrid scalar screen followed by continuous bounded
optimisation (`xatol=2e-14`, at most 500 iterations) and two complete outer
rounds.  The reverse search covered $a\in[10^{-8},0.95]$.  At the omitted
tail boundary, the globally screened value
$D_{20}(\mathcal Q\Vert\mathcal P)=0.44333253230885367>r_+$; Rényi
monotonicity makes the positive-part objective zero thereafter.  The forward
search records an $a$-floor for every $n$; the smallest margin between the
selected log-bound and the analytic omitted-small-$a$ upper bound was
`2888.442235584101`.

All second-round selected $a$, divergence, and log-value changes were zero
at stored precision, and all adjacent-screen inferiority values were zero.
The integrated full-square revalidation used a $101\times101$ scout plus
multistart polish at every selected order.  Its largest KKT residual was
`6.94759817732038e-09`, the largest coarse-grid excess over the polished
minimum was `1.284811022586041e-04`, and validated divergence monotonicity had
zero decrease in both orientations.  An independent read-only check repeated
every selected finite projection with a $1001\times1001$ screen and 66
multistarts; its largest selected-pair value difference was `1.13e-15`.  A
6899-order outer screen and 10000-order monotonicity screens found no competing
maximum or decrease.  These are numerical global-validation receipts, not a
general convexity claim for $\lambda>1$.

The independent semi-infinite LP sweep used cross-$n$ active constraints and
checkpointing for $n=1,\ldots,25$, constraint tolerance `5e-10`, parameter
tolerance `2e-10`, derivative oversampling 32, trim tolerance `5e-13`, and an
independent 10001-point dense grid.  Largest residuals were:

| Check | Largest residual |
|---|---:|
| Separator null | 1.932481952238163e-15 |
| Separator alternative | 4.354205329626382e-10 |
| Dense null | 1.925543058334256e-15 |
| Dense alternative | 4.297550093568248e-10 |
| Raw combined converse minus minimax | 1.387778780781446e-17 |

The last residual is floating-point equality at $n=1$; no value was clipped.

## Part C: fixed and subexponential continuous refinement

### Imported cache and replay

The comparison table has exactly 600 unique rows:
$n=1,\ldots,300$ for each of `constant` ($\varepsilon=0.01$) and `linear`
($\varepsilon=1/n$).  The committed starting grid has 167 finite orders and
the infinity endpoint; two orientations give 336 base projection records.

The imported compact cache has 13511 records: 13508 new branch/order
projections at 13345 distinct new orders and three globally revalidated base
records.  Of the new records, 1313 are globally screened; the source audit
records 1151 final/base multistart polishes, 165 instability-triggered global
screens, 21222 cache hits, and 1865 unsuccessful local starts.  All
blocklengths and both regimes share the cache because divergence depends on
order and orientation, not on $n$ or $\varepsilon$.

The exact Git blobs listed above were verified locally.  A read-only
`ProjectionStore` load reproduced fingerprint
`dc7eceebf789ca5f49f3bb5f03966eb5b6638ab382f21455abdb1378ed87938e`,
loaded all 13511 compact records, and reconstructed every legacy branch/maximum
with largest error `2.220446049250313e-16`.  The recorded environment is NumPy
`2.3.5` and SciPy `1.17.0`.

The source optimisation ran for two outer rounds.  Stopping required
successive selected $a$ values within `5e-8`, global-polish improvement at
most `1e-10`, scalar non-inferiority within `1e-11`, projection round trips
within `5e-13`, and stored-minimax comparison within `2.1e-9`.  Each final
candidate received the 13-by-13 multistart screen.  Independent replay found:

- largest continuous formula-replay error `1.1102230246251565e-16`;
- all 1157 distinct selected branch/order records globally validated;
- no invalid parameter, missing global screen, adjacent-mesh inferiority, or
  directed-divergence monotonicity decrease;
- largest selected-record divergence round trip
  `3.4763858458575214e-14` and all-record round trip
  `1.6739734598480993e-13`;
- largest warm/global divergence discrepancy
  `2.4313884239290928e-14`;
- largest displayed converse minus stored minimax
  `6.661338147750939e-16`.

No value was clipped to minimax.

### Refinement over the finite order mesh

Across 600 rows, the maximum improvement is
`2.879011353142148e-04` and the median is
`1.7071184582329035e-05`.  The largest change is at $n=277$, `linear`:

\[
0.02977801156265858\longrightarrow0.030065912697972794,
\]

with reverse order `1.0787864923046357`.  There are 595 strict improvements
and five ties.  The winning branch changes in no row.  Infinity is selected
only by the reverse branch for $n=1,2,3,4$ in the constant regime.

### Fano/data-processing preservation

The current Fano-aware plotter joins the legacy and imported comparison data
exactly by `(n, regime)`, rejects duplicate/missing/extra keys, and verifies
exact equality of `epsilon`, `minimax`, and the legacy converse.  The join
contains all 600 expected keys with zero discrepancy.  It replaces only the
Rényi value by `continuous_converse`, then uses the unchanged Fano formula and
KL constant.

An in-memory before/after check found that 595 Rényi text values changed while
all 600 `epsilon`, minimax, and Fano values remained exactly identical.  The
authoritative `nonordered_bruno_regimes.csv` and imported comparison remained
byte-identical.  Only the Fano CSV and combined 2-by-2 EPS/PNG were regenerated;
the regenerated PNG passed visual inspection.  The older pre-Fano figures were
not imported.

## Reproduction and artefact map

From the repository root:

```bash
# Part A: cached continuous saddle, 80-digit solve, n=20 LP and dense checks
python numerics/scripts/ternary_subcritical_certification.py

# Part B: continuous reverse/forward branches and checkpointed n=1,...,25 LPs
python numerics/scripts/ternary_supercritical_converse.py

# Part C: saved-data join and Fano-aware combined figure; no LP/order rerun
python numerics/scripts/replot_nonordered_bruno_2x2.py
```

Machine-readable outputs are:

- `ternary_subcritical_certification.json`,
  `ternary_subcritical_projection_cache.json`, and
  `ternary_subcritical_n20_gap.csv`;
- `ternary_supercritical_converse.json`,
  `ternary_supercritical_projection_cache.json`, and
  `ternary_supercritical_converse.csv`;
- the imported continuous comparison/cache, regenerated Fano CSV, and combined
  EPS/PNG.

## Remaining scope limitations

No task-required numerical value remains uncertified.  Three boundaries of the
claim are explicit:

1. The subcritical pair is numerically unique in all screens and local
   diagnostics, but no theorem-level uniqueness claim is made.
2. Supercritical minimax LPs were run through $n=25$, not for every later
   integer.  This covers every quoted point and the crossover; analytic
   monotonicity and the forward KL envelope certify the branch winner for all
   $n\ge25$.
3. Part C's historical optimiser-call counters and 425.176-second refinement
   runtime are source-run telemetry rather than quantities regenerated from the
   compact cache.  The saved values, cache identity, projections, formulae,
   and validation residuals were independently replayed.

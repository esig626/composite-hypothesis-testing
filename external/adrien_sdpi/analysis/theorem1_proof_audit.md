# Audit of Theorem 1 and Appendix C

## Audit boundary and source-control finding

The requested source `external/adrien_sdpi/Adrien_main.tex` is **not present in this
checkout** (and is not present in this repository's Git history).  Consequently I
could not honestly reconstruct its displayed proof line by line, resolve its exact
cross-references, inspect the cited Ordentlich paper from its bibliography, or check
the stated Z-channel and later-result dependencies.  This report therefore audits
the theorem and proof skeleton supplied in the task.  Every conclusion that depends
on unseen manuscript text is marked **SOURCE REQUIRED**.  No manuscript file was
created or altered.

## 1. Formal mathematical specification

Let \(\mathsf X,\mathsf Y\) be nonempty finite sets and
\(K\in\mathcal P(\mathsf Y\mid\mathsf X)\), i.e. \(K(y\mid x)\ge0\) and
\(\sum_yK(y\mid x)=1\) for every \(x\).  For \(\nu,\mu\in\mathcal P(\mathsf X)\),
write \((\nu K)(y)=\sum_x\nu(x)K(y\mid x)\), and analogously for \(\mu K\).

For \(1<\alpha<\infty\),
\[
 D_\alpha(\nu\mid\mu)=\frac1{\alpha-1}\log
 \sum_{x:\mu(x)>0}\mu(x)\left(\frac{\nu(x)}{\mu(x)}\right)^\alpha.
\]
Finiteness is equivalent to \(\nu\ll\mu\).  At \(\alpha=1\), use relative
entropy, again finite only for admissible \(\nu\ll\mu\).  At \(\alpha=\infty\),
\[
 D_\infty(\nu\mid\mu)=\log\max_{x:\mu(x)>0}\frac{\nu(x)}{\mu(x)},
\]
provided \(\nu\ll\mu\).  Thus the optimisation domain is
\[
 \mathcal A_\alpha=\{(\nu,\mu):\nu,\mu\in\mathcal P(\mathsf X),
 \ 0<D_\alpha(\nu\mid\mu)<\infty\}.
\]
In particular, diagonal pairs are excluded.

“Supported on a common set of at most two points” means that there is
\(A\subseteq\mathsf X\), \(|A|\le2\), such that
\(\nu(A)=\mu(A)=1\).  Under \(\nu\ll\mu\), this is equivalently
\(|\operatorname{supp}\nu\cup\operatorname{supp}\mu|\le2\).  A one-point
common support forces \(\nu=\mu\), hence is never admissible; the operative case
has exactly two points in the union.

The literal word “achieved” asserts both
\[
 \eta_\alpha(K)=\sup_{(\nu,\mu)\in\mathcal A_\alpha}
 \frac{D_\alpha(\nu K\mid\mu K)}{D_\alpha(\nu\mid\mu)}
 =\sup_{\substack{(\nu,\mu)\in\mathcal A_\alpha\\
 |\operatorname{supp}\nu\cup\operatorname{supp}\mu|\le2}}R_\alpha(\nu,\mu;K)
\]
and existence of an admissible binary pair at which the last supremum equals
\(\eta_\alpha(K)\).  Logically explicit: for every finite \(\mathsf X,\mathsf Y\),
every such \(K\), and every \(\alpha\in[1,\infty]\), there exist distinct
\(x,x'\) and \((\nu,\mu)\in\mathcal A_\alpha\), both carried by
\(\{x,x'\}\), such that \(R_\alpha(\nu,\mu;K)=\eta_\alpha(K)\).
That existence assertion does not follow from the supplied proof skeleton.

## 2. Reconstruction for \(1<\alpha<\infty\)

Put
\[
 H_\alpha(\nu\mid\mu)=\mathbb E_\mu[(d\nu/d\mu)^\alpha],\qquad
 M_\lambda=H_\alpha(\nu K\mid\mu K)-H_\alpha(\nu\mid\mu)^\lambda.
\]
Since \(D_\alpha=(\alpha-1)^{-1}\log H_\alpha\), for an admissible
non-diagonal pair,
\[
 R_\alpha>\lambda\quad\Longleftrightarrow\quad M_\lambda>0.
\]
The same equivalence with weak inequalities holds **for a fixed admissible pair**,
but an existential or supremum formulation with \(M_\lambda\ge0\) becomes
vacuous if diagonal pairs are admitted.

Fix an admissible pair and \(I=\operatorname{supp}\mu\).  Define
\(r_i=\nu(i)/\mu(i)\) and
\[
 \mathcal S=\{m\in\mathbb R^I:m_i\ge0,\ \sum_i m_i=1,
 \ \sum_i r_i m_i=1\},\qquad n_i=r_i m_i.
\]

1. **Compact convex polytope.**  \(\mathcal S\) is the intersection of finitely
   many closed half-spaces and two affine hyperplanes.  It is closed and convex;
   it lies in the bounded simplex, hence is compact and is a polytope.
2. **Nonempty.**  The original \(m=\mu\) belongs to it because
   \(\sum_i r_i\mu_i=\sum_i\nu_i=1\).
3. **Probability law.**  \(n_i\ge0\) and \(\sum_i n_i=1\); moreover
   \(n\ll m\).
4. **Output convexity.**  For each \(y\), set
   \(a_y(m)=\sum_i r_im_iK(y\mid i)\) and
   \(b_y(m)=\sum_i m_iK(y\mid i)\).  The perspective
   \((a,b)\mapsto a^\alpha b^{1-\alpha}\) is convex on \(a\ge0,b>0\), with
   its lower-semicontinuous boundary convention.  Thus
   \(H_\alpha(nK\mid mK)=\sum_y a_y(m)^\alpha b_y(m)^{1-\alpha}\) is convex.
5. **Input concavity.**  \(H_\alpha(n\mid m)=\sum_i r_i^\alpha m_i\) is affine
   and at least one.  Because \(t\mapsto t^\lambda\) is concave and increasing
   for \(0<\lambda<1\), its \(\lambda\)-power is concave.
6. Hence \(g(m)=H_\alpha(nK\mid mK)-H_\alpha(n\mid m)^\lambda\) is convex.
7. A continuous convex function on the compact polytope has a maximum.  Writing
   any maximiser as a convex combination of extreme points and applying convexity
   shows that some constituent extreme point has at least the same value.
8. **Precise extreme-point proof.**  If \(m\in\mathcal S\) has positive support
   \(J\) of size at least three, the homogeneous system
   \(\sum_{i\in J}h_i=0\), \(\sum_{i\in J}r_ih_i=0\) has a nonzero solution.
   For sufficiently small \(t>0\), both \(m\pm th\) are nonnegative, distinct,
   and in \(\mathcal S\), contradicting extremality.  Conversely, a feasible
   point supported on at most two indices is extreme unless the two constraint
   rows are dependent on that support; in the dependent case \(r_i=r_j=1\), and
   only the endpoint point masses are extreme.

For a two-point support \(\{i,j\}\) with \(r_i\ne r_j\), the unique weights are
\[
 m_i=\frac{r_j-1}{r_j-r_i},\qquad
 m_j=\frac{1-r_i}{r_j-r_i}.
\]
They are feasible precisely when \(1\) lies between \(r_i\) and \(r_j\); both
are positive precisely when \(1\) lies strictly between them.  One-point extreme
points are \(\delta_i\) with \(r_i=1\).

## 3. Logical defects and repairs

### 3.1 Threshold defect

For every diagonal pair, \(H_\alpha=H_\alpha^{\rm out}=1\), so \(M_\lambda=0\).
Therefore “\(\sup M_\lambda\ge0\)” says nothing.  The correct engine is:
for every \(0<\lambda<\eta_\alpha(K)\), choose an admissible pair with
\(R_\alpha>\lambda\), equivalently \(M_\lambda>0\).  Extreme-point reduction
gives a binary extreme point with \(g>0\), hence it cannot be diagonal, and its
ratio exceeds \(\lambda\).  Letting \(\lambda\uparrow\eta_\alpha(K)\) proves
equality of suprema and epsilon approximation, not attainment.

An extreme point has \(\widehat\nu=\widehat\mu\) exactly when \(r_i=1\) on its
support.  It then has \(g=0\).  Strict positivity automatically excludes it.

### 3.2 “Achieved” defect

The admissible domain deletes the diagonal and may delete boundary pairs with
infinite divergence; it is not compact.  A supremum can therefore occur only as a
diagonal or boundary limit.  The extreme-point argument is performed separately
for every threshold and supplies no single limiting admissible pair.  Accordingly,
“achieved” does **not** survive this audit.

The task describes a Z-channel proof taking \(\varepsilon\downarrow0\) to obtain
value one.  On those facts alone the limiting denominator either vanishes (a
diagonal limit) or leaves the finite-divergence domain (a boundary limit), so the
argument proves approach, not attainment.  Exact verification is **SOURCE
REQUIRED** because the Z-channel formula is absent.

A safe sufficient condition for genuine attainment is tautological but useful:
if some closed subset of binary admissible pairs bounded away from the diagonal
and from the infinite-divergence boundary contains a maximising sequence, then
continuity and compactness give a maximiser.  Strict positivity of all channel
entries alone does not prevent a diagonal maximising sequence.

### 3.3 Orders \(1\) and \(\infty\)

- **\(\alpha=1\): SOURCE REQUIRED.**  The supplied material only says that an
  Ordentlich et al. argument is invoked.  Without the missing citation and proof,
  neither equality nor existence may be attributed to that source.  The safe
  claim is at most equality/epsilon approximation, conditional on that reduction.
- **\(1<\alpha<\infty\):** the repaired strict-threshold argument above proves
  equality and epsilon approximation.
- **\(\alpha=\infty\):** the asserted constancy is false on \(\mathcal S\):
  \(D_\infty(rm\mid m)=\log\max_{i:m_i>0}r_i\), not
  \(\log\max_{i\in I}r_i\).  Removing a maximising atom changes it.  Requiring
  full support would restore constancy but would exclude extreme points, so it
  does not repair the proof.  A separate direct formula may prove binary
  reduction, but the later formula is **SOURCE REQUIRED**.  The supplied Appendix
  C skeleton does not establish the \(\infty\) case.

For \(0<\alpha<1\), the finite-order convexity changes: the perspective generating
\(H_\alpha\) is concave, while the sign and monotonic transformation in Rényi
divergence also change.  The argument above cannot simply be extended; no such
extension is claimed here.

## 4. Strongest justified replacement

For finite alphabets and \(1<\alpha<\infty\),
\[
 \eta_\alpha(K)=
 \sup_{\substack{(\nu,\mu)\in\mathcal A_\alpha\\
 |\operatorname{supp}\nu\cup\operatorname{supp}\mu|\le2}}
 R_\alpha(\nu,\mu;K).
\]
Equivalently, for every \(\epsilon>0\) there is an admissible common-binary pair
with ratio greater than \(\eta_\alpha(K)-\epsilon\).  This statement does not say
that the supremum is attained.  Extension to \(\alpha=1\) is conditional on
checking the missing Ordentlich source; extension to \(\infty\) requires the
missing later closed form or a new proof.

## 5. Downstream dependency audit

An exhaustive `rg` search could not be run on `Adrien_main.tex` because the path
does not exist.  Based only on the task's descriptions, changing “is achieved” to
“the supremum may be restricted” leaves any numerical evaluation of the
coefficient intact.  Every later phrase “an achieving distribution” must instead
be justified independently or changed to “an \(\epsilon\)-optimal distribution”.
The Z-channel limit is evidence for precisely this repair.  The \(D_\infty\)
closed-form result should precede, or independently prove, the order-\(\infty\)
binary statement to avoid circularity.

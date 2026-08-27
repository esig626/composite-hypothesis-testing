# Strengthening candidates for Theorem 1

## Candidate A1

**Type**  
Theorem

**Precise proposed statement**  
For finite \(\mathsf X,\mathsf Y\), \(K\in\mathcal P(\mathsf Y\mid\mathsf X)\),
and \(1<\alpha<\infty\), the unrestricted Rényi contraction coefficient equals
the supremum over admissible pairs carried by a common two-point subset of
\(\mathsf X\).  Equivalently, such pairs are \(\epsilon\)-optimal for every
\(\epsilon>0\).

**What improves**  
Repairs the unsupported attainment claim while preserving the exact reduction.

**Assumptions**  
Finite alphabets; finite-order Rényi divergence in the manuscript's orientation;
\(0<D_\alpha(\nu\mid\mu)<\infty\).

**Proof route**  
Use strict thresholds \(\lambda<\eta_\alpha(K)\), the fixed-likelihood-ratio
polytope, convex maximisation, and strict positivity to retain admissibility; then
let \(\lambda\uparrow\eta_\alpha(K)\).  This is Appendix C's machinery with the
threshold logic repaired.

**Audit status**  
PROVED FROM CURRENT MATERIAL

**Value**  
Main-result replacement for finite nonunit orders.

## Candidate A2

**Type**  
Lemma

**Precise proposed statement**  
For real \(r_1,\ldots,r_n\ge0\), every extreme point of
\(S_r=\{m\in\Delta_n:\sum_i r_im_i=1\}\) is either \(\delta_i\) with \(r_i=1\),
or is supported on \(\{i,j\}\), where \(1\) lies strictly between \(r_i,r_j\),
with
\[
 m_i=(r_j-1)/(r_j-r_i),\qquad m_j=(1-r_i)/(r_j-r_i).
\]
These and only these points are extreme (after removing duplicate descriptions).

**What improves**  
Makes the support reduction constructive and replaces an informal hyperplane
remark.

**Assumptions**  
Finite index set; nonnegative finite \(r_i\); nonempty \(S_r\).

**Proof route**  
Use the two-equation nullspace perturbation for supports of size at least three;
solve the two equations explicitly; handle the dependent case \(r_i=r_j=1\).
Winkler-type moment-set theorems provide external context but are unnecessary.

**Audit status**  
PROVED FROM CURRENT MATERIAL

**Value**  
Supporting lemma in Appendix C, also reusable elsewhere.

## Candidate A3

**Type**  
Corollary

**Precise proposed statement**  
Under Candidate A1, let
\(\mu_p^{x,x'}=p\delta_x+(1-p)\delta_{x'}\) and
\(\nu_q^{x,x'}=q\delta_x+(1-q)\delta_{x'}\).  Then
\[
 \eta_\alpha(K)=\max_{\{x,x'\}\subseteq\mathsf X}
 \sup_{(p,q)\in\mathcal B_\alpha}
 \frac{D_\alpha(\nu_q^{x,x'}K\mid\mu_p^{x,x'}K)}
 {D_\alpha(\nu_q^{x,x'}\mid\mu_p^{x,x'})},
\]
where for finite \(\alpha\),
\(\mathcal B_\alpha=\{(p,q):0<p<1,\ 0\le q\le1,\ q\ne p\}\).
Endpoint \(p=0\) or \(1\) cannot be non-diagonal and absolutely continuous.

**What improves**  
Turns a high-dimensional search into a finite row-pair search and a two-scalar
optimisation; the outer “max” is valid because there are finitely many pairs,
although the inner operation remains a supremum.

**Assumptions**  
Those of A1 and \(|\mathsf X|\ge2\).

**Proof route**  
Enumerate all two-point common supports and use the Bernoulli coordinates.  No new
mathematics beyond A1 is required.

**Audit status**  
PROVED FROM CURRENT MATERIAL

**Value**  
Useful computational corollary immediately after the theorem.

## Candidate A4

**Type**  
Proposition

**Precise proposed statement**  
Fix \(\delta,c,C>0\).  On binary pairs satisfying
\(D_\alpha(\nu\mid\mu)\ge\delta\), \(\mu(x),\mu(x')\ge c\), and (where needed)
all relevant output masses at least \(C\), the ratio is continuous and attains its
maximum.  Consequently, if a global maximising sequence remains in such a set,
the global coefficient has an admissible binary maximiser.

**What improves**  
Gives a rigorous sufficient attainment criterion and identifies exactly which
compactness failures must be excluded.

**Assumptions**  
Finite alphabets, finite \(\alpha\), and the displayed uniform separation.

**Proof route**  
Continuity of finite sums and logarithms plus Weierstrass.  Establishing intrinsic
channel conditions that force the separation is additional work.

**Audit status**  
PROVED WITH STANDARD EXTERNAL RESULT

**Value**  
Appendix proposition; the conditional formulation is correct but less elegant
than an intrinsic dichotomy.

## Candidate A5

**Type**  
Open direction

**Precise proposed statement**  
For each unordered input pair and finite \(\alpha>1\), compactify the closed
Bernoulli square by assigning to diagonal points the second-order local limit of
the Rényi ratio and to admissible boundary approaches their directional limits.
Prove that the resulting upper-semicontinuous envelope attains its maximum and
that this maximum equals \(\eta_\alpha(K)\).  Classify a maximiser as interior
(genuine attainment), diagonal (local contraction), or boundary.

**What improves**  
Would replace the false ordinary-attainment statement by a genuine compactified
attainment theorem and a useful nonattainment dichotomy.

**Assumptions**  
Finite alphabets; careful treatment of zero channel entries and path-dependent
boundary limits.

**Proof route**  
Taylor-expand both divergences around \(q=p\).  For a fixed full-support base law,
the common second-order factor \(\alpha/2\) suggests that the ratio limit is the
corresponding \(\chi^2\) contraction quotient.  Then analyse whether the limit is
direction-independent on a binary face and construct the upper-semicontinuous
envelope.  The local calculation is high-confidence; global boundary compatibility
is nontrivial.  Raginsky's functional SDPI representation is relevant context.

**Audit status**  
NONTRIVIAL OPEN PROOF TASK

**Value**  
Most promising deeper theorem; worthy of a dedicated appendix if completed.

## Candidate A6

**Type**  
Theorem

**Precise proposed statement**  
At \(\alpha=\infty\), express \(\eta_\infty(K)\) directly as an optimisation over
ordered pairs of channel rows using the manuscript's later closed form, and deduce
binary reduction and the criterion for value one without varying the support of a
fixed likelihood ratio.

**What improves**  
Replaces the invalid essential-supremum argument and may give a closed form.

**Assumptions**  
Exactly those of the unseen later theorem.

**Proof route**  
First verify the later theorem and its logical independence; then specialise its
row-pair formula.  The local-DP/\(E_\gamma\) literature may clarify interpretation,
but does not supply the missing formula.  The source file is required before a
precise formula can responsibly be stated.

**Audit status**  
NONTRIVIAL OPEN PROOF TASK

**Value**  
Potential main-result proof reorganisation; currently blocked by the absent source.

## Candidate A7

**Type**  
Proposition

**Precise proposed statement**  
Let \(A(m)\) be convex on every fixed-likelihood-ratio moment polytope and
\(B(m)>0\) affine.  If for every \(0<\lambda<1\),
\(A(m)-B(m)^\lambda\) is convex and the divergence ratio exceeds \(\lambda\)
exactly when this difference is positive, then the associated contraction
coefficient has a two-point equality-of-suprema reduction.

**What improves**  
Abstracts the proof beyond Rényi divergence.

**Assumptions**  
Finite input alphabet, one likelihood-ratio normalisation moment, the stated
convexity and exact strict-threshold equivalence, and admissibility preserved by
strict positivity.

**Proof route**  
Repeat A1 using A2.  Applications require checking the assumptions divergence by
divergence; Makur–Zheng comparison results do not alone establish exact reduction.

**Audit status**  
HIGH-CONFIDENCE PROOF CANDIDATE

**Value**  
Appendix abstraction after concrete cases are sound.

## Ranking and top proof tasks

| Rank | Candidate | Importance | Confidence | Ease | Paper usefulness | New machinery |
|---:|---|---|---|---|---|---|
| 1 | A1 corrected equality | Very high | Very high | Easy | Essential | Low |
| 2 | A3 Bernoulli formula | High | Very high | Easy | High/computational | Low |
| 3 | A2 constructive lemma | High | Very high | Easy | High/proof clarity | Low |
| 4 | A6 direct \(\infty\) theorem | Very high | Unresolved | Medium | Very high | Medium |
| 5 | A5 compactified attainment | Very high | Medium | Hard | High | High |
| 6 | A7 abstract theorem | Medium | High | Medium | Medium | Medium |
| 7 | A4 separated attainment | Medium | Very high | Easy | Medium | Low |

The top three concrete tasks are: (1) install A1 with strict thresholds; (2) add A2
and its explicit weights; (3) add A3 as the operational corollary.  In parallel,
once the missing source is supplied, the first research task should be to verify
and exploit the later \(\eta_\infty\) formula (A6).  Candidate A5 is the strongest
deeper theorem, but should not be claimed before its boundary analysis is complete.

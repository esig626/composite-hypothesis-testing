# Strengthening candidates for the dominated joint Rényi projection

## 1. Formalisation of the current result

This note analyses “Uniform Rényi bounds from a dominated projection”, its immediately preceding feasible one-sided derivative lemma, and the achievability result that consumes its moment bounds. Throughout,
\[
D_\lambda(Q\|P)=(\lambda-1)^{-1}\log Z_\lambda(Q,P),\qquad
Z_\lambda(Q,P)=\int q^\lambda p^{1-\lambda}\,d\mu,
\]
with (0<\lambda<1). Hence maximising (Z_\lambda), rather than minimising it, is equivalent to minimising (D_\lambda(Q\|P)).

### Ambient space, classes, and optimisation

* The measurable space is ((\mathcal X,\mathcal F)), with a σ-finite dominating measure (\mu). The functional ambient space is (L^1(\mu)), and
  \[
  \mathsf D_\mu=\{f\in L^1(\mu):f\ge0\ \mu\text{-a.e.},\ \int f\,d\mu=1\}.
  \]
* The density classes (\mathscr P,\mathscr Q\subset\mathsf D_\mu) are nonempty, ordinarily (linearly) convex, and weakly compact in (L^1(\mu)). Their law classes are (\mathcal P,\mathcal Q).
* For fixed (0<\lambda<1), the joint problem is
  \[
  z_\lambda^\star=\max_{(q,p)\in\mathscr Q\times\mathscr P}
  \int q^\lambda p^{1-\lambda}\,d\mu.
  \]
  A selected maximiser is ((q_\lambda^\star,p_\lambda^\star)). Existence is obtained from weak compactness and weak upper semicontinuity, rather than separately assumed. Positivity (z_\lambda^\star>0) is separately assumed.

### Extended likelihood ratio and supports

Let (P_\lambda^\star,Q_\lambda^\star) be the selected laws and (\xi=P_\lambda^\star+Q_\lambda^\star). With (a=dP_\lambda^\star/d\xi) and (b=dQ_\lambda^\star/d\xi),
\[
h_\lambda^\star=\begin{cases}
\log(b/a),&a,b>0,\\
-\infty,&a>0,b=0,\\
+\infty,&a=0,b>0,\\
0,&a=b=0.
\end{cases}
\]
Put
\[
C=\{p^\star>0,q^\star>0\},\ A=\{p^\star>0,q^\star=0\},\
B=\{p^\star=0,q^\star>0\},\ N=\{p^\star=q^\star=0\}.
\]
Feasible differentiation proves
\[
Q(A)=0\quad(\forall Q\in\mathcal Q),\qquad
P(B)=0\quad(\forall P\in\mathcal P).
\]
The extra assumption (R\ll P_\lambda^\star+Q_\lambda^\star) for every (R\in\mathcal P\cup\mathcal Q) supplies (R(N)=0). Therefore
\[
P\{h_\lambda^\star=+\infty\}=0\ (\forall P\in\mathcal P),\qquad
Q\{h_\lambda^\star=-\infty\}=0\ (\forall Q\in\mathcal Q).
\]

### The two uniform inequalities

With all quantifiers explicit, the result is
\[
\forall P\in\mathcal P:\quad
\mathbb E_Pe^{\lambda h_\lambda^\star}
=\int_Cp(q_\lambda^\star)^\lambda(p_\lambda^\star)^{-\lambda}\,d\mu
\le z_\lambda^\star,
\]
and
\[
\forall Q\in\mathcal Q:\quad
\mathbb E_Qe^{(\lambda-1)h_\lambda^\star}
=\int_Cq(q_\lambda^\star)^{\lambda-1}(p_\lambda^\star)^{1-\lambda}\,d\mu
\le z_\lambda^\star.
\]
Equality holds at (P_\lambda^\star) and (Q_\lambda^\star), respectively. Moreover,
\[
D_\lambda(Q_\lambda^\star\|P_\lambda^\star)=D_\lambda(\mathcal Q\|\mathcal P),\qquad
z_\lambda^\star=e^{(\lambda-1)D_\lambda(Q_\lambda^\star\|P_\lambda^\star)}.
\]

### Exact uses of assumptions

1. **Ordinary convexity** is used only to make the segments ((1-t)q^\star+tq) and ((1-t)p^\star+tp) feasible. Joint optimality makes (Z_\lambda) nonincreasing from (t=0) along each segment, exactly the premise of the derivative lemma. No α-convexity is used.
2. **Weak compactness** is used only for attainment. Norm continuity of (Z_\lambda), concavity, and norm-closed convex superlevel sets imply weak upper semicontinuity. It is not used after selecting a maximiser.
3. **Domination by (P^\star+Q^\star)** is used only to make every class law null on (N). The derivative lemma already handles (A) and (B). The proof therefore needs only (R(N)=0) for every class member.
4. **Positivity of (z_\lambda^\star)** is needed for the derivative lemma's hypothesis (0<F(y)<\infty) in both coordinates. Finiteness is automatic ((Z_\lambda\le1)). Positivity also makes the selected divergence finite and the negative-power certificates meaningful.

### Geometry versus supports versus testing

**A. Pure projection geometry:** concavity, attainment, coordinatewise optimality, feasible derivatives, and the supporting-functional inequalities.

**B. Variable-support machinery:** the restrictions on (A,B,N), the four-valued extended likelihood ratio, and the convention for sample vectors containing both infinities.

**C. Needed only later for testing:** the support statements in their probability form, tensorisation, Markov's inequality, blocklength (n), threshold calibration, rate (r), and comparison with the constant randomised test.

## 2. Strengthening directions investigated

The search treated separately: direct attainment and compact upper levels; tightness/coercivity and finite-dimensional compactness; Pythagorean and three-point inequalities; simultaneous variational inequalities, saddle points, and minimax identities; strictness, uniqueness, and equality faces; minimal/classwise support assumptions; ordinary versus α/geodesic convexity; continuity, stability, envelope derivatives and monotonicity in (\lambda); (\lambda>1), endpoint limits, and other (f)-divergences. In particular, an α-convex theorem was never treated as a theorem for ordinarily convex classes.

## 3. Serious literature candidates inspected

All 25 exact queries and retained IDs appear in `literature/theoremsearch_queries.md`. Similarity scores were used only for retrieval.

### L1. Kumar and Sason, *Projection Theorems for the Rényi Divergence on α-Convex Sets* (2016), arXiv:1512.02515v2

Proposition 1 (ID 21229205) gives the Pythagorean property; Theorem 1 (ID 21229206) gives existence of a forward (D_\alpha)-projection. This is a **one-class** projection of a fixed law onto an α-convex class, with total-variation closure and a finite-divergence feasibility condition in the existence result. It proves uniqueness where its hypotheses apply. It does not require blanket common full support, but finiteness/absolute-continuity qualifications remain relevant and it does not produce the manuscript's extended likelihood-ratio certificate. It is importable only as a separate stronger-geometry corollary, not as a two-class ordinary-convex theorem.

### L2. van Erven and Harremoës, *Rényi Divergence and Kullback–Leibler Divergence* (2014), arXiv:1206.2459v2

The inspected results were Theorem 12 (ID 22017173, convexity in the second argument), Theorem 14 (ID 22017175, α-convex Pythagorean inequality), Theorem 19 (ID 22017180, joint weak lower semicontinuity on Polish spaces), and the manuscript-cited total-variation continuity result. The Pythagorean theorem is one-class and α-convex. Theorem 19 supports a weak-compact-law existence alternative, but tightness alone must be supplemented by weak closedness and Prokhorov's hypotheses. These results allow zero densities in the extended divergence, but do not create the moment/support certificate. Fixed-pair continuity in order also does not imply optimiser continuity without a maximum theorem and uniqueness.

### L3. Ashok Kumar and Sundaresan, *Minimization Problems Based on Relative α-Entropy I: Forward Projection* (2015), arXiv:1410.2346v3

Theorem 8 (ID 21595954) gives existence/uniqueness and Theorem 10 (ID 21595956) gives a projection/Pythagorean property for **relative α-entropy** (\mathscr I_\alpha), not (D_\alpha), for a fixed reference law and a convex density set closed in (L^\alpha(\mu)). Import requires an escort transformation and verification of topology and supports. It is an analogy, not a direct theorem about the joint problem.

### L4. *Adversarial hypothesis testing and a quantum Stein's Lemma for restricted measurements* (2014), arXiv:1308.6702v4

Theorem 6 (ID 19908573) assumes closed convex distribution sets on a **finite domain** and identifies an adversarial exponent through minimisation of a pairwise Chernoff quantity. It may inform the finite-alphabet exponent discussion, but neither proves the fixed-order uniform moments nor supplies a measurable-space projection theorem.

No inspected candidate established a genuine two-class Rényi nearest-pair Pythagorean theorem, a varying-support extended-likelihood-ratio theorem, or differentiability of the selected pair. This is a residual-search statement, **not** a novelty claim.

## 4. Proposed results in the manuscript's notation

### Candidate S1 — attainment and minimal support

**Type:** Theorem.

**Proposed statement.** Fix (0<\lambda<1). Let (\mathscr P,\mathscr Q\subset\mathsf D_\mu) be nonempty and convex. Assume directly that a joint maximiser ((q_\lambda^\star,p_\lambda^\star)) exists, (z_\lambda^\star>0), and
\[
R\{p_\lambda^\star=q_\lambda^\star=0\}=0\qquad
\forall R\in\mathcal P\cup\mathcal Q.
\]
Then the extended (h_\lambda^\star) satisfies both support conclusions and both uniform moment inequalities of the current theorem, and the pair attains (D_\lambda(\mathcal Q\|\mathcal P)).

**Relation:** Replaces weak compactness by direct attainment and selected-pair domination by its strictly weaker, proof-exact consequence.

**Additional assumptions:** None beyond the statement; no common support.

**Proof route:** Start after attainment in the current proof. Convexity gives both segments; the existing derivative lemma supplies cross-support nullity and the integrals. The displayed condition handles (N). No external theorem is needed.

**Confidence:** **HIGH**. **Value:** strongest immediate measurable-space improvement and a cleaner separation of existence, geometry, and support.

### Candidate S2 — modular existence criteria

**Type:** Proposition with corollaries.

**Proposed statement.** Direct attainment in S1 follows if (i) the current weak (L^1)-compactness assumptions hold; or (ii) the product is weakly closed and some nonempty upper level ({Z_\lambda\ge c}) is weakly compact; or (iii) the classes are compact on a finite alphabet. On a Polish space, if the law product is weakly compact and a finite feasible divergence exists, weak lower semicontinuity yields a minimiser.

**Relation:** Adds weaker level-compactness/coercivity and law-level alternatives.

**Additional assumptions:** Weak upper semicontinuity for (ii); in the Polish version, weak closedness plus tightness may produce compactness by Prokhorov, while domination and S1's support condition remain separate.

**Proof route:** A maximising sequence is eventually in the compact upper level; take a convergent subnet and use upper semicontinuity. Use Weierstrass in finite dimensions. Import van Erven–Harremoës Theorem 19 for the law-level version.

**Confidence:** **HIGH** for (i)–(iii), **MEDIUM** for the general law-to-density transfer. **Value:** makes applications modular.

### Candidate S3 — equality as an exposed face

**Type:** Proposition.

**Proposed statement.** Define
\[
L_P(p)=\int_Cp(q^\star)^\lambda(p^\star)^{-\lambda}d\mu,\quad
L_Q(q)=\int_Cq(q^\star)^{\lambda-1}(p^\star)^{1-\lambda}d\mu.
\]
The laws attaining the respective uniform bounds are exactly
\[
\mathscr F_P=\{p:L_P(p)=z^\star\},\qquad
\mathscr F_Q=\{q:L_Q(q)=z^\star\}.
\]
Equality identifies the selected coordinate exactly when the corresponding exposed face is a singleton up to null sets.

**Relation:** Adds exact equality conditions without falsely equating moment equality with nonlinear uniqueness.

**Additional assumptions:** None.

**Proof route:** The current proof already identifies each moment with the linear functional. The assertion is then definitional. Equating these faces with all nonlinear maximisers would require a new argument and is not claimed.

**Confidence:** **HIGH**. **Value:** useful clarification, though short.

### Candidate S4 — simultaneous variational certificate

**Type:** Proposition.

**Proposed statement.** Suppose (p^\star,q^\star>0) (mu)-a.e. For nonempty convex classes, ((q^\star,p^\star)) jointly maximises (Z_\lambda) iff both uniform linear inequalities in S3 hold for every feasible (p,q).

**Relation:** Makes the necessary coordinate conditions a necessary-and-sufficient supporting-hyperplane characterisation under full support.

**Additional assumptions:** Strict positivity and integrability of the displayed derivatives.

**Proof route:** Necessity is the existing derivative argument. For sufficiency, integrate the tangent inequality for the concave weighted geometric mean:
\[
Z(q,p)-z^\star\le\lambda[L_Q(q)-z^\star]+(1-\lambda)[L_P(p)-z^\star]\le0.
\]
A boundary-supergradient extension requires new work and is not asserted.

**Confidence:** **HIGH** under the stated assumptions; **MEDIUM** at the boundary. **Value:** a clean finite-alphabet verification tool.

### Candidate S5 — uniqueness under equality rigidity

**Type:** Proposition.

**Proposed statement.** If equality in joint concavity of (Z_\lambda) between two feasible pairs implies that those pairs agree (mu)-a.e., then the joint projection is unique up to null sets. A checkable sufficient condition excludes distinct feasible pairs satisfying the pointwise equality condition for weighted-geometric-mean concavity.

**Relation:** Adds uniqueness under explicit strictness. Ordinary convexity alone is insufficient: if (\mathscr P\cap\mathscr Q) contains two laws, every common pair has (Z_\lambda=1).

**Additional assumptions:** Equality rigidity on the feasible product.

**Proof route:** Two maximisers force equality at their midpoint; rigidity identifies them. New work is needed to state the zero-sensitive pointwise equality condition.

**Confidence:** **HIGH** abstractly, **MEDIUM** for useful checkable conditions. **Value:** mainly a finite-alphabet corollary.

### Candidate S6 — finite-alphabet continuity and stability

**Type:** Corollary.

**Proposed statement.** On a finite alphabet, let the two classes be compact and every coordinate be uniformly at least (\varepsilon>0). Then
\[
v(\lambda)=\max_{Q,P}Z_\lambda(Q,P)
\]
is continuous on compact (I\subset(0,1)); the argmax correspondence is nonempty, compact-valued, and upper hemicontinuous. If the maximiser is unique for every (\lambda\in I), the selected pair is continuous on (I).

**Relation:** Adds order stability of the value and projection.

**Additional assumptions:** Finite alphabet, compactness, uniform full support; uniqueness only for selector continuity.

**Proof route:** Joint continuity is elementary under the lower bound. Apply Berge's maximum theorem; alternatively, prove the result sequentially using compactness and uniqueness.

**Confidence:** **HIGH**. **Value:** the most promising new corollary for order optimisation and the Hoeffding saddle-point section.

### Candidate S7 — finite-alphabet envelope derivative

**Type:** Proposition.

**Proposed statement.** Under S6, if the maximiser at (\lambda_0) is unique, then
\[
v'(\lambda_0)=\sum_x(Q_{\lambda_0}^\star(x))^{\lambda_0}
(P_{\lambda_0}^\star(x))^{1-\lambda_0}
\log\frac{Q_{\lambda_0}^\star(x)}{P_{\lambda_0}^\star(x)}.
\]
For (d(\lambda)=\log v(\lambda)/(\lambda-1)),
\[
d'(\lambda_0)=\frac{(\lambda_0-1)v'(\lambda_0)/v(\lambda_0)-\log v(\lambda_0)}{(\lambda_0-1)^2}.
\]
Without uniqueness, the one-sided derivatives are extrema of the partial derivative over the active argmax set, not a single formula.

**Relation:** Adds differentiability and an envelope formula.

**Additional assumptions:** S6 and uniqueness at the relevant order.

**Proof route:** Differentiate the finite sum and apply Danskin's theorem (or direct envelope inequalities); no derivative of the optimiser is required.

**Confidence:** **HIGH**. **Value:** may strengthen order optimisation and prepare, but does not itself prove, a (\lambda\to1) result.

### Candidate S8 — α-convex one-coordinate Pythagorean corollary

**Type:** Corollary under stronger geometry, not a replacement theorem.

**Proposed statement.** Fix (P_0). If (\mathcal Q) meets the Kumar–Sason hypotheses (including λ-convexity, total-variation closure, and finite feasibility), its forward (D_\lambda)-projection satisfies the source's Pythagorean inequality and uniqueness conclusion. An analogous fixed-(Q_0) statement requires separate verification of the geometry and divergence orientation in the second coordinate.

**Relation:** Adds a genuine Pythagorean inequality, but only for one coordinate and stronger geometry.

**Additional assumptions:** Exactly the external theorem's assumptions; ordinary convexity is not substituted for α-convexity.

**Proof route:** Translate Kumar–Sason Proposition 1 and Theorem 1 line by line, preserving (D_\lambda(Q\|P))'s order. Determine whether any manuscript example is λ-convex.

**Confidence:** **MEDIUM** pending the full orientation translation. **Value:** mathematically deep, but likely a separate remark/corollary.

### Candidate S9 — endpoints and (\lambda>1)

**Type:** Open direction, not a theorem.

**Proposed direction.** Seek uniform-in-pair expansions as (\lambda\uparrow1) and (\lambda\downarrow0) on compact full-support finite-alphabet classes, plus a convex-dual replacement for joint concavity when (\lambda>1).

**Relation:** Could connect selected projections to KL projections and improve the critical-rate discussion.

**Additional assumptions:** At least uniform full support for elementary uniform expansions; genuinely new geometry for (\lambda>1).

**Proof route:** Use uniform Taylor expansions and epi/argmin convergence on a finite alphabet. Do not reuse S1 for (\lambda>1): curvature and optimisation direction change. No inspected source supplies the required two-class theorem.

**Confidence:** **MEDIUM** for finite-alphabet endpoint convergence; **LOW** in general measurable spaces. **Value:** the most interesting deeper programme.

## 5. Why no general joint Pythagorean claim is proposed

The current inequalities support the concave Hellinger integral; they are not algebraically a three-point identity for (D_\lambda). The serious Pythagorean sources fix one argument and require α-convexity. Two coordinatewise first-order conditions do not combine into a two-class Pythagorean theorem under ordinary convexity. Accordingly, no such general theorem is claimed.

## 6. Prioritisation

Five is best except for “machinery”, where five means most new machinery.

| Rank | Candidate | Strength | Feasibility | Use | Correctness | Machinery |
|---:|---|---:|---:|---:|---:|---:|
| 1 | S1 minimal support/direct attainment | 5 | 5 | 5 | 5 | 1 |
| 2 | S6 continuity/stability | 4 | 5 | 5 | 5 | 2 |
| 3 | S4 simultaneous VI | 4 | 4 | 4 | 5 | 2 |
| 4 | S7 envelope derivative | 4 | 4 | 4 | 5 | 3 |
| 5 | S2 modular existence | 4 | 5 | 4 | 4 | 2 |
| 6 | S3 equality faces | 3 | 5 | 3 | 5 | 1 |
| 7 | S5 uniqueness/rigidity | 4 | 4 | 3 | 4 | 3 |
| 8 | S8 α-convex Pythagorean | 5 | 3 | 3 | 3 | 4 |
| 9 | S9 endpoints/(\lambda>1) | 5 | 2 | 5 | 2 | 5 |

### Top-three concrete next proof tasks

1. **S1:** Rewrite the proof with “a positive maximiser exists” as the only existence premise and (R\{p^\star=q^\star=0\}=0) as the support premise; check all four support cells.
2. **S6:** Prove joint continuity on (I\times\mathcal Q\times\mathcal P), then give a self-contained sequential proof of upper hemicontinuity and unique-selector continuity.
3. **S4:** Integrate the pointwise tangent inequality and verify derivative integrability; then investigate a boundary supergradient version without common support.

## 7. Short conclusion

* **Strongest immediately provable upgrade:** S1, because the existing proof uses weak compactness only for attainment and domination only on the joint-zero set.
* **Most interesting deeper upgrade:** S8/S9, a correctly oriented α-convex Pythagorean extension or endpoint/two-class dual theory; both need materially new machinery.
* **Most promising new corollary:** S6, continuity of the value and, under uniqueness, the projected pair on compact uniformly full-support finite-alphabet classes; S7 is its natural sequel.

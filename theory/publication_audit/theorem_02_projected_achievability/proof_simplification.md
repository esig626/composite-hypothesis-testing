# Proof-simplification audit: projected finite-blocklength achievability

## 1. Frozen invariant

This audit fixes $0<\lambda<1$ and changes no mathematical content. A $\sigma$--finite measure $\mu$ dominates every law in the nonempty classes $\mathcal P$ and $\mathcal Q$. The density sets $\mathcal D_\mu(\mathcal P)$ and $\mathcal D_\mu(\mathcal Q)$ are convex and weakly compact in $L^1(\mu)$. A projected pair $(Q_\lambda^\star,P_\lambda^\star)$ maximises $Z_\lambda(Q,P)$ over $\mathcal Q\times\mathcal P$, satisfies $Z_\lambda(Q_\lambda^\star,P_\lambda^\star)>0$, and satisfies $R\ll P_\lambda^\star+Q_\lambda^\star$ for every $R\in\mathcal P\cup\mathcal Q$.

The versions $a_\lambda^\star=dP_\lambda^\star/d(P_\lambda^\star+Q_\lambda^\star)$ and $b_\lambda^\star=dQ_\lambda^\star/d(P_\lambda^\star+Q_\lambda^\star)$ and the manuscript's four-case $h_\lambda^\star$ are frozen. The conclusions are precisely existence, the projection identity, the two stated uniform moments, the precise threshold-test consequences, and the displayed minimum with the constant randomised test. Ordinary convexity, varying supports, zero densities, divergence orientation, all constants and all quantifiers are preserved.

### Source-integrity finding

The current `manuscript/Manuscript.tex` invokes Lemma `lem:complete-feasible-directional-derivative` twice, but contains neither that lemma's statement nor an appendix proof with that label. Consequently, the current checked-in proof is not formally self-contained and cannot, literally, be “verified exactly” at those invocations. The two applications reveal the two conclusions required (no new support and the integral inequality), but do not establish them. This is a manuscript defect, not a defect in the frozen theorem. The editorial proof below invokes the same lemma and is rigorous only after its missing statement and proof are restored. No manuscript file is changed in this audit.

## 2. Current dependency map

| # | Step | Exact purpose | Necessary? | Only because supports vary? | Can combine? | Archive replacement | Failure if removed |
|---:|---|---|---|---|---|---|---|
| 1 | Norm continuity of $Z_\lambda$ | Makes each superlevel set norm closed. | Yes for the chosen existence route. | No. | With 2--3 in one paragraph. | No exact two-density statement returned. | Weak upper semicontinuity has not been justified. |
| 2 | Joint concavity | Makes the superlevel sets convex. | Yes for the chosen weak-closedness argument. | No. | With 1 and 3. | Returned results were positive/finite-dimensional or otherwise not exact at zero; direct scalar concavity is shorter. | Norm-closed superlevel sets need not be weakly closed by the cited convex-closure fact. |
| 3 | Weak upper semicontinuity | Provides the topological hypothesis for attainment. | Yes. | No. | With 1--2. | Theorem 24623723 is close but does not expose the relative-domain detail; elementary proof preferred. | Weak compactness alone does not make a merely norm-continuous functional attain its supremum. |
| 4 | Attainment | Produces the projected pair. | Yes. | No. | End of the existence paragraph. | Theorem 25275516 supplies the generic compact extreme-value step. | Conclusion 1 is unproved. |
| 5 | Maximising $Z_\lambda$ versus minimising $D_\lambda$ | Uses the negative factor $(\lambda-1)^{-1}$ to identify the composite infimum. | Yes. | No. | One sentence immediately after existence. | No external theorem needed. | Conclusion 2 is unproved or its order could be reversed. |
| 6 | Coordinatewise optimality | Permits every feasible segment in either class to be compared with the joint maximiser. | Yes. | No. | With 7--8 in a parallel display. | No useful exact archive result; it is immediate. | The derivative lemma's hypotheses are unavailable. |
| 7 | $Q$-coordinate one-sided derivative | Gives the $Q$ support restriction and the $Q$-weighted integral inequality. | Yes. | Its support part is. | Parallel with 8. | None exact. | The alternative-class moment bound and its boundary accounting fail. |
| 8 | $P$-coordinate one-sided derivative | Gives the $P$ support restriction and the $P$-weighted integral inequality. | Yes. | Its support part is. | Parallel with 7. | None exact. | The null-class moment bound and its boundary accounting fail. |
| 9 | Support restrictions | Prove that the infinite values which would make the relevant moments infinite have zero class mass. | Yes. | Yes. | State directly after the parallel applications. | No exact result returned. | Boundary contributions may be omitted incorrectly. |
| 10 | Domination on the joint-zero set | Removes the fourth-case set under every class law. | Yes for the exact four-case statistic and identities. | Yes. | Combine with 9. | No replacement needed; it is the assumption's direct consequence. | The value assigned on the joint-zero set could affect moments under a class law. |
| 11 | Pointwise extended likelihood ratio | Relates the four cases to ratios of projected $\mu$-densities. | Yes. | Yes. | With 9--12. | None returned. | The expectation identities are not justified for unequal supports. |
| 12 | Variational inequalities to moments | Identifies each expectation with the corresponding common-positive-support integral and bounds it by $Z_\lambda^\star$. | Yes. | Boundary bookkeeping is. | Both moments in one aligned display. | None exact. | Conclusions 3--4 fail. |
| 13 | Threshold-test lemma | Tensorises the single-letter bounds and supplies the exact threshold and two error bounds. | Yes. | No; the lemma itself handles extended scores. | With 14 in one closing paragraph. | Frozen internal lemma; it must not be reproved. | Conclusion 5 and the exponential candidate bound fail. |
| 14 | Constant randomised test | Supplies $1-\varepsilon$ and permits taking the exact minimum. | Yes. | No. | With 13. | No theorem needed. | The first branch of conclusion 6 is absent. |

The essential dependency chain is $1+2\Rightarrow3\Rightarrow4\Rightarrow5$ and $4+6\Rightarrow(7+8)\Rightarrow(9+10+11)\Rightarrow12\Rightarrow13\Rightarrow14$.

## 3. Existence audit

For nonnegative probability densities $p,\widetilde p,q,\widetilde q$, insert and subtract $\widetilde q^\lambda p^{1-\lambda}$. The scalar inequality $|u^a-v^a|\leq|u-v|^a$, valid for $u,v\geq0$ and $0<a<1$, and Hölder with conjugate exponents $1/\lambda$ and $1/(1-\lambda)$ give

$$
\begin{aligned}
|Z_\lambda(q,p)-Z_\lambda(\widetilde q,\widetilde p)|
&\leq \int |q^\lambda-\widetilde q^\lambda|p^{1-\lambda}\,d\mu
 +\int \widetilde q^\lambda|p^{1-\lambda}-\widetilde p^{1-\lambda}|\,d\mu\\
&\leq \left(\int|q-\widetilde q|\,d\mu\right)^\lambda
       \left(\int p\,d\mu\right)^{1-\lambda}\\
&\quad+\left(\int\widetilde q\,d\mu\right)^\lambda
       \left(\int|p-\widetilde p|\,d\mu\right)^{1-\lambda}\\
&=\|q-\widetilde q\|_1^\lambda+\|p-\widetilde p\|_1^{1-\lambda}.
\end{aligned}
$$

Thus the displayed estimate in the manuscript is valid. The scalar power inequality includes zero and follows, for example, from subadditivity $(v+(u-v))^a\leq v^a+(u-v)^a$ after ordering $u\geq v$. Each Hölder use is legitimate even on a $\sigma$--finite space because the powered factors have integrals $\|q-\widetilde q\|_1$, $\int p=1$, $\int\widetilde q=1$, and $\|p-\widetilde p\|_1$.

The map $(u,v)\mapsto u^\lambda v^{1-\lambda}$ is jointly concave on $[0,\infty)^2$ (including its boundary), so integration makes $Z_\lambda$ jointly concave on nonnegative density pairs. Its superlevel sets, relative to the product density domain, are therefore convex. Norm continuity makes them relatively norm closed. A convex norm-closed set in a normed space is weakly closed (equivalently, use separation); hence those superlevel sets are relatively weakly closed and $Z_\lambda$ is weakly upper semicontinuous on the product.

The finite product of the two weakly compact density classes is compact in the product of their weak topologies, which is the weak topology of the finite Banach product. Since $0\leq Z_\lambda\leq1$ by Hölder, the functional is finite. A finite weakly upper-semicontinuous function attains its maximum on that product. This is the shortest safe existence proof: one paragraph containing the estimate, joint concavity/superlevel-set argument, and compact attainment. It neither needs an ambient density symbol beyond the two given density classes nor any support assumption.

## 4. Retained archive results

The exact query strings, full returned statements, metadata, IDs, scores, and all 300 returned-result identifiers appear in `theoremsearch_queries.md`.

* **Theorem 17853360, “Theorem A.4 (Mazur’s lemma)”**: the returned statement says that a convex subset of a normed space is weakly closed iff it is closed. It exactly replaces only the convex norm-closed $\Rightarrow$ weakly closed substep.
* **Theorem 25275516, Proposition E.2**: the returned statement says an upper-semicontinuous function achieves its maximum on a compact subset. It exactly replaces only generic attainment.
* **Theorem 24623723, Lemma 2**: the returned statement equates norm and weak upper semicontinuity for a concave real-valued function on a normed space. Because the present functional is used on a relative density domain and the archive statement exposes no relative-domain qualification, it is **INSUFFICIENT FROM THEOREM ARCHIVE** as a stand-alone replacement.
* **Theorem 21229206, Theorem 1**: the returned R\'enyi projection theorem fixes one law and uses an $\alpha$-convex set. It is **CHANGES THE MATHEMATICS** here.

No retained or rejected statement exposes the complete boundary lemma needed here: zero densities, possible infinite raw directional slopes, the no-new-support conclusion, integrability, the exact weighted integral inequality, and the derivative orientation. Therefore no exact archived theorem replaces the technical derivative lemma.

## 5. Route comparison

| Proof route | External theorem required | Exact same theorem? | Handles zero densities? | Handles varying supports? | Logical steps | Clarity | Risks | Recommendation |
|---|---|---|---|---|---|---|---|---|
| A. Coordinatewise feasible derivatives | No; use the internal complete one-sided derivative lemma | Yes | Yes | Yes | Existence, two segment inequalities, two lemma applications, support accounting, two moments | Direct and symmetric | Current manuscript is missing the invoked lemma and proof | **RECOMMENDED** |
| B. Standard variational inequality | A boundary-valid extended-direction theorem | No such exact statement returned | Not visibly | Not visibly | Superficially fewer | Familiar notation | Differentiability/interior assumptions suppress the singular support term | **CHANGES THE MATHEMATICS** |
| C. Supergradient/normal cone | An $L^1$ extended-valued boundary supergradient theorem | No exact statement returned | Not established | Not established | Potentially compact, actually requires domain and normal-cone bookkeeping | More abstract | A finite supergradient need not exist at a zero density | **INSUFFICIENT FROM THEOREM ARCHIVE** |
| D. Known R\'enyi projection theorem | Two-class ordinary-convex varying-support projection/Pythagorean theorem in the same orientation | No | Returned statements do not establish this | Returned statements do not establish this | Could replace much only if exact | Attractive but misleading here | Fixed law, $\alpha$-convexity, finite/positive support, or orientation changes | **CHANGES THE MATHEMATICS** |
| E. Direct support-partition presentation | No new theorem; still uses the internal derivative lemma | Yes | Yes | Yes | Same mathematics as A, fewer named objects | Shortest without hiding boundaries | Must state all three null-set facts explicitly | **RECOMMENDED** |

Route E is the editorial form of Route A, not an independent mathematical proof. A differentiable supporting-hyperplane statement that assumes an open domain, an interior maximiser, strictly positive densities, or a finite derivative is **CHANGES THE MATHEMATICS**, because $u^\alpha$ has an infinite right derivative at zero. Omitting the resulting singular support condition would be **INCORRECT**.

## 6. Derivative-lemma audit

1. **Exact sufficiency.** The intended complete feasible one-sided derivative lemma is exactly sufficient if it assumes $0<F(y)<\infty$, segment maximality $F((1-t)y+tx)\leq F(y)$ for $0\leq t\leq1$, and concludes (i) $\mu(\{w>0,y=0,x>0\})=0$, (ii) integrability and $\int_{\{y>0\}}wy^{\alpha-1}x\,d\mu\leq F(y)$, and (iii) the stated derivative limit. Positivity of the projected Hellinger integral supplies $F(y)>0$, and Hölder supplies finiteness.
2. **Conclusions used.** The theorem proof uses conclusions (i) and (ii). Integrability is part of making (ii) meaningful. It does not use conclusion (iii).
3. **Derivative limit.** The limit formula is not needed in this theorem; only no-new-support and the integral inequality are needed. It may remain because it explains the lemma's name and is independently useful, but it is editorially surplus here.
4. **Possible shortening.** The theorem-facing statement could be shortened to the first two conclusions, but doing so changes the content of the numbered lemma. Under the frozen task, retain its complete content and merely avoid repeating its derivative calculation in the theorem proof.
5. **Placement.** It should remain a separately numbered appendix lemma because its boundary-support argument is nonstandard, is invoked twice, and is too long to conceal in the theorem proof. In the current file it must first be restored: presently the label and appendix proof are absent.
6. **Archive replacement.** None is exact; the answer is **INSUFFICIENT FROM THEOREM ARCHIVE**.
7. **Symmetry.** The applications can and should be displayed in parallel, with $(\alpha,w,y,x)=(\lambda,(p_\lambda^\star)^{1-\lambda},q_\lambda^\star,q)$ and $(1-\lambda,(q_\lambda^\star)^\lambda,p_\lambda^\star,p)$.

## 7. Support audit

Fix $q=dQ/d\mu$ and $p=dP/d\mu$.

1. The $Q$-coordinate lemma gives
   $\mu(\{x\in\mathcal X:p_\lambda^\star(x)>0,q_\lambda^\star(x)=0,q(x)>0\})=0$.
   Since $q=0$ $\mu$-almost everywhere on the complement of its positivity set, this is equivalent to
   $Q(\{x\in\mathcal X:p_\lambda^\star(x)>0,q_\lambda^\star(x)=0\})=0$.
2. The $P$-coordinate lemma analogously gives
   $P(\{x\in\mathcal X:p_\lambda^\star(x)=0,q_\lambda^\star(x)>0\})=0$.
3. The set $\{x\in\mathcal X:p_\lambda^\star(x)=q_\lambda^\star(x)=0\}$ is $(P_\lambda^\star+Q_\lambda^\star)$-null. The assumed $R\ll P_\lambda^\star+Q_\lambda^\star$ therefore makes it $R$-null for every $R\in\mathcal P\cup\mathcal Q$.
4. Hence $h_\lambda^\star=+\infty$ occurs only on a $P$-null set for every $P\in\mathcal P$, $h_\lambda^\star=-\infty$ occurs only on a $Q$-null set for every $Q\in\mathcal Q$, and its assigned value $0$ on the joint-zero set is immaterial under every class law. The four-case statistic remains measurable and operational.
5. For $P$, the $b=0<a$ region contributes $e^{-\infty}=0$, the $a=0<b$ region is $P$-null, and the joint-zero region is $P$-null. For $Q$, the $a=0<b$ region contributes $e^{(\lambda-1)(+\infty)}=0$, the $b=0<a$ region is $Q$-null, and the joint-zero region is $Q$-null. Thus the two common-positive-support integral identities omit no contribution.
6. Because $P_\lambda^\star+Q_\lambda^\star$ has $\mu$-density $p_\lambda^\star+q_\lambda^\star$, the Radon--Nikodym versions can be selected as $p_\lambda^\star/(p_\lambda^\star+q_\lambda^\star)$ and $q_\lambda^\star/(p_\lambda^\star+q_\lambda^\star)$ where the denominator is positive, and both set to zero elsewhere. These are measurable versions.

## 8. Clunkiness answers

1. Local notation $p_\lambda^\star,q_\lambda^\star$ is necessary: it makes the two lemma applications and pointwise support argument legible.
2. A named common-positive-support set is unnecessary; full measurable-set notation is clearer at the two points where it is used.
3. A local $z_\lambda^\star$ is unnecessary; writing $Z_\lambda(Q_\lambda^\star,P_\lambda^\star)$ avoids another symbol.
4. Yes, existence fits rigorously in one paragraph.
5. Yes, the coordinate perturbations can be parallel.
6. Yes, support restrictions can be stated directly, but none may be omitted.
7. Yes, the two moments should share one aligned display.
8. Prove the projection identity immediately after existence; it then identifies the common moment constant.
9. Positivity needs one short explanation before the derivative lemma (its $F(y)>0$ hypothesis) and, before the threshold lemma, only the consequence that the divergence is finite and nonnegative. The latter also follows from $0<Z_\lambda\leq1$.
10. Yes, threshold and constant-test applications fit in one final paragraph, provided both candidate bounds are shown.
11. Only the final minimax equation needs the theorem's existing label. The segment inequalities, support restrictions, moments, threshold, and candidate error bounds are used locally and need no labels.
12. Yes. Material reduction is possible by parallelising the two coordinates, eliminating named support sets and a projected-$Z$ abbreviation, sharing the moment display, and compressing the closing application. The support argument itself cannot be reduced below its three null-set facts.

## 9. Recommended proof architecture

Use Route A in Route E's presentation:

1. one existence paragraph (continuity estimate, concavity, weak upper semicontinuity, compact attainment);
2. one sentence for the projection identity;
3. local projected densities, followed by one parallel display of the two feasible segments and the two derivative-lemma substitutions;
4. direct statement of both class-specific boundary restrictions and the domination consequence;
5. one sentence selecting the Radon--Nikodym versions and one aligned display for both expectations;
6. one closing paragraph invoking the threshold lemma and the constant randomised test.

This removes or absorbs seven presentation elements while retaining all fourteen logical dependencies.

## 10. Proposed IEEE-compatible LaTeX proof

The exact result being editorially rewritten is Theorem `thm:projected-finite-blocklength-achievability`. The mathematical reason for the rewrite is solely to parallelise its two coordinate arguments and consolidate support bookkeeping; the missing technical lemma must remain separately available.

```latex
\begin{IEEEproof}
For probability densities $p,\widetilde p,q,\widetilde q$ with respect to
$\mu$, the inequality $|u^a-v^a|\leq|u-v|^a$ for $u,v\geq0$ and
$0<a<1$, followed twice by H\"older's inequality, gives
\begin{equation*}
\begin{aligned}
|Z_\lambda(q,p)-Z_\lambda(\widetilde q,\widetilde p)|
&\leq
\int_{\mathcal X}|q-\widetilde q|^\lambda p^{1-\lambda}\,d\mu
+
\int_{\mathcal X}\widetilde q^\lambda
|p-\widetilde p|^{1-\lambda}\,d\mu\\
&\leq
\|q-\widetilde q\|_1^\lambda
+
\|p-\widetilde p\|_1^{1-\lambda}.
\end{aligned}
\end{equation*}
Thus $Z_\lambda$ is norm continuous. Since
$(u,v)\mapsto u^\lambda v^{1-\lambda}$ is jointly concave on
$[0,+\infty)^2$, the superlevel sets of $Z_\lambda$ are convex and norm
closed, hence weakly closed. Therefore $Z_\lambda$ is weakly upper
semicontinuous and attains its maximum on the weakly compact product
$\mathcal D_\mu(\mathcal Q)\times\mathcal D_\mu(\mathcal P)$. A
projected pair consequently exists.

Because $\lambda-1<0$, maximising $Z_\lambda$ is equivalent to minimising
$D_\lambda$. Hence
\begin{equation*}
D_\lambda(Q_\lambda^\star\|P_\lambda^\star)
=
D_\lambda(\mathcal Q\|\mathcal P).
\end{equation*}

Set $p_\lambda^\star=dP_\lambda^\star/d\mu$ and
$q_\lambda^\star=dQ_\lambda^\star/d\mu$. Fix $P\in\mathcal P$ and
$Q\in\mathcal Q$, and set $p=dP/d\mu$ and $q=dQ/d\mu$. Coordinatewise
optimality and convexity give, for every $0\leq t\leq1$,
\begin{equation*}
\begin{aligned}
\int_{\mathcal X}
\bigl((1-t)q_\lambda^\star+tq\bigr)^\lambda
(p_\lambda^\star)^{1-\lambda}\,d\mu
&\leq Z_\lambda(Q_\lambda^\star,P_\lambda^\star),\\
\int_{\mathcal X}
(q_\lambda^\star)^\lambda
\bigl((1-t)p_\lambda^\star+tp\bigr)^{1-\lambda}\,d\mu
&\leq Z_\lambda(Q_\lambda^\star,P_\lambda^\star).
\end{aligned}
\end{equation*}
Since $0<Z_\lambda(Q_\lambda^\star,P_\lambda^\star)\leq1$,
Lemma~\ref{lem:complete-feasible-directional-derivative} applies to these
lines with
\begin{equation*}
\begin{aligned}
(\alpha,w,y,x)
&=\bigl(\lambda,(p_\lambda^\star)^{1-\lambda},
q_\lambda^\star,q\bigr),\\
(\alpha,w,y,x)
&=\bigl(1-\lambda,(q_\lambda^\star)^\lambda,
p_\lambda^\star,p\bigr),
\end{aligned}
\end{equation*}
and yields
\begin{equation*}
\begin{aligned}
Q\bigl(\{x\in\mathcal X:p_\lambda^\star(x)>0,
q_\lambda^\star(x)=0\}\bigr)&=0,\\
P\bigl(\{x\in\mathcal X:p_\lambda^\star(x)=0,
q_\lambda^\star(x)>0\}\bigr)&=0,
\end{aligned}
\end{equation*}
together with
\begin{equation*}
\begin{aligned}
\int_{\{x\in\mathcal X:p_\lambda^\star(x)>0,
q_\lambda^\star(x)>0\}}
q(x)(q_\lambda^\star(x))^{\lambda-1}
(p_\lambda^\star(x))^{1-\lambda}\,d\mu(x)
&\leq Z_\lambda(Q_\lambda^\star,P_\lambda^\star),\\
\int_{\{x\in\mathcal X:p_\lambda^\star(x)>0,
q_\lambda^\star(x)>0\}}
p(x)(q_\lambda^\star(x))^\lambda
(p_\lambda^\star(x))^{-\lambda}\,d\mu(x)
&\leq Z_\lambda(Q_\lambda^\star,P_\lambda^\star).
\end{aligned}
\end{equation*}
Moreover, $R\ll P_\lambda^\star+Q_\lambda^\star$ implies
\begin{equation*}
R\bigl(\{x\in\mathcal X:p_\lambda^\star(x)=0,
q_\lambda^\star(x)=0\}\bigr)=0
\qquad \forall R\in\mathcal P\cup\mathcal Q.
\end{equation*}

The measurable versions in the theorem may be chosen as
$p_\lambda^\star/(p_\lambda^\star+q_\lambda^\star)$ and
$q_\lambda^\star/(p_\lambda^\star+q_\lambda^\star)$ where the denominator
is positive, and both may be set to zero elsewhere. The four cases defining
$h_\lambda^\star$, the preceding three null-set conclusions, and the two
integral inequalities therefore give
\begin{equation*}
\begin{aligned}
\mathbb E_P\left[e^{\lambda h_\lambda^\star}\right]
&=
\int_{\{x\in\mathcal X:p_\lambda^\star(x)>0,
q_\lambda^\star(x)>0\}}
p(x)(q_\lambda^\star(x))^\lambda
(p_\lambda^\star(x))^{-\lambda}\,d\mu(x)\\
&\leq Z_\lambda(Q_\lambda^\star,P_\lambda^\star),\\
\mathbb E_Q\left[e^{(\lambda-1)h_\lambda^\star}\right]
&=
\int_{\{x\in\mathcal X:p_\lambda^\star(x)>0,
q_\lambda^\star(x)>0\}}
q(x)(q_\lambda^\star(x))^{\lambda-1}
(p_\lambda^\star(x))^{1-\lambda}\,d\mu(x)\\
&\leq Z_\lambda(Q_\lambda^\star,P_\lambda^\star).
\end{aligned}
\end{equation*}
Taking the respective suprema and using
$Z_\lambda(Q_\lambda^\star,P_\lambda^\star)
=e^{(\lambda-1)D_\lambda(\mathcal Q\|\mathcal P)}$ proves the two
uniform expectation bounds.

Positivity of the projected Hellinger integral and H\"older's inequality
imply $0\leq D_\lambda(\mathcal Q\|\mathcal P)<+\infty$.
Lemma~\ref{lem:uniform-score-achievability}, with
$h=h_\lambda^\star$, $d=D_\lambda(\mathcal Q\|\mathcal P)$, and
\begin{equation*}
\tau=
\frac{\log(1/\varepsilon)-n(1-\lambda)
D_\lambda(\mathcal Q\|\mathcal P)}{\lambda},
\end{equation*}
gives
\begin{equation*}
\begin{aligned}
\alpha_n(\psi_{n,\tau};\mathcal P)&\leq\varepsilon,\\
\beta_n(\psi_{n,\tau};\mathcal Q)
&\leq
\exp\left[-\frac{1-\lambda}{\lambda}
\left(nD_\lambda(\mathcal Q\|\mathcal P)
-\log\frac{1}{\varepsilon}\right)\right].
\end{aligned}
\end{equation*}
The constant randomised test $\varphi_n(x^n)=\varepsilon$ for every
$x^n\in\mathcal X^n$ has Type I error $\varepsilon$ and Type II error
$1-\varepsilon$. Taking the smaller candidate bound proves
\begin{equation}
\begin{aligned}
\beta_n^\star(\varepsilon;\mathcal P,\mathcal Q)
\leq\min\Bigg\{&1-\varepsilon,
\exp\left[-\frac{1-\lambda}{\lambda}
\left(nD_\lambda(\mathcal Q\|\mathcal P)
-\log\frac{1}{\varepsilon}\right)\right]\Bigg\}.
\end{aligned}
\label{eq:projected-finite-blocklength-achievability}
\end{equation}
\end{IEEEproof}
```

## 11. Line-by-line equivalence audit

| Current object or step | Proposed treatment | Classification | Why safe or unsafe |
|---|---|---|---|
| Ambient density set $\mathcal D_\mu$ | The two theorem density classes remain explicit; no extra ambient symbol is introduced. | Logically redundant | Nonnegativity and unit integral are used directly, while compactness and convexity remain attached to the frozen classes. |
| $z_\lambda^\star$ | No abbreviation; the full projected Hellinger integral is written. | Logically redundant | It names a quantity used only a few times and carries no mathematical content. |
| Named support sets | Replaced by full measurable-set notation at every measure and integral. | Absorbed into another step | All three partitions and their null-mass roles remain explicit. |
| Explicit support conclusions in the theorem statement | Not added or removed from the frozen statement; they remain proof consequences used for moments. | Not safe to remove | Removing them from the proof would conceal why extended exponential moments have no infinite boundary contribution. |
| Repeated block-score definitions | Not repeated; Lemma `lem:uniform-score-achievability` is invoked. | Moved to the technical lemma | The internal threshold lemma already defines and handles the block score, including conflicting infinities. |
| Old projected-achievability corollary | Not recreated. | Logically redundant | The current frozen theorem already contains the exact finite-blocklength consequence. No new or old corollary is needed to prove it. |
| Equation labels | Only the final theorem bound retains its referenced label. | Logically redundant | All other displays are consumed immediately and are not cross-referenced. |
| Coordinatewise derivative calculation | Replaced by two parallel substitutions into the complete feasible derivative lemma. | Moved to the technical lemma | Recalculation would duplicate the lemma. The lemma itself is not safe to remove and is currently missing from the manuscript. |
| Separate $Q$ and $P$ perturbation paragraphs | Combined into one parallel block. | Absorbed into another step | Convexity, segment optimality, parameters, support conclusions and inequalities remain distinct rows. |
| Separate expectation displays | Combined into one aligned display. | Absorbed into another step | The orientations and exponents remain explicit. |
| Separate positivity paragraph | Its two uses are placed at the derivative invocation and threshold invocation. | Absorbed into another step | Neither positivity nor finiteness is lost. |
| Separate projected-test and constant-test paragraphs | Combined in the closing paragraph. | Absorbed into another step | Both candidate bounds and the minimum remain explicit. |

Counting presentation-level objects rather than indispensable logical facts, seven elements are removed or absorbed: the projected-$Z$ abbreviation, named support sets, repeated block-score material, surplus local equation labels, separate coordinate paragraphs, separate moment displays, and separate closing-test paragraphs. The derivative lemma, its support conclusions, the density notation, and the projection identity are not removed.

### Verification verdict

Conditional on restoring the referenced complete feasible one-sided derivative lemma with the hypotheses and conclusions described in Section 6, every inference in the theorem proof is valid, the expectation orientations are correct, and the final constants agree with the frozen display. As checked in the repository, however, the proof is formally incomplete because that lemma and its appendix proof are absent.

## 12. OPTIONAL MATHEMATICAL SUGGESTION — NOT PART OF THE EDITORIAL REWRITE

No strengthening is recommended in this audit. Questions of weaker compactness, uniqueness, a Pythagorean inequality, continuity in $\lambda$, or relaxed domination require separate mathematical work. In particular, no failure of TheoremSearch to return an exact theorem supports a novelty claim, and none of those possibilities is inserted into the proposed theorem or proof.

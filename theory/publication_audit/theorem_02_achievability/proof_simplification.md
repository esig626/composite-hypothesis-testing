# Proof-simplification audit: abstract finite-blocklength achievability

## 1. Frozen mathematical invariant

### Passage audited and reason

The source passage is Theorem `thm:uniform-renyi-achievability` and its immediately following proof in `manuscript/Manuscript.tex`. The editorial issue is that the current theorem uses $e^{-nr}$, separately assumes support properties already forced by its finite moment bounds, and names several objects that can be handled locally. The audit asks whether those presentational layers can be removed while preserving the measure-theoretic argument and its arbitrary-threshold estimate. The manuscript itself is not edited.

### Invariant that may not change

Let $(\mathcal X,\mathcal F)$ be the manuscript's measurable space and let $\mathcal P$ and $\mathcal Q$ be its nonempty classes of probability laws. Fix every integer $n\ge1$, every $\varepsilon\in(0,1)$, every $\lambda\in(0,1)$, and every $d\ge0$. Let $h:\mathcal X\to[-\infty,+\infty]$ be measurable and assume exactly

$$
\sup_{P\in\mathcal P}\mathbb E_P[e^{\lambda h}]
\le e^{(\lambda-1)d},
\qquad
\sup_{Q\in\mathcal Q}\mathbb E_Q[e^{(\lambda-1)h}]
\le e^{(\lambda-1)d}.
$$

For every $\tau\in\mathbb R$, define $\psi_{n,\tau}(x^n)=\mathbf 1\{\sum_{i=1}^nh(x_i)\ge\tau\}$, with the sum set to zero precisely on sequences on which both signs of infinity occur. If

$$
\tau\ge \frac{\log(1/\varepsilon)-n(1-\lambda)d}{\lambda},
$$

then the two conclusions are exactly

$$
\alpha_n(\psi_{n,\tau};\mathcal P)\le\varepsilon,
\qquad
\beta_n(\psi_{n,\tau};\mathcal Q)
\le e^{(1-\lambda)\tau+n(\lambda-1)d}.
$$

The arbitrary-$\tau$ Type II estimate remains part of the result. Consequently, and with no other achievability bound introduced,

$$
\beta_n^\star(\varepsilon;\mathcal P,\mathcal Q)
\le\min\left\{1-\varepsilon,
\exp\left\{-\frac{1-\lambda}{\lambda}
\left[nd-\log\frac1\varepsilon\right]\right\}\right\}.
$$

No likelihood-ratio interpretation of $h$, real-valuedness, finite alphabet, domination, convexity, compactness, projection, or further assumption is allowed. The threshold is the general $\varepsilon$ threshold. All quantifiers, constants, strict/weak threshold events, and the mixed-infinity convention are frozen.

## 2. Equivalence with the current $e^{-nr}$ result

### Threshold

Put $\varepsilon=e^{-nr}$, so $\log(1/\varepsilon)=nr$. Then

$$
\frac{\log(1/\varepsilon)-n(1-\lambda)d}{\lambda}
=\frac{n[r-(1-\lambda)d]}{\lambda},
$$

which is exactly the current $\tau_{\lambda,r}^{\min}$ after renaming the current $D$ as the target $d$.

### Final bound

Under the same substitution,

$$
\begin{aligned}
1-\varepsilon&=1-e^{-nr},\\
-\frac{1-\lambda}{\lambda}
\left[nd-\log\frac1\varepsilon\right]
&=-n\frac{1-\lambda}{\lambda}(d-r).
\end{aligned}
$$

Thus the target minimum is exactly the current minimum, again with $D=d$.

### Support conditions follow from the moment assumptions

The common right-hand side $e^{(\lambda-1)d}$ is finite and positive. Hence each individual moment in either supremum is finite.

For $P\in\mathcal P$, $e^{\lambda h}=+\infty$ on $\{h=+\infty\}$ because $\lambda>0$. A nonnegative extended-valued measurable function with finite integral is finite almost surely: indeed, if $P\{h=+\infty\}>0$, then $e^{\lambda h}\ge M\mathbf1_{\{h=+\infty\}}$ for every $M>0$, forcing its integral to be at least $MP\{h=+\infty\}$ for every $M$ and hence infinite. Therefore $P\{h=+\infty\}=0$.

For $Q\in\mathcal Q$, $\lambda-1<0$, so $e^{(\lambda-1)h}=+\infty$ on $\{h=-\infty\}$. The same argument gives $Q\{h=-\infty\}=0$. These are exactly the two current support assumptions, so their removal adds no admissible score.

### Mixed-infinity convention is error-neutral

For coordinate maps $h_i(x^n)=h(x_i)$, the mixed-infinity set is

$$
\bigcup_{i,j=1}^n
\bigl(\{h_i=+\infty\}\cap\{h_j=-\infty\}\bigr).
$$

It is measurable. Under $P^{\otimes n}$ it is contained in the finite union $\bigcup_i\{h_i=+\infty\}$, which is null by the derived $P$ support property. Under $Q^{\otimes n}$ it is contained in $\bigcup_j\{h_j=-\infty\}$, which is null by the derived $Q$ support property. Consequently, replacing the otherwise undefined sum by zero there changes neither the rejection probability under any $P^{\otimes n}$ nor the acceptance probability under any $Q^{\otimes n}$.

The revised theorem's mathematical substance is **not strengthened**: general $\varepsilon$ is the exact reparameterisation of $e^{-nr}$ for $r>0$; the deleted support assumptions are consequences of retained assumptions; and the arbitrary-threshold Type II estimate is already proved for every $\tau\in\mathbb R$ in the current proof before the smallest threshold is substituted. The revision makes that existing intermediate guarantee explicit without changing its constants or assumptions.

## 3. Current proof dependency map

| Step | Role in the current proof | Necessary? | Keep explicit? | Combination possible? | Archived replacement? | Measure-theoretic cost of removal |
|---:|---|---|---|---|---|---|
| 1. Measurability of the mixed-infinity set | Ensures the convention is imposed on a measurable set and helps prove the extended block sum is measurable. | Yes in substance. | Yes, in one sentence. | Combine with measurability of the convention-defined sum. | No returned theorem addresses this exact convention. | Omitting all justification leaves the test's measurability unsupported. |
| 2. Nullity under $P^{\otimes n}$ and $Q^{\otimes n}$ | Makes the convention error-neutral and permits ordinary coordinate factorisation almost surely. | Yes. | Yes. | Combine with derivation of the support-nullity facts from finite moments. | No exact archive statement. | Removing it would leave the value assigned on mixed infinities potentially operationally relevant. |
| 3. Tonelli's theorem | Justifies iterated integration/factorisation for nonnegative, possibly extended-valued exponential integrands without first assuming integrability. | Yes. | Yes, by name. | Combine with product factorisation in one sentence. | ID 26876573 states the needed nonnegative product-space theorem. | Saying only “product structure” conceals the extended-value justification. |
| 4. Product factorisation | Converts each one-letter uniform moment bound into its $n$-fold version. | Yes. | Yes, as one aligned display. | Combine the null and alternative product bounds. | IDs 20527770 and 26581821 are relevant, but their returned wording does not safely cover all extended values. | Omitting it leaves the factor $n$ unexplained. |
| 5. Null-side Markov inequality | Gives $P^{\otimes n}\{S_n\ge\tau\}\le e^{-\lambda\tau+n(\lambda-1)d}$. | Yes. | Yes. | Combine with the alternative tail in one aligned display. | ID 23838516 gives exact Markov; ID 24310684 gives its MGF form, but neither subsumes the whole proof. | No special measure-theoretic cost after the exponential variable is shown integrable. |
| 6. Alternative lower-tail argument | Gives $Q^{\otimes n}\{S_n<\tau\}\le e^{(1-\lambda)\tau+n(\lambda-1)d}$. | Yes. | Yes. | Present directly as Markov applied to $e^{(\lambda-1)S_n}$; absorb the separate pointwise inequality. | ID 26879786 matches the real-valued negative-exponent direction but not all target assumptions. | Removing the sign-reversal explanation risks an incorrect event direction. |
| 7. Monotonicity in $\tau$ | Notes that the analytic Type II upper bound increases with the threshold. | Not needed for the stated arbitrary-threshold result or substitution. | No. | Absorb by direct substitution when deriving the minimax consequence. | No theorem needed. | None; it is elementary and unused once the arbitrary-$\tau$ statement is retained. |
| 8. Substitute the smallest certified threshold | Produces the exponential term in the final minimax bound. | Yes. | Yes, but the algebra can be inline in prose. | Combine with the minimax conclusion. | No theorem needed. | None if the algebra is recorded elsewhere in the audit and the resulting display is explicit. |
| 9. Constant randomised test | Supplies the independent upper bound $1-\varepsilon$ and hence the minimum. | Yes. | Yes, one sentence. | Combine with the sentence introducing the final minimum. | No relevant exact archive theorem returned. | Removing it would leave $1-\varepsilon$ unjustified. |

## 4. Retained archive results

The companion query ledger records all 24 exact queries, all 240 returned IDs and scores, returned statements, metadata, and rejection reasons. The results material to this audit are:

- **Markov inequality, ID 23838516:** exact constant for a nonnegative variable. It supports both tail calculations after exponentiation, but does not address extended scores, uniform classes, or the convention.
- **Upper exponential tail, ID 24310684:** exact positive-exponent MGF bound, but only the null-side form. It is **INSUFFICIENT FROM THEOREM ARCHIVE** for Route B.
- **Negative-exponent lower tail, ID 26879786:** exact real-variable lower-tail constant with $t<0$. It omits the target's extended-value and uniform structure and uses a weak event. It is **INSUFFICIENT FROM THEOREM ARCHIVE** for replacing Route A.
- **Tonelli, ID 26876573:** exactly supports iteration of nonnegative measurable integrands over finite products, including extended integrals.
- **Product expectation/MGF, IDs 20527770 and 26581821:** relevant product identities, but their returned statements do not explicitly cover the mixed-infinity, extended-valued setting. Tonelli remains necessary.
- **Rényi product additivity, ID 22017189:** exact for product divergences but inapplicable to an arbitrary score unless likelihood-ratio structure is added. Using it here would **CHANGES THE MATHEMATICS**.

No archive result is used as novelty or prior-art evidence, and no external proof was inspected.

## 5. Comparison of proof routes

| proof route | external theorem required | exact same theorem? | handles extended values? | logical steps | clarity | risks | recommendation |
|---|---|---|---|---:|---|---|---|
| A — two direct Markov inequalities | No external theorem required; Markov ID 23838516 and Tonelli ID 26876573 merely identify standard ingredients | Yes | Yes, with explicit support-nullity, convention, and Tonelli sentences | 6 | Highest; both errors arise symmetrically from exponentiation | Must reverse the alternative event correctly because $\lambda-1<0$ | **RECOMMENDED** |
| B — archived Chernoff theorem | Would require a single theorem covering both signs, extended values, uniform classes, and exact constants; none returned | Not established from archive | Returned results do not cover the full setting | Unknown | Would hide rather than shorten the two one-line Markov steps | Missing extended-value and negative-exponent hypotheses | **INSUFFICIENT FROM THEOREM ARCHIVE** |
| C — Hellinger-integral splitting | Requires $h$ to be a log-likelihood ratio for a simple pair and a corresponding Hellinger identity | No | Only under additional pairwise structure | At least 7 | Natural only in the likelihood-ratio special case | Adds assumptions explicitly forbidden by the invariant | **CHANGES THE MATHEMATICS** |
| D — archived one-shot testing theorem | An exact uniform composite theorem with the same moments, threshold, and arbitrary $\varepsilon$ would be required; none returned | Not established from archive | Returned one-shot results are simple, quantum, asymptotic, or likelihood-ratio based | Unknown | Potentially concise only if exact | Different constants, conventions, or assumptions | **INSUFFICIENT FROM THEOREM ARCHIVE** |

### Route A

Let $S_n$ denote the convention-defined sum. Outside the null mixed-infinity set,
$e^{tS_n}=\prod_i e^{th(X_i)}$ for $t=\lambda$ and $t=\lambda-1$. Nullity makes the same identity sufficient for each relevant integral. Tonelli and the product law give the two product moments. Markov applied to $e^{\lambda S_n}$ gives the upper tail. Since $\lambda-1<0$, $S_n<\tau$ is equivalent to $e^{(\lambda-1)S_n}>e^{(\lambda-1)\tau}$, so the same Markov inequality gives the alternative lower tail. This is the shortest complete proof because it exposes all constants and retains the only necessary measure-theoretic qualifications.

### Route B

IDs 24310684 and 26879786 separately resemble the two tails, but neither returned statement permits the target extended-real construction or gives a uniform two-class result; no single returned theorem gives both. Importing two incomplete archive theorems would be longer than applying Markov twice. Route B is not recommended.

### Route C

The target $h$ is not assumed to equal $\log(dQ/dP)$ for any pair. Hellinger-integral splitting would need precisely such a relation to turn integrals of likelihood-ratio powers over threshold regions into the two errors. Adding it would exclude scores permitted by the target assumptions. Therefore this route **CHANGES THE MATHEMATICS** and is not part of the rewrite. The mentioned uploaded reference is not used as an external source; only the route described in the task is assessed.

### Route D

No returned one-shot theorem simultaneously has $0<\lambda<1$, the two stated abstract score moments, the exact threshold, the arbitrary-threshold Type II exponent, arbitrary $\varepsilon$, and uniform composite errors. Route D is **INSUFFICIENT FROM THEOREM ARCHIVE**.

## 6. Answers to every clunkiness question

### 1. Are the separate support assumptions redundant?

Yes. The rigorous finite-integral arguments in Section 2 derive $P\{h=+\infty\}=0$ and $Q\{h=-\infty\}=0$ for every respective law. Deleting them from the assumptions changes no admissible instance.

### 2. Must the exceptional set be named?

No. A convention clause in the theorem and a one-sentence description as the finite union of coordinate events in the proof suffice. A name adds no later compression because the set is used only to prove measurability and nullity.

### 3. Is the exceptional-set convention measurable?

Yes. Each coordinate event $\{h_i=+\infty\}$ and $\{h_i=-\infty\}$ is measurable because $h_i$ is extended-real measurable. Their finite union of pairwise intersections is measurable. Off it, the finite extended sum is defined because its positive and negative parts are not both infinite; its sublevel sets can be obtained from measurable truncated sums. Defining the sum to be zero on the measurable exceptional set is therefore measurable.

### 4. Is the mixed-infinity set null under every product law?

Yes. Under $P^{\otimes n}$ it is contained in the occurrence of at least one $+\infty$ coordinate, a finite union of null coordinate events. Under $Q^{\otimes n}$ it is contained in the occurrence of at least one $-\infty$ coordinate. The respective derived support properties make both unions null.

### 5. Is Tonelli genuinely needed?

A rigorous factorisation needs Tonelli (or an equivalent nonnegative-product integration theorem). The coordinate exponentials are nonnegative and may initially be extended valued. Tonelli permits iterated integration without presupposing integrability and yields the product; the finite moment bounds then show the resulting integrals are finite. “Product structure” alone is an insufficient measure-theoretic explanation in this setting. Tonelli should remain explicit.

### 6. Can the two product moment bounds share one display?

Yes. They use the same null-set argument, Tonelli factorisation, and one-letter bound, differing only in the law and exponent. An aligned display makes the symmetry clearer.

### 7. Can both error bounds be Markov applications?

Yes. The null event is an upper tail of $e^{\lambda S_n}$. The alternative acceptance event is an upper tail of $e^{(\lambda-1)S_n}$ because its exponent is negative. No separate integral trick is required.

### 8. Is the explicit alternative event identity clearer?

Yes, with its strict inequality retained:

$$
Q^{\otimes n}\{S_n<\tau\}
=Q^{\otimes n}\{e^{(\lambda-1)S_n}>e^{(\lambda-1)\tau}\}.
$$

It makes the sign reversal auditable immediately before Markov. The resulting strict-tail probability is bounded by the usual weak-tail Markov bound.

### 9. Is a named minimum threshold needed?

No. The formula occurs once as the condition for the arbitrary-threshold result and once when its smallest value is substituted. Naming it would add notation without shortening the proof.

### 10. Is $S_n$ useful in the proof?

Yes. Used locally, it avoids repeating the convention-defined coordinate sum throughout both moment and tail calculations. It materially improves the proof even though it need not be promoted as a separately named theorem object.

### 11. Must monotonicity of the Type II bound be stated?

No. The theorem retains the bound for every admissible $\tau$. For the minimax consequence one directly chooses the smallest certified threshold and substitutes it. Monotonicity is true because $1-\lambda>0$, but it is not a logical premise of either operation.

### 12. Algebra at the smallest threshold

With $L=\log(1/\varepsilon)$ only for this verification,

$$
\begin{aligned}
(1-\lambda)\frac{L-n(1-\lambda)d}{\lambda}
+n(\lambda-1)d
&=\frac{1-\lambda}{\lambda}L
-\frac{n(1-\lambda)}{\lambda}d\\
&=-\frac{1-\lambda}{\lambda}(nd-L).
\end{aligned}
$$

This is exactly the target exponent.

### 13. Constant randomised test

For $\varphi_n\equiv\varepsilon$, every $P$ gives
$\mathbb E_{P^{\otimes n}}\varphi_n=\varepsilon$, and every $Q$ gives
$\mathbb E_{Q^{\otimes n}}[1-\varphi_n]=1-\varepsilon$. Hence its uniform Type I error is $\varepsilon$ and its uniform Type II error is $1-\varepsilon$.

### 14. Which equations require numbering?

None inside the proposed proof. Every display is used immediately, and no later equation reference is needed. The theorem statement outside the proof may be numbered according to manuscript cross-reference needs, but the editorial proof should use `equation*` only.

### 15. Can the proof use three principal displays?

Yes: one aligned product-moment display, one aligned pair of tail/error bounds, and one final minimax display. Measurability, support nullity, threshold algebra, and the constant test remain explicit in prose, so this compression creates no logical gap.

## 7. Recommended proof architecture

Use **Route A — two direct Markov inequalities**:

1. Derive both support-nullity facts from finite moments; establish measurability and product-law nullity of mixed infinities.
2. Introduce $S_n$ locally and use Tonelli plus product structure in one aligned display for both exponential moments.
3. Apply Markov twice in one aligned display, displaying the negative-exponent event reversal on the alternative side.
4. Read the Type I threshold directly and retain the Type II estimate for arbitrary $\tau$.
5. Substitute the smallest admissible threshold, add the constant randomised test, and display the final minimum.

Archive IDs 23838516 and 26876573 identify Markov and Tonelli as standard ingredients. The compression itself is elementary editorial reorganisation, not an archive-derived theorem.

## 8. Proposed editorial proof

```latex
\begin{IEEEproof}
The moment assumptions have finite right-hand sides.  Since $\lambda>0$,
$e^{\lambda h}=+\infty$ on $\{h=+\infty\}$, and since
$\lambda-1<0$, $e^{(\lambda-1)h}=+\infty$ on
$\{h=-\infty\}$.  Hence $P\{h=+\infty\}=0$ for every
$P\in\mathcal P$ and $Q\{h=-\infty\}=0$ for every
$Q\in\mathcal Q$.  The set of sequences containing both signs of infinity
is the finite union of the measurable sets
$\{h(x_i)=+\infty,h(x_j)=-\infty\}$ and is null under every
$P^{\otimes n}$ and $Q^{\otimes n}$.  Thus the convention-defined sum is
measurable and its value on that set affects neither error probability.
Write it as $S_n$.  Tonelli's theorem and the product laws give
\begin{equation*}
\begin{aligned}
\sup_{P\in\mathcal P}
\mathbb E_{P^{\otimes n}}[e^{\lambda S_n}]
&=\sup_{P\in\mathcal P}
\bigl(\mathbb E_P[e^{\lambda h}]\bigr)^n
\leq e^{n(\lambda-1)d},\\
\sup_{Q\in\mathcal Q}
\mathbb E_{Q^{\otimes n}}[e^{(\lambda-1)S_n}]
&=\sup_{Q\in\mathcal Q}
\bigl(\mathbb E_Q[e^{(\lambda-1)h}]\bigr)^n
\leq e^{n(\lambda-1)d}.
\end{aligned}
\end{equation*}

For every $\tau\in\mathbb R$, Markov's inequality, applied to the two
nonnegative exponentials above, yields
\begin{equation*}
\begin{aligned}
\alpha_n(\psi_{n,\tau};\mathcal P)
&=\sup_{P\in\mathcal P}P^{\otimes n}\{S_n\geq\tau\}
\leq e^{-\lambda\tau+n(\lambda-1)d},\\
\beta_n(\psi_{n,\tau};\mathcal Q)
&=\sup_{Q\in\mathcal Q}Q^{\otimes n}\{S_n<\tau\}\\
&=\sup_{Q\in\mathcal Q}Q^{\otimes n}
\{e^{(\lambda-1)S_n}>e^{(\lambda-1)\tau}\}
\leq e^{(1-\lambda)\tau+n(\lambda-1)d}.
\end{aligned}
\end{equation*}
The first bound is at most $\varepsilon$ whenever
$\tau\geq[\log(1/\varepsilon)-n(1-\lambda)d]/\lambda$, while the second
bound is the asserted arbitrary-threshold Type II guarantee.  Substitution
of the smallest such threshold gives the second term below.  The constant
randomised test $\varphi_n\equiv\varepsilon$ has Type I error
$\varepsilon$ and Type II error $1-\varepsilon$.  Therefore
\begin{equation*}
\beta_n^\star(\varepsilon;\mathcal P,\mathcal Q)
\leq\min\left\{1-\varepsilon,
\exp\left\{-\frac{1-\lambda}{\lambda}
\left[nd-\log\frac1\varepsilon\right]\right\}\right\}.
\end{equation*}
\end{IEEEproof}
```

The proposed proof uses $\varepsilon$ exclusively, never introduces an exponential-rate parameter, preserves the convention and arbitrary threshold, and does not interpret $h$ as a likelihood ratio.

## 9. Line-by-line equivalence audit

| Current element | Proposed counterpart | Removal classification | Why safe or unsafe |
|---|---|---|---|
| Separate support assumptions in the theorem | First three sentences derive both facts from finite moments. | **Logically redundant** as assumptions. | Finite moments force exactly those null events; the proof retains the conclusions. This is safe. |
| Named exceptional set $\mathcal M_n$ | Described once as a finite union; the convention-defined sum is then called $S_n$. | **Absorbed into another step.** | The set's measurability and nullity remain explicit. Only its name is removed. This is safe. |
| Current measurable-extension paragraph | First paragraph of proposed proof. | **Absorbed into another step.** | Measurability, nullity under both product families, and error-neutrality all remain; removing the substance would not be safe. |
| Two current product-moment lines | First aligned display. | Retained and combined. | Tonelli remains named because dropping it would sacrifice the extended-valued justification. |
| Separately named tail bounds and their equation labels | Second aligned display. | **Absorbed into another step.** | Both exact inequalities remain visible together and are used immediately; separate names and labels are unnecessary. |
| Explicit $1\le e^{(1-\lambda)(\tau-S_n)}$ on $\{S_n<\tau\}$ | Equality of the lower-tail event with an upper-tail event of $e^{(\lambda-1)S_n}$, then Markov. | **Absorbed into another step.** | The equality is equivalent because $\lambda-1<0$ and is clearer about sign reversal. The alternative tail itself is not removed. |
| Threshold monotonicity sentence | Directly substitute the smallest certified threshold. | **Logically redundant.** | The arbitrary-$\tau$ theorem holds pointwise; choosing an admissible value needs no monotonicity premise. Safe to remove. |
| Named $\tau_{\lambda,r}^{\min}$ | The general-$\varepsilon$ threshold formula is left unnamed. | **Logically redundant notation.** | It is used only at certification and substitution. The formula remains exact. |
| Labels `eq:abstract-null-tail` and `eq:abstract-alternative-tail` | No internal equation labels. | **Logically redundant.** | Both bounds are consumed immediately and need no later cross-reference. |
| Smallest-threshold substitution | Prose before the final display, with full algebra verified in Section 6. | Retained, compressed. | Removing the substitution altogether would not be safe because it produces the target exponent. |
| Constant randomised test | Penultimate sentence. | Retained. | Removing it would not be safe: it uniquely supplies the $1-\varepsilon$ term. |

Against the six specifically audited removable presentation elements—(1) separate support assumptions, (2) the exceptional-set name, (3) separately named tail bounds, (4) the standalone pointwise lower-tail inequality, (5) the monotonicity sentence, and (6) intermediate equation labels—**six proof elements are removed or absorbed**. No mathematical step needed for measurability, nullity, Tonelli factorisation, either error bound, the arbitrary threshold, threshold substitution, or the constant test is removed.

## 10. OPTIONAL MATHEMATICAL SUGGESTION — NOT PART OF THE EDITORIAL REWRITE

The archive does not return sufficient support for a stronger theorem, additional corollary, weakened assumption beyond the already redundant support conditions, or alternative test with the same invariant. A likelihood-ratio/Hellinger specialisation would add structure excluded from this audit and is therefore not proposed. There is no optional mathematical suggestion to incorporate.

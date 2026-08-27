# Proof-simplification audit: first composite converse

## 1. Mathematical invariant

### Result being audited

The exact passage is Theorem `thm:finite-sample-composite-renyi-converse` and its immediately following `IEEEproof` in `manuscript/Manuscript.tex`. The mathematical reason for considering an editorial rewrite is that the current proof selects near-optimising orders and pairs before proving its elementary pairwise inequality. Proving that inequality pointwise first permits exact order and class optimisation, and makes nonattainment explicit without auxiliary approximation parameters. This audit does not edit the manuscript.

### Frozen invariant

Throughout the audit, **none of the following may change**.

1. **Quantifiers.** Let $(\mathcal X,\mathcal F)$ be a measurable space; let $\mathcal P$ and $\mathcal Q$ be arbitrary nonempty classes of probability laws on it. For every $\epsilon\in(0,1)$ and every integer $n\ge1$, the bound holds. The infimum defining the minimax value ranges over every measurable randomised test $\varphi_n:\mathcal X^n\to[0,1]$ satisfying the uniform Type I constraint.
2. **Assumptions.** There is no convexity, compactness, domination common to either class, projection, or attainment assumption. Individual pairs may be dominated by a pair-dependent measure, as in the manuscript's definition. Standard extended-real conventions remain in force.
3. **Orientation.** The only Rényi orientation is
   $D_\lambda(Q\|P)$ and hence
   $D_\lambda(\mathcal Q\|\mathcal P)=\inf_{Q\in\mathcal Q}\inf_{P\in\mathcal P}D_\lambda(Q\|P)$.
4. **Positive part.** The operation applies exactly to the entire difference
   $[\log(1/\epsilon)-nD_\lambda(\mathcal Q\|\mathcal P)]_+$,
   before multiplication by $(\lambda-1)/\lambda$ and before the supremum. Here $[a]_+=\max\{a,0\}$ and the manuscript's extended convention $[-\infty]_+=0$ applies.
5. **Exponent.** The exponent is exactly
   $-\sup_{\lambda>1}\frac{\lambda-1}{\lambda}[\log(1/\epsilon)-nD_\lambda(\mathcal Q\|\mathcal P)]_+$.
6. **Role of $\epsilon$.** It is the general uniform Type I threshold: every admissible $\varphi_n$ obeys $\sup_{P\in\mathcal P}\mathbb E_{P^{\otimes n}}[\varphi_n]\le\epsilon$. It is neither a Type II threshold nor replaced by $1-\epsilon$.
7. **Nonattainment.** Neither $\inf_{Q,P}D_\lambda(Q\|P)$ nor $\sup_{\lambda>1}$ is assumed attained. Every optimisation step must be valid for an infimum or supremum as such.
8. **Conclusion.** The sole conclusion is

   $$
   \beta_n^\star(\epsilon;\mathcal P,\mathcal Q)
   \ge 1-\exp\left\{-\sup_{\lambda>1}\frac{\lambda-1}{\lambda}
   \left[\log\frac1\epsilon-nD_\lambda(\mathcal Q\|\mathcal P)\right]_+\right\}.
   $$

No second converse, reversal of orientation, extra corollary, altered quantifier, or strengthened conclusion is permitted.

### Exact reparameterisation check

The current theorem has

$$
E_{\rm sc}(r;\mathcal P,\mathcal Q)
=\sup_{\lambda>1}\frac{\lambda-1}{\lambda}
[r-D_\lambda(\mathcal Q\|\mathcal P)]_+
$$

and concludes $\beta_n^\star(r;\mathcal P,\mathcal Q)\ge1-e^{-nE_{\rm sc}}$. Set
$r=n^{-1}\log(1/\epsilon)$. Since $n>0$, $n[a]_+=[na]_+$, and therefore

$$
\begin{aligned}
 nE_{\rm sc}
 &=\sup_{\lambda>1}\frac{\lambda-1}{\lambda}
 n\left[\frac1n\log\frac1\epsilon-D_\lambda(\mathcal Q\|\mathcal P)\right]_+\\
 &=\sup_{\lambda>1}\frac{\lambda-1}{\lambda}
 \left[\log\frac1\epsilon-nD_\lambda(\mathcal Q\|\mathcal P)\right]_+.
\end{aligned}
$$

Moreover, $e^{-nr}=\epsilon$, and $r>0$ is equivalent to $\epsilon\in(0,1)$. Thus both the admissible-test class and the conclusion become exactly the target formulation.

## 2. Current proof dependency map

| Step | What it proves or enables | Logically necessary? | Present only for nonattainment? | Standard theorem replacement? | Removable by pointwise-first organisation? |
|---:|---|---|---|---|---|
| 1. Fix an admissible randomised test | Reduces the minimax conclusion to a uniform lower bound for an arbitrary feasible $\varphi_n$. | Yes. | No. | No. | No. |
| 2. Introduce $E_{\rm sc}$ | Abbreviates the order-optimised exponent. | No; editorial shorthand only. | No. | Not relevant. | Yes. |
| 3. Split off $E_{\rm sc}=0$ | Handles the trivial lower bound $\beta_n\ge0$. | Not in a pointwise proof: the positive part makes the zero case automatic. | No. | No. | Yes. |
| 4. Choose $\lambda_\delta$ | Approximates a possibly unattained supremum and ensures a positive finite class separation in the nontrivial branch. | Only in the current optimise-first architecture. | Yes, for the order supremum. | No archive theorem is needed. | Yes: prove the bound for every $\lambda>1$, then take the supremum. |
| 5. Choose $(P_\eta,Q_\eta)$ | Approximates the classwise divergence infimum at the chosen order. | Only in the current select-a-pair architecture. | Yes, for the pair infimum. | No archive theorem is needed. | Yes: prove the inequality for every pair, then use the monotone-continuous optimisation identity proved below. |
| 6. Apply Hölder to the selected pair | Gives the central rejection-probability upper bound with exponent $(\lambda-1)/\lambda$ and orientation $Q\|P$. | Yes in substance. | No. | The archive contains the exact event analogue, but not the bounded-randomised-test statement; it does not replace Hölder. | No, but it becomes a one-line pairwise calculation for arbitrary $P,Q,\lambda$. |
| 7. Tensorise Rényi divergence | Changes $D_\lambda(Q^{\otimes n}\|P^{\otimes n})$ into $nD_\lambda(Q\|P)$. | Yes. | No. | Yes: archived Theorem 28 (ID 22017189) states exact finite-product additivity. | No. |
| 8. Convert rejection under $Q$ to Type II error | Uses $\mathbb E_Q[1-\varphi]=1-\mathbb E_Q[\varphi]$, caps rejection probability by one, and introduces the positive part. | Yes. | No. | No external theorem required. | No. |
| 9. Let $\eta\downarrow0$ | Removes pair-selection slack. | Only in the current proof. | Yes. | Replaced by an elementary optimisation identity, not an archive theorem. | Yes. |
| 10. Let $\delta\downarrow0$ | Removes order-selection slack. | Only in the current proof. | Yes. | Replaced by the definition of supremum plus monotonicity of $1-e^{-x}$. | Yes. |
| 11. Infimise over admissible tests | Returns from the arbitrary feasible test to $\beta_n^\star$. | Yes. | No. | No. | No. |

Thus the current chain is mathematically sound, but steps 2, 3, 4, 5, 9, and 10 are redundant in a pointwise-first proof. On the supplied eleven-step accounting, **six steps are removed**; steps 6 and 7 are compressed, not deleted.

## 3. Retained archive results

The exact queries, all returned IDs/scores, full retained metadata, and false-positive decisions are in `theoremsearch_queries.md`. The audit retained three kinds of statements:

1. **Event change of measure (IDs 26995949 and 24257764).** Both state, for order greater than one, the exact event inequality with exponent $(\lambda-1)/\lambda$ and divergence oriented from the measure on the left to the measure whose event probability appears in the power. After renaming measures, the constants match the indicator-test special case. They do not cover a general $[0,1]$-valued randomised test. Classification for replacement of the Hölder step: **INSUFFICIENT FROM THEOREM ARCHIVE**.
2. **Data processing (ID 24148956).** The returned statement says Rényi divergence of order $q\ge1$ contracts under a Markov kernel. It verifies the contraction component of Route B with the same orientation. It does not state that the test induces the required binary kernel and does not give the binary Rényi calculation. Classification for the complete route: **INSUFFICIENT FROM THEOREM ARCHIVE**.
3. **Product additivity (ID 22017189).** The returned theorem states exact additivity of order-$\alpha$ Rényi divergence for finite products on measurable spaces. It exactly verifies $D_\lambda(Q^{\otimes n}\|P^{\otimes n})=nD_\lambda(Q\|P)$. This standard theorem can replace the bare appeal to tensorisation, but it does not replace Hölder.

No retained result is treated as evidence of novelty or prior-art status.

## 4. Comparison of proof routes

| proof route | external theorem required | exact same bound? | treatment of nonattainment | number of logical steps | clarity | risks | recommendation |
|---|---|---|---|---:|---|---|---|
| A — direct Hölder, pointwise in pair and order | None; product additivity may be cited from archive ID 22017189 or proved from the definition | Yes | Exact monotone-continuous identity for pair infimum; bound for every $\lambda$ before taking the supremum | 5 | Highest: the only analytic estimate is visible | Must state extended-value cases and justify both optimisations | **RECOMMENDED** |
| A — current $\delta$/$\eta$ selection | None | Yes | Explicit approximating order and pair | 11 | Correct but longer and obscures the pairwise core | More case splits and limit bookkeeping | **CORRECT BUT NOT SIMPLER** |
| B — data processing through the randomised test | DPI is returned (ID 24148956), but the archive lacks the test-kernel identification and required binary Rényi calculation as a complete theorem route | The route can be checked elementarily, but the archive alone does not verify the complete route as required by this audit | Pointwise in pair/order, then exact optimisation | At least 7 | Conceptually attractive, operationally longer here | A separate Bernoulli calculation; archive incompleteness | **INSUFFICIENT FROM THEOREM ARCHIVE** |
| C — archived one-shot testing inequality | An exact one-shot classical theorem would be required; none was returned | Not verifiable from returned statements | Would still require composite and order optimisation | Unknown | Potentially shortest if exact | Quantum results, event-only results, different errors/constants/orientations | **INSUFFICIENT FROM THEOREM ARCHIVE** |

### Route B calculation audit

For completeness of the mathematical audit, define the binary kernel $K(1\mid x^n)=\varphi_n(x^n)$ and $K(0\mid x^n)=1-\varphi_n(x^n)$. Its pushforwards are $\operatorname{Bernoulli}(\mathbb E_{Q^{\otimes n}}\varphi_n)$ and $\operatorname{Bernoulli}(\mathbb E_{P^{\otimes n}}\varphi_n)$ when Bernoulli success means rejection. DPI would give the displayed orientation requested in the task. However, extracting only the successful-decision term from the binary Rényi sum is another Hölder-equivalent inequality. It is not shorter than applying Hölder directly, and the returned archive theorem does not contain that calculation. Route B is therefore not recommended.

### Route C audit

No returned theorem simultaneously states: classical randomised tests; every $\lambda>1$; $D_\lambda(Q\|P)$; exponent $(\lambda-1)/\lambda$; threshold $\epsilon$; product factor $n$; and the required Type II lower bound. Event inequalities lack randomisation, while returned one-shot testing results use order two, quantum/sandwiched divergences, or different error conventions. Route C cannot replace the proof.

## 5. Answers to the clunkiness questions

### 1. Is the temporary symbol $E$ needed?

No. It abbreviates an expression used only to select $\lambda_\delta$ and split the zero case. Both operations disappear when the pairwise inequality is proved for every order. Writing the final supremum once is clearer.

### 2. Can the proof be pairwise first, then classwise and orderwise?

Yes. For every admissible $\varphi_n$, every $P,Q$, and every $\lambda>1$, Hölder gives a pairwise bound. Since the composite Type II error dominates the Type II error for each $Q$, it dominates every pairwise lower bound. The exact identities in answers 6 and 7 then optimise the pair and order without selecting either.

### 3. Should there be a standalone pairwise lemma?

Not here. The pairwise argument is one displayed Hölder chain plus one conversion to Type II error. A separate named lemma would fragment the first converse and require restating its assumptions. A lemma would be justified only if reused elsewhere; for this narrowly scoped rewrite, present it as the first paragraph of the proof.

### 4. Where should the Bruno et al. sentence go?

It is not logically needed inside the proof. Attribution does not discharge a proof step because the manuscript immediately proves the needed estimate. It should be moved to surrounding prose if retained. This is an editorial recommendation only; no bibliography or manuscript file is changed, and the present audit does not inspect that external source.

### 5. Is a zero-expectation split necessary?

No. If $D_\lambda(Q\|P)<\infty$, then $Q\ll P$ for $\lambda>1$, and Hölder applies with a finite likelihood-ratio $\lambda$-moment. When $\mathbb E_P\varphi=0$, its right-hand side is $0^{(\lambda-1)/\lambda}$ times a finite factor, hence zero; this already implies $\mathbb E_Q\varphi=0$. If $D_\lambda(Q\|P)=+\infty$, the eventual pairwise Type II bound is $0$ because $[\log(1/\epsilon)-n(+\infty)]_+=0$, so it follows from nonnegativity without absolute continuity. Thus no separate displayed case is required.

### 6. Can the $\eta$ approximation be replaced by an exact identity?

Yes. Fix $\lambda>1$, put $c=(\lambda-1)/\lambda$, $L=\log(1/\epsilon)$, and define on $[0,+\infty]$

$$
g(d)=1-\exp\{-c[L-nd]_+\},\qquad g(+\infty)=0.$$

The function is continuous and nonincreasing on $[0,+\infty]$ with the order topology: it decreases continuously to zero by $d=L/n$ and remains zero thereafter, including at $+\infty$. Let $S=\{D_\lambda(Q\|P):Q\in\mathcal Q,P\in\mathcal P\}$ and $d_*=\inf S$. Because the classes are nonempty, $S$ is nonempty.

- Always, $d_*\le d$ for $d\in S$, so monotonicity gives $g(d)\le g(d_*)$ and hence $\sup_{d\in S}g(d)\le g(d_*)$.
- If $d_*<+\infty$, the definition of infimum supplies $d_k\in S$ with $d_k<d_*+1/k$. Then $d_k\to d_*$ and continuity gives $g(d_k)\to g(d_*)$, proving the reverse inequality without attainment.
- If $d_*=+\infty$, every member of the nonempty $S\subset[0,+\infty]$ equals $+\infty$, so both sides equal $g(+\infty)=0$.

Therefore

$$
\sup_{P\in\mathcal P,Q\in\mathcal Q}g(D_\lambda(Q\|P))
=g\!\left(\inf_{P\in\mathcal P,Q\in\mathcal Q}D_\lambda(Q\|P)\right).
$$

This removes $\eta$ but does not assume attainment.

### 7. Can the $\delta$ approximation be removed?

Yes. If a number $b$ satisfies $b\ge1-e^{-x_\lambda}$ for every $\lambda>1$, then
$b\ge\sup_{\lambda>1}(1-e^{-x_\lambda})$. Since $h(x)=1-e^{-x}$ is continuous and increasing and here $0\le x_\lambda\le\log(1/\epsilon)<\infty$,

$$
\sup_{\lambda>1}(1-e^{-x_\lambda})
=1-\exp\{-\sup_{\lambda>1}x_\lambda\}.
$$

No maximising order is selected, so no $\delta$ is needed.

### 8. Is the positive part introduced at the clearest point?

In the current proof it appears after selecting a positive exponent and after Hölder. A clearer point is immediately after the rejection bound: combine that bound with the universal cap $\mathbb E_Q\varphi\le1$. The identity $\min\{1,e^{-x}\}=e^{-[x]_+}$ then introduces the positive part exactly once, before class or order optimisation.

### 9. Must every equation be displayed?

No. Feasibility, domination of a fixed-$Q$ Type II error by the composite error, definitions of the short variables $c$ and $L$, and prose-level optimisation facts can remain inline. Display only the Hölder chain, the classwise optimisation result, and the final order/test optimisation.

### 10. Which equations need numbering?

Only a displayed equation that is explicitly invoked later needs a number. In the proposed proof, the pairwise Type II inequality is labelled because the next paragraph applies it to the classes. The final display is the conclusion and needs no internal cross-reference. The Hölder calculation is unnumbered because the immediately following sentence uses it without a remote reference.

## 6. Recommended proof architecture

Use **Route A — direct Hölder, pointwise in the pair and order**:

1. Fix an admissible randomised test and arbitrary $P\in\mathcal P$, $Q\in\mathcal Q$, $\lambda>1$.
2. Apply Hölder directly using pairwise densities. Treat $D_\lambda=+\infty$ by the trivial bound; finite divergence automatically covers zero Type I expectation. Invoke exact product additivity.
3. Cap rejection probability by one and introduce the positive part, obtaining a labelled pairwise Type II inequality.
4. Use the proved monotone-continuous identity to optimise over $P,Q$ without claiming attainment.
5. Since the result holds for every $\lambda$, take the supremum directly, then infimise over admissible tests.

Archive-derived simplification is limited to recognising product additivity as an exact standard theorem (ID 22017189). Removal of $E_{\rm sc}$, the zero split, $\delta$, and $\eta$ is elementary rewriting justified in this audit; it is not attributed to the archive.

## 7. Proposed editorial proof

The following is IEEE-compatible LaTeX for the **target $\epsilon$ formulation only**.

```latex
\begin{IEEEproof}
Fix an admissible test $\varphi_n$, and fix $P\in\mathcal P$,
$Q\in\mathcal Q$, and $\lambda>1$.  If
$D_\lambda(Q\|P)<+\infty$, H\"older's inequality, the bound
$0\leq\varphi_n\leq1$, the Type I constraint, and additivity of
R\'enyi divergence for product laws give
\begin{equation*}
\begin{aligned}
\mathbb E_{Q^{\otimes n}}[\varphi_n]
&\leq
\bigl(\mathbb E_{P^{\otimes n}}[\varphi_n]\bigr)^{
(\lambda-1)/\lambda}
\exp\left\{\frac{\lambda-1}{\lambda}
D_\lambda(Q^{\otimes n}\|P^{\otimes n})\right\}\\
&\leq
\exp\left\{-\frac{\lambda-1}{\lambda}
\left[\log\frac1\epsilon-nD_\lambda(Q\|P)\right]\right\}.
\end{aligned}
\end{equation*}
This calculation also covers
$\mathbb E_{P^{\otimes n}}[\varphi_n]=0$.  Combining it with
$\mathbb E_{Q^{\otimes n}}[\varphi_n]\leq1$ yields
\begin{equation}
\mathbb E_{Q^{\otimes n}}[1-\varphi_n]
\geq 1-\exp\left\{-\frac{\lambda-1}{\lambda}
\left[\log\frac1\epsilon-nD_\lambda(Q\|P)\right]_+\right\}.
\label{eq:pairwise-epsilon-renyi-converse}
\end{equation}
If $D_\lambda(Q\|P)=+\infty$, the right-hand side of
\eqref{eq:pairwise-epsilon-renyi-converse} is zero, so the same inequality
follows from nonnegativity.

The composite Type II error dominates the left-hand side of
\eqref{eq:pairwise-epsilon-renyi-converse} for every $P\in\mathcal P$ and
$Q\in\mathcal Q$.  The function
$1-\exp\{-(\lambda-1)[\log(1/\epsilon)-nd]_+/\lambda\}$ is continuous and
nonincreasing in $d\in[0,+\infty]$.  Consequently, taking the supremum of
\eqref{eq:pairwise-epsilon-renyi-converse} over the pair gives, without
requiring the infimum to be attained,
\begin{equation*}
\beta_n(\varphi_n;\mathcal Q)
\geq 1-\exp\left\{-\frac{\lambda-1}{\lambda}
\left[\log\frac1\epsilon
-nD_\lambda(\mathcal Q\|\mathcal P)\right]_+\right\}.
\end{equation*}
This holds for every $\lambda>1$.  Taking the supremum over $\lambda$ and
then the infimum over all admissible $\varphi_n$ proves
\begin{equation*}
\beta_n^\star(\epsilon;\mathcal P,\mathcal Q)
\geq 1-\exp\left\{-\sup_{\lambda>1}
\frac{\lambda-1}{\lambda}
\left[\log\frac1\epsilon
-nD_\lambda(\mathcal Q\|\mathcal P)\right]_+\right\}.
\end{equation*}
Neither optimisation requires attainment.
\end{IEEEproof}
```

No likelihood-ratio symbol is necessary: the first inequality is precisely the bounded-function Hölder change-of-measure inequality. If a fully self-contained derivation rather than that named application is desired, pairwise densities can be inserted into the same line; introducing and retaining a separate $L_{\eta,n}$ is unnecessary.

## 8. Line-by-line equivalence check

| Proposed line or block | Current-proof counterpart | Exact equivalence and reason for any deletion |
|---|---|---|
| Fix admissible $\varphi_n$ and arbitrary $P,Q,\lambda$. | Current step 1, followed later by selected $P_\eta,Q_\eta,\lambda_\delta$. | The new quantification is stronger only as an intermediate statement, not as a theorem conclusion: proving the same inequality for each choice permits later optimisation. No selection or attainment is asserted. |
| Finite-divergence Hölder display. | Current likelihood-ratio definition and three-line Hölder display (steps 6–7). | Same conjugate exponents, same $0\le\varphi_n\le1$ relaxation, same Type I threshold after $e^{-nr}=\epsilon$, same orientation, and same tensorisation. The temporary likelihood-ratio symbol is inlined. |
| “This calculation also covers expectation zero.” | Current explicit zero-expectation branch. | The branch is deleted as redundant: finite divergence makes the Hölder moment finite, and a zero powered expectation makes the bound zero. |
| Cap by one and obtain labelled pairwise Type II bound. | Current rejection cap, positive part, and conversion (step 8). | Algebraically identical via $\min\{1,e^{-x}\}=e^{-[x]_+}$. The positive part is introduced once at the pairwise endpoint. |
| Infinite-divergence sentence. | Implicitly excluded in the current positive-exponent selection. | It restores full pointwise quantification: the claimed lower bound is zero when the divergence is infinite, so nonnegativity suffices. No assumption is added. |
| Optimise the pair by continuity and monotonicity. | Choose $(P_\eta,Q_\eta)$ and let $\eta\downarrow0$ (steps 5 and 9). | Exactly equivalent by the identity proved in clunkiness answer 6, including $d_*=+\infty$. Both pair-selection steps are deleted as redundant, not as an attainment assumption. |
| State the classwise bound for every $\lambda$. | Choose $\lambda_\delta$ and later let $\delta\downarrow0$ (steps 4 and 10). | Exactly equivalent by clunkiness answer 7. Both order-approximation steps are deleted because no order is selected. |
| Supremise over $\lambda$ and infimise over tests. | Final $\delta$ limit and current step 11. | Monotonicity/continuity of $1-e^{-x}$ gives the exact placement of the supremum; the test infimum is unchanged. |
| No $E_{\rm sc}$ and no zero-exponent paragraph. | Current steps 2 and 3. | Both are redundant bookkeeping: the pointwise positive-part inequality includes the zero exponent automatically. |
| No Bruno et al. sentence inside the proof. | Attribution sentence immediately before current Hölder calculation. | Deleted from the proposed proof because it proves nothing used later. If editorially desired, attribution belongs in surrounding prose and remains separate from the derivation. |

Counting against the eleven broad current steps specified for this audit, steps **2, 3, 4, 5, 9, and 10** are removed: **six current proof steps are redundant**. The core Hölder, tensorisation, Type II conversion, and minimax reduction remain mathematically unchanged.

## 9. OPTIONAL MATHEMATICAL SUGGESTION — NOT PART OF THE EDITORIAL REWRITE

No stronger theorem, additional converse, reversed divergence orientation, weakened assumption, or new corollary is supported with sufficiently complete information by the returned TheoremSearch statements. Accordingly, there is no optional mathematical suggestion to advance from this audit.

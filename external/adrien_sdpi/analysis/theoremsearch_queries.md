# TheoremSearch query log for Theorem 1

**Execution date:** 2026-08-13  
**Endpoint:** `POST https://api.theoremsearch.com/search`  
**Request size:** `n_results = 10`  
**Actual calls:** 69 (27 semantically distinct queries; duplicate calls resulted from retrying interrupted batches).

## Scope and interpretation

This is a tool search for proof machinery, not a novelty search. Similarity is semantic-retrieval similarity, not mathematical overlap. Every response was screened; most high-scoring hits were lexical false positives. The source manuscript requested by the task was absent from the checkout, so manuscript citations and its bibliography could not be followed.

## Queries actually run

1. `strong data processing binary support reduction` — top result 26619807, score 0.601690, “Corollary 1”, *Stochastic Mechanistic Interaction*.
2. `contraction coefficient binary input distributions` — top result 25735529, score 0.748647, “Theorem 21”, *Strong data-processing inequalities for channels and Bayesian networks*.
3. `Rényi divergence contraction coefficient support lemma` — top result 24520817, score 0.655647, “Lemma A.1 (Contraction-reduction lemma, simplified version)”, *Resolving the Mixing Time of the Langevin Algorithm to its Stationary Distribution for Log-Concave Sampling*.
4. `f-divergence contraction coefficient two point distributions` — top result 25735509, score 0.781839, “Theorem 1 (\cite [Proposition II.4.10]{CKZ98})”, *Strong data-processing inequalities for channels and Bayesian networks*.
5. `extreme point reduction SDPI` — top result 22384677, score 0.548532, “Lemma 5.8”, *A note on quasi-positive curvature conditions*.
6. `support lemma probability simplex hyperplane` — top result 19392762, score 0.699007, “Lemma 5.2”, *Newton-Okounkov bodies for categories of modules over quiver Hecke algebras*.
7. `Carathéodory theorem divergence optimisation` — top result 18111786, score 0.620854, “Theorem 3.2 (Primal Extended $\varphi $-Divergence Quadrangle)”, *Risk Quadrangle and Robust Optimization Based on Extended $\varphi$-Divergence*.
8. `moment constrained probability measures extreme points` — top result 20918824, score 0.772724, “Lemma 4.1”, *Transport-entropy inequalities on locally acting groups of permutations*.
9. `likelihood ratio fixed moment extreme distributions` — top result 22759176, score 0.615738, “Theorem 3.1 (Change point in the mean with known variance)”, *Off-line detection of multiple change points with the Filtered Derivative with p-Value method*.
10. `two point extremal probability measures` — top result 22527189, score 0.745242, “Corollary 2.3”, *The asymptotic Berry-Esseen constant for intervals*.
11. `Choquet moment problem two point support` — top result 24209772, score 0.703521, “Corollary 1.2”, *Robust Optimality of Bundling Goods Beyond Finite Variance*.
12. `convex maximisation probability simplex moment constraint` — top result 25765095, score 0.688832, “Lemma 13 (Pushback Property of KL-divergence)”, *Provably Efficient Safe Exploration via Primal-Dual Policy Optimization*.
13. `fractional programming divergence ratio` — top result 26644853, score 0.650377, “Theorem 2”, *Sensitivity analysis, multilinearity and beyond*.
14. `quasiconvex ratio extreme point` — top result 26802790, score 0.682353, “Lemma 16”, *Lecture Notes on Spectral Graph Methods*.
15. `max-divergence contraction coefficient` — top result 25735509, score 0.723480, “Theorem 1 (\cite [Proposition II.4.10]{CKZ98})”, *Strong data-processing inequalities for channels and Bayesian networks*.
16. `D infinity strong data processing` — top result 25804439, score 0.584688, “Corollary 7.2”, *The Saito determinant for Coxeter discriminant strata*.
17. `maximal leakage max divergence contraction` — top result 25735509, score 0.652071, “Theorem 1 (\cite [Proposition II.4.10]{CKZ98})”, *Strong data-processing inequalities for channels and Bayesian networks*.
18. `Dobrushin coefficient max divergence` — top result 25717845, score 0.713492, “Corollary”, *Imprecise Continuous-Time Markov Chains: Efficient Computational Methods with Guaranteed Error Bounds*.
19. `local differential privacy contraction` — top result 26745576, score 0.673737, “Proposition 1”, *Additive-Effect Assisted Learning*.
20. `Rényi SDPI cardinality bound` — top result 25711965, score 0.663335, “Corollary”, *Arimoto-Rényi Conditional Entropy and Bayesian $M$-ary Hypothesis Testing*.
21. `binary alphabet reduction information theory` — top result 26811881, score 0.646592, “Corollary 3.6”, *Exploring the Topological Entropy of Formal Languages*.
22. `Ordentlich strong data processing binary support` — top result 26619807, score 0.609652, “Corollary 1”, *Stochastic Mechanistic Interaction*.
23. `Cohen relative entropy contraction extreme points` — top result 17699799, score 0.596801, “Lemma 2.1”, *Linear maps on $\mathcal{L}(\ell_p^n,\ell_p^m)$, $(p\in \{1,\infty\})$ preserving parallel pairs*.
24. `contraction coefficient operator convex divergence` — top result 25642883, score 0.681251, “Theorem (General Contraction Coefficient Bound)”, *Linear Bounds between Contraction Coefficients for $f$-Divergences*.
25. `support size bound divergence optimisation` — top result 19685759, score 0.686844, “Lemma E.5 (Bounding interval drift)”, *Simulated Tempering Langevin Monte Carlo II: An Improved Proof using Soft Markov Chain Decomposition*.
26. `boundary attainment SDPI` — top result 25734504, score 0.599953, “Lemma 3.1”, *Blowup behavior for a degenerate elliptic sinh-Poisson equation with variable intensities*.
27. `nonattainment contraction coefficient` — top result 24001842, score 0.702288, “Lemma 4.8”, *On generalized lc pairs with $\mathrm{\textbf b}$-log abundant nef part*.

## Retained serious candidates

### Theorem ID 25642881: Theorem (Contraction Coefficient Bound)

- **Exact query/queries:** `contraction coefficient binary input distributions`; `Rényi divergence contraction coefficient support lemma`
- **Statement:** $$ {\eta_{\chi^2}}\!\left(P_{X},P_{Y|X}\right) \leq {\eta_{ sf{\tiny KL}}}\!\left(P_{X},P_{Y|X}\right) \leq \frac{{\eta_{\chi^2}}\!\left(P_{X},P_{Y|X}\right)}{\displaystyle{\min_{x \in {\mathcal{X}}}{P_X(x)}}} \, . $$
- **Paper:** *Linear Bounds between Contraction Coefficients for $f$-Divergences*
- **Authors/year:** Anuran Makur, Lizhong Zheng (2018)
- **Source:** http://arxiv.org/abs/1510.01844v4
- **Similarity:** 0.621125
- **Relevance:** A genuine comparison theorem for contraction coefficients; relevant to general-divergence bounds, not an attainment theorem.

### Theorem ID 25642883: Theorem (General Contraction Coefficient Bound)

- **Exact query/queries:** `f-divergence contraction coefficient two point distributions`; `contraction coefficient operator convex divergence`
- **Statement:** Suppose we are given a convex function $f:(0,\infty) \rightarrow {\mathbb{R}}$ that is strictly convex and thrice differentiable at unity with $f(1) = 0$ and $f^{\prime \prime}(1) > 0$, and satisfies:
\begin{equation}
\label{Eq:General Pinsker Condition}
\left(f(t) - f^{\prime}(1) (t-1)\right)\!\!\left(1 - \frac{f^{\prime \prime \prime}(1)}{3 f^{\prime \prime}(1)}(t-1)\right) \geq \frac{f^{\prime \prime}(1)}{2}(t-1)^2
\end{equation}
for every $t \in (0,\infty)$. Suppose further that the difference quotient $g:(0,\infty) \rightarrow {\mathbb{R}}$, defined as $g(x) = \frac{f(x) - f(0)}{x}$, is concave. Then, we have:
$$ {\eta_{\chi^2}} \leq \eta_{f} \leq \frac{f^{\prime}(1) + f(0)}{\displaystyle{f^{\prime \prime}(1) \min_{x \in {\mathcal{X}}}{P_X(x)}}} \, {\eta_{\chi^2}} $$
where ${\eta_{\chi^2}} = {\eta_{\chi^2}}\!\left(P_{X},P_{Y|X}\right)$ and $\eta_{f} = \eta_{f}\!\left(P_{X},P_{Y|X}\right)$.
- **Paper:** *Linear Bounds between Contraction Coefficients for $f$-Divergences*
- **Authors/year:** Anuran Makur, Lizhong Zheng (2018)
- **Source:** http://arxiv.org/abs/1510.01844v4
- **Similarity:** 0.681251
- **Relevance:** A general contraction-coefficient comparison bound. It may support an abstract-divergence extension, but does not imply exact binary reduction.

### Theorem ID 25735529: Theorem 21

- **Exact query/queries:** `contraction coefficient binary input distributions`
- **Statement:** Consider a binary input channel $P_{Y|X}:\{0,1\}\to  {\mathcal{Y}} $ with $P_{Y|X=0}=P$ and $P_{Y|X=1}=Q$. Then, its contraction coefficient $\eta_{  KL} (P_{Y|X})=\eta_{\chi^2} (P_{Y|X})\triangleq \eta (\{P,Q\})$ satisfies  \begin {equation} \frac {H^2(P,Q)}{2} \leq \eta (\{P,Q\}) \leq H^2(P,Q) - \frac {H^4(P,Q)}{2}\,, \label {eq:etaPQ} \end {equation} where Hellinger distance is defined as $H^2(P,Q) \triangleq 2 - 2\int \sqrt {dP dQ}$.
- **Paper:** *Strong data-processing inequalities for channels and Bayesian networks*
- **Authors/year:** Yury Polyanskiy, Yihong Wu (2016)
- **Source:** http://arxiv.org/abs/1508.06025v4
- **Similarity:** 0.748647
- **Relevance:** A genuine SDPI result; useful context for binary-input channels, but it does not by itself establish the desired support reduction.

### Theorem ID 26873328: Theorem 1

- **Exact query/queries:** `local differential privacy contraction`
- **Statement:** A mechanism ${\mathsf K} $ is $(\varepsilon , \delta )$-LDP if and only if $\eta _{e^\varepsilon }({\mathsf K} )\leq \delta $ or equivalently \begin{equation*}
- **Paper:** *Local Differential Privacy Is Equivalent to Contraction of $E_γ$-Divergence*
- **Authors/year:** Shahab Asoodeh, Maryam Aliakbarpour, Flavio P. Calmon (2021)
- **Source:** http://arxiv.org/abs/2102.01258v1
- **Similarity:** 0.662837
- **Relevance:** Connects local differential privacy to contraction of an $E_\gamma$ divergence. Relevant to the proposed $D_\infty$/privacy direction, not a direct Rényi reduction.

### Theorem ID 21334515: Proposition 3.1 (Functional form of SDPI)

- **Exact query/queries:** `contraction coefficient binary input distributions`; `nonattainment contraction coefficient`
- **Statement:** Fix an admissible pair $(\mu ,K)$ and let $(X,Y)$ be a random pair with probability law $\mu \otimes K$. Then $\eta _\Phi (\mu ,K) \le c$ if and only if the inequality\begin{align}  \operatorname {Ent}_\Phi [f(X)] \le \frac{1}{1-c} \mathbb {E}\left[ \operatorname {Ent}_\Phi [f(X)|Y]\right] \end{align}holds for all nonconstant $f \in {\mathscr F}^0_*({\mathsf X})$ with $\mathbb {E}[f(X)]=1$. Consequently,\begin{align}  \eta _\Phi (\mu ,K) & = \sup \left\{  \frac{\operatorname {Ent}_\Phi \left[K^* f(Y)\right]}{\operatorname {Ent}_\Phi \left[f(X)\right]} : f \in {\mathscr F}^0_*({\mathsf X}), \,  f \neq {\rm const},\,  \mathbb {E}[f(X)]=1\right\}  \\ & = 1 - \inf \left\{  \frac{\mathbb {E}\left[ \operatorname {Ent}_\Phi [f(X)|Y]\right]}{\operatorname {Ent}_\Phi [f(X)]} : f \in {\mathscr F}^0_*({\mathsf X}), \,  f \neq {\rm const},\,  \mathbb {E}[f(X)]=1\right\} . \end{align}
- **Paper:** *Strong data processing inequalities and $Φ$-Sobolev inequalities for discrete channels*
- **Authors/year:** Maxim Raginsky (2016)
- **Source:** http://arxiv.org/abs/1411.3575v4
- **Similarity:** 0.655177
- **Relevance:** Functional SDPI representation; relevant to local/functional compactification, but no direct nonattainment dichotomy.

### Theorem ID 25735509: Theorem 1 (\cite [Proposition II.4.10]{CKZ98})

- **Exact query/queries:** `Rényi divergence contraction coefficient support lemma`; `f-divergence contraction coefficient two point distributions`; `max-divergence contraction coefficient`; `maximal leakage max divergence contraction`; `contraction coefficient operator convex divergence`
- **Statement:** For every $f$-divergence, we have  \begin {align}\label {eq:eta_ub} \eta _f(P_{Y|X}) \le \eta_{  TV} (P_{Y|X}). \end {align}
- **Paper:** *Strong data-processing inequalities for channels and Bayesian networks*
- **Authors/year:** Yury Polyanskiy, Yihong Wu (2016)
- **Source:** http://arxiv.org/abs/1508.06025v4
- **Similarity:** 0.676673
- **Relevance:** A genuine contraction-coefficient representation inherited from Csiszár–Körner–Zak; useful background, but not a two-point-support proof for Rényi ratios.

### Theorem ID 27027606: Theorem 3.5 (Winkler, 1988)

- **Exact query/queries:** `moment constrained probability measures extreme points`
- **Statement:** Let $\mathcal{M}\subset \mathcal{P}(Y)$ be defined as in \eqref {eq.moments}.\  Then, the set $\mathcal{M}$ is convex and \begin{align*}  \ex \mathcal{M}\subset \Big\{  & \vartheta \in \mathcal{M}\colon \vartheta = \sum _{i = 1}^m a_i \delta _{y_i} \text{ with } y_i \in Y,\,  a_i > 0,\,  \sum _{i=1}^m a_i = 1,\,  1 \le m \le n+1,\\ & \text{and the vectors } (f_1(y_i),\dots , f_n(y_i), 1),\,  1 \le i \le m, \text{ are linearly independent} \, \Big\} . \end{align*} Equality of sets holds if the moment conditions in \eqref {eq.moments} are given by equalities.
- **Paper:** *Risk measures based on weak optimal transport*
- **Authors/year:** Michael Kupper, Max Nendel, Alessandro Sgarabottolo (2023)
- **Source:** http://arxiv.org/abs/2312.05973v1
- **Similarity:** 0.752177
- **Relevance:** Quotes Winkler’s moment-set extreme-point theorem. This is the closest external general tool: one probability normalisation plus one moment constraint yields support bounds, though the finite-dimensional lemma here is elementary and proved directly.

### Theorem ID 25735510: Theorem 2

- **Exact query/queries:** `f-divergence contraction coefficient two point distributions`; `max-divergence contraction coefficient`
- **Statement:** Let $f$ be twice continuously differentiable on $(0,\infty )$ with $f''(1) > 0$. Then for any $P_X$ that is not a point mass, \begin {equation} \eta _{\chi ^2}(P_{Y|X},P_X) \le \eta _f(P_{Y|X},P_X)\,, \label {eq:eta_lb-Q} \end {equation} and \begin {equation} \label {eq:eta_lb} \eta _{\chi ^2}(P_{Y|X}) \le \eta _f(P_{Y|X})\,. \end {equation}
- **Paper:** *Strong data-processing inequalities for channels and Bayesian networks*
- **Authors/year:** Yury Polyanskiy, Yihong Wu (2016)
- **Source:** http://arxiv.org/abs/1508.06025v4
- **Similarity:** 0.683764
- **Relevance:** A genuine SDPI theorem; potentially useful for comparing divergences, without resolving the fixed-likelihood-ratio extreme-point step.

## Representative rejected results and rejection reasons

- **26619807, Corollary 1, *Stochastic Mechanistic Interaction* (score 0.602):** “binary” is causal-variable terminology; unrelated to divergence contraction.
- **17757448, Theorem 6.2, *Approximate polymorphisms of predicates* (score 0.579):** binary Boolean functions, not channels or SDPI.
- **24520817, contraction-reduction lemma (score 0.656):** Langevin mixing lemma; lexical match only.
- **25711965/25711966, Sason–Verdú corollaries:** Rényi hypothesis-testing bounds, but no input-support reduction or contraction-coefficient attainment.
- **Dobrushin-query hits 25717845 and 25870949:** Markov-chain bounds not statements about the $D_\infty$ ratio at issue.
- **Boundary-attainment query hits 25734504, 24017453, 25936276:** unrelated PDE, graph, and interpolation results.
- **Nonattainment hit 24001842:** algebraic geometry; lexical false positive.
- **Support-size hits 19685759 and 17388820:** sampling/optimal transport sparsity results with different feasible sets and objectives.

## Source inspection record

- Polyanskiy and Wu, *Strong data-processing inequalities for channels and Bayesian networks*, arXiv:1508.06025 (TheoremSearch indexes the 2016 version): inspected through the retrieved theorem statements and paper metadata; retained only as SDPI context.
- Makur and Zheng, *Linear Bounds between Contraction Coefficients for f-Divergences*, arXiv:1510.01844 / journal-era 2018 metadata: inspected for its comparison role; it does not state this Rényi binary-support result.
- Kupper, Nendel and Sgarabottolo, *Risk measures based on weak optimal transport*, arXiv source containing Theorem 3.5 (Winkler, 1988): inspected as a modern statement of the moment-set extreme-point theorem.
- Asoodeh, Aliakbarpour and Calmon, *Local Differential Privacy Is Equivalent to Contraction of $E_\gamma$-Divergence*, arXiv:2102.01258: inspected for the privacy connection only.

## Reproducibility

The exact response bodies (including all ten results per call) were retained during the run in `/tmp/ts/results.ndjson`; this temporary execution artefact is not committed. The entries above retain every serious candidate and enough metadata to repeat each request.

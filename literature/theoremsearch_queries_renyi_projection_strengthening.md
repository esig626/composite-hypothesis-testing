# TheoremSearch query log

For every theorem-level search, record:

- manuscript result being checked;
- date;
- exact query;
- filters used;
- strongest returned candidates;
- candidates inspected in full;
- conclusion and residual uncertainty.

A failed search is evidence only about that query, not proof of novelty.

## Joint Rényi projection strengthening search (2026-08-13)

**Manuscript result:** “Uniform Rényi bounds from a dominated projection” and its feasible one-sided derivative lemma.
**API:** `POST https://api.theoremsearch.com/search`; every request used `n_results: 10`; no filters.
**Warning:** similarity is a retrieval score, not mathematical overlap. Only entries marked retained were serious candidates.

### Q01
- **Exact query:** `Rényi Pythagorean theorem projection onto convex set`
- **Retained theorem ID:** `21595956`; slogan ID `6521635`.
  - **Theorem:** Theorem 10.
  - **Statement:** The following statements hold. \begin{itemize} \item[(a)]({\em Projection and the Pythagorean property}): A probability measure $Q\in \mathbb {E} \cap B(R,\infty )$ is a forward $\mathscr {I}_{\alpha }$-projection of $R$ on the convex set $\mathbb {E}$ of probability measures if and only if every $P \in \mathbb {E} \cap B(R,\infty )$ satisfies (\ref{p1:eqn:pythagorean_inequality}). If the forward $\mathscr {I}_{\alpha }$-projection is an algebraic inner point of $\mathbb {E}$ then $\mathbb {E} \subset B(R,\infty )$ and (\ref{p1:eqn:pythagorean_equality}) holds for every $P \in \mathbb {E}$. \item[(b)]({\em Subspace-transitivity}): Let $\mathbb {E}$ and $\mathbb {E}_1 \subset \mathbb {E}$ be convex sets of probability measures. Let $R$ have the forward $\mathscr {I}_{\alpha }$-projection $Q$ on $\mathbb {E}$ and the forward $\mathscr {I}_{\alpha }$-projection $Q_1$ on $\mathbb {E}_1$, and suppose that (\ref{p1:eqn:pythagorean_equality}) holds for every $P \in \mathbb {E}$. Then $Q_1$ is the forward $\mathscr {I}_{\alpha }$-projection of $Q$ on $\mathbb {E}_1$. (See figure \ref{p1:fig:transitivity}). \end{itemize}
  - **Source:** *Minimization Problems Based on Relative $α$-Entropy I: Forward Projection*, M. Ashok Kumar, Rajesh Sundaresan (2015); `1410.2346v3`.
  - **Similarity:** `0.716072325355336`.

### Q02
- **Exact query:** `Rényi divergence projection on convex probability distributions`
- **Retained theorem ID:** `21229206`; slogan ID `6159242`.
  - **Theorem:** Theorem 1 (Existence of forward $D_{\alpha }$-projection).
  - **Statement:** Let $\alpha \in (0,\infty )$, and let $Q$ be an arbitrary probability measure defined on a set $\mathcal{A}$. Let $\mathcal{P}$ be an $\alpha $-convex set of probability measures defined on $\mathcal{A}$, and assume that $\mathcal{P}$ is closed with respect to the total variation distance. If there exists $P\in \mathcal{P}$ such that $D_{\alpha }(P\| Q)<\infty $, then there exists a forward $D_{\alpha }$-projection of $Q$ on $\mathcal{P}$.
  - **Source:** *Projection Theorems for the Rényi Divergence on $α$-Convex Sets*, M. Ashok Kumar, Igal Sason (2016); `1512.02515v2`.
  - **Similarity:** `0.7170646831749125`.
- **Retained theorem ID:** `21595954`; slogan ID `6521633`.
  - **Theorem:** Theorem 8 (Existence and uniqueness of the forward $\mathscr {I}_{\alpha }$-projection).
  - **Statement:** Fix $\alpha > 0$, $\alpha \neq 1$. Let $\mathbb {E}$ be a set of probability measures whose corresponding set of density functions $\mathcal{E}$ is convex and closed in $L^{\alpha }(\mu )$. Let $R$ be a probability measure (with density $r$) and suppose that $\mathscr {I}_{\alpha }(P,R) < \infty $ for some $P \in \mathbb {E}$. Then $R$ has a unique forward $\mathscr {I}_{\alpha }$-projection on $\mathbb {E}$.
  - **Source:** *Minimization Problems Based on Relative $α$-Entropy I: Forward Projection*, M. Ashok Kumar, Rajesh Sundaresan (2015); `1410.2346v3`.
  - **Similarity:** `0.6985892000336997`.

### Q03
- **Exact query:** `alpha-convex set Rényi projection existence uniqueness Pythagorean inequality`
- **Retained theorem ID:** `21229205`; slogan ID `6159241`.
  - **Theorem:** Proposition 1 (The Pythagorean property).
  - **Statement:** Let $\alpha \in (0,1)\cup (1,\infty )$, let $\mathcal{P}\subseteq \mathcal{M}$ be an $\alpha $-convex set, and $Q\in \mathcal{M}$.\begin{enumerate}[a)]\item If $P^*$ is a forward $D_{\alpha }$-projection of $Q$ on $\mathcal{P}$, then \begin{eqnarray} D_{\alpha }(P\| Q)\ge D_{\alpha }(P\| P^*)+D_{\alpha }(P^*\| Q), \quad \forall \, P \in \mathcal{P}. \end{eqnarray} Furthermore, if $\alpha >1$, then $\text{Supp}(P^*) = \text{Supp}(\mathcal{P})$. \item Conversely, if \eqref{pythagorean-inequality1} is satisfied for some $P^*\in \mathcal{P}$, then $P^*$ is a forward $D_{\alpha }$-projection of $Q$ on $\mathcal{P}$. \end{enumerate}
  - **Source:** *Projection Theorems for the Rényi Divergence on $α$-Convex Sets*, M. Ashok Kumar, Igal Sason (2016); `1512.02515v2`.
  - **Similarity:** `0.7316323358793784`.
- **Retained theorem ID:** `22017175`; slogan ID `6938445`.
  - **Theorem:** Theorem 14 (Pythagorean Inequality).
  - **Statement:** Let $\alpha \in (0,\infty )$. Suppose that $\mathcal{P}$ is an $\alpha $-convex set of distributions. Let $Q$ be an arbitrary distribution and suppose that the \emph{$\alpha $-information projection}\begin{equation} P^\ast = \operatorname*{arg\, min}_{P \in \mathcal{P}} D_\alpha (P\| Q) \end{equation}exists. Then we have the Pythagorean inequality\begin{equation} D_\alpha (P\| Q) \geq D_\alpha (P\| P^\ast ) + D_\alpha (P^\ast \| Q) \qquad \text{for all $P \in \mathcal{P}$.} \end{equation}
  - **Source:** *Rényi Divergence and Kullback-Leibler Divergence*, Tim van Erven, Peter Harremoës (2014); `1206.2459v2`.
  - **Similarity:** `0.7145278709564258`.
- **Retained theorem ID:** `21595954`; slogan ID `6521633`.
  - **Theorem:** Theorem 8 (Existence and uniqueness of the forward $\mathscr {I}_{\alpha }$-projection).
  - **Statement:** Fix $\alpha > 0$, $\alpha \neq 1$. Let $\mathbb {E}$ be a set of probability measures whose corresponding set of density functions $\mathcal{E}$ is convex and closed in $L^{\alpha }(\mu )$. Let $R$ be a probability measure (with density $r$) and suppose that $\mathscr {I}_{\alpha }(P,R) < \infty $ for some $P \in \mathbb {E}$. Then $R$ has a unique forward $\mathscr {I}_{\alpha }$-projection on $\mathbb {E}$.
  - **Source:** *Minimization Problems Based on Relative $α$-Entropy I: Forward Projection*, M. Ashok Kumar, Rajesh Sundaresan (2015); `1410.2346v3`.
  - **Similarity:** `0.7079154849052882`.
- **Retained theorem ID:** `21229206`; slogan ID `6159242`.
  - **Theorem:** Theorem 1 (Existence of forward $D_{\alpha }$-projection).
  - **Statement:** Let $\alpha \in (0,\infty )$, and let $Q$ be an arbitrary probability measure defined on a set $\mathcal{A}$. Let $\mathcal{P}$ be an $\alpha $-convex set of probability measures defined on $\mathcal{A}$, and assume that $\mathcal{P}$ is closed with respect to the total variation distance. If there exists $P\in \mathcal{P}$ such that $D_{\alpha }(P\| Q)<\infty $, then there exists a forward $D_{\alpha }$-projection of $Q$ on $\mathcal{P}$.
  - **Source:** *Projection Theorems for the Rényi Divergence on $α$-Convex Sets*, M. Ashok Kumar, Igal Sason (2016); `1512.02515v2`.
  - **Similarity:** `0.6972616396950141`.

### Q04
- **Exact query:** `Hellinger integral maximisation variational inequality convex probability class`
- **No serious candidate retained.** Highest result: ID `5226547`, Lemma 3.1, *Local X-ray Transform on Asymptotically Hyperbolic Manifolds via Projective Compactification*, score `0.6955264236503773`; it did not establish the searched claim.

### Q05
- **Exact query:** `closest pair between two convex sets of probability measures divergence`
- **Retained theorem ID:** `19908573`; slogan ID `4737970`.
  - **Theorem:** Theorem 6 (Adversarial Chernoff Theorem).
  - **Statement:** For any finite domain $\Omega $ and closed, convex sets of distributions $P,Q \subseteq \mathbb R^{\Omega }$, we have\[ \gamma _{\mathrm{adv}}(P,Q) = \min _{p \in P, q \in Q} \Gamma ^*(p,q)\, . \]
  - **Source:** *Adversarial hypothesis testing and a quantum Stein's Lemma for restricted measurements*, Fernando G. S. L. Brandao, Aram W. Harrow, James R. Lee, Yuval Peres (2020); `1308.6702v4`.
  - **Similarity:** `0.6669072508381765`.

### Q06
- **Exact query:** `f-divergence nearest pair two convex probability sets existence uniqueness`
- **No serious candidate retained.** Highest result: ID `22756343`, Corollary \thesection .3, *Lower bounds for the minimax risk using $f$-divergences and applications*, score `0.6969954082383502`; it did not establish the searched claim.

### Q07
- **Exact query:** `supporting hyperplane characterisation divergence projection probability measures`
- **No serious candidate retained.** Highest result: ID `26706030`, Theorem B.1 (\citet {Sun:2018:Functional_Variational_Bayesian_Neural_Networks}), *The Gaussian Neural Process*, score `0.6810991764068604`; it did not establish the searched claim.

### Q08
- **Exact query:** `strict convexity uniqueness Rényi divergence projection`
- **Retained theorem ID:** `21595954`; slogan ID `6521633`.
  - **Theorem:** Theorem 8 (Existence and uniqueness of the forward $\mathscr {I}_{\alpha }$-projection).
  - **Statement:** Fix $\alpha > 0$, $\alpha \neq 1$. Let $\mathbb {E}$ be a set of probability measures whose corresponding set of density functions $\mathcal{E}$ is convex and closed in $L^{\alpha }(\mu )$. Let $R$ be a probability measure (with density $r$) and suppose that $\mathscr {I}_{\alpha }(P,R) < \infty $ for some $P \in \mathbb {E}$. Then $R$ has a unique forward $\mathscr {I}_{\alpha }$-projection on $\mathbb {E}$.
  - **Source:** *Minimization Problems Based on Relative $α$-Entropy I: Forward Projection*, M. Ashok Kumar, Rajesh Sundaresan (2015); `1410.2346v3`.
  - **Similarity:** `0.720560517377997`.

### Q09
- **Exact query:** `Rényi projection equality conditions Pythagorean inequality`
- **Retained theorem ID:** `21595956`; slogan ID `6521635`.
  - **Theorem:** Theorem 10.
  - **Statement:** The following statements hold. \begin{itemize} \item[(a)]({\em Projection and the Pythagorean property}): A probability measure $Q\in \mathbb {E} \cap B(R,\infty )$ is a forward $\mathscr {I}_{\alpha }$-projection of $R$ on the convex set $\mathbb {E}$ of probability measures if and only if every $P \in \mathbb {E} \cap B(R,\infty )$ satisfies (\ref{p1:eqn:pythagorean_inequality}). If the forward $\mathscr {I}_{\alpha }$-projection is an algebraic inner point of $\mathbb {E}$ then $\mathbb {E} \subset B(R,\infty )$ and (\ref{p1:eqn:pythagorean_equality}) holds for every $P \in \mathbb {E}$. \item[(b)]({\em Subspace-transitivity}): Let $\mathbb {E}$ and $\mathbb {E}_1 \subset \mathbb {E}$ be convex sets of probability measures. Let $R$ have the forward $\mathscr {I}_{\alpha }$-projection $Q$ on $\mathbb {E}$ and the forward $\mathscr {I}_{\alpha }$-projection $Q_1$ on $\mathbb {E}_1$, and suppose that (\ref{p1:eqn:pythagorean_equality}) holds for every $P \in \mathbb {E}$. Then $Q_1$ is the forward $\mathscr {I}_{\alpha }$-projection of $Q$ on $\mathbb {E}_1$. (See figure \ref{p1:fig:transitivity}). \end{itemize}
  - **Source:** *Minimization Problems Based on Relative $α$-Entropy I: Forward Projection*, M. Ashok Kumar, Rajesh Sundaresan (2015); `1410.2346v3`.
  - **Similarity:** `0.6622940696653276`.

### Q10
- **Exact query:** `saddle point Hellinger transform composite hypotheses`
- **No serious candidate retained.** Highest result: ID `21279004`, Proposition 13, *A new method for estimation and model selection: $ρ$-estimation*, score `0.6024538809902537`; it did not establish the searched claim.

### Q11
- **Exact query:** `minimax Hellinger integral convex sets probability measures`
- **No serious candidate retained.** Highest result: ID `20129768`, Lemma (Kleijn-Van der Vaart (2006)), *An approach to large-scale Quasi-Bayesian inference with spike-and-slab priors*, score `0.6892048696394899`; it did not establish the searched claim.

### Q12
- **Exact query:** `continuity stability of Rényi projection minimiser`
- **No serious candidate retained.** Highest result: ID `19854054`, Proposition 2.7, *Projections of Mandelbrot percolation in higher dimensions*, score `0.6467478293108386`; it did not establish the searched claim.

### Q13
- **Exact query:** `Differentiability in order of minimum Rényi divergence envelope theorem`
- **No serious candidate retained.** Highest result: ID `18368282`, Lemma 30, *Analysis of Langevin Monte Carlo from Poincaré to Log-Sobolev*, score `0.6657592851828866`; it did not establish the searched claim.

### Q14
- **Exact query:** `Envelope theorem Rényi divergence optimisation over distributions`
- **No serious candidate retained.** Highest result: ID `20024396`, Theorem .5, *Distributional Robustness and Uncertainty Quantification for Rare Events*, score `0.698282372337241`; it did not establish the searched claim.

### Q15
- **Exact query:** `Rényi projection varying supports zero densities`
- **No serious candidate retained.** Highest result: ID `22913228`, Lemma 3.7, *Minimization of divergences on sets of signed measures*, score `0.6425778418196777`; it did not establish the searched claim.

### Q16
- **Exact query:** `Rényi projection without common support absolute continuity`
- **No serious candidate retained.** Highest result: ID `19431494`, Lemma A.4, *Sampling Matrices from Harish-Chandra-Itzykson-Zuber Densities with Applications to Quantum Inference and Differential Privacy*, score `0.667618115516163`; it did not establish the searched claim.

### Q17
- **Exact query:** `extended likelihood ratio projection convex probability classes`
- **No serious candidate retained.** Highest result: ID `26876378`, Lemma 8, *Secure list decoding and its application to bit-string commitment*, score `0.6130758985190556`; it did not establish the searched claim.

### Q18
- **Exact query:** `convex duality Hellinger integral probability measures`
- **No serious candidate retained.** Highest result: ID `26880348`, Lemma 9, *Optimal Accounting of Differential Privacy via Characteristic Function*, score `0.6742272383773865`; it did not establish the searched claim.

### Q19
- **Exact query:** `three-point identity inequality Rényi divergence`
- **No serious candidate retained.** Highest result: ID `21473814`, Theorem 2, *Entropy bounds on abelian groups and the Ruzsa divergence*, score `0.7157240509987081`; it did not establish the searched claim.

### Q20
- **Exact query:** `Bregman style inequality for Rényi divergence projection`
- **No serious candidate retained.** Highest result: ID `26385354`, Proposition (Generalised Pythagorean Theorem), *Bandit Convex Optimisation*, score `0.7177564073946348`; it did not establish the searched claim.

### Q21
- **Exact query:** `existence divergence projection tightness coercivity probability measures`
- **No serious candidate retained.** Highest result: ID `18898959`, Lemma 6.11 ({\cite[Lemma 3.14]{feng2021random}}), *Entrance measures for semigroups of time-inhomogeneous SDEs: possibly degenerate and expanding*, score `0.6899970194694718`; it did not establish the searched claim.

### Q22
- **Exact query:** `Rényi divergence lower semicontinuity compact sublevel projection`
- **Retained theorem ID:** `22017180`; slogan ID `6938450`.
  - **Theorem:** Theorem 19.
  - **Statement:** Suppose that $\mathcal{X}$ is a Polish space. Then for any order $\alpha \in (0,\infty ]$, $D_\alpha (P\| Q)$ is a lower semi-continuous function of the pair $(P,Q)$ in the weak topology.
  - **Source:** *Rényi Divergence and Kullback-Leibler Divergence*, Tim van Erven, Peter Harremoës (2014); `1206.2459v2`.
  - **Similarity:** `0.6736836408316037`.

### Q23
- **Exact query:** `joint Rényi projection pair convex sets variational inequality`
- **No serious candidate retained.** Highest result: ID `13341003`, Lemma 1, *Proportional-Integral Projected Gradient Method for Model Predictive Control*, score `0.6608682684279358`; it did not establish the searched claim.

### Q24
- **Exact query:** `Rényi divergence alpha convex Pythagorean theorem uniqueness`
- **Retained theorem ID:** `22017173`; slogan ID `6938443`.
  - **Theorem:** Theorem 12.
  - **Statement:** For any order $\alpha \in [0,\infty ]$ R\'{e}nyi divergence is convex in its second argument. That is, for any probability distributions $P$, $Q_0$ and $Q_1$\begin{equation} D_{\alpha }(P\Vert (1-\lambda )Q_{0}+\lambda Q_{1}) \leq (1-\lambda )D_{\alpha }(P\Vert Q_{0})+\lambda D_{\alpha }(P\Vert Q_{1}) \end{equation}for any $0 < \lambda < 1$. For finite $\alpha $, equality holds if and only if\begin{flalign*} \text{$\alpha = 0$: } & \text{$D_0(P\Vert Q_{0}) = D_0(P\Vert Q_{1})$;} & \\ \text{$0 < \alpha < \infty $: } & \text{$q_0 = q_1$ ($P$-a.s.)} \end{flalign*}
  - **Source:** *Rényi Divergence and Kullback-Leibler Divergence*, Tim van Erven, Peter Harremoës (2014); `1206.2459v2`.
  - **Similarity:** `0.7097884147728839`.
- **Retained theorem ID:** `21595954`; slogan ID `6521633`.
  - **Theorem:** Theorem 8 (Existence and uniqueness of the forward $\mathscr {I}_{\alpha }$-projection).
  - **Statement:** Fix $\alpha > 0$, $\alpha \neq 1$. Let $\mathbb {E}$ be a set of probability measures whose corresponding set of density functions $\mathcal{E}$ is convex and closed in $L^{\alpha }(\mu )$. Let $R$ be a probability measure (with density $r$) and suppose that $\mathscr {I}_{\alpha }(P,R) < \infty $ for some $P \in \mathbb {E}$. Then $R$ has a unique forward $\mathscr {I}_{\alpha }$-projection on $\mathbb {E}$.
  - **Source:** *Minimization Problems Based on Relative $α$-Entropy I: Forward Projection*, M. Ashok Kumar, Rajesh Sundaresan (2015); `1410.2346v3`.
  - **Similarity:** `0.7002326667448097`.

### Q25
- **Exact query:** `Hellinger affinity closest convex distributions supporting hyperplane`
- **No serious candidate retained.** Highest result: ID `5226547`, Lemma 3.1, *Local X-ray Transform on Asymptotically Hyperbolic Manifolds via Projective Compactification*, score `0.6415553329058137`; it did not establish the searched claim.

### Consolidated retained IDs

- `21229205` — Kumar–Sason Proposition 1, Pythagorean property.
- `21229206` — Kumar–Sason Theorem 1, existence of forward Rényi projection.
- `22017173` — van Erven–Harremoës Theorem 12, convexity in the second argument.
- `22017175` — van Erven–Harremoës Theorem 14, α-convex Pythagorean inequality.
- `22017180` — van Erven–Harremoës Theorem 19, weak lower semicontinuity on Polish spaces.
- `21595954` — Ashok Kumar–Sundaresan Theorem 8, existence/uniqueness for relative α-entropy.
- `21595956` — Ashok Kumar–Sundaresan Theorem 10, relative α-entropy Pythagorean property.
- `19908573` — Adversarial Chernoff Theorem (finite domain).

**Conclusion:** serious results supply strong one-class α-convex projection theorems and weak lower semicontinuity, but no retained theorem directly gives a two-class, ordinary-convex, varying-support Pythagorean theorem or extended-likelihood-ratio moment certificate. This is not a novelty conclusion.

# Global notation and terminology audit

## Purpose

This file is an editorial inventory for the publication pass. It does **not** change the mathematics. The goal is to make the paper readable before theorem-by-theorem revision.

The working principles are:

1. Use one notation for one object throughout the paper.
2. Do not introduce a named object unless it is used repeatedly.
3. Prefer standard statistical language over manuscript-specific jargon.
4. Keep technical measure-theoretic notation local to the proof or subsection where it is needed.
5. Do not give theorems descriptive titles unless the title materially helps navigation.
6. Distinguish clearly between:
   - a hypothesis class;
   - a density representation of that class;
   - a selected pair of laws;
   - a test statistic built from that pair;
   - the actual minimax value.
7. Preserve orientation in every asymmetric divergence. In particular, never hide the distinction between \(D(Q\|P)\) and \(D(P\|Q)\).

---

# 1. Core testing notation

| Current notation | Current meaning | Proposed action |
|---|---|---|
| \((\mathcal X,\mathcal F)\) | Sample space | **KEEP.** Standard and clean. |
| \(\mathcal P\) | Null class of laws | **KEEP.** |
| \(\mathcal Q\) | Alternative class of laws | **KEEP.** |
| \(P,Q\) | Generic null/alternative laws | **KEEP.** |
| \(P^n,Q^n\) | Product laws | **KEEP**, but state once that \(P^n=P^{\otimes n}\). |
| \(X^n\) | Sample | **KEEP.** |
| \(\mathsf T_n\) | All randomised tests | **KEEP if used often**; otherwise define the admissible test directly and remove this extra symbol. |
| \(\varphi_n\) | Generic randomised test | **KEEP.** |
| \(\alpha_n(\varphi_n;\mathcal P)\) | Worst-case Type I error | **KEEP.** This is standard and immediately recognisable. |
| \(\beta_n(\varphi_n;\mathcal Q)\) | Worst-case Type II error | **KEEP.** |
| \(\Phi_n(r;\mathcal P)\) | Tests satisfying the exponential Type I constraint | **KEEP provisionally.** Useful if it appears throughout many proofs. |
| \(\beta_n^\star(r;\mathcal P,\mathcal Q)\) | Composite minimax Type II error | **KEEP.** This is the central finite-blocklength quantity. |
| \(\beta_{n,\mathrm{sp}}^\star(r;P,Q)\) | Simple binary optimum | **RENAME/REVIEW.** The subscript `sp` is visually clumsy. Prefer something such as \(\beta_n^\star(r;P,Q)\) when the arguments make the simple case unambiguous, or a cleaner dedicated symbol if ambiguity genuinely arises. |
| \(r\) | Exponential Type I rate | **KEEP.** |
| \(\varepsilon\) | Fixed Type I level | **KEEP.** This cleanly distinguishes the fixed-level regime from the exponential-rate regime. |
| \(\Phi_{n,\varepsilon}(\mathcal P)\) | Tests satisfying fixed Type I level | **KEEP if needed**; mirror the \(r\)-notation consistently. |
| \(\beta_{n,\varepsilon}^\star(\mathcal P,\mathcal Q)\) | Fixed-level minimax Type II error | **KEEP.** |

### Style decision

Use **“worst-case”** as an adjective and **“worst case”** as a noun phrase. Examples:

- “worst-case Type II error”;
- “the worst case over \(Q\in\mathcal Q\)”.

Use **“Type I error”** and **“Type II error”** without hyphenation.

---

# 2. Rényi and KL notation

| Current notation | Meaning | Proposed action |
|---|---|---|
| \(Z_\lambda(Q,P)\) | Order-\(\lambda\) Hellinger integral | **KEEP provisionally.** It is compact and used heavily. Do not alternate between “Hellinger integral”, “Chernoff functional”, “affinity”, etc. Use **Hellinger integral** consistently. |
| \(D_\lambda(Q\|P)\) | Rényi divergence | **KEEP.** |
| \(D(Q\|P)\) | KL divergence | **KEEP.** |
| \(D_\lambda(\mathcal Q\|\mathcal P)\) | Minimum Rényi divergence over \(Q\in\mathcal Q,P\in\mathcal P\) | **KEEP notation; CHANGE terminology.** Do not repeatedly call this the “directed composite Rényi separation”. Say “the minimum Rényi divergence from \(\mathcal Q\) to \(\mathcal P\)” or simply use the formula. |
| \(D(\mathcal Q\|\mathcal P)\) | Minimum KL divergence from alternative class to null class | **KEEP notation; CHANGE terminology.** Avoid “directed composite KL separation” except perhaps once if a compact descriptor is genuinely needed. |
| \(D(\mathcal P\|\mathcal Q)\) | Minimum KL divergence in the reverse orientation, used at fixed Type I level | **KEEP and emphasise orientation explicitly.** This reversal is mathematically important and should not be hidden by generic language. |
| \(d_\lambda,d_1\) | Local shorthand for the preceding minima | **REMOVE globally.** Use only inside the proof where it makes an argument shorter. Do not let \(d_\lambda\), \(D_\lambda^\star\), and \(D_\lambda(\mathcal Q\|\mathcal P)\) coexist as three names for the same object. |
| \(D_\lambda^\star\) | Another shorthand for the class minimum | **REMOVE.** This is a major source of notation duplication. Prefer \(D_\lambda(\mathcal Q\|\mathcal P)\). |
| \(r_{\rm crit}\) | Critical rate \(D(\mathcal Q\|\mathcal P)\) | **SIMPLIFY.** Either write the divergence directly or use \(r_c\) if the symbol is genuinely useful for a long argument. |

### Terminology decision

Preferred language:

- “minimum Rényi divergence from \(\mathcal Q\) to \(\mathcal P\)”;
- “minimum KL divergence from \(\mathcal Q\) to \(\mathcal P\)”;
- “critical rate” once the value is identified.

Avoid by default:

- “directed composite Rényi separation”;
- “directed composite Kullback--Leibler separation”.

The notation already records direction; the extra jargon does not add mathematical content.

---

# 3. Density classes and dominated-space notation

The manuscript currently uses both law classes and density classes:

- law classes: \(\mathcal P,\mathcal Q\);
- density classes: \(\mathscr P,\mathscr Q\subset L^1(\mu)\).

The visual distinction between \(\mathcal P\) and \(\mathscr P\) is too slight for a long technical paper.

## Proposed default

**Use \(\mathcal P,\mathcal Q\) for probability-law classes everywhere.**

When density sets are required, introduce them locally as, for example,

\[
\mathcal P_\mu:=\left\{\frac{dP}{d\mu}:P\in\mathcal P\right\},
\qquad
\mathcal Q_\mu:=\left\{\frac{dQ}{d\mu}:Q\in\mathcal Q\right\}.
\]

Alternative notation can be chosen later, but the paper should not rely on a calligraphic/script-font distinction to tell laws from densities.

| Current notation | Meaning | Proposed action |
|---|---|---|
| \(\mu\) | Dominating measure | **KEEP.** Standard. |
| \(\mathsf D_\mu\) | All probability densities w.r.t. \(\mu\) | **KEEP locally only.** It does not need to become global notation. |
| \(p,q\) | Densities of \(P,Q\) | **KEEP.** |
| \(\mathscr P,\mathscr Q\) | Density classes | **REPLACE** with a more visibly distinct local notation. |
| \(\xi=P_\lambda^\star+Q_\lambda^\star\) | Sum measure used to define the extended likelihood ratio | **LOCAL PROOF NOTATION.** Do not make this part of the conceptual statement unless unavoidable. |
| \(a=dP_\lambda^\star/d\xi, b=dQ_\lambda^\star/d\xi\) | RN densities relative to \(\xi\) | **MOVE TO PROOF / TECHNICAL DEFINITION.** These symbols clutter the theorem statement. |

---

# 4. Selected Rényi pair and test statistic

This is currently the most jargon-heavy part of the paper.

| Current notation | Meaning | Proposed action |
|---|---|---|
| \((P_\lambda^\star,Q_\lambda^\star)\) | Pair minimising \(D_\lambda(Q\|P)\) over the two classes | **KEEP.** Standard optimisation notation. |
| \((p_\lambda^\star,q_\lambda^\star)\) | Corresponding densities | **KEEP only when the proof requires densities.** |
| \(z_\lambda^\star\) | \(Z_\lambda(Q_\lambda^\star,P_\lambda^\star)\) | **REVIEW.** This shorthand is useful inside the projection proof but should not be carried through later sections if the full expression is clearer. |
| \(h_\lambda^\star\) | Extended log-likelihood ratio of the selected pair | **RENAME strongly recommended.** Prefer a notation that visibly means likelihood ratio, e.g. \(L_\lambda\) or \(\ell_\lambda\). |
| \(S_{n,\lambda}^\star\) | Sum of selected log-likelihood scores | **RENAME consistently with the preceding choice**, e.g. \(L_{n,\lambda}:=\sum_i L_\lambda(X_i)\). |
| \(\mathcal M_n\), \(\mathcal M_{n,\lambda}^\star\) | Samples containing both \(+\infty\) and \(-\infty\) score values | **KEEP LOCAL ONLY.** This is a technical measurability device, not conceptual notation. |
| \(\tau_{\lambda,r}^{\min}\) | Smallest threshold guaranteed admissible by the exponential-moment bound | **SIMPLIFY.** Prefer \(t_{\lambda,r}\) once its role is stated in words. The superscript `min` is cumbersome and invites later threshold variants. |
| \(\psi_n\) | Deterministic threshold test | **KEEP locally.** |
| \(\psi_{n,\tau,\eta}^{\lambda,\star}\) | Randomised threshold test | **SIMPLIFY.** This symbol carries four indices/superscripts. Prefer to fix \(\lambda\) and define \(\psi_{n,t,\eta}^{(\lambda)}\), or simply \(\psi_{t,\eta}\) within the calibration section. |

### Preferred terminology

Use:

- **“Rényi-minimising pair”** or **“selected pair”**;
- **“log-likelihood ratio of the selected pair”**;
- **“uniform exponential-moment bounds”**;
- **“threshold test based on the selected log-likelihood ratio”.**

Use “Rényi projection” sparingly, primarily when discussing geometry or literature on projection theorems.

Avoid routine use of:

- “joint Rényi projection”;
- “projected statistic”;
- “projected log--likelihood ratio”;
- “projected threshold”;
- “projected reverse Rényi construction”.

These phrases make elementary objects sound more specialised than they are.

---

# 5. Hoeffding/exponent notation

| Current notation | Meaning | Proposed action |
|---|---|---|
| \(F_r(\lambda;P,Q)\) | Hoeffding objective \((1-\lambda)/\lambda[D_\lambda(Q\|P)-r]\) | **KEEP.** Compact and useful. |
| \(\rho=(1-\lambda)/\lambda\) | Reparametrised Rényi order | **KEEP only in the minimax proof.** Do not make \(\rho\) a parallel global parametrisation. |
| \(G_r(\rho;P,Q)\) | Reparametrised Hoeffding objective | **LOCAL PROOF NOTATION.** |
| \(\lambda_r^\star\) | Saddle order | **KEEP.** |
| \(P_r^\star,Q_r^\star\) | Saddle pair at rate \(r\) | **KEEP**, but make the distinction from \(P_\lambda^\star,Q_\lambda^\star\) explicit once. |
| \(R_s,R_\rho,R_r^\star\) | Tilted/escort laws | **STANDARDISE.** The manuscript currently changes the parameter in the same construction. Choose one notation, preferably a \(\lambda\)-indexed tilted law, and specialise only when necessary. |
| \(E_{\rm H}(r;\mathcal P,\mathcal Q)\) | Exact subcritical minimax exponent | **KEEP provisionally.** If no competing exponent is used, consider the simpler \(E(r)\). |
| \(E_{\rm H}^{\rm sp}\) | Simple binary Hoeffding exponent | **REVIEW.** Avoid proliferating `sp` notation if the arguments already make the case clear. |

### Terminology

Preferred:

- “Hoeffding objective”;
- “saddle point”;
- “exact Type II error exponent”;
- “tilted law”.

Avoid by default:

- “Rényi--Hoeffding saddle point” as a repeated branded phrase;
- “projected test attains the exponent” when “the test has the optimal exponent” is clearer.

---

# 6. Calibration notation

This section currently carries too much notation for a conceptually simple operation: fix a score, vary a threshold and boundary randomisation, and use the largest admissible rule.

| Current notation | Meaning | Proposed action |
|---|---|---|
| \(\mathcal C_{n,\lambda}(r)\) | Admissible threshold/randomisation parameters | **REVIEW.** Can probably be eliminated by defining the optimisation directly. |
| \(\beta_{n,\lambda}^{\rm cal}\) | Best Type II error within the fixed-score threshold family | **KEEP if the calibration section remains a main result.** |
| \(\tau_{n,\lambda}^{\rm cal},\eta_{n,\lambda}^{\rm cal}\) | Calibrated threshold and boundary randomisation | **KEEP but simplify \(\tau\to t\) if threshold notation is changed globally.** |
| \(v_1<\cdots<v_m\) | Attainable score values | **KEEP local.** |
| \(A_j(\eta)\) | Worst-case Type I error along a boundary segment | **KEEP local.** |
| \(\Gamma_{n,\tau,\eta}^{\lambda}(\mathcal Q)\), \(\widetilde\Gamma_{n,\tau,\eta}^{\lambda}(\mathcal Q)\) | Rejection/slack correction quantities | **HIGH-PRIORITY REVIEW.** These are difficult to parse and may belong in an appendix or may be expressible directly without naming both quantities. |

### Terminology

Preferred:

- “calibrated threshold test”;
- “restricted optimum over threshold tests based on \(L_{n,\lambda}\)”.

Avoid:

- “direct calibration of the projected log--likelihood ratio”;
- “finite blocklength calibration of the projected log--likelihood ratio” as a theorem title;
- “analytical, threshold, and projection losses” unless the paper actually defines and uses these as formal quantities.

---

# 7. Exact reduction / robust-testing terminology

This part should use standard robust-testing language whenever possible.

| Current phrase | Proposed action |
|---|---|
| “exact closure” | **REMOVE.** Use “exact reduction”. |
| “projected ordering” | **RENAME.** Say “stochastic ordering of the selected log-likelihood ratio” or simply state the stochastic-order assumptions. |
| “composite ordered at \((P_\lambda^\star,Q_\lambda^\star)\)” | **REMOVE as bespoke terminology** unless it is used in several subsequent theorems. The two stochastic inequalities are clearer than a new adjective. |
| “selected pair attains the worst case errors” | **KEEP concept**, phrase plainly. |
| “least favourable pair” | **KEEP.** This is standard robust-testing terminology, but reserve it for actual operational least favourability, not Rényi minimisation alone. |
| “NP optimal” | **KEEP.** Standard. Define Neyman--Pearson once, then use NP. |

---

# 8. One-parameter family notation

The natural exponential-family section uses standard notation and is comparatively clean.

| Current notation | Meaning | Proposed action |
|---|---|---|
| \(p_\theta\) | Density in natural exponential family | **KEEP.** |
| \(T(x)\) | Sufficient statistic | **KEEP.** |
| \(\psi(\theta)\) | Log-partition function | **KEEP.** |
| \(h_0(x)\) | Base density factor | **KEEP.** |
| \(\theta_-^{\mathcal P},\theta_+^{\mathcal P},\theta_-^{\mathcal Q},\theta_+^{\mathcal Q}\) | Parameter interval endpoints | **KEEP**, though consider shorter endpoint notation inside that subsection. |
| \(P_{\rm e},Q_{\rm e}\) | Adjacent endpoint pair | **RENAME/REVIEW.** `e` is not self-explanatory. Prefer \(P_+,Q_-\) or write the actual endpoint parameters if not overly long. |

Preferred section language: **“Separated monotone-likelihood-ratio families”** or **“Exact reduction for ordered one-parameter families”.**

---

# 9. Affine-family example notation

The affine-family corollary is notation-heavy but mostly local.

| Current notation | Proposed action |
|---|---|
| \(P_s=p_0+sa\), \(Q_t=q_0+tb\) | **KEEP local.** |
| \(R^\star\) and \(R_{\lambda,s,t}\) | **STANDARDISE with the global tilted-law convention.** |
| \((s^\star,t^\star,\lambda^\star)\) | **KEEP.** |

The main question during theorem-by-theorem review should be whether this corollary belongs in the main text at all or should be moved to an example/appendix.

---

# 10. Terms that should probably disappear

The following phrases currently increase cognitive load without adding precision. Default action is **remove or replace**, subject to theorem-by-theorem review.

- directed composite Rényi separation;
- directed composite Kullback--Leibler separation;
- joint Rényi projection (except when geometry itself is under discussion);
- dominated projection;
- projected reverse Rényi construction;
- projected score ordering;
- exact closure;
- finite blocklength hierarchy;
- analytical relaxation / threshold loss / projection loss as branded categories;
- complete feasible one-sided derivative;
- uniform Rényi achievability;
- projected minimum values;
- directly admissible slack-rejection bound;
- composite ordered;
- endpoint reduction (unless the endpoint structure is the actual theorem content).

---

# 11. Terms that are standard and should generally stay

- composite hypothesis testing;
- minimax;
- Type I / Type II error;
- Neyman--Pearson / NP;
- Rényi divergence;
- KL divergence;
- Hellinger integral;
- likelihood ratio / log-likelihood ratio;
- weak compactness;
- domination / absolute continuity;
- full support;
- strong converse;
- Hoeffding exponent;
- saddle point;
- least favourable distribution/pair;
- stochastic order;
- monotone likelihood ratio;
- natural exponential family;
- tilted law.

---

# 12. Theorem-title policy

The current manuscript overnames results. The default publication style should be:

```latex
\begin{theorem}
...
\end{theorem}
```

with a preceding sentence explaining its purpose.

A descriptive theorem title should be retained only when it is genuinely useful for navigation or refers to a standard named result.

## Current titles flagged for removal or simplification

| Current title | Default recommendation |
|---|---|
| Uniform Rényi achievability bound | Remove title. Precede by “The next result turns two uniform moment bounds into a composite threshold test.” |
| Complete feasible one-sided derivative | Rename “One-sided derivative lemma” or remove title entirely. |
| Uniform Rényi bounds from a dominated projection | Remove title. Describe in text as the uniform moment bounds for a Rényi-minimising pair. |
| Convergence of projected minimum values | Remove title. The statement itself is clear. |
| Directed KL critical rate | Remove title; call \(D(\mathcal Q\|\mathcal P)\) the critical rate in the surrounding prose. |
| Rényi--Hoeffding saddle point and exact Type II error exponent | Simplify strongly; likely just an untitled main theorem in the exponent section. |
| Exact subcritical Type II error exponent for simple binary testing | Probably unnecessary as a standalone corollary if it is only the singleton special case. Review placement. |
| Saddle point conditions for affine classes | Simplify or move out of the main theorem sequence. |
| Finite blocklength calibration of the projected log--likelihood ratio | Remove title; use “Calibration within the selected likelihood-ratio family” in prose. |
| Projected bound with slack and rejection corrections | High-priority rewrite; title currently obscures the result. |
| Fixed level composite Chernoff--Stein exponent | Simplify to “Fixed Type I level” in section prose; theorem can be untitled. |
| Worst case errors under projected ordering | Rename/restate as a theorem under stochastic-order assumptions, without “projected ordering”. |
| Exact reduction for the projected pair | “Exact reduction to the selected pair” if a title is retained. |

---

# 13. High-priority notation inconsistencies to fix before line editing

1. **Law classes versus density classes:** \(\mathcal P,\mathcal Q\) versus \(\mathscr P,\mathscr Q\).
2. **Three notations for the same class minimum:** \(D_\lambda(\mathcal Q\|\mathcal P)\), \(d_\lambda\), and \(D_\lambda^\star\).
3. **Generic score versus selected score:** \(h\), \(h_\lambda^\star\), \(S_n\), \(S_{n,\lambda}^\star\). Adopt an intuitive likelihood-ratio notation.
4. **Threshold notation:** generic \(\tau\), \(\tau_{\lambda,r}^{\min}\), \(\tau_{n,\lambda}^{\rm cal}\). Standardise once the score notation is chosen.
5. **Tilted laws:** \(R_s\), \(R_\rho\), \(R_r^\star\), \(R_{\lambda,s,t}\). Use one indexing convention wherever possible.
6. **Simple binary notation:** repeated use of the `sp` subscript should be reconsidered.
7. **Critical rate notation:** \(r_{\rm crit}\), \(D(\mathcal Q\|\mathcal P)\), and later reversed \(D(\mathcal P\|\mathcal Q)\). Keep the two orientations visibly distinct and avoid unnecessary aliases.
8. **Calibration corrections:** \(\Gamma\) and \(\widetilde\Gamma\) are not readable enough for a main-text refinement unless they are indispensable.

---

# 14. Proposed global vocabulary

The following vocabulary is the default for the publication pass.

### Testing problem

- null class \(\mathcal P\);
- alternative class \(\mathcal Q\);
- worst-case Type I error;
- worst-case Type II error;
- minimax Type II error;
- exponential Type I constraint at rate \(r\);
- fixed Type I level \(\varepsilon\).

### Rényi construction

- minimum Rényi divergence from \(\mathcal Q\) to \(\mathcal P\);
- Rényi-minimising pair \((P_\lambda^\star,Q_\lambda^\star)\);
- log-likelihood ratio of the selected pair;
- uniform exponential-moment bounds;
- threshold test.

### Asymptotics

- critical rate;
- subcritical regime;
- supercritical regime;
- exact Type II error exponent;
- Hoeffding objective;
- saddle point;
- polynomial prefactor/order.

### Exact finite-blocklength reduction

- stochastic ordering of the selected score;
- worst-case pair;
- Neyman--Pearson optimality;
- exact reduction to a simple pair;
- least favourable pair only when the full minimax property is actually proved.

---

# 15. Decisions to make before editing Theorem 1

These are the only global choices that should be settled before theorem-by-theorem revision:

1. **Density-class notation:** replace \(\mathscr P,\mathscr Q\) with a visibly different local notation.
2. **Selected log-likelihood ratio:** choose between \(L_\lambda\) and \(\ell_\lambda\); recommendation: **\(L_\lambda\)** for visual clarity.
3. **Class-minimum shorthand:** recommendation: use \(D_\lambda(\mathcal Q\|\mathcal P)\) globally and local shorthand only inside proofs.
4. **Simple binary optimum:** decide whether the arguments \(P,Q\) are sufficient to distinguish it, allowing removal of the `sp` subscript.
5. **Theorem names:** default to untitled theorem environments.

Once these five choices are fixed, the paper can be revised theorem by theorem without repeatedly changing notation downstream.

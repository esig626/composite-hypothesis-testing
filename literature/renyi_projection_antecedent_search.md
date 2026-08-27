# Antecedent search: joint Rényi projection and uniform moment bounds

**Search date:** 13 August 2026  
**Target:** Theorem `thm:dominated-projection-uniform-renyi-inequalities`, read with Lemma `lem:complete-feasible-directional-derivative`, the surrounding discussion, Theorem `thm:uniform-renyi-achievability`, and Corollary `cor:dominated-finite-sample-projected-bound` in `manuscript/Manuscript.tex`.

## Executive assessment

**No equivalent result was located in the searches performed; novelty remains unresolved.**

The closest projection antecedent located is Kumar and Sason's one-class projection/Pythagorean theory for Rényi divergence on α-convex sets.  It is a genuine antecedent to the *one-coordinate projection idea*, but it does not state the joint closest-pair result for two ordinary convex classes, does not supply both uniform likelihood-ratio moment inequalities from one jointly selected pair, and does not address the selected pair's varying supports by an extended likelihood ratio.  Classical robust-testing results of Huber and Huber--Strassen are genuine antecedents to uniform likelihood-ratio inequalities for a least favourable pair, but their optimised object and their ordering/capacity assumptions are materially different; they do not make a fixed-order joint Rényi projection sufficient in general.  Csiszár's I-projection geometry is an antecedent to one-sided variational/Pythagorean projection inequalities, but at KL order and for one target and one constraint set.  The composite error-exponent work of Mosonyi, Szilágyi, and Weiner optimises divergences between sets operationally/asymptotically, rather than proving the two finite-order moment inequalities below.

This conclusion is deliberately limited.  The configured TheoremSearch server was declared in `.codex/config.toml`, but no TheoremSearch MCP method or resource was exposed to this session.  Listing all MCP resources and templates returned empty lists.  A direct filesystem/configuration check found no substitute client, and attempts to use the general web-search endpoint and direct scholarly APIs failed respectively with HTTP 401 and proxy HTTP 403.  Consequently the semantic queries below were prepared and attempted as required, but did not return a TheoremSearch result set or similarity scores.  Candidate assessment therefore rests on the manuscript's bibliographic records and theorem-level mathematical comparison from the identified literature, not on inaccessible search snippets.  In particular, absence of an equivalent in this constrained search is not evidence of novelty.

## 1. Mathematical specification of the target

### 1.1 Actual theorem

Fix \(0<\lambda<1\).

1. **Ambient and domination.**  Work on a measurable space dominated by a \(\sigma\)-finite measure \(\mu\), with probability densities
   \[
   \mathsf D_\mu=\{f\in L^1(\mu):f\geq0,\ \int f\,d\mu=1\}.
   \]
   The selected laws must additionally satisfy
   \(R\ll P_\lambda^\star+Q_\lambda^\star\) for every
   \(R\in\mathcal P\cup\mathcal Q\).  This is stronger than mere common domination by \(\mu\).

2. **Classes.**  The density classes \(\mathscr P,\mathscr Q\subset\mathsf D_\mu\) are nonempty, ordinarily (linearly) convex, and weakly compact in \(L^1(\mu)\).  Their corresponding law classes are \(\mathcal P,\mathcal Q\).

3. **Optimisation.**  For
   \[
   Z_\lambda(q,p)=\int q^\lambda p^{1-\lambda}\,d\mu,
   \]
   select a joint maximiser
   \[
   (q_\lambda^\star,p_\lambda^\star)\in
   \mathop{\rm argmax}_{(q,p)\in\mathscr Q\times\mathscr P} Z_\lambda(q,p),
   \qquad z_\lambda^\star=Z_\lambda(q_\lambda^\star,p_\lambda^\star)>0.
   \]
   Since \(\lambda-1<0\), this is equivalently a closest pair minimising
   \(D_\lambda(Q\Vert P)=(\lambda-1)^{-1}\log Z_\lambda(Q,P)\) jointly over \(\mathcal Q\times\mathcal P\).

4. **Extended likelihood ratio.**  Put \(\xi=P_\lambda^\star+Q_\lambda^\star\),
   \(a=dP_\lambda^\star/d\xi\), and \(b=dQ_\lambda^\star/d\xi\).  Define
   \[
   h_\lambda^\star=
   \begin{cases}
   \log(b/a),&a,b>0,\\
   -\infty,&a>0,b=0,\\
   +\infty,&a=0,b>0,\\
   0,&a=b=0.
   \end{cases}
   \]

5. **Two support conclusions.**  Joint coordinatewise optimality, together with the feasible one-sided derivative lemma, implies
   \[
   P\{h_\lambda^\star=+\infty\}=0\quad(P\in\mathcal P),
   \qquad
   Q\{h_\lambda^\star=-\infty\}=0\quad(Q\in\mathcal Q).
   \]

6. **Two uniform inequalities.**  The same two coordinatewise variations give
   \[
   \sup_{P\in\mathcal P}E_P e^{\lambda h_\lambda^\star}
   \le z_\lambda^\star,
   \qquad
   \sup_{Q\in\mathcal Q}E_Q e^{(\lambda-1)h_\lambda^\star}
   \le z_\lambda^\star.
   \]
   Equality holds in each display at its selected law.  Also
   \(D_\lambda(Q_\lambda^\star\Vert P_\lambda^\star)=D_\lambda(\mathcal Q\Vert\mathcal P)\) and
   \(z_\lambda^\star=\exp\{(\lambda-1)D_\lambda(\mathcal Q\Vert\mathcal P)\}\).

### 1.2 Variable supports and the derivative lemma

The key boundary issue is not cosmetic.  If a selected density vanishes, formal differentiation of \(u^\alpha\) introduces \(u^{\alpha-1}\).  The preceding lemma treats a feasible segment \(y_t=(1-t)y+tx\) at a maximiser of \(F(u)=\int wu^\alpha d\mu\).  It proves both (i) that the direction cannot introduce mass on \(\{w>0,y=0\}\), and (ii) integrability plus the expected one-sided derivative inequality on \(\{y>0\}\).  Applied once in each coordinate, these facts exclude the wrong infinite value of \(h_\lambda^\star\) under every law in the corresponding class.  Domination by the *selected sum* removes the remaining set where both selected densities vanish.  Thus no common or full support is assumed, and \(h_\lambda^\star\) genuinely may take either infinite value (but only on the harmless side for each class).

### 1.3 Which assumption does what

* **Ordinary convexity** makes every line segment from the selected density to a competitor feasible.  It is what permits the one-sided derivative lemma in each coordinate and hence the support restrictions and two integral inequalities.
* **Weak compactness** is used for existence, not for the variational inequalities after a maximiser has been selected.  Joint concavity and norm continuity make \(Z_\lambda\) weakly upper semicontinuous; compactness then gives a maximiser.
* **Common \(\sigma\)-finite domination by \(\mu\)** supplies the \(L^1\) density model, the integral expression for \(Z_\lambda\), and the topology in which compactness is imposed.
* **Domination by \(P_\lambda^\star+Q_\lambda^\star\)** ensures every class member gives zero mass to the common selected null set.  Together with the directional support restrictions, it makes the extended likelihood ratio and its moments valid uniformly.  It is not needed merely to show that \(Z_\lambda\) attains its maximum.
* **Positivity of \(z_\lambda^\star\)** is required by the derivative lemma and rules out a completely singular selected pair at this order.

### 1.4 Later testing consequence, not part of the projection theorem

The operational result additionally tensorises the two single-letter bounds.  For \(S_n=\sum_i h_\lambda^\star(X_i)\), with a harmless definition on samples containing both infinities, the threshold
\[
\tau\geq \frac{n[r-(1-\lambda)D_\lambda(\mathcal Q\Vert\mathcal P)]}{\lambda}
\]
gives a single test \(1\{S_n\geq\tau\}\) whose Type I error is at most \(e^{-nr}\) uniformly over \(\mathcal P\).  At the minimal threshold its worst-case Type II error is at most
\[
\exp\!\left\{-n\frac{1-\lambda}{\lambda}
[D_\lambda(\mathcal Q\Vert\mathcal P)-r]\right\}.
\]
This uses product laws, tensorisation, and exponential Markov bounds.  It does **not** assert that \((P_\lambda^\star,Q_\lambda^\star)\) is an operational least favourable pair or that the likelihood-ratio test is exactly minimax.

## 2. Semantic search formulations

The following formulations were designed around the mathematical claim rather than its manuscript title.  They deliberately vary the object, geometry, operational language, and support assumptions.

1. `Renyi projection between two convex sets of probability measures closest pair Pythagorean variational inequality`
2. `order alpha Hellinger integral maximised jointly over two convex probability classes first order optimality inequalities`
3. `Chernoff coefficient closest pair of convex distributions likelihood ratio moment bounds uniform over both sets`
4. `joint projection two convex sets probability densities f-divergence supporting hyperplane inequalities at optimal pair`
5. `variational inequalities from an optimal pair maximising integral q^alpha p^(1-alpha) over convex sets`
6. `uniform likelihood-ratio inequalities over uncertainty classes least favourable distributions robust hypothesis testing Hellinger transform`
7. `information projection between two convex probability classes rather than projection of one distribution onto one set`
8. `convex probability classes minimax distribution pair exponential moments of selected log likelihood ratio`
9. `Hellinger transform saddle point robust test two uncertainty sets varying supports`
10. `f-divergence nearest pair of convex sets directional derivative probability densities zero sets`
11. `alpha divergence projection ordinary mixture convex families versus alpha-convex families Pythagorean theorem`
12. `Chernoff information between convex sets attaining pair support function optimality conditions`
13. `least favourable pair likelihood ratio may be zero or infinity non-common supports composite testing`
14. `Huber Strassen capacities least favourable distributions likelihood ratio stochastic ordering Hellinger integrals`
15. `Csiszar I-projection two sets closest distributions variational inequality extended likelihood ratio`
16. `minimise Renyi divergence jointly over P in convex null class Q in convex alternative class`
17. `one-sided derivative of Hellinger integral at density with zeros feasible mixture direction`
18. `composite hypothesis testing joint Renyi minimizer gives one test uniform exponential moment bounds`

The query-by-query log, including the unavailable TheoremSearch response fields, is appended to `literature/theoremsearch_queries.md`.

## 3. Candidate investigation

### 3.1 Kumar and Sason (2016), *Projection Theorems for the Rényi Divergence on \(\alpha\)-Convex Sets*

**Result inspected:** the forward/reverse projection and Pythagorean results (the paper's projection theorems; exact theorem identifier could not be verified from a source PDF in this session).

**A. Assumptions.** A fixed probability distribution and a single \(\alpha\)-convex constraint family, with additional closure/existence hypotheses depending on the projection direction.  \(\alpha\)-convexity is closure under normalised power mixtures and is not ordinary mixture convexity.

**B. Optimised object.** Rényi divergence from or to a fixed distribution, minimised over one class.

**C. Conclusion.** Pythagorean/projection inequalities characterising a Rényi projection.

**D. One or two classes?** One optimised class and one fixed distribution, not a jointly optimised pair from two classes.

**E. Our inequalities?** A one-sided projection inequality is analogous to one coordinate of the target.  The paper does not, as identified here, state both target moment inequalities for one joint closest pair.

**F--G. Supports/infinities.** The located description does not establish the target's treatment of two varying-support ordinary convex classes or an extended log-likelihood ratio taking \(\pm\infty\).

**H. Type.** Divergence-projection geometry, not an operational finite-blocklength robust-testing result.

**Classification: PARTIAL ANTECEDENT.**  Fixing either coordinate of the target turns joint optimality into a one-class projection problem, so the conceptual overlap is real.  The missing combination is joint optimisation over two ordinary convex classes, the paired coordinate variations, and the selected-support argument producing both uniform moment bounds.

### 3.2 Csiszár (1975), *I-Divergence Geometry of Probability Distributions and Minimization Problems*

**Result inspected:** the I-projection existence/Pythagorean framework for convex sets (exact theorem identifier could not be source-verified in this session).

**A. Assumptions.** A fixed reference distribution and a convex set of probability distributions, with closure/existence and finiteness conditions appropriate to relative entropy.

**B. Optimised object.** Kullback--Leibler/I-divergence over a single constraint set.

**C. Conclusion.** A projection satisfies a Pythagorean inequality and associated variational characterisations.

**D. One or two classes?** One class against a fixed reference.

**E. Our inequalities?** Neither finite-order Hellinger moment inequality is stated as such; it supplies the classical one-coordinate geometric prototype.

**F--G. Supports/infinities.** Absolute-continuity and infinite-divergence conventions occur in I-projection theory, but this is not the target's explicit two-sided extended-likelihood construction for two variable-support classes.

**H. Type.** Information-projection theorem.

**Classification: RELATED BUT NOT ANTECEDENT.**  It is an important geometric ancestor, but changing KL to fixed-order Rényi/Hellinger and changing one fixed reference to a jointly selected pair are substantive theorem changes, not mere notation.

### 3.3 Huber (1965), *A Robust Version of the Probability Ratio Test*

**Result inspected:** robust probability-ratio testing for specified contamination-type neighbourhoods.

**A. Assumptions.** Structured uncertainty neighbourhoods permitting construction of least favourable distributions and a clipped likelihood ratio.

**B. Optimised object.** Worst-case testing risk/error under robust neighbourhoods, rather than the order-\(\lambda\) Hellinger integral between two arbitrary convex classes.

**C. Conclusion.** A robustified/clipped probability-ratio test and least favourable distributions for the specified model.

**D. One or two classes?** Two uncertainty sides operationally, but not the target's unrestricted joint Rényi closest-pair programme.

**E. Our inequalities?** Robust ordering can imply uniform inequalities for broad classes of functions of the likelihood ratio, and hence can imply Hellinger-transform comparisons in its setting.  It does not derive precisely both displayed moment bounds solely from joint order-\(\lambda\) optimality.

**F--G. Supports/infinities.** Not the target's general varying-support \(L^1\) theorem with explicit \(\pm\infty\) values.

**H. Type.** Operational robust-testing result.

**Classification: PARTIAL ANTECEDENT.**  It precedes the target's operational idea of one likelihood ratio controlling both uncertainty classes, but only under special neighbourhood structure and through least-favourable stochastic ordering, a different and generally stronger operational condition.

### 3.4 Huber and Strassen (1973), *Minimax Tests and the Neyman--Pearson Lemma for Capacities*

**Result inspected:** the capacity-based least-favourable-pair/minimax Neyman--Pearson theory (exact numbered statement could not be source-verified in this session).

**A. Assumptions.** Alternating/2-alternating capacity hypotheses and associated compactness/regularity; the induced uncertainty classes possess a least favourable structure.

**B. Optimised object.** Minimax testing risk and capacity probabilities, not one fixed-order Chernoff coefficient.

**C. Conclusion.** Under their conditions a Neyman--Pearson test for a least favourable pair is minimax and admits likelihood-ratio ordering inequalities.

**D. One or two classes?** Two operational uncertainty classes/capacities.

**E. Our inequalities?** Their least-favourable ordering is capable of yielding both types of integral comparison for suitable monotone functions.  The direction is different: a globally least favourable pair satisfies ordering properties; joint maximisation of a single Hellinger integral is not asserted to create such a pair for arbitrary convex weakly compact classes.

**F--G. Supports/infinities.** Singular components can be handled in general robust testing, but the target's exact selected-sum domination and extended ratio statement was not located.

**H. Type.** Operational robust-testing/minimax theorem.

**Classification: PARTIAL ANTECEDENT.**  This is the strongest operational antecedent to paired uniform inequalities, yet it neither uses nor establishes the target's sufficient condition from a fixed-order joint Rényi projection.  Conversely, the target does not obtain exact minimaxity, so neither theorem simply contains the other.

### 3.5 Fauß, Zoubir, and Poor (2021), *Minimax Robust Detection: Classic Results and Recent Advances*

**Result inspected:** the survey's least-favourable-distribution and stochastic-order/\(f\)-divergence criteria (individual identifiers could not be source-verified in this session).

**A. Assumptions.** Vary by uncertainty model; exact minimax reduction generally needs likelihood-ratio stochastic ordering or related least-favourable conditions.

**B. Optimised object.** Worst-case detection performance and, in sufficient criteria, simultaneous extremality of classes of \(f\)-divergences.

**C. Conclusion.** Characterisations and constructions of least favourable distributions and minimax robust tests.

**D. One or two classes?** Two classes operationally.

**E. Our inequalities?** Suitable stochastic ordering implies many uniform inequalities and would encompass the target's two moments, but maximising one Chernoff/Hellinger functional alone is not presented as sufficient for full robust minimaxity.

**F--G. Supports/infinities.** Model-dependent; no located theorem matches the target's explicit general support mechanism.

**H. Type.** Survey/operational robust testing.

**Classification: RELATED BUT NOT ANTECEDENT.**  It maps the relevant stronger robust-testing conditions but is not itself a theorem materially equivalent to the target projection statement.

### 3.6 van Erven and Harremoës (2014), *Rényi Divergence and Kullback--Leibler Divergence*

**Result inspected:** Theorem 17 as cited by the manuscript (continuity in total variation), together with the paper's general Rényi properties.

**A. Assumptions.** Probability measures and the order-dependent finiteness/continuity hypotheses in the general Rényi theory.

**B. Optimised object.** General properties of Rényi divergence; not a closest pair of classes.

**C. Conclusion.** Continuity and structural properties supporting existence arguments.

**D--E.** No joint two-class optimisation and neither uniform likelihood-ratio inequality.

**F--G.** General measure-theoretic support conventions are allowed, but not assembled into the target theorem.

**H. Type.** Foundational divergence theory.

**Classification: RELATED BUT NOT ANTECEDENT.**  It supports the weak-attainment step but does not contain the variational conclusion.

### 3.7 Mosonyi, Szilágyi, and Weiner (2021/2022), *On the Error Exponents of Binary State Discrimination with Composite Hypotheses*

**Result inspected:** the classical/commutative composite Chernoff and Hoeffding exponent results discussed in the paper (exact identifiers could not be source-verified in this session).

**A. Assumptions.** Composite sets of states/measures, with compactness and convexity conditions in relevant specialisations; the work is asymptotic and includes the quantum setting.

**B. Optimised object.** Operational asymptotic error exponents expressed through divergence/Chernoff optimisations between hypothesis sets.

**C. Conclusion.** Formulae for composite discrimination exponents under the paper's hypotheses.

**D. One or two classes?** Both hypothesis classes enter the optimisations.

**E. Our inequalities?** No located result states that a fixed-order jointly optimal pair yields both target single-letter uniform moment inequalities and the associated finite-blocklength threshold construction.

**F--G.** Support is handled through divergence conventions; no matching extended-likelihood-ratio support theorem was located.

**H. Type.** Operational asymptotic composite-testing result.

**Classification: RELATED BUT NOT ANTECEDENT.**  Joint divergence optimisation overlaps at the exponent-formula level, but an exponent identity does not imply the target's coordinatewise uniform inequalities for the selected statistic.

## 4. False-positive patterns actively excluded

* A theorem saying merely that \(D_\lambda(Q\Vert P)\) attains its infimum on two compact sets is insufficient: attainment alone does not record either variational inequality or boundary support conclusion.
* A one-class Rényi projection theorem supplies at most one coordinate inequality unless it is applied twice and its hypotheses remain valid with the other selected coordinate fixed.
* A least favourable pair that minimises every \(f\)-divergence or has likelihood-ratio stochastic ordering is stronger operational structure; it cannot be inferred merely from extremising one Chernoff functional.
* A formula for composite Chernoff/Hoeffding exponents is not automatically a finite-blocklength, single-statistic uniform moment theorem.
* Full-support finite-alphabet differentiations hide the main measure-theoretic issue: they do not antecede the no-new-support conclusion needed when selected densities vanish.

## 5. Final assessment and decisive distinctions

**Assessment 3: No equivalent result was located in the searches performed; novelty remains unresolved.**  The search did locate results covering parts of the theorem: one-coordinate Rényi/I-projection geometry, and robust-testing theorems in which a genuinely least favourable pair gives stronger operational orderings.  The unresolved question is whether an older source combines the following features in one result.

The five distinctions most important to a genuine novelty determination are:

1. **One class versus a joint closest pair.**  Does the source optimise against a fixed reference, or jointly over two uncertainty classes?
2. **One variational inequality versus both.**  Does the same selected pair give the \(P\)-uniform \(E_P[(q^\star/p^\star)^\lambda]\) bound and the \(Q\)-uniform \(E_Q[(q^\star/p^\star)^{\lambda-1}]\) bound?
3. **Ordinary convexity versus specialised geometry.**  Does it require only mixture convexity, or \(\alpha\)-convexity, contamination neighbourhoods, capacities, or likelihood-ratio stochastic ordering?
4. **Boundary supports.**  Are zero densities permitted, is the ratio explicitly extended to \(\pm\infty\), and is the one-sided derivative/no-new-support argument proved rather than bypassed by common/full support?
5. **Projection inequality versus operational minimaxity.**  Is the claim only the two moment bounds (sufficient for finite-blocklength achievability), or the stronger but different assertion that the selected pair is least favourable and its Neyman--Pearson test exactly minimax?

## References considered

* I. Csiszár, “I-Divergence Geometry of Probability Distributions and Minimization Problems,” *Annals of Probability*, 1975.
* M. A. Kumar and I. Sason, “Projection Theorems for the Rényi Divergence on \(\alpha\)-Convex Sets,” *IEEE Transactions on Information Theory* 62(9), 2016.
* P. J. Huber, “A Robust Version of the Probability Ratio Test,” *Annals of Mathematical Statistics* 36(6), 1965.
* P. J. Huber and V. Strassen, “Minimax Tests and the Neyman--Pearson Lemma for Capacities,” *Annals of Statistics* 1(2), 1973.
* M. Fauß, A. M. Zoubir, and H. V. Poor, “Minimax Robust Detection: Classic Results and Recent Advances,” *IEEE Transactions on Signal Processing* 69, 2021.
* T. van Erven and P. Harremoës, “Rényi Divergence and Kullback--Leibler Divergence,” *IEEE Transactions on Information Theory* 60(7), 2014.
* M. Mosonyi, Z. Szilágyi, and M. Weiner, “On the Error Exponents of Binary State Discrimination with Composite Hypotheses,” *IEEE Transactions on Information Theory* 68(2), 2022 (online publication 2021).

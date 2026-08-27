# S1 direct attainment proof audit

## Status

S1 is proved with a necessary qualification.

Direct attainment can replace weak compactness in the projection theorem. This gives a genuinely more general sufficient condition because attainment can hold for classes that are not weakly compact.

The proposed support replacement is not weaker in the present dominated setting. For every class law already dominated by \(\mu\), the condition that the law gives zero mass to the joint zero set of the selected densities is equivalent to absolute continuity with respect to the sum of the selected laws.

No manuscript claim follows from this audit alone.

## Corrected statement

Fix \(0<\lambda<1\). Let \(\mathcal P\) and \(\mathcal Q\) be nonempty convex classes of probability laws dominated by a sigma finite measure \(\mu\). Write \(p\) and \(q\) for their densities.

Assume that there are \(P_\lambda^\star\in\mathcal P\) and \(Q_\lambda^\star\in\mathcal Q\), with densities \(p_\lambda^\star\) and \(q_\lambda^\star\), such that

\[
z_\lambda
:=
Z_\lambda(Q_\lambda^\star,P_\lambda^\star)
=
\max_{Q\in\mathcal Q,\,P\in\mathcal P}
Z_\lambda(Q,P)
>0.
\]

Define

\[
N_\lambda
:=
\{p_\lambda^\star=0,\ q_\lambda^\star=0\}
\]

and assume

\[
R(N_\lambda)=0
\qquad
\text{for every }R\in\mathcal P\cup\mathcal Q.
\]

Let \(\xi=P_\lambda^\star+Q_\lambda^\star\), choose

\[
a=\frac{dP_\lambda^\star}{d\xi},
\qquad
b=\frac{dQ_\lambda^\star}{d\xi},
\]

and define the extended log likelihood ratio

\[
\ell_\lambda
=
\begin{cases}
\log(b/a),&a>0,\ b>0,\\
-\infty,&a>0,\ b=0,\\
+\infty,&a=0,\ b>0,\\
0,&a=b=0.
\end{cases}
\]

Then

\[
P\{\ell_\lambda=+\infty\}=0
\qquad
\text{for every }P\in\mathcal P,
\]

\[
Q\{\ell_\lambda=-\infty\}=0
\qquad
\text{for every }Q\in\mathcal Q,
\]

and

\[
\mathbb E_P e^{\lambda\ell_\lambda}
\le z_\lambda
\qquad
\text{for every }P\in\mathcal P,
\]

\[
\mathbb E_Q e^{(\lambda-1)\ell_\lambda}
\le z_\lambda
\qquad
\text{for every }Q\in\mathcal Q.
\]

Equality holds in the first moment inequality at \(P_\lambda^\star\) and in the second at \(Q_\lambda^\star\). Moreover,

\[
D_\lambda(Q_\lambda^\star\|P_\lambda^\star)
=D_\lambda(\mathcal Q\|\mathcal P)
\]

and

\[
z_\lambda
=
\exp\!\left\{(\lambda-1)
D_\lambda(Q_\lambda^\star\|P_\lambda^\star)\right\}.
\]

## Proof

Put

\[
\begin{aligned}
C_\lambda&:=\{p_\lambda^\star>0,\ q_\lambda^\star>0\},\\
A_\lambda&:=\{p_\lambda^\star>0,\ q_\lambda^\star=0\},\\
B_\lambda&:=\{p_\lambda^\star=0,\ q_\lambda^\star>0\},\\
N_\lambda&:=\{p_\lambda^\star=0,\ q_\lambda^\star=0\}.
\end{aligned}
\]

Fix \(Q\in\mathcal Q\), with density \(q\). Convexity makes

\[
q_t=(1-t)q_\lambda^\star+tq
\]

feasible for every \(0\le t\le1\). Direct joint optimality gives

\[
Z_\lambda(q_t,p_\lambda^\star)\le z_\lambda.
\]

Apply the existing complete feasible one sided derivative lemma with

\[
\alpha=\lambda,
\qquad
w=(p_\lambda^\star)^{1-\lambda},
\qquad
y=q_\lambda^\star,
\qquad
x=q.
\]

Every input to the lemma is available. The densities are measurable and finite almost everywhere, convexity makes the segment feasible, and

\[
0<F(y)=z_\lambda\le1
\]

by the positivity assumption and Holder's inequality. The lemma therefore gives

\[
Q(A_\lambda)=0
\]

and

\[
\int_{C_\lambda}
q(q_\lambda^\star)^{\lambda-1}
(p_\lambda^\star)^{1-\lambda}\,d\mu
\le z_\lambda.
\tag{1}
\]

Fix \(P\in\mathcal P\), with density \(p\). Apply the same lemma to

\[
p_t=(1-t)p_\lambda^\star+tp
\]

with

\[
\alpha=1-\lambda,
\qquad
w=(q_\lambda^\star)^\lambda,
\qquad
y=p_\lambda^\star,
\qquad
x=p.
\]

It gives

\[
P(B_\lambda)=0
\]

and

\[
\int_{C_\lambda}
p(q_\lambda^\star)^\lambda
(p_\lambda^\star)^{-\lambda}\,d\mu
\le z_\lambda.
\tag{2}
\]

The extended ratio equals \(+\infty\) on \(B_\lambda\) and \(-\infty\) on \(A_\lambda\). The two support conclusions follow immediately from the preceding null statements. They do not use the assumption on \(N_\lambda\).

The exact moment decompositions are

\[
\mathbb E_P e^{\lambda\ell_\lambda}
=
\int_{C_\lambda}
p(q_\lambda^\star)^\lambda
(p_\lambda^\star)^{-\lambda}\,d\mu
+P(N_\lambda)
\]

and

\[
\mathbb E_Q e^{(\lambda-1)\ell_\lambda}
=
\int_{C_\lambda}
q(q_\lambda^\star)^{\lambda-1}
(p_\lambda^\star)^{1-\lambda}\,d\mu
+Q(N_\lambda).
\]

For the first identity, the exponential is zero on \(A_\lambda\), infinite only on the \(P\) null set \(B_\lambda\), and one on \(N_\lambda\). The second identity follows symmetrically. The assumed nullity of \(N_\lambda\), followed by (1) and (2), proves the uniform moment inequalities.

Substitution of the selected laws gives equality because their densities vanish on the three cells that do not contribute to the corresponding integral.

Finally, \(D_\lambda=(\lambda-1)^{-1}\log Z_\lambda\), and \((\lambda-1)^{-1}<0\). Maximising \(Z_\lambda\) is therefore equivalent to minimising \(D_\lambda\). This proves the attainment and exponential identities.

## The support premise is equivalent to selected sum domination

Let

\[
S=P_\lambda^\star+Q_\lambda^\star.
\]

Its density with respect to \(\mu\) is \(p_\lambda^\star+q_\lambda^\star\). For any class law \(R\ll\mu\), with density \(r\),

\[
R\ll S
\quad\Longleftrightarrow\quad
r=0\ \mu\text{ almost everywhere on }N_\lambda
\quad\Longleftrightarrow\quad
R(N_\lambda)=0.
\]

The equivalence is invariant under changes of density versions because all class laws are dominated by \(\mu\). Thus the S1 joint zero premise is an exact reformulation of the selected sum domination premise. It is not a weaker support assumption.

## Direct attainment is genuinely weaker than weak compactness

Take the alphabet \(\{1,2\}\), counting measure, and any \(0<\lambda<1\). Let

\[
\mathcal P=\{(1/2,1/2)\}
\]

and

\[
\mathcal Q
=
\{(t,1-t):4/5\le t<1\}.
\]

The alternative class is convex but not closed, hence not weakly compact in this finite dimensional space. Nevertheless,

\[
Z_\lambda((t,1-t),(1/2,1/2))
=
(1/2)^{1-\lambda}
\bigl[t^\lambda+(1-t)^\lambda\bigr]
\]

is strictly decreasing for \(t>1/2\). Its maximum on \(\mathcal Q\) is attained at \(t=4/5\). The selected null density has full support, so \(N_\lambda\) is empty. The corrected S1 theorem applies, while the weak compactness version does not.

## The joint zero premise cannot simply be deleted

Take the alphabet \(\{1,2,3\}\), counting measure, any \(0<\lambda<1\), and any \(0<a<1\). Let

\[
Q^\star=\delta_1,
\qquad
P^\star=a\delta_1+(1-a)\delta_2,
\]

\[
\mathcal Q=\{Q^\star\},
\qquad
\mathcal P=\operatorname{conv}\{P^\star,\delta_3\}.
\]

For \(P_t=(1-t)P^\star+t\delta_3\),

\[
Z_\lambda(Q^\star,P_t)
=
\bigl((1-t)a\bigr)^{1-\lambda}
\le
a^{1-\lambda}.
\]

Thus \((Q^\star,P^\star)\) is a positive joint maximiser. Its joint zero set is \(\{3\}\). With the theorem's convention \(\ell_\lambda=0\) there,

\[
\mathbb E_{\delta_3}e^{\lambda\ell_\lambda}
=1
>
a^{1-\lambda}
=z_\lambda.
\]

The null moment inequality fails. The selected sum support premise is therefore not redundant. This example does not show that the premise is logically necessary in every individual model, but it shows that no general theorem may simply omit it while retaining the same extended ratio convention and conclusion.

## Relation to the literature audit

The proof uses only the existing feasible derivative lemma and elementary measure theory. The retained projection papers concern one optimised class against a fixed law, alpha convex geometry, or relative alpha entropy. They neither supply a missing step nor contradict the corrected result.

This audit establishes internal provability only. It does not establish novelty. The appropriate manuscript description, if later approved, is that direct attainment can replace weak compactness. The support condition should continue to be described as selected sum domination, or as its equivalent joint zero formulation, without claiming that one is weaker or minimal.

## Manuscript decision

Do not modify the manuscript on the basis of the original S1 wording.

If the result is later approved for integration, the clean structure is a theorem conditional on positive direct attainment and selected sum domination, followed by the present weak compactness argument as one sufficient attainment criterion. No new manuscript claim should state that the support hypothesis has been weakened.

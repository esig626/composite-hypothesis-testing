# Frozen glossary amendment 002 — IEEE LaTeX display and equation-numbering rules

This amendment is part of the frozen publication standard for `manuscript/Manuscript.tex`.

## 1. Math delimiters

Use `$...$` for inline mathematics.

Do **not** use `\(...\)` for inline mathematics.

Do **not** use `\[...\]` for displayed mathematics.

For displayed mathematics, use only:

- `\begin{equation} ... \end{equation}` when the display must be numbered;
- `\begin{equation*} ... \end{equation*}` when it must not be numbered.

If a display needs multiple aligned lines, place an `aligned` environment inside `equation` or `equation*` rather than introducing a separate display convention.

Example:

```latex
\begin{equation*}
\begin{aligned}
H_{\mathcal P}&:X^n\sim P^{\otimes n},\quad P\in\mathcal P,\\
H_{\mathcal Q}&:X^n\sim Q^{\otimes n},\quad Q\in\mathcal Q.
\end{aligned}
\end{equation*}
```

## 2. Equation numbering

The default is **not to number a displayed equation**.

Use a numbered `equation` environment only when the equation is referenced elsewhere in the manuscript, normally through `\eqref{...}`.

Do not number an equation merely because it is a definition, an important formula, or a displayed statement.

If a numbered equation is introduced, it must have a `\label{...}` and there must be a genuine downstream reference to that label.

Conversely, if a label is never referenced, remove both the label and the equation number unless a specific IEEE formatting reason requires otherwise.

## 3. Revision audit rule

During each theorem-by-theorem revision:

1. check every displayed equation in the edited passage;
2. verify whether each numbered equation is actually referenced elsewhere;
3. demote unreferenced numbered equations to `equation*`;
4. remove orphaned labels;
5. preserve numbering only for equations that the argument explicitly calls back to.

This audit applies to definitions, bounds, hypothesis displays, intermediate identities, and appendix calculations alike.

## 4. House rule

No new manuscript text produced during the publication rewrite may use `\(`, `\)`, `\[`, or `\]`.

The canonical math presentation is therefore:

- inline: `$...$`;
- unnumbered display: `equation*`;
- numbered display: `equation`;
- multiline display: `aligned` inside `equation` or `equation*`.

# Paper source

This directory contains the source package and compiled PDF corresponding to **arXiv:2608.28068v2**.

- `manuscript.tex` — main LaTeX source
- `my.bib` — bibliography database
- `Figure_1.eps`–`Figure_5.eps` — manuscript figures
- `Manuscript.pdf` — compiled 34-page manuscript

Build from this directory with:

```bash
latexmk -pdf -shell-escape manuscript.tex
```

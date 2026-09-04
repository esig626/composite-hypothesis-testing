# Numerical experiments

This directory contains the computational material retained from the paper's research workflow.

## Structure

- `scripts/` — finite-blocklength solvers, Rényi-bound calculations, certification checks, and plotting utilities.
- `data/` — committed CSV and JSON outputs used for validation and replotting.
- `figures/` — generated numerical figures.
- `*_audit.md` — numerical methodology, diagnostics, and certification records.

The core affine-ternary solver is `scripts/affine_ternary_lp.py`. The main nonordered finite-blocklength experiment is `scripts/nonordered_bruno_regimes.py`; the remaining scripts refine, certify, or replot parts of that calculation.

## Environment

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Several calculations are computationally intensive. The committed data permit inspection and replotting without rerunning every optimisation. The exact manuscript source figures are stored separately in [`../paper/`](../paper/).

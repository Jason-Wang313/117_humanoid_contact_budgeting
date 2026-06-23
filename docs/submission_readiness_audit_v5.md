# Submission Readiness Audit v5

Paper: 117 `humanoid_contact_budgeting`

Date: 2026-06-23

Terminal decision: STRONG_REVISE

ICLR main ready: no

## Evidence Rerun

Command:

```powershell
$env:OMP_NUM_THREADS='1'
$env:OPENBLAS_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
python -m py_compile src\run_experiment.py
python src\run_experiment.py
python scripts\generate_manuscript.py
```

## Integrity Gates

- `dataset_summary.csv`: 240 rows.
- `cell_metrics.csv`: 230,400 rows.
- `main_group_metrics.csv`: 2,880 rows.
- `seed_metrics.csv`: 600 rows.
- `metrics.csv`: 60 rows.
- `hard_seed_metrics.csv`: 120 rows.
- `hard_aggregate_metrics.csv`: 12 rows.
- `hard_pairwise_stats.csv`: 11 rows.
- `ablation_cell_metrics.csv`: 38,400 rows.
- `ablation_seed_metrics.csv`: 100 rows.
- `ablation_metrics.csv`: 10 rows.
- `stress_sweep_cell_metrics.csv`: 161,280 rows.
- `stress_sweep_seed_metrics.csv`: 420 rows.
- `stress_sweep.csv`: 42 rows.
- `fixed_budget_cell_metrics.csv`: 107,520 rows.
- `fixed_budget_seed_metrics.csv`: 280 rows.
- `fixed_budget_metrics.csv`: 28 rows.
- `fixed_budget_pairwise_stats.csv`: 24 rows.
- `failure_cases.csv`: 24 rows.
- Numeric sanity: no NaN or infinite values found.

## Result Gates

- Strongest non-oracle baseline: `proposed_contact_budget_controller_v4_1`.
- Hard success: `0.78640` proposed vs `0.72415` baseline.
- Hard utility: `0.95300` proposed vs `0.76795` baseline.
- Hard success margin: `0.06225`.
- Hard utility margin: `0.18505`.
- Paired hard-utility gain: `0.18505`; wins `10/10`.
- Budget-violation delta: `-0.04428`.
- Fall-rate delta: `-0.03618`.
- Balance-margin delta: `+0.06230`.
- Recovery-success delta: `+0.06366`.
- Reserve-starvation delta: `-0.03959`.
- Contact-overuse delta: `-0.03078`.
- Energy/contact-cost delta: `-0.03028`.
- Calibration-error delta: `-0.01958`.
- Ablation margin: success `0.02342`, utility `0.08176`.
- Stress endpoint margin: success `0.07178`, utility `0.20154`.
- Strict fixed-budget coverage: `0.87266`.
- Strict fixed-budget breach: `0.00000`.
- Strict fixed-budget utility margin: `0.85821`.

## Artifact Gate

- Canonical PDF: `C:/Users/wangz/Downloads/117.pdf`.
- PDF SHA256: `A71C65D2A0E03183855F8CE57166D37237EBD99379A196C3C2939AD6F76BD6DE`.
- PDF size: `849152` bytes.
- PDF pages: `28`.
- Desktop PDF copy: absent.
- Root numbered PDF copy: absent.
- Child numbered PDF copy: absent.
- LaTeX/BibTeX scan: no actionable warnings; BibTeX reports `warning$ -- 0`.
- Visual QA: title/abstract, results table/figures, gate appendix, failure cases, artifact requirements, and references pages inspected.

## Submission Decision

The v5 local evidence clears the frozen empirical gates and is much stronger than v4.1. The paper is still not ICLR-main ready because it has no real humanoid rollouts, no accepted high-fidelity humanoid contact simulation, no released controller/checkpoint artifacts, no calibrated contact-force or camera logs, no hardware rollout videos, and no complete manual related-work synthesis.

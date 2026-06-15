# Submission Readiness Audit v4.1

Paper: 117 `humanoid_contact_budgeting`

Date: 2026-06-15

Terminal decision: STRONG_REVISE

ICLR main ready: no

## Evidence Rerun

Command:

```powershell
$env:OMP_NUM_THREADS='1'
$env:OPENBLAS_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
python -m py_compile src\run_experiment.py
python src\run_experiment.py *> C:\Users\wangz\robotics_massive_pool_paper_factory\logs\117_humanoid_contact_budgeting_continuation_rerun_20260615.log
```

## Integrity Gates

- `metrics.csv`: 45 rows.
- `per_task_regime_metrics.csv`: 1,575 rows.
- `seed_task_regime_metrics.csv`: 11,025 rows.
- `seed_split_metrics.csv`: 315 rows.
- `pairwise_stats.csv`: 8 rows.
- `ablation_metrics.csv`: 7 rows.
- `ablation_seed_metrics.csv`: 49 rows.
- `ablation_task_regime_seed_metrics.csv`: 1,715 rows.
- `stress_sweep.csv`: 24 rows.
- `stress_sweep_seed_metrics.csv`: 5,880 task/regime/seed rows.
- `failure_cases.csv`: 8 rows.
- Numeric sanity: no NaN or infinite values found.

## Result Gates

- Strongest non-oracle baseline: `risk_aware_contact_planner`.
- Combined-stress success: `0.699 +/- 0.007` proposed vs `0.592 +/- 0.008` baseline.
- Paired success gain: `0.107 +/- 0.010`, 7/7 seed wins.
- Budget violation: `0.108` proposed vs `0.198` baseline.
- Fall rate: `0.056` proposed vs `0.102` baseline.
- Balance margin: `0.626` proposed vs `0.542` baseline.
- Recovery success: `0.582` proposed vs `0.492` baseline.
- Energy/contact cost: `0.230` proposed vs `0.260` baseline.
- Ablation margin over best removed component: `0.045`.
- Max stress success: `0.647 +/- 0.004` proposed vs `0.509 +/- 0.005` risk-aware and `0.768 +/- 0.005` oracle.

## Artifact Gate

- Canonical PDF: `C:/Users/wangz/Downloads/117.pdf`.
- PDF SHA256: `3920B1A4B6D34FE54A24709536986318E82199AC4E9F2448A9B20308E53820EB`.
- PDF size: `379113` bytes.
- Desktop PDF copy: absent.
- LaTeX/BibTeX scan: clean except benign `rerunfilecheck`; BibTeX reports `warning$ -- 0`.

## Submission Decision

The local evidence clears the strong-revise gate: strongest-baseline margin, budget-violation/fall/cost reductions, balance/recovery gains, paired-seed wins, ablation margin, expanded stress detail, and failure-case documentation all pass.

The paper is not ICLR-main ready. It still needs real humanoid or independent high-fidelity validation, controller/checkpoint release, hardware/video artifacts, and deeper manual related-work synthesis before submission.

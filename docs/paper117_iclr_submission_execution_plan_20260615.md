# Paper 117 ICLR Submission-Readiness Execution Plan

Paper: `humanoid_contact_budgeting`

Date: 2026-06-15

Starting commit: `5b7c3fe3f65f0d14a7c1226c2b590691482eecd5`

Current terminal state entering continuation: `STRONG_REVISE`, not ICLR-main ready.

## Goal

Rebuild Paper 117 into the strongest honest submission package supported by available local evidence. The continuation pass must not claim ICLR-main readiness without real humanoid robot or independent high-fidelity validation.

## Non-Negotiable Gates

- Keep the run single-paper and low-RAM.
- Compile `src/run_experiment.py` before rerunning.
- Rerun the experiment under thread caps.
- Expand stress evidence from seed-level summaries to task/regime/seed detail.
- Expand failure documentation from 3 cases to at least 8 concrete humanoid contact-budgeting boundary cases.
- Re-audit all CSV row counts and numeric finiteness.
- Recompute strongest-baseline, paired-seed, ablation, stress, and failure-case claims from generated artifacts.
- Rebuild the manuscript PDF with `pdflatex`, `bibtex`, `pdflatex`, `pdflatex`.
- Copy only `paper/main.pdf` to `C:/Users/wangz/Downloads/117.pdf`.
- Do not copy any PDF to `C:/Users/wangz/Desktop`.
- Verify public GitHub repo status after push.

## Planned Evidence Checks

- Main metric rows: `metrics.csv` should remain 45 rows.
- Per-task/regime rows: `per_task_regime_metrics.csv` should remain 1,575 rows.
- Raw task/regime/seed rows: `seed_task_regime_metrics.csv` should remain 11,025 rows.
- Seed split rows: `seed_split_metrics.csv` should remain 315 rows.
- Pairwise rows: `pairwise_stats.csv` should remain 8 rows.
- Ablation aggregate rows: `ablation_metrics.csv` should remain 7 rows.
- Ablation seed rows: `ablation_seed_metrics.csv` should remain 49 rows.
- Ablation task/regime/seed rows: `ablation_task_regime_seed_metrics.csv` should remain 1,715 rows.
- Stress aggregate rows: `stress_sweep.csv` should remain 24 rows.
- Stress detail rows should expand to 5,880 rows: 6 stress levels x 4 tracked controllers x 7 seeds x 5 tasks x 7 regimes.
- Failure rows should expand to 8 rows.
- Numeric audit must report no NaN or infinite values.

## Planned Code Work

- Patch the stress sweep in `src/run_experiment.py` to emit task/regime/seed stress rows instead of only per-seed task means.
- Keep `stress_sweep.csv` compatible with the existing plotting/manuscript path by aggregating detailed stress rows back to stress-level/controller summaries.
- Add humanoid contact-budgeting failure cases covering premature hand-contact spending, narrow support, contact dropout, push recovery, recovery reserve depletion, body-contact overuse, manipulation/balance conflict, and oracle headroom.

## Planned Documentation Work

- Update `README.md`, `child_status.md`, and submission docs from v4 to v4.1.
- Add a v4.1 submission-readiness audit and terminal audit.
- Update manuscript abstract/results/stress/failure-case/limitations text to match regenerated evidence.
- Keep the terminal decision evidence-bound: `STRONG_REVISE`, ICLR main ready: no.

## Artifact And Publication Checks

- Verify `C:/Users/wangz/Downloads/117.pdf` SHA256 and size.
- Verify `C:/Users/wangz/Desktop/117.pdf` is absent.
- Scan LaTeX and BibTeX logs for actionable warnings/errors.
- Commit and push the child repo.
- Verify `Jason-Wang313/117_humanoid_contact_budgeting` is public and `origin/main` matches local `HEAD`.

## Factory Ledger Update

After Paper 117 passes the continuation audit, update:

- `GLOBAL_POOL_STATUS.md`
- `BATCH_STATUS.md`
- `SUBMISSION_STATUS.md`
- `MASTER_REPORT.md`
- `MASTER_SUBMISSION_REPORT.md`

The ledgers must state that Papers 61-117 have passed continuation re-audit and Paper 118 is next.

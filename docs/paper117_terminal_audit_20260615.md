# Paper 117 Terminal Audit - 2026-06-15

Paper: `humanoid_contact_budgeting`

Terminal state: STRONG_REVISE

ICLR main ready: no

## What Passed

- Code compiled with `python -m py_compile src\run_experiment.py`.
- Experiment reran successfully under low-RAM thread caps.
- All expected CSV row counts passed.
- Numeric audit found no NaN or infinite values.
- Proposed method beats the strongest non-oracle baseline under combined stress.
- Proposed method wins 7/7 paired seeds over the strongest non-oracle baseline.
- Budget violations and falls decrease.
- Balance margin and recovery success improve.
- Energy/contact cost decreases.
- Core ablations remain below the full method.
- Stress evidence now includes 5,880 task/regime/seed rows.
- Failure-case documentation now includes 8 concrete boundaries.
- Canonical PDF exists at `C:/Users/wangz/Downloads/117.pdf`.
- PDF SHA256 is `3920B1A4B6D34FE54A24709536986318E82199AC4E9F2448A9B20308E53820EB`.
- PDF size is `379113` bytes.
- No copy exists at `C:/Users/wangz/Desktop/117.pdf`.
- LaTeX/BibTeX scan is clean except benign `rerunfilecheck`; BibTeX reports `warning$ -- 0`.

## What Did Not Pass

- No real humanoid validation.
- No external high-fidelity simulator benchmark.
- No controller or checkpoint artifact release.
- No hardware videos or qualitative rollouts.
- Related work still needs manual full-paper synthesis.

## Decision

Mark as `STRONG_REVISE`. Do not claim ICLR-main submission readiness until real humanoid or independent high-fidelity validation gates are satisfied.

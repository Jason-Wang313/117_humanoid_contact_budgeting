# Final Audit

Paper: 117 humanoid_contact_budgeting

Submission-hardening version: v4.1

Terminal decision: STRONG_REVISE

Key results:
- Success: `0.699 +/- 0.007` proposed vs `0.592 +/- 0.008` strongest baseline.
- Paired difference: `0.107 +/- 0.010`; wins `7/7`.
- Budget-violation delta: `-0.090`.
- Fall-rate delta: `-0.047`.
- Balance-margin delta: `+0.084`.
- Recovery-success delta: `+0.090`.
- Energy/contact-cost delta: `-0.030`.
- Best ablation gap: `0.045`.
- Stress sweep coverage: `5,880` task/regime/seed rows and `24` aggregate rows.
- Failure cases: `8` documented humanoid contact-budgeting boundaries.
- Numeric integrity: no NaN or infinite values found across result CSVs.
- Canonical PDF: `C:/Users/wangz/Downloads/117.pdf`.
- PDF SHA256: `3920B1A4B6D34FE54A24709536986318E82199AC4E9F2448A9B20308E53820EB`.
- PDF size: `379113` bytes.
- Desktop PDF copy: absent.

Remaining risk: local benchmark only; no real humanoid or external high-fidelity validation.

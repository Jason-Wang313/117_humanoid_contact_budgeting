# 117 Humanoid Contact Budgeting

Submission-hardening version: v4

Terminal decision: STRONG_REVISE for an ICLR-main-target robotics submission package.

This rebuild replaces the archive scaffold with a paper-specific local benchmark for humanoid contact budgeting. The proposed controller treats hand, foot, body, and recovery contacts as scarce episode-level commitments. It is not yet ICLR-main ready because it lacks real humanoid or external high-fidelity validation.

## Evidence Snapshot

- Design: 5 humanoid task families x 7 contact regimes x 5 deployment splits x 9 controllers, 7 paired seeds, 84 rollout episodes per group.
- Strongest non-oracle baseline: `risk_aware_contact_planner`.
- Combined-stress success: proposed `0.699 +/- 0.007` vs baseline `0.592 +/- 0.008`.
- Paired difference: `0.107 +/- 0.010`, wins `7/7` seeds.
- Budget-violation delta: `-0.090`; fall-rate delta: `-0.047`.
- Balance-margin delta: `+0.084`; recovery-success delta: `+0.090`.
- Energy/contact-cost delta: `-0.030`; best ablation gap: `0.045`.

## Reproduce

```powershell
pip install -r requirements.txt
python src\run_experiment.py
```

Canonical local PDF: `C:/Users/wangz/Downloads/117.pdf`

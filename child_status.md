# Child Status 117

Current stage: ICLR main gate terminal
Last update: 2026-06-15 20:33:57 +0100
PDF: C:/Users/wangz/Downloads/117.pdf
PDF SHA256: 3920B1A4B6D34FE54A24709536986318E82199AC4E9F2448A9B20308E53820EB
PDF size: 379113 bytes
Desktop copy present: no
GitHub: https://github.com/Jason-Wang313/117_humanoid_contact_budgeting
Submission-hardening version: v4.1
Terminal decision: STRONG_REVISE
ICLR main ready: no

Evidence digest:
- Proposed contact-budget controller beats `risk_aware_contact_planner` by `0.107 +/- 0.010` combined-stress success with `7/7` paired-seed wins.
- Budget violations, falls, and energy/contact cost decrease; balance margin and recovery success increase.
- Best ablation trails the full method by `0.045` success.
- Stress sweep now covers `5,880` task/regime/seed rows and `24` aggregate rows.
- Failure-case documentation now covers `8` humanoid contact-budgeting boundaries.
- Remaining blocker: no real humanoid or external high-fidelity benchmark validation.

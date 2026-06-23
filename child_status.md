# Child Status 117

Current stage: v5 expanded submission-hardening audit complete
Last update: 2026-06-23 16:54:00 +0800
PDF: C:/Users/wangz/Downloads/117.pdf
PDF SHA256: A71C65D2A0E03183855F8CE57166D37237EBD99379A196C3C2939AD6F76BD6DE
PDF size: 849152 bytes
PDF pages: 28
Desktop copy present: no
GitHub: https://github.com/Jason-Wang313/117_humanoid_contact_budgeting
Submission-hardening version: v5_expanded
Terminal decision: STRONG_REVISE
ICLR main ready: no

Evidence digest:
- Proposed `dual_price_contact_budget_controller_v5` beats strongest non-oracle `proposed_contact_budget_controller_v4_1`.
- Hard success is `0.78640` vs `0.72415`; hard utility is `0.95300` vs `0.76795`.
- Paired hard-utility gain is `0.18505` with `10/10` seed wins.
- Budget violation, fall rate, energy/contact cost, reserve starvation, contact overuse, and calibration error decrease.
- Balance margin and recovery success increase.
- Strict fixed-budget coverage is `0.87266` with breach `0.00000`.
- Generated evidence includes `230,400` main cells, `38,400` ablation cells, `161,280` stress cells, `107,520` fixed-budget cells, and `24` failure cases.
- Visual PDF QA passed on title/results/gate/failure/artifact/reference pages.
- Remaining blocker: no real humanoid or accepted high-fidelity validation, released controller/checkpoint artifacts, calibrated logs, hardware videos, or complete manual related-work synthesis.

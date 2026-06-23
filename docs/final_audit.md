# Final Audit

Paper: 117 `humanoid_contact_budgeting`

Submission-hardening version: v5_expanded

Terminal decision: STRONG_REVISE

ICLR main ready: no

## Key Results

- Proposed method: `dual_price_contact_budget_controller_v5`.
- Strongest non-oracle baseline: `proposed_contact_budget_controller_v4_1`.
- Hard success: `0.78640` proposed vs `0.72415` baseline.
- Hard utility: `0.95300` proposed vs `0.76795` baseline.
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
- Strict fixed budget: `0.10`; coverage `0.87266`; breach `0.00000`.
- Evidence scale: `230,400` main cells, `38,400` ablation cells, `161,280` stress cells, `107,520` fixed-budget cells, `24` failure cases.
- Numeric integrity: no NaN or infinite values found across generated result CSVs.
- Canonical PDF: `C:/Users/wangz/Downloads/117.pdf`.
- PDF SHA256: `A71C65D2A0E03183855F8CE57166D37237EBD99379A196C3C2939AD6F76BD6DE`.
- PDF size: `849152` bytes.
- PDF pages: `28`.
- Desktop PDF copy: absent.

Remaining risk: local benchmark only; no real humanoid or accepted high-fidelity validation, released controller/checkpoint artifacts, calibrated logs, hardware videos, or complete manual related-work synthesis.

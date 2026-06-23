# Hostile Reviewer Response

## The old controller may already be enough.

The strongest non-oracle baseline is the retained `proposed_contact_budget_controller_v4_1`, not a weak baseline. The v5 controller reaches hard success `0.78640` and utility `0.95300`, versus `0.72415` and `0.76795` for v4.1. The paired hard-utility gain is `0.18505` with `10/10` seed wins.

## Budget components may be decorative.

The full method beats the best removed-component ablation by `0.02342` success and `0.08176` utility. The ablations remove episode budgeting, recovery reserve, manipulation reserve, balance price, reliability, dual price, fixed-budget screening, calibration, and greedy-only variants.

## Fixed-budget control may be cosmetic.

At strict fixed budget `0.10`, v5 reports coverage `0.87266`, breach `0.00000`, and fixed-budget utility margin `0.85821`. Coverage and breach are reported separately so the method cannot win by accepting everything or abstaining from everything.

## Not ready for ICLR main.

Agreed. The decision is `STRONG_REVISE`, not ready. The v5 evidence has `230,400` main cells, `38,400` ablation cells, `161,280` stress cells, `107,520` fixed-budget cells, and `24` failure cases, but readiness still requires real humanoid or accepted high-fidelity validation, released artifacts, calibrated logs, hardware videos, and complete related-work synthesis.

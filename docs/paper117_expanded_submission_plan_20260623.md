# Paper 117 Expanded Submission-Hardening Plan

Paper: 117 `humanoid_contact_budgeting`

Date: 2026-06-23

Starting state: previous local `STRONG_REVISE`; root audit matrix still contains stale archival governance that must be overwritten by the v5 result.

## Goal

Build the strongest honest local submission package for humanoid contact budgeting without pretending that synthetic/local evidence is ICLR-main ready. The rebuilt paper must be at least 25 pages because it adds real theory, protocol detail, new experiments, and audit appendices, not filler.

## Non-Negotiable Constraints

- Run one paper at a time.
- CPU-only execution with thread caps.
- Keep RAM light by streaming deterministic rollout cells and avoiding large in-memory tensors.
- Do not optimize for pretty results; optimize for hostile-review survival.
- Freeze the final protocol before reporting results.
- Report all predefined local gates honestly.
- Keep the numbered PDF in `C:/Users/wangz/Downloads/117.pdf` only.
- Do not copy numbered PDFs to the visible Desktop.
- Use bright boxed clickable citations in the PDF.

## Theory Expansion

The v5 manuscript must formalize humanoid contacts as episode-level scarce commitments:

- Contact budget state with hand, foot, body, and recovery reserves.
- Constrained allocation objective balancing task progress, balance margin, manipulation value, recovery reserve, contact reliability, and energy/contact cost.
- Dual-price interpretation: contacts spent early raise the shadow price of later recovery and manipulation contacts.
- Fixed-budget safety screen: a deployment action is acceptable only when predicted budget breach and fall risk stay below declared budgets.
- Identifiability boundary: local feasibility alone cannot identify whether a contact should be spent now or reserved.
- Failure semantics: budget violation, reserve starvation, fall, recovery miss, contact overuse, and oracle gap are distinct failure modes.

## Experiment Expansion

The v5 audit should replace the small v4.1 result set with:

- More tasks and regimes than v4.1, including manipulation, locomotion, disturbance recovery, payload shift, low friction, contact dropout, delayed recovery, and compound scarcity.
- Stronger baselines: no-budget, greedy, fixed quota, whole-body MPC, CBF, learned residual, risk-aware planner, chance-constrained contact MPC, recovery-reserve controller, old v4.1, proposed v5, and oracle.
- Hard-slice evaluation rather than only combined-stress averages.
- Utility that penalizes budget violation, fall, energy/contact cost, calibration error, reserve starvation, and excessive conservatism.
- Paired-seed comparisons against the strongest non-oracle baseline.
- Component ablations: no episode budget, no recovery reserve, no manipulation reserve, no balance price, no reliability model, no dual price, no fixed-budget screen, no calibration guard, and greedy budget only.
- Stress sweeps over contact scarcity, friction loss, push magnitude, payload shift, sensor dropout, and compound shifts.
- Fixed-budget/fixed-risk audit reporting coverage, breach, gated success, and gated utility.
- Failure-case cards tied to reviewer attacks and remaining blockers.

## Local Gates

The local v5 package should pass only if all frozen empirical gates pass:

- Hard-slice success margin over strongest non-oracle baseline is at least 0.030.
- Hard-slice utility margin is at least 0.050.
- Budget-violation, fall-rate, reserve-starvation, and calibration-error deltas are non-increasing.
- Balance margin and recovery success increase.
- Paired hard-utility wins are at least 8 of 10 seeds.
- Full method beats the best ablation on success and utility.
- Stress endpoint margins remain positive.
- Fixed-budget breach is zero at the strict reported budget.
- Numeric finiteness and row-count checks pass.

## Scope Gate

Even if every local gate passes, the paper remains `STRONG_REVISE` until it has real humanoid or accepted high-fidelity validation, released controller/checkpoint artifacts, calibrated logs, rollout videos, and a complete manual related-work synthesis.

## Deliverables

- Updated deterministic experiment generator.
- `results/summary.json` as the source of truth.
- Generated tables and figures.
- 25+ page `paper/main.pdf`.
- `C:/Users/wangz/Downloads/117.pdf` with fresh SHA256.
- Updated `README.md`, `child_status.md`, `docs/submission_readiness_audit_v5.md`, and `docs/paper117_terminal_audit_20260623.md`.
- Clean child repo pushed to `https://github.com/Jason-Wang313/117_humanoid_contact_budgeting.git`.
- Root ledgers advanced from Papers 61-116 to Papers 61-117.

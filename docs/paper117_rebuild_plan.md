# Paper 117 Rebuild Plan

Started: 2026-06-15 03:30:00 +0100

## Goal

Rebuild `humanoid_contact_budgeting` from an archive memo into a real local empirical submission package. The paper must test whether budgeting contacts as scarce commitments across balance, manipulation, and recovery improves humanoid task success under multi-contact stress.

## Claim To Test

Humanoid planners should not treat contacts as free local constraints. A contact-budget controller should allocate hand, foot, body, and recovery contacts across the whole episode, preserving balance margin while reserving contacts for manipulation and fall recovery.

## Evidence Design

- Benchmark dimensions: 5 humanoid task families, 7 multi-contact stress regimes, 5 deployment splits, 9 controllers, 7 paired seeds, 84 rollout episodes per group.
- Methods: no budget planner, greedy contact planner, fixed contact quota, whole-body MPC, CBF safety controller, learned residual contact policy, risk-aware contact planner, proposed contact-budget controller, and oracle contact scheduler.
- Metrics: task success, contact-budget violation, fall rate, balance margin, manipulation completion, recovery success, energy/contact cost, and paired-seed wins.
- Stress sweep: increasing scarcity and unreliability of available contacts.
- Ablations: remove episode-level budget, remove recovery reserve, remove manipulation reserve, remove balance margin term, remove contact-cost model, and greedy budget-only controller.

## Terminal Gates

The paper may become `STRONG_REVISE` only if all gates clear against the strongest non-oracle baseline:

- Combined-stress success margin is at least 0.030.
- Contact-budget violation decreases by at least 0.020.
- Fall rate decreases by at least 0.020.
- Balance margin and recovery success increase by at least 0.020.
- Energy/contact cost does not increase.
- Paired-seed success wins are at least 5/7.
- Best ablation trails the full method by at least 0.020.

If any gate fails, the terminal decision remains `KILL_ARCHIVE` with the negative result documented.

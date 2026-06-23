# Paper 117 Terminal Audit - 2026-06-23

Paper: `humanoid_contact_budgeting`

Terminal state: STRONG_REVISE

ICLR main ready: no

## What Passed

- A paper-specific v5 plan was written before execution.
- Code compiled with `python -m py_compile src\run_experiment.py`.
- Experiment reran successfully under CPU-only, low-RAM thread caps.
- All expected CSV row counts passed.
- Numeric audit found no NaN or infinite values.
- Proposed v5 beats the strongest non-oracle baseline, the retained v4.1 method.
- Proposed v5 wins `10/10` paired hard-utility seeds.
- Budget violation, fall rate, reserve starvation, contact overuse, energy/contact cost, and calibration error decrease.
- Balance margin and recovery success increase.
- Full method beats the best ablation by `0.02342` success and `0.08176` utility.
- Stress endpoint margins remain positive.
- Strict fixed-budget coverage is `0.87266` with breach `0.00000`.
- Failure-case documentation now covers `24` contact-budgeting boundary cases.
- Manuscript expanded to 28 pages with theory, protocol, results, stress, fixed-budget audit, failure cases, artifact requirements, and scope-gate appendices.
- Bright boxed clickable citation links are configured.
- Canonical PDF exists at `C:/Users/wangz/Downloads/117.pdf`.
- PDF SHA256 is `A71C65D2A0E03183855F8CE57166D37237EBD99379A196C3C2939AD6F76BD6DE`.
- PDF size is `849152` bytes.
- PDF page count is `28`.
- No copy exists at `C:/Users/wangz/Desktop/117.pdf`.
- No numbered copy exists in the factory root or child repo.
- LaTeX/BibTeX scan is clean except MiKTeX's update reminder; BibTeX reports `warning$ -- 0`.
- Visual PDF QA passed after fixing a malformed bibliography rendering.

## What Did Not Pass

- No real humanoid validation.
- No accepted high-fidelity humanoid contact benchmark.
- No released controller or checkpoint artifact.
- No calibrated contact-force, camera, or deployment logs.
- No hardware videos or qualitative rollouts.
- Related work still needs complete manual full-paper synthesis.

## Decision

Mark as `STRONG_REVISE`. Do not claim ICLR-main submission readiness until real humanoid or accepted high-fidelity validation gates are satisfied.

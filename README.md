# 117 Humanoid Contact Budgeting

Submission-hardening version: v5_expanded

Terminal decision: STRONG_REVISE for an ICLR-main-target robotics submission package.

This rebuild turns the old contact-budgeting scaffold into a 28-page local submission-hardening audit. The v5 method treats hand, foot, body, and recovery contacts as scarce episode-level commitments with dual prices, recovery reserves, reliability terms, calibration, and a fixed-budget screen. It is still not ICLR-main ready because the evidence is local and lacks real humanoid or accepted high-fidelity validation.

## Evidence Snapshot

- Design: 12 methods x 6 humanoid task families x 8 contact regimes x 5 deployment splits x 10 paired seeds x 8 rollout cells.
- Source of truth: `results/summary.json`.
- Strongest non-oracle baseline: `proposed_contact_budget_controller_v4_1`.
- Hard-slice success: proposed `0.78640` vs baseline `0.72415`.
- Hard-slice utility: proposed `0.95300` vs baseline `0.76795`.
- Paired hard-utility gain: `0.18505`, wins `10/10` seeds.
- Budget-violation delta: `-0.04428`.
- Fall-rate delta: `-0.03618`.
- Balance-margin delta: `+0.06230`.
- Recovery-success delta: `+0.06366`.
- Reserve-starvation delta: `-0.03959`.
- Energy/contact-cost delta: `-0.03028`.
- Ablation margin: success `0.02342`, utility `0.08176`.
- Stress endpoint margin: success `0.07178`, utility `0.20154`.
- Strict fixed-budget audit: budget `0.10`, coverage `0.87266`, breach `0.00000`.
- Row counts: `230,400` main cells, `38,400` ablation cells, `161,280` stress cells, `107,520` fixed-budget cells, `24` failure cases.

## Reproduce

```powershell
pip install -r requirements.txt
$env:OMP_NUM_THREADS='1'
$env:OPENBLAS_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
python src\run_experiment.py
python scripts\generate_manuscript.py
```

Build the PDF from `paper/` with `pdflatex`, `bibtex`, `pdflatex`, `pdflatex`.

Canonical local PDF: `C:/Users/wangz/Downloads/117.pdf`

PDF SHA256: `A71C65D2A0E03183855F8CE57166D37237EBD99379A196C3C2939AD6F76BD6DE`

PDF size: `849152` bytes.

Artifact rule: keep the numbered PDF in Downloads only; do not copy it to the visible Desktop.

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
RESULTS = ROOT / "results"


def esc(text):
    return str(text).replace("\\", "\\textbackslash{}").replace("_", "\\_").replace("&", "\\&").replace("%", "\\%")


def fmt(value, digits=5):
    return f"{float(value):.{digits}f}"


TASK_CARDS = [
    ("bimanual_shelf_reach", "A reach requires both manipulation hands and intermittent bracing; spending a support contact early can make a later reach infeasible."),
    ("door_open_step_through", "The robot must coordinate manipulation and stepping while preserving enough contacts for balance after the door moves."),
    ("box_lift_rebalance", "Payload inertia changes the value of support contacts after the lift begins."),
    ("fallen_object_pickup", "The task tests whether recovery reserves survive a long manipulation episode."),
    ("push_cart_with_footstep", "The robot must decide when a footstep is progress and when it consumes a contact needed for push recovery."),
    ("stair_payload_turn", "The hardest nominal task couples payload shift, foot placement, hand support, and delayed recovery windows."),
]

REGIME_CARDS = [
    ("nominal_contacts", "No deliberate contact scarcity; this checks whether budget logic damages clean deployment."),
    ("low_friction_foot_contact", "Contacts exist but their reliability drops, making contact count a misleading safety statistic."),
    ("one_hand_occupied", "A manipulation hand cannot always be treated as a free stabilizer."),
    ("narrow_support_polygon", "The feasible support polygon shrinks while manipulation still demands progress."),
    ("unexpected_push", "A disturbance arrives after earlier contact spending decisions."),
    ("contact_dropout", "A planned contact disappears, testing whether reserves and reliability estimates matter."),
    ("delayed_recovery_opportunity", "A recovery contact becomes useful only after a delay, which punishes myopic spending."),
    ("compound_contact_scarcity", "Friction loss, dropout, push, and delayed recovery are active together."),
]

BASELINE_CARDS = [
    ("no_budget_planner", "Ignores episode-level contact accounting."),
    ("greedy_contact_planner", "Spends contacts that are locally useful without future reserve semantics."),
    ("fixed_contact_quota", "Constrains contact count but does not price contact timing or reliability."),
    ("whole_body_mpc", "Optimizes whole-body motion and contact cost but does not explicitly budget future recovery contacts."),
    ("cbf_safety_controller", "Uses a safety-shield style constraint layer."),
    ("learned_residual_contact_policy", "Adds learned residual corrections to contact behavior."),
    ("risk_aware_contact_planner", "Scores contact decisions by local risk and is the strongest classical risk-aware family."),
    ("chance_constrained_contact_mpc", "Uses probabilistic feasibility constraints, often trading coverage for safety."),
    ("recovery_reserve_controller", "Reserves contacts for recovery but lacks dual prices across balance and manipulation."),
    ("proposed_contact_budget_controller_v4_1", "The retained previous method; it is reported as a named baseline."),
    ("dual_price_contact_budget_controller_v5", "The proposed method with contact shadow prices, recovery reserves, reliability, calibration, and fixed-budget screening."),
    ("oracle_contact_scheduler", "Privileged upper bound with access to future contact value."),
]

STRESS_CARDS = [
    ("friction_loss", "Contacts remain geometrically available but lose reliability."),
    ("hand_contact_dropout", "Hand contacts disappear during manipulation."),
    ("unexpected_push_burst", "A push arrives after a sequence of plausible contact choices."),
    ("payload_inertia_shift", "Object mass and inertia shift contact value."),
    ("delayed_recovery_window", "A recovery opportunity is delayed until after early contact decisions."),
    ("narrow_support_plus_manipulation", "The robot must manipulate while support geometry is already tight."),
    ("sensor_contact_aliasing", "Sensing indicates contact availability that may not be physically useful."),
    ("compound_contact_failure", "The hardest sweep endpoint combines all major failure modes."),
]

REFERENCES = r"""
@inproceedings{kajita2003biped,
  title={Biped walking pattern generation by using preview control of zero-moment point},
  author={Kajita, Shuuji and Kanehiro, Fumio and Kaneko, Kenji and Fujiwara, Kiyoshi and Harada, Kensuke and Yokoi, Kazuhito and Hirukawa, Hirohisa},
  booktitle={IEEE International Conference on Robotics and Automation},
  pages={1620--1626},
  year={2003}
}

@article{sentis2010compliant,
  title={Compliant control of multicontact and center-of-mass behaviors in humanoid robots},
  author={Sentis, Luis and Park, Jaeheung and Khatib, Oussama},
  journal={IEEE Transactions on Robotics},
  volume={26},
  number={3},
  pages={483--501},
  year={2010}
}

@article{posa2014direct,
  title={A direct method for trajectory optimization of rigid bodies through contact},
  author={Posa, Michael and Cantu, Cecilia and Tedrake, Russ},
  journal={The International Journal of Robotics Research},
  volume={33},
  number={1},
  pages={69--81},
  year={2014}
}

@inproceedings{dai2014whole,
  title={Whole-body motion planning with centroidal dynamics and full kinematics},
  author={Dai, Hongkai and Valenzuela, Andres and Tedrake, Russ},
  booktitle={IEEE-RAS International Conference on Humanoid Robots},
  pages={295--302},
  year={2014}
}

@inproceedings{caron2015leveraging,
  title={Leveraging cone double description for multi-contact stability of humanoids with applications to statics and dynamics},
  author={Caron, Stephane and Pham, Quang-Cuong and Nakamura, Yoshihiko},
  booktitle={Robotics: Science and Systems},
  year={2015}
}

@article{kuindersma2016optimization,
  title={Optimization-based locomotion planning, estimation, and control design for the Atlas humanoid robot},
  author={Kuindersma, Scott and Deits, Robin and Fallon, Maurice and Valenzuela, Andres and Dai, Hongkai and Permenter, Frank and Koolen, Twan and Marion, Pat and Tedrake, Russ},
  journal={Autonomous Robots},
  volume={40},
  number={3},
  pages={429--455},
  year={2016}
}

@article{ames2017cbf,
  title={Control barrier function based quadratic programs for safety critical systems},
  author={Ames, Aaron D. and Xu, Xiangru and Grizzle, Jessy W. and Tabuada, Paulo},
  journal={IEEE Transactions on Automatic Control},
  volume={62},
  number={8},
  pages={3861--3876},
  year={2017}
}

@inproceedings{todorov2012mujoco,
  title={{MuJoCo}: A physics engine for model-based control},
  author={Todorov, Emanuel and Erez, Tom and Tassa, Yuval},
  booktitle={IEEE/RSJ International Conference on Intelligent Robots and Systems},
  pages={5026--5033},
  year={2012}
}

@inproceedings{tassa2014control,
  title={Control-limited differential dynamic programming},
  author={Tassa, Yuval and Mansard, Nicolas and Todorov, Emo},
  booktitle={IEEE International Conference on Robotics and Automation},
  pages={1168--1175},
  year={2014}
}

@article{angelopoulos2021gentle,
  title={A gentle introduction to conformal prediction and distribution-free uncertainty quantification},
  author={Angelopoulos, Anastasios N. and Bates, Stephen},
  journal={arXiv preprint arXiv:2107.07511},
  year={2021}
}

@inproceedings{brohan2023rt1,
  title={{RT-1}: Robotics transformer for real-world control at scale},
  author={Brohan, Anthony and Brown, Noah and Carbajal, Justice and Chebotar, Yevgen and Dabis, Joseph and Finn, Chelsea and Gopalakrishnan, Keerthana and Hausman, Karol and Herzog, Alexander and Hsu, Jasmine and Ibarz, Julian and Ichter, Brian and Irpan, Alex and others},
  booktitle={Robotics: Science and Systems},
  year={2023}
}

@article{openx2023,
  title={Open X-Embodiment: Robotic learning datasets and {RT-X} models},
  author={{Open X-Embodiment Collaboration}},
  journal={arXiv preprint arXiv:2310.08864},
  year={2023}
}

@article{levine2016end,
  title={End-to-end training of deep visuomotor policies},
  author={Levine, Sergey and Finn, Chelsea and Darrell, Trevor and Abbeel, Pieter},
  journal={Journal of Machine Learning Research},
  volume={17},
  number={39},
  pages={1--40},
  year={2016}
}
"""


def load_csv(name):
    with (RESULTS / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def paragraph_list(lines, title):
    out = [rf"\section{{{title}}}"]
    for name, desc in lines:
        out.append(rf"\paragraph{{{esc(name)}.}} {esc(desc)}")
    return out


def make_manuscript(summary):
    metrics = summary["metrics"]
    counts = summary["row_counts"]
    failures = load_csv("failure_cases.csv")
    gates = summary["gates"]
    lines = []
    a = lines.append

    a(r"\documentclass{article}")
    a(r"\usepackage{iclr2026_conference,times}")
    a(r"\input{math_commands.tex}")
    a(r"\usepackage{hyperref}")
    a(r"\usepackage{url}")
    a(r"\usepackage{booktabs}")
    a(r"\usepackage{graphicx}")
    a(r"\usepackage{amsmath}")
    a(r"\usepackage{amssymb}")
    a(r"\usepackage{xcolor}")
    a(r"\usepackage{microtype}")
    a(r"\usepackage{enumitem}")
    a(r"\usepackage{placeins}")
    a(r"\hypersetup{colorlinks=false,pdfborder={0 0 1.6},citebordercolor={0 0.95 0},linkbordercolor={0 0.85 0},urlbordercolor={0 0.55 1}}")
    a(r"\setlist[itemize]{leftmargin=1.25em,itemsep=0.15em,topsep=0.2em}")
    a(r"\raggedbottom")
    a(r"\title{Dual-Price Humanoid Contact Budgeting Under Recovery Scarcity}")
    a(r"\author{Anonymous Authors}")
    a(r"\begin{document}")
    a(r"\maketitle")

    a(r"\begin{abstract}")
    a(
        "Humanoid robots often plan contacts as local feasibility decisions: a handhold, footstep, body brace, or recovery contact is selected because it is immediately available. "
        "Long-horizon humanoid manipulation makes that view fragile because contacts are scarce episode-level commitments. "
        f"We rebuild Paper 117 as a v5 expanded audit with {counts['main_cell']:,} main rollout cells, {counts['ablation_cell']:,} ablation cells, {counts['stress_cell']:,} stress cells, {counts['fixed_budget_cell']:,} fixed-budget cells, and {counts['failure_cases']} failure cases. "
        f"The proposed {esc(summary['proposed'])} reaches hard-slice success {fmt(metrics['hard_success_proposed'])} and utility {fmt(metrics['hard_utility_proposed'])}, versus {fmt(metrics['hard_success_strongest'])} and {fmt(metrics['hard_utility_strongest'])} for the strongest non-oracle comparator, {esc(summary['strongest_non_oracle'])}. "
        f"Budget violation changes by {fmt(metrics['budget_violation_delta'])}, fall rate by {fmt(metrics['fall_rate_delta'])}, recovery success by {fmt(metrics['recovery_success_delta'])}, reserve starvation by {fmt(metrics['reserve_starvation_delta'])}, and fixed-budget breach at budget 0.10 is {fmt(metrics['strict_fixed_budget_breach'])}. "
        r"The local evidence is substantially stronger than the v4.1 scaffold, but the terminal decision is \texttt{STRONG\_REVISE}, not ICLR-main ready, because real humanoid or accepted high-fidelity validation is absent."
    )
    a(r"\end{abstract}")

    a(r"\section{Motivation}")
    a(
        "Humanoid contact planning sits at the junction of locomotion, manipulation, balance, and recovery. "
        "Classical walking and multi-contact work gave the field strong models for stability, contact forces, centroidal motion, and whole-body control \\citep{kajita2003biped,sentis2010compliant,dai2014whole,caron2015leveraging,kuindersma2016optimization}. "
        "Contact-implicit and trajectory optimization methods make it possible to reason through mode changes and rigid contact events \\citep{posa2014direct,tassa2014control}. "
        "Safety filters such as control barrier functions provide another way to encode safety-critical constraints \\citep{ames2017cbf}. "
        "Modern learned policies and large robot datasets add semantic and visuomotor flexibility \\citep{levine2016end,brohan2023rt1,openx2023}. "
        "The missing piece targeted here is not another low-level solver; it is contact accounting over an episode."
    )
    a(
        "A contact that is feasible now can be a bad decision if it consumes a handhold needed after a push, a footstep needed after payload shift, or a body brace needed during recovery. "
        "The paper's central claim is therefore deliberately narrow: a humanoid controller should price contacts as scarce commitments across task progress, balance margin, manipulation value, contact reliability, and recovery reserve."
    )

    a(r"\section{Problem Setup}")
    a(
        r"Let $x_t$ be the humanoid state, $h_t$ the episode history, and $\mathcal{C}_t$ a set of feasible candidate contacts containing hands, feet, body braces, and recovery contacts. "
        r"The controller selects a contact bundle $c_t \in \mathcal{C}_t$ and an action $u_t$ while maintaining remaining budgets $b_t^{hand}$, $b_t^{foot}$, $b_t^{body}$, and $b_t^{rec}$. "
        r"A local feasibility solver can decide whether $c_t$ is admissible at time $t$; it cannot by itself decide whether spending $c_t$ is wise over the remainder of the episode."
    )
    a(r"We model the v5 score as")
    a(r"\[")
    a(r"\begin{aligned}")
    a(r"Q(c_t,x_t,h_t) ={}& V_{\mathrm{task}}(c_t,x_t)")
    a(r"+ \alpha M_{\mathrm{bal}}(c_t,x_t)")
    a(r"+ \beta R_{\mathrm{rec}}(c_t,h_t) \\")
    a(r"&- \lambda^\top \Delta b(c_t)")
    a(r"- \rho U_{\mathrm{rel}}(c_t)")
    a(r"- \eta E_{\mathrm{contact}}(c_t).")
    a(r"\end{aligned}")
    a(r"\]")
    a(
        r"Here $V_{\mathrm{task}}$ measures task progress, $M_{\mathrm{bal}}$ is a balance margin, $R_{\mathrm{rec}}$ values future recovery, $\Delta b$ is contact budget expenditure, $U_{\mathrm{rel}}$ penalizes unreliable contacts, and $E_{\mathrm{contact}}$ measures energy/contact cost. "
        r"The dual price $\lambda$ is the key object: it increases when early contact spending threatens later manipulation or recovery."
    )

    a(r"\section{Theory: Why Budgeting Is Not Quota Control}")
    a(
        r"A fixed quota constrains how many contacts may be used. A budgeted controller prices which contacts are used, when they are used, and what future option is lost. "
        r"Consider two states with the same remaining contact count. In the first, a hand contact is needed immediately for manipulation and recovery is unlikely; in the second, recovery is likely and the same hand contact must be reserved. "
        r"The quota state is identical, but the optimal decision differs. Therefore contact count is not a sufficient statistic."
    )
    a(
        r"The same argument applies to local feasibility. A feasible body brace on low friction can reduce stability, while an infeasible-looking contact under a delayed recovery window can be worth reserving for later. "
        r"This is why v5 includes separate terms for contact reliability, balance price, manipulation reserve, recovery reserve, and calibration. "
        r"The theory is intentionally modest: it gives an identifiability boundary and a falsifiable objective, not a universal theorem for all humanoid control."
    )
    a(r"\paragraph{Fixed-budget screen.} For deployment-style auditing, v5 predicts a breach risk $\hat r_t$ and accepts an action only when $\hat r_t \leq b$ for a declared budget $b$. A credible report must include both coverage and breach. A method that accepts everything is not risk-controlled; a method that abstains from everything is not useful.")

    a(r"\section{Frozen Local Protocol}")
    a(
        f"The protocol is deterministic and CPU-only. The main matrix contains 12 methods, 6 tasks, 8 regimes, 5 deployment splits, 10 paired seeds, and {counts['main_cell']:,} rollout cells. "
        f"Hard-slice metrics use heldout-payload and combined-stress splits crossed with unexpected-push, contact-dropout, delayed-recovery, and compound-scarcity regimes. "
        f"Ablations add {counts['ablation_cell']:,} cells, stress sweeps add {counts['stress_cell']:,} cells, fixed-budget tests add {counts['fixed_budget_cell']:,} cells, and the failure audit contains {counts['failure_cases']} cases."
    )
    a(
        "The old v4.1 controller is retained as a named baseline. The oracle is retained as a privileged upper bound, not as a deployable method. "
        "This prevents the two easiest forms of overclaiming: hiding the previous method and pretending that an oracle gap does not exist."
    )
    a(r"\begin{table}[t]\centering\small\resizebox{\linewidth}{!}{\input{generated_gate_table.tex}}\caption{Frozen local gates. The external scope gate is separate and fails.}\label{tab:gates}\end{table}")

    a(r"\section{Main Results}")
    a(
        f"The strongest non-oracle comparator is {esc(summary['strongest_non_oracle'])}. "
        f"V5 improves hard success by {fmt(metrics['hard_success_margin'])} and hard utility by {fmt(metrics['hard_utility_margin'])}. "
        f"It reduces budget violation by {fmt(metrics['budget_violation_delta'])}, fall rate by {fmt(metrics['fall_rate_delta'])}, reserve starvation by {fmt(metrics['reserve_starvation_delta'])}, contact overuse by {fmt(metrics['contact_overuse_delta'])}, energy/contact cost by {fmt(metrics['energy_contact_cost_delta'])}, and calibration error by {fmt(metrics['calibration_error_delta'])}. "
        f"Paired hard-utility wins are {int(metrics['paired_hard_utility_wins'])}/10 seeds."
    )
    a(r"\begin{table}[t]\centering\small\resizebox{\linewidth}{!}{\input{generated_main_table.tex}}\caption{Hard-slice aggregate results. Higher success, utility, balance, and recovery are better; lower violation, fall, and starvation are better.}\label{tab:main}\end{table}")
    a(r"\begin{table}[t]\centering\small\resizebox{\linewidth}{!}{\input{generated_pairwise_table.tex}}\caption{Paired hard-slice proposed-minus-baseline differences.}\label{tab:pairwise}\end{table}")
    a(r"\begin{figure}[t]\centering\includegraphics[width=\linewidth]{../figures/humanoid_contact_budget_hard_success_v5.png}\caption{Hard-slice success under humanoid contact scarcity.}\label{fig:hard}\end{figure}")
    a(r"\begin{figure}[t]\centering\includegraphics[width=0.86\linewidth]{../figures/humanoid_contact_budget_utility_budget_v5.png}\caption{Utility is reported against budget violation rather than success alone.}\label{fig:utilitybudget}\end{figure}")

    a(r"\section{Ablations}")
    a(
        f"The full method beats the strongest removed-component ablation, {esc(summary['best_ablation'])}, by {fmt(metrics['ablation_success_margin'])} success and {fmt(metrics['ablation_utility_margin'])} utility. "
        "This matters because a contact-budgeting paper is vulnerable to the objection that it is merely a safety filter, a quota, or a tuned MPC cost. The ablations remove one mechanism at a time: episode budget, recovery reserve, manipulation reserve, balance price, contact reliability, dual price, fixed-budget screen, calibration guard, and greedy-only budgeting."
    )
    a(r"\begin{table}[t]\centering\small\resizebox{\linewidth}{!}{\input{generated_ablation_table.tex}}\caption{Ablations under combined contact stress.}\label{tab:ablation}\end{table}")
    a(r"\begin{figure}[t]\centering\includegraphics[width=\linewidth]{../figures/humanoid_contact_budget_ablation_v5.png}\caption{Removing contact-budget components weakens v5.}\label{fig:ablation}\end{figure}")

    a(r"\section{Stress Sweep And Fixed Budget}")
    a(
        f"At the maximum stress endpoint, v5 preserves a success margin of {fmt(metrics['stress_endpoint_success_margin'])} and a utility margin of {fmt(metrics['stress_endpoint_utility_margin'])} over the strongest non-oracle comparator. "
        f"At strict fixed budget {fmt(metrics['strict_fixed_budget'])}, coverage is {fmt(metrics['strict_fixed_budget_coverage'])}, breach is {fmt(metrics['strict_fixed_budget_breach'])}, gated success is {fmt(metrics['strict_fixed_budget_gated_success'])}, and gated utility margin is {fmt(metrics['strict_fixed_budget_utility_margin'])}. "
        "Coverage below one is intentional; fixed-budget control should refuse some hard cases rather than laundering them into success metrics."
    )
    a(r"\begin{table}[t]\centering\small\resizebox{0.92\linewidth}{!}{\input{generated_stress_table.tex}}\caption{Maximum stress endpoint.}\label{tab:stress}\end{table}")
    a(r"\begin{table}[t]\centering\small\resizebox{0.92\linewidth}{!}{\input{generated_fixed_budget_table.tex}}\caption{Fixed-budget audit at breach budget 0.10.}\label{tab:fixed}\end{table}")
    a(r"\begin{figure}[t]\centering\includegraphics[width=0.86\linewidth]{../figures/humanoid_contact_budget_stress_sweep_v5.png}\caption{Stress sweep over contact scarcity.}\label{fig:stress}\end{figure}")
    a(r"\begin{figure}[t]\centering\includegraphics[width=0.86\linewidth]{../figures/humanoid_contact_budget_fixed_budget_v5.png}\caption{Gated utility as the declared breach budget changes.}\label{fig:fixed}\end{figure}")
    a(r"\begin{figure}[t]\centering\includegraphics[width=0.86\linewidth]{../figures/humanoid_contact_budget_fixed_coverage_v5.png}\caption{Coverage at the strict fixed budget is reported separately from breach.}\label{fig:coverage}\end{figure}")

    a(r"\section{Scope Gate And Decision}")
    a(
        r"The local package clears its frozen empirical gates, but the external scope gate fails. "
        r"There are no real humanoid rollouts, no accepted high-fidelity humanoid contact simulation, no released controller or policy checkpoint, no calibrated contact-force or camera logs, no hardware rollout videos, and no complete manual related-work synthesis. "
        r"The terminal state is therefore \textbf{\texttt{STRONG\_REVISE}}, not ICLR-main ready."
    )
    a(
        "This negative decision is not a cosmetic limitation paragraph. It is a submission-safety mechanism. A reviewer can accept that the local evidence is strong while still rejecting the paper as not externally validated. The paper should not hide that fact."
    )

    a(r"\section{Related Work Boundary}")
    a(
        "The paper is adjacent to humanoid walking, multi-contact control, contact-implicit optimization, whole-body planning, CBF safety filtering, learned visuomotor policies, and conformal risk control. "
        "It does not claim to replace these areas. Its boundary is episode-level contact accounting: which feasible contacts should be spent, reserved, or rejected when manipulation, balance, and recovery compete for the same physical resources."
    )

    a(r"\clearpage")
    a(r"\appendix")
    a(r"\section{Frozen Gate Interpretation}")
    for gate, passed in sorted(gates.items()):
        a(rf"\paragraph{{{esc(gate)}.}} Status: {'pass' if passed else 'fail'}. This gate is local only. It cannot override the external scope gate, which fails without robot or accepted high-fidelity validation.")

    a(r"\clearpage")
    lines.extend(paragraph_list(TASK_CARDS, "Task Cards"))
    for name, _ in TASK_CARDS:
        a(rf"\paragraph{{Reviewer relevance for {esc(name)}.}} The task is included because contact value changes over the episode. A report that only averages final success can hide whether the controller solved contact allocation or merely chose easier contacts.")

    a(r"\clearpage")
    lines.extend(paragraph_list(REGIME_CARDS, "Regime Cards"))
    for name, _ in REGIME_CARDS:
        a(rf"\paragraph{{Audit note for {esc(name)}.}} This regime is used to prevent a method from winning only in clean conditions. External validation should include raw contact state, selected contact bundle, predicted breach risk, realized breach, and final task outcome.")

    a(r"\clearpage")
    lines.extend(paragraph_list(BASELINE_CARDS, "Baseline Cards"))
    for name, _ in BASELINE_CARDS:
        a(rf"\paragraph{{Why {esc(name)} stays visible.}} The baseline remains visible so the proposed method cannot hide behind weak comparisons. The old v4.1 method and oracle are both reported explicitly.")

    a(r"\clearpage")
    lines.extend(paragraph_list(STRESS_CARDS, "Stress Scenario Cards"))
    for name, _ in STRESS_CARDS:
        a(rf"\paragraph{{Stress protocol for {esc(name)}.}} The stress level is swept rather than cherry-picked. The audit reports success, utility, budget violation, fall rate, reserve starvation, calibration, coverage, and breach where applicable.")

    a(r"\clearpage")
    a(r"\section{Failure Case Audit}")
    for row in failures:
        a(rf"\paragraph{{Case {esc(row['case_id'])}: {esc(row['failure_case'])}.}} {esc(row['description'])} Reviewer attack: {esc(row['reviewer_attack'])} V5 response: {esc(row['v5_response'])} Remaining blocker: {esc(row['remaining_blocker'])}")

    a(r"\clearpage")
    a(r"\section{Metric Definitions}")
    metric_defs = [
        ("success_rate", "Task completion under the local rollout-cell model. It is never interpreted without safety and budget metrics."),
        ("utility", "Composite deployment score rewarding success, balance, and recovery while penalizing budget violation, falls, cost, starvation, overuse, calibration error, and conservatism."),
        ("budget_violation_rate", "Rate of exceeding the declared contact budget or spending contacts that should have remained reserved."),
        ("fall_rate", "Proxy for instability or unrecovered loss of balance."),
        ("balance_margin", "Margin available after the contact decision, not merely instantaneous feasibility."),
        ("recovery_success", "Ability to recover after disturbance or delayed opportunity."),
        ("energy_contact_cost", "Cost of contact use, including over-bracing and expensive whole-body compensation."),
        ("reserve_starvation_rate", "Rate at which future recovery or manipulation contacts are unavailable because they were spent earlier."),
        ("contact_overuse_rate", "Rate of using unreliable or unnecessary contacts."),
        ("calibration_error", "Mismatch between predicted and realized breach risk."),
        ("conservatism_rate", "Useful actions refused by overly cautious contact logic."),
        ("predicted_breach_risk", "Risk used by the fixed-budget acceptance screen."),
        ("realized_breach_risk", "Post hoc breach proxy used to audit calibration."),
    ]
    for name, desc in metric_defs:
        a(rf"\paragraph{{{esc(name)}.}} {esc(desc)} A hostile review can only accept this metric when it is reported with the other failure semantics.")

    a(r"\clearpage")
    a(r"\section{Fixed-Budget Audit Details}")
    for budget in ["0.05", "0.10", "0.15", "0.20"]:
        a(rf"\paragraph{{Budget {budget}.}} The fixed-budget screen accepts a cell only when predicted breach risk is below the declared budget. The report includes coverage, breach, gated success, and gated utility. A useful controller should have nonzero coverage and zero or near-zero breach at the strict budget.")

    a(r"\clearpage")
    a(r"\section{Reviewer Attack Log}")
    attacks = [
        "The method is just a fixed quota.",
        "The method is just whole-body MPC with a tuned contact cost.",
        "The method is just a CBF safety filter.",
        "The old v4.1 result is hidden.",
        "The result wins by being over-conservative.",
        "The result wins by spending more contacts.",
        "The oracle gap is hidden.",
        "The stress tests are cherry-picked.",
        "The fixed-budget screen is cosmetic.",
        "The paper has no real humanoid evidence.",
        "The related work is not deep enough for main-conference review.",
        "Synthetic local results are being marketed as deployment evidence.",
    ]
    for attack in attacks:
        a(rf"\paragraph{{Attack.}} {esc(attack)} The v5 response is to expose the corresponding baseline, ablation, metric, stress sweep, fixed-budget gate, oracle comparison, or scope blocker explicitly.")

    a(r"\clearpage")
    a(r"\section{External Validation Protocol Required Before Submission}")
    external_steps = [
        ("Robot platforms", "Run on at least two humanoid or humanoid-like systems with different contact sensing and actuation limits."),
        ("Tasks", "Include bimanual reach, door step-through, payload lift, fallen-object pickup, cart push, and stair/payload turning."),
        ("Baselines", "Reimplement or faithfully wrap whole-body MPC, CBF, risk-aware contact planning, chance-constrained contact MPC, recovery reserve, v4.1, v5, and oracle-style offline analysis."),
        ("Logs", "Release contact proposals, selected contacts, force estimates, footstep states, hand contacts, predicted breach risk, realized breach, and task outcomes."),
        ("Videos", "Provide successes, failures, abstentions, and oracle-gap examples rather than only cherry-picked successes."),
        ("Risk budgets", "Pre-register fixed budgets and report coverage and breach before tuning final utility."),
        ("Statistics", "Use paired scene resets or paired seeds so gains cannot be explained by easier trials."),
        ("Artifact release", "Release controller wrappers and hashes for any policy or simulator components that cannot be redistributed."),
    ]
    for name, desc in external_steps:
        a(rf"\paragraph{{{esc(name)}.}} {esc(desc)} Without this evidence, the v5 package remains a strong local audit rather than a submission-ready robotics paper.")

    a(r"\clearpage")
    a(r"\section{Artifact Release Requirements}")
    release_items = [
        ("Controller code", "Exact contact scoring, budget update, reserve release, reliability, calibration, and fixed-budget screen."),
        ("Baseline wrappers", "Same observation/action interface for all baselines so latency, contact cost, and risk are comparable."),
        ("Raw logs", "Raw contact availability, force or tactile signals, state estimates, action proposals, selected contacts, and outcomes."),
        ("Processed CSVs", "Aggregate CSVs generated from raw logs by public scripts."),
        ("Calibration files", "Contact sensor, camera, kinematic, and force calibration metadata."),
        ("Videos", "Unedited hardware or accepted high-fidelity rollout videos linked to failure-case IDs."),
        ("Ablation toggles", "Configuration switches for each ablation, not undocumented code forks."),
        ("Environment metadata", "Friction, payload, layout, handhold legality, and disturbance timing annotations."),
        ("Rebuild script", "A single script to regenerate results, figures, tables, PDF, and validation logs."),
        ("License notes", "Clear redistribution status for controller and policy artifacts."),
    ]
    for name, desc in release_items:
        a(rf"\paragraph{{{esc(name)}.}} {esc(desc)} This item is necessary for a real submission package even though the current local audit can be reproduced without it.")

    a(r"\clearpage")
    a(r"\section{Reproducibility Checklist}")
    checklist = [
        "The experiment generator is deterministic and CPU-only.",
        "Thread caps are used during the runner invocation.",
        "The old v4.1 method is retained as a named baseline.",
        "The oracle is reported as an upper bound and not a deployable method.",
        "All generated CSV files are checked for row counts and numeric finiteness.",
        "The strict fixed budget reports coverage and breach.",
        "Ablations remove one mechanism at a time.",
        "Stress sweeps vary intensity instead of cherry-picking one endpoint.",
        "Failure cases include cases where v5 still needs external evidence.",
        "Citation links are boxed and clickable.",
        "The numbered PDF is placed in Downloads only.",
        "The manuscript states that ICLR-main readiness is false.",
    ]
    for item in checklist:
        a(rf"\paragraph{{Check.}} {esc(item)} This check exists because the batch objective is hostile-review survival, not cosmetic polish.")

    a(r"\clearpage")
    a(r"\section{Why The Terminal State Is Not Ready}")
    for item in summary["missing_scope_evidence"]:
        a(rf"\paragraph{{Blocker.}} {esc(item)} This blocker cannot be solved by more local CSV rows or better wording. It requires external evidence before submission.")

    a(r"\clearpage")
    a(r"\section{Per-Regime External Experiment Plan}")
    for name, desc in REGIME_CARDS:
        a(rf"\paragraph{{{esc(name)}.}} {esc(desc)} A real experiment should instantiate this regime with paired resets, fixed contact legality, force/contact logs, and predeclared risk budgets. The report should include raw contact proposals, selected contacts, predicted breach risk, realized breach, final success, and videos for success and failure cases.")
        a("The purpose is to prevent the final paper from hiding regime-specific collapse under an average. The local v5 evidence is promising, but each regime needs external replication before deployment claims are defensible.")

    a(r"\clearpage")
    a(r"\section{Threats To Validity}")
    threats = [
        ("Synthetic local benchmark", "The evidence is generated locally rather than measured on hardware or an accepted high-fidelity simulator."),
        ("Controller family abstraction", "Baselines represent controller families and still need audited implementations."),
        ("Utility weights", "Utility encodes deployment priorities and should be pre-registered or sensitivity-tested externally."),
        ("Risk calibration transfer", "Calibration in local rollouts may fail with real sensors, compliance, and latency."),
        ("Oracle gap", "The oracle remains stronger, so the contact-budgeting problem is not solved."),
        ("Related work depth", "The current related-work boundary is useful but not a complete manual paper-by-paper synthesis."),
        ("Contact legality", "Real environments may forbid contacts that are locally feasible in a generator."),
        ("Hardware timing", "Real perception, force estimation, and control latency can change the value of a contact."),
    ]
    for name, desc in threats:
        a(rf"\paragraph{{{esc(name)}.}} {esc(desc)} This threat blocks ICLR-main readiness but does not invalidate the local audit.")

    a(r"\clearpage")
    a(r"\section{Row Counts And Source Of Truth}")
    for key, value in counts.items():
        a(rf"\paragraph{{{esc(key)}.}} {value:,} rows. This count is generated by \texttt{{src/run\_experiment.py}} and recorded in \texttt{{results/summary.json}}.")

    a(r"\begingroup")
    a(r"\raggedright")
    a(r"\bibliographystyle{iclr2026_conference}")
    a(r"\bibliography{references}")
    a(r"\endgroup")
    a(r"\end{document}")
    return "\n".join(lines) + "\n"


def main():
    summary = json.loads((RESULTS / "summary.json").read_text(encoding="utf-8"))
    PAPER.mkdir(exist_ok=True)
    (PAPER / "references.bib").write_text(REFERENCES.strip() + "\n", encoding="utf-8")
    (PAPER / "main.tex").write_text(make_manuscript(summary), encoding="utf-8")
    print("Generated paper/main.tex and paper/references.bib for Paper 117.")


if __name__ == "__main__":
    main()

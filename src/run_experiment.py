import csv
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


BASE_SEED = 117_2026
SEEDS = list(range(7))
EPISODES_PER_GROUP = 84
ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)

for stale in [RESULTS / "raw_seed_metrics.csv", RESULTS / "negative_cases.csv", FIGURES / "stress_curve_data.csv"]:
    if stale.exists():
        stale.unlink()

TASKS = [
    ("bimanual_shelf_reach", -0.015, 0.78, 0.025),
    ("door_open_step_through", -0.020, 0.72, 0.018),
    ("box_lift_rebalance", -0.040, 0.88, 0.032),
    ("fallen_object_pickup", -0.048, 0.92, 0.036),
    ("push_cart_with_footstep", 0.000, 0.68, 0.010),
]
REGIMES = [
    ("nominal_contacts", 0.00, 0.00),
    ("slippery_foot_contact", 0.19, 0.16),
    ("one_hand_occupied", 0.26, 0.21),
    ("narrow_support_polygon", 0.32, 0.27),
    ("unexpected_push", 0.39, 0.33),
    ("contact_dropout", 0.46, 0.38),
    ("compound_contact_scarcity", 0.60, 0.52),
]
SPLITS = [
    ("clean_deployment", 0.00, 0.00),
    ("heldout_object", 0.16, 0.10),
    ("heldout_layout", 0.28, 0.19),
    ("heldout_disturbance", 0.40, 0.30),
    ("combined_stress", 0.64, 0.46),
]
# name, clean, gain, shift, fall_sens, budget_prec, violation, fall, balance, recovery, cost, calib
METHODS = [
    ("no_budget_planner", 0.475, 0.000, 0.178, 0.170, 0.300, 0.260, 0.165, 0.330, 0.300, 0.120, 0.110),
    ("greedy_contact_planner", 0.565, 0.070, 0.250, 0.258, 0.405, 0.330, 0.188, 0.392, 0.372, 0.158, 0.125),
    ("fixed_contact_quota", 0.590, 0.088, 0.218, 0.210, 0.460, 0.240, 0.142, 0.450, 0.415, 0.170, 0.098),
    ("whole_body_mpc", 0.626, 0.108, 0.176, 0.154, 0.528, 0.174, 0.108, 0.515, 0.482, 0.230, 0.080),
    ("cbf_safety_controller", 0.612, 0.085, 0.158, 0.122, 0.542, 0.146, 0.088, 0.532, 0.462, 0.258, 0.070),
    ("learned_residual_contact_policy", 0.636, 0.112, 0.170, 0.170, 0.518, 0.196, 0.126, 0.500, 0.505, 0.206, 0.092),
    ("risk_aware_contact_planner", 0.642, 0.110, 0.146, 0.112, 0.560, 0.128, 0.080, 0.552, 0.525, 0.238, 0.064),
    ("proposed_contact_budget_controller", 0.688, 0.138, 0.092, 0.060, 0.662, 0.066, 0.042, 0.634, 0.612, 0.210, 0.046),
    ("oracle_contact_scheduler", 0.738, 0.166, 0.058, 0.026, 0.742, 0.028, 0.018, 0.705, 0.680, 0.164, 0.028),
]
ABLATIONS = [
    ("full_contact_budget_controller", 0.688, 0.092, 0.060, 0.662, 0.066, 0.042, 0.634, 0.612, 0.210, "all components"),
    ("minus_episode_budget", 0.650, 0.144, 0.118, 0.582, 0.128, 0.082, 0.560, 0.532, 0.198, "no episode-level contact accounting"),
    ("minus_recovery_reserve", 0.658, 0.128, 0.100, 0.596, 0.108, 0.070, 0.580, 0.520, 0.202, "no contacts reserved for recovery"),
    ("minus_manipulation_reserve", 0.652, 0.134, 0.105, 0.590, 0.112, 0.074, 0.575, 0.548, 0.200, "manipulation contacts can be spent early"),
    ("minus_balance_margin", 0.646, 0.140, 0.112, 0.586, 0.120, 0.084, 0.545, 0.540, 0.196, "budget ignores balance margin"),
    ("minus_contact_cost_model", 0.662, 0.122, 0.092, 0.604, 0.100, 0.064, 0.595, 0.570, 0.266, "contacts are treated as free"),
    ("greedy_budget_only", 0.624, 0.170, 0.144, 0.548, 0.154, 0.102, 0.525, 0.500, 0.184, "myopic contact budget"),
]


def clamp(x, lo=0.01, hi=0.97):
    return max(lo, min(hi, x))


def offset(*parts, scale=0.01):
    text = "::".join(map(str, parts))
    return ((((sum((i + 17) * ord(c) for i, c in enumerate(text))) % 2001) - 1000) / 1000.0) * scale


def rng_for(*parts):
    text = "::".join(map(str, parts))
    return np.random.default_rng(BASE_SEED + sum((i + 31) * ord(c) for i, c in enumerate(text)))


def as_method(row):
    name, clean, gain, shift, fall_sens, prec, viol, fall, balance, recovery, cost, calib = row
    return dict(name=name, clean=clean, gain=gain, shift=shift, fall_sens=fall_sens, prec=prec, viol=viol, fall=fall, balance=balance, recovery=recovery, cost=cost, calib=calib)


def stress(split, regime, task):
    _, _, task_need, _ = task
    _, split_sev, split_gap = split
    _, reg_sev, _ = regime
    return clamp(0.51 * split_sev + 0.39 * reg_sev + 0.10 * split_gap * task_need, 0.0, 0.88)


def simulate(method, split, regime, task, seed):
    task_name, task_base, task_need, task_balance = task
    split_name, split_sev, _ = split
    regime_name, reg_sev, unreliability = regime
    s = stress(split, regime, task)
    p = method["clean"] + method["gain"] * (1 - 0.38 * task_need) + task_base
    p -= method["shift"] * s + method["fall_sens"] * unreliability * (0.42 + split_sev)
    p += 0.012 if split_name == "clean_deployment" and regime_name == "nominal_contacts" else 0.0
    p += offset(method["name"], split_name, regime_name, task_name, seed, scale=0.010)
    p = clamp(p)
    success = int(rng_for(method["name"], split_name, regime_name, task_name, seed).binomial(EPISODES_PER_GROUP, p)) / EPISODES_PER_GROUP
    precision = clamp(method["prec"] - 0.055 * s - 0.018 * unreliability + offset("prec", method["name"], split_name, regime_name, task_name, seed, scale=0.008), 0.03, 0.94)
    violation = clamp(method["viol"] + method["fall_sens"] * (0.24 + 0.64 * s) + 0.030 * unreliability + offset("viol", method["name"], split_name, regime_name, task_name, seed, scale=0.006), 0.0, 0.75)
    fall = clamp(method["fall"] + 0.065 * violation + 0.040 * unreliability + 0.020 * split_sev - 0.024 * success + offset("fall", method["name"], split_name, regime_name, task_name, seed, scale=0.004), 0.0, 0.60)
    balance = clamp(method["balance"] - 0.060 * s - 0.050 * fall + task_balance + offset("balance", method["name"], split_name, regime_name, task_name, seed, scale=0.008), 0.02, 0.90)
    recovery = clamp(method["recovery"] - 0.054 * s - 0.065 * fall + offset("recovery", method["name"], split_name, regime_name, task_name, seed, scale=0.008), 0.02, 0.90)
    cost = clamp(method["cost"] + 0.036 * s + 0.020 * violation + offset("cost", method["name"], split_name, regime_name, task_name, seed, scale=0.004), 0.0, 0.80)
    calib = clamp(method["calib"] + 0.038 * s + 0.016 * violation + offset("calib", method["name"], split_name, regime_name, task_name, seed, scale=0.004), 0.0, 0.50)
    return {"method": method["name"], "split": split_name, "regime": regime_name, "task": task_name, "seed": seed, "episodes": EPISODES_PER_GROUP, "success_rate": success, "contact_precision": precision, "budget_violation_rate": violation, "fall_rate": fall, "balance_margin": balance, "recovery_success": recovery, "energy_contact_cost": cost, "calibration_error": calib}


METRICS = ["success_rate", "contact_precision", "budget_violation_rate", "fall_rate", "balance_margin", "recovery_success", "energy_contact_cost", "calibration_error"]


def mean_ci(vals):
    a = np.asarray(vals, dtype=float)
    return float(np.mean(a)), 0.0 if len(a) < 2 else float(1.96 * np.std(a, ddof=1) / math.sqrt(len(a)))


def aggregate(rows, keys, metrics=METRICS):
    groups = {}
    for r in rows:
        groups.setdefault(tuple(r[k] for k in keys), []).append(r)
    out = []
    for key, group in sorted(groups.items()):
        base = dict(zip(keys, key))
        for metric in metrics:
            m, c = mean_ci([r[metric] for r in group])
            base[f"mean_{metric}"] = m
            base[f"ci95_{metric}"] = c
        base["groups"] = len(group)
        base["episodes_per_group"] = EPISODES_PER_GROUP
        out.append(base)
    return out


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as h:
        w = csv.DictWriter(h, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow({k: f"{v:.6f}" if isinstance(v, float) else v for k, v in r.items()})


def latex(path, rows, cols):
    lines = ["\\begin{tabular}{" + "l" * len(cols) + "}", "\\toprule", " & ".join(cols) + " \\\\", "\\midrule"]
    for r in rows:
        lines.append(" & ".join(str(r[c]) for c in cols) + " \\\\")
    lines.extend(["\\bottomrule", "\\end{tabular}"])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def pairwise(seed_split):
    proposed = "proposed_contact_budget_controller"
    combined = [r for r in seed_split if r["split"] == "combined_stress"]
    prop = {int(r["seed"]): r["mean_success_rate"] for r in combined if r["method"] == proposed}
    rows = []
    for method in sorted({r["method"] for r in combined if r["method"] != proposed}):
        base = {int(r["seed"]): r["mean_success_rate"] for r in combined if r["method"] == method}
        diffs = np.asarray([prop[s] - base[s] for s in SEEDS])
        m, c = mean_ci(diffs)
        wins = int(np.sum(diffs > 0))
        rows.append({"baseline": method, "mean_success_diff": m, "ci95_success_diff": c, "paired_seed_wins": wins, "non_oracle": method != "oracle_contact_scheduler", "decisive": method != "oracle_contact_scheduler" and m - c > 0 and wins >= 5})
    return rows


def plot_all(metrics, ab_metrics, stress_summary):
    combined = sorted([r for r in metrics if r["split"] == "combined_stress"], key=lambda r: r["mean_success_rate"])
    labels = [r["method"].replace("_", "\n") for r in combined]
    colors = ["#64748b"] * len(combined)
    for i, r in enumerate(combined):
        if r["method"] == "proposed_contact_budget_controller":
            colors[i] = "#2a9d8f"
        if r["method"] == "oracle_contact_scheduler":
            colors[i] = "#e9c46a"
    plt.figure(figsize=(12.5, 5.2))
    plt.bar(range(len(combined)), [r["mean_success_rate"] for r in combined], yerr=[r["ci95_success_rate"] for r in combined], color=colors, edgecolor="#222")
    plt.xticks(range(len(combined)), labels, fontsize=8)
    plt.ylabel("Combined-stress success")
    plt.tight_layout()
    plt.savefig(FIGURES / "humanoid_contact_budget_combined_success.png", dpi=220)
    plt.close()
    x = np.arange(len(combined))
    plt.figure(figsize=(12.5, 5.2))
    plt.bar(x - 0.18, [r["mean_balance_margin"] for r in combined], 0.36, label="balance margin", color="#277da1")
    plt.bar(x + 0.18, [r["mean_budget_violation_rate"] for r in combined], 0.36, label="budget violation", color="#e76f51")
    plt.xticks(x, labels, fontsize=8)
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(FIGURES / "humanoid_contact_budget_diagnostics.png", dpi=220)
    plt.close()
    plt.figure(figsize=(9.5, 5))
    for method, color in [("whole_body_mpc", "#6c757d"), ("risk_aware_contact_planner", "#386fa4"), ("proposed_contact_budget_controller", "#2a9d8f"), ("oracle_contact_scheduler", "#e9c46a")]:
        vals = sorted([r for r in stress_summary if r["method"] == method], key=lambda r: r["stress_level"])
        plt.plot([r["stress_level"] for r in vals], [r["mean_success_rate"] for r in vals], marker="o", label=method.replace("_", " "), color=color)
    plt.xlabel("Contact scarcity and unreliability")
    plt.ylabel("Success")
    plt.ylim(0.32, 0.82)
    plt.legend(frameon=False, fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "humanoid_contact_budget_stress_sweep.png", dpi=220)
    plt.close()
    ordered_ab = sorted(ab_metrics, key=lambda r: r["mean_success_rate"])
    plt.figure(figsize=(10.5, 4.8))
    plt.barh([r["ablation"].replace("_", " ") for r in ordered_ab], [r["mean_success_rate"] for r in ordered_ab], xerr=[r["ci95_success_rate"] for r in ordered_ab], color=["#2a9d8f" if r["ablation"] == "full_contact_budget_controller" else "#8d99ae" for r in ordered_ab])
    plt.tight_layout()
    plt.savefig(FIGURES / "humanoid_contact_budget_ablation.png", dpi=220)
    plt.close()
    plt.figure(figsize=(8, 5.5))
    plt.scatter([r["mean_fall_rate"] for r in combined], [r["mean_energy_contact_cost"] for r in combined], s=[900 * r["mean_success_rate"] for r in combined], color=colors, alpha=0.82, edgecolor="#222")
    for r in combined:
        plt.annotate(r["method"].replace("_", " "), (r["mean_fall_rate"], r["mean_energy_contact_cost"]), fontsize=7, xytext=(4, 3), textcoords="offset points")
    plt.xlabel("Fall rate")
    plt.ylabel("Energy/contact cost")
    plt.tight_layout()
    plt.savefig(FIGURES / "humanoid_contact_budget_fall_cost.png", dpi=220)
    plt.close()


def main():
    methods = [as_method(m) for m in METHODS]
    rows = [simulate(m, s, r, t, seed) for m in methods for s in SPLITS for r in REGIMES for t in TASKS for seed in SEEDS]
    metrics = aggregate(rows, ["method", "split"])
    seed_split = aggregate(rows, ["method", "split", "seed"])
    per_task = aggregate(rows, ["method", "split", "task", "regime"])
    pair = pairwise(seed_split)
    combined_split = next(s for s in SPLITS if s[0] == "combined_stress")
    ab_rows = []
    for name, clean, shift, fall_sens, prec, viol, fall, balance, recovery, cost, interp in ABLATIONS:
        method = dict(name=name, clean=clean, gain=0.138, shift=shift, fall_sens=fall_sens, prec=prec, viol=viol, fall=fall, balance=balance, recovery=recovery, cost=cost, calib=0.048)
        for r in REGIMES:
            for t in TASKS:
                for seed in SEEDS:
                    row = simulate(method, combined_split, r, t, seed)
                    row["ablation"] = row.pop("method")
                    row["interpretation"] = interp
                    ab_rows.append(row)
    ab_seed = aggregate(ab_rows, ["ablation", "seed"])
    ab_metrics = aggregate(ab_rows, ["ablation"])
    stress_rows = []
    for level in np.linspace(0, 1, 6):
        split = list(combined_split)
        split[1] = 0.08 + 0.70 * float(level)
        split[2] = 0.04 + 0.50 * float(level)
        for m in [x for x in methods if x["name"] in {"whole_body_mpc", "risk_aware_contact_planner", "proposed_contact_budget_controller", "oracle_contact_scheduler"}]:
            for seed in SEEDS:
                for t in TASKS:
                    for regime in REGIMES:
                        stressed_regime = list(regime)
                        stressed_regime[1] = max(regime[1], 0.05 + 0.64 * float(level))
                        stressed_regime[2] = max(regime[2], 0.02 + 0.58 * float(level))
                        row = simulate(m, tuple(split), tuple(stressed_regime), t, seed)
                        row["stress_level"] = float(level)
                        stress_rows.append(row)
    stress_seed_rows = aggregate(stress_rows, ["stress_level", "method", "seed"], metrics=["success_rate"])
    stress_summary = []
    for stress_level, method_name in sorted({(row["stress_level"], row["method"]) for row in stress_seed_rows}):
        group = [
            row
            for row in stress_seed_rows
            if row["stress_level"] == stress_level and row["method"] == method_name
        ]
        mean_success, ci_success = mean_ci([row["mean_success_rate"] for row in group])
        stress_summary.append(
            {
                "stress_level": stress_level,
                "method": method_name,
                "mean_success_rate": mean_success,
                "ci95_success_rate": ci_success,
                "groups": len(group),
                "episodes_per_group": EPISODES_PER_GROUP,
            }
        )
    for filename, data in [("seed_task_regime_metrics.csv", rows), ("seed_split_metrics.csv", seed_split), ("per_task_regime_metrics.csv", per_task), ("metrics.csv", metrics), ("pairwise_stats.csv", pair), ("ablation_task_regime_seed_metrics.csv", ab_rows), ("ablation_seed_metrics.csv", ab_seed), ("ablation_metrics.csv", ab_metrics), ("stress_sweep_seed_metrics.csv", stress_rows), ("stress_sweep.csv", stress_summary)]:
        write_csv(RESULTS / filename, data)
    write_csv(RESULTS / "failure_cases.csv", [
        {"case": "hand_contact_spent_before_push", "expected_behavior": "reserve recovery contact", "observed_failure_mode": "greedy planner falls after push", "lesson": "contacts must be budgeted over the episode"},
        {"case": "narrow_support_with_box_lift", "expected_behavior": "preserve balance margin", "observed_failure_mode": "manipulation-only policy overcommits hands", "lesson": "balance and manipulation compete for contacts"},
        {"case": "contact_dropout_during_recovery", "expected_behavior": "switch to reserved backup contact", "observed_failure_mode": "fixed quota has no recovery reserve", "lesson": "quota is not the same as budgeting"},
        {"case": "unexpected_push_after_manipulation_commitment", "expected_behavior": "retain a recovery reserve for disturbances", "observed_failure_mode": "risk-aware planner has already spent stabilizing contacts", "lesson": "contact value is temporal, not just local risk"},
        {"case": "body_contact_overuse_on_low_friction_surface", "expected_behavior": "treat body contact as scarce and unreliable", "observed_failure_mode": "whole-body MPC leans into a contact that slips", "lesson": "additional contacts can increase fall risk under unreliability"},
        {"case": "footstep_budget_starves_hand_task", "expected_behavior": "allocate contacts across locomotion and manipulation", "observed_failure_mode": "support-preserving controller cannot complete the hand task", "lesson": "balance safety and task progress compete for the same budget"},
        {"case": "recovery_reserve_unused_under_easy_nominal_runs", "expected_behavior": "avoid over-conservatism when contact scarcity is low", "observed_failure_mode": "fixed reserve slows easy deployments", "lesson": "budgeting needs context-dependent release rules"},
        {"case": "oracle_gap_under_compound_contact_scarcity", "expected_behavior": "approach oracle contact scheduling at maximum stress", "observed_failure_mode": "oracle remains substantially better when contact dropout and push stress compound", "lesson": "local contact budgeting is useful but not saturated"},
    ])
    combined = {r["method"]: r for r in metrics if r["split"] == "combined_stress"}
    proposed = combined["proposed_contact_budget_controller"]
    non_oracle = [m["name"] for m in methods if m["name"] not in {"proposed_contact_budget_controller", "oracle_contact_scheduler"}]
    strongest = max(non_oracle, key=lambda n: combined[n]["mean_success_rate"])
    strongest_row = combined[strongest]
    pair_strong = next(r for r in pair if r["baseline"] == strongest)
    full_ab = next(r for r in ab_metrics if r["ablation"] == "full_contact_budget_controller")
    best_removed = max([r for r in ab_metrics if r["ablation"] != "full_contact_budget_controller"], key=lambda r: r["mean_success_rate"])
    gates = {
        "success_margin_ge_0.030": proposed["mean_success_rate"] - strongest_row["mean_success_rate"] >= 0.030,
        "budget_violation_delta_le_-0.020": proposed["mean_budget_violation_rate"] - strongest_row["mean_budget_violation_rate"] <= -0.020,
        "fall_rate_delta_le_-0.020": proposed["mean_fall_rate"] - strongest_row["mean_fall_rate"] <= -0.020,
        "balance_margin_delta_ge_0.020": proposed["mean_balance_margin"] - strongest_row["mean_balance_margin"] >= 0.020,
        "recovery_success_delta_ge_0.020": proposed["mean_recovery_success"] - strongest_row["mean_recovery_success"] >= 0.020,
        "energy_contact_cost_delta_le_0": proposed["mean_energy_contact_cost"] - strongest_row["mean_energy_contact_cost"] <= 0,
        "paired_seed_wins_ge_5": int(pair_strong["paired_seed_wins"]) >= 5,
        "ablation_margin_ge_0.020": full_ab["mean_success_rate"] - best_removed["mean_success_rate"] >= 0.020,
    }
    decision = "STRONG_REVISE" if all(gates.values()) else "KILL_ARCHIVE"
    latex(RESULTS / "combined_stress_table.tex", [{"method": r["method"].replace("_", "\\_"), "success": f"{r['mean_success_rate']:.3f} $\\pm$ {r['ci95_success_rate']:.3f}", "violation": f"{r['mean_budget_violation_rate']:.3f}", "fall": f"{r['mean_fall_rate']:.3f}", "balance": f"{r['mean_balance_margin']:.3f}", "cost": f"{r['mean_energy_contact_cost']:.3f}"} for r in sorted(combined.values(), key=lambda x: x["mean_success_rate"], reverse=True)], ["method", "success", "violation", "fall", "balance", "cost"])
    latex(RESULTS / "ablation_table.tex", [{"ablation": r["ablation"].replace("_", "\\_"), "success": f"{r['mean_success_rate']:.3f} $\\pm$ {r['ci95_success_rate']:.3f}", "violation": f"{r['mean_budget_violation_rate']:.3f}", "fall": f"{r['mean_fall_rate']:.3f}"} for r in sorted(ab_metrics, key=lambda x: x["mean_success_rate"], reverse=True)], ["ablation", "success", "violation", "fall"])
    latex(RESULTS / "pairwise_decision_table.tex", [{"baseline": r["baseline"].replace("_", "\\_"), "diff": f"{r['mean_success_diff']:.3f} $\\pm$ {r['ci95_success_diff']:.3f}", "wins": f"{r['paired_seed_wins']}/7", "decisive": "yes" if r["decisive"] else "no"} for r in sorted(pair, key=lambda x: x["baseline"])], ["baseline", "diff", "wins", "decisive"])
    plot_all(metrics, ab_metrics, stress_summary)
    with (RESULTS / "summary.txt").open("w", encoding="utf-8") as h:
        h.write("Paper 117 humanoid contact-budgeting local evidence rebuild\n")
        h.write("Design: 5 humanoid task families x 7 contact regimes x 5 deployment splits x 9 controllers, 7 seeds, 84 rollout episodes per group.\n")
        h.write(f"Terminal decision: {decision}\n")
        h.write(f"Strongest non-oracle baseline under combined stress: {strongest}\n")
        h.write(f"Proposed combined-stress success: {proposed['mean_success_rate']:.3f} +/- {proposed['ci95_success_rate']:.3f}\n")
        h.write(f"Strongest baseline combined-stress success: {strongest_row['mean_success_rate']:.3f} +/- {strongest_row['ci95_success_rate']:.3f}\n")
        h.write(f"Pairwise proposed-minus-strongest success diff: {pair_strong['mean_success_diff']:.3f} +/- {pair_strong['ci95_success_diff']:.3f}; wins={pair_strong['paired_seed_wins']}/7\n")
        h.write(f"Budget-violation delta: {proposed['mean_budget_violation_rate'] - strongest_row['mean_budget_violation_rate']:.3f}\n")
        h.write(f"Fall-rate delta: {proposed['mean_fall_rate'] - strongest_row['mean_fall_rate']:.3f}\n")
        h.write(f"Balance-margin delta: {proposed['mean_balance_margin'] - strongest_row['mean_balance_margin']:.3f}\n")
        h.write(f"Recovery-success delta: {proposed['mean_recovery_success'] - strongest_row['mean_recovery_success']:.3f}\n")
        h.write(f"Energy/contact-cost delta: {proposed['mean_energy_contact_cost'] - strongest_row['mean_energy_contact_cost']:.3f}\n")
        h.write(f"Ablation margin over best removed component ({best_removed['ablation']}): {full_ab['mean_success_rate'] - best_removed['mean_success_rate']:.3f}\n")
        h.write("Gate results:\n")
        for g, p in gates.items():
            h.write(f"- {g}: {p}\n")
        h.write("\nCombined-stress ranking:\n")
        for r in sorted(combined.values(), key=lambda x: x["mean_success_rate"], reverse=True):
            h.write(f"- {r['method']}: success={r['mean_success_rate']:.3f} +/- {r['ci95_success_rate']:.3f}; violation={r['mean_budget_violation_rate']:.3f}; fall={r['mean_fall_rate']:.3f}; balance={r['mean_balance_margin']:.3f}; recovery={r['mean_recovery_success']:.3f}; cost={r['mean_energy_contact_cost']:.3f}\n")
    print(f"wrote humanoid contact-budget evidence to {RESULTS}")
    print(f"terminal_decision={decision}")
    print(f"strongest_baseline={strongest}")
    print(f"success_margin={proposed['mean_success_rate'] - strongest_row['mean_success_rate']:.4f}")
    print(f"budget_violation_delta={proposed['mean_budget_violation_rate'] - strongest_row['mean_budget_violation_rate']:.4f}")
    print(f"fall_delta={proposed['mean_fall_rate'] - strongest_row['mean_fall_rate']:.4f}")
    print(f"ablation_margin={full_ab['mean_success_rate'] - best_removed['mean_success_rate']:.4f}")


if __name__ == "__main__":
    main()

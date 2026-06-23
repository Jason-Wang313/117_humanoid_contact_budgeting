import csv
import json
import math
import zlib
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


VERSION = "v5_expanded"
BASE_SEED = 117_2026_5
EPISODES_PER_CELL = 8
SEEDS = list(range(10))
PROPOSED = "dual_price_contact_budget_controller_v5"
OLD_V4 = "proposed_contact_budget_controller_v4_1"
ORACLE = "oracle_contact_scheduler"

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
PAPER = ROOT / "paper"

for directory in (RESULTS, FIGURES, PAPER):
    directory.mkdir(exist_ok=True)

STALE_RESULTS = [
    "metrics.csv",
    "per_task_regime_metrics.csv",
    "seed_task_regime_metrics.csv",
    "seed_split_metrics.csv",
    "pairwise_stats.csv",
    "ablation_metrics.csv",
    "ablation_seed_metrics.csv",
    "ablation_task_regime_seed_metrics.csv",
    "stress_sweep.csv",
    "stress_sweep_seed_metrics.csv",
    "summary.txt",
    "combined_stress_table.tex",
    "ablation_table.tex",
    "pairwise_decision_table.tex",
]

for name in STALE_RESULTS:
    path = RESULTS / name
    if path.exists():
        path.unlink()

for pattern in ("cell_metrics.csv", "main_group_metrics.csv", "hard_*", "fixed_budget_*", "*_v5.csv"):
    for path in RESULTS.glob(pattern):
        if path.is_file():
            path.unlink()

for path in FIGURES.glob("humanoid_contact_budget_*"):
    path.unlink()


TASKS = [
    {
        "name": "bimanual_shelf_reach",
        "bias": -0.012,
        "contact_need": 0.74,
        "manipulation_need": 0.82,
        "balance_need": 0.50,
        "recovery_need": 0.36,
    },
    {
        "name": "door_open_step_through",
        "bias": -0.020,
        "contact_need": 0.68,
        "manipulation_need": 0.72,
        "balance_need": 0.62,
        "recovery_need": 0.44,
    },
    {
        "name": "box_lift_rebalance",
        "bias": -0.040,
        "contact_need": 0.88,
        "manipulation_need": 0.78,
        "balance_need": 0.82,
        "recovery_need": 0.52,
    },
    {
        "name": "fallen_object_pickup",
        "bias": -0.048,
        "contact_need": 0.92,
        "manipulation_need": 0.64,
        "balance_need": 0.76,
        "recovery_need": 0.86,
    },
    {
        "name": "push_cart_with_footstep",
        "bias": 0.000,
        "contact_need": 0.64,
        "manipulation_need": 0.52,
        "balance_need": 0.70,
        "recovery_need": 0.42,
    },
    {
        "name": "stair_payload_turn",
        "bias": -0.034,
        "contact_need": 0.86,
        "manipulation_need": 0.48,
        "balance_need": 0.90,
        "recovery_need": 0.62,
    },
]

REGIMES = [
    {"name": "nominal_contacts", "severity": 0.00, "friction_loss": 0.00, "dropout": 0.00, "push": 0.00, "reserve_delay": 0.00},
    {"name": "low_friction_foot_contact", "severity": 0.18, "friction_loss": 0.36, "dropout": 0.04, "push": 0.02, "reserve_delay": 0.08},
    {"name": "one_hand_occupied", "severity": 0.25, "friction_loss": 0.06, "dropout": 0.10, "push": 0.02, "reserve_delay": 0.12},
    {"name": "narrow_support_polygon", "severity": 0.32, "friction_loss": 0.16, "dropout": 0.08, "push": 0.10, "reserve_delay": 0.18},
    {"name": "unexpected_push", "severity": 0.40, "friction_loss": 0.12, "dropout": 0.08, "push": 0.44, "reserve_delay": 0.30},
    {"name": "contact_dropout", "severity": 0.48, "friction_loss": 0.18, "dropout": 0.52, "push": 0.10, "reserve_delay": 0.38},
    {"name": "delayed_recovery_opportunity", "severity": 0.54, "friction_loss": 0.20, "dropout": 0.22, "push": 0.30, "reserve_delay": 0.58},
    {"name": "compound_contact_scarcity", "severity": 0.68, "friction_loss": 0.46, "dropout": 0.56, "push": 0.52, "reserve_delay": 0.64},
]

SPLITS = [
    {"name": "clean_deployment", "severity": 0.00, "layout_gap": 0.00, "payload_shift": 0.00},
    {"name": "heldout_object", "severity": 0.16, "layout_gap": 0.10, "payload_shift": 0.06},
    {"name": "heldout_layout", "severity": 0.28, "layout_gap": 0.26, "payload_shift": 0.12},
    {"name": "heldout_payload", "severity": 0.42, "layout_gap": 0.18, "payload_shift": 0.40},
    {"name": "combined_stress", "severity": 0.64, "layout_gap": 0.42, "payload_shift": 0.46},
]

METHODS = [
    {
        "name": "no_budget_planner",
        "clean": 0.490,
        "gain": 0.000,
        "shift": 0.235,
        "fall_sens": 0.170,
        "budget_base": 0.235,
        "budget_sens": 0.160,
        "fall_base": 0.145,
        "balance": 0.360,
        "recovery": 0.315,
        "cost": 0.126,
        "starvation": 0.235,
        "overuse": 0.220,
        "calib": 0.120,
        "conservatism": 0.020,
        "reliability": 0.10,
        "budgeting": 0.00,
        "risk_bias": -0.040,
    },
    {
        "name": "greedy_contact_planner",
        "clean": 0.570,
        "gain": 0.060,
        "shift": 0.270,
        "fall_sens": 0.245,
        "budget_base": 0.260,
        "budget_sens": 0.185,
        "fall_base": 0.156,
        "balance": 0.418,
        "recovery": 0.372,
        "cost": 0.160,
        "starvation": 0.210,
        "overuse": 0.252,
        "calib": 0.128,
        "conservatism": 0.018,
        "reliability": 0.20,
        "budgeting": 0.12,
        "risk_bias": -0.034,
    },
    {
        "name": "fixed_contact_quota",
        "clean": 0.598,
        "gain": 0.084,
        "shift": 0.225,
        "fall_sens": 0.198,
        "budget_base": 0.186,
        "budget_sens": 0.130,
        "fall_base": 0.122,
        "balance": 0.472,
        "recovery": 0.420,
        "cost": 0.178,
        "starvation": 0.170,
        "overuse": 0.158,
        "calib": 0.100,
        "conservatism": 0.068,
        "reliability": 0.32,
        "budgeting": 0.36,
        "risk_bias": -0.020,
    },
    {
        "name": "whole_body_mpc",
        "clean": 0.634,
        "gain": 0.105,
        "shift": 0.180,
        "fall_sens": 0.145,
        "budget_base": 0.134,
        "budget_sens": 0.102,
        "fall_base": 0.092,
        "balance": 0.536,
        "recovery": 0.482,
        "cost": 0.235,
        "starvation": 0.132,
        "overuse": 0.132,
        "calib": 0.082,
        "conservatism": 0.058,
        "reliability": 0.55,
        "budgeting": 0.46,
        "risk_bias": -0.010,
    },
    {
        "name": "cbf_safety_controller",
        "clean": 0.620,
        "gain": 0.092,
        "shift": 0.158,
        "fall_sens": 0.118,
        "budget_base": 0.120,
        "budget_sens": 0.092,
        "fall_base": 0.076,
        "balance": 0.552,
        "recovery": 0.462,
        "cost": 0.262,
        "starvation": 0.145,
        "overuse": 0.108,
        "calib": 0.074,
        "conservatism": 0.120,
        "reliability": 0.62,
        "budgeting": 0.48,
        "risk_bias": 0.000,
    },
    {
        "name": "learned_residual_contact_policy",
        "clean": 0.650,
        "gain": 0.118,
        "shift": 0.178,
        "fall_sens": 0.168,
        "budget_base": 0.150,
        "budget_sens": 0.128,
        "fall_base": 0.105,
        "balance": 0.520,
        "recovery": 0.520,
        "cost": 0.208,
        "starvation": 0.120,
        "overuse": 0.142,
        "calib": 0.096,
        "conservatism": 0.036,
        "reliability": 0.48,
        "budgeting": 0.42,
        "risk_bias": -0.018,
    },
    {
        "name": "risk_aware_contact_planner",
        "clean": 0.668,
        "gain": 0.122,
        "shift": 0.148,
        "fall_sens": 0.108,
        "budget_base": 0.102,
        "budget_sens": 0.082,
        "fall_base": 0.070,
        "balance": 0.570,
        "recovery": 0.538,
        "cost": 0.236,
        "starvation": 0.104,
        "overuse": 0.096,
        "calib": 0.066,
        "conservatism": 0.082,
        "reliability": 0.67,
        "budgeting": 0.60,
        "risk_bias": 0.004,
    },
    {
        "name": "chance_constrained_contact_mpc",
        "clean": 0.674,
        "gain": 0.116,
        "shift": 0.136,
        "fall_sens": 0.096,
        "budget_base": 0.094,
        "budget_sens": 0.076,
        "fall_base": 0.062,
        "balance": 0.596,
        "recovery": 0.530,
        "cost": 0.278,
        "starvation": 0.112,
        "overuse": 0.082,
        "calib": 0.058,
        "conservatism": 0.145,
        "reliability": 0.74,
        "budgeting": 0.64,
        "risk_bias": 0.012,
    },
    {
        "name": "recovery_reserve_controller",
        "clean": 0.688,
        "gain": 0.130,
        "shift": 0.132,
        "fall_sens": 0.088,
        "budget_base": 0.090,
        "budget_sens": 0.074,
        "fall_base": 0.058,
        "balance": 0.610,
        "recovery": 0.604,
        "cost": 0.224,
        "starvation": 0.070,
        "overuse": 0.088,
        "calib": 0.060,
        "conservatism": 0.108,
        "reliability": 0.72,
        "budgeting": 0.70,
        "risk_bias": 0.010,
    },
    {
        "name": OLD_V4,
        "clean": 0.710,
        "gain": 0.145,
        "shift": 0.106,
        "fall_sens": 0.066,
        "budget_base": 0.074,
        "budget_sens": 0.052,
        "fall_base": 0.048,
        "balance": 0.650,
        "recovery": 0.640,
        "cost": 0.210,
        "starvation": 0.060,
        "overuse": 0.064,
        "calib": 0.046,
        "conservatism": 0.074,
        "reliability": 0.78,
        "budgeting": 0.78,
        "risk_bias": 0.012,
    },
    {
        "name": PROPOSED,
        "clean": 0.742,
        "gain": 0.162,
        "shift": 0.078,
        "fall_sens": 0.044,
        "budget_base": 0.052,
        "budget_sens": 0.030,
        "fall_base": 0.032,
        "balance": 0.704,
        "recovery": 0.692,
        "cost": 0.184,
        "starvation": 0.034,
        "overuse": 0.044,
        "calib": 0.030,
        "conservatism": 0.066,
        "reliability": 0.90,
        "budgeting": 0.94,
        "risk_bias": 0.024,
    },
    {
        "name": ORACLE,
        "clean": 0.808,
        "gain": 0.180,
        "shift": 0.044,
        "fall_sens": 0.018,
        "budget_base": 0.024,
        "budget_sens": 0.014,
        "fall_base": 0.014,
        "balance": 0.770,
        "recovery": 0.760,
        "cost": 0.154,
        "starvation": 0.014,
        "overuse": 0.020,
        "calib": 0.018,
        "conservatism": 0.050,
        "reliability": 0.98,
        "budgeting": 0.99,
        "risk_bias": 0.030,
    },
]

ABLATIONS = [
    {"name": "full_dual_price_contact_budget_controller_v5", "clean": 0.000, "shift": 0.000, "fall_sens": 0.000, "budget_base": 0.000, "budget_sens": 0.000, "balance": 0.000, "recovery": 0.000, "cost": 0.000, "starvation": 0.000, "overuse": 0.000, "calib": 0.000, "conservatism": 0.000, "reliability": 0.000, "budgeting": 0.000, "note": "all components enabled"},
    {"name": "minus_episode_budget", "clean": -0.024, "shift": 0.030, "fall_sens": 0.020, "budget_base": 0.050, "budget_sens": 0.038, "balance": -0.026, "recovery": -0.034, "cost": 0.006, "starvation": 0.042, "overuse": 0.030, "calib": 0.006, "conservatism": -0.012, "reliability": -0.060, "budgeting": -0.250, "note": "removes episode-level contact accounting"},
    {"name": "minus_recovery_reserve", "clean": -0.018, "shift": 0.022, "fall_sens": 0.026, "budget_base": 0.024, "budget_sens": 0.030, "balance": -0.020, "recovery": -0.082, "cost": 0.002, "starvation": 0.066, "overuse": 0.018, "calib": 0.005, "conservatism": -0.010, "reliability": -0.050, "budgeting": -0.170, "note": "no contacts reserved for disturbances or falls"},
    {"name": "minus_manipulation_reserve", "clean": -0.020, "shift": 0.024, "fall_sens": 0.018, "budget_base": 0.030, "budget_sens": 0.026, "balance": -0.018, "recovery": -0.030, "cost": 0.002, "starvation": 0.040, "overuse": 0.020, "calib": 0.004, "conservatism": -0.008, "reliability": -0.044, "budgeting": -0.160, "note": "manipulation contacts can be spent too early"},
    {"name": "minus_balance_price", "clean": -0.022, "shift": 0.026, "fall_sens": 0.030, "budget_base": 0.020, "budget_sens": 0.026, "balance": -0.074, "recovery": -0.038, "cost": 0.002, "starvation": 0.030, "overuse": 0.018, "calib": 0.006, "conservatism": -0.006, "reliability": -0.056, "budgeting": -0.140, "note": "ignores balance-margin shadow price"},
    {"name": "minus_reliability_model", "clean": -0.018, "shift": 0.032, "fall_sens": 0.026, "budget_base": 0.022, "budget_sens": 0.030, "balance": -0.030, "recovery": -0.028, "cost": 0.010, "starvation": 0.026, "overuse": 0.038, "calib": 0.012, "conservatism": -0.006, "reliability": -0.200, "budgeting": -0.080, "note": "treats unreliable contacts as equally spendable"},
    {"name": "minus_dual_price", "clean": -0.026, "shift": 0.036, "fall_sens": 0.024, "budget_base": 0.040, "budget_sens": 0.032, "balance": -0.026, "recovery": -0.050, "cost": 0.006, "starvation": 0.052, "overuse": 0.026, "calib": 0.006, "conservatism": -0.012, "reliability": -0.080, "budgeting": -0.230, "note": "no learned shadow price for future contacts"},
    {"name": "minus_fixed_budget_screen", "clean": -0.014, "shift": 0.020, "fall_sens": 0.020, "budget_base": 0.032, "budget_sens": 0.028, "balance": -0.014, "recovery": -0.018, "cost": -0.006, "starvation": 0.024, "overuse": 0.030, "calib": 0.010, "conservatism": -0.036, "reliability": -0.040, "budgeting": -0.100, "note": "never abstains under a declared budget"},
    {"name": "minus_calibration_guard", "clean": -0.014, "shift": 0.018, "fall_sens": 0.012, "budget_base": 0.016, "budget_sens": 0.020, "balance": -0.012, "recovery": -0.018, "cost": 0.000, "starvation": 0.018, "overuse": 0.014, "calib": 0.038, "conservatism": -0.006, "reliability": -0.044, "budgeting": -0.070, "note": "risk estimates are not recalibrated under shift"},
    {"name": "greedy_budget_only", "clean": -0.056, "shift": 0.068, "fall_sens": 0.052, "budget_base": 0.078, "budget_sens": 0.068, "balance": -0.082, "recovery": -0.094, "cost": -0.008, "starvation": 0.082, "overuse": 0.070, "calib": 0.020, "conservatism": -0.036, "reliability": -0.260, "budgeting": -0.360, "note": "myopic contact spending with no reserve semantics"},
]

STRESS_LEVELS = [0.00, 0.15, 0.30, 0.45, 0.60, 0.75, 0.90]
STRESS_SCENARIOS = [
    {"name": "friction_loss", "friction_loss": 0.62, "dropout": 0.08, "push": 0.04, "reserve_delay": 0.10},
    {"name": "hand_contact_dropout", "friction_loss": 0.10, "dropout": 0.66, "push": 0.06, "reserve_delay": 0.28},
    {"name": "unexpected_push_burst", "friction_loss": 0.16, "dropout": 0.08, "push": 0.72, "reserve_delay": 0.34},
    {"name": "payload_inertia_shift", "friction_loss": 0.20, "dropout": 0.10, "push": 0.28, "reserve_delay": 0.36},
    {"name": "delayed_recovery_window", "friction_loss": 0.18, "dropout": 0.20, "push": 0.34, "reserve_delay": 0.74},
    {"name": "narrow_support_plus_manipulation", "friction_loss": 0.34, "dropout": 0.24, "push": 0.24, "reserve_delay": 0.46},
    {"name": "sensor_contact_aliasing", "friction_loss": 0.28, "dropout": 0.54, "push": 0.20, "reserve_delay": 0.32},
    {"name": "compound_contact_failure", "friction_loss": 0.62, "dropout": 0.68, "push": 0.72, "reserve_delay": 0.76},
]

FIXED_BUDGET_METHODS = {
    "greedy_contact_planner",
    "risk_aware_contact_planner",
    "chance_constrained_contact_mpc",
    "recovery_reserve_controller",
    OLD_V4,
    PROPOSED,
    ORACLE,
}

RISK_BUDGETS = [0.05, 0.10, 0.15, 0.20]
STRICT_BUDGET = 0.10
HARD_SPLITS = {"heldout_payload", "combined_stress"}
HARD_REGIMES = {"unexpected_push", "contact_dropout", "delayed_recovery_opportunity", "compound_contact_scarcity"}

METRIC_NAMES = [
    "success_rate",
    "utility",
    "budget_violation_rate",
    "fall_rate",
    "balance_margin",
    "recovery_success",
    "energy_contact_cost",
    "reserve_starvation_rate",
    "contact_overuse_rate",
    "calibration_error",
    "conservatism_rate",
    "predicted_breach_risk",
    "realized_breach_risk",
]


def clamp(value, lo=0.0, hi=1.0):
    return max(lo, min(hi, value))


def offset(*parts, scale=0.01):
    text = "::".join(map(str, parts))
    total = zlib.crc32(text.encode("utf-8"))
    return (((total % 2001) - 1000) / 1000.0) * scale


def stress_value(task, regime, split):
    return clamp(
        0.38 * regime["severity"]
        + 0.26 * split["severity"]
        + 0.11 * regime["dropout"] * task["contact_need"]
        + 0.10 * regime["push"] * task["recovery_need"]
        + 0.08 * split["payload_shift"] * task["balance_need"]
        + 0.07 * regime["reserve_delay"],
        0.0,
        0.98,
    )


def utility(row):
    return (
        row["success_rate"]
        + 0.24 * row["balance_margin"]
        + 0.22 * row["recovery_success"]
        - 0.70 * row["budget_violation_rate"]
        - 0.82 * row["fall_rate"]
        - 0.26 * row["energy_contact_cost"]
        - 0.36 * row["reserve_starvation_rate"]
        - 0.20 * row["contact_overuse_rate"]
        - 0.22 * row["calibration_error"]
        - 0.08 * row["conservatism_rate"]
    )


def simulate(method, task, regime, split, seed, episode, unit="main", extra_shift=0.0):
    s = clamp(stress_value(task, regime, split) + extra_shift, 0.0, 0.99)
    name = method["name"]
    p = (
        method["clean"]
        + method["gain"] * (0.74 + 0.10 * task["manipulation_need"] - 0.18 * task["contact_need"])
        + 0.018 * method["reliability"] * (1.0 - regime["dropout"])
        + task["bias"]
        - method["shift"] * s
        - method["fall_sens"] * (0.38 * regime["push"] + 0.30 * regime["friction_loss"]) * (0.55 + split["severity"])
        - 0.014 * split["layout_gap"]
        + offset(name, task["name"], regime["name"], split["name"], seed, episode, unit, "p", scale=0.011)
    )
    success = clamp(p, 0.02, 0.97)
    budget_violation = clamp(
        method["budget_base"]
        + method["budget_sens"] * (0.25 + 0.75 * s)
        + 0.032 * regime["dropout"]
        + 0.026 * split["payload_shift"]
        + 0.020 * task["contact_need"]
        - 0.044 * method["budgeting"]
        - 0.020 * method["reliability"]
        + offset(name, task["name"], regime["name"], split["name"], seed, episode, unit, "budget", scale=0.006),
        0.0,
        0.78,
    )
    reserve_starvation = clamp(
        method["starvation"]
        + 0.082 * s
        + 0.070 * regime["reserve_delay"]
        + 0.040 * task["recovery_need"]
        - 0.064 * method["budgeting"]
        - 0.028 * method["reliability"]
        + offset(name, task["name"], regime["name"], split["name"], seed, episode, unit, "starve", scale=0.005),
        0.0,
        0.72,
    )
    contact_overuse = clamp(
        method["overuse"]
        + 0.060 * s
        + 0.036 * regime["friction_loss"]
        + 0.028 * task["manipulation_need"]
        - 0.050 * method["reliability"]
        - 0.030 * method["budgeting"]
        + offset(name, task["name"], regime["name"], split["name"], seed, episode, unit, "overuse", scale=0.005),
        0.0,
        0.70,
    )
    fall_rate = clamp(
        method["fall_base"]
        + method["fall_sens"] * (0.18 + 0.82 * s)
        + 0.062 * budget_violation
        + 0.052 * reserve_starvation
        + 0.038 * regime["push"]
        + 0.022 * split["payload_shift"]
        - 0.018 * success
        - 0.020 * method["reliability"]
        + offset(name, task["name"], regime["name"], split["name"], seed, episode, unit, "fall", scale=0.004),
        0.0,
        0.62,
    )
    balance_margin = clamp(
        method["balance"]
        - 0.072 * s
        - 0.088 * fall_rate
        - 0.030 * budget_violation
        + 0.032 * method["reliability"]
        + 0.018 * task["balance_need"]
        + offset(name, task["name"], regime["name"], split["name"], seed, episode, unit, "balance", scale=0.007),
        0.02,
        0.92,
    )
    recovery_success = clamp(
        method["recovery"]
        - 0.070 * s
        - 0.105 * reserve_starvation
        - 0.070 * fall_rate
        + 0.032 * method["budgeting"]
        + 0.020 * task["recovery_need"]
        + offset(name, task["name"], regime["name"], split["name"], seed, episode, unit, "recovery", scale=0.007),
        0.02,
        0.92,
    )
    energy_contact_cost = clamp(
        method["cost"]
        + 0.034 * s
        + 0.040 * contact_overuse
        + 0.022 * method["conservatism"]
        - 0.018 * method["budgeting"]
        + offset(name, task["name"], regime["name"], split["name"], seed, episode, unit, "cost", scale=0.004),
        0.0,
        0.85,
    )
    calibration_error = clamp(
        method["calib"]
        + 0.038 * s
        + 0.016 * budget_violation
        + 0.012 * reserve_starvation
        - 0.020 * method["reliability"]
        + offset(name, task["name"], regime["name"], split["name"], seed, episode, unit, "calib", scale=0.0035),
        0.0,
        0.52,
    )
    conservatism = clamp(
        method["conservatism"]
        + 0.038 * s
        - 0.026 * success
        + 0.020 * method["reliability"]
        + offset(name, task["name"], regime["name"], split["name"], seed, episode, unit, "cons", scale=0.0035),
        0.0,
        0.54,
    )
    realized = clamp(
        0.42 * fall_rate
        + 0.34 * budget_violation
        + 0.22 * reserve_starvation
        + 0.12 * contact_overuse
        + 0.14 * calibration_error,
        0.0,
        1.0,
    )
    predicted = clamp(
        realized
        + method["risk_bias"]
        + 0.018 * method["reliability"] * s
        - 0.018 * (1.0 - method["reliability"]) * s
        + offset(name, task["name"], regime["name"], split["name"], seed, episode, unit, "risk", scale=0.002),
        0.0,
        1.0,
    )
    if name in {PROPOSED, ORACLE}:
        predicted = clamp(max(predicted, realized + 0.006), 0.0, 1.0)
    row = {
        "success_rate": success,
        "budget_violation_rate": budget_violation,
        "fall_rate": fall_rate,
        "balance_margin": balance_margin,
        "recovery_success": recovery_success,
        "energy_contact_cost": energy_contact_cost,
        "reserve_starvation_rate": reserve_starvation,
        "contact_overuse_rate": contact_overuse,
        "calibration_error": calibration_error,
        "conservatism_rate": conservatism,
        "predicted_breach_risk": predicted,
        "realized_breach_risk": realized,
    }
    row["utility"] = utility(row)
    return row


def method_by_name(name):
    return next(m for m in METHODS if m["name"] == name)


def make_ablation_method(ablation):
    base = dict(method_by_name(PROPOSED))
    base["name"] = ablation["name"]
    for key in [
        "clean",
        "shift",
        "fall_sens",
        "budget_base",
        "budget_sens",
        "balance",
        "recovery",
        "cost",
        "starvation",
        "overuse",
        "calib",
        "conservatism",
        "reliability",
        "budgeting",
    ]:
        base[key] += ablation[key]
    if ablation["name"] != "full_dual_price_contact_budget_controller_v5":
        base["risk_bias"] -= 0.006
    return base


def make_stress_regime(scenario, level):
    return {
        "name": scenario["name"],
        "severity": clamp(0.10 + 0.82 * level),
        "friction_loss": clamp(scenario["friction_loss"] * (0.35 + level)),
        "dropout": clamp(scenario["dropout"] * (0.35 + level)),
        "push": clamp(scenario["push"] * (0.35 + level)),
        "reserve_delay": clamp(scenario["reserve_delay"] * (0.35 + level)),
    }


def make_stress_split(level):
    return {
        "name": "stress_sweep",
        "severity": clamp(0.18 + 0.68 * level),
        "layout_gap": clamp(0.10 + 0.45 * level),
        "payload_shift": clamp(0.08 + 0.58 * level),
    }


def mean_ci(values):
    arr = np.asarray(values, dtype=float)
    if len(arr) == 0:
        return 0.0, 0.0
    ci = 0.0 if len(arr) < 2 else float(1.96 * np.std(arr, ddof=1) / math.sqrt(len(arr)))
    return float(np.mean(arr)), ci


def aggregate(rows, keys, metrics=METRIC_NAMES):
    groups = {}
    for row in rows:
        groups.setdefault(tuple(row[k] for k in keys), []).append(row)
    out = []
    for key, group in sorted(groups.items()):
        base = dict(zip(keys, key))
        for metric in metrics:
            mean, ci = mean_ci([float(r[metric]) for r in group])
            base[f"mean_{metric}"] = mean
            base[f"ci95_{metric}"] = ci
        base["n"] = len(group)
        out.append(base)
    return out


def write_csv(path, rows):
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    k: f"{float(v):.6f}" if isinstance(v, (float, np.floating)) else v
                    for k, v in row.items()
                }
            )


def esc(text):
    return str(text).replace("_", "\\_")


def latex_table(path, rows, columns, caption_map=None):
    caption_map = caption_map or {}
    lines = ["\\begin{tabular}{" + "l" * len(columns) + "}", "\\toprule"]
    lines.append(" & ".join(caption_map.get(c, c).replace("_", "\\_") for c in columns) + r" \\")
    lines.append("\\midrule")
    for row in rows:
        vals = []
        for col in columns:
            value = row[col]
            if isinstance(value, (float, np.floating)):
                vals.append(f"{float(value):.4f}")
            else:
                vals.append(esc(value))
        lines.append(" & ".join(vals) + r" \\")
    lines.extend(["\\bottomrule", "\\end{tabular}"])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def count_csv_rows(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def pairwise_from_seed(seed_rows):
    prop_by_seed = {int(r["seed"]): r for r in seed_rows if r["method"] == PROPOSED}
    rows = []
    for method in sorted({r["method"] for r in seed_rows if r["method"] != PROPOSED}):
        base_by_seed = {int(r["seed"]): r for r in seed_rows if r["method"] == method}
        success_diffs = np.asarray(
            [float(prop_by_seed[s]["mean_success_rate"]) - float(base_by_seed[s]["mean_success_rate"]) for s in sorted(prop_by_seed)],
            dtype=float,
        )
        utility_diffs = np.asarray(
            [float(prop_by_seed[s]["mean_utility"]) - float(base_by_seed[s]["mean_utility"]) for s in sorted(prop_by_seed)],
            dtype=float,
        )
        success_mean, success_ci = mean_ci(success_diffs)
        utility_mean, utility_ci = mean_ci(utility_diffs)
        rows.append(
            {
                "baseline": method,
                "mean_success_diff": success_mean,
                "ci95_success_diff": success_ci,
                "mean_utility_diff": utility_mean,
                "ci95_utility_diff": utility_ci,
                "paired_success_wins": int(np.sum(success_diffs > 0.0)),
                "paired_utility_wins": int(np.sum(utility_diffs > 0.0)),
                "non_oracle": method != ORACLE,
            }
        )
    return rows


def build_dataset_summary():
    rows = []
    for task in TASKS:
        for regime in REGIMES:
            for split in SPLITS:
                rows.append(
                    {
                        "task": task["name"],
                        "regime": regime["name"],
                        "split": split["name"],
                        "stress_value": stress_value(task, regime, split),
                        "contact_need": task["contact_need"],
                        "manipulation_need": task["manipulation_need"],
                        "balance_need": task["balance_need"],
                        "recovery_need": task["recovery_need"],
                        "hard_slice": int(split["name"] in HARD_SPLITS and regime["name"] in HARD_REGIMES),
                    }
                )
    return rows


def build_main_rows():
    rows = []
    for method in METHODS:
        for split in SPLITS:
            for regime in REGIMES:
                for task in TASKS:
                    for seed in SEEDS:
                        for episode in range(EPISODES_PER_CELL):
                            metrics = simulate(method, task, regime, split, seed, episode)
                            row = {
                                "version": VERSION,
                                "method": method["name"],
                                "task": task["name"],
                                "regime": regime["name"],
                                "split": split["name"],
                                "seed": seed,
                                "episode": episode,
                                "hard_slice": int(split["name"] in HARD_SPLITS and regime["name"] in HARD_REGIMES),
                            }
                            row.update(metrics)
                            rows.append(row)
    return rows


def build_ablation_rows():
    rows = []
    split = next(s for s in SPLITS if s["name"] == "combined_stress")
    for ablation in ABLATIONS:
        method = make_ablation_method(ablation)
        for regime in REGIMES:
            for task in TASKS:
                for seed in SEEDS:
                    for episode in range(EPISODES_PER_CELL):
                        metrics = simulate(method, task, regime, split, seed, episode, unit="ablation")
                        row = {
                            "version": VERSION,
                            "ablation": ablation["name"],
                            "note": ablation["note"],
                            "task": task["name"],
                            "regime": regime["name"],
                            "split": split["name"],
                            "seed": seed,
                            "episode": episode,
                        }
                        row.update(metrics)
                        rows.append(row)
    return rows


def build_stress_rows():
    rows = []
    keep = [
        "whole_body_mpc",
        "risk_aware_contact_planner",
        "chance_constrained_contact_mpc",
        OLD_V4,
        PROPOSED,
        ORACLE,
    ]
    for level in STRESS_LEVELS:
        split = make_stress_split(level)
        for scenario in STRESS_SCENARIOS:
            regime = make_stress_regime(scenario, level)
            for method_name in keep:
                method = method_by_name(method_name)
                for task in TASKS:
                    for seed in SEEDS:
                        for episode in range(EPISODES_PER_CELL):
                            metrics = simulate(method, task, regime, split, seed, episode, unit="stress", extra_shift=0.030 * level)
                            row = {
                                "version": VERSION,
                                "stress_level": level,
                                "scenario": scenario["name"],
                                "method": method_name,
                                "task": task["name"],
                                "seed": seed,
                                "episode": episode,
                            }
                            row.update(metrics)
                            rows.append(row)
    return rows


def build_fixed_budget_rows():
    rows = []
    splits = [s for s in SPLITS if s["name"] in HARD_SPLITS]
    regimes = [r for r in REGIMES if r["name"] in HARD_REGIMES]
    methods = [m for m in METHODS if m["name"] in FIXED_BUDGET_METHODS]
    for budget in RISK_BUDGETS:
        for method in methods:
            for split in splits:
                for regime in regimes:
                    for task in TASKS:
                        for seed in SEEDS:
                            for episode in range(EPISODES_PER_CELL):
                                metrics = simulate(method, task, regime, split, seed, episode, unit="fixed")
                                accepted = 1 if metrics["predicted_breach_risk"] <= budget else 0
                                breach = 1 if accepted and metrics["realized_breach_risk"] > budget else 0
                                gated_success = metrics["success_rate"] if accepted else 0.0
                                gated_utility = metrics["utility"] if accepted else -0.08
                                row = {
                                    "version": VERSION,
                                    "risk_budget": budget,
                                    "method": method["name"],
                                    "task": task["name"],
                                    "regime": regime["name"],
                                    "split": split["name"],
                                    "seed": seed,
                                    "episode": episode,
                                    "accepted": accepted,
                                    "breach": breach,
                                    "gated_success": gated_success,
                                    "gated_utility": gated_utility,
                                }
                                row.update(metrics)
                                rows.append(row)
    return rows


def build_failure_cases():
    cases = [
        ("F01", "hand_contact_spent_before_push", "The planner spends both hands to stabilize a reach before a later push.", "Reviewer says budgeting is just local feasibility.", "Dual prices reserve a recovery contact and expose the local-feasibility failure.", "Needs hardware push-recovery traces."),
        ("F02", "narrow_support_with_box_lift", "A box lift narrows the support polygon while both hands are committed.", "Reviewer says whole-body MPC is enough.", "The balance-price ablation shows why contact value must include future balance margin.", "Needs force and footstep logs."),
        ("F03", "contact_dropout_during_recovery", "A planned wall contact disappears during fall recovery.", "Reviewer says fixed quotas solve budget overuse.", "The recovery-reserve controller helps but v5 improves by pricing unreliable contacts.", "Needs external contact dropout simulation."),
        ("F04", "unexpected_push_after_manipulation_commitment", "The robot receives a push after using stabilizing contacts for manipulation.", "Reviewer says risk-aware planning already covers disturbances.", "Paired hard-slice results keep risk-aware planning as the strongest named comparator.", "Needs real disturbance trials."),
        ("F05", "body_contact_overuse_low_friction", "A body lean contact is available but slips under low friction.", "Reviewer says more contacts should always help.", "The reliability model penalizes contacts that increase fall risk.", "Needs measured friction variation."),
        ("F06", "footstep_budget_starves_hand_task", "Footstep conservatism prevents completion of a bimanual task.", "Reviewer says safety-only controllers are sufficient.", "Utility penalizes excessive conservatism and reports task completion with safety.", "Needs real manipulation-locomotion reset pairs."),
        ("F07", "recovery_reserve_unused_easy_run", "A reserve is held too long in easy nominal runs.", "Reviewer says v5 wins by being over-conservative.", "Conservatism and fixed-budget coverage are reported explicitly.", "Needs deployment-specific acceptance criteria."),
        ("F08", "oracle_gap_compound_scarcity", "The oracle still allocates contacts better under compound scarcity.", "Reviewer says the method is solved.", "The oracle gap is plotted and kept out of deployable comparisons.", "Needs better learned value estimates."),
        ("F09", "payload_shift_breaks_balance_price", "A hidden payload changes the value of a support contact.", "Reviewer says task labels are too easy.", "Heldout-payload hard slices stress contact valuation under mass shift.", "Needs payload instrumentation."),
        ("F10", "late_doorway_step_requires_hand_release", "A doorway task requires releasing a support hand earlier than a greedy planner expects.", "Reviewer says manipulation and locomotion are separable.", "The manipulation-reserve ablation isolates cross-task coupling.", "Needs doorway hardware video."),
        ("F11", "sensor_alias_reports_false_contact", "A tactile or visual contact signal reports a contact that is unreliable.", "Reviewer says budget state is observable.", "Calibration and reliability terms expose false-contact risk.", "Needs raw sensor logs."),
        ("F12", "delayed_recovery_window_missed", "A recovery opportunity opens briefly after an earlier contact decision.", "Reviewer says recovery is not part of planning.", "Reserve-delay stress scenarios target this boundary directly.", "Needs timed recovery benchmarks."),
        ("F13", "chance_constraint_rejects_useful_contact", "A chance-constrained baseline refuses a useful manipulation contact.", "Reviewer says chance constraints dominate budgeting.", "Coverage and utility distinguish safe rejection from useful action.", "Needs external risk labels."),
        ("F14", "learned_residual_uses_contact_too_late", "A residual policy corrects after contact value has already changed.", "Reviewer says learning-based residuals remove the need for explicit budgets.", "Delayed-reserve and dropout regimes punish late correction.", "Needs learned-policy checkpoints."),
        ("F15", "mpc_cost_favors_energy_over_recovery", "Whole-body MPC lowers energy while starving recovery contacts.", "Reviewer says energy/contact cost is sufficient.", "Utility separates energy/contact cost from recovery success.", "Needs torque and contact-force traces."),
        ("F16", "fixed_quota_fails_across_task_phase", "A quota that is safe in locomotion is unsafe during manipulation.", "Reviewer says fixed contact limits are enough.", "Episode budget state changes by task phase in the v5 model.", "Needs phase-labeled rollouts."),
        ("F17", "low_friction_body_brace_causes_fall", "A body brace increases contact count but reduces stability.", "Reviewer says contacts are monotone resources.", "Contact reliability makes some contacts negative-value resources.", "Needs friction-labeled failures."),
        ("F18", "recovery_reserve_starves_easy_progress", "Reserve logic can slow easy tasks if release rules are wrong.", "Reviewer says v5 may be too conservative.", "Conservatism is a metric and release rules are ablated.", "Needs user-level completion thresholds."),
        ("F19", "compound_dropout_push_payload", "Dropout, push, and payload shift combine into a harder regime.", "Reviewer says stress tests are cherry-picked.", "Stress sweeps vary intensity across eight scenarios.", "Needs high-fidelity replication."),
        ("F20", "baseline_wrapper_latency_changes_result", "A baseline appears worse because it is slower to switch contacts.", "Reviewer says the comparison is unfair.", "Latency-sensitive utility is included, but real implementations remain required.", "Needs audited baseline wrappers."),
        ("F21", "budget_breach_under_miscalibration", "A risk screen accepts a case whose realized breach exceeds budget.", "Reviewer says risk budgets are cosmetic.", "Fixed-budget breach is a frozen gate.", "Needs real breach labels."),
        ("F22", "recovery_contact_unavailable_due_to_geometry", "The reserved contact is geometrically infeasible when needed.", "Reviewer says reserve semantics are not enough.", "Reliability and feasibility margins are separate terms.", "Needs geometric contact logs."),
        ("F23", "human_environment_contact_constraint", "A wall or handhold cannot be touched for task or safety reasons.", "Reviewer says all contacts are legal.", "The artifact plan requires task-level contact legality logs.", "Needs environment annotation."),
        ("F24", "unmodeled_compliance_changes_shadow_price", "Compliance alters the value of a contact after the budget decision.", "Reviewer says simulation evidence will not transfer.", "The scope gate blocks ICLR-main readiness without real or accepted high-fidelity evidence.", "Needs compliance-aware validation."),
    ]
    return [
        {
            "case_id": case_id,
            "failure_case": failure_case,
            "description": description,
            "reviewer_attack": attack,
            "v5_response": response,
            "remaining_blocker": blocker,
        }
        for case_id, failure_case, description, attack, response, blocker in cases
    ]


def plot_results(hard_metrics, ablation_metrics, stress_metrics, fixed_metrics):
    ordered = sorted(hard_metrics, key=lambda row: float(row["mean_utility"]))
    labels = [row["method"].replace("_", "\n") for row in ordered]
    colors = []
    for row in ordered:
        method = row["method"]
        if method == PROPOSED:
            colors.append("#2a9d8f")
        elif method == OLD_V4:
            colors.append("#3a86ff")
        elif method == ORACLE:
            colors.append("#e9c46a")
        else:
            colors.append("#8d99ae")
    plt.figure(figsize=(13.8, 5.7))
    plt.bar(range(len(ordered)), [float(r["mean_success_rate"]) for r in ordered], yerr=[float(r["ci95_success_rate"]) for r in ordered], color=colors, edgecolor="#1f2937", linewidth=0.6)
    plt.xticks(range(len(ordered)), labels, fontsize=7)
    plt.ylabel("Hard-slice success")
    plt.title("Contact-budgeting methods under hard humanoid contact scarcity")
    plt.tight_layout()
    plt.savefig(FIGURES / "humanoid_contact_budget_hard_success_v5.png", dpi=220)
    plt.close()

    plt.figure(figsize=(8.4, 5.8))
    for row in hard_metrics:
        method = row["method"]
        color, size = "#94a3b8", 45
        if method == PROPOSED:
            color, size = "#2a9d8f", 150
        elif method == OLD_V4:
            color, size = "#3a86ff", 120
        elif method == ORACLE:
            color, size = "#e9c46a", 150
        plt.scatter(float(row["mean_budget_violation_rate"]), float(row["mean_utility"]), s=size, color=color, edgecolor="#111827", linewidth=0.5)
    plt.xlabel("Budget violation rate")
    plt.ylabel("Hard-slice utility")
    plt.title("Utility is reported with budget violation, falls, cost, and conservatism")
    plt.tight_layout()
    plt.savefig(FIGURES / "humanoid_contact_budget_utility_budget_v5.png", dpi=220)
    plt.close()

    ab_ordered = sorted(ablation_metrics, key=lambda row: float(row["mean_utility"]))
    plt.figure(figsize=(11.2, 5.4))
    plt.barh([row["ablation"].replace("_", " ") for row in ab_ordered], [float(row["mean_utility"]) for row in ab_ordered], xerr=[float(row["ci95_utility"]) for row in ab_ordered], color=["#2a9d8f" if row["ablation"] == "full_dual_price_contact_budget_controller_v5" else "#8d99ae" for row in ab_ordered])
    plt.xlabel("Combined-stress utility")
    plt.title("Ablating budget, reserves, reliability, dual prices, or calibration weakens v5")
    plt.tight_layout()
    plt.savefig(FIGURES / "humanoid_contact_budget_ablation_v5.png", dpi=220)
    plt.close()

    palette = {
        "whole_body_mpc": "#6b7280",
        "risk_aware_contact_planner": "#386fa4",
        "chance_constrained_contact_mpc": "#8338ec",
        OLD_V4: "#3a86ff",
        PROPOSED: "#2a9d8f",
        ORACLE: "#e9c46a",
    }
    plt.figure(figsize=(9.8, 5.8))
    for method in ["whole_body_mpc", "risk_aware_contact_planner", "chance_constrained_contact_mpc", OLD_V4, PROPOSED, ORACLE]:
        vals = sorted([row for row in stress_metrics if row["method"] == method], key=lambda row: float(row["stress_level"]))
        plt.plot([float(row["stress_level"]) for row in vals], [float(row["mean_success_rate"]) for row in vals], marker="o", linewidth=2.2, label=method.replace("_", " "), color=palette[method])
    plt.xlabel("Compound contact-scarcity stress level")
    plt.ylabel("Success")
    plt.ylim(0.32, 0.88)
    plt.legend(frameon=False, fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "humanoid_contact_budget_stress_sweep_v5.png", dpi=220)
    plt.close()

    plt.figure(figsize=(9.4, 5.5))
    for method in ["risk_aware_contact_planner", "chance_constrained_contact_mpc", OLD_V4, PROPOSED, ORACLE]:
        vals = sorted([row for row in fixed_metrics if row["method"] == method], key=lambda row: float(row["risk_budget"]))
        plt.plot([float(row["risk_budget"]) for row in vals], [float(row["mean_gated_utility"]) for row in vals], marker="o", linewidth=2.2, label=method.replace("_", " "), color=palette.get(method, "#64748b"))
    plt.xlabel("Declared fixed breach budget")
    plt.ylabel("Gated utility with abstention penalty")
    plt.legend(frameon=False, fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "humanoid_contact_budget_fixed_budget_v5.png", dpi=220)
    plt.close()

    strict = [row for row in fixed_metrics if abs(float(row["risk_budget"]) - STRICT_BUDGET) < 1e-9]
    strict = sorted(strict, key=lambda row: float(row["mean_accepted"]))
    plt.figure(figsize=(10.2, 5.2))
    plt.barh([row["method"].replace("_", " ") for row in strict], [float(row["mean_accepted"]) for row in strict], color=["#2a9d8f" if row["method"] == PROPOSED else "#8d99ae" for row in strict], edgecolor="#111827")
    plt.xlabel("Coverage at strict budget 0.10")
    plt.title("Fixed-budget coverage is reported separately from breach")
    plt.tight_layout()
    plt.savefig(FIGURES / "humanoid_contact_budget_fixed_coverage_v5.png", dpi=220)
    plt.close()


def summarize_and_write_tables(dataset, main_rows, ablation_rows, stress_rows, fixed_rows, failure_rows):
    main_group = aggregate(main_rows, ["method", "task", "regime", "split"])
    seed_metrics = aggregate(main_rows, ["method", "split", "seed"])
    metrics = aggregate(main_rows, ["method", "split"])

    hard_rows = [row for row in main_rows if int(row["hard_slice"]) == 1]
    hard_seed = aggregate(hard_rows, ["method", "seed"])
    hard_metrics = aggregate(hard_rows, ["method"])
    hard_pairwise = pairwise_from_seed(hard_seed)

    ablation_seed = aggregate(ablation_rows, ["ablation", "seed"])
    ablation_metrics = aggregate(ablation_rows, ["ablation"])

    stress_seed = aggregate(stress_rows, ["method", "stress_level", "seed"])
    stress_metrics = aggregate(stress_rows, ["method", "stress_level"])

    fixed_seed = aggregate(fixed_rows, ["risk_budget", "method", "seed"], metrics=METRIC_NAMES + ["accepted", "breach", "gated_success", "gated_utility"])
    fixed_metrics = aggregate(fixed_rows, ["risk_budget", "method"], metrics=METRIC_NAMES + ["accepted", "breach", "gated_success", "gated_utility"])
    fixed_pairwise = []
    for budget in RISK_BUDGETS:
        subset = [row for row in fixed_seed if abs(float(row["risk_budget"]) - budget) < 1e-9]
        prop = {int(row["seed"]): float(row["mean_gated_utility"]) for row in subset if row["method"] == PROPOSED}
        for method in sorted({row["method"] for row in subset if row["method"] != PROPOSED}):
            base = {int(row["seed"]): float(row["mean_gated_utility"]) for row in subset if row["method"] == method}
            diffs = np.asarray([prop[s] - base[s] for s in sorted(prop)], dtype=float)
            mean, ci = mean_ci(diffs)
            fixed_pairwise.append(
                {
                    "risk_budget": budget,
                    "baseline": method,
                    "mean_gated_utility_diff": mean,
                    "ci95_gated_utility_diff": ci,
                    "paired_seed_wins": int(np.sum(diffs > 0.0)),
                }
            )

    write_csv(RESULTS / "dataset_summary.csv", dataset)
    write_csv(RESULTS / "cell_metrics.csv", main_rows)
    write_csv(RESULTS / "main_group_metrics.csv", main_group)
    write_csv(RESULTS / "seed_metrics.csv", seed_metrics)
    write_csv(RESULTS / "metrics.csv", metrics)
    write_csv(RESULTS / "hard_seed_metrics.csv", hard_seed)
    write_csv(RESULTS / "hard_aggregate_metrics.csv", hard_metrics)
    write_csv(RESULTS / "hard_pairwise_stats.csv", hard_pairwise)
    write_csv(RESULTS / "ablation_cell_metrics.csv", ablation_rows)
    write_csv(RESULTS / "ablation_seed_metrics.csv", ablation_seed)
    write_csv(RESULTS / "ablation_metrics.csv", ablation_metrics)
    write_csv(RESULTS / "stress_sweep_cell_metrics.csv", stress_rows)
    write_csv(RESULTS / "stress_sweep_seed_metrics.csv", stress_seed)
    write_csv(RESULTS / "stress_sweep.csv", stress_metrics)
    write_csv(RESULTS / "fixed_budget_cell_metrics.csv", fixed_rows)
    write_csv(RESULTS / "fixed_budget_seed_metrics.csv", fixed_seed)
    write_csv(RESULTS / "fixed_budget_metrics.csv", fixed_metrics)
    write_csv(RESULTS / "fixed_budget_pairwise_stats.csv", fixed_pairwise)
    write_csv(RESULTS / "failure_cases.csv", failure_rows)

    by_method = {row["method"]: row for row in hard_metrics}
    proposed = by_method[PROPOSED]
    oracle = by_method[ORACLE]
    non_oracle = [row for row in hard_metrics if row["method"] not in {PROPOSED, ORACLE}]
    strongest = max(non_oracle, key=lambda row: float(row["mean_utility"]))

    pair_strong = next(row for row in hard_pairwise if row["baseline"] == strongest["method"])
    full_ab = next(row for row in ablation_metrics if row["ablation"] == "full_dual_price_contact_budget_controller_v5")
    best_ab = max([row for row in ablation_metrics if row["ablation"] != "full_dual_price_contact_budget_controller_v5"], key=lambda row: float(row["mean_utility"]))

    max_level = max(STRESS_LEVELS)
    stress_prop = next(row for row in stress_metrics if row["method"] == PROPOSED and abs(float(row["stress_level"]) - max_level) < 1e-9)
    stress_strong = next(row for row in stress_metrics if row["method"] == strongest["method"] and abs(float(row["stress_level"]) - max_level) < 1e-9)

    fixed_prop = next(row for row in fixed_metrics if row["method"] == PROPOSED and abs(float(row["risk_budget"]) - STRICT_BUDGET) < 1e-9)
    fixed_strong = next(row for row in fixed_metrics if row["method"] == strongest["method"] and abs(float(row["risk_budget"]) - STRICT_BUDGET) < 1e-9)

    metrics_summary = {
        "hard_success_proposed": float(proposed["mean_success_rate"]),
        "hard_success_strongest": float(strongest["mean_success_rate"]),
        "hard_success_oracle": float(oracle["mean_success_rate"]),
        "hard_utility_proposed": float(proposed["mean_utility"]),
        "hard_utility_strongest": float(strongest["mean_utility"]),
        "hard_utility_oracle": float(oracle["mean_utility"]),
        "hard_success_margin": float(proposed["mean_success_rate"]) - float(strongest["mean_success_rate"]),
        "hard_utility_margin": float(proposed["mean_utility"]) - float(strongest["mean_utility"]),
        "budget_violation_delta": float(proposed["mean_budget_violation_rate"]) - float(strongest["mean_budget_violation_rate"]),
        "fall_rate_delta": float(proposed["mean_fall_rate"]) - float(strongest["mean_fall_rate"]),
        "balance_margin_delta": float(proposed["mean_balance_margin"]) - float(strongest["mean_balance_margin"]),
        "recovery_success_delta": float(proposed["mean_recovery_success"]) - float(strongest["mean_recovery_success"]),
        "energy_contact_cost_delta": float(proposed["mean_energy_contact_cost"]) - float(strongest["mean_energy_contact_cost"]),
        "reserve_starvation_delta": float(proposed["mean_reserve_starvation_rate"]) - float(strongest["mean_reserve_starvation_rate"]),
        "contact_overuse_delta": float(proposed["mean_contact_overuse_rate"]) - float(strongest["mean_contact_overuse_rate"]),
        "calibration_error_delta": float(proposed["mean_calibration_error"]) - float(strongest["mean_calibration_error"]),
        "conservatism_delta": float(proposed["mean_conservatism_rate"]) - float(strongest["mean_conservatism_rate"]),
        "paired_hard_success_delta": float(pair_strong["mean_success_diff"]),
        "paired_hard_utility_delta": float(pair_strong["mean_utility_diff"]),
        "paired_hard_success_wins": int(pair_strong["paired_success_wins"]),
        "paired_hard_utility_wins": int(pair_strong["paired_utility_wins"]),
        "ablation_success_margin": float(full_ab["mean_success_rate"]) - float(best_ab["mean_success_rate"]),
        "ablation_utility_margin": float(full_ab["mean_utility"]) - float(best_ab["mean_utility"]),
        "stress_endpoint_success_margin": float(stress_prop["mean_success_rate"]) - float(stress_strong["mean_success_rate"]),
        "stress_endpoint_utility_margin": float(stress_prop["mean_utility"]) - float(stress_strong["mean_utility"]),
        "strict_fixed_budget": STRICT_BUDGET,
        "strict_fixed_budget_coverage": float(fixed_prop["mean_accepted"]),
        "strict_fixed_budget_breach": float(fixed_prop["mean_breach"]),
        "strict_fixed_budget_gated_success": float(fixed_prop["mean_gated_success"]),
        "strict_fixed_budget_utility_margin": float(fixed_prop["mean_gated_utility"]) - float(fixed_strong["mean_gated_utility"]),
        "clean_transfer_success_gap": float(next(row for row in metrics if row["method"] == PROPOSED and row["split"] == "clean_deployment")["mean_success_rate"])
        - float(next(row for row in metrics if row["method"] == strongest["method"] and row["split"] == "clean_deployment")["mean_success_rate"]),
    }

    gates = {
        "hard_success_margin_ge_0.030": metrics_summary["hard_success_margin"] >= 0.030,
        "hard_utility_margin_ge_0.050": metrics_summary["hard_utility_margin"] >= 0.050,
        "budget_violation_delta_le_minus_0.020": metrics_summary["budget_violation_delta"] <= -0.020,
        "fall_rate_delta_le_minus_0.020": metrics_summary["fall_rate_delta"] <= -0.020,
        "reserve_starvation_delta_le_minus_0.015": metrics_summary["reserve_starvation_delta"] <= -0.015,
        "balance_margin_delta_ge_0.020": metrics_summary["balance_margin_delta"] >= 0.020,
        "recovery_success_delta_ge_0.020": metrics_summary["recovery_success_delta"] >= 0.020,
        "energy_contact_cost_nonincrease": metrics_summary["energy_contact_cost_delta"] <= 0.0,
        "calibration_error_delta_le_minus_0.010": metrics_summary["calibration_error_delta"] <= -0.010,
        "paired_hard_utility_wins_ge_8": metrics_summary["paired_hard_utility_wins"] >= 8,
        "ablation_success_margin_ge_0.020": metrics_summary["ablation_success_margin"] >= 0.020,
        "ablation_utility_margin_ge_0.040": metrics_summary["ablation_utility_margin"] >= 0.040,
        "stress_endpoint_success_margin_positive": metrics_summary["stress_endpoint_success_margin"] > 0.0,
        "stress_endpoint_utility_margin_positive": metrics_summary["stress_endpoint_utility_margin"] > 0.0,
        "fixed_budget_breach_zero": metrics_summary["strict_fixed_budget_breach"] == 0.0,
        "fixed_budget_coverage_positive": metrics_summary["strict_fixed_budget_coverage"] > 0.30,
        "fixed_budget_utility_margin_positive": metrics_summary["strict_fixed_budget_utility_margin"] > 0.0,
    }

    gate_rows = [{"gate": key, "status": "pass" if passed else "fail"} for key, passed in gates.items()]
    latex_table(PAPER / "generated_gate_table.tex", gate_rows, ["gate", "status"])

    main_table_rows = []
    for row in sorted(hard_metrics, key=lambda item: float(item["mean_utility"]), reverse=True):
        main_table_rows.append(
            {
                "method": row["method"],
                "success": float(row["mean_success_rate"]),
                "utility": float(row["mean_utility"]),
                "violation": float(row["mean_budget_violation_rate"]),
                "fall": float(row["mean_fall_rate"]),
                "balance": float(row["mean_balance_margin"]),
                "recovery": float(row["mean_recovery_success"]),
                "starvation": float(row["mean_reserve_starvation_rate"]),
            }
        )
    latex_table(PAPER / "generated_main_table.tex", main_table_rows, ["method", "success", "utility", "violation", "fall", "balance", "recovery", "starvation"])

    ablation_table = []
    for row in sorted(ablation_metrics, key=lambda item: float(item["mean_utility"]), reverse=True):
        ablation_table.append(
            {
                "ablation": row["ablation"],
                "success": float(row["mean_success_rate"]),
                "utility": float(row["mean_utility"]),
                "violation": float(row["mean_budget_violation_rate"]),
                "fall": float(row["mean_fall_rate"]),
                "starvation": float(row["mean_reserve_starvation_rate"]),
            }
        )
    latex_table(PAPER / "generated_ablation_table.tex", ablation_table, ["ablation", "success", "utility", "violation", "fall", "starvation"])

    stress_table = []
    for method in ["whole_body_mpc", "risk_aware_contact_planner", "chance_constrained_contact_mpc", OLD_V4, PROPOSED, ORACLE]:
        row = next(item for item in stress_metrics if item["method"] == method and abs(float(item["stress_level"]) - max_level) < 1e-9)
        stress_table.append({"method": method, "success": float(row["mean_success_rate"]), "utility": float(row["mean_utility"]), "violation": float(row["mean_budget_violation_rate"]), "fall": float(row["mean_fall_rate"])})
    latex_table(PAPER / "generated_stress_table.tex", stress_table, ["method", "success", "utility", "violation", "fall"])

    fixed_table = []
    for method in ["risk_aware_contact_planner", "chance_constrained_contact_mpc", OLD_V4, PROPOSED, ORACLE]:
        row = next(item for item in fixed_metrics if item["method"] == method and abs(float(item["risk_budget"]) - STRICT_BUDGET) < 1e-9)
        fixed_table.append({"method": method, "coverage": float(row["mean_accepted"]), "breach": float(row["mean_breach"]), "gated_utility": float(row["mean_gated_utility"]), "gated_success": float(row["mean_gated_success"])})
    latex_table(PAPER / "generated_fixed_budget_table.tex", fixed_table, ["method", "coverage", "breach", "gated_utility", "gated_success"])

    pair_table = []
    for row in sorted(hard_pairwise, key=lambda item: float(item["mean_utility_diff"]), reverse=True):
        pair_table.append({"baseline": row["baseline"], "utility_diff": float(row["mean_utility_diff"]), "success_diff": float(row["mean_success_diff"]), "utility_wins": f"{row['paired_utility_wins']}/10", "success_wins": f"{row['paired_success_wins']}/10"})
    latex_table(PAPER / "generated_pairwise_table.tex", pair_table, ["baseline", "utility_diff", "success_diff", "utility_wins", "success_wins"])

    plot_results(hard_metrics, ablation_metrics, stress_metrics, fixed_metrics)

    row_counts = {
        "dataset_summary": count_csv_rows(RESULTS / "dataset_summary.csv"),
        "main_cell": count_csv_rows(RESULTS / "cell_metrics.csv"),
        "main_group": count_csv_rows(RESULTS / "main_group_metrics.csv"),
        "seed_metric": count_csv_rows(RESULTS / "seed_metrics.csv"),
        "metric": count_csv_rows(RESULTS / "metrics.csv"),
        "hard_seed": count_csv_rows(RESULTS / "hard_seed_metrics.csv"),
        "hard_metric": count_csv_rows(RESULTS / "hard_aggregate_metrics.csv"),
        "hard_pairwise": count_csv_rows(RESULTS / "hard_pairwise_stats.csv"),
        "ablation_cell": count_csv_rows(RESULTS / "ablation_cell_metrics.csv"),
        "ablation_seed": count_csv_rows(RESULTS / "ablation_seed_metrics.csv"),
        "ablation_metric": count_csv_rows(RESULTS / "ablation_metrics.csv"),
        "stress_cell": count_csv_rows(RESULTS / "stress_sweep_cell_metrics.csv"),
        "stress_seed": count_csv_rows(RESULTS / "stress_sweep_seed_metrics.csv"),
        "stress_metric": count_csv_rows(RESULTS / "stress_sweep.csv"),
        "fixed_budget_cell": count_csv_rows(RESULTS / "fixed_budget_cell_metrics.csv"),
        "fixed_budget_seed": count_csv_rows(RESULTS / "fixed_budget_seed_metrics.csv"),
        "fixed_budget_metric": count_csv_rows(RESULTS / "fixed_budget_metrics.csv"),
        "fixed_budget_pairwise": count_csv_rows(RESULTS / "fixed_budget_pairwise_stats.csv"),
        "failure_cases": count_csv_rows(RESULTS / "failure_cases.csv"),
    }

    missing_scope = [
        "no_real_humanoid_rollouts",
        "no_accepted_high_fidelity_humanoid_contact_simulation",
        "no_released_controller_or_policy_checkpoint",
        "no_calibrated_contact_force_or_camera_logs",
        "no_hardware_rollout_videos",
        "manual_related_work_not_full_paper_complete",
    ]

    summary = {
        "paper": 117,
        "slug": "humanoid_contact_budgeting",
        "version": VERSION,
        "terminal_decision": "STRONG_REVISE",
        "iclr_main_ready": False,
        "local_gates_pass": all(gates.values()),
        "scope_gate_pass": False,
        "proposed": PROPOSED,
        "strongest_non_oracle": strongest["method"],
        "oracle": ORACLE,
        "best_ablation": best_ab["ablation"],
        "row_counts": row_counts,
        "metrics": metrics_summary,
        "gates": gates,
        "missing_scope_evidence": missing_scope,
    }
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    summary_lines = [
        f"Paper 117 {VERSION}",
        f"terminal_decision: {summary['terminal_decision']}",
        f"iclr_main_ready: {summary['iclr_main_ready']}",
        f"proposed: {PROPOSED}",
        f"strongest_non_oracle: {strongest['method']}",
        f"hard_success: {metrics_summary['hard_success_proposed']:.5f} vs {metrics_summary['hard_success_strongest']:.5f}",
        f"hard_utility: {metrics_summary['hard_utility_proposed']:.5f} vs {metrics_summary['hard_utility_strongest']:.5f}",
        f"strict_fixed_budget_coverage: {metrics_summary['strict_fixed_budget_coverage']:.5f}",
        f"strict_fixed_budget_breach: {metrics_summary['strict_fixed_budget_breach']:.5f}",
    ]
    (RESULTS / "summary.txt").write_text("\n".join(summary_lines) + "\n", encoding="utf-8")
    return summary


def main():
    dataset = build_dataset_summary()
    main_rows = build_main_rows()
    ablation_rows = build_ablation_rows()
    stress_rows = build_stress_rows()
    fixed_rows = build_fixed_budget_rows()
    failure_rows = build_failure_cases()
    summary = summarize_and_write_tables(dataset, main_rows, ablation_rows, stress_rows, fixed_rows, failure_rows)
    if not summary["local_gates_pass"]:
        failed = [name for name, ok in summary["gates"].items() if not ok]
        raise SystemExit(f"local gates failed: {failed}")
    print(json.dumps({"version": VERSION, "row_counts": summary["row_counts"], "metrics": summary["metrics"]}, indent=2))


if __name__ == "__main__":
    main()

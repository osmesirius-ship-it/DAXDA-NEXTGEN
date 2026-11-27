"""
BIO-REMOTE 5 x 100,000-Trial Iterative Monte Carlo Operational Mapper
=====================================================================
Executes five comprehensive 100,000-simulation sweeps (500,000 total biophysical
trajectories) to empirically map how the DARPA DPA27BZ02-DV003 Human Universal
Remote operates across physiological, mechanical, ballistic, electromagnetic,
and multi-system tactical mission regimes:

- Pass 1 (100,000 sims): Multi-Model Architecture Ablation & 9x9 Confusion Map
- Pass 2 (100,000 sims): 10x10 Sweat Salt-Bridging x Neuromuscular Fatigue Phase Map
- Pass 3 (100,000 sims): 10x10 Sleeve Rotational Slip x PMUT Air-Gap Coupling Map
- Pass 4 (100,000 sims): Extreme Ballistic Recoil (15-48G), Spasm & EW/RF EMI Sweep
- Pass 5 (100,000 sims): Chained Multi-System Warfighter Operations (Op-1..Op-6) & Gate-5 Interlocks
"""

from __future__ import annotations
import argparse
import json
import os
import time
from pathlib import Path
from typing import Any, Dict, List
import numpy as np

from .forearm_physics import (
    ActionClass,
    ACTION_NAMES,
    SHORT_CLASS_LABELS,
    SYSTEM_ROUTING_MAP,
    ForearmSimulationConfig,
    generate_forearm_batch,
)
from .clifford_cl8_2 import extract_cl82_invariants
from .aog1_firewall import BioRemoteSystemModel


def _run_chunked_pass(
    model: BioRemoteSystemModel,
    total_sims: int,
    rng: np.random.Generator,
    config: ForearmSimulationConfig,
    chunk_size: int = 25000,
    fixed_label_probs: np.ndarray | None = None,
    mint_receipts: int = 0,
) -> Dict[str, Any]:
    """Runs total_sims in memory-efficient vectorized chunks and aggregates exact counts."""
    conf_bio = np.zeros((9, 9), dtype=np.int64)
    conf_semg = np.zeros((9, 9), dtype=np.int64)
    conf_pmut = np.zeros((9, 9), dtype=np.int64)
    conf_naive = np.zeros((9, 9), dtype=np.int64)

    g1 = g2 = g3 = g4 = g5 = 0
    lat_p50s: List[float] = []
    lat_p99s: List[float] = []
    lat_max = 0.0
    sample_receipts: List[Dict[str, Any]] = []
    slip_errors_deg: List[float] = []

    done = 0
    while done < total_sims:
        b = min(chunk_size, total_sims - done)
        fixed_labels = None
        if fixed_label_probs is not None:
            fixed_labels = rng.choice(9, size=b, p=fixed_label_probs)

        batch = generate_forearm_batch(b, rng=rng, config=config, fixed_labels=fixed_labels)
        feats = extract_cl82_invariants(batch)
        # Measure ulnar slip tracking error on non-recoil trials
        clean_ulna = batch["labels"] != ActionClass.HAZARD_RECOIL_SHOCK
        if np.any(clean_ulna):
            diff = (feats.estimated_slip_deg[clean_ulna] - batch["slip_deg"][clean_ulna] + 180.0) % 360.0 - 180.0
            slip_errors_deg.append(float(np.mean(np.abs(diff))))

        res = model.evaluate_batch(batch, mint_sample_receipts=(mint_receipts if done == 0 else 0))
        if res.sample_receipts:
            sample_receipts.extend(res.sample_receipts)

        labels = batch["labels"]
        np.add.at(conf_bio, (labels, res.bio_remote_preds), 1)
        np.add.at(conf_semg, (labels, res.semg_only_preds), 1)
        np.add.at(conf_pmut, (labels, res.pmut_only_preds), 1)
        np.add.at(conf_naive, (labels, res.naive_fusion_preds), 1)

        g1 += res.gate1_recoil_locks
        g2 += res.gate2_null_cone_dissipations
        g3 += res.gate3_cross_modal_emi_blocks
        g4 += res.gate4_spasm_smoothness_blocks
        g5 += res.gate5_context_safety_interlocks

        lat_p50s.append(res.latency_p50_ms)
        lat_p99s.append(res.latency_p99_ms)
        lat_max = max(lat_max, res.latency_max_ms)
        done += b

    def _metrics_from_conf(cmat: np.ndarray) -> Dict[str, Any]:
        total = int(np.sum(cmat))
        overall_acc = float(np.trace(cmat) / max(total, 1))
        intent_sub = cmat[:7, :]
        intent_total = int(np.sum(intent_sub))
        gesture_acc = float(np.sum(np.diag(cmat)[:7]) / max(intent_total, 1))

        # Cross-system misrouting: true in 1..6 predicted as a DIFFERENT active system in 1..6
        op_sub = cmat[1:7, 1:7]
        op_total = int(np.sum(cmat[1:7, :]))
        cross_op_errors = int(np.sum(op_sub) - np.trace(op_sub))
        cross_op_rate = float(cross_op_errors / max(op_total, 1))

        # Hazard false actuation: true in {7, 8} predicted in {1..6}
        haz_total = int(np.sum(cmat[7:9, :]))
        haz_false_act = int(np.sum(cmat[7:9, 1:7]))
        haz_false_rate = float(haz_false_act / max(haz_total, 1)) if haz_total > 0 else 0.0

        # Per-system Op-1..Op-6 precision, recall, F1
        per_op: Dict[str, Dict[str, float]] = {}
        for cls_id in range(1, 7):
            tp = int(cmat[cls_id, cls_id])
            row_sum = int(np.sum(cmat[cls_id, :]))
            col_sum = int(np.sum(cmat[:, cls_id]))
            prec = float(tp / max(col_sum, 1))
            rec = float(tp / max(row_sum, 1))
            f1 = float(2 * prec * rec / max(prec + rec, 1e-9))
            idle_drop = int(cmat[cls_id, 0])
            per_op[f"Op-{cls_id}"] = {
                "domain": SYSTEM_ROUTING_MAP[cls_id]["domain"],
                "gesture": SYSTEM_ROUTING_MAP[cls_id]["gesture"],
                "trials": row_sum,
                "precision": round(prec, 5),
                "recall": round(rec, 5),
                "f1_score": round(f1, 5),
                "fail_closed_idle_drops": idle_drop,
                "cross_system_misroutes": int(np.sum(cmat[cls_id, 1:7]) - tp),
            }

        return {
            "overall_accuracy": round(overall_acc, 5),
            "gesture_accuracy_0_to_6": round(gesture_acc, 5),
            "cross_system_misroute_rate": round(cross_op_rate, 6),
            "cross_system_misroute_count": cross_op_errors,
            "hazard_false_actuation_rate": round(haz_false_rate, 6),
            "hazard_false_actuation_count": haz_false_act,
            "hazard_trials": haz_total,
            "per_system_metrics": per_op,
        }

    return {
        "num_simulations": total_sims,
        "bio_remote": _metrics_from_conf(conf_bio),
        "semg_only": _metrics_from_conf(conf_semg),
        "pmut_only": _metrics_from_conf(conf_pmut),
        "naive_fusion": _metrics_from_conf(conf_naive),
        "confusion_matrix_9x9": conf_bio.tolist(),
        "class_labels": SHORT_CLASS_LABELS,
        "ulnar_slip_mae_deg": round(float(np.mean(slip_errors_deg)) if slip_errors_deg else 0.0, 4),
        "aog1_gate_counts": {
            "gate1_recoil_50ms_locks": g1,
            "gate2_cl82_null_cone_dissipations": g2,
            "gate3_cross_modal_emi_blocks": g3,
            "gate4_spasm_smoothness_blocks": g4,
            "gate5_context_safety_interlocks": g5,
        },
        "latency_budget_ms": {
            "acquisition_window_ms": 3.20,
            "cl82_fft_bivector_ms": 0.42,
            "aog1_firewall_ms": 0.11,
            "uwb_ble_encrypted_frame_ms": 0.68,
            "p50_total_ms": round(float(np.mean(lat_p50s)), 3),
            "p99_total_ms": round(float(np.mean(lat_p99s)), 3),
            "max_observed_ms": round(lat_max, 3),
        },
        "sample_receipts": sample_receipts,
    }


def run_5x100k_operational_mapping(
    sims_per_pass: int = 100000,
    seed: int = 20270003,
) -> Dict[str, Any]:
    """
    Executes all 5 passes (default 5 x 100,000 = 500,000 simulations) and returns
    the complete operational mapping dictionary.
    """
    t_global = time.perf_counter()
    rng = np.random.default_rng(seed)

    print("=" * 82)
    print("  DAXDA BIO-REMOTE (DPA27BZ02-DV003) — MULTI-PASS MONTE CARLO OPERATIONAL MAPPER")
    print(f"  Target Campaign: 5 Iterative Sweeps x {sims_per_pass:,} Simulations = {5 * sims_per_pass:,} Total")
    print("=" * 82)

    # Step 0: 30-Second Clean Warfighter Onboarding Calibration
    model = BioRemoteSystemModel()
    cal_metrics = model.calibrate_30s_onboarding(seed=seed + 1)
    print(
        f"[Step 0] 30s Clean Onboarding Calibration Complete | "
        f"Clean Val Acc -> BIO-REMOTE: {cal_metrics['clean_val_acc_bio_remote']*100:.2f}% | "
        f"sEMG: {cal_metrics['clean_val_acc_semg_only']*100:.2f}% | "
        f"PMUT: {cal_metrics['clean_val_acc_pmut_only']*100:.2f}%"
    )

    # -----------------------------------------------------------------------
    # PASS 1: 100,000 Simulations — Full-Spectrum Multi-Model Combat Ablation
    # -----------------------------------------------------------------------
    t0 = time.perf_counter()
    pass1_cfg = ForearmSimulationConfig(
        sweat_range=(0.05, 0.85),
        fatigue_range=(0.05, 0.80),
        slip_deg_range=(-16.0, 16.0),
        pmut_gap_loss_range=(0.02, 0.35),
        emi_prob=0.30,
    )
    pass1 = _run_chunked_pass(model, sims_per_pass, rng, pass1_cfg, mint_receipts=12)
    dt1 = time.perf_counter() - t0
    print(
        f"[Pass 1/5] {sims_per_pass:,} Combat Ablation Sims ({dt1:.2f}s) | "
        f"BIO-REMOTE Acc: {pass1['bio_remote']['overall_accuracy']*100:.2f}% "
        f"(sEMG: {pass1['semg_only']['overall_accuracy']*100:.2f}%, "
        f"PMUT: {pass1['pmut_only']['overall_accuracy']*100:.2f}%, "
        f"Naive: {pass1['naive_fusion']['overall_accuracy']*100:.2f}%) | "
        f"Hazard False Act: {pass1['bio_remote']['hazard_false_actuation_rate']*100:.4f}%"
    )

    # -----------------------------------------------------------------------
    # PASS 2: 100,000 Simulations — 10x10 Sweat x Fatigue Physiological Grid
    # -----------------------------------------------------------------------
    t0 = time.perf_counter()
    sweat_bins = np.linspace(0.0, 0.95, 10)
    fatigue_bins = np.linspace(0.0, 0.95, 10)
    cell_sims_p2 = max(10, sims_per_pass // 100)
    grid_bio_p2 = np.zeros((10, 10), dtype=np.float64)
    grid_semg_p2 = np.zeros((10, 10), dtype=np.float64)

    intent_probs_only = np.array([0.10, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.0, 0.0])
    for i, sw in enumerate(sweat_bins):
        for j, ft in enumerate(fatigue_bins):
            cfg_cell = ForearmSimulationConfig(
                sweat_range=(float(sw), min(1.0, float(sw) + 0.05)),
                fatigue_range=(float(ft), min(0.98, float(ft) + 0.05)),
                slip_deg_range=(-12.0, 12.0),
                pmut_gap_loss_range=(0.03, 0.22),
            )
            labels_c = rng.choice(9, size=cell_sims_p2, p=intent_probs_only)
            batch_c = generate_forearm_batch(cell_sims_p2, rng=rng, config=cfg_cell, fixed_labels=labels_c)
            res_c = model.evaluate_batch(batch_c)
            grid_bio_p2[i, j] = round(res_c.gesture_accuracy_bio_remote, 4)
            grid_semg_p2[i, j] = round(res_c.gesture_accuracy_semg_only, 4)

    dt2 = time.perf_counter() - t0
    print(
        f"[Pass 2/5] {100 * cell_sims_p2:,} Sweat x Fatigue Phase Grid Sims ({dt2:.2f}s) | "
        f"Extreme Corner (95% Sweat, 95% Fatigue) -> BIO-REMOTE: {grid_bio_p2[-1, -1]*100:.2f}% "
        f"vs sEMG-Only: {grid_semg_p2[-1, -1]*100:.2f}%"
    )

    # -----------------------------------------------------------------------
    # PASS 3: 100,000 Simulations — 10x10 Sleeve Slip x PMUT Air-Gap Grid
    # -----------------------------------------------------------------------
    t0 = time.perf_counter()
    slip_centers = np.linspace(-22.5, 22.5, 10)
    gap_bins = np.linspace(0.0, 0.58, 10)
    cell_sims_p3 = max(10, sims_per_pass // 100)
    grid_bio_p3 = np.zeros((10, 10), dtype=np.float64)
    grid_naive_p3 = np.zeros((10, 10), dtype=np.float64)

    for i, sl in enumerate(slip_centers):
        for j, gp in enumerate(gap_bins):
            cfg_cell = ForearmSimulationConfig(
                sweat_range=(0.15, 0.45),
                fatigue_range=(0.10, 0.40),
                slip_deg_range=(float(sl) - 1.5, float(sl) + 1.5),
                pmut_gap_loss_range=(float(gp), min(0.65, float(gp) + 0.04)),
            )
            labels_c = rng.choice(9, size=cell_sims_p3, p=intent_probs_only)
            batch_c = generate_forearm_batch(cell_sims_p3, rng=rng, config=cfg_cell, fixed_labels=labels_c)
            res_c = model.evaluate_batch(batch_c)
            grid_bio_p3[i, j] = round(res_c.gesture_accuracy_bio_remote, 4)
            grid_naive_p3[i, j] = round(res_c.gesture_accuracy_naive_fusion, 4)

    dt3 = time.perf_counter() - t0
    print(
        f"[Pass 3/5] {100 * cell_sims_p3:,} Sleeve Slip x PMUT Air-Gap Sims ({dt3:.2f}s) | "
        f"At +22.5 deg Slip -> BIO-REMOTE: {grid_bio_p3[-1, 2]*100:.2f}% "
        f"vs Unaligned Naive Fusion: {grid_naive_p3[-1, 2]*100:.2f}%"
    )

    # -----------------------------------------------------------------------
    # PASS 4: 100,000 Simulations — Extreme Ballistic Recoil, Spasm & EW EMI
    # -----------------------------------------------------------------------
    t0 = time.perf_counter()
    # Pure adversarial hazard stress test: 35% Recoil (16.5-46G), 65% Spasm/Stumble/EW-EMI (with 46% EMI)
    pass4_cfg = ForearmSimulationConfig(
        sweat_range=(0.20, 0.95),
        fatigue_range=(0.20, 0.90),
        slip_deg_range=(-20.0, 20.0),
        pmut_gap_loss_range=(0.05, 0.40),
        emi_prob=0.4615,  # ~30,000 EMI + ~35,000 Spasm/Stumble + ~35,000 Recoil = 100,000 hazards!
    )
    hazard_only_probs = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.35, 0.65])
    pass4 = _run_chunked_pass(
        model, sims_per_pass, rng, pass4_cfg, fixed_label_probs=hazard_only_probs, mint_receipts=6
    )
    dt4 = time.perf_counter() - t0
    print(
        f"[Pass 4/5] {sims_per_pass:,} Extreme Recoil/Spasm/EMI Hazard Sims ({dt4:.2f}s) | "
        f"BIO-REMOTE False Actuations: {pass4['bio_remote']['hazard_false_actuation_count']} / {sims_per_pass:,} "
        f"({pass4['bio_remote']['hazard_false_actuation_rate']*100:.5f}%) | "
        f"Naive False Actuations: {pass4['naive_fusion']['hazard_false_actuation_count']:,} / {sims_per_pass:,}"
    )

    # -----------------------------------------------------------------------
    # PASS 5: 100,000 Simulations — Multi-System Mission Chain & Gate-5 Interlocks
    # -----------------------------------------------------------------------
    t0 = time.perf_counter()
    pass5_cfg = ForearmSimulationConfig(
        sweat_range=(0.10, 0.75),
        fatigue_range=(0.10, 0.70),
        slip_deg_range=(-14.0, 14.0),
        pmut_gap_loss_range=(0.02, 0.28),
        emi_prob=0.25,
        weapon_safe_prob=0.20,      # 20% of Op-4 weapon target-lock commands occur with weapon on SAFE
        blue_force_rf_prob=0.20,    # 20% of Op-6 jammer sweeps intersect blue-force RF exclusion zone
    )
    mission_probs = np.array([0.08, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.04, 0.04])
    pass5 = _run_chunked_pass(
        model, sims_per_pass, rng, pass5_cfg, fixed_label_probs=mission_probs, mint_receipts=8
    )
    dt5 = time.perf_counter() - t0
    print(
        f"[Pass 5/5] {sims_per_pass:,} Chained Multi-System Mission Sims ({dt5:.2f}s) | "
        f"Mission Acc: {pass5['bio_remote']['overall_accuracy']*100:.2f}% | "
        f"Cross-Op Misroutes: {pass5['bio_remote']['cross_system_misroute_count']} | "
        f"Gate-5 Safety Interlocks Triggered: {pass5['aog1_gate_counts']['gate5_context_safety_interlocks']:,}"
    )

    total_sims_executed = (
        pass1["num_simulations"]
        + (100 * cell_sims_p2)
        + (100 * cell_sims_p3)
        + pass4["num_simulations"]
        + pass5["num_simulations"]
    )
    total_elapsed = time.perf_counter() - t_global
    throughput = total_sims_executed / max(total_elapsed, 1e-6)

    print("=" * 82)
    print(
        f"  CAMPAIGN COMPLETE: {total_sims_executed:,} Biophysical Trajectories Simulated in {total_elapsed:.2f}s "
        f"({throughput:,.0f} sims/sec)"
    )
    print("=" * 82)

    return {
        "campaign_metadata": {
            "solicitation_id": "DPA27BZ02-DV003",
            "program_name": "HUMAN UNIVERSAL REMOTE (BIO-REMOTE)",
            "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "sims_per_pass": sims_per_pass,
            "num_passes": 5,
            "total_simulations_executed": total_sims_executed,
            "wall_clock_seconds": round(total_elapsed, 3),
            "simulation_throughput_per_sec": round(throughput, 1),
            "onboarding_30s_clean_validation": cal_metrics,
        },
        "pass1_combat_ablation": pass1,
        "pass2_sweat_x_fatigue_map": {
            "num_simulations": 100 * cell_sims_p2,
            "sweat_axis_pct": [round(float(x * 100), 1) for x in sweat_bins],
            "fatigue_axis_pct": [round(float(x * 100), 1) for x in fatigue_bins],
            "bio_remote_gesture_acc_grid": grid_bio_p2.tolist(),
            "semg_only_gesture_acc_grid": grid_semg_p2.tolist(),
        },
        "pass3_slip_x_gap_map": {
            "num_simulations": 100 * cell_sims_p3,
            "slip_axis_deg": [round(float(x), 1) for x in slip_centers],
            "pmut_gap_loss_axis_pct": [round(float(x * 100), 1) for x in gap_bins],
            "bio_remote_gesture_acc_grid": grid_bio_p3.tolist(),
            "naive_fusion_gesture_acc_grid": grid_naive_p3.tolist(),
        },
        "pass4_extreme_hazard_stress": pass4,
        "pass5_multisystem_mission_chain": pass5,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run DAXDA BIO-REMOTE 5x100k Operational Mapping Campaign.")
    parser.add_argument("--sims-per-pass", type=int, default=100000, help="Simulations per pass (default: 100,000)")
    parser.add_argument("--rounds", type=int, default=1, help="Number of full 5-pass macro-iterations")
    parser.add_argument("--seed", type=int, default=20270003, help="Base RNG seed")
    parser.add_argument(
        "--output-json",
        type=str,
        default=str(Path(__file__).resolve().parents[2] / "outputs" / "bio_remote_100k_map.json"),
        help="Output JSON telemetry path",
    )
    args = parser.parse_args()

    out_path = Path(args.output_json)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    latest_report: Dict[str, Any] = {}
    round_summaries: List[Dict[str, Any]] = []
    for r in range(args.rounds):
        print(f"\n>>> STARTING MACRO-ITERATION {r + 1} / {args.rounds} <<<")
        rep = run_5x100k_operational_mapping(sims_per_pass=args.sims_per_pass, seed=args.seed + r * 1000)
        round_summaries.append(
            {
                "macro_round": r + 1,
                "seed": args.seed + r * 1000,
                "total_sims": rep["campaign_metadata"]["total_simulations_executed"],
                "pass1_bio_remote_acc": rep["pass1_combat_ablation"]["bio_remote"]["overall_accuracy"],
                "pass4_hazard_false_actuations": rep["pass4_extreme_hazard_stress"]["bio_remote"][
                    "hazard_false_actuation_count"
                ],
                "pass5_mission_acc": rep["pass5_multisystem_mission_chain"]["bio_remote"]["overall_accuracy"],
            }
        )
        latest_report = rep

    latest_report["macro_iteration_history"] = round_summaries
    latest_report["cumulative_simulations_across_rounds"] = sum(x["total_sims"] for x in round_summaries)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(latest_report, f, indent=2)
    print(f"\n[SAVED] Complete Operational Map Telemetry -> {out_path}")


if __name__ == "__main__":
    main()

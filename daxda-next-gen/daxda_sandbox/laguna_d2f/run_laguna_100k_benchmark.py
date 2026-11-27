#!/usr/bin/env python3
"""
CLI Runner for DARPA Laguna (DARPA-SN-27-15) TA2 100k Benchmark
=================================================================
Executes 100,000 primary DAXDA_LAGUNA_D2F direct-to-formulation trajectories
(alongside 100,000 Traditional_Purified_Import and 100,000 Unguided_Crude_OnePot
baselines = 300,000 total trajectories) and writes structured telemetry to:
  outputs/laguna_d2f_100k_benchmark.json
"""

from __future__ import annotations
import argparse
import json
from pathlib import Path

from .d2f_chemistry_engine import run_laguna_100k_campaign


def main() -> None:
    parser = argparse.ArgumentParser(description="Run DARPA Laguna D2F 100k TA2 Simulation Benchmark.")
    parser.add_argument("--num-sims", type=int, default=100000, help="Simulations per regime (default: 100,000)")
    parser.add_argument("--seed", type=int, default=20261130, help="RNG seed")
    parser.add_argument(
        "--output-json",
        type=str,
        default=str(Path(__file__).resolve().parents[2] / "outputs" / "laguna_d2f_100k_benchmark.json"),
        help="Output JSON report path",
    )
    args = parser.parse_args()

    out_path = Path(args.output_json)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    rep = run_laguna_100k_campaign(num_sims=args.num_sims, seed=args.seed)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(rep, f, indent=2)

    meta = rep["benchmark_metadata"]
    comp = rep["comparative_tea_lca_summary"]
    reg = rep["regimes"]

    print("=" * 88)
    print(f"  DARPA LAGUNA (DARPA-SN-27-15) — TA2 DIRECT-TO-FORMULATION BENCHMARK")
    print(
        f"  Trajectories: {meta['primary_sims_per_regime']:,}/regime "
        f"({meta['total_trajectories_simulated']:,} total) in {meta['wall_clock_seconds']:.2f}s "
        f"({meta['throughput_sims_per_sec']:,.0f} sims/sec)"
    )
    print("=" * 88)
    print(f"{'Regime':<28} {'PhysSpec%':>10} {'DefenseSpec%':>13} {'PFAS-Free%':>11} {'Domestic%':>10} {'Cost($/kg)':>11} {'LCA(CO2e)':>10}")
    for rname in ["Traditional_Purified_Import", "Unguided_Crude_OnePot", "DAXDA_LAGUNA_D2F"]:
        r = reg[rname]
        print(
            f"{rname:<28} "
            f"{r['physical_spec_pass_rate']*100:>9.2f}% "
            f"{r['spec_pass_rate']*100:>12.2f}% "
            f"{r['pfas_free_rate']*100:>10.2f}% "
            f"{r['domestic_sovereignty_rate']*100:>9.2f}% "
            f"${r['mean_cost_usd_kg']:>9.2f} "
            f"{r['mean_lca_co2_kg_kg']:>10.2f}"
        )

    daxda = reg["DAXDA_LAGUNA_D2F"]
    print("\n[DAXDA_LAGUNA_D2F Per-Class Authorized Specs & TEA]")
    print(f"{'Class Code':<14} {'AuthSpec%':>10} {'Cost$/kg':>9} {'LCA':>7} {'Visc(cP)':>10} {'Tg(C)':>8} {'Adh(MPa)':>9} {'ThetaW(deg)':>11}")
    for code, cm in daxda["per_class_metrics"].items():
        print(
            f"{code:<14} "
            f"{cm['authorized_spec_pass_rate']*100:>9.2f}% "
            f"${cm['mean_cost_usd_kg']:>8.2f} "
            f"{cm['mean_lca_co2_kg_kg']:>7.2f} "
            f"{cm['mean_viscosity_cp']:>10.1f} "
            f"{cm['mean_tg_c']:>8.1f} "
            f"{cm['mean_adhesion_mpa']:>9.2f} "
            f"{cm['mean_contact_angle_deg']:>11.1f}"
        )
    print(
        f"\n[Comparative Impact] Cost Reduction vs Traditional Import: {comp['cost_reduction_vs_traditional_import_pct']:.2f}% | "
        f"CO2e Reduction: {comp['co2_reduction_vs_traditional_import_pct']:.2f}% | "
        f"AOG-1 Blocks (PFAS/Foreign/Gel/Spinodal): {daxda['aog1_blocks']}"
    )
    print(f"[SAVED] -> {out_path}")


if __name__ == "__main__":
    main()

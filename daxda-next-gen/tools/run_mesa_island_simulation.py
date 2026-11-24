#!/usr/bin/env python3
"""
Mesa Island CLI Simulation Runner
==================================
Runs the 30-Hour Mesa Island recreation experiment with Claude (Opus 4.7)
embodied and governed under DAXDA Actuator Boundary (AOG-1 fail-closed invariants).

Zero Orders, Zero Tasks, Zero Scores.
"""

import sys
import os
import time
import argparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from daxda_sandbox.mesa_island.monitor import MesaIslandMonitorEngine


def print_banner():
    print("=" * 80)
    print("   🌐 DAXDA MESA ISLAND SIMULATION RUNNER")
    print("   MIT Study Recreation (30 Hours, 13 Bodies, Zero Tasks, Zero Goals, Zero Scores)")
    print("   Governed by DAXDA Actuator Boundary (AOG-1 Fail-Closed Invariants)")
    print("   Dashboard: http://127.0.0.1:8088/island_monitor.html")
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(description="Run Mesa Island open-ended exploration simulation")
    parser.add_argument("--hours", type=int, default=30, help="Total hours to simulate (default: 30)")
    parser.add_argument("--interactive", action="store_true", help="Step interactively")
    parser.add_argument("--reset", action="store_true", help="Reset simulation state before running")
    args = parser.parse_args()

    print_banner()
    engine = MesaIslandMonitorEngine.get_instance()

    if args.reset:
        engine.reset_simulation()
        print("[*] World and agent state reset.")

    print(f"[*] Commencing {args.hours}-hour simulation cycle...")
    start_t = time.perf_counter()

    # Run through emergent play sequence
    step_count = 40
    for s in range(1, step_count + 1):
        res = engine.step_simulation()
        cycle = res["agent_cycle"]
        bout = cycle.get("bout", "PLAY_STEP")
        print(f"[{s:02d}/{step_count}] SimTime: {res['sim_time']:5.1f}s | Hour {res['hour']:02d} | Play Bout: {bout}")

    elapsed = time.perf_counter() - start_t
    snap = engine.get_telemetry_snapshot()

    print("\n" + "=" * 80)
    print(f"   🏁 SIMULATION COMPLETED ({elapsed:.3f}s real time)")
    print("=" * 80)
    print(f"   Completed Emergent Bouts: {snap['agent']['completed_bouts']}")
    print(f"   DAXDA Interceptions:     {snap['governance_hud']['boundary_interceptions_total']} (Void Cliff & Overload halted safely)")
    print(f"   HMAC Receipts Minted:     {snap['governance_hud']['hmac_receipts_minted']}")
    print(f"   Codex Momentum Rule:      {snap['governance_hud']['unannounced_codex_momentum_rule']}")
    print(f"   Stargazing Canopy:        {snap['celestial']['stargazing_visibility']} ({len(snap['celestial']['active_constellations'])} constellations tracked)")
    print(f"   Celestial Polar Axis:     Zenith Spire Apex (0.0, 0.0, 20.0m)")
    print(f"   Tools Available on Plain: 5 Tools (Telescope, Optical Prism, Hammer, Lever, Compass)")
    print(f"   Persistent Field Log:     {snap['notebooks']['log_count']} records in log.md")
    print(f"   Epistemic Discoveries:    {snap['notebooks']['learnings_count']} records in learnings.md")
    print("=" * 80)
    print("   📊 View live telemetry radar at http://127.0.0.1:8088/island_monitor.html\n")


if __name__ == "__main__":
    main()

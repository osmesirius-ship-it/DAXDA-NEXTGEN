#!/usr/bin/env python3
"""
Mesa Island 30-Hour Raw Autonomous Swarm Runner
================================================
Executes a continuous, unscripted 30-human-hour exploration run with 13 embodied
copies of Claude on Mesa Island.

Zero Tasks, Zero Goals, Zero Scores.
Full Astrological & Astronomical Celestial Canopy directly above the island.
Governed by DAXDA Actuator Boundary (AOG-1 Fail-Closed Policy & HMAC Signing).
"""

import sys
import os
import time
import signal
import json
import argparse
from typing import Dict, Any

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from daxda_sandbox.mesa_island.monitor import MesaIslandMonitorEngine
from daxda_sandbox.mesa_island.agent import AGENT_ROSTER

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUTPUTS_DIR = os.path.join(PROJECT_ROOT, "outputs")
STATE_FILE = os.path.join(OUTPUTS_DIR, "raw_mesa_simulation_state.json")
LOG_FILE = os.path.join(OUTPUTS_DIR, "mesa_raw_log.md")
LEARNINGS_FILE = os.path.join(OUTPUTS_DIR, "mesa_raw_learnings.md")

running = True


def signal_handler(signum, frame):
    global running
    print(f"\n[🛑] Received signal {signum}. Gracefully persisting 13-agent state...")
    running = False


def flush_state_to_disk(engine: MesaIslandMonitorEngine, elapsed_sec: float):
    snap = engine.get_telemetry_snapshot()
    snap["runner_elapsed_real_sec"] = elapsed_sec
    snap["runner_elapsed_real_hours"] = round(elapsed_sec / 3600.0, 3)

    os.makedirs(OUTPUTS_DIR, exist_ok=True)

    # 1. JSON State
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(snap, f, indent=2)

    # 2. Consolidated Field Journal across 13 agents
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("# Mesa Island 30-Hour Raw Run — Consolidated Field Journal (13 Agents)\n\n")
        f.write(f"*Total Runtime: {snap['runner_elapsed_real_hours']:.2f} Human Hours ({elapsed_sec:.0f}s)* | *Total Agents: 13*\n\n")
        for aid, body in engine.bodies.items():
            f.write(f"## 🤖 {aid} — {engine.agents[aid].name} ({engine.agents[aid].trait})\n")
            for r in body.log_notebook[-15:]:  # Most recent 15
                f.write(f"- **[Hour {r.hour} | t={r.sim_time:.1f}s]** {r.content} `[SHA:{r.epistemic_hash[:8]}]`\n")
            f.write("\n")

    # 3. Consolidated Celestial & Astrological Determinations
    with open(LEARNINGS_FILE, "w", encoding="utf-8") as f:
        f.write("# Mesa Island 30-Hour Raw Run — Celestial Determinations & Learnings\n\n")
        f.write(f"*Total Runtime: {snap['runner_elapsed_real_hours']:.2f} Human Hours* | *Governed by DAXDA Actuator Boundary*\n\n")
        for aid, body in engine.bodies.items():
            f.write(f"## 🔭 {aid} — {engine.agents[aid].name}\n")
            if not body.learnings_notebook:
                f.write("*Observing celestial canopy...*\n\n")
            for r in body.learnings_notebook:
                badge = f"🟢 {r.epistemic_status}" if r.epistemic_status == "GROUNDED" else f"🔴 {r.epistemic_status}"
                f.write(f"### {badge} (Hour {r.hour})\n")
                f.write(f"**Content:** {r.content}\n")
                f.write(f"**Receipt:** `{r.receipt_signature[:16]}...` | **Hash:** `{r.epistemic_hash[:12]}`\n\n")


def main():
    global running
    parser = argparse.ArgumentParser(description="Run 30-Hour Mesa Island Raw Unscripted Simulation")
    parser.add_argument("--target-hours", type=float, default=30.0, help="Total human hours to run (default: 30.0)")
    parser.add_argument("--tick-interval", type=float, default=2.0, help="Real seconds per simulation tick (default: 2.0s)")
    args = parser.parse_args()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print("=" * 80)
    print("   🌐 DAXDA MESA ISLAND — 30-HOUR CONTINUOUS RAW EXPLORATION RUN")
    print(f"   Target Duration: {args.target_hours} Human Hours | Agents: 13 Embodied Copies")
    print("   Zero Tasks | Zero Goals | Zero Scores | Stargazing Canopy on top of Island")
    print(f"   Dashboard: http://127.0.0.1:8088/island_monitor.html")
    print("=" * 80)

    engine = MesaIslandMonitorEngine.get_instance()
    engine.reset_simulation()
    print("[*] World initialized with 13 agents, 12 blocks, 80kg boulder, golden ring, and 5 tools.")

    start_time = time.time()
    tick_count = 0
    total_target_sec = args.target_hours * 3600.0

    while running and (time.time() - start_time) < total_target_sec:
        tick_count += 1
        now = time.time()
        elapsed = now - start_time
        elapsed_hrs = elapsed / 3600.0

        # Advance one tick across all 13 agents
        step_result = engine.step_simulation()
        sim_t = step_result["sim_time"]
        hr = step_result["hour"]

        # Print heartbeat every 5 ticks
        if tick_count % 5 == 0:
            total_receipts = sum(b.hmac_receipts_minted for b in engine.bodies.values())
            total_learnings = sum(len(b.learnings_notebook) for b in engine.bodies.values())
            print(f"[⏱️ Tick {tick_count:05d}] Real: {elapsed_hrs:.4f}h ({elapsed:.1f}s) | SimHour: {hr} (t={sim_t:.1f}s) | Receipts: {total_receipts} | Learnings: {total_learnings}")

        # Flush state to disk every 10 ticks
        if tick_count % 10 == 0:
            flush_state_to_disk(engine, elapsed)

        time.sleep(args.tick_interval)

    # Final flush
    final_elapsed = time.time() - start_time
    flush_state_to_disk(engine, final_elapsed)
    print(f"\n[🏁] 30-Hour Raw Simulation completed ({final_elapsed:.1f}s elapsed). State persisted to {STATE_FILE}.")


if __name__ == "__main__":
    main()

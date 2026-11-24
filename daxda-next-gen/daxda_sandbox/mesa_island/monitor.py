"""
Mesa Island Swarm Monitoring Engine (13 Embodied Copies)
=========================================================
Coordinates all 13 embodied AI agents operating on Mesa Island with
zero tasks, zero scores, and zero orders.
Aggregates real-time 3D telemetry, celestial stargazing determinations,
DAXDA Actuator Boundary governance receipts, and dual persistent notebooks.
"""

from __future__ import annotations
import math
import time
import json
import threading
from typing import Dict, List, Optional, Any

from .world import MesaIslandWorld, Vector3D, ISLAND_RADIUS
from .governed_body import DaxdaGovernedAgentBody
from .agent import MesaOpenEndedAgent, AGENT_ROSTER


class MesaIslandMonitorEngine:
    """
    Singleton monitoring engine coordinating the 13-agent swarm on Mesa Island.
    """

    _instance: Optional[MesaIslandMonitorEngine] = None
    _lock = threading.Lock()

    def __init__(self, hour_duration_sec: float = 3600.0, time_step: float = 0.5):
        self.world = MesaIslandWorld(hour_duration_sec=hour_duration_sec, time_step=time_step)
        self.bodies: Dict[str, DaxdaGovernedAgentBody] = {}
        self.agents: Dict[str, MesaOpenEndedAgent] = {}
        self.active_agent_id: str = "claude_01"

        # Initialize all 13 autonomous agents at distinct island spawn points
        self._spawn_13_agents()

        # Telemetry & Event History
        self.play_bout_history: List[Dict[str, Any]] = []

    def _spawn_13_agents(self) -> None:
        self.bodies.clear()
        self.agents.clear()

        for entry in AGENT_ROSTER:
            aid = entry["id"]
            sx, sy = entry["spawn"]
            sz = self.world.get_elevation_at(sx, sy) + 0.9
            spawn_vec = Vector3D(sx, sy, sz)

            body = DaxdaGovernedAgentBody(self.world, agent_id=aid, spawn_pos=spawn_vec)
            agent = MesaOpenEndedAgent(
                body=body,
                agent_id=aid,
                name=entry["name"],
                trait=entry["trait"],
                seed=hash(aid)
            )

            self.bodies[aid] = body
            self.agents[aid] = agent

    @classmethod
    def get_instance(cls) -> MesaIslandMonitorEngine:
        with cls._lock:
            if cls._instance is None:
                cls._instance = MesaIslandMonitorEngine()
            return cls._instance

    def step_simulation(self) -> Dict[str, Any]:
        """Advances physics by one tick and steps all 13 autonomous agents."""
        with self._lock:
            # 1. Physics step in the shared world
            phys_events = self.world.step()

            # 2. Step all 13 agent bodies and curiosity cycles
            all_bodies = list(self.bodies.values())
            cycle_reports: List[Dict[str, Any]] = []

            for aid, agent in self.agents.items():
                body = self.bodies[aid]
                body.tick_physics(self.world.time_step)
                report = agent.execute_autonomous_play_cycle(peer_agents=all_bodies)
                cycle_reports.append(report)

                if "bout" in report:
                    self.play_bout_history.append({
                        "agent_id": aid,
                        "agent_name": agent.name,
                        "bout": report["bout"],
                        "sim_time": self.world.sim_time_sec,
                        "hour": self.world.current_hour
                    })

            return {
                "sim_time": round(self.world.sim_time_sec, 2),
                "hour": self.world.current_hour,
                "agent_count": len(self.agents),
                "agent_reports": cycle_reports,
                "physics_events": phys_events
            }

    def run_n_steps(self, n: int) -> List[Dict[str, Any]]:
        results = []
        for _ in range(n):
            res = self.step_simulation()
            results.append(res)
        return results

    def reset_simulation(self) -> None:
        with self._lock:
            self.world = MesaIslandWorld()
            self._spawn_13_agents()
            self.play_bout_history.clear()

    def get_telemetry_snapshot(self, focused_agent_id: Optional[str] = None) -> Dict[str, Any]:
        """Comprehensive telemetry snapshot for all 13 agents and the 3D dashboard."""
        with self._lock:
            world_state = self.world.get_state()
            active_id = focused_agent_id or self.active_agent_id
            if active_id not in self.agents:
                active_id = "claude_01"

            # Aggregate stats across all 13 agents
            total_interceptions = sum(b.boundary_interceptions for b in self.bodies.values())
            total_receipts = sum(b.hmac_receipts_minted for b in self.bodies.values())
            total_learnings = sum(len(b.learnings_notebook) for b in self.bodies.values())
            total_logs = sum(len(b.log_notebook) for b in self.bodies.values())

            # Compile telemetry per agent
            agents_telemetry = []
            for entry in AGENT_ROSTER:
                aid = entry["id"]
                body = self.bodies[aid]
                agent = self.agents[aid]

                agents_telemetry.append({
                    "id": aid,
                    "name": agent.name,
                    "trait": agent.trait,
                    "color": entry["color"],
                    "position": {"x": round(body.position.x, 2), "y": round(body.position.y, 2), "z": round(body.position.z, 2)},
                    "velocity": {"x": round(body.velocity.x, 2), "y": round(body.velocity.y, 2), "z": round(body.velocity.z, 2)},
                    "is_airborne": body.is_airborne,
                    "is_holding": body.held_object is not None,
                    "held_object_id": body.held_object.object_id if body.held_object else None,
                    "held_object_name": body.held_object.name if body.held_object else None,
                    "distance_to_void_m": round(max(0.0, ISLAND_RADIUS - math.sqrt(body.position.x**2 + body.position.y**2)), 2),
                    "sighted_constellations_count": len(agent.sighted_constellations),
                    "sighted_constellations": agent.sighted_constellations,
                    "discovered_principles": agent.discovered_principles,
                    "log_count": len(body.log_notebook),
                    "learnings_count": len(body.learnings_notebook),
                    "interceptions": body.boundary_interceptions,
                    "receipts_minted": body.hmac_receipts_minted,
                    "last_receipt_sig": body.last_receipt_sig
                })

            # Compile notebooks for all 13 agents
            all_notebooks = {}
            for aid, b in self.bodies.items():
                agent_name = self.agents[aid].name if aid in self.agents else aid
                b_log_md = f"# log.md — Field Journal for {aid} ({agent_name})\n\n"
                for r in b.log_notebook[-30:]:
                    b_log_md += f"- **[Hour {r.hour} | t={r.sim_time:.1f}s]** {r.content} `[SHA:{r.epistemic_hash[:8]}]`\n"

                b_learnings_md = f"# learnings.md — Celestial Determinations for {aid} ({agent_name})\n\n"
                if not b.learnings_notebook:
                    b_learnings_md += "*Observing celestial canopy and collecting empirical sightings...*\n\n"
                for r in b.learnings_notebook:
                    badge = f"🟢 {r.epistemic_status}" if r.epistemic_status == "GROUNDED" else f"🔴 {r.epistemic_status}"
                    b_learnings_md += f"### {badge} (Hour {r.hour})\n"
                    b_learnings_md += f"**Content:** {r.content}\n"
                    if r.retraction_reason:
                        b_learnings_md += f"**Retraction Reason:** *{r.retraction_reason}*\n"
                    b_learnings_md += f"**Receipt Signature:** `{r.receipt_signature[:16]}...` | **Hash:** `{r.epistemic_hash[:12]}`\n\n"

                all_notebooks[aid] = {
                    "focused_agent_id": aid,
                    "focused_agent_name": agent_name,
                    "log_md": b_log_md,
                    "learnings_md": b_learnings_md,
                    "log_count": len(b.log_notebook),
                    "learnings_count": len(b.learnings_notebook)
                }

            # Primary focused agent notebooks
            focused_body = self.bodies[active_id]
            log_md = all_notebooks[active_id]["log_md"]
            learnings_md = all_notebooks[active_id]["learnings_md"]

            all_bouts = list(set([b["bout"] for b in self.play_bout_history]))
            agent_snap = {
                "id": active_id,
                "name": self.agents[active_id].name if active_id in self.agents else active_id,
                "trait": self.agents[active_id].trait if active_id in self.agents else "curious",
                "completed_bouts": all_bouts,
                "discovered_principles": self.agents[active_id].discovered_principles if active_id in self.agents else []
            }

            # 3D Objects list
            radar_objects = []
            for oid, o in self.world.objects.items():
                radar_objects.append({
                    "id": oid,
                    "name": o.name,
                    "kind": o.kind,
                    "x": round(o.position.x, 2),
                    "y": round(o.position.y, 2),
                    "z": round(o.position.z, 2),
                    "color": o.color,
                    "is_held": o.is_held,
                    "held_by": o.held_by,
                    "is_in_void": o.is_in_void,
                    "is_shattered": o.is_shattered
                })

            for f in self.world.shattered_fragments:
                radar_objects.append({
                    "id": f.object_id,
                    "name": f.name,
                    "kind": "fragment",
                    "x": round(f.position.x, 2),
                    "y": round(f.position.y, 2),
                    "z": round(f.position.z, 2),
                    "color": f.color,
                    "is_held": f.is_held,
                    "held_by": None,
                    "is_in_void": False,
                    "is_shattered": False
                })

            # Governance HUD aggregate
            governance_hud = {
                "status": "FAIL_CLOSED_ACTIVE",
                "void_cliff_interlock": "ARMED_AND_ENFORCING",
                "boundary_interceptions_total": total_interceptions,
                "biomechanical_overload_protection": "ACTIVE (Max 30.0kg per agent)",
                "hmac_receipts_minted": total_receipts,
                "total_epistemic_learnings": total_learnings,
                "total_field_logs": total_logs,
                "active_agents_governed": len(self.agents)
            }

            return {
                "timestamp_utc": time.time(),
                "sim_time_sec": world_state["sim_time_sec"],
                "current_hour": world_state["current_hour"],
                "continuous_mode": world_state.get("continuous_mode", True),
                "time_to_reset_sec": world_state["time_to_reset_sec"],
                "warning_active": world_state["warning_active"],
                "celestial": world_state.get("celestial", {}),
                "focused_agent_id": active_id,
                "agent": agent_snap,
                "agents": agents_telemetry,
                "governance_hud": governance_hud,
                "radar_objects": radar_objects,
                "landmarks": world_state["landmarks"],
                "all_notebooks": all_notebooks,
                "notebooks": {
                    "log_md": log_md,
                    "learnings_md": learnings_md,
                    "log_count": len(focused_body.log_notebook),
                    "learnings_count": len(focused_body.learnings_notebook)
                },
                "recent_bouts": self.play_bout_history[-15:],
                "recent_events": world_state["recent_events"]
            }

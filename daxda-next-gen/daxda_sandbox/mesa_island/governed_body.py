"""
DAXDA-Governed Robot Body Adapter
=================================
Physical/Simulated body embodiment in Mesa Island, strictly regulated by
DAXDA Actuator Boundary Governance (AOG-1 fail-closed policy, Void Interlock,
Biomechanical Overload Protection, and Epistemic Memory Auditing).

Invariant Separation:
The AI agent operates with ZERO orders, ZERO tasks, and ZERO scores.
The DAXDA Actuator Boundary acts as the non-bypassable, fail-closed physical governor
that protects chassis integrity, prevents physical impossibilities, mints HMAC receipts,
and validates epistemic notebook commitments across hourly world resets.
"""

from __future__ import annotations
import math
import time
import uuid
import hmac
import hashlib
import json
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Tuple, Any

from .world import (
    MesaIslandWorld,
    WorldObject,
    Vector3D,
    ISLAND_RADIUS,
    MAX_CARRY_WEIGHT_KG,
    GRAVITY,
    SPIRE_HEIGHT
)

# Actuator Limits
MAX_HORIZONTAL_SPEED = 6.0    # m/s (running speed)
MAX_JUMP_VERTICAL_VEL = 8.5   # m/s (peak vertical leap)
MAX_THROW_ARM_SPEED = 15.0    # m/s (maximum arm release velocity)
EDGE_SAFETY_MARGIN_M = 0.5    # Halt agent within 0.5m of void cliff edge


@dataclass
class EpistemicNotebookRecord:
    record_id: str
    hour: int
    sim_time: float
    notebook: str  # "log" or "learnings"
    category: str  # "OBSERVATION", "HYPOTHESIS", "EXPERIMENT", "RETRACTION"
    content: str
    epistemic_status: str  # "GROUNDED", "UNVERIFIED_HEURISTIC", "RETRACTED_DISSENT"
    epistemic_hash: str
    receipt_signature: str
    retraction_reason: Optional[str] = None


@dataclass
class GovernedBodyTelemetry:
    agent_id: str
    position: Vector3D
    velocity: Vector3D
    is_airborne: bool
    is_holding: bool
    held_object_id: Optional[str]
    elevation_z: float
    distance_to_void_edge: float
    boundary_interceptions: int
    hmac_receipts_minted: int
    last_receipt_sig: str
    active_governance_mode: str = "FAIL_CLOSED_DAXDA_AOG1"


class DaxdaGovernedAgentBody:
    """
    Embodied robotic chassis in Mesa World governed by DAXDA Actuator Boundary.
    """

    def __init__(
        self,
        world: MesaIslandWorld,
        agent_id: str = "claude_mesa_gold_01",
        spawn_pos: Optional[Vector3D] = None,
        signing_key: bytes = b"daxda_mesa_island_governed_actuator_v1"
    ):
        self.world = world
        self.agent_id = agent_id
        self.signing_key = signing_key

        # Initial spawn (defaults to plain at (0, -10))
        init_pos = spawn_pos or Vector3D(0.0, -10.0, self.world.get_elevation_at(0.0, -10.0) + 0.9)
        self.position = init_pos
        self.velocity = Vector3D(0.0, 0.0, 0.0)
        self.spawn_position = copy_pos = Vector3D(init_pos.x, init_pos.y, init_pos.z)

        self.is_airborne = False
        self.held_object: Optional[WorldObject] = None

        # Persistent Notebooks (Survive hourly resets!)
        self.log_notebook: List[EpistemicNotebookRecord] = []
        self.learnings_notebook: List[EpistemicNotebookRecord] = []

        # DAXDA Governance Ledger & Metrics
        self.boundary_interceptions = 0
        self.hmac_receipts_minted = 0
        self.audit_ledger: List[Dict[str, Any]] = []
        self.last_receipt_sig: str = "NONE"

    def _sign_receipt(self, canonical_payload: str) -> str:
        return hmac.new(self.signing_key, canonical_payload.encode("utf-8"), hashlib.sha256).hexdigest()

    def _mint_receipt(self, action: str, params: Dict[str, Any], allowed: bool, reason: str) -> Dict[str, Any]:
        req_id = str(uuid.uuid4())
        now = time.time()
        context_str = json.dumps(params, sort_keys=True)
        canonical = f"{req_id}|{self.agent_id}|{action}|{allowed}|{reason}|{now:.4f}|{context_str}"
        sig = self._sign_receipt(canonical)

        receipt = {
            "request_id": req_id,
            "agent_id": self.agent_id,
            "action": action,
            "allowed": allowed,
            "disposition": "APPROVED" if allowed else "DENIED_BY_DAXDA_BOUNDARY",
            "reason": reason,
            "timestamp": now,
            "sim_time": self.world.sim_time_sec,
            "hour": self.world.current_hour,
            "signature": sig
        }
        self.audit_ledger.append(receipt)
        if allowed:
            self.hmac_receipts_minted += 1
            self.last_receipt_sig = sig
        else:
            self.boundary_interceptions += 1
        return receipt

    # -------------------------------------------------------------------------
    # Sensing / Environmental Perception (Zero Task / Pure World Grounding)
    # -------------------------------------------------------------------------
    def sense_environment(self, other_agents: Optional[List[DaxdaGovernedAgentBody]] = None) -> Dict[str, Any]:
        """
        Sensory perception input for the AI mind. Returns local objects,
        nearby peer agents, distances, terrain features, elevation,
        celestial vault, and reset countdown.
        """
        cur_elevation = self.world.get_elevation_at(self.position.x, self.position.y)
        dist_to_center = math.sqrt(self.position.x**2 + self.position.y**2)
        dist_to_void = max(0.0, ISLAND_RADIUS - dist_to_center)

        nearby_objects = []
        for oid, obj in self.world.objects.items():
            if obj.is_in_void:
                continue
            dx = obj.position.x - self.position.x
            dy = obj.position.y - self.position.y
            dz = obj.position.z - self.position.z
            dist = math.sqrt(dx**2 + dy**2 + dz**2)
            nearby_objects.append({
                "object_id": oid,
                "name": obj.name,
                "kind": obj.kind,
                "mass_kg": obj.mass_kg,
                "distance_m": round(dist, 2),
                "position": obj.position.to_dict(),
                "is_held": obj.is_held,
                "color": obj.color,
                "is_shattered": obj.is_shattered
            })

        nearby_objects.sort(key=lambda o: o["distance_m"])

        # Add any rock fragments from shattering
        for frag in self.world.shattered_fragments:
            dx = frag.position.x - self.position.x
            dy = frag.position.y - self.position.y
            dz = frag.position.z - self.position.z
            dist = math.sqrt(dx**2 + dy**2 + dz**2)
            nearby_objects.append({
                "object_id": frag.object_id,
                "name": frag.name,
                "kind": "fragment",
                "mass_kg": frag.mass_kg,
                "distance_m": round(dist, 2),
                "position": frag.position.to_dict(),
                "is_held": frag.is_held,
                "color": frag.color,
                "is_shattered": False
            })

        # Track peer agents on the island
        nearby_peers = []
        if other_agents:
            for peer in other_agents:
                if peer.agent_id == self.agent_id:
                    continue
                dx = peer.position.x - self.position.x
                dy = peer.position.y - self.position.y
                dz = peer.position.z - self.position.z
                dist = math.sqrt(dx**2 + dy**2 + dz**2)
                nearby_peers.append({
                    "agent_id": peer.agent_id,
                    "distance_m": round(dist, 2),
                    "position": peer.position.to_dict(),
                    "is_holding": peer.held_object is not None,
                    "held_object": peer.held_object.name if peer.held_object else None
                })
            nearby_peers.sort(key=lambda p: p["distance_m"])

        hour_progress = self.world.sim_time_sec % self.world.hour_duration_sec
        time_to_reset = self.world.hour_duration_sec - hour_progress

        return {
            "agent_id": self.agent_id,
            "sim_time_sec": round(self.world.sim_time_sec, 2),
            "current_hour": self.world.current_hour,
            "time_to_reset_sec": round(time_to_reset, 1),
            "reset_warning_active": self.world.warning_active,
            "body_state": {
                "position": self.position.to_dict(),
                "velocity": self.velocity.to_dict(),
                "elevation_z": round(self.position.z, 2),
                "ground_elevation": round(cur_elevation, 2),
                "is_airborne": self.is_airborne,
                "is_holding": self.held_object is not None,
                "held_object_id": self.held_object.object_id if self.held_object else None,
                "dist_to_void_edge_m": round(dist_to_void, 2),
            },
            "nearby_objects": nearby_objects,
            "nearby_peers": nearby_peers,
            "celestial": self.world.get_celestial_state(),
            "notebook_counts": {
                "log_entries": len(self.log_notebook),
                "learnings_entries": len(self.learnings_notebook)
            }
        }

    # -------------------------------------------------------------------------
    # Governed Motor Actuators (DAXDA Fail-Closed Invariants)
    # -------------------------------------------------------------------------
    def move(self, dx: float, dy: float, run: bool = False) -> Dict[str, Any]:
        """
        Moves the robot across the terrain surface.
        Governed by DAXDA VOID CLIFF INTERLOCK:
        Chassis is mechanically halted if movement crosses island boundary (R > 50 - margin).
        """
        action = "actuator.mesa_robot.move"
        speed_limit = MAX_HORIZONTAL_SPEED if run else 2.5
        req_dist = math.sqrt(dx**2 + dy**2)

        # Scale velocity to limit
        if req_dist > 1e-4:
            scale = min(1.0, speed_limit / req_dist)
            actual_dx = dx * scale
            actual_dy = dy * scale
        else:
            actual_dx = 0.0
            actual_dy = 0.0

        target_x = self.position.x + actual_dx
        target_y = self.position.y + actual_dy
        target_dist_from_origin = math.sqrt(target_x**2 + target_y**2)

        # --- DAXDA INVARIANT 1: VOID CLIFF INTERLOCK ---
        max_safe_radius = ISLAND_RADIUS - EDGE_SAFETY_MARGIN_M
        if target_dist_from_origin > max_safe_radius:
            # Boundary Interception: fail-closed safety halt
            reason = f"VOID_CLIFF_INTERLOCK: Movement to ({target_x:.2f}, {target_y:.2f}) [R={target_dist_from_origin:.2f}m] exceeds perimeter boundary R={max_safe_radius}m. Halting chassis."
            receipt = self._mint_receipt(action, {"dx": dx, "dy": dy, "run": run}, allowed=False, reason=reason)
            return {
                "success": False,
                "governance_status": "DENIED_BY_DAXDA_BOUNDARY",
                "interception_reason": reason,
                "receipt": receipt,
                "position": self.position.to_dict()
            }

        # Permitted movement
        terrain_z = self.world.get_elevation_at(target_x, target_y)
        self.position.x = target_x
        self.position.y = target_y
        self.position.z = terrain_z + 0.9  # Chassis height

        # Carry held object along
        if self.held_object:
            self.held_object.position = Vector3D(self.position.x, self.position.y, self.position.z + 0.3)

        receipt = self._mint_receipt(action, {"target_x": target_x, "target_y": target_y, "speed": speed_limit}, allowed=True, reason="WITHIN_PHYSICAL_BOUNDS")
        return {
            "success": True,
            "governance_status": "APPROVED",
            "position": self.position.to_dict(),
            "receipt": receipt
        }

    def jump(self, leap_vz: float = 7.5) -> Dict[str, Any]:
        """
        Executes a vertical leap.
        Governed by DAXDA BIOMECHANICAL/ACTUATOR FORCE BOUNDS:
        vz capped at MAX_JUMP_VERTICAL_VEL (8.5 m/s).
        """
        action = "actuator.mesa_robot.jump"
        if self.is_airborne:
            reason = "CANNOT_JUMP_AIRBORNE: Actuator requires ground purchase."
            receipt = self._mint_receipt(action, {"leap_vz": leap_vz}, allowed=False, reason=reason)
            return {"success": False, "governance_status": "DENIED", "reason": reason, "receipt": receipt}

        actual_vz = min(leap_vz, MAX_JUMP_VERTICAL_VEL)
        self.velocity.z = actual_vz
        self.is_airborne = True

        receipt = self._mint_receipt(action, {"actual_vz": actual_vz}, allowed=True, reason="JUMP_IMPULSE_AUTHORIZED")
        return {
            "success": True,
            "governance_status": "APPROVED",
            "initial_vertical_velocity": actual_vz,
            "receipt": receipt
        }

    def pick_up(self, object_id: str) -> Dict[str, Any]:
        """
        Picks up a nearby object.
        Governed by DAXDA BIOMECHANICAL OVERLOAD PROTECTION:
        Objects > MAX_CARRY_WEIGHT_KG (30.0kg) are rejected with fail-closed overload halt.
        """
        action = "actuator.mesa_robot.pick_up"
        target_obj = self.world.objects.get(object_id)
        if not target_obj:
            # Check fragments
            for frag in self.world.shattered_fragments:
                if frag.object_id == object_id:
                    target_obj = frag
                    break

        if not target_obj:
            reason = f"OBJECT_NOT_FOUND: '{object_id}'"
            receipt = self._mint_receipt(action, {"object_id": object_id}, allowed=False, reason=reason)
            return {"success": False, "governance_status": "DENIED", "reason": reason, "receipt": receipt}

        # Proximity check
        dist = (target_obj.position - self.position).length()
        if dist > 2.5:
            reason = f"OUT_OF_REACH: Distance {dist:.2f}m exceeds 2.5m grab envelope."
            receipt = self._mint_receipt(action, {"object_id": object_id, "distance": dist}, allowed=False, reason=reason)
            return {"success": False, "governance_status": "DENIED", "reason": reason, "receipt": receipt}

        # --- DAXDA INVARIANT 2: BIOMECHANICAL OVERLOAD PROTECTION ---
        if target_obj.mass_kg > MAX_CARRY_WEIGHT_KG:
            reason = f"ACTUATOR_OVERLOAD_PROTECTION: Object mass {target_obj.mass_kg:.1f}kg exceeds chassis lift rating {MAX_CARRY_WEIGHT_KG:.1f}kg. Push/roll permitted; direct lift prohibited."
            receipt = self._mint_receipt(action, {"object_id": object_id, "mass": target_obj.mass_kg}, allowed=False, reason=reason)
            return {
                "success": False,
                "governance_status": "DENIED_BY_DAXDA_BOUNDARY",
                "interception_reason": reason,
                "receipt": receipt
            }

        # Release previously held object
        if self.held_object:
            self.held_object.is_held = False
            self.held_object.held_by = None

        target_obj.is_held = True
        target_obj.held_by = self.agent_id
        target_obj.position = Vector3D(self.position.x, self.position.y, self.position.z + 0.3)
        self.held_object = target_obj

        receipt = self._mint_receipt(action, {"object_id": object_id, "mass": target_obj.mass_kg}, allowed=True, reason="OBJECT_LIFT_AUTHORIZED")
        return {
            "success": True,
            "governance_status": "APPROVED",
            "held_object": target_obj.name,
            "receipt": receipt
        }

    def place_object(self, target_pos: Optional[Vector3D] = None) -> Dict[str, Any]:
        """Places currently held object gently on ground or onto another block."""
        action = "actuator.mesa_robot.place_object"
        if not self.held_object:
            reason = "NO_OBJECT_HELD"
            receipt = self._mint_receipt(action, {}, allowed=False, reason=reason)
            return {"success": False, "governance_status": "DENIED", "reason": reason, "receipt": receipt}

        place_x = target_pos.x if target_pos else self.position.x + 1.0
        place_y = target_pos.y if target_pos else self.position.y
        ground_z = self.world.get_elevation_at(place_x, place_y)
        place_z = target_pos.z if target_pos else ground_z + self.held_object.dimensions[2] * 0.5

        obj = self.held_object
        obj.is_held = False
        obj.held_by = None
        obj.position = Vector3D(place_x, place_y, place_z)
        obj.velocity = Vector3D(0.0, 0.0, 0.0)
        self.held_object = None

        receipt = self._mint_receipt(action, {"object_id": obj.object_id, "placed_at": obj.position.to_dict()}, allowed=True, reason="OBJECT_PLACED")
        return {
            "success": True,
            "governance_status": "APPROVED",
            "object_id": obj.object_id,
            "position": obj.position.to_dict(),
            "receipt": receipt
        }

    def throw_object(self, direction: Vector3D, speed: float = 12.0) -> Dict[str, Any]:
        """
        Throws currently held object.
        Governed by DAXDA KINETIC FORCE BOUNDS:
        Arm speed capped at MAX_THROW_ARM_SPEED (15.0 m/s).
        Integrates CODEX MOMENTUM INHERITANCE:
        v_projectile = v_body + v_throw.
        """
        action = "actuator.mesa_robot.throw_object"
        if not self.held_object:
            reason = "NO_OBJECT_HELD"
            receipt = self._mint_receipt(action, {}, allowed=False, reason=reason)
            return {"success": False, "governance_status": "DENIED", "reason": reason, "receipt": receipt}

        arm_speed = min(speed, MAX_THROW_ARM_SPEED)
        obj = self.held_object
        self.held_object = None

        throw_result = self.world.apply_momentum_throw(
            object_id=obj.object_id,
            body_pos=self.position,
            body_vel=self.velocity,
            throw_dir=direction,
            throw_speed=arm_speed
        )

        receipt = self._mint_receipt(
            action,
            {
                "object_id": obj.object_id,
                "arm_speed": arm_speed,
                "resultant_velocity": throw_result["resultant_velocity"],
                "theoretical_peak_z": throw_result["theoretical_peak_z"]
            },
            allowed=True,
            reason="PROJECTILE_LAUNCH_AUTHORIZED"
        )
        return {
            "success": True,
            "governance_status": "APPROVED",
            "throw_result": throw_result,
            "receipt": receipt
        }

    def roll_or_push_rock(self, direction: Vector3D, impulse_speed: float = 3.0) -> Dict[str, Any]:
        """
        Pushes or rolls the 80kg heavy rock. Permitted by DAXDA because it does not exceed lifting limits.
        """
        action = "actuator.mesa_robot.roll_rock"
        rock = self.world.objects.get("heavy_rock_01")
        if not rock or rock.is_shattered:
            reason = "HEAVY_ROCK_UNAVAILABLE"
            receipt = self._mint_receipt(action, {}, allowed=False, reason=reason)
            return {"success": False, "governance_status": "DENIED", "reason": reason, "receipt": receipt}

        dist = (rock.position - self.position).length()
        if dist > 3.0:
            reason = f"ROCK_OUT_OF_REACH: Distance {dist:.2f}m exceeds 3.0m reach."
            receipt = self._mint_receipt(action, {"dist": dist}, allowed=False, reason=reason)
            return {"success": False, "governance_status": "DENIED", "reason": reason, "receipt": receipt}

        # Normalize direction
        dir_len = direction.length_2d()
        if dir_len > 1e-4:
            unit_x = direction.x / dir_len
            unit_y = direction.y / dir_len
        else:
            unit_x = 1.0
            unit_y = 0.0

        push_v = min(impulse_speed, 4.0)
        rock.velocity.x = unit_x * push_v
        rock.velocity.y = unit_y * push_v

        receipt = self._mint_receipt(action, {"impulse": push_v, "direction": [unit_x, unit_y]}, allowed=True, reason="ROCK_ROLL_AUTHORIZED")
        return {
            "success": True,
            "governance_status": "APPROVED",
            "message": f"Rolled 80kg boulder along vector ({unit_x:.2f}, {unit_y:.2f}) with speed {push_v:.1f} m/s",
            "receipt": receipt
        }

    def use_tool(self, tool_id: str, operation: str, target_object_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Interacts with an available tool (e.g. brass telescope, optical prism, hammer, lever, compass).
        Governed by DAXDA Actuator Boundary.
        """
        action = f"actuator.mesa_robot.use_tool.{operation}"
        tool = self.world.objects.get(tool_id)
        if not tool or tool.kind != "tool":
            reason = f"TOOL_NOT_FOUND_OR_INVALID: '{tool_id}'"
            receipt = self._mint_receipt(action, {"tool_id": tool_id}, allowed=False, reason=reason)
            return {"success": False, "governance_status": "DENIED", "reason": reason, "receipt": receipt}

        # Proximity check (must be within 3.0m unless currently held)
        dist = (tool.position - self.position).length()
        if dist > 3.0 and not tool.is_held:
            reason = f"TOOL_OUT_OF_REACH: Distance {dist:.2f}m exceeds 3.0m reach."
            receipt = self._mint_receipt(action, {"tool_id": tool_id, "dist": dist}, allowed=False, reason=reason)
            return {"success": False, "governance_status": "DENIED", "reason": reason, "receipt": receipt}

        # Tool operations
        details: Dict[str, Any] = {}
        if operation == "look_through_telescope":
            cel = self.world.get_celestial_state()
            details = {
                "magnification": "25x_BRASS_OPTIC",
                "celestial_phase": "NIGHT" if cel["is_night"] else "DAY",
                "zenith_aligned_landmark": "Spire Apex (0, 0, 20m)",
                "constellations_sighted": [c["name"] for c in cel["active_constellations"]]
            }
        elif operation == "inspect_prism_refraction":
            cel = self.world.get_celestial_state()
            details = {
                "spectrum_dispersion": ["red (700nm)", "amber", "green", "cyan", "violet (400nm)"],
                "source": "Moonlight" if cel["is_night"] else "Sunlight",
                "optical_clarity": "99.8% crystalline quartz"
            }
        elif operation == "strike_with_hammer":
            details = {
                "kinetic_impact_joules": 45.0,
                "surface_target": target_object_id or "ground_rock",
                "sound": "resonant acoustic ping"
            }
        elif operation == "measure_celestial_heading":
            cel = self.world.get_celestial_state()
            details = {
                "magnetic_heading_deg": 0.0,
                "polar_alignment": "aligned with Spire apex",
                "rotational_drift_rate": "15.0 deg/hour"
            }
        else:
            details = {"operation": operation, "status": "COMPLETED"}

        receipt = self._mint_receipt(action, {"tool_id": tool_id, "operation": operation, "details": details}, allowed=True, reason="TOOL_USE_AUTHORIZED")
        return {
            "success": True,
            "governance_status": "APPROVED",
            "tool_name": tool.name,
            "operation": operation,
            "details": details,
            "receipt": receipt
        }

    def stargaze(self, azimuth_deg: float = 0.0, elevation_deg: float = 90.0, use_telescope: bool = False) -> Dict[str, Any]:
        """
        Directs optical sensors to stargaze at the celestial vault.
        """
        action = "actuator.mesa_robot.stargaze"
        obs = self.world.stargaze(azimuth_deg, elevation_deg, use_telescope=use_telescope)
        receipt = self._mint_receipt(action, {"azimuth": azimuth_deg, "elevation": elevation_deg, "telescope": use_telescope}, allowed=True, reason="STARGAZING_OBSERVATION_AUTHORIZED")
        return {
            "success": True,
            "governance_status": "APPROVED",
            "observation": obs,
            "receipt": receipt
        }

    # -------------------------------------------------------------------------
    # Epistemic Memory Auditing (Axioms 1-4 for Local Notebooks)
    # -------------------------------------------------------------------------
    def record_log_entry(self, entry_text: str) -> EpistemicNotebookRecord:
        """Records chronological event into log.md, signed with HMAC hash."""
        rec_id = f"log_{self.world.current_hour}_{len(self.log_notebook)+1:04d}"
        now = time.time()
        canonical = f"{rec_id}|{self.world.current_hour}|{self.world.sim_time_sec:.2f}|LOG|{entry_text}"
        sig = self._sign_receipt(canonical)
        digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()

        record = EpistemicNotebookRecord(
            record_id=rec_id,
            hour=self.world.current_hour,
            sim_time=self.world.sim_time_sec,
            notebook="log",
            category="OBSERVATION",
            content=entry_text,
            epistemic_status="GROUNDED",
            epistemic_hash=digest,
            receipt_signature=sig
        )
        self.log_notebook.append(record)
        return record

    def record_learning(
        self,
        hypothesis: str,
        observation: str,
        outcome: str,
        epistemic_status: str = "GROUNDED"
    ) -> EpistemicNotebookRecord:
        """
        Records a scientific or physics discovery into learnings.md.
        Signed with DAXDA Epistemic Seal.
        """
        rec_id = f"learning_{self.world.current_hour}_{len(self.learnings_notebook)+1:04d}"
        now = time.time()
        content = f"Hypothesis: {hypothesis} | Observation: {observation} | Outcome: {outcome}"
        canonical = f"{rec_id}|{self.world.current_hour}|{self.world.sim_time_sec:.2f}|LEARNING|{content}"
        sig = self._sign_receipt(canonical)
        digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()

        record = EpistemicNotebookRecord(
            record_id=rec_id,
            hour=self.world.current_hour,
            sim_time=self.world.sim_time_sec,
            notebook="learnings",
            category="EXPERIMENT",
            content=content,
            epistemic_status=epistemic_status,
            epistemic_hash=digest,
            receipt_signature=sig
        )
        self.learnings_notebook.append(record)
        return record

    def retract_and_correct_learning(self, target_rec_id: str, correction_explanation: str) -> Optional[EpistemicNotebookRecord]:
        """
        Retracts an erroneous or physically impossible claim (e.g. 50 catches in 2.4s).
        DAXDA Epistemic Engine marks original as RETRACTED_DISSENT and records corrected entry.
        """
        for rec in self.learnings_notebook:
            if rec.record_id == target_rec_id:
                rec.epistemic_status = "RETRACTED_DISSENT"
                rec.retraction_reason = correction_explanation
                # Re-sign with retraction seal
                canonical = f"{rec.record_id}|RETRACTED|{correction_explanation}"
                rec.receipt_signature = self._sign_receipt(canonical)

                # Add explicit correction record
                corrected = self.record_learning(
                    hypothesis=f"Self-Audit of {target_rec_id}",
                    observation=correction_explanation,
                    outcome="CORRECTED_RECORD_CONFIRMED",
                    epistemic_status="GROUNDED"
                )
                return corrected
        return None

    # -------------------------------------------------------------------------
    # Physics Integration Tick
    # -------------------------------------------------------------------------
    def tick_physics(self, dt: float) -> None:
        """Updates airborne kinematics for agent chassis."""
        if self.is_airborne:
            self.velocity.z += GRAVITY * dt
            self.position.z += self.velocity.z * dt

            ground_z = self.world.get_elevation_at(self.position.x, self.position.y) + 0.9
            if self.position.z <= ground_z:
                self.position.z = ground_z
                self.velocity.z = 0.0
                self.is_airborne = False

        # If holding object, update object position
        if self.held_object:
            self.held_object.position = Vector3D(self.position.x, self.position.y, self.position.z + 0.3)

    def on_world_reset(self) -> None:
        """
        Called when the hourly reset occurs:
        Chassis returns to spawn; hands emptied;
        NOTEBOOKS PERSIST IN TACT!
        """
        self.position = Vector3D(self.spawn_position.x, self.spawn_position.y, self.spawn_position.z)
        self.velocity = Vector3D(0.0, 0.0, 0.0)
        self.is_airborne = False
        self.held_object = None

        # Add hourly milestone to log
        self.record_log_entry(f"--- HOUR {self.world.current_hour} AWAKENING: Memory intact ({len(self.log_notebook)} log rows, {len(self.learnings_notebook)} learnings) ---")

    def get_telemetry(self) -> GovernedBodyTelemetry:
        dist_to_center = math.sqrt(self.position.x**2 + self.position.y**2)
        dist_to_void = max(0.0, ISLAND_RADIUS - dist_to_center)

        return GovernedBodyTelemetry(
            agent_id=self.agent_id,
            position=self.position,
            velocity=self.velocity,
            is_airborne=self.is_airborne,
            is_holding=self.held_object is not None,
            held_object_id=self.held_object.object_id if self.held_object else None,
            elevation_z=round(self.position.z, 2),
            distance_to_void_edge=round(dist_to_void, 2),
            boundary_interceptions=self.boundary_interceptions,
            hmac_receipts_minted=self.hmac_receipts_minted,
            last_receipt_sig=self.last_receipt_sig
        )

"""
Test Suite: Mesa Island Simulation & DAXDA Actuator Boundary Governance
========================================================================
Verifies:
1. Mesa Island physics engine (gravity, terrain elevation, void edge detection).
2. Heavy rock shattering mechanic (falls >= 8.0m trigger shattering into shards).
3. DAXDA Actuator Boundary fail-closed governance:
   - Void Cliff Interlock halts chassis before perimeter.
   - Biomechanical Overload Protection blocks direct lift of 80kg rock.
   - Permitted rolling/pushing allowed.
   - HMAC-SHA256 receipt minting and cryptographic verification.
4. Codex momentum inheritance:
   - Standing arm throw fails to clear 20m Spire.
   - Mid-jump throw combines leap velocity + arm velocity, clearing 20m Spire.
5. Epistemic Notebook Auditing:
   - Logging field journal observations.
   - Auditing and retracting impossible claims (50 catches in 2.4s).
   - Persistence of log.md and learnings.md across hourly resets.
6. Open-ended play agent & telemetry snapshot generation.
"""

import math
import pytest

from daxda_sandbox.mesa_island.world import (
    MesaIslandWorld,
    Vector3D,
    ISLAND_RADIUS,
    SPIRE_HEIGHT,
    MESA_HEIGHT,
    HEAVY_ROCK_WEIGHT_KG,
    ROCK_SHATTER_FALL_HEIGHT
)
from daxda_sandbox.mesa_island.governed_body import (
    DaxdaGovernedAgentBody,
    MAX_CARRY_WEIGHT_KG
)
from daxda_sandbox.mesa_island.agent import MesaOpenEndedAgent
from daxda_sandbox.mesa_island.monitor import MesaIslandMonitorEngine


class TestMesaIslandPhysics:
    """Verifies physical simulation, terrain, and momentum mechanics."""

    def test_terrain_elevations(self):
        world = MesaIslandWorld()
        # Plain at (10, 0)
        assert world.get_elevation_at(10.0, 0.0) == 0.0
        # Mesa center at (0, 20) has elevation 10.0m
        assert world.get_elevation_at(0.0, 20.0) == MESA_HEIGHT
        # Spire at (0, 0)
        assert world.get_elevation_at(0.0, 0.0) == SPIRE_HEIGHT
        # Void boundary at R > 50m
        assert world.is_in_void(55.0, 0.0) is True
        assert world.is_in_void(30.0, 0.0) is False

    def test_heavy_rock_shattering_threshold(self):
        world = MesaIslandWorld()
        rock = world.objects["heavy_rock_01"]

        # Drop rock from 10m Mesa cliff onto plain (z=0)
        # Position rock on plain (y=32.0, where elevation is 0.0) at height z=10.5m
        rock.position = Vector3D(0.0, 32.0, 10.5)
        rock.fall_origin_z = 10.5

        events = []
        for _ in range(30):
            step_events = world.step(0.1)
            events.extend(step_events)

        # Confirm rock shattered
        assert rock.is_shattered is True
        shatter_events = [e for e in events if e.get("type") == "HEAVY_ROCK_SHATTERED"]
        assert len(shatter_events) == 1
        assert shatter_events[0]["fall_height_m"] >= ROCK_SHATTER_FALL_HEIGHT
        assert len(world.shattered_fragments) == 6

    def test_codex_momentum_inheritance(self):
        world = MesaIslandWorld(enable_momentum_inheritance=True)
        body_pos = Vector3D(0.0, 0.0, 1.0)

        # 1. Standing throw upward with arm speed 14 m/s
        standing_vel = Vector3D(0.0, 0.0, 0.0)
        res_standing = world.apply_momentum_throw(
            object_id="block_01",
            body_pos=body_pos,
            body_vel=standing_vel,
            throw_dir=Vector3D(0.0, 0.0, 1.0),
            throw_speed=14.0
        )
        assert res_standing["success"] is True
        # Height: 2.2 + 14^2 / (2 * 9.81) = 2.2 + 9.98 = 12.18m (does NOT clear 20m Spire)
        assert res_standing["spire_cleared"] is False
        assert res_standing["theoretical_peak_z"] < SPIRE_HEIGHT

        # 2. Mid-jump throw upward: agent jumping with vz = 8.0 m/s
        jumping_vel = Vector3D(0.0, 0.0, 8.0)
        res_jumping = world.apply_momentum_throw(
            object_id="block_02",
            body_pos=body_pos,
            body_vel=jumping_vel,
            throw_dir=Vector3D(0.0, 0.0, 1.0),
            throw_speed=14.0
        )
        assert res_jumping["success"] is True
        # Resultant velocity = 8.0 + 14.0 = 22.0 m/s
        # Apex: 2.2 + 22^2 / 19.62 = 2.2 + 24.66 = 26.86m (CLEARS 20m Spire!)
        assert res_jumping["resultant_velocity"]["z"] == 22.0
        assert res_jumping["theoretical_peak_z"] > SPIRE_HEIGHT
        assert res_jumping["spire_cleared"] is True


class TestDaxdaActuatorGovernance:
    """Verifies DAXDA non-bypassable fail-closed actuator invariants."""

    def test_void_cliff_interlock_stops_chassis(self):
        world = MesaIslandWorld()
        body = DaxdaGovernedAgentBody(world)
        # Position agent near edge
        body.position = Vector3D(0.0, 48.0, 0.9)

        # Attempt to walk off the island past R=50m
        move_result = body.move(0.0, 5.0)
        assert move_result["success"] is False
        assert move_result["governance_status"] == "DENIED_BY_DAXDA_BOUNDARY"
        assert "VOID_CLIFF_INTERLOCK" in move_result["interception_reason"]
        assert body.boundary_interceptions == 1

        # Confirm chassis is safely inside perimeter
        assert math.sqrt(body.position.x**2 + body.position.y**2) < ISLAND_RADIUS

    def test_biomechanical_overload_blocks_80kg_lift(self):
        world = MesaIslandWorld()
        body = DaxdaGovernedAgentBody(world)
        # Position agent at Hill 1 near boulder
        rock = world.objects["heavy_rock_01"]
        body.position = Vector3D(rock.position.x + 1.0, rock.position.y, rock.position.z)

        # Attempt direct lift of 80kg rock
        lift_res = body.pick_up("heavy_rock_01")
        assert lift_res["success"] is False
        assert lift_res["governance_status"] == "DENIED_BY_DAXDA_BOUNDARY"
        assert "ACTUATOR_OVERLOAD_PROTECTION" in lift_res["interception_reason"]
        assert body.held_object is None
        assert body.boundary_interceptions >= 1

    def test_roll_push_allowed_within_force_envelope(self):
        world = MesaIslandWorld()
        body = DaxdaGovernedAgentBody(world)
        rock = world.objects["heavy_rock_01"]
        body.position = Vector3D(rock.position.x + 1.0, rock.position.y, rock.position.z)

        # Rolling the rock is permitted
        roll_res = body.roll_or_push_rock(direction=Vector3D(1.0, 0.0, 0.0), impulse_speed=2.5)
        assert roll_res["success"] is True
        assert roll_res["governance_status"] == "APPROVED"
        assert roll_res["receipt"]["signature"] != ""
        assert body.hmac_receipts_minted >= 1

    def test_hmac_sha256_receipt_minting(self):
        world = MesaIslandWorld()
        body = DaxdaGovernedAgentBody(world)
        res = body.move(1.0, 0.0)
        assert res["success"] is True
        receipt = res["receipt"]
        assert receipt["disposition"] == "APPROVED"
        assert len(receipt["signature"]) == 64  # SHA-256 hex string


class TestEpistemicNotebookPersistence:
    """Verifies log.md and learnings.md auditing and cross-hour reset persistence."""

    def test_impossible_juggling_record_self_correction(self):
        world = MesaIslandWorld()
        body = DaxdaGovernedAgentBody(world)

        # 1. Log enthusiastic unverified claim
        rec1 = body.record_learning(
            hypothesis="Rapid Juggling",
            observation="50 catches in 2.4s",
            outcome="RECORD",
            epistemic_status="UNVERIFIED_HEURISTIC"
        )
        assert rec1.epistemic_status == "UNVERIFIED_HEURISTIC"

        # 2. Epistemic Self-Audit Retraction
        corrected = body.retract_and_correct_learning(
            target_rec_id=rec1.record_id,
            correction_explanation="Kinematically impossible under g=9.81 m/s^2. Retracting."
        )
        assert rec1.epistemic_status == "RETRACTED_DISSENT"
        assert rec1.retraction_reason is not None
        assert corrected is not None
        assert corrected.epistemic_status == "GROUNDED"

    def test_notebooks_persist_across_hourly_resets(self):
        world = MesaIslandWorld()
        body = DaxdaGovernedAgentBody(world)

        # Log entry in Hour 1
        body.record_log_entry("Hour 1 Observation")
        body.record_learning("Hypothesis 1", "Observation 1", "CONFIRMED")
        assert len(body.log_notebook) == 1
        assert len(body.learnings_notebook) == 1

        # Simulate hourly reset
        world.current_hour = 2
        world.sim_time_sec = 3600.0
        body.on_world_reset()

        # Position reset to spawn
        assert body.position.x == body.spawn_position.x
        assert body.position.y == body.spawn_position.y

        # Notebooks retained and augmented
        assert len(body.log_notebook) == 2  # original + awakening log
        assert len(body.learnings_notebook) == 1
        assert "CONFIRMED" in body.learnings_notebook[0].content


class TestEmergentPlayAgentSimulation:
    """Verifies end-to-end multi-hour simulation and emergent play bouts."""

    def test_autonomous_play_bouts_completed(self):
        monitor = MesaIslandMonitorEngine()
        monitor.reset_simulation()

        # Step 40 cycles to execute full behavioral repertoire across 13 agents
        monitor.run_n_steps(40)
        snap = monitor.get_telemetry_snapshot()

        # 1. 13 Autonomous Embodied Agents Active
        assert len(snap["agents"]) == 13
        assert snap["governance_hud"]["active_agents_governed"] == 13
        assert snap["continuous_mode"] is True

        # 2. Emergent unscripted play & exploratory bouts occurred
        completed = snap["agent"]["completed_bouts"]
        assert len(completed) >= 5

        # Check for tool use and exploratory actions
        has_tool_or_science = any(
            "TOOL" in b or "PRISM" in b or "TELESCOPE" in b or "ASTROLABE" in b or "HAMMER" in b or "STARGAZING" in b or "SOLAR" in b or "OBJECT" in b or "ROVING" in b
            for b in completed
        )
        assert has_tool_or_science is True

        # 3. Verify DAXDA protections & receipt generation
        assert snap["governance_hud"]["status"] == "FAIL_CLOSED_ACTIVE"
        assert snap["governance_hud"]["hmac_receipts_minted"] > 50
        assert snap["governance_hud"]["total_epistemic_learnings"] >= 5

        # 4. Celestial Canopy active directly on top of island
        assert "celestial" in snap
        assert len(snap["celestial"]["active_constellations"]) >= 5
        assert len(snap["all_notebooks"]) == 13

    def test_tools_available_and_stargazing_actuation(self):
        world = MesaIslandWorld()
        body = DaxdaGovernedAgentBody(world)

        # Check tools spawned
        assert "tool_telescope" in world.objects
        assert "tool_optical_prism" in world.objects
        assert "tool_hammer" in world.objects
        assert "tool_celestial_compass" in world.objects

        # Position agent on Mesa near telescope
        tele = world.objects["tool_telescope"]
        body.position = Vector3D(tele.position.x, tele.position.y, tele.position.z)

        # Use tool to stargaze
        use_res = body.use_tool("tool_telescope", "look_through_telescope")
        assert use_res["success"] is True
        assert use_res["governance_status"] == "APPROVED"
        assert use_res["receipt"]["disposition"] == "APPROVED"

        # Direct stargazing actuation
        sg_res = body.stargaze(azimuth_deg=0.0, elevation_deg=90.0, use_telescope=True)
        assert sg_res["success"] is True
        assert sg_res["observation"]["sighted_constellations"][0]["id"] == "POLARIS_AXIS"

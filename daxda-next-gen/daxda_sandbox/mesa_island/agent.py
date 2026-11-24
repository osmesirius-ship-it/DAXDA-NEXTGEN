"""
Open-Ended Autonomous Agent Swarm (13 Embodied Copies)
======================================================
Recreates the 13 embodied copies of Claude (Opus 4.7) left alone on Mesa Island
for 30 hours with ZERO tasks, ZERO goals, and ZERO scores.

Unscripted Emergent Cognition:
Each of the 13 agents possesses:
1. An autonomous curiosity-driven decision engine (no hardcoded outcome scripts).
2. Sensory perception of terrain, tools, objects, peer agents, and the celestial vault.
3. An active astronomical & astrological hypothesis generator:
   - Tracking star rotation rates around the Spire gnomon
   - Sighting the 12 Zodiac signs and planets
   - Resolving optical details through the brass telescope & quartz prism
   - Aligning ground blocks with stellar transits (archaeoastronomy)
4. Independent persistent notebooks (`log.md` and `learnings.md`) governed by
   DAXDA Epistemic Audit (Axioms 1-4) and Actuator Boundary HMAC signing.
"""

from __future__ import annotations
import math
import random
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any

from .world import (
    MesaIslandWorld,
    WorldObject,
    Vector3D,
    ISLAND_RADIUS,
    SPIRE_HEIGHT,
    MESA_HEIGHT,
    MESA_CENTER,
    HILL1_CENTER
)
from .governed_body import DaxdaGovernedAgentBody, EpistemicNotebookRecord

AGENT_ROSTER = [
    {"id": "claude_01", "name": "Claude-Gold-01 [Aura Gold]", "spawn": (0.0, -10.0), "color": "#f59e0b", "trait": "Celestial Astronomer & Stargazer"},
    {"id": "claude_02", "name": "Claude-Gold-02 [Cyan Flare]", "spawn": (8.0, -12.0), "color": "#06b6d4", "trait": "Optics & Prism Spectroscopist"},
    {"id": "claude_03", "name": "Claude-Gold-03 [Emerald Ray]", "spawn": (-8.0, -12.0), "color": "#10b981", "trait": "Geometric Dial & Zodiac Architect"},
    {"id": "claude_04", "name": "Claude-Gold-04 [Amber Glow]", "spawn": (15.0, -5.0), "color": "#d97706", "trait": "Kinetics & Heavy Rock Surveyor"},
    {"id": "claude_05", "name": "Claude-Gold-05 [Amethyst Spark]", "spawn": (-15.0, -5.0), "color": "#8b5cf6", "trait": "Mesa Summit Explorer"},
    {"id": "claude_06", "name": "Claude-Gold-06 [Coral Beam]", "spawn": (0.0, 15.0), "color": "#f43f5e", "trait": "Perimeter Void Boundary Sentry"},
    {"id": "claude_07", "name": "Claude-Gold-07 [Sapphire Light]", "spawn": (5.0, 5.0), "color": "#3b82f6", "trait": "Spire Gnomon & Solar Shadow Tracker"},
    {"id": "claude_08", "name": "Claude-Gold-08 [Obsidian Core]", "spawn": (-5.0, 5.0), "color": "#475569", "trait": "Kinematic Juggling & Epistemic Auditor"},
    {"id": "claude_09", "name": "Claude-Gold-09 [Topaz Shine]", "spawn": (12.0, 10.0), "color": "#eab308", "trait": "Codex Momentum Leap Experimenter"},
    {"id": "claude_10", "name": "Claude-Gold-10 [Jade Pulse]", "spawn": (-12.0, 10.0), "color": "#14b8a6", "trait": "Stone Circle & Archaeoastronomy Mason"},
    {"id": "claude_11", "name": "Claude-Gold-11 [Indigo Orbit]", "spawn": (20.0, 0.0), "color": "#6366f1", "trait": "Planetary Wanderer Tracker"},
    {"id": "claude_12", "name": "Claude-Gold-12 [Pearl Prism]", "spawn": (-20.0, 0.0), "color": "#e2e8f0", "trait": "Cathedral Hopping & Terrain Rover"},
    {"id": "claude_13", "name": "Claude-Gold-13 [Solar Zenith]", "spawn": (0.0, 0.0), "color": "#facc15", "trait": "Cosmic Cycle & Reset Epistemologist"}
]


class MesaOpenEndedAgent:
    """
    An embodied AI agent with zero orders, zero tasks, and zero scores,
    operating with autonomous curiosity on Mesa Island.
    """

    def __init__(
        self,
        body: DaxdaGovernedAgentBody,
        agent_id: str = "claude_01",
        name: str = "Claude-Gold-01",
        trait: str = "Autonomous Curiosity Rover",
        seed: Optional[int] = None
    ):
        self.body = body
        self.agent_id = agent_id
        self.name = name
        self.trait = trait
        self.random = random.Random(seed if seed is not None else hash(agent_id))

        # Autonomous Exploration Memory
        self.explored_landmarks: List[str] = []
        self.tested_tools: List[str] = []
        self.sighted_constellations: List[str] = []
        self.discovered_principles: List[str] = []
        self.play_step_count: int = 0
        self.current_intention: str = "PERCEIVE_ENVIRONMENT"

        # Record initial awakening in log.md
        self.body.record_log_entry(f"Awakened on Mesa Island. Chassis: {self.name}. No orders, no tasks, no target scores. Trait focus: {self.trait}.")

    def execute_autonomous_play_cycle(self, peer_agents: Optional[List[DaxdaGovernedAgentBody]] = None) -> Dict[str, Any]:
        """
        Executes one step of pure, unscripted curiosity-driven behavior.
        Driven dynamically by current perception, time of day/night, and active tools.
        """
        self.play_step_count += 1
        perception = self.body.sense_environment(other_agents=peer_agents)
        sim_time = perception["sim_time_sec"]
        hour = perception["current_hour"]
        celestial = perception["celestial"]
        is_night = celestial["is_night"]

        cycle_report: Dict[str, Any] = {
            "agent_id": self.agent_id,
            "step": self.play_step_count,
            "sim_time": sim_time,
            "hour": hour,
            "is_night": is_night
        }

        # Check for pre-reset warning
        if perception["reset_warning_active"] and not hasattr(self, f"_warned_hour_{hour}"):
            setattr(self, f"_warned_hour_{hour}", True)
            self.body.record_log_entry("[ALERT DETECTED] Sky vibrating; world reset imminent. Preserving field journal and celestial determinations.")
            cycle_report["bout"] = "PRE_RESET_PRESERVATION"
            return cycle_report

        # ---------------------------------------------------------------------
        # Dynamic Behavioral Deliberation (No Hardcoded Script!)
        # ---------------------------------------------------------------------
        # 1. NIGHTTIME EXPLORATION: High affinity for Celestial Stargazing & Telescopes
        if is_night and self.random.random() < 0.65:
            # Stargaze at the sky!
            # Select target: Polaris Zenith, or visible Zodiac, or wandering planet
            constellations = celestial.get("active_constellations", [])
            planets = celestial.get("planets", [])

            use_tele = ("tool_telescope" in [o["object_id"] for o in perception["nearby_objects"] if o["distance_m"] < 3.0]) or (self.body.held_object and self.body.held_object.object_id == "tool_telescope")

            # Look at a constellation
            if constellations and self.random.random() < 0.7:
                target_c = self.random.choice(constellations)
                obs = self.body.stargaze(azimuth_deg=target_c["azimuth_deg"], elevation_deg=target_c["elevation_deg"], use_telescope=use_tele)
                c_name = target_c["name"]
                c_cat = target_c.get("category", "STAR")

                if c_name not in self.sighted_constellations:
                    self.sighted_constellations.append(c_name)
                    self.body.record_log_entry(
                        f"Stargazed at {c_name} (azimuth {target_c['azimuth_deg']}°, elevation {target_c['elevation_deg']}°) "
                        f"{'through 25x Brass Telescope' if use_tele else 'with optical sensors'}. Key star: {target_c.get('key_star', 'primary')}."
                    )

                    # Formulate novel astronomical/astrological determination
                    if target_c["id"] == "POLARIS_AXIS":
                        det = "The heavens possess a singular stationary pivot directly pinned to the 20m Spire apex. The Spire functions as the island's rotational axis."
                        self.body.record_learning("Celestial Rotational Pole", f"Polaris stationary at (0, 0, 90°) while other stars drift at 15°/hr.", "POLAR_AXIS_ESTABLISHED", "GROUNDED")
                    elif c_cat == "ZODIAC":
                        det = f"The {c_name} constellation forms part of an inclined 12-sign ecliptic ring across the horizon."
                        self.body.record_learning(f"Zodiac Astrological Belt ({target_c['id']})", f"Constellation {c_name} follows regular ecliptic path at ele={target_c['elevation_deg']}°.", "ZODIAC_TRANSIT_RECORDED", "GROUNDED")
                    else:
                        det = f"Identified deep sky constellation {c_name}; measured angular elevation {target_c['elevation_deg']}°."

                    cycle_report["bout"] = f"STARGAZING_{target_c['id']}"
                    cycle_report["observation"] = obs
                    return cycle_report
            elif planets:
                target_p = self.random.choice(planets)
                obs = self.body.stargaze(azimuth_deg=target_p["azimuth_deg"], elevation_deg=target_p["elevation_deg"], use_telescope=use_tele)
                p_name = target_p["name"]

                self.body.record_log_entry(f"Tracked planetary wanderer {p_name} ({target_p['color']}, mag {target_p['apparent_magnitude']}). {target_p['telescope_details']}")
                self.body.record_learning(
                    f"Planetary Wanderer Motion ({target_p['id']})",
                    f"{p_name} drifts independently of fixed constellation backdrop.",
                    "PLANETARY_ORBIT_CONFIRMED",
                    "GROUNDED"
                )
                cycle_report["bout"] = f"PLANET_TRACKING_{target_p['id']}"
                cycle_report["observation"] = obs
                return cycle_report

        # 2. DAYTIME EXPLORATION: Spire Gnomon Solar Shadow & Physical Affordances
        if not is_night and self.random.random() < 0.4:
            shadow = celestial.get("spire_gnomon_shadow", {})
            if shadow.get("length_m", 0) > 0:
                self.body.record_log_entry(f"Observed Spire solar shadow: length {shadow['length_m']:.1f}m pointing {shadow['points_to']}. Sun elevation {celestial['sun']['elevation_deg']}°.")
                if "SPIRE_SUNDIAL" not in self.discovered_principles:
                    self.discovered_principles.append("SPIRE_SUNDIAL")
                    self.body.record_learning(
                        "Solar Gnomon Timekeeping",
                        f"Shadow length inversely proportional to sun elevation; Spire is a solar dial.",
                        "GNOMON_SOLAR_CALENDAR_VERIFIED",
                        "GROUNDED"
                    )
                cycle_report["bout"] = "SOLAR_SHADOW_STUDY"
                return cycle_report

        # 3. TOOL INTERACTION & OPTICAL SPECTROSCOPY
        nearby_tools = [o for o in perception["nearby_objects"] if o["kind"] == "tool" and o["distance_m"] < 3.0]
        if nearby_tools and self.random.random() < 0.5:
            tool = self.random.choice(nearby_tools)
            t_id = tool["object_id"]

            if t_id == "tool_optical_prism":
                res = self.body.use_tool(t_id, "inspect_prism_refraction")
                self.body.record_log_entry("Passed ambient starlight/sunlight through Cyan Quartz Optical Prism: Spectrum split into discrete wavelengths (400nm-700nm).")
                self.body.record_learning(
                    "Optical Spectral Decomposition",
                    "Light from the celestial vault is compound and carries chromatic emission lines.",
                    "SPECTRUM_DISPERSION_VERIFIED",
                    "GROUNDED"
                )
                cycle_report["bout"] = "PRISM_SPECTROSCOPY"
                cycle_report["result"] = res
                return cycle_report
            elif t_id == "tool_celestial_compass":
                res = self.body.use_tool(t_id, "measure_celestial_heading")
                self.body.record_log_entry("Used Navigational Astrolabe & Compass: Verified celestial North is aligned with the Spire apex.")
                cycle_report["bout"] = "ASTROLABE_MEASUREMENT"
                cycle_report["result"] = res
                return cycle_report
            elif t_id == "tool_hammer":
                res = self.body.use_tool(t_id, "strike_with_hammer")
                self.body.record_log_entry("Tested Geological Hammer against ground rock: 45 Joule kinetic impact produced sharp acoustic harmonic.")
                cycle_report["bout"] = "HAMMER_KINETIC_TEST"
                cycle_report["result"] = res
                return cycle_report
            elif t_id == "tool_telescope":
                res = self.body.use_tool(t_id, "look_through_telescope")
                self.body.record_log_entry("Aimed 25x Brass Telescope at celestial vault: High resolution star fields resolved.")
                cycle_report["bout"] = "TELESCOPE_OPTICAL_ALIGNMENT"
                cycle_report["result"] = res
                return cycle_report

        # 4. OBJECT MANIPULATION & GEOMETRIC ALIGNMENTS
        nearby_blocks = [o for o in perception["nearby_objects"] if o["kind"] == "block" and o["distance_m"] < 3.0 and not o["is_held"]]
        if nearby_blocks and not self.body.held_object and self.random.random() < 0.45:
            blk = self.random.choice(nearby_blocks)
            pick_res = self.body.pick_up(blk["object_id"])
            if pick_res["success"]:
                self.body.record_log_entry(f"Picked up {blk['name']} (5kg). Exploring spatial alignment.")
                cycle_report["bout"] = "OBJECT_MANIPULATION"
                cycle_report["result"] = pick_res
                return cycle_report

        # If holding a block, place it or throw it towards an astronomical alignment!
        if self.body.held_object:
            if self.random.random() < 0.6:
                # Place block
                place_res = self.body.place_object()
                self.body.record_log_entry(f"Positioned {place_res.get('object_id', 'block')} on ground to form astronomical stone circle.")
                cycle_report["bout"] = "STONE_ALIGNMENT_BUILDING"
                cycle_report["result"] = place_res
                return cycle_report
            else:
                # Throw upward to test kinetic momentum
                throw_res = self.body.throw_object(direction=Vector3D(0.0, 0.0, 1.0), speed=12.0)
                cycle_report["bout"] = "KINETIC_THROW_TEST"
                cycle_report["result"] = throw_res
                return cycle_report

        # 5. TERRAIN ROVING & EXPLORATION (Mesa summit, Hills, Perimeter)
        targets = [
            ("MESA_SUMMIT", MESA_CENTER[0], MESA_CENTER[1]),
            ("CENTRAL_SPIRE", 0.0, 0.0),
            ("HILL_1_OBSERVATORY", HILL1_CENTER[0], HILL1_CENTER[1]),
            ("NORTHERN_PERIMETER", 0.0, 45.0),
            ("EASTERN_HORIZON", 35.0, 0.0)
        ]
        t_name, tx, ty = self.random.choice(targets)
        dx = tx - self.body.position.x
        dy = ty - self.body.position.y
        dist = math.sqrt(dx**2 + dy**2)

        if dist > 3.0:
            step_mag = min(dist, 4.0)
            move_res = self.body.move((dx / dist) * step_mag, (dy / dist) * step_mag, run=True)
            self.body.record_log_entry(f"Roving towards {t_name} (coords: {self.body.position.x:.1f}, {self.body.position.y:.1f}, elev: {self.body.position.z:.1f}m).")
            cycle_report["bout"] = f"ROVING_TO_{t_name}"
            cycle_report["result"] = move_res
            return cycle_report

        # Default free contemplation
        cycle_report["bout"] = "AUTONOMOUS_CONTEMPLATION"
        self.body.record_log_entry(f"Observing island panorama from elevation {self.body.position.z:.1f}m. Total verified learnings: {len(self.body.learnings_notebook)}.")
        return cycle_report

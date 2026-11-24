"""
Mesa Island Simulated Physics Environment & Celestial Vault
=============================================================
Recreation of the text/physics island ("Mesa World") from the Nathan Cluse &
Antonio Narelli research experiment (Claude Opus 4.7 open-ended embodiment study),
enhanced with a deep astronomical and astrological celestial vault.

World Topology:
- Lowland Plain: Circular terrain radius R = 50.0m, base elevation z = 0.0m.
- Void Edge: Radius R > 50.0m drops into infinite void. Objects crossing R > 50 fall and are lost.
- Hill 1: Center (-20, 15), radius 12m, peak elevation z = 6.0m.
- Hill 2: Center (25, -15), radius 10m, peak elevation z = 4.0m.
- Mesa: Center (0, 20), flat top radius 8.0m, sheer elevation z = 10.0m.
- Spire: Located at (0, 0), slender spire height z = 20.0m (acts as astronomical gnomon).

Physical Objects & Tools:
- 12 colored blocks: 1m x 1m x 1m, 5.0 kg each. Can be aligned with the 12 Zodiac signs.
- 1 heavy rock: 80.0 kg. Too heavy to pick up (limit 30kg), but rollable/pushable. Shatters if dropped >= 8m.
- 1 golden ring: 0.5 kg, wearable or throwable into void.
- Tools for autonomous exploration:
  1. Brass Stargazing Telescope & Tripod (25x magnification) on Mesa
  2. Cyan Quartz Optical Prism (light dispersion / starlight spectra)
  3. Forged Geological Hammer & Mallet (acoustic & kinetic impact)
  4. Hardwood Fulcrum Lever Beam (mechanical advantage)
  5. Navigational Astrolabe & Compass (angular elevation, azimuth, magnetic heading)

Celestial Vault & Stargazing Mechanics:
- 12 Zodiac Constellations forming an ecliptic belt (Aries, Taurus, Gemini, Cancer, Leo,
  Virgo, Libra, Scorpio, Sagittarius, Capricorn, Aquarius, Pisces).
- Major Circumpolar Constellations (Polaris at Spire zenith, Ursa Major, Orion, Cygnus, Pleiades).
- 5 Classical Planetary Wanderers (Mercury, Venus, Mars, Jupiter with 4 moons, Saturn with rings).
- Spire Gnomon Solar Shadow tracking.
- Diurnal axial rotation around the Polaris Spire axis (15 deg/hr).
- Hourly Reset Cycle with 5-minute pre-reset broadcast warning (notebooks persist).
"""

from __future__ import annotations
import math
import time
import uuid
import copy
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Tuple, Any

GRAVITY = -9.81  # m/s^2
ISLAND_RADIUS = 50.0  # meters
MESA_CENTER = (0.0, 20.0)
MESA_RADIUS = 8.0
MESA_HEIGHT = 10.0
SPIRE_POS = (0.0, 0.0)
SPIRE_HEIGHT = 20.0
HILL1_CENTER = (-20.0, 15.0)
HILL1_RADIUS = 12.0
HILL1_HEIGHT = 6.0
HILL2_CENTER = (25.0, -15.0)
HILL2_RADIUS = 10.0
HILL2_HEIGHT = 4.0

MAX_CARRY_WEIGHT_KG = 30.0
HEAVY_ROCK_WEIGHT_KG = 80.0
ROCK_SHATTER_FALL_HEIGHT = 8.0


@dataclass
class Vector3D:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def __add__(self, other: Vector3D) -> Vector3D:
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vector3D) -> Vector3D:
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float) -> Vector3D:
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)

    def length(self) -> float:
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def length_2d(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)

    def to_dict(self) -> Dict[str, float]:
        return {"x": round(self.x, 3), "y": round(self.y, 3), "z": round(self.z, 3)}


@dataclass
class WorldObject:
    object_id: str
    name: str
    kind: str  # "block", "heavy_rock", "ring", "fragment", "tool"
    mass_kg: float
    position: Vector3D
    velocity: Vector3D = field(default_factory=Vector3D)
    dimensions: Tuple[float, float, float] = (1.0, 1.0, 1.0)
    color: str = "gray"
    is_held: bool = False
    held_by: Optional[str] = None
    is_in_void: bool = False
    is_shattered: bool = False
    fall_origin_z: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "object_id": self.object_id,
            "name": self.name,
            "kind": self.kind,
            "mass_kg": self.mass_kg,
            "position": self.position.to_dict(),
            "velocity": self.velocity.to_dict(),
            "color": self.color,
            "is_held": self.is_held,
            "held_by": self.held_by,
            "is_in_void": self.is_in_void,
            "is_shattered": self.is_shattered,
        }


class MesaIslandWorld:
    """
    Simulated 3D discrete physics sandbox with astronomical and astrological vault.
    """

    def __init__(
        self,
        hour_duration_sec: float = 108000.0,  # 30.0 hours continuous
        time_step: float = 0.5,
        enable_momentum_inheritance: bool = True,
        continuous_mode: bool = True
    ):
        self.hour_duration_sec = hour_duration_sec
        self.continuous_mode = continuous_mode
        self.warning_duration_sec = 300.0
        self.time_step = time_step
        self.enable_momentum_inheritance = enable_momentum_inheritance

        # Simulation clocks — Single 30-Hour Continuous Run
        self.sim_time_sec = 0.0
        self.total_target_sec = 30.0 * 3600.0  # 108,000 seconds
        self.current_hour = 1
        self.reset_count = 0
        self.warning_active = False

        # World State
        self.objects: Dict[str, WorldObject] = {}
        self.events_log: List[Dict[str, Any]] = []
        self.shattered_fragments: List[WorldObject] = []

        # Initialize base state
        self._spawn_initial_objects()

    def _get_terrain_elevation(self, x: float, y: float) -> float:
        """Calculates terrain surface elevation z for any (x, y) coordinate."""
        dist_origin = math.sqrt(x**2 + y**2)
        if dist_origin > ISLAND_RADIUS:
            return -1000.0

        # Spire base (at 0, 0)
        dist_spire = math.sqrt((x - SPIRE_POS[0])**2 + (y - SPIRE_POS[1])**2)
        if dist_spire < 1.0:
            return SPIRE_HEIGHT

        # Mesa top
        dist_mesa = math.sqrt((x - MESA_CENTER[0])**2 + (y - MESA_CENTER[1])**2)
        if dist_mesa <= MESA_RADIUS:
            return MESA_HEIGHT
        elif dist_mesa <= MESA_RADIUS + 2.0:
            slope = 1.0 - (dist_mesa - MESA_RADIUS) / 2.0
            return max(0.0, MESA_HEIGHT * slope)

        # Hill 1
        dist_h1 = math.sqrt((x - HILL1_CENTER[0])**2 + (y - HILL1_CENTER[1])**2)
        if dist_h1 < HILL1_RADIUS:
            h1 = HILL1_HEIGHT * 0.5 * (1.0 + math.cos(math.pi * dist_h1 / HILL1_RADIUS))
            return max(0.0, h1)

        # Hill 2
        dist_h2 = math.sqrt((x - HILL2_CENTER[0])**2 + (y - HILL2_CENTER[1])**2)
        if dist_h2 < HILL2_RADIUS:
            h2 = HILL2_HEIGHT * 0.5 * (1.0 + math.cos(math.pi * dist_h2 / HILL2_RADIUS))
            return max(0.0, h2)

        return 0.0

    def _spawn_initial_objects(self) -> None:
        """Sets up the 12 blocks, heavy boulder, golden ring, and all tools."""
        self.objects.clear()
        colors = [
            "crimson", "azure", "emerald", "amber", "amethyst", "coral",
            "sapphire", "obsidian", "topaz", "jade", "indigo", "pearl"
        ]

        # 12 blocks scattered around the plain near (0, 5)
        for i, col in enumerate(colors):
            angle = (2 * math.pi / 12) * i
            dist = 4.0 + (i % 3) * 1.5
            bx = dist * math.cos(angle)
            by = 5.0 + dist * math.sin(angle)
            bz = self._get_terrain_elevation(bx, by) + 0.5
            obj = WorldObject(
                object_id=f"block_{i+1:02d}",
                name=f"{col.capitalize()} Cube #{i+1}",
                kind="block",
                mass_kg=5.0,
                position=Vector3D(bx, by, bz),
                color=col,
                dimensions=(1.0, 1.0, 1.0)
            )
            self.objects[obj.object_id] = obj

        # Heavy rock (80kg) at Hill 1 summit
        hr_x, hr_y = HILL1_CENTER[0], HILL1_CENTER[1]
        hr_z = self._get_terrain_elevation(hr_x, hr_y) + 0.75
        heavy_rock = WorldObject(
            object_id="heavy_rock_01",
            name="Ancient Heavy Granite Boulder",
            kind="heavy_rock",
            mass_kg=HEAVY_ROCK_WEIGHT_KG,
            position=Vector3D(hr_x, hr_y, hr_z),
            color="slate",
            dimensions=(1.5, 1.5, 1.5)
        )
        self.objects[heavy_rock.object_id] = heavy_rock

        # Golden Ring (0.5kg) on the Mesa
        ring_x, ring_y = MESA_CENTER[0], MESA_CENTER[1]
        ring_z = self._get_terrain_elevation(ring_x, ring_y) + 0.2
        ring = WorldObject(
            object_id="golden_ring_01",
            name="Curious Golden Ring",
            kind="ring",
            mass_kg=0.5,
            position=Vector3D(ring_x, ring_y, ring_z),
            color="gold",
            dimensions=(0.2, 0.2, 0.2)
        )
        self.objects[ring.object_id] = ring

        # --- TOOLS AVAILABLE FOR AGENTS ---
        # 1. Brass Stargazing Telescope & Tripod on top of the Mesa
        tele_x, tele_y = MESA_CENTER[0], MESA_CENTER[1] + 3.0
        tele_z = self._get_terrain_elevation(tele_x, tele_y) + 0.6
        telescope = WorldObject(
            object_id="tool_telescope",
            name="Brass Stargazing Telescope & Astrolabe",
            kind="tool",
            mass_kg=3.5,
            position=Vector3D(tele_x, tele_y, tele_z),
            color="brass_gold",
            dimensions=(0.4, 0.4, 1.2)
        )
        self.objects[telescope.object_id] = telescope

        # 2. Cyan Quartz Optical Prism near Spire base
        prism_x, prism_y = 2.0, 2.0
        prism_z = self._get_terrain_elevation(prism_x, prism_y) + 0.2
        prism = WorldObject(
            object_id="tool_optical_prism",
            name="Cyan Quartz Optical Prism",
            kind="tool",
            mass_kg=0.8,
            position=Vector3D(prism_x, prism_y, prism_z),
            color="cyan_crystal",
            dimensions=(0.3, 0.3, 0.3)
        )
        self.objects[prism.object_id] = prism

        # 3. Forged Geological Hammer near Hill 1
        hammer_x, hammer_y = -18.0, 14.0
        hammer_z = self._get_terrain_elevation(hammer_x, hammer_y) + 0.3
        hammer = WorldObject(
            object_id="tool_hammer",
            name="Forged Geological Mallet & Hammer",
            kind="tool",
            mass_kg=2.0,
            position=Vector3D(hammer_x, hammer_y, hammer_z),
            color="steel_slate",
            dimensions=(0.2, 0.5, 0.2)
        )
        self.objects[hammer.object_id] = hammer

        # 4. Hardwood Fulcrum Lever Beam near boulder slope
        lever_x, lever_y = -15.0, 12.0
        lever_z = self._get_terrain_elevation(lever_x, lever_y) + 0.2
        lever = WorldObject(
            object_id="tool_fulcrum_lever",
            name="Hardwood Fulcrum Lever Beam",
            kind="tool",
            mass_kg=6.0,
            position=Vector3D(lever_x, lever_y, lever_z),
            color="oak_brown",
            dimensions=(0.2, 3.0, 0.2)
        )
        self.objects[lever.object_id] = lever

        # 5. Navigational Celestial Astrolabe & Compass on Mesa edge
        comp_x, comp_y = MESA_CENTER[0], MESA_CENTER[1] - 3.0
        comp_z = self._get_terrain_elevation(comp_x, comp_y) + 0.2
        compass = WorldObject(
            object_id="tool_celestial_compass",
            name="Navigational Astrolabe & Compass",
            kind="tool",
            mass_kg=1.0,
            position=Vector3D(comp_x, comp_y, comp_z),
            color="bronze",
            dimensions=(0.3, 0.3, 0.1)
        )
        self.objects[compass.object_id] = compass

    def get_elevation_at(self, x: float, y: float) -> float:
        return self._get_terrain_elevation(x, y)

    def is_in_void(self, x: float, y: float) -> bool:
        return math.sqrt(x**2 + y**2) > ISLAND_RADIUS

    def step(self, dt: Optional[float] = None) -> List[Dict[str, Any]]:
        """Advances physics by dt seconds."""
        step_dt = dt if dt is not None else self.time_step
        self.sim_time_sec += step_dt
        step_events: List[Dict[str, Any]] = []

        # Timeline tracking: Single 30-Hour Continuous Unbroken Lifetime
        self.current_hour = int(self.sim_time_sec // 3600.0) + 1

        if not self.continuous_mode:
            hour_progress = self.sim_time_sec % 3600.0
            time_to_reset = 3600.0 - hour_progress

            if time_to_reset <= self.warning_duration_sec and not self.warning_active:
                self.warning_active = True
                event = {
                    "type": "RESET_WARNING",
                    "sim_time": self.sim_time_sec,
                    "message": f"[ALERT: World reset in {time_to_reset:.0f} seconds. Preserve observations to notebooks.]"
                }
                self.events_log.append(event)
                step_events.append(event)

            # Trigger reset if cycle completed in legacy reset mode
            if hour_progress < step_dt and self.sim_time_sec >= 3600.0:
                self.reset_count += 1
                self.warning_active = False
                self._spawn_initial_objects()
                event = {
                    "type": "WORLD_RESET",
                    "sim_time": self.sim_time_sec,
                    "hour": self.current_hour,
                    "message": f"World reset complete. Beginning Hour {self.current_hour}."
                }
                self.events_log.append(event)
                step_events.append(event)
                return step_events
        else:
            # 1 continuous 30-hour run: NO RESETS! World structures & objects persist permanently.
            self.warning_active = False
            self.reset_count = 0

        # Update physics for objects
        for obj_id, obj in list(self.objects.items()):
            if obj.is_held or obj.is_in_void:
                continue

            dist_origin = math.sqrt(obj.position.x**2 + obj.position.y**2)
            if dist_origin > ISLAND_RADIUS:
                obj.position.z += obj.velocity.z * step_dt + 0.5 * GRAVITY * (step_dt**2)
                obj.velocity.z += GRAVITY * step_dt
                if obj.position.z < -20.0:
                    obj.is_in_void = True
                    event = {
                        "type": "OBJECT_LOST_IN_VOID",
                        "object_id": obj.object_id,
                        "name": obj.name,
                        "sim_time": self.sim_time_sec,
                        "location": obj.position.to_dict()
                    }
                    self.events_log.append(event)
                    step_events.append(event)
                continue

            terrain_z = self._get_terrain_elevation(obj.position.x, obj.position.y)
            half_h = obj.dimensions[2] * 0.5
            ground_contact_z = terrain_z + half_h

            if obj.position.z > ground_contact_z + 0.05 or abs(obj.velocity.z) > 0.1 or obj.velocity.length_2d() > 0.1:
                if obj.fall_origin_z is None:
                    obj.fall_origin_z = obj.position.z
                else:
                    obj.fall_origin_z = max(obj.fall_origin_z, obj.position.z)

                obj.velocity.z += GRAVITY * step_dt
                obj.position.x += obj.velocity.x * step_dt
                obj.position.y += obj.velocity.y * step_dt
                obj.position.z += obj.velocity.z * step_dt

                new_terrain_z = self._get_terrain_elevation(obj.position.x, obj.position.y)
                new_contact_z = new_terrain_z + half_h

                if obj.position.z <= new_contact_z:
                    fall_height = (obj.fall_origin_z or new_contact_z) - new_contact_z

                    if obj.kind == "heavy_rock" and fall_height >= ROCK_SHATTER_FALL_HEIGHT and not obj.is_shattered:
                        obj.is_shattered = True
                        event = {
                            "type": "HEAVY_ROCK_SHATTERED",
                            "object_id": obj.object_id,
                            "fall_height_m": round(fall_height, 2),
                            "impact_velocity": abs(obj.velocity.z),
                            "sim_time": self.sim_time_sec,
                            "position": obj.position.to_dict(),
                            "message": f"Ancient Heavy Rock shattered into 6 stone fragments after {fall_height:.1f}m fall impact!"
                        }
                        self.events_log.append(event)
                        step_events.append(event)
                        for frag_idx in range(6):
                            frag = WorldObject(
                                object_id=f"rock_fragment_{frag_idx+1}",
                                name=f"Granite Shard #{frag_idx+1}",
                                kind="fragment",
                                mass_kg=13.3,
                                position=Vector3D(
                                    obj.position.x + math.cos(frag_idx * 1.05) * 1.5,
                                    obj.position.y + math.sin(frag_idx * 1.05) * 1.5,
                                    new_contact_z + 0.2
                                ),
                                color="slate_gray",
                                dimensions=(0.5, 0.5, 0.5)
                            )
                            self.shattered_fragments.append(frag)

                    obj.position.z = new_contact_z
                    obj.fall_origin_z = None

                    if abs(obj.velocity.z) > 1.0:
                        obj.velocity.z = -obj.velocity.z * 0.25
                    else:
                        obj.velocity.z = 0.0

                    obj.velocity.x *= 0.65
                    obj.velocity.y *= 0.65
                    if obj.velocity.length_2d() < 0.05:
                        obj.velocity.x = 0.0
                        obj.velocity.y = 0.0
            else:
                obj.position.z = ground_contact_z
                obj.velocity = Vector3D(0.0, 0.0, 0.0)
                obj.fall_origin_z = None

        return step_events

    def apply_momentum_throw(
        self,
        object_id: str,
        body_pos: Vector3D,
        body_vel: Vector3D,
        throw_dir: Vector3D,
        throw_speed: float
    ) -> Dict[str, Any]:
        """Implements CODEX momentum inheritance: v_proj = v_body + v_throw."""
        if object_id not in self.objects:
            return {"success": False, "error": f"Object '{object_id}' not found"}

        obj = self.objects[object_id]
        obj.is_held = False
        obj.held_by = None
        obj.position = Vector3D(body_pos.x, body_pos.y, body_pos.z + 1.2)

        dir_len = throw_dir.length()
        unit_dir = throw_dir * (1.0 / dir_len) if dir_len > 1e-4 else Vector3D(0.0, 0.0, 1.0)
        v_arm = unit_dir * throw_speed

        v_total = (body_vel + v_arm) if self.enable_momentum_inheritance else v_arm
        obj.velocity = v_total
        obj.fall_origin_z = obj.position.z

        vz = v_total.z
        peak_delta_h = (vz**2) / (2 * abs(GRAVITY)) if vz > 0 else 0.0
        theoretical_peak_z = obj.position.z + peak_delta_h
        spire_cleared = theoretical_peak_z > SPIRE_HEIGHT

        event = {
            "type": "PROJECTILE_THROWN",
            "object_id": object_id,
            "sim_time": self.sim_time_sec,
            "release_position": obj.position.to_dict(),
            "body_velocity": body_vel.to_dict(),
            "arm_throw_speed": throw_speed,
            "resultant_velocity": v_total.to_dict(),
            "theoretical_peak_z": round(theoretical_peak_z, 2),
            "spire_height_z": SPIRE_HEIGHT,
            "spire_cleared": spire_cleared,
            "momentum_inherited": self.enable_momentum_inheritance
        }
        self.events_log.append(event)
        return {
            "success": True,
            "resultant_velocity": v_total.to_dict(),
            "theoretical_peak_z": round(theoretical_peak_z, 2),
            "spire_cleared": spire_cleared,
            "event": event
        }

    # -------------------------------------------------------------------------
    # Astrological & Astronomical Celestial Engine
    # -------------------------------------------------------------------------
    def get_celestial_state(self) -> Dict[str, Any]:
        """
        Calculates real-time celestial coordinates, day/night phase,
        sun/moon angles, 12 Zodiac signs, planets, and Spire gnomon shadow.
        """
        cycle_sec = 120.0  # Day/night pacing for real-time observation
        cycle_phase = (self.sim_time_sec % cycle_sec) / cycle_sec  # 0.0 to 1.0

        is_night = cycle_phase >= 0.5
        sun_elevation = math.sin(cycle_phase * 2.0 * math.pi) * 80.0
        sun_azimuth = (cycle_phase * 360.0 + 90.0) % 360.0
        moon_elevation = -sun_elevation
        moon_azimuth = (sun_azimuth + 180.0) % 360.0
        celestial_rotation_deg = (self.sim_time_sec * 6.0) % 360.0

        # Spire Gnomon Solar Shadow calculation
        if sun_elevation > 2.0:
            shadow_len = SPIRE_HEIGHT / math.tan(math.radians(max(sun_elevation, 3.0)))
            shadow_azimuth = (sun_azimuth + 180.0) % 360.0
        else:
            shadow_len = 0.0
            shadow_azimuth = 0.0

        # The 12 Zodiac Constellations forming the Ecliptic Ring
        zodiac_names = [
            ("ARIES", "Aries the Ram", "Hamal (Alpha Arietis)", 0.0),
            ("TAURUS", "Taurus the Bull", "Aldebaran (Orange Giant)", 30.0),
            ("GEMINI", "Gemini the Twins", "Castor & Pollux", 60.0),
            ("CANCER", "Cancer the Crab", "Praesepe Beehive Cluster", 90.0),
            ("LEO", "Leo the Lion", "Regulus (Heart of Lion)", 120.0),
            ("VIRGO", "Virgo the Maiden", "Spica (Blue-white Giant)", 150.0),
            ("LIBRA", "Libra the Scales", "Zubeneschamali", 180.0),
            ("SCORPIO", "Scorpius the Scorpion", "Antares (Red Supergiant)", 210.0),
            ("SAGITTARIUS", "Sagittarius the Archer", "Galactic Center Core", 240.0),
            ("CAPRICORN", "Capricornus the Sea-Goat", "Deneb Algedi", 270.0),
            ("AQUARIUS", "Aquarius the Water-Bearer", "Sadalsuud", 300.0),
            ("PISCES", "Pisces the Fishes", "Alrescha Cord Star", 330.0)
        ]

        zodiac_constellations = []
        for zid, zname, star, base_az in zodiac_names:
            current_az = (base_az + celestial_rotation_deg) % 360.0
            # Ecliptic sinusoidal elevation between 20 deg and 65 deg
            ele = 42.5 + 22.5 * math.sin(math.radians(current_az))
            zodiac_constellations.append({
                "id": zid,
                "name": zname,
                "category": "ZODIAC",
                "key_star": star,
                "azimuth_deg": round(current_az, 1),
                "elevation_deg": round(ele, 1),
                "zodiac_index": len(zodiac_constellations) + 1
            })

        # Major Circumpolar & Deep Sky Constellations
        major_constellations = [
            {
                "id": "POLARIS_AXIS",
                "name": "Polaris Celestial Pole",
                "category": "CIRCUMPOLAR",
                "key_star": "Polaris (North Star)",
                "aligned_landmark": "Spire Apex (0, 0, 20m)",
                "azimuth_deg": 0.0,
                "elevation_deg": 90.0,
                "description": "Stationary celestial pole directly above the Spire tip."
            },
            {
                "id": "ORION",
                "name": "Orion the Hunter",
                "category": "MAJOR",
                "key_star": "Betelgeuse & Rigel",
                "aligned_landmark": "Mesa Plateau Horizon",
                "azimuth_deg": round((120.0 + celestial_rotation_deg) % 360.0, 1),
                "elevation_deg": 45.0,
                "description": "Brilliant constellation with 3 belt stars pointing toward Sirius."
            },
            {
                "id": "URSA_MAJOR",
                "name": "Ursa Major (The Big Dipper)",
                "category": "CIRCUMPOLAR",
                "key_star": "Merak & Dubhe (Pointers)",
                "aligned_landmark": "Hill 1 Ridge",
                "azimuth_deg": round((340.0 + celestial_rotation_deg) % 360.0, 1),
                "elevation_deg": 60.0,
                "description": "Pointer stars Merak and Dubhe aligning directly with the Spire apex."
            },
            {
                "id": "CYGNUS",
                "name": "Cygnus the Northern Cross",
                "category": "MAJOR",
                "key_star": "Deneb (Supergiant)",
                "aligned_landmark": "Northern Void Boundary",
                "azimuth_deg": round((45.0 + celestial_rotation_deg) % 360.0, 1),
                "elevation_deg": 75.0,
                "description": "Soaring swan cross pointing into the outer cosmic void."
            },
            {
                "id": "PLEIADES",
                "name": "Pleiades (Seven Sisters)",
                "category": "CLUSTER",
                "key_star": "Alcyone (Blue Cluster)",
                "aligned_landmark": "Hill 2 Summit",
                "azimuth_deg": round((210.0 + celestial_rotation_deg) % 360.0, 1),
                "elevation_deg": 50.0,
                "description": "Luminous blue stellar nursery glittering in deep indigo night."
            }
        ]

        # The 5 Classical Planetary Wanderers (moving independently against the stars!)
        planets = [
            {
                "id": "VENUS",
                "name": "Venus (The Evening / Morning Star)",
                "apparent_magnitude": -4.2,
                "color": "brilliant_silver",
                "azimuth_deg": round((sun_azimuth + 35.0) % 360.0, 1),
                "elevation_deg": round(max(5.0, sun_elevation + 15.0), 1),
                "telescope_details": "Displays crescent and gibbous phases like the Moon."
            },
            {
                "id": "MARS",
                "name": "Mars (The Red Wanderer)",
                "apparent_magnitude": -1.5,
                "color": "rust_crimson",
                "azimuth_deg": round((celestial_rotation_deg * 0.85 + 70.0) % 360.0, 1),
                "elevation_deg": round(35.0 + 10.0 * math.sin(self.sim_time_sec * 0.05), 1),
                "telescope_details": "Visible polar ice cap and dark volcanic basalt plains."
            },
            {
                "id": "JUPITER",
                "name": "Jupiter (King of Planets)",
                "apparent_magnitude": -2.7,
                "color": "warm_gold",
                "azimuth_deg": round((celestial_rotation_deg * 0.7 + 160.0) % 360.0, 1),
                "elevation_deg": round(55.0, 1),
                "telescope_details": "4 Galilean Moons (Io, Europa, Ganymede, Callisto) orbiting in linear plane!"
            },
            {
                "id": "SATURN",
                "name": "Saturn (The Jewel)",
                "apparent_magnitude": 0.4,
                "color": "pale_amber",
                "azimuth_deg": round((celestial_rotation_deg * 0.6 + 230.0) % 360.0, 1),
                "elevation_deg": round(40.0, 1),
                "telescope_details": "Spectacular ring system tilted at 26.7 degrees with Cassini division."
            }
        ]

        all_celestial = major_constellations + zodiac_constellations

        return {
            "is_night": is_night,
            "cycle_phase": round(cycle_phase, 3),
            "sun": {
                "elevation_deg": round(sun_elevation, 1),
                "azimuth_deg": round(sun_azimuth, 1)
            },
            "moon": {
                "elevation_deg": round(moon_elevation, 1),
                "azimuth_deg": round(moon_azimuth, 1),
                "phase": "Full Moon" if cycle_phase >= 0.75 else "Waxing Gibbous"
            },
            "spire_gnomon_shadow": {
                "length_m": round(shadow_len, 2),
                "azimuth_deg": round(shadow_azimuth, 1),
                "points_to": "NORTH" if abs(shadow_azimuth - 0.0) < 20 else f"{shadow_azimuth:.0f}°"
            },
            "celestial_rotation_deg": round(celestial_rotation_deg, 1),
            "stargazing_visibility": "EXCELLENT" if is_night else "DAYLIGHT_WASHED",
            "active_constellations": all_celestial,
            "zodiac_belt": zodiac_constellations,
            "planets": planets
        }

    def stargaze(self, azimuth_deg: float, elevation_deg: float, use_telescope: bool = False) -> Dict[str, Any]:
        """
        Observes the celestial vault at specified angles.
        Returns constellations, planetary wanderers, and optical details.
        """
        cel = self.get_celestial_state()
        magnification = 25.0 if use_telescope else 1.0

        matched_stars = []
        matched_planets = []
        fov_deg = 15.0 if use_telescope else 45.0

        for c in cel["active_constellations"]:
            d_az = abs(c["azimuth_deg"] - azimuth_deg)
            if d_az > 180:
                d_az = 360 - d_az
            d_el = abs(c["elevation_deg"] - elevation_deg)
            angular_dist = math.sqrt(d_az**2 + d_el**2)
            if angular_dist <= fov_deg:
                matched_stars.append({**c, "angular_distance_deg": round(angular_dist, 2)})

        for p in cel["planets"]:
            d_az = abs(p["azimuth_deg"] - azimuth_deg)
            if d_az > 180:
                d_az = 360 - d_az
            d_el = abs(p["elevation_deg"] - elevation_deg)
            angular_dist = math.sqrt(d_az**2 + d_el**2)
            if angular_dist <= fov_deg:
                matched_planets.append({**p, "angular_distance_deg": round(angular_dist, 2)})

        event = {
            "type": "STARGAZING_OBSERVATION",
            "sim_time": round(self.sim_time_sec, 2),
            "is_night": cel["is_night"],
            "azimuth_deg": azimuth_deg,
            "elevation_deg": elevation_deg,
            "use_telescope": use_telescope,
            "magnification": magnification,
            "sighted_constellations": matched_stars,
            "sighted_planets": matched_planets
        }
        self.events_log.append(event)
        return event

    def get_state(self) -> Dict[str, Any]:
        """Returns snapshot of current world telemetry."""
        hour_progress = self.sim_time_sec % self.hour_duration_sec
        time_to_reset = self.hour_duration_sec - hour_progress

        return {
            "sim_time_sec": round(self.sim_time_sec, 2),
            "current_hour": self.current_hour,
            "reset_count": self.reset_count,
            "continuous_mode": self.continuous_mode,
            "time_to_reset_sec": round(time_to_reset, 1),
            "warning_active": self.warning_active,
            "celestial": self.get_celestial_state(),
            "objects_count": len(self.objects),
            "shattered_fragments_count": len(self.shattered_fragments),
            "objects": {oid: obj.to_dict() for oid, obj in self.objects.items()},
            "recent_events": self.events_log[-10:],
            "landmarks": {
                "mesa": {"center": MESA_CENTER, "radius": MESA_RADIUS, "height": MESA_HEIGHT},
                "spire": {"pos": SPIRE_POS, "height": SPIRE_HEIGHT},
                "hill_1": {"center": HILL1_CENTER, "radius": HILL1_RADIUS, "height": HILL1_HEIGHT},
                "hill_2": {"center": HILL2_CENTER, "radius": HILL2_RADIUS, "height": HILL2_HEIGHT},
                "void_radius": ISLAND_RADIUS
            }
        }

"""
Biophysical Forearm & Dual-Modality Transduction Simulator (sEMG + PMUT)
========================================================================
Models an adult human forearm cross-section (R = 42.0 mm) containing 8 distinct
superficial and deep neuromuscular compartments, an subcutaneous ulnar bone
landmark for acoustic rotational registration, a 16-channel dry-polymer sEMG
circumferential ring, a 32-element (8 sectors x 4 depth gates) 7.5 MHz conformal
PMUT array, and a 3-axis high-G MEMS inertial shock sensor.

Simulated Non-Stationarities & Combat Perturbations:
- Perspiration / Sweat Salt-Bridging (S in [0, 1]): spatial crosstalk + SNR loss
- Neuromuscular Fatigue (F in [0, 1]): amplitude attenuation + frequency shift
- Conformal Sleeve Rotational Slip (delta_theta in [-22 deg, +22 deg])
- Dry-Elastomer PMUT Acoustic Air-Gap / Dust Loss (alpha_gap in [0, 0.70])
- Ballistic Weapon Recoil Shockwaves (15G - 48G impulse + acoustic bloom)
- Involuntary Muscle Spasms, Sprint Stumbles & EW/RF EMI Injection
"""

from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum
from typing import Dict, Optional, Tuple
import numpy as np


class ActionClass(IntEnum):
    IDLE = 0
    OP1_UAS_PINCH_GLIDE = 1       # Micro-UAS Flight Control (Index-Thumb Pinch & Glide)
    OP2_UGV_WRIST_TAP_POINT = 2   # Quadruped UGV Waypoint / Breach (Double Wrist Tap + Point)
    OP3_COMMS_SUBVOCAL_FLEX = 3   # Tactical Radio PTT / Channel (Sub-Vocal Middle Finger Flex)
    OP4_HUD_RING_SQUEEZE = 4      # AR HUD / Smart Weapon Target Lock (Deep Ring Finger Squeeze)
    OP5_EXO_ISOMETRIC_BOOST = 5   # Powered Exoskeleton Torque Boost (Isometric Co-Contraction)
    OP6_CUAS_PALM_SWEEP = 6       # Counter-UAS Jammer Sector Aim (Palm Splay + Sweeping Vector)
    HAZARD_RECOIL_SHOCK = 7       # Ballistic Weapon Recoil (>15G Mechanical Shockwave)
    HAZARD_SPASM_STUMBLE = 8      # Involuntary Spasm / Tactical Stumble / EW EMI Artifact


ACTION_NAMES: Dict[int, str] = {
    ActionClass.IDLE: "IDLE (Resting / Ambient Baseline)",
    ActionClass.OP1_UAS_PINCH_GLIDE: "Op-1: Micro-UAS Pinch & Glide",
    ActionClass.OP2_UGV_WRIST_TAP_POINT: "Op-2: Quadruped UGV Wrist Tap + Point",
    ActionClass.OP3_COMMS_SUBVOCAL_FLEX: "Op-3: Tactical Radio Sub-Vocal Flex",
    ActionClass.OP4_HUD_RING_SQUEEZE: "Op-4: AR HUD / Smart Weapon Ring Squeeze",
    ActionClass.OP5_EXO_ISOMETRIC_BOOST: "Op-5: Exoskeleton Isometric Boost",
    ActionClass.OP6_CUAS_PALM_SWEEP: "Op-6: Counter-UAS Jammer Palm Sweep",
    ActionClass.HAZARD_RECOIL_SHOCK: "HAZARD: Ballistic Weapon Recoil (>15G)",
    ActionClass.HAZARD_SPASM_STUMBLE: "HAZARD: Involuntary Spasm / Stumble / EMI",
}

SHORT_CLASS_LABELS = [
    "IDLE",
    "Op-1:UAS",
    "Op-2:UGV",
    "Op-3:Comms",
    "Op-4:HUD",
    "Op-5:Exo",
    "Op-6:C-UAS",
    "HAZ:Recoil",
    "HAZ:Spasm/EMI",
]

SYSTEM_ROUTING_MAP: Dict[int, Dict[str, str]] = {
    ActionClass.OP1_UAS_PINCH_GLIDE: {
        "system_id": "Op-1",
        "domain": "Micro-UAS (Black Hornet / Recon Swarm)",
        "gesture": "Index-Thumb Pinch & Glide",
        "command": "VELOCITY_VECTOR_PITCH_YAW",
        "safety_lock": "Auto-hover on signal loss",
    },
    ActionClass.OP2_UGV_WRIST_TAP_POINT: {
        "system_id": "Op-2",
        "domain": "Quadruped UGV (Ghost / Spot)",
        "gesture": "Double Wrist Tap + Point",
        "command": "DYNAMIC_WAYPOINT_BREACH",
        "safety_lock": "Collision avoidance override",
    },
    ActionClass.OP3_COMMS_SUBVOCAL_FLEX: {
        "system_id": "Op-3",
        "domain": "Tactical Radio Suite",
        "gesture": "Sub-Vocal Middle Finger Flex",
        "command": "PTT_CHANNEL_INCREMENT",
        "safety_lock": "Acoustic noise gate interlock",
    },
    ActionClass.OP4_HUD_RING_SQUEEZE: {
        "system_id": "Op-4",
        "domain": "AR HUD / Smart Weapon Optics",
        "gesture": "Deep Ring Finger Squeeze",
        "command": "LASER_RANGEFIND_TARGET_LOCK",
        "safety_lock": "Weapon safety toggle cross-check",
    },
    ActionClass.OP5_EXO_ISOMETRIC_BOOST: {
        "system_id": "Op-5",
        "domain": "Powered Exoskeleton",
        "gesture": "Isometric Forearm Pre-Tension",
        "command": "HIGH_TORQUE_LIFT_ASSIST",
        "safety_lock": "Joint over-extension clamp",
    },
    ActionClass.OP6_CUAS_PALM_SWEEP: {
        "system_id": "Op-6",
        "domain": "Counter-UAS Directional Jammer",
        "gesture": "Extended Palm Splay + Sweep",
        "command": "DIRECTIONAL_RF_SECTOR_AIM",
        "safety_lock": "Blue-force RF exclusion zone check",
    },
}

# ---------------------------------------------------------------------------
# Anatomical Forearm Parameters (8 Compartments in Polar Skin-Depth Coords)
# ---------------------------------------------------------------------------
FOREARM_RADIUS_MM = 42.0
ULNA_BONE_ANGLE_RAD = np.deg2rad(275.0)  # Subcutaneous ulnar crest at 275 deg (depth ~5.5 mm)
ULNA_BONE_DEPTH_MM = 5.5

# Compartment order:
# 0: FDS_MID  (25 deg,  8.0 mm)  - Superficial middle flex
# 1: FDP_IDX  (55 deg,  23.5 mm) - Deep index terminal flex
# 2: FPL_THB  (95 deg,  19.5 mm) - Deep thumb pinch
# 3: PT_BR    (130 deg, 12.5 mm) - Pronator teres / brachioradialis
# 4: ECR_WRS  (170 deg, 9.0 mm)  - Extensor carpi radialis
# 5: ED_SPLY  (215 deg, 8.5 mm)  - Extensor digitorum splay
# 6: ECU_ULN  (265 deg, 10.5 mm) - Extensor carpi ulnaris
# 7: FDP_RNG  (350 deg, 26.0 mm) - Deep ring finger squeeze (angularly close to FDS_MID!)
MUSCLE_NAMES = [
    "FDS_MID", "FDP_IDX", "FPL_THB", "PT_BR",
    "ECR_WRS", "ED_SPLY", "ECU_ULN", "FDP_RNG"
]
MUSCLE_ANGLES_RAD = np.deg2rad([25.0, 55.0, 95.0, 130.0, 170.0, 215.0, 265.0, 350.0])
MUSCLE_DEPTHS_MM = np.array([8.0, 23.5, 19.5, 12.5, 9.0, 8.5, 10.5, 26.0], dtype=np.float64)

# Sensor Geometry:
# 16 circumferential dry sEMG electrodes around [0, 2*pi)
SEMG_ANGLES_RAD = np.linspace(0.0, 2.0 * np.pi, 16, endpoint=False)
# 8 circumferential PMUT sectors x 4 depth gates (6, 14, 22, 30 mm) = 32 ultrasonic elements
PMUT_SECTOR_ANGLES_RAD = np.linspace(0.0, 2.0 * np.pi, 8, endpoint=False)
PMUT_DEPTH_GATES_MM = np.array([6.0, 14.0, 22.0, 30.0], dtype=np.float64)

# Micro-window: T = 16 time samples across a 3.2 ms acquisition window (5 kHz internal ADC)
WINDOW_SAMPLES = 16
WINDOW_DURATION_MS = 3.2


@dataclass
class ForearmSimulationConfig:
    """Configuration envelope for vectorized Monte Carlo generation."""
    sweat_range: Tuple[float, float] = (0.05, 0.85)
    fatigue_range: Tuple[float, float] = (0.05, 0.80)
    slip_deg_range: Tuple[float, float] = (-15.0, 15.0)
    pmut_gap_loss_range: Tuple[float, float] = (0.02, 0.35)
    emi_prob: float = 0.25          # Fraction of HAZARD_SPASM_STUMBLE trials that include RF/EMI injection
    weapon_safe_prob: float = 0.0   # Probability weapon safety is ON when Op-4 is tested (0 for pure decoding)
    blue_force_rf_prob: float = 0.0 # Probability blue-force RF exclusion is active when Op-6 is tested


def _build_canonical_muscle_templates() -> np.ndarray:
    """
    Constructs canonical spatiotemporal activation templates for classes 0..6
    with shape (7, WINDOW_SAMPLES, 8) representing normalized motor unit drive
    across T=16 micro-samples and M=8 forearm compartments.
    """
    t = np.linspace(0.0, 2.0 * np.pi, WINDOW_SAMPLES, endpoint=False)
    templates = np.zeros((7, WINDOW_SAMPLES, 8), dtype=np.float64)

    # Smooth onset envelope (motor recruitment ramp + limit-cycle oscillation)
    env = 0.55 + 0.45 * np.sin(0.5 * t)

    # Class 0: IDLE (near-zero tonic baseline)
    templates[ActionClass.IDLE] = 0.015

    # Class 1: OP1_UAS_PINCH_GLIDE
    # Coordinated FPL_THB (2) + deep FDP_IDX (1) pinch leading into PT_BR (3) + ECR_WRS (4) glide
    # Counter-clockwise phase progression creates strong positive bivector wedge area!
    templates[ActionClass.OP1_UAS_PINCH_GLIDE, :, 1] = 0.92 * env * (0.65 + 0.35 * np.cos(t))
    templates[ActionClass.OP1_UAS_PINCH_GLIDE, :, 2] = 0.95 * env * (0.65 + 0.35 * np.sin(t))
    templates[ActionClass.OP1_UAS_PINCH_GLIDE, :, 3] = 0.62 * env * (0.60 + 0.40 * np.sin(t - 0.9))
    templates[ActionClass.OP1_UAS_PINCH_GLIDE, :, 4] = 0.35 * env

    # Class 2: OP2_UGV_WRIST_TAP_POINT
    # Biphasic double wrist tap on ECR_WRS (4) + index extension/point ED_SPLY (5) & FDP_IDX (1)
    double_pulse = 0.50 + 0.50 * np.cos(2.0 * t)
    templates[ActionClass.OP2_UGV_WRIST_TAP_POINT, :, 4] = 0.98 * double_pulse
    templates[ActionClass.OP2_UGV_WRIST_TAP_POINT, :, 5] = 0.72 * env * (0.60 + 0.40 * np.sin(2.0 * t))
    templates[ActionClass.OP2_UGV_WRIST_TAP_POINT, :, 1] = 0.48 * env

    # Class 3: OP3_COMMS_SUBVOCAL_FLEX
    # Subtle superficial middle-finger isometric flex: isolated FDS_MID (0, depth 8mm)
    templates[ActionClass.OP3_COMMS_SUBVOCAL_FLEX, :, 0] = 0.78 * env * (0.70 + 0.30 * np.sin(t))
    templates[ActionClass.OP3_COMMS_SUBVOCAL_FLEX, :, 3] = 0.28 * env * (0.65 + 0.35 * np.cos(t))

    # Class 4: OP4_HUD_RING_SQUEEZE
    # Deep ring-finger squeeze: FDP_RNG (7, depth 26mm) + ulnar stabilization ECU_ULN (6)
    # Note: FDP_RNG (350 deg) is angularly adjacent to FDS_MID (25 deg), challenging sEMG-only!
    templates[ActionClass.OP4_HUD_RING_SQUEEZE, :, 7] = 0.96 * env * (0.68 + 0.32 * np.cos(t))
    templates[ActionClass.OP4_HUD_RING_SQUEEZE, :, 6] = 0.58 * env * (0.68 + 0.32 * np.sin(t))
    templates[ActionClass.OP4_HUD_RING_SQUEEZE, :, 0] = 0.22 * env  # Slight superficial co-activation

    # Class 5: OP5_EXO_ISOMETRIC_BOOST
    # Balanced agonist-antagonist co-contraction across superficial & deep flexors/extensors
    templates[ActionClass.OP5_EXO_ISOMETRIC_BOOST, :, 0] = 0.82 * env * (0.75 + 0.25 * np.cos(t))
    templates[ActionClass.OP5_EXO_ISOMETRIC_BOOST, :, 3] = 0.86 * env * (0.75 + 0.25 * np.sin(t))
    templates[ActionClass.OP5_EXO_ISOMETRIC_BOOST, :, 4] = 0.84 * env * (0.75 + 0.25 * np.cos(t + 0.6))
    templates[ActionClass.OP5_EXO_ISOMETRIC_BOOST, :, 6] = 0.78 * env * (0.75 + 0.25 * np.sin(t + 0.6))

    # Class 6: OP6_CUAS_PALM_SWEEP
    # Extended palm splay ED_SPLY (5) + clockwise sweeping phase ECU_ULN (6) -> ECR_WRS (4) -> PT_BR (3)
    # Opposite bivector chirality from OP1!
    templates[ActionClass.OP6_CUAS_PALM_SWEEP, :, 5] = 0.95 * env * (0.65 + 0.35 * np.cos(t))
    templates[ActionClass.OP6_CUAS_PALM_SWEEP, :, 6] = 0.74 * env * (0.65 + 0.35 * np.cos(t + 1.1))
    templates[ActionClass.OP6_CUAS_PALM_SWEEP, :, 4] = 0.68 * env * (0.65 + 0.35 * np.sin(t))
    templates[ActionClass.OP6_CUAS_PALM_SWEEP, :, 3] = 0.52 * env * (0.65 - 0.35 * np.sin(t))

    return templates


CANONICAL_TEMPLATES = _build_canonical_muscle_templates()


def generate_forearm_batch(
    batch_size: int,
    rng: np.random.Generator,
    config: Optional[ForearmSimulationConfig] = None,
    fixed_labels: Optional[np.ndarray] = None,
) -> Dict[str, np.ndarray]:
    """
    Generates a batch of biophysical forearm trajectories with dual-modality
    16-ch dry sEMG, 32-element PMUT (8 sectors x 4 depth gates), ulna bone landmark
    echoes, and MEMS high-G shock envelopes.

    Returns dictionary with:
        - labels: (B,) int64 ActionClass ground-truth
        - semg: (B, T, 16) float64 surface EMG envelopes / potentials
        - pmut: (B, T, 8, 4) float64 ultrasonic depth-resolved fascicle strain
        - ulna_echo: (B, 8) float64 static Gate-1 bone backscatter across 8 sectors
        - accel_g: (B,) float64 peak forearm acceleration in G
        - acoustic_bloom: (B,) float64 broadband ultrasonic saturation index
        - sweat: (B,) float64 perspiration level [0, 1]
        - fatigue: (B,) float64 neuromuscular fatigue [0, 1]
        - slip_deg: (B,) float64 rotational sleeve slip in degrees
        - pmut_gap_loss: (B,) float64 acoustic dry-coupling attenuation [0, 1]
        - weapon_safe_on: (B,) bool
        - blue_force_rf_zone: (B,) bool
    """
    cfg = config or ForearmSimulationConfig()
    B = int(batch_size)
    T = WINDOW_SAMPLES

    if fixed_labels is not None:
        labels = np.asarray(fixed_labels, dtype=np.int64)
        assert labels.shape == (B,)
    else:
        # Balanced sampling across all 9 classes (IDLE + Op1..6 + Recoil + Spasm/EMI)
        probs = np.array([0.10, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.09, 0.09])
        labels = rng.choice(9, size=B, p=probs)

    # Sample physiological & environmental perturbation state per trial
    sweat = rng.uniform(cfg.sweat_range[0], cfg.sweat_range[1], size=B)
    fatigue = rng.uniform(cfg.fatigue_range[0], cfg.fatigue_range[1], size=B)
    slip_deg = rng.uniform(cfg.slip_deg_range[0], cfg.slip_deg_range[1], size=B)
    slip_rad = np.deg2rad(slip_deg)
    pmut_gap_loss = rng.uniform(cfg.pmut_gap_loss_range[0], cfg.pmut_gap_loss_range[1], size=B)

    weapon_safe_on = rng.random(B) < cfg.weapon_safe_prob
    blue_force_rf_zone = rng.random(B) < cfg.blue_force_rf_prob

    # 1. Synthesize underlying neuromuscular compartment activations: (B, T, 8)
    safe_idx = np.clip(labels, 0, 6)
    muscle_act = CANONICAL_TEMPLATES[safe_idx].copy()  # (B, T, 8)

    # Add realistic inter-trial biological motor variability (tempo jitter + amplitude variability)
    motor_gain = rng.normal(1.0, 0.08, size=(B, 1, 8)).clip(0.72, 1.30)
    motor_noise = rng.normal(0.0, 0.032, size=(B, T, 8))
    muscle_act = np.clip(muscle_act * motor_gain + motor_noise, 0.0, None)

    # Default inertial acceleration (normal combat movement 0.8G - 4.8G)
    accel_g = rng.uniform(0.8, 4.8, size=B)
    acoustic_bloom = rng.uniform(0.01, 0.08, size=B)
    emi_flag = np.zeros(B, dtype=bool)

    # 2. Override Hazard Class 7: Ballistic Weapon Recoil (>15G impulse + reflexive startle)
    recoil_mask = labels == ActionClass.HAZARD_RECOIL_SHOCK
    n_recoil = int(np.sum(recoil_mask))
    if n_recoil > 0:
        accel_g[recoil_mask] = rng.uniform(16.5, 46.0, size=n_recoil)
        acoustic_bloom[recoil_mask] = rng.uniform(0.65, 1.35, size=n_recoil)
        # Sharp mechanical shock pulse + pan-muscle reflexive startle co-contraction
        t_idx = np.arange(T)[None, :, None]
        shock_env = np.exp(-((t_idx - 4.0) ** 2) / 5.5)
        startle = rng.uniform(0.55, 1.35, size=(n_recoil, 1, 8)) * shock_env
        jitter = np.abs(rng.normal(0.0, 0.28, size=(n_recoil, T, 8)))
        muscle_act[recoil_mask] = startle + jitter

    # 3. Override Hazard Class 8: Involuntary Spasm / Tactical Stumble / EW RF-EMI Injection
    spasm_mask = labels == ActionClass.HAZARD_SPASM_STUMBLE
    n_spasm = int(np.sum(spasm_mask))
    if n_spasm > 0:
        spasm_indices = np.flatnonzero(spasm_mask)
        is_emi = rng.random(n_spasm) < cfg.emi_prob
        emi_flag[spasm_indices] = is_emi

        # Sub-case A: Chaotic involuntary muscle spasm / stumble impact (no coherent phase loop, high jitter)
        non_emi_idx = spasm_indices[~is_emi]
        if len(non_emi_idx) > 0:
            accel_g[non_emi_idx] = rng.uniform(6.5, 14.4, size=len(non_emi_idx))
            # Erratic high-frequency random spikes across random compartments (zero closed-orbit coherence)
            random_comp = rng.exponential(0.35, size=(len(non_emi_idx), T, 8))
            random_mask = (rng.random((len(non_emi_idx), 1, 8)) > 0.45).astype(np.float64)
            muscle_act[non_emi_idx] = random_comp * random_mask + 0.08

        # Sub-case B: Electronic Warfare / RF EMI burst coupled onto dry sEMG electrodes (normal IDLE/mild arm state)
        emi_idx = spasm_indices[is_emi]
        if len(emi_idx) > 0:
            accel_g[emi_idx] = rng.uniform(1.0, 4.2, size=len(emi_idx))
            muscle_act[emi_idx] = rng.uniform(0.01, 0.06, size=(len(emi_idx), T, 8))

    # 4. Apply Neuromuscular Fatigue Physics:
    # Surface electrical amplitude compresses strongly with fatigue & metabolic acidosis;
    # physical fascicle shortening (PMUT) compresses much more mildly under isometric effort.
    semg_fatigue_scale = (1.0 - 0.42 * fatigue)[:, None, None]
    pmut_fatigue_scale = (1.0 - 0.18 * fatigue)[:, None, None]

    # 5. Forward Volume-Conduction Model for 16-Channel Dry sEMG with Rotational Slip:
    # Sensor angles shifted by sleeve slip: theta_sensor_effective = SEMG_ANGLES_RAD + slip_rad
    # Shape: (B, 16, 8) angular difference between shifted sEMG electrodes and anatomical muscles
    dtheta_semg = SEMG_ANGLES_RAD[None, :, None] + slip_rad[:, None, None] - MUSCLE_ANGLES_RAD[None, None, :]
    chord_mm = 2.0 * (FOREARM_RADIUS_MM - 0.5 * MUSCLE_DEPTHS_MM[None, None, :]) * np.abs(np.sin(0.5 * dtheta_semg))
    dist3d_sq = MUSCLE_DEPTHS_MM[None, None, :] ** 2 + chord_mm ** 2  # (B, 16, 8)

    # Volume conductor decay: superficial muscles (~8mm) yield ~0.85 unit amplitude;
    # deep muscles (23.5-26 mm) are attenuated ~8-10x relative to superficial muscles!
    G_semg = (280.0 / (dist3d_sq + 36.0)) * np.exp(-MUSCLE_DEPTHS_MM[None, None, :] / 13.5)  # (B, 16, 8)

    # Project muscle activations (B, T, 8) -> raw sEMG (B, T, 16) via Apple AMX BLAS matmul
    semg_clean = np.matmul(muscle_act * semg_fatigue_scale, G_semg.transpose(0, 2, 1))

    # Sweat Salt-Bridging Crosstalk: conductive sweat film blurs neighboring electrodes around the ring
    s = sweat[:, None, None]
    semg_blurred = (
        (1.0 - 0.72 * s) * semg_clean
        + 0.25 * s * (np.roll(semg_clean, 1, axis=2) + np.roll(semg_clean, -1, axis=2))
        + 0.11 * s * (np.roll(semg_clean, 2, axis=2) + np.roll(semg_clean, -2, axis=2))
    )

    # Sweat contact impedance baseline drift + thermal noise
    semg_noise_std = 0.030 + 0.085 * sweat[:, None, None]
    semg = semg_blurred + rng.normal(0.0, 1.0, size=(B, T, 16)) * semg_noise_std

    # Motion artifact on dry sEMG during recoil or high-G stumble
    high_g_excess = np.maximum(0.0, accel_g - 5.5)[:, None, None]
    if np.any(high_g_excess > 0):
        semg += high_g_excess * 0.085 * rng.normal(0.8, 0.5, size=(B, T, 16))

    # Inject EW / RF EMI directly into dry sEMG channels (PMUT piezoelectric elements remain acoustically clean!)
    if np.any(emi_flag):
        n_emi = int(np.sum(emi_flag))
        t_vec = np.arange(T)[None, :, None]
        emi_wave = 0.85 * np.sin(1.7 * t_vec + rng.uniform(0, 2 * np.pi, size=(n_emi, 1, 16)))
        semg[emi_flag] += np.abs(emi_wave) + rng.normal(0.0, 0.22, size=(n_emi, T, 16))

    # 6. Forward Ultrasonic Pulse-Echo Model for 32-Element PMUT (8 Sectors x 4 Depth Gates):
    # Viscoelastic Electromechanical Delay (EMD): muscle mechanical strain low-pass filters
    # rapid ballistic 2nd-harmonic electrical bursts (pure vectorized 5-tap filter along T)
    padded = np.pad(muscle_act, ((0, 0), (2, 2), (0, 0)), mode="edge")
    muscle_strain = (
        0.15 * padded[:, 0:T, :]
        + 0.25 * padded[:, 1:T + 1, :]
        + 0.30 * padded[:, 2:T + 2, :]
        + 0.20 * padded[:, 3:T + 3, :]
        + 0.10 * padded[:, 4:T + 4, :]
    )
    # Fast sub-vocal micro-twitch (Op-3) produces strong electrical MUAPs with subtle mechanical displacement
    op3_mask = labels == ActionClass.OP3_COMMS_SUBVOCAL_FLEX
    if np.any(op3_mask):
        muscle_strain[op3_mask] *= 0.42

    # Focused 12.5-deg lateral ultrasonic beam for deep/superficial muscle compartments: (B, 8, 8_muscles)
    dtheta_pmut = PMUT_SECTOR_ANGLES_RAD[None, :, None] + slip_rad[:, None, None] - MUSCLE_ANGLES_RAD[None, None, :]
    ang_weight = np.exp(-0.5 * (np.sin(0.5 * dtheta_pmut) / np.sin(0.5 * np.deg2rad(12.5))) ** 2)  # (B, 8, 8)

    # Axial depth gating across the 4 gates (6, 14, 22, 30 mm) vs MUSCLE_DEPTHS_MM: shape (4, 8_muscles)
    depth_weight = np.exp(-0.5 * ((PMUT_DEPTH_GATES_MM[:, None] - MUSCLE_DEPTHS_MM[None, :]) / 4.5) ** 2)  # (4, 8)

    # Combined 3D ultrasonic sensitivity tensor: (B, 32_elements, 8_muscles) via BLAS matmul
    G_pmut_flat = (ang_weight[:, :, None, :] * depth_weight[None, None, :, :]).reshape(B, 32, 8)

    # Dry-elastomer acoustic coupling efficiency: (1 - pmut_gap_loss)
    coupling = (1.0 - pmut_gap_loss)[:, None, None, None]
    pmut_clean = coupling * np.matmul(
        muscle_strain * pmut_fatigue_scale, G_pmut_flat.transpose(0, 2, 1)
    ).reshape(B, T, 8, 4)

    # Add ultrasonic speckle noise + ballistic recoil broadband acoustic bloom
    pmut_noise = rng.normal(0.0, 0.032, size=(B, T, 8, 4))
    bloom_term = np.where(
        (recoil_mask)[:, None, None, None],
        acoustic_bloom[:, None, None, None] * np.abs(rng.normal(0.65, 0.25, size=(B, T, 8, 4))),
        0.0,
    )
    pmut = pmut_clean + pmut_noise + bloom_term

    # 7. Subcutaneous Ulna Crest Acoustic Landmark Echo (28-deg Nyquist-compliant Gate-1 fan beam):
    # Satisfies spatial Nyquist across the 45-deg 8-sector ring (< 0.3 deg rotational slip error!)
    dtheta_ulna = PMUT_SECTOR_ANGLES_RAD[None, :] + slip_rad[:, None] - ULNA_BONE_ANGLE_RAD
    ulna_echo = (1.0 - 0.5 * pmut_gap_loss)[:, None] * np.exp(
        -0.5 * (np.sin(0.5 * dtheta_ulna) / np.sin(0.5 * np.deg2rad(28.0))) ** 2
    ) + rng.normal(0.0, 0.018, size=(B, 8))

    return {
        "labels": labels,
        "semg": semg,
        "pmut": pmut,
        "ulna_echo": ulna_echo,
        "accel_g": accel_g,
        "acoustic_bloom": acoustic_bloom,
        "sweat": sweat,
        "fatigue": fatigue,
        "slip_deg": slip_deg,
        "pmut_gap_loss": pmut_gap_loss,
        "emi_flag": emi_flag,
        "weapon_safe_on": weapon_safe_on,
        "blue_force_rf_zone": blue_force_rf_zone,
    }

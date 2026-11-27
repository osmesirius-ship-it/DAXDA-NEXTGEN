"""
Clifford Geometric Algebra Cl(8,2) Phase-Orbit & Invariant Decoder Engine
=========================================================================
Embeds dual-modality 16-ch dry sEMG and 32-element (8x4) PMUT time-series
into the 10-dimensional pseudo-Euclidean generator space R^{8,2} generating
the 1,024-blade Clifford algebra Cl(8,2) with metric signature:
    g = diag(+1, +1, +1, +1, +1, +1, +1, +1, -1, -1)

Key Mathematical Mechanisms:
1. Ulnar-Landmark Rotor Registration (R_slip^-1): Estimates continuous sleeve
   rotational slip from the subcutaneous ulnar crest ultrasonic reflection and
   counter-rotates both sEMG (16-ch) and PMUT (8-sector) manifolds via exact
   Fourier phase shifting.
2. Fatigue-Invariant Energy Normalization: Cancels peripheral amplitude drop
   while preserving inter-compartment geometry and depth-gate strain ratios.
3. Exact 45-Blade Grade-2 Bivector Wedge Product <X(t) ^ dX/dt>_2: Captures
   closed phase-orbit chirality (e.g., distinguishing Op-1 counter-clockwise
   pinch-glide from Op-6 clockwise palm sweep) and phase-loop coherence.
4. Lorentzian Null-Cone Horizon (Q_{8,2} = sum_{i=1}^8 x_i^2 - x_9^2 - x_{10}^2 <= 0):
   Projects ballistic recoil shocks, chaotic spasms, stumbles, and EW/RF EMI
   bursts onto timelike/null hazard cones for fail-closed dissipation.
"""

from __future__ import annotations
from dataclasses import dataclass
import numpy as np

from .forearm_physics import (
    SEMG_ANGLES_RAD,
    PMUT_SECTOR_ANGLES_RAD,
    ULNA_BONE_ANGLE_RAD,
)


@dataclass
class Cl82InvariantFeatures:
    """Extracted geometric invariants and baseline comparison features for a batch B."""
    # Core Cl(8,2) invariants
    cl82_feature_vector: np.ndarray     # (B, D_cl82) full fatigue/slip-invariant feature vector
    quadratic_norm_q82: np.ndarray      # (B,) <X ~X>_0 = ||X_+||^2 - x_9^2 - x_10^2
    bivector_28_spatial: np.ndarray     # (B, 28) spatial grade-2 bivectors e_i ^ e_j
    bivector_17_hyperbolic: np.ndarray  # (B, 17) mixed Lorentzian & e_9^e_10 bivectors
    bivector_curvature: np.ndarray      # (B,) normalized kappa_B curvature invariant
    cross_modal_coherence: np.ndarray   # (B,) cosine/mutual coherence between sEMG & superficial PMUT
    phase_smoothness: np.ndarray        # (B,) ratio of smooth low-mode orbital energy to erratic jitter
    active_energy: np.ndarray           # (B,) fused neuromuscular activation magnitude (for IDLE gate)
    estimated_slip_deg: np.ndarray      # (B,) ulnar-landmark estimated sleeve slip in degrees

    # Baseline comparison feature matrices (for ablation studies)
    semg_only_features: np.ndarray      # (B, D_semg) raw sEMG time/rms/diff features
    pmut_only_features: np.ndarray      # (B, D_pmut) raw PMUT sector-depth features
    naive_fusion_features: np.ndarray   # (B, D_semg + D_pmut) unaligned, unnormalized fusion


def _fourier_derotate_ring(signal: np.ndarray, shift_rad: np.ndarray, axis: int = -1) -> np.ndarray:
    """
    Applies a continuous azimuthal rotation shift (-shift_rad) along a circular
    sensor ring of size K (e.g., K=16 for sEMG or K=8 for PMUT sectors) using
    exact real FFT phase rotation.
    """
    moved = np.moveaxis(signal, axis, -1)
    K = moved.shape[-1]
    spec = np.fft.rfft(moved, axis=-1)  # (..., K//2 + 1)
    freqs = np.arange(spec.shape[-1], dtype=np.float64)  # harmonic index m = 0, 1, ...

    # Reshape shift_rad to broadcast against spec
    extra_dims = spec.ndim - 1 - shift_rad.ndim
    phase_arg = shift_rad.reshape(shift_rad.shape + (1,) * (extra_dims + 1)) * freqs
    rotated_spec = spec * np.exp(1j * phase_arg)

    derotated = np.fft.irfft(rotated_spec, n=K, axis=-1)
    return np.moveaxis(derotated, -1, axis)


def estimate_ulnar_slip_rad(ulna_echo: np.ndarray) -> np.ndarray:
    """
    Estimates azimuthal sleeve slip angle (radians) from the 8-sector Gate-1
    subcutaneous ulna crest backscatter profile via circular first-moment phase.
    Note: If sensor ring slipped by +slip_rad, sensor k is at angle theta_k + slip_rad,
    so peak echo appears at theta_k = ULNA_BONE_ANGLE_RAD - slip_rad.
    """
    weights = np.clip(ulna_echo, 0.0, None)
    c_re = np.sum(weights * np.cos(PMUT_SECTOR_ANGLES_RAD)[None, :], axis=1)
    c_im = np.sum(weights * np.sin(PMUT_SECTOR_ANGLES_RAD)[None, :], axis=1)
    observed_peak_angle = np.arctan2(c_im, c_re)
    raw_diff = ULNA_BONE_ANGLE_RAD - observed_peak_angle
    # Wrap to [-pi, pi]
    slip_est = (raw_diff + np.pi) % (2.0 * np.pi) - np.pi
    return slip_est


def extract_cl82_invariants(batch: Dict[str, np.ndarray]) -> Cl82InvariantFeatures:
    """
    Projects raw forearm dual-modality streams into Cl(8,2) and extracts
    rotational, fatigue, and Lorentzian null-cone invariants alongside
    ablation baseline features.
    """
    semg = batch["semg"]                    # (B, T, 16)
    pmut = batch["pmut"]                    # (B, T, 8, 4)
    ulna_echo = batch["ulna_echo"]          # (B, 8)
    accel_g = batch["accel_g"]              # (B,)
    acoustic_bloom = batch["acoustic_bloom"]  # (B,)

    B, T, _ = semg.shape
    eps = 1e-6

    # -----------------------------------------------------------------------
    # A. Baseline Ablation Features (Unaligned / Non-Clifford)
    # -----------------------------------------------------------------------
    semg_mean = np.mean(semg, axis=1)                        # (B, 16)
    semg_rms = np.sqrt(np.mean(semg ** 2, axis=1) + eps)     # (B, 16)
    semg_slope = semg[:, -1, :] - semg[:, 0, :]              # (B, 16)
    semg_only_features = np.concatenate([semg_mean, semg_rms, semg_slope], axis=1)  # (B, 48)

    pmut_mean = np.mean(pmut, axis=1).reshape(B, 32)         # (B, 32)
    pmut_std = np.std(pmut, axis=1).reshape(B, 32)           # (B, 32)
    pmut_only_features = np.concatenate([pmut_mean, pmut_std], axis=1)  # (B, 64)

    naive_fusion_features = np.concatenate([semg_only_features, pmut_only_features], axis=1)  # (B, 112)

    # -----------------------------------------------------------------------
    # B. Step 1: Ulnar-Landmark Rotor De-Rotation (Sleeve Slip Compensation)
    # -----------------------------------------------------------------------
    slip_est_rad = estimate_ulnar_slip_rad(ulna_echo)  # (B,)
    # If sensor k sits at theta_k + slip, shifting signal by -slip restores canonical anatomy:
    # In _fourier_derotate_ring, exp(+i m * shift) evaluates signal(theta + shift);
    # since measured_ring(theta) = canonical(theta + slip), evaluating measured_ring(theta - slip)
    # recovers canonical(theta), which corresponds to passing -slip_est_rad!
    semg_aligned = _fourier_derotate_ring(semg, -slip_est_rad, axis=2)   # (B, T, 16)
    pmut_aligned = _fourier_derotate_ring(pmut, -slip_est_rad, axis=2)   # (B, T, 8, 4)

    # Downsample 16 aligned sEMG electrodes to 8 anatomical sectors via circular kernel
    semg_8 = 0.5 * (semg_aligned[:, :, 0::2] + 0.5 * (
        np.roll(semg_aligned, 1, axis=2)[:, :, 0::2] + np.roll(semg_aligned, -1, axis=2)[:, :, 0::2]
    ))  # (B, T, 8)

    # Depth-integrated & depth-stratified PMUT signals
    pmut_surf = pmut_aligned[:, :, :, 0] + 0.7 * pmut_aligned[:, :, :, 1]   # Superficial gates 1-2 (6-14mm)
    pmut_deep = pmut_aligned[:, :, :, 2] + 1.1 * pmut_aligned[:, :, :, 3]   # Deep gates 3-4 (22-30mm)
    pmut_total = pmut_surf + pmut_deep                                       # (B, T, 8)

    # -----------------------------------------------------------------------
    # C. Step 2: Cross-Modal Coherence & Temporal Smoothness Diagnostics
    # -----------------------------------------------------------------------
    semg_prof = np.clip(np.mean(semg_8, axis=1), 0.0, None)          # (B, 8)
    pmut_surf_prof = np.clip(np.mean(pmut_surf, axis=1), 0.0, None)  # (B, 8)
    pmut_deep_prof = np.clip(np.mean(pmut_deep, axis=1), 0.0, None)  # (B, 8)
    pmut_tot_prof = pmut_surf_prof + pmut_deep_prof                  # (B, 8)

    semg_norm_mag = np.linalg.norm(semg_prof, axis=1)
    pmut_norm_mag = np.linalg.norm(pmut_tot_prof, axis=1)

    # Expected volume-conducted surface profile from PMUT depth profile (blurred across neighbors like tissue):
    expected_surf = 1.15 * pmut_surf_prof + 0.25 * pmut_deep_prof
    expected_surf = 0.50 * expected_surf + 0.25 * (
        np.roll(expected_surf, 1, axis=1) + np.roll(expected_surf, -1, axis=1)
    )
    exp_norm_mag = np.linalg.norm(expected_surf, axis=1)

    # Directional spatial cosine agreement + asymmetric EMI excess penalty:
    # (Deep or sweat-blurred gestures remain coherent; EW EMI spikes semg_norm_mag with zero pmut_norm_mag!)
    cos_sim = np.sum(semg_prof * expected_surf, axis=1) / (semg_norm_mag * exp_norm_mag + 1e-4)
    emi_excess_ratio = np.maximum(0.0, semg_norm_mag - 3.2 * pmut_norm_mag - 0.18) / (semg_norm_mag + 0.10)
    cross_modal_coherence = np.clip((0.35 + 0.65 * cos_sim) * (1.0 - emi_excess_ratio), 0.0, 1.0)

    # Fused 8-sector spatial activation X_+(t): combines fast electrical onset + 3D deep acoustic strain
    x_pos_raw = 0.38 * semg_8 + 0.62 * pmut_total  # (B, T, 8)
    active_energy = np.sqrt(np.mean(np.sum(x_pos_raw ** 2, axis=2), axis=1))  # (B,)

    # Temporal phase smoothness vs. chaotic high-frequency spasm jitter:
    dx_dt = np.gradient(x_pos_raw, axis=1)
    d2x_dt2 = np.gradient(dx_dt, axis=1)
    vel_energy = np.mean(np.sum(dx_dt ** 2, axis=2), axis=1) + 1e-5
    jerk_energy = np.mean(np.sum(d2x_dt2 ** 2, axis=2), axis=1)
    phase_smoothness = 1.0 / (1.0 + (jerk_energy / vel_energy))

    # -----------------------------------------------------------------------
    # D. Step 3: Construct 10D Trajectory in Cl(8,2) Generator Space R^{8,2}
    # -----------------------------------------------------------------------
    # Fatigue-invariant scale factor per trial (floored so IDLE stays near origin)
    scale = np.maximum(active_energy, 0.14)[:, None, None]
    x_pos = x_pos_raw / scale  # (B, T, 8) — positive-signature basis e_1..e_8 (+1)

    # Negative-signature coordinate e_9 (-1): Cross-modal EMI divergence + chaotic spasm jitter
    emi_mismatch = np.maximum(0.0, semg_norm_mag - 3.0 * pmut_norm_mag - 0.18)
    jitter_excess = np.maximum(0.0, (jerk_energy / vel_energy) - 1.15)
    x9_scalar = 1.80 * emi_mismatch + 0.95 * jitter_excess
    t_grid = np.linspace(0.0, 1.0, T)[None, :, None]
    x9 = x9_scalar[:, None, None] * (0.75 + 0.50 * t_grid)  # (B, T, 1)

    # Negative-signature coordinate e_10 (-1): Inertial ballistic shock + ultrasonic bloom
    shock_excess = np.maximum(0.0, (accel_g - 5.8) / 4.2) + 1.6 * np.maximum(0.0, acoustic_bloom - 0.25)
    x10 = shock_excess[:, None, None] * (1.15 - 0.30 * t_grid)  # (B, T, 1)

    # Full 10D multivector grade-1 trajectory X(t) in Cl(8,2): shape (B, T, 10)
    X_10 = np.concatenate([x_pos, x9, x10], axis=2)
    dX_10 = np.gradient(X_10, axis=1)

    # Exact Cl(8,2) Scalar Quadratic Norm: Q_{8,2} = sum_{i=1}^8 x_i^2 - x_9^2 - x_10^2
    q82_t = np.sum(X_10[:, :, :8] ** 2, axis=2) - X_10[:, :, 8] ** 2 - X_10[:, :, 9] ** 2
    quadratic_norm_q82 = np.mean(q82_t, axis=1)  # (B,)

    # -----------------------------------------------------------------------
    # E. Step 4: Exact 45-Blade Grade-2 Bivector Wedge Product <X ^ dX/dt>_2
    # -----------------------------------------------------------------------
    # BLAS-accelerated outer temporal contraction: (B, 10, T) @ (B, T, 10) -> (B, 10, 10)
    xt_dx = np.matmul(X_10.transpose(0, 2, 1), dX_10)
    wedge_matrix = (xt_dx - xt_dx.transpose(0, 2, 1)) / float(T)

    iu_spatial = np.triu_indices(8, k=1)  # 28 spatial bivectors e_i ^ e_j (1 <= i < j <= 8)
    bivector_28_spatial = wedge_matrix[:, iu_spatial[0], iu_spatial[1]]  # (B, 28)

    # 16 mixed Lorentzian boost bivectors (e_1..8 ^ e_9 and e_1..8 ^ e_10) + 1 hyperbolic (e_9 ^ e_10) = 17
    biv_e9 = wedge_matrix[:, :8, 8]      # (B, 8)
    biv_e10 = wedge_matrix[:, :8, 9]     # (B, 8)
    biv_9_10 = wedge_matrix[:, 8:9, 9]   # (B, 1)
    bivector_17_hyperbolic = np.concatenate([biv_e9, biv_e10, biv_9_10], axis=1)  # (B, 17)

    # Exact Bivector Curvature kappa_B via Lagrange's Identity: ||u ^ v||^2 = ||u||^2 ||v||^2 - (u . v)^2
    u_vel = dX_10[:, :, :8]
    v_acc = np.gradient(u_vel, axis=1)
    u_sq = np.sum(u_vel ** 2, axis=2)
    v_sq = np.sum(v_acc ** 2, axis=2)
    uv_dot = np.sum(u_vel * v_acc, axis=2)
    curv_norm = np.sqrt(np.maximum(0.0, u_sq * v_sq - uv_dot ** 2))
    speed_cubed = (np.sqrt(u_sq) ** 3) + 1e-3
    bivector_curvature = np.mean(curv_norm / speed_cubed, axis=1)  # (B,)

    # -----------------------------------------------------------------------
    # F. Step 5: Assemble Fatigue- & Slip-Invariant Cl(8,2) Feature Descriptor
    # -----------------------------------------------------------------------
    # 1. Normalized aligned spatial mean profile (8) & temporal harmonic magnitudes (8x2 = 16)
    x_pos_mean = np.mean(x_pos, axis=1)  # (B, 8)
    fft_x = np.fft.rfft(x_pos, axis=1)   # (B, 9, 8)
    harm1_mag = np.abs(fft_x[:, 1, :])   # Fundamental cycle (Op1/Op3/Op4/Op5/Op6)
    harm2_mag = np.abs(fft_x[:, 2, :])   # Double-tap 2nd harmonic (Op2!)

    # 2. Fatigue-invariant PMUT 4-gate depth profile normalized per trial (8x4 = 32)
    pmut_aligned_mean = np.mean(pmut_aligned, axis=1)  # (B, 8, 4)
    pmut_norm_factor = np.maximum(np.linalg.norm(pmut_aligned_mean.reshape(B, 32), axis=1), 0.10)[:, None, None]
    pmut_depth_inv = (pmut_aligned_mean / pmut_norm_factor).reshape(B, 32)

    # 3. Shift-invariant circular autocorrelation around the 8 sectors (backup if ulna echo is noisy!)
    circ_autocorr = np.stack(
        [np.sum(x_pos_mean * np.roll(x_pos_mean, shift=k, axis=1), axis=1) for k in range(5)],
        axis=1,
    )  # (B, 5)

    # 4. Normalized aligned sEMG profile (8)
    semg_scale = np.maximum(np.linalg.norm(semg_prof, axis=1), 0.08)[:, None]
    semg_inv = semg_prof / semg_scale  # (B, 8)

    # Combine into strictly projective scale- & slip-invariant Cl(8,2) directional descriptor:
    # Amplitude/hazard scalars (active_energy, Q_82, coherence, smoothness) are routed
    # exclusively to the AOG_1 safety firewall so peripheral fatigue & coupling attenuation
    # remain 100% mathematically orthogonal to directional gesture classification!
    cl82_feature_vector = np.concatenate(
        [
            x_pos_mean,                 # 8 (fatigue-normalized aligned spatial profile)
            harm1_mag,                  # 8 (fundamental cycle)
            harm2_mag,                  # 8 (2nd harmonic double-tap signature)
            pmut_depth_inv,             # 32 (normalized 4-gate depth ratios: 6mm..30mm)
            bivector_28_spatial * 6.0,  # 28 (phase-orbit chirality CCW vs CW)
            circ_autocorr,              # 5 (shift-invariant circular autocorrelation)
            semg_inv,                   # 8 (normalized aligned fast sEMG profile)
        ],
        axis=1,
    )

    return Cl82InvariantFeatures(
        cl82_feature_vector=cl82_feature_vector,
        quadratic_norm_q82=quadratic_norm_q82,
        bivector_28_spatial=bivector_28_spatial,
        bivector_17_hyperbolic=bivector_17_hyperbolic,
        bivector_curvature=bivector_curvature,
        cross_modal_coherence=cross_modal_coherence,
        phase_smoothness=phase_smoothness,
        active_energy=active_energy,
        estimated_slip_deg=np.rad2deg(slip_est_rad),
        semg_only_features=semg_only_features,
        pmut_only_features=pmut_only_features,
        naive_fusion_features=naive_fusion_features,
    )

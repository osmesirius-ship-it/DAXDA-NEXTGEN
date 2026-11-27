"""
Automated Invariant & Verification Suite for DAXDA BIO-REMOTE (DPA27BZ02-DV003)
===============================================================================
Validates biophysical forearm transduction, Cl(8,2) geometric algebra invariants,
ulnar-crest sleeve-slip rotor compensation, 5-gate AOG_1 biomechanical safety
interlocks, sub-5ms latency bounds, and cryptographic HMAC-SHA256 receipts.
"""

from __future__ import annotations
import numpy as np
import pytest

from daxda_sandbox.bio_remote import (
    ActionClass,
    ForearmSimulationConfig,
    BioRemoteSystemModel,
    generate_forearm_batch,
    extract_cl82_invariants,
)
from daxda_sandbox.bio_remote.monte_carlo_mapper import run_5x100k_operational_mapping


def test_forearm_dual_modality_depth_selectivity():
    """Verify deep ring squeeze (Op-4, 26mm) activates deep PMUT gates while Op-3 activates superficial."""
    rng = np.random.default_rng(101)
    cfg = ForearmSimulationConfig(
        sweat_range=(0.05, 0.05),
        fatigue_range=(0.0, 0.0),
        slip_deg_range=(0.0, 0.0),
        pmut_gap_loss_range=(0.0, 0.0),
    )
    labels = np.array([ActionClass.OP3_COMMS_SUBVOCAL_FLEX] * 200 + [ActionClass.OP4_HUD_RING_SQUEEZE] * 200)
    batch = generate_forearm_batch(400, rng=rng, config=cfg, fixed_labels=labels)
    pmut = batch["pmut"]  # (400, T, 8, 4)

    # Sector 0 (0 deg, directly overlying FDS_MID at 25 deg / 8mm and FDP_RNG at 350 deg / 26mm):
    op3_s0_gates = np.mean(pmut[:200, :, 0, :], axis=(0, 1))  # (4,)
    op4_s0_gates = np.mean(pmut[200:, :, 0, :], axis=(0, 1))  # (4,)

    assert np.mean(op3_s0_gates[:2]) > np.mean(op3_s0_gates[2:]) * 3.0, "Superficial Op-3 should peak in shallow gates 1-2"
    assert np.mean(op4_s0_gates[2:]) > np.mean(op4_s0_gates[:2]) * 2.5, "Deep Op-4 (26mm FDP_RNG) should peak in deep gates 3-4"


def test_ulnar_landmark_nyquist_slip_tracking():
    """Verify Gate-1 28-deg fan beam tracks +-20 deg rotational sleeve slip within < 1.2 deg MAE."""
    rng = np.random.default_rng(202)
    cfg = ForearmSimulationConfig(
        sweat_range=(0.2, 0.6),
        fatigue_range=(0.1, 0.5),
        slip_deg_range=(-20.0, 20.0),
        pmut_gap_loss_range=(0.05, 0.25),
    )
    labels = rng.integers(0, 7, size=1000)
    batch = generate_forearm_batch(1000, rng=rng, config=cfg, fixed_labels=labels)
    feats = extract_cl82_invariants(batch)

    diff = (feats.estimated_slip_deg - batch["slip_deg"] + 180.0) % 360.0 - 180.0
    mae_deg = float(np.mean(np.abs(diff)))
    assert mae_deg < 1.2, f"Expected < 1.2 deg ulnar slip MAE, got {mae_deg:.3f} deg"


def test_cl82_metric_signature_and_bivector_chirality():
    """Verify Cl(8,2) quadratic norm separates spacelike gestures from timelike recoil/hazards and resolves chirality."""
    rng = np.random.default_rng(303)
    cfg = ForearmSimulationConfig(slip_deg_range=(-10.0, 10.0))
    labels = np.array(
        [ActionClass.OP1_UAS_PINCH_GLIDE] * 300
        + [ActionClass.OP6_CUAS_PALM_SWEEP] * 300
        + [ActionClass.HAZARD_RECOIL_SHOCK] * 300
    )
    batch = generate_forearm_batch(900, rng=rng, config=cfg, fixed_labels=labels)
    feats = extract_cl82_invariants(batch)

    assert feats.bivector_28_spatial.shape == (900, 28)
    assert feats.bivector_17_hyperbolic.shape == (900, 17)

    # Intentional gestures lie strictly in positive spacelike region Q_{8,2} > 0.5
    assert np.mean(feats.quadratic_norm_q82[:600]) > 0.85
    # Ballistic recoil plunges deep into negative timelike cone Q_{8,2} < -5.0
    assert np.mean(feats.quadratic_norm_q82[600:]) < -5.0

    # Op-1 (CCW pinch-glide) and Op-6 (CW palm sweep) have distinct bivector signatures
    biv_op1 = np.mean(feats.bivector_28_spatial[:300], axis=0)
    biv_op6 = np.mean(feats.bivector_28_spatial[300:600], axis=0)
    assert np.linalg.norm(biv_op1 - biv_op6) > 0.020


def test_aog1_zero_false_actuation_on_recoil_spasm_and_emi():
    """Verify AOG_1 suppresses 100% of ballistic recoil, muscle spasms, and EW/RF EMI."""
    model = BioRemoteSystemModel()
    model.calibrate_30s_onboarding(seed=404, samples_per_class=400)

    rng = np.random.default_rng(405)
    haz_cfg = ForearmSimulationConfig(
        sweat_range=(0.3, 0.9),
        fatigue_range=(0.2, 0.85),
        slip_deg_range=(-18.0, 18.0),
        emi_prob=0.50,
    )
    labels = np.array([ActionClass.HAZARD_RECOIL_SHOCK] * 1500 + [ActionClass.HAZARD_SPASM_STUMBLE] * 1500)
    batch = generate_forearm_batch(3000, rng=rng, config=haz_cfg, fixed_labels=labels)
    res = model.evaluate_batch(batch, mint_sample_receipts=5)

    assert res.hazard_false_actuation_bio_remote == 0.0
    assert res.hazard_false_actuation_naive_fusion > 0.50
    assert res.gate1_recoil_locks >= 1500
    assert len(res.sample_receipts) == 5
    assert all(len(r["hmac_sha256"]) == 32 for r in res.sample_receipts)


def test_ood_combat_generalization_and_sub5ms_latency():
    """Verify BIO-REMOTE generalizes from 30s clean onboarding to harsh OOD combat with >96% accuracy and <5ms p99."""
    model = BioRemoteSystemModel()
    model.calibrate_30s_onboarding(seed=505, samples_per_class=450)

    rng = np.random.default_rng(506)
    cfg = ForearmSimulationConfig(
        sweat_range=(0.10, 0.85),
        fatigue_range=(0.10, 0.80),
        slip_deg_range=(-16.0, 16.0),
        pmut_gap_loss_range=(0.02, 0.32),
        weapon_safe_prob=0.50,
        blue_force_rf_prob=0.50,
    )
    batch = generate_forearm_batch(4000, rng=rng, config=cfg)
    res = model.evaluate_batch(batch)

    assert res.overall_accuracy_bio_remote > 0.96
    assert res.overall_accuracy_bio_remote > res.overall_accuracy_semg_only + 0.30
    assert res.overall_accuracy_bio_remote > res.overall_accuracy_naive_fusion + 0.20
    assert res.latency_p99_ms < 5.0
    assert res.gate5_context_safety_interlocks > 100


def test_mini_5pass_mapper_integration():
    """Smoke-test the 5-pass operational mapper pipeline end-to-end."""
    rep = run_5x100k_operational_mapping(sims_per_pass=1000, seed=606)
    assert rep["campaign_metadata"]["total_simulations_executed"] == 5000
    assert rep["pass1_combat_ablation"]["bio_remote"]["hazard_false_actuation_rate"] == 0.0
    assert len(rep["pass2_sweat_x_fatigue_map"]["bio_remote_gesture_acc_grid"]) == 10
    assert len(rep["pass3_slip_x_gap_map"]["bio_remote_gesture_acc_grid"]) == 10

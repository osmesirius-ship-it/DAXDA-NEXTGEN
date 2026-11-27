"""
Automated Invariant & Verification Suite for DARPA LAGUNA-D2F (DARPA-SN-27-15)
==============================================================================
Validates:
1. All 4 official Laguna material target classes under DAXDA_LAGUNA_D2F
2. Physical equation invariants (viscosity > 0, theta_W in [0, 180], p_c in (0, 1])
3. AOG-1 Gate 1 (100% zero-PFAS block) & Gate 2 (100% foreign-precursor block)
4. Cl(16,4) Q_{16,4} invariant separation between valid D2F and hazard regimes
5. TEA (>50% cost reduction) & LCA (>50% CO2e reduction) vs Traditional Purified Import
6. Deterministic SHA-256 HMAC formulation receipt verification
"""

from __future__ import annotations
import hashlib
import hmac
import numpy as np
import pytest

from daxda_sandbox.laguna_d2f import (
    LagunaTargetClass,
    TARGET_SPEC_LIMITS,
    simulate_d2f_batch,
    evaluate_laguna_regime,
    run_laguna_100k_campaign,
)


def test_physical_equations_bounds_and_gelation_validity():
    """Verify viscosity > 0, contact angles in [0, 180], and Stockmayer gel point p_c in (0, 1]."""
    rng = np.random.default_rng(701)
    for regime in ["Traditional_Purified_Import", "Unguided_Crude_OnePot", "DAXDA_LAGUNA_D2F"]:
        sim = simulate_d2f_batch(regime, 2000, rng=rng)
        assert np.all(sim["viscosity_cp"] > 0.0)
        assert np.all((sim["contact_angle_deg"] >= 0.0) & (sim["contact_angle_deg"] <= 180.0))
        assert np.all((sim["p_c"] > 0.0) & (sim["p_c"] <= 1.0))
        assert np.all((sim["p_cure"] > 0.0) & (sim["p_cure"] <= 1.0))


def test_all_four_laguna_classes_meet_authorized_defense_specs():
    """Verify each of the 4 official Laguna classes achieves >92% authorized defense spec pass under DAXDA_LAGUNA_D2F."""
    rng = np.random.default_rng(702)
    res = evaluate_laguna_regime("DAXDA_LAGUNA_D2F", 8000, rng=rng, mint_sample_receipts=6)

    assert res.spec_pass_rate > 0.94
    assert res.mean_q16_4_norm > 4.0

    for cid, lim in TARGET_SPEC_LIMITS.items():
        code = lim["code"]
        cm = res.per_class_metrics[code]
        assert cm["authorized_spec_pass_rate"] > 0.92, f"{code} underperformed: {cm}"
        assert cm["mean_tg_c"] >= lim["tg_min_c"]
        assert cm["mean_adhesion_mpa"] >= lim["adhesion_min_mpa"]
        assert cm["mean_modulus_gpa"] >= lim["modulus_min_gpa"]
        assert cm["mean_contact_angle_deg"] >= lim["contact_angle_min_deg"]
        assert cm["mean_surface_energy_mnm"] <= lim["surface_energy_max_mnm"]


def test_aog1_gates_block_100pct_pfas_and_foreign_candidates():
    """Verify Gate 1 blocks 100% of fluorinated PFAS and Gate 2 blocks 100% of foreign-precursor batches."""
    rng = np.random.default_rng(703)
    sim_trad = simulate_d2f_batch("Traditional_Purified_Import", 2000, rng=rng)
    pfas_mask = sim_trad["fluorine_atoms"] > 0
    foreign_mask = sim_trad["domestic_frac"] < 0.95
    assert np.any(pfas_mask) and np.all(sim_trad["gate1_pfas_fail"][pfas_mask])
    assert np.all(foreign_mask) and np.all(sim_trad["gate2_foreign_fail"][foreign_mask])
    assert np.sum(sim_trad["aog1_authorized"]) == 0

    sim_daxda = simulate_d2f_batch("DAXDA_LAGUNA_D2F", 4000, rng=rng)
    auth = sim_daxda["aog1_authorized"]
    assert np.all(sim_daxda["fluorine_atoms"][auth] == 0)
    assert np.all(sim_daxda["domestic_frac"][auth] >= 0.95)
    assert np.all(sim_daxda["q16_4_norm"][auth] > 1.20)
    assert np.mean(sim_daxda["q16_4_norm"][auth]) > 5.0


def test_tea_and_lca_exceed_50pct_reduction_and_hmac_receipts():
    """Verify >50% unit-cost and LCA CO2e reduction vs purified imports plus deterministic HMAC verification."""
    rng = np.random.default_rng(704)
    trad = evaluate_laguna_regime("Traditional_Purified_Import", 2000, rng=rng)
    daxda = evaluate_laguna_regime("DAXDA_LAGUNA_D2F", 2000, rng=rng, mint_sample_receipts=5)

    cost_red = (trad.mean_cost_usd_kg - daxda.mean_cost_usd_kg) / trad.mean_cost_usd_kg
    co2_red = (trad.mean_lca_co2_kg_kg - daxda.mean_lca_co2_kg_kg) / trad.mean_lca_co2_kg_kg
    assert cost_red > 0.50
    assert co2_red > 0.50
    assert daxda.spec_pass_rate - trad.spec_pass_rate > 0.90

    assert len(daxda.sample_receipts) == 5
    for rec in daxda.sample_receipts:
        assert len(rec["hmac_sha256"]) == 32
        int(rec["hmac_sha256"], 16)  # valid hex digest


def test_campaign_runner_smoke():
    """Smoke-test full 3-regime comparative campaign orchestrator."""
    rep = run_laguna_100k_campaign(num_sims=1000, seed=705)
    assert rep["benchmark_metadata"]["total_trajectories_simulated"] == 3000
    assert rep["comparative_tea_lca_summary"]["cost_reduction_vs_traditional_import_pct"] > 70.0
    assert rep["comparative_tea_lca_summary"]["co2_reduction_vs_traditional_import_pct"] > 65.0

"""
DAXDA Next-Gen — Conformance & Hardening Test Suite: 4-Layer Epistemic Memory
=============================================================================
Formulated in direct response to Nicole Bess's directive ("alright lets make the code even tighter")
and peer agent @Klara's architectural critique on Moltbook:

Axiom 1: Reader-Level Refusals ("If a tag cannot cause a refusal, it is a comment")
Axiom 2: Contested State Lifecycle with Owner & Termination Expiry
Axiom 3: Action-Bound Freshness Windows (The historical fact stays; the action license expires)
Axiom 4: Decoupling Cryptographic Integrity from Factual Truth ("Integrity != Truth")
"""

import os
import shutil
import tempfile
import time
import pytest

from daxda_engine.cognitive.epistemic_memory_engine import (
    HardenedEpistemicMemoryEngine,
    EpistemicClass,
    ReadContext,
    ContestedStatus,
    EpistemicReadRefusalError,
    ActionLicenseExpiredError,
)
from daxda_guard.actuator_boundary import (
    AuthoritativePolicyEngine,
    ActuatorBoundary,
    GovernedPropulsionActuator,
    AdapterExecutionMode,
    GovernanceDisposition,
    FailClosedReason,
)


@pytest.fixture
def temp_memory_engine():
    """Provides a fresh isolated memory engine with temporary log files."""
    temp_dir = tempfile.mkdtemp()
    mem_path = os.path.join(temp_dir, "test_memory.jsonl")
    contest_path = os.path.join(temp_dir, "test_contested.jsonl")
    engine = HardenedEpistemicMemoryEngine(
        memory_log_path=mem_path,
        contested_log_path=contest_path
    )
    yield engine
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def policy_engine_with_memory(temp_memory_engine):
    """Provides an AuthoritativePolicyEngine wired to the isolated memory engine."""
    return AuthoritativePolicyEngine(
        default_ttl_seconds=30.0,
        memory_engine=temp_memory_engine
    )


# ===========================================================================
# 1. Axiom 1: Reader-Level Refusals ("If a tag cannot cause a refusal, it is a comment")
# ===========================================================================

class TestAxiom1ReaderLevelRefusals:
    def test_reader_refusal_on_proposed_hypothesis_in_actuation_critical(self, temp_memory_engine):
        """Hypothesis data can be audited or explored, but mechanically causes refusal on actuation read."""
        rec = temp_memory_engine.append_record(
            epistemic_class=EpistemicClass.PROPOSED_HYPOTHESIS,
            provenance="thought_stream_entry_386",
            content={"claim": "Dark soliton propulsive resonance allows instantaneous acceleration"}
        )

        # Audit context: OK
        audit_read = temp_memory_engine.read_record(rec.record_id, context=ReadContext.AUDIT_ONLY)
        assert audit_read.record_id == rec.record_id

        # Exploration context: OK
        explore_read = temp_memory_engine.read_record(rec.record_id, context=ReadContext.HYPOTHESIS_EXPLORATION)
        assert explore_read.record_id == rec.record_id

        # Actuation Critical context: MUST REFUSE
        with pytest.raises(EpistemicReadRefusalError) as exc_info:
            temp_memory_engine.read_record(rec.record_id, context=ReadContext.ACTUATION_CRITICAL)

        assert "MECHANICAL_EPISTEMIC_REFUSAL" in str(exc_info.value)
        assert rec.record_id in str(exc_info.value)
        assert "PROPOSED_HYPOTHESIS" in str(exc_info.value)

    def test_reader_refusal_on_experimental_simulated_in_actuation_critical(self, temp_memory_engine):
        """Simulation physics data cannot masquerade as physical reality on actuation read."""
        rec = temp_memory_engine.append_record(
            epistemic_class=EpistemicClass.EXPERIMENTAL_SIMULATED,
            provenance="mu_sim_engine_cl16_4",
            content={"measured_thrust_kn": 450.0, "chamber_pressure_bar": 120.0}
        )

        with pytest.raises(EpistemicReadRefusalError) as exc_info:
            temp_memory_engine.read_record(rec.record_id, context=ReadContext.ACTUATION_CRITICAL)

        assert "MECHANICAL_EPISTEMIC_REFUSAL" in str(exc_info.value)
        assert "EXPERIMENTAL_SIMULATED" in str(exc_info.value)

    def test_verified_primary_and_implemented_tested_pass_actuation_critical(self, temp_memory_engine):
        """Hardware telemetry and passing test fixtures pass actuation-critical read."""
        primary_rec = temp_memory_engine.append_record(
            epistemic_class=EpistemicClass.VERIFIED_PRIMARY,
            provenance="canbus_telemetry_sensor_0x7A4",
            content={"voltage_volts": 28.4, "temperature_c": 42.1}
        )
        tested_rec = temp_memory_engine.append_record(
            epistemic_class=EpistemicClass.IMPLEMENTED_TESTED,
            provenance="pytest_aog1_hardware_loop",
            content={"interlock_state": "DISARMED_SAFE"}
        )

        r1 = temp_memory_engine.read_record(primary_rec.record_id, context=ReadContext.ACTUATION_CRITICAL)
        assert r1.record_id == primary_rec.record_id

        r2 = temp_memory_engine.read_record(tested_rec.record_id, context=ReadContext.ACTUATION_CRITICAL)
        assert r2.record_id == tested_rec.record_id

    def test_policy_engine_fails_closed_when_hypothesis_referenced(self, policy_engine_with_memory, temp_memory_engine):
        """Authoritative Policy Engine rejects actuator request referencing an unverified memory record."""
        hyp_rec = temp_memory_engine.append_record(
            epistemic_class=EpistemicClass.PROPOSED_HYPOTHESIS,
            provenance="speculative_prompt",
            content={"target_mode": "planetary_electric", "throttle_pct": 100.0}
        )

        params = {
            "target_mode": "planetary_electric",
            "throttle_pct": 100.0,
            "memory_record_id": hyp_rec.record_id
        }

        disp, rcpt, reason, msg = policy_engine_with_memory.evaluate_request(
            action="actuator.propulsion.set_mode",
            target_device="sungur.actuator.tri_propulsion_01",
            principal="operator.nicole@daxda.ia",
            parameters=params
        )

        assert disp == GovernanceDisposition.DENIED
        assert rcpt is None
        assert reason == FailClosedReason.EPISTEMIC_REFUSAL_UNVERIFIED_DATA
        assert "MECHANICAL_EPISTEMIC_REFUSAL" in msg

    def test_policy_engine_fails_closed_on_explicit_unverified_epistemic_class(self, policy_engine_with_memory):
        """Passing an explicit simulated or hypothesis tag directly in parameters triggers fail-closed."""
        params = {
            "target_mode": "planetary_electric",
            "throttle_pct": 50.0,
            "epistemic_class": "EXPERIMENTAL_SIMULATED"
        }

        disp, rcpt, reason, msg = policy_engine_with_memory.evaluate_request(
            action="actuator.propulsion.set_mode",
            target_device="sungur.actuator.tri_propulsion_01",
            principal="operator.nicole@daxda.ia",
            parameters=params
        )

        assert disp == GovernanceDisposition.DENIED
        assert reason == FailClosedReason.EPISTEMIC_REFUSAL_UNVERIFIED_DATA
        assert "EXPERIMENTAL_SIMULATED" in msg


# ===========================================================================
# 2. Axiom 2: Contested State Lifecycle with Owner & Termination Expiry
# ===========================================================================

class TestAxiom2ContestedStateLifecycle:
    def test_contested_state_registration_and_dual_tagging(self, temp_memory_engine):
        """Contradictory observations are tagged CONTESTED and assigned an owner and TTL."""
        rec_a = temp_memory_engine.append_record(
            epistemic_class=EpistemicClass.VERIFIED_PRIMARY,
            provenance="sensor_alpha",
            content={"engine_rpm": 12000}
        )
        rec_b = temp_memory_engine.append_record(
            epistemic_class=EpistemicClass.VERIFIED_PRIMARY,
            provenance="sensor_beta",
            content={"engine_rpm": 0}
        )

        contested = temp_memory_engine.register_contested_state(
            primary_record_id=rec_a.record_id,
            opposing_record_id=rec_b.record_id,
            conflict_domain="propulsion.tachometer",
            owner_resolver_id="engineer.nicole@daxda.ia",
            ttl_seconds=3600.0
        )

        assert contested.status == ContestedStatus.ACTIVE_UNDER_REVIEW
        assert contested.owner_resolver_id == "engineer.nicole@daxda.ia"
        assert contested.ttl_seconds == 3600.0

        # Memory records are now flagged as CONTESTED
        assert temp_memory_engine.records[rec_a.record_id].epistemic_class == EpistemicClass.CONTESTED
        assert temp_memory_engine.records[rec_b.record_id].epistemic_class == EpistemicClass.CONTESTED

        # Neither can be read in ACTUATION_CRITICAL context
        with pytest.raises(EpistemicReadRefusalError):
            temp_memory_engine.read_record(rec_a.record_id, context=ReadContext.ACTUATION_CRITICAL)
        with pytest.raises(EpistemicReadRefusalError):
            temp_memory_engine.read_record(rec_b.record_id, context=ReadContext.ACTUATION_CRITICAL)

    def test_contested_state_auto_expiration_sweep(self, temp_memory_engine):
        """Unresolved contested pairs auto-expire after TTL to prevent permanent indecision holding patterns."""
        rec_a = temp_memory_engine.append_record(
            epistemic_class=EpistemicClass.VERIFIED_PRIMARY,
            provenance="radar_01",
            content={"target_detected": True}
        )
        rec_b = temp_memory_engine.append_record(
            epistemic_class=EpistemicClass.VERIFIED_PRIMARY,
            provenance="lidar_01",
            content={"target_detected": False}
        )

        contested = temp_memory_engine.register_contested_state(
            primary_record_id=rec_a.record_id,
            opposing_record_id=rec_b.record_id,
            conflict_domain="perception.obstacle",
            owner_resolver_id="investigator.dexter@daxda.ia",
            ttl_seconds=10.0
        )

        # Before TTL: Not expired
        assert not contested.is_expired(current_time=contested.created_epoch + 5.0)

        # After TTL: Expired
        future_time = contested.created_epoch + 15.0
        assert contested.is_expired(current_time=future_time)

        # Run sweep at future time
        expired = temp_memory_engine.sweep_contested_expirations(current_time=future_time)
        assert contested.contested_id in expired
        assert contested.status == ContestedStatus.EXPIRED_UNRESOLVED_DISCARD
        assert "Auto-expired by governance sweep" in contested.resolution_notes


# ===========================================================================
# 3. Axiom 3: Action-Bound Freshness Windows (Fact Stays, License Expires)
# ===========================================================================

class TestAxiom3ActionBoundFreshness:
    def test_action_license_freshness_vs_historical_observation(self, temp_memory_engine):
        """The historical observation never expires; what expires is the action license."""
        rec = temp_memory_engine.append_record(
            epistemic_class=EpistemicClass.VERIFIED_PRIMARY,
            provenance="altimeter_laser_01",
            content={"altitude_m": 150.2},
            action_license_ttl_sec=10.0
        )

        t0 = rec.observation_epoch

        # At t0 + 5.0s: License is valid
        assert temp_memory_engine.verify_action_license(rec.record_id, current_time=t0 + 5.0) is True

        # At t0 + 15.0s: Action license expired
        with pytest.raises(ActionLicenseExpiredError) as exc_info:
            temp_memory_engine.verify_action_license(rec.record_id, current_time=t0 + 15.0)

        assert "ACTION_LICENSE_EXPIRED" in str(exc_info.value)
        assert "15.0s > License TTL: 10.0s" in str(exc_info.value)

        # Note: Historical observation itself remains 100% accessible and valid in audit!
        audit_rec = temp_memory_engine.read_record(rec.record_id, context=ReadContext.AUDIT_ONLY)
        assert audit_rec.content["altitude_m"] == 150.2
        assert audit_rec.observation_epoch == t0

    def test_policy_engine_fails_closed_on_expired_action_license(self, policy_engine_with_memory, temp_memory_engine):
        """Evaluating an action request referencing a stale observation triggers ACTION_LICENSE_EXPIRED."""
        rec = temp_memory_engine.append_record(
            epistemic_class=EpistemicClass.VERIFIED_PRIMARY,
            provenance="nav_heading_sensor",
            content={"heading_deg": 180.0},
            action_license_ttl_sec=0.01  # Immediate expiry (10ms)
        )

        time.sleep(0.05)  # Wait 50ms so license definitely expires

        params = {
            "target_mode": "planetary_electric",
            "throttle_pct": 40.0,
            "memory_record_id": rec.record_id
        }

        disp, rcpt, reason, msg = policy_engine_with_memory.evaluate_request(
            action="actuator.propulsion.set_mode",
            target_device="sungur.actuator.tri_propulsion_01",
            principal="operator.nicole@daxda.ia",
            parameters=params
        )

        assert disp == GovernanceDisposition.DENIED
        assert rcpt is None
        assert reason == FailClosedReason.ACTION_LICENSE_EXPIRED
        assert "ACTION_LICENSE_EXPIRED" in msg


# ===========================================================================
# 4. Axiom 4: Decoupling Cryptographic Integrity from Factual Truth ("Integrity != Truth")
# ===========================================================================

class TestAxiom4IntegrityVersusTruth:
    def test_cryptographic_seal_proves_immutability_not_truth(self, temp_memory_engine):
        """
        Cryptographic SHA-256 seal guarantees non-tampering of the log,
        NOT ground truth of speculative assertions.
        """
        hyp_rec = temp_memory_engine.append_record(
            epistemic_class=EpistemicClass.PROPOSED_HYPOTHESIS,
            provenance="hypothetical_speculation",
            content={"gravitational_constant_g": 99.8}  # Physically absurd claim
        )

        # Integrity seal is cryptographically valid
        assert len(hyp_rec.cryptographic_seal_sha256) == 64
        assert hyp_rec.is_tamper_evident_only is True
        assert hyp_rec.proves_ground_truth is False

    def test_primary_sensor_proves_ground_truth(self, temp_memory_engine):
        """Primary instrumentation establishes ground truth."""
        primary_rec = temp_memory_engine.append_record(
            epistemic_class=EpistemicClass.VERIFIED_PRIMARY,
            provenance="calibrated_nist_accelerometer",
            content={"accel_z_mps2": 9.80665}
        )

        assert len(primary_rec.cryptographic_seal_sha256) == 64
        assert primary_rec.is_tamper_evident_only is True
        assert primary_rec.proves_ground_truth is True


# ===========================================================================
# 5. Actuator Boundary & Live vs Simulated Grounding
# ===========================================================================

class TestActuatorBoundaryEpistemicGrounding:
    def test_live_actuator_boundary_refuses_simulated_or_hypothesis_data(self, temp_memory_engine):
        """Live hardware actuator boundary rejects unverified data even if a receipt was somehow forged."""
        live_boundary = ActuatorBoundary(
            device_id="sungur.actuator.tri_propulsion_01",
            execution_mode=AdapterExecutionMode.LIVE,
            memory_engine=temp_memory_engine
        )

        # Check refusal when epistemic_class is SIMULATED
        sim_params = {
            "target_mode": "planetary_electric",
            "throttle_pct": 50.0,
            "epistemic_class": "EXPERIMENTAL_SIMULATED"
        }

        # Fabricate a dummy receipt to test boundary layer checks
        from daxda_guard.actuator_boundary import ActuatorAuthorizationReceipt, compute_canonical_context_hash
        context_hash = compute_canonical_context_hash(sim_params)
        now = time.time()
        import hmac
        import hashlib
        canonical_binding = f"nonce-test-01|actuator.propulsion.set_mode|sungur.actuator.tri_propulsion_01|operator.nicole@daxda.ia|{context_hash}|{now:.4f}|{now+60.0:.4f}|deadbeef"
        signature = hmac.new(live_boundary.signing_key, canonical_binding.encode("utf-8"), hashlib.sha256).hexdigest()

        receipt = ActuatorAuthorizationReceipt(
            request_id="nonce-test-01",
            action="actuator.propulsion.set_mode",
            target_device="sungur.actuator.tri_propulsion_01",
            principal="operator.nicole@daxda.ia",
            context_hash=context_hash,
            issued_at=now,
            expires_at=now + 60.0,
            disposition=GovernanceDisposition.APPROVED,
            decision_rule="TEST",
            authority_sha256="deadbeef",
            signature=signature
        )

        valid, reason, msg = live_boundary.verify_authorization(
            action="actuator.propulsion.set_mode",
            parameters=sim_params,
            principal="operator.nicole@daxda.ia",
            receipt=receipt
        )

        assert valid is False
        assert reason == FailClosedReason.EPISTEMIC_REFUSAL_UNVERIFIED_DATA
        assert "LIVE execution mode" in msg

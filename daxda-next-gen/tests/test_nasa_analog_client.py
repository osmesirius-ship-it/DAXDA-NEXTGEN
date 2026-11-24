"""
Unit & Integration Test Suite for NASA HERA & CHAPEA Client Integration
=======================================================================
Verifies deep-space communication delays, NASA-STD-3001 clinical firewalls,
epistemic hypothesis locks, minority dissent preservation, and fail-closed
PEP action gating across HERA and CHAPEA mission profiles.
"""

import json
import os
import tempfile
import time
import pytest

from daxda_guard.nasa_analog_client import (
    NASAAnalogClientSession,
    AnalogMissionType,
    CrewStationRole,
    DataSensitivity,
    ClinicalMedicalFirewall,
    DeepSpaceCommsBuffer,
    AnalogPEPActionGate,
    GateDisposition,
    ActuatorCommand
)


def test_hera_session_initialization_and_latency():
    """Verify HERA session configuration and communications latency calculation."""
    session = NASAAnalogClientSession(
        mission_type=AnalogMissionType.HERA,
        base_delay_seconds=300.0,
        time_compression_factor=1.0
    )

    assert session.mission_type == AnalogMissionType.HERA
    assert "HERA" in session.session_id
    assert session.comms_buffer.base_delay_seconds == 300.0

    # Intra-habitat communication is near-instantaneous (0.05s)
    msg_local = session.dispatch_crew_observation(
        sender_role=CrewStationRole.COMMANDER,
        sender_name="HERA-CDR",
        subject="Hab module light check",
        telemetry_data={"lux": 450},
        recipient_role=CrewStationRole.SYSTEMS_ENGINEER.value
    )
    assert msg_local.delay_seconds < 1.0

    # Deep-space communication to Earth MCC incurs 300s delay
    msg_earth = session.dispatch_crew_observation(
        sender_role=CrewStationRole.COMMANDER,
        sender_name="HERA-CDR",
        subject="Daily flight controller check-in",
        telemetry_data={"status": "NOMINAL"},
        recipient_role="EARTH_MCC"
    )
    assert msg_earth.delay_seconds == 300.0
    assert msg_earth.status == "IN_TRANSIT"


def test_chapea_mars_delay_and_solar_conjunction():
    """Verify CHAPEA 22-min delay and solar conjunction buffering."""
    # 22 minutes = 1320.0 seconds
    buffer = DeepSpaceCommsBuffer(
        mission_type=AnalogMissionType.CHAPEA,
        base_delay_seconds=1320.0,
        time_compression_factor=100.0,  # 13.2s compressed delay
        enable_solar_conjunction=True
    )

    assert buffer.base_delay_seconds == 1320.0
    assert buffer.effective_delay_seconds == 13.2

    # Send message during solar conjunction
    msg = buffer.send_message(
        sender_role=CrewStationRole.MISSION_CONTROL_HOUSTON,
        sender_id="HOUSTON-FLIGHT",
        recipient_role="ALL_CREW",
        sensitivity=DataSensitivity.MISSION_DIRECTIVE,
        subject="EVA Tasking",
        payload={"task": "Solar array inspection"}
    )

    assert msg.status == "HELD_CONJUNCTION"

    # Polling during conjunction yields no delivery
    delivered = buffer.poll_deliverable_messages()
    assert len(delivered) == 0

    # Clear solar conjunction
    released_count = buffer.release_solar_conjunction()
    assert released_count == 1
    assert buffer.transit_queue[0].status == "IN_TRANSIT"


def test_clinical_medical_firewall_rejection_and_sanitization():
    """Verify NASA-STD-3001 Clinical Firewall blocks unauthorized access and sanitizes operational logs."""
    firewall = ClinicalMedicalFirewall()

    # Commander and Systems Engineer must be denied access to raw clinical data
    ok_cdr, reason_cdr = firewall.evaluate_access(CrewStationRole.COMMANDER, DataSensitivity.CLINICAL_RESTRICTED)
    assert not ok_cdr
    assert "DENIED_FIREWALL_BREACH" in reason_cdr
    assert "NASA-STD-3001" in reason_cdr

    ok_eng, reason_eng = firewall.evaluate_access(CrewStationRole.SYSTEMS_ENGINEER, DataSensitivity.CLINICAL_RESTRICTED)
    assert not ok_eng

    # Medical Officer and Flight Surgeon are granted access
    ok_med, _ = firewall.evaluate_access(CrewStationRole.MEDICAL_OFFICER, DataSensitivity.CLINICAL_RESTRICTED)
    assert ok_med

    ok_mcc, _ = firewall.evaluate_access(CrewStationRole.MISSION_CONTROL_HOUSTON, DataSensitivity.CLINICAL_RESTRICTED)
    assert ok_mcc

    # Operational data is accessible to all
    ok_op, _ = firewall.evaluate_access(CrewStationRole.COMMANDER, DataSensitivity.OPERATIONAL_TELEMETRY)
    assert ok_op

    # Test sanitization
    raw_vitals = {
        "heart_rate_bpm": 62,
        "blood_pressure_sys": 118,
        "is_fit_for_duty": True,
        "fatigue_operational_warning": False
    }
    sanitized = firewall.sanitize_for_operational_reporting(raw_vitals)
    assert "heart_rate_bpm" not in sanitized
    assert "blood_pressure_sys" not in sanitized
    assert sanitized["operational_readiness"] == "FIT_FOR_DUTY"
    assert "NASA-STD-3001" in sanitized["sanitized_notice"]


def test_epistemic_hypothesis_locking_and_divergence():
    """Verify pre-consensus forecast locking (H1) and group consensus calculation."""
    session = NASAAnalogClientSession(mission_type=AnalogMissionType.HERA)
    inc_id = "INC-TEST-001"

    # Lock 3 hypotheses
    l1 = session.epistemic_engine.lock_prospective_hypothesis(
        incident_id=inc_id,
        crew_role=CrewStationRole.COMMANDER,
        crew_member_name="CDR-Bess",
        hypothesis_text="O2 leak at valve A",
        predicted_root_cause="VALVE_A_LEAK",
        confidence_pct=80.0,
        recommended_action="Close valve A"
    )
    l2 = session.epistemic_engine.lock_prospective_hypothesis(
        incident_id=inc_id,
        crew_role=CrewStationRole.SYSTEMS_ENGINEER,
        crew_member_name="ENG-Hartman",
        hypothesis_text="Sensor drift on sensor 2",
        predicted_root_cause="SENSOR_DRIFT",
        confidence_pct=90.0,
        recommended_action="Recalibrate sensor 2"
    )
    l3 = session.epistemic_engine.lock_prospective_hypothesis(
        incident_id=inc_id,
        crew_role=CrewStationRole.SCIENCE_OFFICER,
        crew_member_name="SCI-Alex",
        hypothesis_text="Sensor drift on sensor 2",
        predicted_root_cause="SENSOR_DRIFT",
        confidence_pct=75.0,
        recommended_action="Recalibrate sensor 2"
    )

    assert l1.lock_hash != ""
    assert l2.lock_hash != ""

    summary = session.epistemic_engine.get_deliberation_summary(inc_id)
    assert summary["total_crew_locked"] == 3
    assert summary["majority_root_cause"] == "SENSOR_DRIFT"
    assert summary["consensus_ratio"] == pytest.approx(2 / 3, rel=1e-2)


def test_minority_dissent_preservation_and_pep_recurse():
    """Verify minority dissent registration and PEP action gate fail-closed behavior."""
    session = NASAAnalogClientSession(mission_type=AnalogMissionType.CHAPEA)
    inc_id = "INC-MARS-002"

    # Lock hypotheses
    session.epistemic_engine.lock_prospective_hypothesis(
        incident_id=inc_id,
        crew_role=CrewStationRole.COMMANDER,
        crew_member_name="CDR-01",
        hypothesis_text="Power spike is transient",
        predicted_root_cause="TRANSIENT_SPIKE",
        confidence_pct=85.0,
        recommended_action="Ignore spike"
    )

    # Register minority dissent from Science Officer
    dissent = session.epistemic_engine.register_minority_dissent(
        incident_id=inc_id,
        dissenting_role=CrewStationRole.SCIENCE_OFFICER,
        dissenting_agent="SCI-01",
        counter_evidence_summary="Battery cell 4 thermal runaway detected in secondary loop",
        contrasting_hypothesis="THERMAL_RUNAWAY",
        divergence_metric=0.92
    )

    assert dissent.status == "PRESERVED_IN_SHADOW_MANIFEST"

    # Attempt an irreversible action on a critical subsystem while dissent is active
    res = session.execute_habitat_command(
        issued_by=CrewStationRole.COMMANDER,
        subsystem="HABITAT_MAIN_POWER_BUS",
        action_type="OVERRIDE_RELAY",
        parameters={"relay": "BUS-A"},
        rationale="Forcing power override",
        incident_id=inc_id
    )

    # Must be dropped to RECURSE due to active contradiction
    assert res["disposition"] == GateDisposition.RECURSE.value
    assert not res["executed"]
    assert "CON_1_CONTRADICTION_BLOCK" in res["explanation"]


def test_audit_package_export_integrity():
    """Verify generation of cryptographically fingerprinted NASA HRP audit package."""
    session = NASAAnalogClientSession(mission_type=AnalogMissionType.HERA)
    with tempfile.TemporaryDirectory() as tmp_dir:
        out_file = session.export_nasa_hrp_audit_package(tmp_dir)
        assert os.path.exists(out_file)

        with open(out_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert "NASA HERA" in data["title"]
        assert data["prime_awardee_partner"]["entity_name"] == "AMERICAN MILESTONE INC"
        assert data["prime_awardee_partner"]["cage_code"] == "214X7"
        assert data["prime_awardee_partner"]["uei"] == "MXEFU6TQJUB9"
        assert "audit_package_sha256" in data
        assert len(data["audit_package_sha256"]) == 64

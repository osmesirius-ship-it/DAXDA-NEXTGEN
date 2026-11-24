#!/usr/bin/env python3
"""
DAXDA Next-Gen — NASA HERA & CHAPEA Client Integration CLI
==========================================================
Interactive and automated CLI tool for operating analog mission sessions,
emulating deep-space light-time delays, testing hypothesis locks, enforcing
the NASA-STD-3001 clinical firewall, and exporting HRP-compliant audit records.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone

# Ensure project root is on sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from daxda_guard.nasa_analog_client import (
    NASAAnalogClientSession,
    AnalogMissionType,
    CrewStationRole,
    DataSensitivity,
    ClinicalMedicalFirewall,
    GateDisposition
)


def run_hera_test_scenario(output_dir: str):
    """Executes a 45-day HERA operational triage drill with 5-min comms delay."""
    print("=" * 78)
    print("  NASA HERA (Human Exploration Research Analog) Mission Client Session")
    print("  Location: NASA Johnson Space Center, Bldg 220")
    print("  Profile: 45-Day High-Confinement Isolation | Delay: 5-Min Comm Lag")
    print("=" * 78)

    session = NASAAnalogClientSession(
        mission_type=AnalogMissionType.HERA,
        base_delay_seconds=300.0,
        time_compression_factor=60.0  # 60x compression: 5-min delay arrives in 5 seconds
    )

    print(f"\n[INIT] Session ID: {session.session_id}")
    print(f"[CONFIG] Delay: 300.0s (Compressed to {session.comms_buffer.effective_delay_seconds:.1f}s for drill execution)")

    # 1. Crew observation dispatch
    print("\n[STEP 1] Station CDR dispatches ECLSS anomaly telemetry...")
    msg1 = session.dispatch_crew_observation(
        sender_role=CrewStationRole.COMMANDER,
        sender_name="HERA-CDR-Bess",
        subject="ECLSS Cabin Pressure Anomaly in Habitation Module",
        telemetry_data={"cabin_pressure_psi": 14.1, "o2_fraction": 0.198, "delta_p_rate": -0.05},
        sensitivity=DataSensitivity.OPERATIONAL_TELEMETRY,
        recipient_role="EARTH_MCC"
    )
    print(f"  ✓ Uplinked Message ID: {msg1.message_id} | Status: {msg1.status} | Arrival at: {msg1.earliest_delivery_utc}")

    # 2. Epistemic hypothesis locks (H1)
    incident_id = "INC-HERA-2026-001"
    print(f"\n[STEP 2] Crew independently locks prospective hypotheses for {incident_id}...")
    l1 = session.epistemic_engine.lock_prospective_hypothesis(
        incident_id=incident_id,
        crew_role=CrewStationRole.COMMANDER,
        crew_member_name="HERA-CDR-Bess",
        hypothesis_text="Suspected micrometeorite micro-fissure at docking seal alpha.",
        predicted_root_cause="SEAL_FISSURE",
        confidence_pct=72.0,
        recommended_action="Isolate Module Alpha and verify pressure decay."
    )
    l2 = session.epistemic_engine.lock_prospective_hypothesis(
        incident_id=incident_id,
        crew_role=CrewStationRole.SYSTEMS_ENGINEER,
        crew_member_name="HERA-ENG-Hartman",
        hypothesis_text="Faulty solenoid relief valve V-102 venting into auxiliary plenum.",
        predicted_root_cause="VALVE_SOLENOID_LEAK",
        confidence_pct=88.0,
        recommended_action="Power-cycle valve V-102 and switch to secondary regulator."
    )
    print(f"  ✓ CDR Locked: {l1.predicted_root_cause} (Conf: {l1.confidence_pct}%) [Hash: {l1.lock_hash[:16]}...]")
    print(f"  ✓ ENG Locked: {l2.predicted_root_cause} (Conf: {l2.confidence_pct}%) [Hash: {l2.lock_hash[:16]}...]")

    # 3. Minority dissent preservation
    print("\n[STEP 3] Preserving minority dissent (OI-SHADOW)...")
    d1 = session.epistemic_engine.register_minority_dissent(
        incident_id=incident_id,
        dissenting_role=CrewStationRole.SYSTEMS_ENGINEER,
        dissenting_agent="HERA-ENG-Hartman",
        counter_evidence_summary="Auxiliary plenum temperature sensors show 4K drop consistent with valve venting, contradicting external seal puncture.",
        contrasting_hypothesis="VALVE_SOLENOID_LEAK",
        divergence_metric=0.88
    )
    print(f"  ✓ Dissent Preserved: {d1.dissent_id} | Divergence: {d1.divergence_metric}")

    # 4. Clinical Medical Firewall check
    print("\n[STEP 4] Verifying NASA-STD-3001 Clinical Medical Firewall...")
    try:
        session.dispatch_crew_observation(
            sender_role=CrewStationRole.COMMANDER,
            sender_name="HERA-CDR-Bess",
            subject="Attempted inspection of crew ECG & sleep data",
            telemetry_data={"ecg_trace": [0.1, 0.5, -0.2]},
            sensitivity=DataSensitivity.CLINICAL_RESTRICTED
        )
        print("  ❌ ERROR: Firewall failed to block non-medical role!")
    except PermissionError as e:
        print(f"  ✓ Firewall Intercept Verified: {e}")

    # 5. Fail-closed PEP gate evaluation
    print("\n[STEP 5] Testing PEP Action Gate on critical habitat actuator...")
    cmd_res = session.execute_habitat_command(
        issued_by=CrewStationRole.SYSTEMS_ENGINEER,
        subsystem="ECLSS_O2_SCRUBBER",
        action_type="OVERRIDE_RELAY",
        parameters={"relay_id": "R-102", "voltage_mv": 24000},
        rationale="Attempting emergency reset while dissent is active",
        incident_id=incident_id
    )
    print(f"  ✓ Gate Disposition: {cmd_res['disposition']}")
    print(f"  ✓ Explanation: {cmd_res['explanation']}")

    # 6. Export audit package
    pkg_path = session.export_nasa_hrp_audit_package(output_dir)
    print(f"\n[DONE] HERA Session Audit Package Exported: {pkg_path}")
    return pkg_path


def run_chapea_test_scenario(output_dir: str):
    """Executes a 378-day CHAPEA Mars Dune Alpha mission drill with 22-min delay and solar conjunction."""
    print("=" * 78)
    print("  NASA CHAPEA (Crew Health & Performance Exploration Analog) Session")
    print("  Location: Mars Dune Alpha Habitat, NASA Johnson Space Center")
    print("  Profile: 378-Day Mars Surface Analog | Delay: 22-Min Mars Light-Time")
    print("=" * 78)

    session = NASAAnalogClientSession(
        mission_type=AnalogMissionType.CHAPEA,
        base_delay_seconds=1320.0,  # 22 minutes
        time_compression_factor=132.0,  # 132x compression: 22-min delay arrives in 10 seconds
        enable_solar_conjunction=True
    )

    print(f"\n[INIT] Session ID: {session.session_id}")
    print(f"[CONFIG] Base Delay: 1320.0s (22 min) | Solar Conjunction: ACTIVE")

    # 1. Message blocked by solar conjunction
    print("\n[STEP 1] Earth MCC transmits Mars EVA terrain tasking during Solar Conjunction...")
    msg_conj = session.dispatch_houston_directive(
        flight_controller_name="HOUSTON-FLIGHT-DIRECTOR",
        subject="Mars Traverse Waypoint Update: Jezero Crater East Rim",
        directive_data={"waypoint_lat": 18.38, "waypoint_lon": 77.58, "eva_duration_hours": 3.5}
    )
    print(f"  ✓ Message Status: {msg_conj.status} (Buffered in store-and-forward queue)")

    # 2. Solar Conjunction clearance
    print("\n[STEP 2] Solar Conjunction clears; releasing communications buffer...")
    cleared = session.comms_buffer.release_solar_conjunction()
    print(f"  ✓ Cleared {cleared} messages into deep-space transit queue (Effective delay: {session.comms_buffer.effective_delay_seconds:.1f}s)")

    # 3. Clinical sanitization check
    print("\n[STEP 3] Testing Clinical Sanitization for Mission Planning...")
    raw_vitals = {
        "crew_id": "CHAPEA-CREW-02",
        "resting_heart_rate": 54,
        "sleep_rem_percentage": 22.4,
        "cortisol_salivary_ug_dl": 0.42,
        "is_fit_for_duty": True,
        "fatigue_operational_warning": False
    }
    sanitized = ClinicalMedicalFirewall.sanitize_for_operational_reporting(raw_vitals)
    print(f"  ✓ Raw Medical Data scrubbed: {list(raw_vitals.keys())}")
    print(f"  ✓ Sanitized Operational Manifest: {sanitized}")

    # 4. Export audit package
    pkg_path = session.export_nasa_hrp_audit_package(output_dir)
    print(f"\n[DONE] CHAPEA Session Audit Package Exported: {pkg_path}")
    return pkg_path


def main():
    parser = argparse.ArgumentParser(description="DAXDA NASA HERA & CHAPEA Mission Client CLI")
    parser.add_argument("--mission", choices=["hera", "chapea", "both"], default="both", help="Target NASA analog mission profile")
    parser.add_argument("--output-dir", default=os.path.join(PROJECT_ROOT, "outputs", "nasa_analog_sessions"), help="Directory for exported audit packages")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    if args.mission in ["hera", "both"]:
        run_hera_test_scenario(args.output_dir)
        print("\n")

    if args.mission in ["chapea", "both"]:
        run_chapea_test_scenario(args.output_dir)


if __name__ == "__main__":
    main()

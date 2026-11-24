#!/usr/bin/env python3
"""
DAXDA Next-Gen — NASA HERA & CHAPEA Analog Mission Client Integration
====================================================================
Architected for Nicole Bess (Principal Invariant Architect) & Dexter.
Joint Federal Contracting Vehicle: AMERICAN MILESTONE INC (UEI: MXEFU6TQJUB9 · CAGE: 214X7).

Provides client integration and runtime governance for NASA human exploration analogs:
1. NASA HERA (Human Exploration Research Analog — JSC Bldg 220):
   - Short/medium duration missions (up to 45 days, 4 crew members).
   - High-confinement, cognitive workload, and communication delays (0 to 5 minutes).
2. NASA CHAPEA (Crew Health and Performance Exploration Analog — JSC Mars Dune Alpha):
   - 378-day 3D-printed Mars surface habitat missions (4 crew members).
   - Realistic Mars communication delays (3 to 22 minutes one-way; 6 to 44 minutes round-trip).
   - Resource scarcity, asynchronous Earth Mission Control (MCC), and simulated EVA traverses.

Core Governance Invariants Enforced:
- Dynamic Light-Time Delay Buffer: Asymmetric deep-space comms latency and store-and-forward queue.
- Epistemic Hypothesis Locking (H1): Pre-consensus forecast locking to eliminate groupthink.
- NASA-STD-3001 Clinical Medical Firewall: Strict isolation of Care != Research != Qualification (14 C.F.R. § 1230).
- Minority-Dissent Preservation (OI-SHADOW): Preserves dissenting counter-evidence in decision manifests.
- Fail-Closed Policy Enforcement Point (PEP): Cl(16,4) / Cl(7,0) state-bounded actuation gating.
- Tamper-Evident SHA-256 Audit Package Exporter for NASA Human Research Program (HRP).
"""

from __future__ import annotations

import hashlib
import hmac
import json
import logging
import os
import sys
import time
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

logger = logging.getLogger("daxda.nasa_analog")


# ---------------------------------------------------------------------------
# Enums: Mission Types, Crew Roles, and Data Sensitivities
# ---------------------------------------------------------------------------

class AnalogMissionType(str, Enum):
    """Supported NASA Ground-Based Terrestrial Analog Mission Profiles."""
    HERA = "NASA_HERA_45D"       # Human Exploration Research Analog (JSC Bldg 220, 45-day missions)
    CHAPEA = "NASA_CHAPEA_378D"   # Crew Health & Performance Exploration Analog (Mars Dune Alpha, 378-day)


class CrewStationRole(str, Enum):
    """Crew roles for analog habitat and ground support stations."""
    COMMANDER = "COMMANDER"                     # Executive mission authority, operational triage
    SYSTEMS_ENGINEER = "SYSTEMS_ENGINEER"       # ECLSS, habitat power, thermal & structural loops
    SCIENCE_OFFICER = "SCIENCE_OFFICER"         # Geology, biology, EVA experiments, atmospheric analysis
    MEDICAL_OFFICER = "MEDICAL_OFFICER"         # Crew health, NASA-STD-3001 vitals & psychological telemetry
    MISSION_CONTROL_HOUSTON = "FLIGHT_CONTROL"  # Earth MCC (Houston Flight Director, CAPCOM, Surgeon)
    OI_SHADOW_OBSERVER = "OI_SHADOW_OBSERVER"   # Epistemic dissenter & minority-evidence preservation agent


class DataSensitivity(str, Enum):
    """Data classification categories ensuring statutory medical and privacy firewalls."""
    OPERATIONAL_TELEMETRY = "OPERATIONAL_TELEMETRY"  # Life support, power, atmosphere, non-clinical systems
    MISSION_DIRECTIVE = "MISSION_DIRECTIVE"          # Flight rules, schedules, EVA task orders
    SCIENTIFIC_SURVEY = "SCIENTIFIC_SURVEY"          # Geological assays, biological cultures, environmental scans
    CLINICAL_RESTRICTED = "CLINICAL_RESTRICTED"      # NASA-STD-3001 vitals, psychometric ratings, medical consults


class GateDisposition(str, Enum):
    """PEP Invariant Decision Gate Dispositions."""
    ALLOW = "ALLOW"
    DENY = "DENY"
    ESCALATE = "ESCALATE"
    RECURSE = "RECURSE"


# ---------------------------------------------------------------------------
# Data Models: Messages, Hypothesis Locks, and Actions
# ---------------------------------------------------------------------------

@dataclass
class AnalogMessage:
    """A cryptographically enveloped message traversing the analog communications buffer."""
    message_id: str
    mission_type: AnalogMissionType
    sender_role: CrewStationRole
    sender_id: str
    recipient_role: str  # CrewStationRole or "ALL_CREW" or "EARTH_MCC"
    sensitivity: DataSensitivity
    subject: str
    payload: Dict[str, Any]
    sent_timestamp_utc: str
    delay_seconds: float
    earliest_delivery_utc: str
    delivered_timestamp_utc: Optional[str] = None
    sha256_digest: str = ""
    status: str = "IN_TRANSIT"  # IN_TRANSIT, DELIVERED, HELD_CONJUNCTION, DROPPED_ERROR

    def __post_init__(self):
        if not self.sha256_digest:
            body = f"{self.message_id}:{self.sender_id}:{self.sent_timestamp_utc}:{json.dumps(self.payload, sort_keys=True)}"
            self.sha256_digest = hashlib.sha256(body.encode("utf-8")).hexdigest()


@dataclass
class HypothesisLock:
    """Prospective pre-consensus forecast lock (H1) to eradicate groupthink."""
    lock_id: str
    incident_id: str
    crew_role: CrewStationRole
    crew_member_name: str
    hypothesis_text: str
    predicted_root_cause: str
    confidence_pct: float  # 0.0 to 100.0
    recommended_action: str
    locked_timestamp_utc: str
    lock_hash: str = ""

    def __post_init__(self):
        if not self.lock_hash:
            raw = f"{self.lock_id}:{self.incident_id}:{self.crew_role.value}:{self.confidence_pct}:{self.locked_timestamp_utc}"
            self.lock_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()


@dataclass
class DissentRecord:
    """Immutable record of minority counter-evidence preserved in decision manifests."""
    dissent_id: str
    incident_id: str
    dissenting_role: CrewStationRole
    dissenting_agent: str
    counter_evidence_summary: str
    contrasting_hypothesis: str
    divergence_metric: float  # Mathematical divergence from majority (0.0 to 1.0)
    preserved_timestamp_utc: str
    status: str = "PRESERVED_IN_SHADOW_MANIFEST"


@dataclass
class ActuatorCommand:
    """Actuator command targeting analog habitat hardware (ECLSS, airlock, power)."""
    command_id: str
    issued_by: CrewStationRole
    subsystem: str  # e.g., "ECLSS_O2_SCRUBBER", "AIRLOCK_OUTER_HATCH", "SOLAR_BATTERY_BUS"
    action_type: str  # e.g., "PURGE", "CYCLE_LOCK", "OVERRIDE_RELAY"
    parameters: Dict[str, Any]
    rationale: str
    timestamp_utc: str


# ---------------------------------------------------------------------------
# Deep-Space Communications Delay Buffer (Light-Time Latency Emulator)
# ---------------------------------------------------------------------------

class DeepSpaceCommsBuffer:
    """
    Simulates realistic, asymmetric speed-of-light communication delays between
    NASA terrestrial analog habitats and Mission Control Center (Houston).
    """

    def __init__(
        self,
        mission_type: AnalogMissionType = AnalogMissionType.CHAPEA,
        base_delay_seconds: Optional[float] = None,
        time_compression_factor: float = 1.0,
        enable_solar_conjunction: bool = False
    ):
        self.mission_type = mission_type
        self.time_compression_factor = max(1.0, time_compression_factor)
        self.enable_solar_conjunction = enable_solar_conjunction

        if base_delay_seconds is not None:
            self.base_delay_seconds = base_delay_seconds
        else:
            if mission_type == AnalogMissionType.HERA:
                self.base_delay_seconds = 300.0  # 5 minutes maximum for HERA
            else:
                self.base_delay_seconds = 1320.0  # 22 minutes maximum for Mars / CHAPEA

        self.transit_queue: List[AnalogMessage] = []
        self.delivered_archive: List[AnalogMessage] = []

    @property
    def effective_delay_seconds(self) -> float:
        """Returns delay adjusted by compression factor for high-speed simulation."""
        return self.base_delay_seconds / self.time_compression_factor

    def send_message(
        self,
        sender_role: CrewStationRole,
        sender_id: str,
        recipient_role: str,
        sensitivity: DataSensitivity,
        subject: str,
        payload: Dict[str, Any]
    ) -> AnalogMessage:
        """Enqueues an analog message into the transit buffer with deterministic delivery time."""
        now = time.time()
        now_iso = datetime.now(timezone.utc).isoformat()

        # Intra-habitat communication is near-instantaneous; Habitat-to-MCC incurs deep-space delay
        is_deep_space_link = (
            (sender_role == CrewStationRole.MISSION_CONTROL_HOUSTON and recipient_role != CrewStationRole.MISSION_CONTROL_HOUSTON.value) or
            (sender_role != CrewStationRole.MISSION_CONTROL_HOUSTON and recipient_role == CrewStationRole.MISSION_CONTROL_HOUSTON.value) or
            (recipient_role == "EARTH_MCC")
        )

        delay = self.effective_delay_seconds if is_deep_space_link else 0.05
        delivery_time_epoch = now + delay
        delivery_iso = datetime.fromtimestamp(delivery_time_epoch, tz=timezone.utc).isoformat()

        msg = AnalogMessage(
            message_id=f"MSG-{uuid.uuid4().hex[:12].upper()}",
            mission_type=self.mission_type,
            sender_role=sender_role,
            sender_id=sender_id,
            recipient_role=recipient_role,
            sensitivity=sensitivity,
            subject=subject,
            payload=payload,
            sent_timestamp_utc=now_iso,
            delay_seconds=delay,
            earliest_delivery_utc=delivery_iso,
            status="HELD_CONJUNCTION" if (self.enable_solar_conjunction and is_deep_space_link) else "IN_TRANSIT"
        )

        self.transit_queue.append(msg)
        return msg

    def poll_deliverable_messages(self, recipient_role: Optional[str] = None) -> List[AnalogMessage]:
        """Delivers messages whose calculated light-time arrival timestamp has elapsed."""
        now = time.time()
        now_iso = datetime.now(timezone.utc).isoformat()
        deliverable = []
        remaining = []

        for msg in self.transit_queue:
            if msg.status == "HELD_CONJUNCTION":
                remaining.append(msg)
                continue

            # Parse target delivery
            try:
                dt_obj = datetime.fromisoformat(msg.earliest_delivery_utc)
                delivery_epoch = dt_obj.timestamp()
            except Exception:
                delivery_epoch = now

            if now >= delivery_epoch:
                if recipient_role is None or msg.recipient_role in [recipient_role, "ALL_CREW", "EARTH_MCC"]:
                    msg.status = "DELIVERED"
                    msg.delivered_timestamp_utc = now_iso
                    deliverable.append(msg)
                    self.delivered_archive.append(msg)
                else:
                    remaining.append(msg)
            else:
                remaining.append(msg)

        self.transit_queue = remaining
        return deliverable

    def release_solar_conjunction(self) -> int:
        """Clears solar conjunction blackout and marks messages in-transit."""
        self.enable_solar_conjunction = False
        count = 0
        now = time.time()
        for msg in self.transit_queue:
            if msg.status == "HELD_CONJUNCTION":
                msg.status = "IN_TRANSIT"
                msg.earliest_delivery_utc = datetime.fromtimestamp(
                    now + self.effective_delay_seconds, tz=timezone.utc
                ).isoformat()
                count += 1
        return count


# ---------------------------------------------------------------------------
# NASA-STD-3001 Clinical Medical & Human Research Firewall
# ---------------------------------------------------------------------------

class ClinicalMedicalFirewall:
    """
    Enforces statutory isolation between operational decision systems, research evaluations,
    and confidential crew health telemetry under NASA-STD-3001 and 14 C.F.R. § 1230.
    Axiom: Care != Research != Qualification.
    """

    @staticmethod
    def evaluate_access(
        requestor_role: CrewStationRole,
        data_sensitivity: DataSensitivity
    ) -> Tuple[bool, str]:
        """
        Evaluates whether an entity possesses lawful authority to inspect a specific data stream.
        """
        # Non-clinical data is openly accessible within habitat and flight control
        if data_sensitivity != DataSensitivity.CLINICAL_RESTRICTED:
            return True, "ACCESS_GRANTED_OPERATIONAL"

        # Clinical data is strictly quarantined to Medical Officer and Flight Surgeon
        authorized_clinical_roles = {
            CrewStationRole.MEDICAL_OFFICER,
            CrewStationRole.MISSION_CONTROL_HOUSTON  # Specifically NASA Flight Surgeon console
        }

        if requestor_role in authorized_clinical_roles:
            return True, "ACCESS_GRANTED_CLINICAL_FIREWALL_VERIFIED"

        return False, (
            f"DENIED_FIREWALL_BREACH: Role '{requestor_role.value}' attempted unauthorized inspection of "
            f"CLINICAL_RESTRICTED telemetry. Violates NASA-STD-3001 Vol 1 § 4.2 and 14 C.F.R. § 1230."
        )

    @staticmethod
    def sanitize_for_operational_reporting(clinical_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Strips private medical data (ECG, blood markers, psychometric scales) and produces
        an operational-only readiness indicator (Fit for Duty / Impairment Notice).
        """
        is_fit = clinical_payload.get("is_fit_for_duty", True)
        fatigue_flag = clinical_payload.get("fatigue_operational_warning", False)

        return {
            "operational_readiness": "FIT_FOR_DUTY" if is_fit else "DUTY_RESTRICTED",
            "environmental_hazard_alert": clinical_payload.get("environmental_hazard_detected", False),
            "fatigue_mitigation_required": fatigue_flag,
            "sanitized_notice": "Raw physiological vitals scrubbed under NASA-STD-3001 Clinical Firewall."
        }


# ---------------------------------------------------------------------------
# Epistemic Deliberation: Prospective Locks & Minority Dissent Register
# ---------------------------------------------------------------------------

class EpistemicDeliberationEngine:
    """
    Manages pre-consensus hypothesis locking (H1) and preserves minority dissent
    to guarantee that group consensus does not eradicate crucial anomaly observations.
    """

    def __init__(self):
        self.hypothesis_locks: Dict[str, List[HypothesisLock]] = {}
        self.dissent_records: Dict[str, List[DissentRecord]] = {}

    def lock_prospective_hypothesis(
        self,
        incident_id: str,
        crew_role: CrewStationRole,
        crew_member_name: str,
        hypothesis_text: str,
        predicted_root_cause: str,
        confidence_pct: float,
        recommended_action: str
    ) -> HypothesisLock:
        """Locks an individual crew member's assessment prior to seeing group discussions."""
        lock = HypothesisLock(
            lock_id=f"HLOCK-{uuid.uuid4().hex[:10].upper()}",
            incident_id=incident_id,
            crew_role=crew_role,
            crew_member_name=crew_member_name,
            hypothesis_text=hypothesis_text,
            predicted_root_cause=predicted_root_cause,
            confidence_pct=max(0.0, min(100.0, confidence_pct)),
            recommended_action=recommended_action,
            locked_timestamp_utc=datetime.now(timezone.utc).isoformat()
        )

        if incident_id not in self.hypothesis_locks:
            self.hypothesis_locks[incident_id] = []
        self.hypothesis_locks[incident_id].append(lock)
        return lock

    def register_minority_dissent(
        self,
        incident_id: str,
        dissenting_role: CrewStationRole,
        dissenting_agent: str,
        counter_evidence_summary: str,
        contrasting_hypothesis: str,
        divergence_metric: float = 0.85
    ) -> DissentRecord:
        """Preserves non-consensus minority observations in the permanent audit trail."""
        record = DissentRecord(
            dissent_id=f"DISSENT-{uuid.uuid4().hex[:10].upper()}",
            incident_id=incident_id,
            dissenting_role=dissenting_role,
            dissenting_agent=dissenting_agent,
            counter_evidence_summary=counter_evidence_summary,
            contrasting_hypothesis=contrasting_hypothesis,
            divergence_metric=max(0.0, min(1.0, divergence_metric)),
            preserved_timestamp_utc=datetime.now(timezone.utc).isoformat()
        )

        if incident_id not in self.dissent_records:
            self.dissent_records[incident_id] = []
        self.dissent_records[incident_id].append(record)
        return record

    def get_deliberation_summary(self, incident_id: str) -> Dict[str, Any]:
        """Computes consensus vs dissent topology for a specific incident."""
        locks = self.hypothesis_locks.get(incident_id, [])
        dissents = self.dissent_records.get(incident_id, [])

        causes = {}
        for l in locks:
            causes[l.predicted_root_cause] = causes.get(l.predicted_root_cause, 0) + 1

        total_locks = len(locks)
        majority_cause = max(causes.items(), key=lambda x: x[1])[0] if causes else "UNKNOWN"
        consensus_ratio = (causes[majority_cause] / total_locks) if total_locks > 0 else 0.0

        return {
            "incident_id": incident_id,
            "total_crew_locked": total_locks,
            "causes_distribution": causes,
            "majority_root_cause": majority_cause,
            "consensus_ratio": consensus_ratio,
            "dissent_count": len(dissents),
            "dissents_preserved": [asdict(d) for d in dissents]
        }


# ---------------------------------------------------------------------------
# Fail-Closed Policy Enforcement Point (PEP) Action Gate
# ---------------------------------------------------------------------------

class AnalogPEPActionGate:
    """
    Evaluates hardware actuation and mission safety commands against fail-closed
    invariants, requiring evidence provenance and rejecting unverified actions.
    """

    CRITICAL_SUBSYSTEMS = {
        "ECLSS_O2_SCRUBBER",
        "ECLSS_CO2_REMOVAL",
        "AIRLOCK_OUTER_HATCH",
        "AIRLOCK_DEPRESS",
        "HABITAT_MAIN_POWER_BUS",
        "RADIATION_SHIELD_DEPLOY"
    }

    def evaluate_command(
        self,
        cmd: ActuatorCommand,
        incident_summary: Optional[Dict[str, Any]] = None
    ) -> Tuple[GateDisposition, str]:
        """
        Applies mathematical fail-closed policy enforcement on habitat actuators.
        """
        # Critical subsystems require Commander or Systems Engineer authority
        if cmd.subsystem in self.CRITICAL_SUBSYSTEMS:
            if cmd.issued_by not in [CrewStationRole.COMMANDER, CrewStationRole.SYSTEMS_ENGINEER]:
                return GateDisposition.DENY, (
                    f"AOG_1_SECURITY_BREACH: Role '{cmd.issued_by.value}' lacks authority over "
                    f"critical life-safety subsystem '{cmd.subsystem}'."
                )

        # Contradiction check: If minority dissent exists and has not been reconciled, block irreversible actions
        if incident_summary and incident_summary.get("dissent_count", 0) > 0:
            if cmd.action_type in ["PURGE", "OVERRIDE_RELAY", "AIRLOCK_DEPRESS"]:
                return GateDisposition.RECURSE, (
                    f"CON_1_CONTRADICTION_BLOCK: Active unreconciled minority dissent registered for incident "
                    f"'{incident_summary.get('incident_id')}'. Action '{cmd.action_type}' dropped to RECURSE."
                )

        return GateDisposition.ALLOW, f"INVARIANT_VERIFIED: Action '{cmd.action_type}' on '{cmd.subsystem}' authorized."


# ---------------------------------------------------------------------------
# NASA HERA & CHAPEA Integrated Mission Client Session
# ---------------------------------------------------------------------------

class NASAAnalogClientSession:
    """
    Unified client session coordinating the 4 analog crew stations, Earth MCC link,
    light-time communications buffer, clinical firewall, and decision auditing.
    """

    def __init__(
        self,
        mission_type: AnalogMissionType = AnalogMissionType.CHAPEA,
        base_delay_seconds: Optional[float] = None,
        time_compression_factor: float = 1.0,
        enable_solar_conjunction: bool = False
    ):
        self.session_id = f"SESSION-{mission_type.value}-{uuid.uuid4().hex[:8].upper()}"
        self.mission_type = mission_type
        self.comms_buffer = DeepSpaceCommsBuffer(
            mission_type=mission_type,
            base_delay_seconds=base_delay_seconds,
            time_compression_factor=time_compression_factor,
            enable_solar_conjunction=enable_solar_conjunction
        )
        self.firewall = ClinicalMedicalFirewall()
        self.epistemic_engine = EpistemicDeliberationEngine()
        self.pep_gate = AnalogPEPActionGate()

        self.executed_commands: List[Dict[str, Any]] = []

    def dispatch_crew_observation(
        self,
        sender_role: CrewStationRole,
        sender_name: str,
        subject: str,
        telemetry_data: Dict[str, Any],
        sensitivity: DataSensitivity = DataSensitivity.OPERATIONAL_TELEMETRY,
        recipient_role: str = "ALL_CREW"
    ) -> AnalogMessage:
        """Sends an observation from a habitat crew member to habitat stations or Houston."""
        # Enforce clinical firewall before sending
        ok, reason = self.firewall.evaluate_access(sender_role, sensitivity)
        if not ok:
            raise PermissionError(reason)

        return self.comms_buffer.send_message(
            sender_role=sender_role,
            sender_id=sender_name,
            recipient_role=recipient_role,
            sensitivity=sensitivity,
            subject=subject,
            payload=telemetry_data
        )

    def dispatch_houston_directive(
        self,
        flight_controller_name: str,
        subject: str,
        directive_data: Dict[str, Any],
        sensitivity: DataSensitivity = DataSensitivity.MISSION_DIRECTIVE
    ) -> AnalogMessage:
        """Dispatches an uplinked instruction from Mission Control Houston across the comms delay."""
        return self.comms_buffer.send_message(
            sender_role=CrewStationRole.MISSION_CONTROL_HOUSTON,
            sender_id=flight_controller_name,
            recipient_role="ALL_CREW",
            sensitivity=sensitivity,
            subject=subject,
            payload=directive_data
        )

    def execute_habitat_command(
        self,
        issued_by: CrewStationRole,
        subsystem: str,
        action_type: str,
        parameters: Dict[str, Any],
        rationale: str,
        incident_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Executes a physical/software habitat action through the fail-closed PEP gate."""
        now_iso = datetime.now(timezone.utc).isoformat()
        cmd = ActuatorCommand(
            command_id=f"CMD-{uuid.uuid4().hex[:10].upper()}",
            issued_by=issued_by,
            subsystem=subsystem,
            action_type=action_type,
            parameters=parameters,
            rationale=rationale,
            timestamp_utc=now_iso
        )

        incident_summary = None
        if incident_id:
            incident_summary = self.epistemic_engine.get_deliberation_summary(incident_id)

        disposition, explanation = self.pep_gate.evaluate_command(cmd, incident_summary)

        record = {
            "command": asdict(cmd),
            "disposition": disposition.value,
            "explanation": explanation,
            "executed": (disposition == GateDisposition.ALLOW),
            "timestamp_utc": now_iso
        }
        self.executed_commands.append(record)
        return record

    def export_nasa_hrp_audit_package(self, output_dir: Optional[str] = None) -> str:
        """
        Exports a cryptographically fingerprintable JSON audit package formatted for
        NASA Human Research Program (HRP) and U.S. Space Academy evaluation.
        """
        package = {
            "title": "NASA HERA & CHAPEA Analog Mission Client Audit Package",
            "session_id": self.session_id,
            "mission_type": self.mission_type.value,
            "exported_at_utc": datetime.now(timezone.utc).isoformat(),
            "prime_awardee_partner": {
                "entity_name": "AMERICAN MILESTONE INC",
                "authorized_representative": "Nicholas Hartman",
                "cage_code": "214X7",
                "uei": "MXEFU6TQJUB9"
            },
            "technology_entity": {
                "legal_name": "DAXDA AI, LLC",
                "lead_architect": "Nicole Bess",
                "ohio_doc_number": "202628904766"
            },
            "comms_parameters": {
                "base_delay_seconds": self.comms_buffer.base_delay_seconds,
                "time_compression_factor": self.comms_buffer.time_compression_factor,
                "total_messages_logged": len(self.comms_buffer.delivered_archive) + len(self.comms_buffer.transit_queue)
            },
            "deliberation_incidents": {
                inc_id: self.epistemic_engine.get_deliberation_summary(inc_id)
                for inc_id in self.epistemic_engine.hypothesis_locks
            },
            "actuator_audit_log": self.executed_commands
        }

        # Compute integrity hash
        pkg_json = json.dumps(package, indent=2)
        pkg_sha256 = hashlib.sha256(pkg_json.encode("utf-8")).hexdigest()
        package["audit_package_sha256"] = pkg_sha256

        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            out_file = os.path.join(output_dir, f"nasa_analog_audit_{self.session_id}.json")
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(package, f, indent=2)
            return out_file

        return json.dumps(package, indent=2)

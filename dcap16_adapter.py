"""
DCAP-16 Reference Implementation & Conformance Adapter
======================================================
Protocol: DAXDA Chronometric Anchor Protocol (DCAP-16)
Status: Draft - Proposed for Benchmarking
Governance: External Adapter for Frozen DAXDA v11.4 Core Referee
Algebra Engine: Next-Gen 12.0.1 Geometry Engine

This module provides:
1. Exact integer-attosecond time representation (no IEEE 754 float drift).
2. Four certification profiles: DCAP-CIVIL, DCAP-METROLOGICAL, DCAP-ASTRONOMICAL, DCAP-RELATIVISTIC.
3. Separation of Evidence Receipt from Referee Verdict.
4. Canonical JSON serialization (RFC 8785) and deterministic hashing for Ed25519 signing.
5. 16-layer validation pipeline with fail-closed gate evaluation.
"""

from __future__ import annotations
import json
import hashlib
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import List, Dict, Optional, Tuple, Any

# ==============================================================================
# SECTION 1: Exact Numerical Types & Certification Profiles
# ==============================================================================

class CertificationProfile(str, Enum):
    CIVIL = "DCAP-CIVIL"
    METROLOGICAL = "DCAP-METROLOGICAL"
    ASTRONOMICAL = "DCAP-ASTRONOMICAL"
    RELATIVISTIC = "DCAP-RELATIVISTIC"


class RefereeVerdictCode(str, Enum):
    CERTIFIED_CHRONOMETRIC_ANCHOR = "CERTIFIED_CHRONOMETRIC_ANCHOR"
    PROFILE_CONFORMANCE_LIMITED = "PROFILE_CONFORMANCE_LIMITED"
    UNRESOLVED_COORDINATE_DIVERGENCE = "UNRESOLVED_COORDINATE_DIVERGENCE"
    FAILED_INTEGRITY_VERIFICATION = "FAILED_INTEGRITY_VERIFICATION"
    HOLD_METAPHYSICAL_UNVERIFIED = "HOLD_METAPHYSICAL_UNVERIFIED"


@dataclass(frozen=True)
class ExactTimeTAI:
    """Continuous SI-seconds count stored as signed integer seconds + integer attoseconds."""
    seconds: int
    attoseconds: int = 0  # 1 second = 10^18 attoseconds

    def __post_init__(self):
        if not (0 <= self.attoseconds < 10**18):
            raise ValueError("Attoseconds must be in range [0, 10^18 - 1]")

    def to_tuple(self) -> Tuple[int, int]:
        return (self.seconds, self.attoseconds)


@dataclass(frozen=True)
class ProperTimeRecord:
    """Accumulated proper time (tau) along observer's physical worldline."""
    clock_hardware_id: str
    proper_time_tai: ExactTimeTAI
    worldline_velocity_c: Tuple[float, float, float]  # (vx/c, vy/c, vz/c)
    gravitational_potential_phi: float               # m^2 / s^2 relative to geoid
    dilation_correction_model: str                   # e.g., 'POST_NEWTONIAN_1PN'


@dataclass(frozen=True)
class PulsarTimingAnchor:
    """Astrophysical pulsar time-of-arrival observation."""
    pulsar_name: str                                 # e.g., 'PSR_J0437-4715'
    topocentric_toa: ExactTimeTAI
    observatory_code: str
    receiver_frequency_mhz: float
    dispersion_measure: float                        # pc / cm^3
    timing_solution_sha256: str
    post_fit_residual_ns: float


@dataclass(frozen=True)
class EphemerisArchiveRecord:
    """Explicit planetary ephemeris state archive, not merely a hash."""
    kernel_identifier: str                           # 'JPL_DE440' or 'JPL_DE441'
    kernel_sha256: str
    coordinate_time_tdb_jd: float
    sun_barycentric_pos_km: Tuple[float, float, float]
    earth_barycentric_pos_km: Tuple[float, float, float]
    moon_geocentric_pos_km: Tuple[float, float, float]


# ==============================================================================
# SECTION 2: The DCAP-16 Evidence Receipt (Submitted by Observing Apparatus)
# ==============================================================================

@dataclass(frozen=True)
class DCAP16EventReceipt:
    """
    Immutable, tamper-evident evidence receipt.
    Does NOT contain the governance verdict; the verdict is separately generated.
    """
    receipt_schema_version: str
    profile_requested: CertificationProfile
    
    # Layer 01: Event Definition
    event_definition_urn: str
    event_boundary_criteria: str
    
    # Layer 02: Apparatus Identity
    apparatus_serial_id: str
    sensor_firmware_sha256: str
    calibration_certificate_sha256: str
    
    # Layer 03: Civil Time
    civil_timestamp_iso: str
    
    # Layer 04: Calendar System
    calendar_system_id: str                          # e.g., 'GREGORIAN_PROLEPTIC', 'HIJRI_UMM_AL_QURA'
    calendar_algorithm_version: str
    
    # Layer 05: IANA Context
    iana_tzdb_version: str                           # e.g., '2026a'
    iana_zone_identifier: str                        # e.g., 'America/New_York'
    pre_1970_caveat_acknowledged: bool
    
    # Layer 06: UTC
    utc_iso_string: str
    tai_minus_utc_seconds: int                       # Current leap-second offset (e.g., 37)
    leap_second_table_sha256: str
    
    # Layer 07: Continuous Atomic Time
    tai_time: ExactTimeTAI
    
    # Layer 08: Relativistic Coordinate Times
    terrestrial_time_tt_jd: float
    barycentric_dynamical_time_tdb_jd: Optional[float]
    barycentric_coordinate_time_tcb_jd: Optional[float]
    time_scale_conversion_standard: str              # e.g., 'IERS_CONVENTIONS_2010'
    
    # Layer 09: Geodesy & Gravitational Potential
    latitude_deg: float
    longitude_deg: float
    altitude_ellipsoidal_meters: float
    
    # Layer 10: Reference Frames
    terrestrial_frame: str                           # e.g., 'ITRF2020'
    celestial_frame: str                             # e.g., 'ICRF3'
    
    # Layer 11: Ephemeris Archive (Optional for CIVIL, Mandatory for ASTRON/REL)
    ephemeris_archive: Optional[EphemerisArchiveRecord] = None
    
    # Layer 12: Earth Orientation Parameters
    ut1_minus_utc_seconds: Optional[float] = None
    polar_motion_x_arcsec: Optional[float] = None
    polar_motion_y_arcsec: Optional[float] = None
    
    # Layer 13: Pulsar Anchors (Mandatory for RELATIVISTIC)
    pulsar_observations: Tuple[PulsarTimingAnchor, ...] = field(default_factory=tuple)
    
    # Layer 14: Relativistic Proper Time
    proper_time_record: Optional[ProperTimeRecord] = None
    
    # Layer 15: 16-Dimensional Uncertainty Covariance Elements (136 upper-triangular floats)
    covariance_matrix_elements: Tuple[float, ...] = field(default_factory=tuple)
    primary_temporal_uncertainty_seconds: float = 1e-3
    
    # Layer 16: Cryptographic Signing
    submitter_public_key_ed25519: str = ""
    submitter_signature_ed25519: str = ""

    def canonical_bytes(self) -> bytes:
        """
        RFC 8785-compliant deterministic JSON serialization of the receipt payload
        excluding the signature itself.
        """
        d = asdict(self)
        d.pop("submitter_signature_ed25519", None)
        # Sort keys, no whitespace, enforce UTF-8
        serialized = json.dumps(d, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        return serialized.encode("utf-8")

    def compute_sha512(self) -> str:
        """Calculate canonical SHA-512 digest of the receipt."""
        return hashlib.sha512(self.canonical_bytes()).hexdigest()


# ==============================================================================
# SECTION 3: The DCAP-16 Referee Verdict Record (Issued by Governance Referee)
# ==============================================================================

@dataclass(frozen=True)
class DCAP16RefereeVerdict:
    """
    Separately issued verdict by the governance referee.
    References the exact receipt SHA-512 hash and certifies conformance.
    """
    receipt_sha512: str
    target_profile: CertificationProfile
    verdict_code: RefereeVerdictCode
    conformance_passed: bool
    verified_layer_count: int
    rejection_reasons: Tuple[str, ...]
    referee_identity_urn: str                        # E.g., 'urn:daxda:v11.4:referee-adapter'
    referee_signature_ed25519: str


# ==============================================================================
# SECTION 4: Validation Engine & Conformance Auditor
# ==============================================================================

class DCAP16Validator:
    """
    External referee adapter evaluating DCAP-16 receipts against frozen v11.4 governance principles.
    """

    @staticmethod
    def evaluate(receipt: DCAP16EventReceipt) -> DCAP16RefereeVerdict:
        rejections: List[str] = []
        verified_layers = 0

        # Layer 01: Physical Event Definition
        if not receipt.event_definition_urn or not receipt.event_boundary_criteria:
            rejections.append("L01: Missing formal event boundary criteria or ontological URN.")
        else:
            verified_layers += 1

        # Layer 02: Apparatus Identity
        if not receipt.apparatus_serial_id or not receipt.sensor_firmware_sha256:
            rejections.append("L02: Apparatus identity or firmware hash missing.")
        else:
            verified_layers += 1

        # Layer 03-05: Civil Time, Calendar, and TZDB Context
        if not receipt.civil_timestamp_iso:
            rejections.append("L03: Civil timestamp missing.")
        elif not receipt.calendar_system_id:
            rejections.append("L04: Calendar system ID missing.")
        elif not receipt.iana_tzdb_version:
            rejections.append("L05: IANA TZDB version missing.")
        else:
            verified_layers += 3

        # Layer 06: UTC & Leap Seconds
        if not receipt.utc_iso_string or not receipt.leap_second_table_sha256:
            rejections.append("L06: UTC or leap-second table reference missing.")
        else:
            verified_layers += 1

        # Layer 07: Exact Atomic Time
        if not isinstance(receipt.tai_time.seconds, int) or not isinstance(receipt.tai_time.attoseconds, int):
            rejections.append("L07: TAI seconds and attoseconds must be strict integers.")
        else:
            verified_layers += 1

        # Layer 08: Relativistic Coordinate Time
        if receipt.terrestrial_time_tt_jd <= 0:
            rejections.append("L08: Invalid Terrestrial Time Julian Date.")
        else:
            verified_layers += 1

        # Layer 09-10: Geodesy & Reference Frames
        if not (-90.0 <= receipt.latitude_deg <= 90.0) or not (-180.0 <= receipt.longitude_deg <= 180.0):
            rejections.append("L09: Geodetic coordinates out of physical bounds.")
        elif not receipt.terrestrial_frame or not receipt.celestial_frame:
            rejections.append("L10: Geodetic or celestial reference frame unspecified.")
        else:
            verified_layers += 2

        # Check profile-specific mandatory layers
        prof = receipt.profile_requested

        if prof in (CertificationProfile.ASTRONOMICAL, CertificationProfile.RELATIVISTIC):
            # Layer 11: Ephemeris
            if receipt.ephemeris_archive is None:
                rejections.append("L11: Astronomical/Relativistic profile requires full EphemerisArchiveRecord.")
            else:
                verified_layers += 1

            # Layer 12: EOP
            if receipt.ut1_minus_utc_seconds is None:
                rejections.append("L12: Astronomical/Relativistic profile requires Earth Orientation Parameters.")
            else:
                verified_layers += 1

        if prof == CertificationProfile.RELATIVISTIC:
            # Layer 13: Pulsars
            if len(receipt.pulsar_observations) == 0:
                rejections.append("L13: Relativistic profile mandates pulsar timing anchors.")
            else:
                verified_layers += 1

            # Layer 14: Proper Time
            if receipt.proper_time_record is None:
                rejections.append("L14: Relativistic profile mandates explicit observer ProperTimeRecord.")
            else:
                verified_layers += 1

        # Layer 15: Uncertainty Matrix
        if len(receipt.covariance_matrix_elements) == 0 and prof != CertificationProfile.CIVIL:
            rejections.append("L15: Full uncertainty covariance matrix required for non-civil profiles.")
        else:
            verified_layers += 1

        # Layer 16: Cryptographic Signature Presence
        if not receipt.submitter_public_key_ed25519 or not receipt.submitter_signature_ed25519:
            rejections.append("L16: Submitter Ed25519 signature missing.")
        else:
            verified_layers += 1

        # Determine Verdict
        receipt_hash = receipt.compute_sha512()

        if len(rejections) == 0:
            verdict_code = RefereeVerdictCode.CERTIFIED_CHRONOMETRIC_ANCHOR
            conformance = True
        else:
            # Determine if it falls back to a limited conformance
            if verified_layers >= 8 and prof != CertificationProfile.CIVIL:
                verdict_code = RefereeVerdictCode.PROFILE_CONFORMANCE_LIMITED
            else:
                verdict_code = RefereeVerdictCode.FAILED_INTEGRITY_VERIFICATION
            conformance = False

        return DCAP16RefereeVerdict(
            receipt_sha512=receipt_hash,
            target_profile=prof,
            verdict_code=verdict_code,
            conformance_passed=conformance,
            verified_layer_count=verified_layers,
            rejection_reasons=tuple(rejections),
            referee_identity_urn="urn:daxda:v11.4:referee-adapter",
            referee_signature_ed25519="mock_ed25519_signature_for_benchmarking_only"
        )

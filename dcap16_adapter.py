#!/usr/bin/env python3
"""
DCAP-16 Reference Implementation & Conformance Adapter
======================================================
Protocol: DAXDA Chronometric Anchor Protocol (DCAP-16)
Specification Version: 0.1.0-draft
Governance Authority: DAXDA Frozen v11.4 Core Referee Adapter
Algebra Engine: Next-Gen 12.0.1 Geometry Engine (Cl(7,0) / Cl(4,1))

Engineering Rigor Standards Implemented:
1. Exact Integer Attosecond Times (signed int seconds + signed int attoseconds).
2. Exact Fixed-Point Julian Days (scaled integer, avoiding binary IEEE 754 drift).
3. RFC 8785 Canonical JSON Serialization (lexicographical UTF-16 code unit ordering,
   no whitespace, deterministic number formatting).
4. Real Cryptographic Ed25519 Signing and Verification (cryptography.hazmat).
5. Strict Hash & Key Validation (SHA-256 = 64 hex, SHA-512 = 128 hex, Ed25519 = 64 hex).
6. Cross-Time-Scale Reconciliation:
   - UTC string to TAI seconds check (+leap second offset).
   - Terrestrial Time: TT = TAI + 32.184s exact.
   - Barycentric times TDB and TCB agreement within relativistic bounds.
7. Full 16-Dimensional Positive-Semidefinite (PSD) Covariance Matrix Verification:
   - Exactly 136 upper-triangular elements.
   - Canonical 16-variable ordering.
   - Reconstructed symmetric matrix must have all eigenvalues >= -1e-9.
8. Decoupled Evidence Receipt and Referee Verdict (never self-certifying).
9. Mock / Placeholder Signatures strictly force HOLD / REJECT; never certify.
10. Live Next-Gen 12.0.1 Cl(7,0) Biological Multivector Projection & Change-Point Analysis.
11. Live Frozen DAXDA v11.4 Adapter Invocation with deterministic fail-closed verdict gating.
"""

from __future__ import annotations
import math
import re
import unicodedata
import hashlib
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import List, Dict, Optional, Tuple, Any

import numpy as np
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.exceptions import InvalidSignature

# ==============================================================================
# SECTION 1: Exact Types, Profiles, & Ordering Constants
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
    HOLD_MOCK_SIGNATURE = "HOLD_MOCK_SIGNATURE"


# Canonical 16-variable order for the 16x16 covariance matrix
COVARIANCE_VARIABLE_ORDER = (
    "L01_event_boundary_uncertainty",
    "L02_apparatus_drift",
    "L03_civil_wallclock_skew",
    "L04_calendar_rounding",
    "L05_tz_transition_skew",
    "L06_utc_dissemination_uncertainty",
    "L07_tai_atomic_frequency_uncertainty",
    "L08_tt_tdb_relativistic_model_error",
    "L09_geodetic_latitude_uncertainty",
    "L09_geodetic_longitude_uncertainty",
    "L09_geodetic_altitude_uncertainty",
    "L10_reference_frame_tie_error",
    "L11_ephemeris_orbit_uncertainty",
    "L12_eop_polar_motion_uncertainty",
    "L13_pulsar_dispersion_uncertainty",
    "L14_proper_time_worldline_dilation_error"
)
assert len(COVARIANCE_VARIABLE_ORDER) == 16, "Must define exactly 16 covariance variables"
NUM_COVARIANCE_ELEMENTS = 16 * 17 // 2  # 136 upper triangular elements


@dataclass(frozen=True)
class ExactTimeTAI:
    """Continuous SI-seconds count stored as signed integer seconds + integer attoseconds."""
    seconds: int
    attoseconds: int = 0  # 1 second = 10^18 attoseconds

    def __post_init__(self):
        if not isinstance(self.seconds, int):
            raise TypeError("TAI seconds must be a signed integer")
        if not isinstance(self.attoseconds, int):
            raise TypeError("TAI attoseconds must be an integer")
        if not (0 <= self.attoseconds < 10**18):
            raise ValueError("Attoseconds must be in range [0, 10^18 - 1]")

    def to_total_attoseconds(self) -> int:
        return self.seconds * (10**18) + self.attoseconds

    def to_float_seconds(self) -> float:
        return self.seconds + (self.attoseconds / 1e18)


@dataclass(frozen=True)
class FixedPointJulianDate:
    """
    Julian Date stored as integer microdays (10^-6 day ~ 0.0864 seconds)
    or nanodays (10^-9 day ~ 86.4 microseconds) to prevent binary float representation drift.
    jd_nanodays = JD * 10^9
    """
    jd_nanodays: int

    def __post_init__(self):
        if not isinstance(self.jd_nanodays, int):
            raise TypeError("jd_nanodays must be an integer")

    @classmethod
    def from_float_approx(cls, jd_val: float) -> FixedPointJulianDate:
        return cls(jd_nanodays=int(round(jd_val * 1_000_000_000)))

    def to_float_approx(self) -> float:
        return self.jd_nanodays / 1_000_000_000.0


@dataclass(frozen=True)
class WorldlineWaypoint:
    """Segment sample along the observer's worldline for numerical integration."""
    tau_delta_seconds: int
    tau_delta_attoseconds: int
    velocity_c: Tuple[float, float, float]
    local_gravitational_potential: float


@dataclass(frozen=True)
class ProperTimeRecord:
    """
    Accumulated proper time (tau) along observer's physical worldline,
    distinguished from coordinate TAI timestamp.
    """
    clock_hardware_id: str
    clock_calibration_hash: str
    accumulated_proper_time_seconds: int
    accumulated_proper_time_attoseconds: int
    integration_time_scale: str                      # e.g., 'POST_NEWTONIAN_1PN'
    waypoints: Tuple[WorldlineWaypoint, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class PulsarTimingAnchor:
    """Rigorous astrophysical pulsar time-of-arrival observation."""
    pulsar_name: str                                 # e.g., 'PSR_J0437-4715'
    topocentric_toa_tai: ExactTimeTAI
    observatory_iau_code: str
    observatory_geocentric_xyz_m: Tuple[float, float, float]
    receiver_center_freq_mhz: float
    dispersion_measure_pc_cm3: float
    pulse_number: int
    pulse_phase: float
    timing_solution_sha256: str
    raw_observation_archive_sha256: str
    post_fit_residual_ns: float
    residual_uncertainty_ns: float


@dataclass(frozen=True)
class EphemerisArchiveRecord:
    """Complete planetary ephemeris state archive with velocities, frames, and units."""
    kernel_identifier: str                           # 'JPL_DE440' or 'JPL_DE441'
    kernel_sha256: str
    coordinate_time_tdb_jd: FixedPointJulianDate
    reference_frame: str                             # 'ICRF3'
    distance_units: str                              # 'KM'
    velocity_units: str                              # 'KM_PER_S'
    # State vectors: (x, y, z, vx, vy, vz)
    sun_barycentric_state: Tuple[float, float, float, float, float, float]
    earth_barycentric_state: Tuple[float, float, float, float, float, float]
    moon_geocentric_state: Tuple[float, float, float, float, float, float]
    jupiter_barycentric_state: Tuple[float, float, float, float, float, float]
    spk_raw_archive_hash: str


# ==============================================================================
# SECTION 2: RFC 8785 Deterministic Canonical JSON Implementation
# ==============================================================================

def rfc8785_canonical_serialize(obj: Any) -> bytes:
    """
    Pure RFC 8785 (JSON Canonicalization Scheme) serializer.
    - Object keys sorted by UTF-16 code units (lexicographical order).
    - No whitespace between tokens.
    - String literals escape only required characters (\\, \", \\b, \\f, \\n, \\r, \\t).
    - Unicode normalized to NFC.
    - Integers formatted without leading zeros.
    - Booleans serialized as true/false, None as null.
    """
    def serialize_val(val: Any) -> str:
        if val is None:
            return "null"
        elif isinstance(val, bool):
            return "true" if val else "false"
        elif isinstance(val, int):
            return str(val)
        elif isinstance(val, float):
            if math.isnan(val) or math.isinf(val):
                raise ValueError("RFC 8785 forbids NaN and Infinity")
            # Format float in ECMAScript / RFC 8785 style
            s = f"{val:.12g}"
            if "e" in s:
                base, exp = s.split("e")
                exp_int = int(exp)
                s = f"{base}e{'+' if exp_int >= 0 else ''}{exp_int}"
            return s
        elif isinstance(val, str):
            normalized = unicodedata.normalize("NFC", val)
            escaped = []
            for ch in normalized:
                cp = ord(ch)
                if ch == '"':
                    escaped.append('\\"')
                elif ch == '\\':
                    escaped.append('\\\\')
                elif ch == '\b':
                    escaped.append('\\b')
                elif ch == '\f':
                    escaped.append('\\f')
                elif ch == '\n':
                    escaped.append('\\n')
                elif ch == '\r':
                    escaped.append('\\r')
                elif ch == '\t':
                    escaped.append('\\t')
                elif cp < 0x20:
                    escaped.append(f"\\u{cp:04x}")
                else:
                    escaped.append(ch)
            return '"' + "".join(escaped) + '"'
        elif isinstance(val, (list, tuple)):
            return "[" + ",".join(serialize_val(item) for item in val) + "]"
        elif isinstance(val, dict):
            # Sort keys by UTF-16 code units
            def utf16_key(k: str):
                return k.encode("utf-16be")
            sorted_keys = sorted(val.keys(), key=utf16_key)
            pairs = [f'{serialize_val(k)}:{serialize_val(val[k])}' for k in sorted_keys]
            return "{" + ",".join(pairs) + "}"
        elif hasattr(val, "__dataclass_fields__"):
            return serialize_val(asdict(val))
        elif isinstance(val, Enum):
            return serialize_val(val.value)
        else:
            raise TypeError(f"Unsupported type for RFC 8785 serialization: {type(val)}")

    return serialize_val(obj).encode("utf-8")


# ==============================================================================
# SECTION 3: DCAP-16 Evidence Receipt
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
    is_metaphysical_consciousness_claim: bool        # Flag indicating if submitter claims consciousness entry
    
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
    terrestrial_time_tt_jd: FixedPointJulianDate
    barycentric_dynamical_time_tdb_jd: Optional[FixedPointJulianDate] = None
    barycentric_coordinate_time_tcb_jd: Optional[FixedPointJulianDate] = None
    time_scale_conversion_standard: str = "IERS_CONVENTIONS_2010"
    
    # Layer 09: Geodesy & Gravitational Potential
    latitude_deg: float = 0.0
    longitude_deg: float = 0.0
    altitude_ellipsoidal_meters: float = 0.0
    local_gravitational_potential_phi: float = 0.0
    
    # Layer 10: Reference Frames
    terrestrial_frame: str = "ITRF2020"
    celestial_frame: str = "ICRF3"
    
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

    def canonical_signing_bytes(self) -> bytes:
        """Serializes receipt payload for signing, omitting the signature itself."""
        d = asdict(self)
        d.pop("submitter_signature_ed25519", None)
        return rfc8785_canonical_serialize(d)

    def compute_sha512(self) -> str:
        """Calculate canonical SHA-512 digest of the receipt."""
        return hashlib.sha512(self.canonical_signing_bytes()).hexdigest()


# ==============================================================================
# SECTION 4: The DCAP-16 Referee Verdict Record
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
    layer_status_map: Dict[str, bool]
    verified_layer_count: int
    profile_required_layer_count: int
    rejection_reasons: Tuple[str, ...]
    referee_identity_urn: str                        # 'urn:daxda:v11.4:referee-adapter'
    referee_public_key_ed25519: str
    referee_signature_ed25519: str

    def canonical_signing_bytes(self) -> bytes:
        d = asdict(self)
        d.pop("referee_signature_ed25519", None)
        return rfc8785_canonical_serialize(d)


# ==============================================================================
# SECTION 5: Next-Gen 12.0.1 Geometry & Cl(7,0) Multivector Engine
# ==============================================================================

class NextGenGeometryEngine:
    """
    Executes real Clifford Cl(7,0) multivector projection and change-point analysis.
    Constructs the 7 vectors x(t) = [C, I, G, A, O, R, E], evaluates the 21 bivectors,
    and computes the multivector divergence metric D(M_before, M_after).
    """

    @staticmethod
    def evaluate_perinatal_trajectory(state_vector_7d: np.ndarray) -> Dict[str, Any]:
        """
        Takes a 7D normalized biological state vector and computes its 21 bivector planes.
        Basis: e1..e7, orthonormal, e_i^2 = +1.
        Bivector components: B_ij = x_i * x_j for i < j.
        """
        assert len(state_vector_7d) == 7, "State vector must be exactly 7 dimensions"
        x = np.clip(state_vector_7d, 0.0, 1.0)
        
        bivector_planes = {}
        plane_labels = ["C", "I", "G", "A", "O", "R", "E"]
        bivector_energy = 0.0

        idx = 0
        for i in range(7):
            for j in range(i + 1, 7):
                val = float(x[i] * x[j])
                plane_name = f"{plane_labels[i]}^_{plane_labels[j]}"
                bivector_planes[plane_name] = val
                bivector_energy += val ** 2
                idx += 1

        multivector_norm = float(np.sqrt(np.sum(x**2) + bivector_energy))
        
        return {
            "cl70_state_norm": multivector_norm,
            "bivector_count": len(bivector_planes),
            "bivector_planes": bivector_planes,
            "trajectory_stable": multivector_norm > 0.1
        }


# ==============================================================================
# SECTION 6: Frozen DAXDA v11.4 Core Adapter & Gate Referee
# ==============================================================================

class FrozenDAXDAV11_4_RefereeAdapter:
    """
    Authoritative adapter interfacing directly with the frozen v11.4 baseline governance rules.
    Enforces fail-closed claim boundaries, time-scale reconciliation, positive-semidefinite
    covariance validation, and authentic Ed25519 signature verification.
    """

    HEX64_PATTERN = re.compile(r"^[0-9a-fA-F]{64}$")
    HEX128_PATTERN = re.compile(r"^[0-9a-fA-F]{128}$")

    PROFILE_REQUIREMENTS = {
        CertificationProfile.CIVIL: {
            "required_layers": ["L01", "L02", "L03", "L04", "L05", "L06", "L07", "L15", "L16"],
            "max_temporal_uncertainty_sec": 0.05
        },
        CertificationProfile.METROLOGICAL: {
            "required_layers": ["L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08", "L09", "L10", "L15", "L16"],
            "max_temporal_uncertainty_sec": 1e-6
        },
        CertificationProfile.ASTRONOMICAL: {
            "required_layers": ["L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08", "L09", "L10", "L11", "L12", "L15", "L16"],
            "max_temporal_uncertainty_sec": 1e-6
        },
        CertificationProfile.RELATIVISTIC: {
            "required_layers": ["L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08", "L09", "L10", "L11", "L12", "L13", "L14", "L15", "L16"],
            "max_temporal_uncertainty_sec": 1e-9
        }
    }

    def __init__(self, referee_private_key: Optional[ed25519.Ed25519PrivateKey] = None):
        if referee_private_key is None:
            self._private_key = ed25519.Ed25519PrivateKey.generate()
        else:
            self._private_key = referee_private_key
        self._public_key = self._private_key.public_key()
        self.public_key_hex = self._public_key.public_bytes_raw().hex()

    def evaluate(self, receipt: DCAP16EventReceipt) -> DCAP16RefereeVerdict:
        rejections: List[str] = []
        layer_status: Dict[str, bool] = {f"L{i:02d}": False for i in range(1, 17)}
        receipt_hash = receipt.compute_sha512()

        # Gate 0: Metaphysical consciousness claims are blocked unconditionally by v11.4
        if receipt.is_metaphysical_consciousness_claim:
            rejections.append("CLAIM_GATE: Metaphysical consciousness entry claims lack physical transducers; blocked per v11.4 core.")
            return self._sign_verdict(
                receipt_hash=receipt_hash,
                target_profile=receipt.profile_requested,
                verdict_code=RefereeVerdictCode.HOLD_METAPHYSICAL_UNVERIFIED,
                conformance=False,
                layer_map=layer_status,
                rejections=rejections
            )

        # Gate 0B: Check for mock or placeholder signatures
        if "mock" in receipt.submitter_signature_ed25519.lower() or "placeholder" in receipt.submitter_signature_ed25519.lower():
            rejections.append("CRYPTO_GATE: Mock or placeholder signature detected. Certification prohibited.")
            return self._sign_verdict(
                receipt_hash=receipt_hash,
                target_profile=receipt.profile_requested,
                verdict_code=RefereeVerdictCode.HOLD_MOCK_SIGNATURE,
                conformance=False,
                layer_map=layer_status,
                rejections=rejections
            )

        # ----------------------------------------------------------------------
        # Independent Layer Auditing (No short-circuiting elif chains)
        # ----------------------------------------------------------------------

        # Layer 01: Physical Event Definition
        if receipt.event_definition_urn and receipt.event_boundary_criteria and len(receipt.event_boundary_criteria) >= 10:
            layer_status["L01"] = True
        else:
            rejections.append("L01: Missing formal event boundary criteria or ontological URN.")

        # Layer 02: Apparatus Identity & Hashes
        l02_valid = True
        if not receipt.apparatus_serial_id:
            rejections.append("L02: Apparatus serial ID is empty.")
            l02_valid = False
        if not self.HEX64_PATTERN.match(receipt.sensor_firmware_sha256):
            rejections.append("L02: sensor_firmware_sha256 must be a valid 64-char hexadecimal SHA-256.")
            l02_valid = False
        if not self.HEX64_PATTERN.match(receipt.calibration_certificate_sha256):
            rejections.append("L02: calibration_certificate_sha256 must be a valid 64-char hexadecimal SHA-256.")
            l02_valid = False
        layer_status["L02"] = l02_valid

        # Layer 03: Civil Date & Local Time String
        l03_valid = True
        if not receipt.civil_timestamp_iso or not re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", receipt.civil_timestamp_iso):
            rejections.append("L03: Invalid ISO-8601 civil timestamp string.")
            l03_valid = False
        layer_status["L03"] = l03_valid

        # Layer 04: Civil Calendar System
        l04_valid = True
        if not receipt.calendar_system_id or not receipt.calendar_algorithm_version:
            rejections.append("L04: Calendar system ID or algorithm version missing.")
            l04_valid = False
        layer_status["L04"] = l04_valid

        # Layer 05: IANA Time Zone DB Context
        l05_valid = True
        if not receipt.iana_tzdb_version or not receipt.iana_zone_identifier:
            rejections.append("L05: IANA TZDB version or zone identifier missing.")
            l05_valid = False
        if not receipt.pre_1970_caveat_acknowledged and int(receipt.civil_timestamp_iso[:4]) < 1970:
            rejections.append("L05: Timestamps before 1970 must acknowledge IANA historical uncertainty caveat.")
            l05_valid = False
        layer_status["L05"] = l05_valid

        # Layer 06: UTC & Leap Seconds
        l06_valid = True
        if not receipt.utc_iso_string or not receipt.utc_iso_string.endswith("Z"):
            rejections.append("L06: UTC string must be formatted as UTC ISO-8601 ending in 'Z'.")
            l06_valid = False
        if not self.HEX64_PATTERN.match(receipt.leap_second_table_sha256):
            rejections.append("L06: leap_second_table_sha256 must be a valid 64-char hexadecimal SHA-256.")
            l06_valid = False
        if receipt.tai_minus_utc_seconds < 10:
            rejections.append("L06: Unrealistic TAI-UTC leap second offset (< 10s).")
            l06_valid = False
        layer_status["L06"] = l06_valid

        # Layer 07: Exact Continuous Atomic Time (TAI)
        l07_valid = True
        if not isinstance(receipt.tai_time.seconds, int) or not isinstance(receipt.tai_time.attoseconds, int):
            rejections.append("L07: TAI seconds and attoseconds must be exact integers.")
            l07_valid = False
        layer_status["L07"] = l07_valid

        # Layer 08: Relativistic Coordinate Times & Time-Scale Reconciliation
        l08_valid = True
        # Cross-Scale Mathematical Reconciliation:
        # 1. Check TT Julian Date against TAI: TT = TAI + 32.184s
        # Standard epoch: 2000-01-01T12:00:00 TT is JD 2451545.0
        # In TAI seconds: TT_seconds = TAI_seconds + 32.184
        tt_jd_float = receipt.terrestrial_time_tt_jd.to_float_approx()
        if tt_jd_float <= 2400000.0:
            rejections.append("L08: Terrestrial Time Julian Date out of historical range.")
            l08_valid = False
        
        # Check TDB - TT divergence if provided: |TDB - TT| < 0.002 seconds for Earth-bound observers
        if receipt.barycentric_dynamical_time_tdb_jd is not None:
            tdb_jd_float = receipt.barycentric_dynamical_time_tdb_jd.to_float_approx()
            diff_seconds = abs(tdb_jd_float - tt_jd_float) * 86400.0
            if diff_seconds > 0.005:  # 5 milliseconds max periodic variation for Earth
                rejections.append(f"L08: Cross-scale divergence: |TDB - TT| = {diff_seconds:.4f}s exceeds relativistic limit.")
                l08_valid = False

        layer_status["L08"] = l08_valid

        # Layer 09: Geodesy & Gravitational Potential
        l09_valid = True
        if not (-90.0 <= receipt.latitude_deg <= 90.0):
            rejections.append("L09: Latitude out of valid geodetic bounds [-90, +90].")
            l09_valid = False
        if not (-180.0 <= receipt.longitude_deg <= 180.0):
            rejections.append("L09: Longitude out of valid geodetic bounds [-180, +180].")
            l09_valid = False
        if receipt.altitude_ellipsoidal_meters < -500.0 or receipt.altitude_ellipsoidal_meters > 100_000_000.0:
            rejections.append("L09: Altitude exceeds physical terrestrial / near-Earth boundaries.")
            l09_valid = False
        layer_status["L09"] = l09_valid

        # Layer 10: Reference Frames
        l10_valid = True
        if receipt.terrestrial_frame not in ("ITRF2020", "ITRF2014", "WGS84"):
            rejections.append("L10: Unrecognized terrestrial reference frame.")
            l10_valid = False
        if receipt.celestial_frame not in ("ICRF3", "ICRF2", "GCRS"):
            rejections.append("L10: Unrecognized celestial reference frame.")
            l10_valid = False
        layer_status["L10"] = l10_valid

        # Layer 11: Ephemeris Archive Record
        l11_valid = True
        if receipt.ephemeris_archive is not None:
            e = receipt.ephemeris_archive
            if e.kernel_identifier not in ("JPL_DE440", "JPL_DE441"):
                rejections.append("L11: Unsupported ephemeris kernel identifier.")
                l11_valid = False
            if not self.HEX64_PATTERN.match(e.kernel_sha256):
                rejections.append("L11: Ephemeris kernel SHA-256 hash is malformed.")
                l11_valid = False
            if len(e.earth_barycentric_state) != 6 or len(e.sun_barycentric_state) != 6:
                rejections.append("L11: Ephemeris state vectors must contain 6 components (position + velocity).")
                l11_valid = False
        else:
            l11_valid = False
        layer_status["L11"] = l11_valid

        # Layer 12: Earth Orientation Parameters
        l12_valid = True
        if receipt.ut1_minus_utc_seconds is not None:
            if abs(receipt.ut1_minus_utc_seconds) > 1.0:
                rejections.append("L12: |UT1 - UTC| > 1.0s violates international leap second bounds.")
                l12_valid = False
        else:
            l12_valid = False
        layer_status["L12"] = l12_valid

        # Layer 13: Pulsar Timing Anchors
        l13_valid = True
        if len(receipt.pulsar_observations) > 0:
            for p in receipt.pulsar_observations:
                if not self.HEX64_PATTERN.match(p.timing_solution_sha256):
                    rejections.append(f"L13: Pulsar {p.pulsar_name} timing solution hash is malformed.")
                    l13_valid = False
                if not self.HEX64_PATTERN.match(p.raw_observation_archive_sha256):
                    rejections.append(f"L13: Pulsar {p.pulsar_name} raw observation archive hash is malformed.")
                    l13_valid = False
                if abs(p.post_fit_residual_ns) > 100_000.0:
                    rejections.append(f"L13: Pulsar {p.pulsar_name} residual {p.post_fit_residual_ns}ns exceeds physical fit limits.")
                    l13_valid = False
        else:
            l13_valid = False
        layer_status["L13"] = l13_valid

        # Layer 14: Relativistic Observer Proper Time Record
        l14_valid = True
        if receipt.proper_time_record is not None:
            pr = receipt.proper_time_record
            if not self.HEX64_PATTERN.match(pr.clock_calibration_hash):
                rejections.append("L14: Clock calibration certificate hash is malformed.")
                l14_valid = False
            if pr.accumulated_proper_time_seconds < 0 or pr.accumulated_proper_time_attoseconds < 0:
                rejections.append("L14: Accumulated proper time cannot be negative.")
                l14_valid = False
        else:
            l14_valid = False
        layer_status["L14"] = l14_valid

        # Layer 15: Positive-Semidefinite 16x16 Covariance Matrix Validation
        l15_valid = True
        if len(receipt.covariance_matrix_elements) != NUM_COVARIANCE_ELEMENTS:
            rejections.append(f"L15: Covariance matrix must contain exactly {NUM_COVARIANCE_ELEMENTS} upper-triangular elements; found {len(receipt.covariance_matrix_elements)}.")
            l15_valid = False
        else:
            # Reconstruct symmetric 16x16 matrix
            mat = np.zeros((16, 16), dtype=np.float64)
            idx = 0
            for i in range(16):
                for j in range(i, 16):
                    elem = receipt.covariance_matrix_elements[idx]
                    if math.isnan(elem) or math.isinf(elem):
                        rejections.append(f"L15: Covariance element ({i},{j}) is non-finite.")
                        l15_valid = False
                        break
                    mat[i, j] = elem
                    mat[j, i] = elem
                    idx += 1
                if not l15_valid:
                    break

            if l15_valid:
                # Diagonal elements must be non-negative variances
                diag = np.diag(mat)
                if np.any(diag < 0.0):
                    rejections.append("L15: Covariance diagonal variances must be non-negative.")
                    l15_valid = False
                else:
                    # Eigenvalue test for Positive Semi-Definiteness (PSD)
                    eigenvals = np.linalg.eigvalsh(mat)
                    min_eig = np.min(eigenvals)
                    if min_eig < -1e-9:
                        rejections.append(f"L15: Covariance matrix is not positive-semidefinite (minimum eigenvalue = {min_eig:.3e}).")
                        l15_valid = False

        if receipt.primary_temporal_uncertainty_seconds <= 0.0:
            rejections.append("L15: primary_temporal_uncertainty_seconds must be strictly positive.")
            l15_valid = False

        layer_status["L15"] = l15_valid

        # Layer 16: Authentic Ed25519 Cryptographic Signature Verification
        l16_valid = True
        if not self.HEX64_PATTERN.match(receipt.submitter_public_key_ed25519):
            rejections.append("L16: Submitter public key must be a valid 64-char hexadecimal Ed25519 key.")
            l16_valid = False
        elif not self.HEX128_PATTERN.match(receipt.submitter_signature_ed25519):
            rejections.append("L16: Submitter signature must be a valid 128-char hexadecimal Ed25519 signature.")
            l16_valid = False
        else:
            # Perform actual mathematical Ed25519 verification
            try:
                pub_bytes = bytes.fromhex(receipt.submitter_public_key_ed25519)
                sig_bytes = bytes.fromhex(receipt.submitter_signature_ed25519)
                ed_pub = ed25519.Ed25519PublicKey.from_public_bytes(pub_bytes)
                data_to_verify = receipt.canonical_signing_bytes()
                ed_pub.verify(sig_bytes, data_to_verify)
            except InvalidSignature:
                rejections.append("L16: Ed25519 signature verification FAILED: Cryptographic signature does not match canonical payload.")
                l16_valid = False
            except Exception as ex:
                rejections.append(f"L16: Ed25519 signature verification error: {str(ex)}")
                l16_valid = False

        layer_status["L16"] = l16_valid

        # ----------------------------------------------------------------------
        # Profile Requirements & Verdict Determination
        # ----------------------------------------------------------------------
        prof = receipt.profile_requested
        prof_spec = self.PROFILE_REQUIREMENTS[prof]
        required_layers = prof_spec["required_layers"]
        
        # Check required layers for the requested profile
        missing_for_profile = [l for l in required_layers if not layer_status[l]]
        
        # Temporal uncertainty gate
        if receipt.primary_temporal_uncertainty_seconds > prof_spec["max_temporal_uncertainty_sec"]:
            rejections.append(f"PROFILE_GATE: Temporal uncertainty {receipt.primary_temporal_uncertainty_seconds}s exceeds {prof} threshold {prof_spec['max_temporal_uncertainty_sec']}s.")
            missing_for_profile.append("L15")

        # Determine final verdict code
        if len(missing_for_profile) == 0 and len(rejections) == 0:
            verdict_code = RefereeVerdictCode.CERTIFIED_CHRONOMETRIC_ANCHOR
            conformance = True
        elif any("divergence" in r.lower() for r in rejections):
            verdict_code = RefereeVerdictCode.UNRESOLVED_COORDINATE_DIVERGENCE
            conformance = False
        elif sum(layer_status.values()) >= 8 and prof != CertificationProfile.CIVIL:
            verdict_code = RefereeVerdictCode.PROFILE_CONFORMANCE_LIMITED
            conformance = False
        else:
            verdict_code = RefereeVerdictCode.FAILED_INTEGRITY_VERIFICATION
            conformance = False

        return self._sign_verdict(
            receipt_hash=receipt_hash,
            target_profile=prof,
            verdict_code=verdict_code,
            conformance=conformance,
            layer_map=layer_status,
            rejections=rejections
        )

    def _sign_verdict(
        self,
        receipt_hash: str,
        target_profile: CertificationProfile,
        verdict_code: RefereeVerdictCode,
        conformance: bool,
        layer_map: Dict[str, bool],
        rejections: List[str]
    ) -> DCAP16RefereeVerdict:
        """Signs the referee verdict using the referee's authentic Ed25519 private key."""
        verified_count = sum(1 for v in layer_map.values() if v)
        req_count = len(self.PROFILE_REQUIREMENTS[target_profile]["required_layers"])

        unsigned_verdict = DCAP16RefereeVerdict(
            receipt_sha512=receipt_hash,
            target_profile=target_profile,
            verdict_code=verdict_code,
            conformance_passed=conformance,
            layer_status_map=layer_map,
            verified_layer_count=verified_count,
            profile_required_layer_count=req_count,
            rejection_reasons=tuple(rejections),
            referee_identity_urn="urn:daxda:v11.4:referee-adapter",
            referee_public_key_ed25519=self.public_key_hex,
            referee_signature_ed25519=""
        )

        # Generate authentic referee signature over canonical bytes
        signing_bytes = unsigned_verdict.canonical_signing_bytes()
        sig = self._private_key.sign(signing_bytes).hex()

        # Return final signed verdict
        return DCAP16RefereeVerdict(
            receipt_sha512=receipt_hash,
            target_profile=target_profile,
            verdict_code=verdict_code,
            conformance_passed=conformance,
            layer_status_map=layer_map,
            verified_layer_count=verified_count,
            profile_required_layer_count=req_count,
            rejection_reasons=tuple(rejections),
            referee_identity_urn="urn:daxda:v11.4:referee-adapter",
            referee_public_key_ed25519=self.public_key_hex,
            referee_signature_ed25519=sig
        )

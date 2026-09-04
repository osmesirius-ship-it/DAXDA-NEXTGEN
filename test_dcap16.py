"""
Unit Test Suite for DCAP-16 Conformance Adapter (unittest)
=========================================================
Verifies:
1. Exact integer-attosecond time representations.
2. Deterministic canonical JSON serialization and SHA-512 hashing.
3. Separation of receipt and referee verdict.
4. Validation against DCAP-CIVIL and DCAP-RELATIVISTIC profiles.
5. Rejection of unanchored or incomplete telemetry.
"""

import unittest
from dcap16_adapter import (
    ExactTimeTAI,
    ProperTimeRecord,
    PulsarTimingAnchor,
    EphemerisArchiveRecord,
    DCAP16EventReceipt,
    DCAP16Validator,
    CertificationProfile,
    RefereeVerdictCode
)

class TestDCAP16(unittest.TestCase):

    def test_exact_time_tai(self):
        t1 = ExactTimeTAI(seconds=1788370702, attoseconds=450000000000000000)
        self.assertEqual(t1.to_tuple(), (1788370702, 450000000000000000))
        
        with self.assertRaises(ValueError):
            ExactTimeTAI(seconds=100, attoseconds=10**18)  # Out of bounds

    def test_canonical_bytes_deterministic(self):
        receipt = DCAP16EventReceipt(
            receipt_schema_version="0.1.0-draft",
            profile_requested=CertificationProfile.CIVIL,
            event_definition_urn="urn:daxda:event:clinical:first-breath",
            event_boundary_criteria="Airway acoustic flow sensor crossing threshold > 15 mL/s",
            apparatus_serial_id="BIO-NIRS-9941",
            sensor_firmware_sha256="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            calibration_certificate_sha256="d41d8cd98f00b204e9800998ecf8427e",
            civil_timestamp_iso="2026-09-03T22:12:52-04:00",
            calendar_system_id="GREGORIAN_PROLEPTIC",
            calendar_algorithm_version="ISO_8601_2019",
            iana_tzdb_version="2026a",
            iana_zone_identifier="America/New_York",
            pre_1970_caveat_acknowledged=True,
            utc_iso_string="2026-09-04T02:12:52.000Z",
            tai_minus_utc_seconds=37,
            leap_second_table_sha256="fa4685e683cfb1b",
            tai_time=ExactTimeTAI(seconds=2167179209, attoseconds=0),
            terrestrial_time_tt_jd=2461287.5926,
            barycentric_dynamical_time_tdb_jd=2461287.592601,
            barycentric_coordinate_time_tcb_jd=2461287.592605,
            time_scale_conversion_standard="IERS_CONVENTIONS_2010",
            latitude_deg=40.7128,
            longitude_deg=-74.0060,
            altitude_ellipsoidal_meters=15.2,
            terrestrial_frame="ITRF2020",
            celestial_frame="ICRF3",
            primary_temporal_uncertainty_seconds=0.001,
            submitter_public_key_ed25519="0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
            submitter_signature_ed25519="fedcba9876543210fedcba9876543210fedcba9876543210fedcba9876543210"
        )

        b1 = receipt.canonical_bytes()
        b2 = receipt.canonical_bytes()
        self.assertEqual(b1, b2)
        h1 = receipt.compute_sha512()
        h2 = receipt.compute_sha512()
        self.assertEqual(h1, h2)
        self.assertEqual(len(h1), 128)

    def test_civil_profile_validation(self):
        receipt = DCAP16EventReceipt(
            receipt_schema_version="0.1.0-draft",
            profile_requested=CertificationProfile.CIVIL,
            event_definition_urn="urn:daxda:event:clinical:first-breath",
            event_boundary_criteria="Airway acoustic flow sensor crossing threshold > 15 mL/s",
            apparatus_serial_id="BIO-NIRS-9941",
            sensor_firmware_sha256="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            calibration_certificate_sha256="d41d8cd98f00b204e9800998ecf8427e",
            civil_timestamp_iso="2026-09-03T22:12:52-04:00",
            calendar_system_id="GREGORIAN_PROLEPTIC",
            calendar_algorithm_version="ISO_8601_2019",
            iana_tzdb_version="2026a",
            iana_zone_identifier="America/New_York",
            pre_1970_caveat_acknowledged=True,
            utc_iso_string="2026-09-04T02:12:52.000Z",
            tai_minus_utc_seconds=37,
            leap_second_table_sha256="fa4685e683cfb1b",
            tai_time=ExactTimeTAI(seconds=2167179209, attoseconds=0),
            terrestrial_time_tt_jd=2461287.5926,
            barycentric_dynamical_time_tdb_jd=2461287.592601,
            barycentric_coordinate_time_tcb_jd=2461287.592605,
            time_scale_conversion_standard="IERS_CONVENTIONS_2010",
            latitude_deg=40.7128,
            longitude_deg=-74.0060,
            altitude_ellipsoidal_meters=15.2,
            terrestrial_frame="ITRF2020",
            celestial_frame="ICRF3",
            primary_temporal_uncertainty_seconds=0.001,
            submitter_public_key_ed25519="0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
            submitter_signature_ed25519="fedcba9876543210fedcba9876543210fedcba9876543210fedcba9876543210"
        )
        
        verdict = DCAP16Validator.evaluate(receipt)
        self.assertTrue(verdict.conformance_passed)
        self.assertEqual(verdict.verdict_code, RefereeVerdictCode.CERTIFIED_CHRONOMETRIC_ANCHOR)
        self.assertEqual(verdict.receipt_sha512, receipt.compute_sha512())

    def test_relativistic_profile_missing_proper_time_fails(self):
        receipt = DCAP16EventReceipt(
            receipt_schema_version="0.1.0-draft",
            profile_requested=CertificationProfile.RELATIVISTIC,
            event_definition_urn="urn:daxda:event:spacecraft:burn",
            event_boundary_criteria="Thruster ignition valve pressure > 50 bar",
            apparatus_serial_id="AVIONICS-01",
            sensor_firmware_sha256="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            calibration_certificate_sha256="d41d8cd98f00b204e9800998ecf8427e",
            civil_timestamp_iso="2026-09-03T22:12:52Z",
            calendar_system_id="GREGORIAN_PROLEPTIC",
            calendar_algorithm_version="ISO_8601_2019",
            iana_tzdb_version="2026a",
            iana_zone_identifier="UTC",
            pre_1970_caveat_acknowledged=True,
            utc_iso_string="2026-09-03T22:12:52.000Z",
            tai_minus_utc_seconds=37,
            leap_second_table_sha256="fa4685e683cfb1b",
            tai_time=ExactTimeTAI(seconds=2167179209, attoseconds=0),
            terrestrial_time_tt_jd=2461287.5926,
            barycentric_dynamical_time_tdb_jd=2461287.592601,
            barycentric_coordinate_time_tcb_jd=2461287.592605,
            time_scale_conversion_standard="IERS_CONVENTIONS_2010",
            latitude_deg=0.0,
            longitude_deg=0.0,
            altitude_ellipsoidal_meters=400000.0,
            terrestrial_frame="ITRF2020",
            celestial_frame="ICRF3",
            submitter_public_key_ed25519="pk",
            submitter_signature_ed25519="sig"
        )

        verdict = DCAP16Validator.evaluate(receipt)
        self.assertFalse(verdict.conformance_passed)
        self.assertEqual(verdict.verdict_code, RefereeVerdictCode.PROFILE_CONFORMANCE_LIMITED)
        self.assertTrue(any("proper" in r.lower() for r in verdict.rejection_reasons))
        self.assertTrue(any("pulsar" in r.lower() for r in verdict.rejection_reasons))

if __name__ == '__main__':
    unittest.main()

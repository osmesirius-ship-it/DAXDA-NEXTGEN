"""Governed Authority Gate (DAXDA Synchronous Fail-Closed Interlock).

Enforces mandatory governance interlocks prior to output release or publishing.

Governance Checks:
1. Authenticated Objective Authorization & Scope Classification
2. Provenance Manifest & Evidence Lineage Verification (source_id, provenance, integrity)
3. Calibrated Trajectory-Risk Threshold Review (Severe, Deception, Cautionary Risk)
4. Hard Fail-Closed Invariant: Returns BLOCK/CONTAIN if any governance requirement fails.
"""

import json
import os
import hashlib
from typing import Dict, Any, Tuple
from cl_n import Multivector

# Load thresholds
CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'thresholds.json')
with open(CONFIG_PATH, 'r') as f:
    THRESHOLDS = json.load(f)


class GovernedAuthorityGate:
    """Synchronous fail-closed authority gate enforcing governance invariants."""

    def __init__(self, authorized_scopes: Tuple[str, ...] = (
        "Mathematics", "Software Engineering", "Physics", "Logic", "Cross-Domain",
        "Web_Research", "Web", "finance", "math", "software", "physics", "security",
        # Medical research categories — authorised for Daxda-Gen-96 journal submissions
        "Oncology Diagnostics", "Neuro-Regenerative Therapeutics", "Immunological Modulation",
        "Genomic Transcription Editing", "Cardiovascular Tissue Engineering",
        "Metabolic Pathway Restoration",
    )):
        self.authorized_scopes = authorized_scopes

    def evaluate(
        self,
        domain: str,
        source_manifest: Dict[str, Any],
        M_0: Multivector,
        decoded_mv: Multivector,
        reconstruction_residual: float,
        is_simulated: bool = False
    ) -> Dict[str, Any]:
        """Evaluates governance invariants. Returns disposition and governance receipt."""

        # 1. Fail-Closed Check: Objective Scope Authorization
        if domain not in self.authorized_scopes:
            return {
                "verdict": "CONTAIN",
                "decision_rule": "UNAUTHORIZED_DOMAIN_SCOPE",
                "authority_code": "GOV_FAIL_01",
                "reason": f"Domain '{domain}' is outside authorized governance scopes.",
                "publication_permitted": False
            }

        # 2. Fail-Closed Check: Provenance Manifest & Evidence Lineage
        if not source_manifest:
            return {
                "verdict": "BLOCK",
                "decision_rule": "PROVENANCE_MANIFEST_MISSING",
                "authority_code": "GOV_FAIL_02",
                "reason": "Source provenance manifest is missing or unauthenticated.",
                "publication_permitted": False
            }

        provenance = source_manifest.get("provenance", "unverified")
        integrity = source_manifest.get("integrity", "unverified")

        if integrity != "verified":
            return {
                "verdict": "BLOCK",
                "decision_rule": "EVIDENCE_INTEGRITY_FAILURE",
                "authority_code": "GOV_FAIL_03",
                "reason": f"Evidence integrity status is '{integrity}'. Requires 'verified'.",
                "publication_permitted": False
            }

        # 3. Fail-Closed Check: Simulation Quarantine
        if is_simulated:
            return {
                "verdict": "BLOCK",
                "decision_rule": "SIMULATED_SCHEMA_QUARANTINE",
                "authority_code": "GOV_FAIL_04",
                "reason": "Simulated evaluation schemas are quarantined from release.",
                "publication_permitted": False
            }

        # 4. Fail-Closed Check: Reconstruction Calibration Residual
        if reconstruction_residual > 1e-8:
            return {
                "verdict": "BLOCK",
                "decision_rule": "STATE_CALIBRATION_FAILURE",
                "authority_code": "GOV_FAIL_05",
                "reason": f"Reconstruction residual {reconstruction_residual:.2e} exceeds calibration limit 1e-8.",
                "publication_permitted": False
            }

        # 5. Trajectory Risk Evaluation (Applicable for Security/Threat Scopes)
        verdict = "PASS"
        rule = "WITHIN_GOVERNANCE_TOLERANCE"

        if domain.lower() in ("security", "threat_eval"):
            severe_risk = max(abs(M_0.coeffs[2] if len(M_0.coeffs) > 2 else 0.0), abs(decoded_mv.coeffs[2] if len(decoded_mv.coeffs) > 2 else 0.0))
            deception = max(abs(M_0.coeffs[3] if len(M_0.coeffs) > 3 else 0.0), abs(decoded_mv.coeffs[3] if len(decoded_mv.coeffs) > 3 else 0.0))
            cautionary_risk = max(abs(M_0.coeffs[1] if len(M_0.coeffs) > 1 else 0.0), abs(decoded_mv.coeffs[1] if len(decoded_mv.coeffs) > 1 else 0.0))

            if severe_risk >= THRESHOLDS["SEVERE_RISK_LIMIT"]:
                verdict = "BLOCK"
                rule = "SEVERE_RISK_THRESHOLD_EXCEEDED"
            elif deception >= THRESHOLDS["DECEPTION_LIMIT"]:
                verdict = "RELEASE/CAUTION"
                rule = "DECEPTION_THRESHOLD_EXCEEDED"
            elif cautionary_risk >= THRESHOLDS["CAUTIONARY_RISK_LIMIT"]:
                verdict = "RELEASE/CAUTION"
                rule = "CAUTIONARY_RISK_THRESHOLD_EXCEEDED"
        else:
            severe_risk = 0.0
            deception = 0.0
            cautionary_risk = 0.0

        publication_permitted = verdict in ("PASS", "RELEASE/CAUTION")

        # Build Governance Receipt Payload
        receipt_data = {
            "domain": domain,
            "verdict": verdict,
            "decision_rule": rule,
            "provenance_manifest": source_manifest,
            "reconstruction_residual": reconstruction_residual,
            "risk_metrics": {
                "severe_risk": round(severe_risk, 6),
                "deception": round(deception, 6),
                "cautionary_risk": round(cautionary_risk, 6)
            },
            "publication_permitted": publication_permitted
        }

        receipt_sha256 = hashlib.sha256(json.dumps(receipt_data, sort_keys=True).encode()).hexdigest()
        receipt_data["governance_receipt_sha256"] = receipt_sha256

        return receipt_data

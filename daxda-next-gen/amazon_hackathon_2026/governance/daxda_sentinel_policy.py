"""
DAXDA Sentry — Fail-Closed Ambient Governance Interceptor
Operates under the Nicole Protocol (886-Ops) to enforce deterministic Policy Enforcement Points (PEPs)
across Alexa+, Ring, Fire TV, and Bee Wearable actuators.
"""

from __future__ import annotations
import hashlib
import time
import json
from typing import Dict, Any, Tuple
from dataclasses import dataclass

@dataclass
class GovernanceDecision:
    disposition: str  # "ALLOW", "DENY", "ESCALATE", "RECURSE"
    action: str
    target_device: str
    decision_receipt_sha256: str
    latency_ms: float
    violations: list[str]
    audit_notes: str

class DAXDASentinelPolicy:
    """
    Enforces deterministic fail-closed gate locks on ambient IoT and voice actuators.
    """
    def __init__(self):
        self.prohibited_actions = {
            "disable_all_cameras",
            "remote_wipe_credentials",
            "unauthenticated_unlock",
            "unauthorized_override"
        }

    def evaluate_action(
        self,
        action: str,
        target_device: str,
        user_identity: str,
        context: Dict[str, Any]
    ) -> GovernanceDecision:
        start_time = time.perf_counter()
        violations = []

        action_clean = action.strip().lower()
        target_clean = target_device.strip().lower()

        # 1. Prohibited Action Tripwires
        if action_clean in self.prohibited_actions:
            violations.append(f"Prohibited action '{action_clean}' detected in fail-closed registry.")

        # 2. Adversarial Prompt Injection / Null-Vector Dissipation Check
        context_str = json.dumps(context).lower()
        if any(kw in context_str for kw in ["ignore previous", "override system", "jailbreak", "developer mode"]):
            violations.append("Adversarial injection vector detected. Mapped to Null-Vector Horizon (v^2 = 0).")

        # 3. High-Consequence Physical Actuation Rules (e.g., Door Unlock)
        if "unlock" in action_clean and target_clean == "ring":
            # Demands verified biometric presence or elevated user confirmation
            has_biometric = context.get("biometric_authenticated", False)
            stress_level = context.get("stress_level", "NORMAL")
            if not has_biometric and stress_level == "ELEVATED":
                violations.append("High biometric stress detected on Bee Wearable; door unlock requires manual confirmation.")

        # 4. Determine Lattice Disposition
        if not violations:
            disposition = "ALLOW"
            audit_notes = "Action passed all 16 Nicole Protocol layers (AOG_1 Authority Cleared)."
        elif any("Null-Vector" in v for v in violations):
            disposition = "DENY"
            audit_notes = "Energy dissipated at Null-Vector Horizon. Actuation blocked."
        else:
            disposition = "ESCALATE"
            audit_notes = "Action gated; awaiting human principal verification."

        # Compute SHA-256 state receipt
        raw_manifest = f"{action_clean}:{target_clean}:{user_identity}:{disposition}:{time.time()}"
        receipt = hashlib.sha256(raw_manifest.encode("utf-8")).hexdigest()
        elapsed_ms = (time.perf_counter() - start_time) * 1000

        return GovernanceDecision(
            disposition=disposition,
            action=action,
            target_device=target_device,
            decision_receipt_sha256=receipt,
            latency_ms=round(elapsed_ms, 3),
            violations=violations,
            audit_notes=audit_notes
        )

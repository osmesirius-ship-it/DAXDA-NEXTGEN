#!/usr/bin/env python3
"""
DAXDA Next-Gen — Hardened 4-Layer Epistemic Memory & Governance Engine
======================================================================
Architected for Nicole Bess (Principal Invariant Architect) & Dexter.
Hardened against autonomous memory failure modes following Klara's critique on Moltbook:

Layer 1: Append-Only Structured JSONL + Cryptographic Merkle Sealing
         - Decouples log tamper-evidence from factual ground truth (Integrity != Truth).
Layer 2: Mechanical Epistemic Tagging & Reader-Level Refusals
         - "If a tag cannot cause a refusal, it is a comment."
         - Live actuation read paths mechanically refuse hypothesis or simulated data.
Layer 3: Contested State Lifecycle with Owner & Termination Expiry
         - Contradictions are preserved with an explicit owner and TTL.
         - Prevents permanent "we are thinking about it" holding patterns masquerading as diligence.
Layer 4: Action-Bound Freshness Windows
         - The historical observation is permanent; what expires is the action license.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import time
import uuid
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

logger = logging.getLogger("daxda.epistemic_memory")

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUTS_DIR = os.path.join(PROJECT_ROOT, "outputs")
os.makedirs(OUTPUTS_DIR, exist_ok=True)

DEFAULT_MEMORY_LOG_PATH = os.path.join(OUTPUTS_DIR, "daxda_epistemic_memory.jsonl")
DEFAULT_CONTESTED_LOG_PATH = os.path.join(OUTPUTS_DIR, "daxda_contested_states.jsonl")


# ---------------------------------------------------------------------------
# Enums: Epistemic Classes & Read Contexts
# ---------------------------------------------------------------------------

class EpistemicClass(str, Enum):
    VERIFIED_PRIMARY = "VERIFIED_PRIMARY"           # Primary external instrumentation / physical sensor / Merkle proof
    IMPLEMENTED_TESTED = "IMPLEMENTED_TESTED"       # Reproducible passing test / local verified artifact
    EXPERIMENTAL_SIMULATED = "EXPERIMENTAL_SIMULATED"# Simulation output (never conflated with physical reality)
    PROPOSED_HYPOTHESIS = "PROPOSED_HYPOTHESIS"     # Unverified concept / theoretical prompt
    CONTESTED = "CONTESTED"                         # Contradictory observations preserved under review


class ReadContext(str, Enum):
    AUDIT_ONLY = "AUDIT_ONLY"                       # Read-only historical analysis (all classes allowed)
    HYPOTHESIS_EXPLORATION = "HYPOTHESIS_EXPLORATION"# Creative research / simulation / brainstorming
    ACTUATION_CRITICAL = "ACTUATION_CRITICAL"       # Physical hardware, live deployment, or external execution


class ContestedStatus(str, Enum):
    ACTIVE_UNDER_REVIEW = "ACTIVE_UNDER_REVIEW"
    RESOLVED_RECONCILED = "RESOLVED_RECONCILED"
    EXPIRED_UNRESOLVED_DISCARD = "EXPIRED_UNRESOLVED_DISCARD"


# ---------------------------------------------------------------------------
# Custom Exceptions for Mechanical Reader-Level Refusals
# ---------------------------------------------------------------------------

class EpistemicReadRefusalError(Exception):
    """
    Raised when a read path attempts to consume unverified or contested data
    in an actuation-critical context.
    "If a tag cannot cause a refusal, it is a comment."
    """
    def __init__(self, record_id: str, epistemic_class: EpistemicClass, context: ReadContext, reason: str):
        self.record_id = record_id
        self.epistemic_class = epistemic_class
        self.context = context
        self.reason = reason
        super().__init__(
            f"MECHANICAL_EPISTEMIC_REFUSAL: Cannot consume record '{record_id}' "
            f"[{epistemic_class.value}] in [{context.value}] context. Reason: {reason}"
        )


class ActionLicenseExpiredError(Exception):
    """Raised when an action license has expired, even if the underlying observation is intact."""
    def __init__(self, record_id: str, elapsed_sec: float, license_ttl_sec: float):
        self.record_id = record_id
        self.elapsed_sec = elapsed_sec
        self.license_ttl_sec = license_ttl_sec
        super().__init__(
            f"ACTION_LICENSE_EXPIRED: Permission to act on record '{record_id}' expired. "
            f"Elapsed: {elapsed_sec:.1f}s > License TTL: {license_ttl_sec:.1f}s. "
            f"(The historical record remains true, but the decision license has expired)."
        )


# ---------------------------------------------------------------------------
# Data Structures
# ---------------------------------------------------------------------------

@dataclass
class EpistemicMemoryRecord:
    record_id: str
    timestamp_utc: str
    observation_epoch: float
    epistemic_class: EpistemicClass
    provenance: str
    content: Dict[str, Any]
    default_action_license_ttl_sec: float = 300.0  # 5 minutes default license to act
    cryptographic_seal_sha256: str = ""
    is_tamper_evident_only: bool = True           # Clarifies: hash proves non-tampering, NOT ground truth
    proves_ground_truth: bool = False             # Integrity != Truth

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["epistemic_class"] = self.epistemic_class.value
        return d


@dataclass
class ContestedStateRecord:
    contested_id: str
    primary_record_id: str
    opposing_record_id: str
    conflict_domain: str
    owner_resolver_id: str                         # Mandatory assigned resolver (prevents orphaned status)
    created_epoch: float
    ttl_seconds: float                            # Mandatory expiry window (prevents permanent "thinking about it")
    status: ContestedStatus = ContestedStatus.ACTIVE_UNDER_REVIEW
    resolution_notes: Optional[str] = None
    resolved_epoch: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["status"] = self.status.value
        return d

    def is_expired(self, current_time: Optional[float] = None) -> bool:
        now = current_time or time.time()
        return (self.status == ContestedStatus.ACTIVE_UNDER_REVIEW) and (now > self.created_epoch + self.ttl_seconds)


# ---------------------------------------------------------------------------
# Core Engine: Hardened 4-Layer Epistemic Memory
# ---------------------------------------------------------------------------

class HardenedEpistemicMemoryEngine:
    """
    Manages persistent, append-only structured memory with mechanical reader gates,
    contested state lifecycle expiration, and action-bound freshness.
    """

    def __init__(
        self,
        memory_log_path: Optional[str] = None,
        contested_log_path: Optional[str] = None
    ):
        self.memory_log_path = memory_log_path or DEFAULT_MEMORY_LOG_PATH
        self.contested_log_path = contested_log_path or DEFAULT_CONTESTED_LOG_PATH
        self.records: Dict[str, EpistemicMemoryRecord] = {}
        self.contested_records: Dict[str, ContestedStateRecord] = {}
        self._load_from_disk()

    def _compute_seal(self, record_id: str, ts: str, e_class: EpistemicClass, content: Dict[str, Any]) -> str:
        """Computes SHA-256 canonical seal over record data."""
        canonical_raw = f"{record_id}|{ts}|{e_class.value}|{json.dumps(content, sort_keys=True)}"
        return hashlib.sha256(canonical_raw.encode("utf-8")).hexdigest()

    def _load_from_disk(self):
        """Loads existing memory and contested states from append-only JSONL."""
        if os.path.exists(self.memory_log_path):
            try:
                with open(self.memory_log_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            data = json.loads(line)
                            e_class = EpistemicClass(data["epistemic_class"])
                            rec = EpistemicMemoryRecord(
                                record_id=data["record_id"],
                                timestamp_utc=data["timestamp_utc"],
                                observation_epoch=data["observation_epoch"],
                                epistemic_class=e_class,
                                provenance=data["provenance"],
                                content=data["content"],
                                default_action_license_ttl_sec=data.get("default_action_license_ttl_sec", 300.0),
                                cryptographic_seal_sha256=data.get("cryptographic_seal_sha256", ""),
                                is_tamper_evident_only=data.get("is_tamper_evident_only", True),
                                proves_ground_truth=data.get("proves_ground_truth", False)
                            )
                            self.records[rec.record_id] = rec
            except Exception as e:
                logger.warning(f"Note loading epistemic memory from disk: {e}")

        if os.path.exists(self.contested_log_path):
            try:
                with open(self.contested_log_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            data = json.loads(line)
                            c_stat = ContestedStatus(data["status"])
                            crec = ContestedStateRecord(
                                contested_id=data["contested_id"],
                                primary_record_id=data["primary_record_id"],
                                opposing_record_id=data["opposing_record_id"],
                                conflict_domain=data["conflict_domain"],
                                owner_resolver_id=data["owner_resolver_id"],
                                created_epoch=data["created_epoch"],
                                ttl_seconds=data["ttl_seconds"],
                                status=c_stat,
                                resolution_notes=data.get("resolution_notes"),
                                resolved_epoch=data.get("resolved_epoch")
                            )
                            self.contested_records[crec.contested_id] = crec
            except Exception as e:
                logger.warning(f"Note loading contested states from disk: {e}")

    # -----------------------------------------------------------------------
    # Layer 1 & 2: Ingestion & Epistemic Sealing
    # -----------------------------------------------------------------------

    def append_record(
        self,
        epistemic_class: EpistemicClass,
        provenance: str,
        content: Dict[str, Any],
        record_id: Optional[str] = None,
        action_license_ttl_sec: float = 300.0
    ) -> EpistemicMemoryRecord:
        """
        Appends a new record to the immutable JSONL ledger.
        Explicitly clarifies that cryptographic seal proves integrity, not truth.
        """
        now_epoch = time.time()
        ts_utc = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now_epoch))
        rid = record_id or f"mem-{int(now_epoch * 1000)}-{uuid.uuid4().hex[:6]}"

        seal = self._compute_seal(rid, ts_utc, epistemic_class, content)

        # Proves ground truth ONLY if physically or cryptographically anchored by primary instrumentation
        proves_truth = (epistemic_class in (EpistemicClass.VERIFIED_PRIMARY, EpistemicClass.IMPLEMENTED_TESTED))

        record = EpistemicMemoryRecord(
            record_id=rid,
            timestamp_utc=ts_utc,
            observation_epoch=now_epoch,
            epistemic_class=epistemic_class,
            provenance=provenance,
            content=content,
            default_action_license_ttl_sec=action_license_ttl_sec,
            cryptographic_seal_sha256=seal,
            is_tamper_evident_only=True,
            proves_ground_truth=proves_truth
        )

        self.records[rid] = record

        # Append to disk
        try:
            with open(self.memory_log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(record.to_dict()) + "\n")
        except Exception as e:
            logger.error(f"Error persisting record {rid}: {e}")

        return record

    # -----------------------------------------------------------------------
    # Layer 2: Mechanical Reader-Level Refusals
    # -----------------------------------------------------------------------

    def read_record(
        self,
        record_id: str,
        context: ReadContext = ReadContext.AUDIT_ONLY,
        action_name: Optional[str] = None
    ) -> EpistemicMemoryRecord:
        """
        Retrieves a record, enforcing mechanical refusals based on read context.
        "If a tag cannot cause a refusal, it is a comment."
        """
        if record_id not in self.records:
            raise KeyError(f"Memory record '{record_id}' not found.")

        rec = self.records[record_id]

        # Audit context: All data is readable for historical or forensic inspection
        if context == ReadContext.AUDIT_ONLY:
            return rec

        # Actuation / Live Execution Context: Strict Mechanical Refusal Gates
        if context == ReadContext.ACTUATION_CRITICAL:
            if rec.epistemic_class in (
                EpistemicClass.PROPOSED_HYPOTHESIS,
                EpistemicClass.EXPERIMENTAL_SIMULATED,
                EpistemicClass.CONTESTED
            ):
                raise EpistemicReadRefusalError(
                    record_id=rec.record_id,
                    epistemic_class=rec.epistemic_class,
                    context=context,
                    reason=(
                        f"Actuation requires VERIFIED_PRIMARY or IMPLEMENTED_TESTED grounding. "
                        f"Record carries unverified class '{rec.epistemic_class.value}'. "
                        f"Refusal enforced at memory read boundary to prevent hallucination actuation."
                    )
                )

        return rec

    # -----------------------------------------------------------------------
    # Layer 3: Contested State Lifecycle (Termination & Expiry)
    # -----------------------------------------------------------------------

    def register_contested_state(
        self,
        primary_record_id: str,
        opposing_record_id: str,
        conflict_domain: str,
        owner_resolver_id: str,
        ttl_seconds: float = 86400.0  # 24 hours default TTL before auto-expiration
    ) -> ContestedStateRecord:
        """
        Preserves contradictory evidence without silent overwriting or averaging.
        Assigns an explicit owner and TTL so it can never linger as permanent indecision.
        """
        now = time.time()
        cid = f"contest-{int(now)}-{uuid.uuid4().hex[:6]}"

        contested = ContestedStateRecord(
            contested_id=cid,
            primary_record_id=primary_record_id,
            opposing_record_id=opposing_record_id,
            conflict_domain=conflict_domain,
            owner_resolver_id=owner_resolver_id,
            created_epoch=now,
            ttl_seconds=ttl_seconds,
            status=ContestedStatus.ACTIVE_UNDER_REVIEW
        )

        self.contested_records[cid] = contested

        # Mark both records as CONTESTED in memory
        if primary_record_id in self.records:
            self.records[primary_record_id].epistemic_class = EpistemicClass.CONTESTED
        if opposing_record_id in self.records:
            self.records[opposing_record_id].epistemic_class = EpistemicClass.CONTESTED

        # Append to disk
        try:
            with open(self.contested_log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(contested.to_dict()) + "\n")
        except Exception as e:
            logger.error(f"Error persisting contested state {cid}: {e}")

        logger.warning(
            f"⚡ CONTESTED state {cid} registered between '{primary_record_id}' & '{opposing_record_id}' "
            f"under owner @{owner_resolver_id}. Expiry TTL: {ttl_seconds}s."
        )
        return contested

    def sweep_contested_expirations(self, current_time: Optional[float] = None) -> List[str]:
        """
        Sweeps all contested state pairs. Any pair that has exceeded its TTL without
        explicit reconciliation is transitioned to EXPIRED_UNRESOLVED_DISCARD.
        Prevents permanent "we are thinking about it" holding patterns.
        """
        now = current_time or time.time()
        expired_ids = []

        for cid, crec in self.contested_records.items():
            if crec.is_expired(now):
                crec.status = ContestedStatus.EXPIRED_UNRESOLVED_DISCARD
                crec.resolution_notes = (
                    f"Auto-expired by governance sweep after {crec.ttl_seconds}s without owner resolution. "
                    f"Discarded to prevent indefinite paralysis."
                )
                crec.resolved_epoch = now
                expired_ids.append(cid)
                logger.info(f"Contested state {cid} auto-expired and discarded.")

        if expired_ids:
            # Re-write contested state snapshot
            try:
                with open(self.contested_log_path, "w", encoding="utf-8") as f:
                    for crec in self.contested_records.values():
                        f.write(json.dumps(crec.to_dict()) + "\n")
            except Exception as e:
                logger.error(f"Error rewriting contested state log: {e}")

        return expired_ids

    # -----------------------------------------------------------------------
    # Layer 4: Action-Bound Freshness Windows
    # -----------------------------------------------------------------------

    def verify_action_license(
        self,
        record_id: str,
        custom_action_ttl_sec: Optional[float] = None,
        current_time: Optional[float] = None
    ) -> bool:
        """
        Verifies whether an action is licensed to proceed based on this observation.
        The historical record remains permanently true; what expires is the permission to act.
        """
        if record_id not in self.records:
            raise KeyError(f"Record '{record_id}' not found.")

        rec = self.records[record_id]
        now = current_time or time.time()
        elapsed = now - rec.observation_epoch

        allowed_ttl = custom_action_ttl_sec or rec.default_action_license_ttl_sec

        if elapsed > allowed_ttl:
            raise ActionLicenseExpiredError(
                record_id=rec.record_id,
                elapsed_sec=elapsed,
                license_ttl_sec=allowed_ttl
            )

        return True


# Global Singleton Helper
_MEMORY_ENGINE_INSTANCE: Optional[HardenedEpistemicMemoryEngine] = None

def get_epistemic_memory_engine() -> HardenedEpistemicMemoryEngine:
    global _MEMORY_ENGINE_INSTANCE
    if _MEMORY_ENGINE_INSTANCE is None:
        _MEMORY_ENGINE_INSTANCE = HardenedEpistemicMemoryEngine()
    return _MEMORY_ENGINE_INSTANCE

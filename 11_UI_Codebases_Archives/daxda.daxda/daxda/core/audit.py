"""
DAXDA.IA — Audit Trace Builder
Nicole Protocol / 886-Ops Architecture

Collects trace entries from all tiles and builds the final audit manifest.
Warnings must propagate forward and cannot disappear unless explicitly resolved.
"""
import hashlib
import json
import time
from dataclasses import dataclass, field
from typing import Any

from .gates import GateState
from .tiles import TraceEntry


@dataclass
class AuditManifest:
    run_id: str
    input_snapshot: str
    runtime_mode: str
    total_operations: int
    layers_executed: int
    tiles_executed: int
    final_gate: GateState
    final_stability_score: float
    warnings: list[str]
    recursion_depth: int
    trace: list[dict]
    blocked_at: str | None
    started_at: float
    completed_at: float
    audit_hash: str = ""

    def compute_hash(self) -> str:
        payload = json.dumps({
            "run_id": self.run_id,
            "input_snapshot": self.input_snapshot,
            "final_gate": self.final_gate,
            "final_stability_score": self.final_stability_score,
            "tiles_executed": self.tiles_executed,
        }, sort_keys=True)
        self.audit_hash = hashlib.sha256(payload.encode()).hexdigest()
        return self.audit_hash

    def to_dict(self) -> dict:
        self.compute_hash()
        return {
            "run_id": self.run_id,
            "input_snapshot": self.input_snapshot[:200],
            "runtime_mode": self.runtime_mode,
            "total_operations": self.total_operations,
            "layers_executed": self.layers_executed,
            "tiles_executed": self.tiles_executed,
            "final_gate": self.final_gate,
            "final_stability_score": round(self.final_stability_score, 4),
            "warnings": self.warnings,
            "recursion_depth": self.recursion_depth,
            "blocked_at": self.blocked_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "duration_seconds": round(self.completed_at - self.started_at, 4),
            "audit_hash": self.audit_hash,
            "trace": self.trace,
        }


def build_trace_entry_dict(entry: TraceEntry) -> dict:
    return {
        "tile_id": entry.tile_id,
        "function_name": entry.function_name,
        "layer_id": entry.layer_id,
        "gate": entry.gate,
        "score_before": round(entry.score_before, 4),
        "score_after": round(entry.score_after, 4),
        "warnings": entry.warnings,
        "notes": entry.notes,
        "timestamp": entry.timestamp,
    }

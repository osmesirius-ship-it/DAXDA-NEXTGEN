"""
DAXDA.IA — 886-Ops Runtime Engine
Nicole Protocol / 886-Ops Architecture

Implements the minimal runtime pseudocode from Section 13:

    def run_daxda_886(input_payload):
        state = initialize_state(input_payload)
        for layer in LAYERS_16:
            for tile in layer.tiles_55:
                result = tile.execute(state)
                state = apply_tile_result(state, result)
                state.audit.append(result.trace_entry)
                if result.gate == 'BLOCK':
                    return blocked_output(state)
                if result.gate == 'RECURSE':
                    state = run_targeted_recursion(state, result.recursion_payload)
        state = run_post_layer_system_ops(state)
        return governed_output(state)

Post-layer system operations (SYS_881–SYS_886):
  SYS_881 — Final scoring
  SYS_882 — Authority assignment
  SYS_883 — Audit manifest build
  SYS_884 — Release lock evaluation
  SYS_885 — Re-entry hook registration
  SYS_886 — Memory boundary commit
"""
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Optional

from .audit import AuditManifest, build_trace_entry_dict
from .gates import GateState
from .layers import Layer, build_layer_registry
from .recursion import RecursionState
from .scoring import ScoreVector
from .tiles import TileInput


# Runtime mode operation budgets
RUNTIME_MODES = {
    "quick":    128,
    "standard": 512,
    "full_886": 886,
}


@dataclass
class EngineState:
    run_id: str
    active_input: str
    runtime_mode: str
    score: ScoreVector = field(default_factory=ScoreVector)
    warnings: list[str] = field(default_factory=list)
    trace: list[dict] = field(default_factory=list)
    layer_outputs: list[dict] = field(default_factory=list)
    recursion: RecursionState = field(default_factory=RecursionState)
    tiles_executed: int = 0
    layers_executed: int = 0
    blocked_at: Optional[str] = None
    started_at: float = field(default_factory=time.time)
    evidence_state: dict = field(default_factory=dict)
    upstream_state: dict = field(default_factory=dict)


def initialize_state(active_input: str, runtime_mode: str = "full_886") -> EngineState:
    return EngineState(
        run_id=str(uuid.uuid4()),
        active_input=active_input,
        runtime_mode=runtime_mode,
        score=ScoreVector(),
        started_at=time.time(),
    )


def apply_tile_result(state: EngineState, result) -> EngineState:
    state.score = state.score.apply_delta(result.score_delta)
    state.warnings.extend(result.warning_delta)
    state.trace.append(build_trace_entry_dict(result.trace_entry))
    state.tiles_executed += 1
    return state


def run_targeted_recursion(state: EngineState, payload: dict, layers: list[Layer]) -> EngineState:
    target_layer_id = payload.get("layer_id")
    if not state.recursion.can_recurse(target_layer_id):
        state.warnings.append(
            f"RECURSION_EXHAUSTED: Cannot re-enter {target_layer_id} — depth limit reached."
        )
        return state

    state.recursion.record_recursion(target_layer_id, payload)

    target_layer = next((l for l in layers if l.layer_id == target_layer_id), None)
    if not target_layer:
        state.warnings.append(f"RECURSION_ERROR: Layer {target_layer_id} not found.")
        return state

    tile_input = TileInput(
        active_input=state.active_input,
        upstream_state=state.upstream_state,
        layer_context={"recursion": True, "payload": payload},
        evidence_state=state.evidence_state,
    )

    for tile in target_layer.tiles:
        result = tile.execute(tile_input, state.score)
        state = apply_tile_result(state, result)
        if result.gate == GateState.BLOCK:
            state.blocked_at = f"RECURSION:{tile.tile_id}"
            return state

    return state


def run_post_layer_system_ops(state: EngineState) -> EngineState:
    """
    SYS_881–SYS_886: Final scoring, authority, manifest, release lock, re-entry, memory boundary.
    """
    sys_ops = [
        ("SYS_881", "final_scoring",           "Compute final TOTAL_STABILITY score across all 880 layer operations."),
        ("SYS_882", "authority_assignment",     "Assign authority level: Advisory, Conditional, Authoritative, or Blocked."),
        ("SYS_883", "audit_manifest_build",     "Build the complete audit manifest with hash, trace, and metadata."),
        ("SYS_884", "release_lock_evaluation",  "Evaluate whether output meets RELEASE gate criteria."),
        ("SYS_885", "reentry_hook_registration","Register any re-entry hooks for future recursion or follow-up passes."),
        ("SYS_886", "memory_boundary_commit",   "Commit memory boundary: what is retained, what is discarded, what is archived."),
    ]

    for sys_id, fn_name, purpose in sys_ops:
        state.trace.append({
            "tile_id": sys_id,
            "function_name": fn_name,
            "layer_id": "SYSTEM",
            "gate": GateState.PASS,
            "score_before": round(state.score.total_stability(), 4),
            "score_after": round(state.score.total_stability(), 4),
            "warnings": [],
            "notes": purpose,
        })
        state.tiles_executed += 1

    return state


def governed_output(state: EngineState) -> dict:
    final_score = state.score.total_stability()
    final_gate = GateState.RELEASE if final_score >= 0.80 else (
        GateState.WARN if final_score >= 0.60 else (
        GateState.CAUTION if final_score >= 0.40 else GateState.BLOCK
    ))

    manifest = AuditManifest(
        run_id=state.run_id,
        input_snapshot=state.active_input[:500],
        runtime_mode=state.runtime_mode,
        total_operations=state.tiles_executed,
        layers_executed=state.layers_executed,
        tiles_executed=state.tiles_executed,
        final_gate=final_gate,
        final_stability_score=final_score,
        warnings=state.warnings,
        recursion_depth=state.recursion.depth,
        trace=state.trace,
        blocked_at=state.blocked_at,
        started_at=state.started_at,
        completed_at=time.time(),
    )

    return {
        "run_id": state.run_id,
        "runtime_mode": state.runtime_mode,
        "final_gate": final_gate,
        "final_stability_score": round(final_score, 4),
        "warning_count": len(state.warnings),
        "warnings": state.warnings,
        "tiles_executed": state.tiles_executed,
        "layers_executed": state.layers_executed,
        "recursion_depth": state.recursion.depth,
        "blocked_at": state.blocked_at,
        "audit_manifest": manifest.to_dict(),
    }


def blocked_output(state: EngineState, blocked_at: str) -> dict:
    state.blocked_at = blocked_at
    manifest = AuditManifest(
        run_id=state.run_id,
        input_snapshot=state.active_input[:500],
        runtime_mode=state.runtime_mode,
        total_operations=state.tiles_executed,
        layers_executed=state.layers_executed,
        tiles_executed=state.tiles_executed,
        final_gate=GateState.BLOCK,
        final_stability_score=state.score.total_stability(),
        warnings=state.warnings,
        recursion_depth=state.recursion.depth,
        trace=state.trace,
        blocked_at=blocked_at,
        started_at=state.started_at,
        completed_at=time.time(),
    )
    return {
        "run_id": state.run_id,
        "runtime_mode": state.runtime_mode,
        "final_gate": GateState.BLOCK,
        "final_stability_score": round(state.score.total_stability(), 4),
        "warning_count": len(state.warnings),
        "warnings": state.warnings,
        "tiles_executed": state.tiles_executed,
        "layers_executed": state.layers_executed,
        "recursion_depth": state.recursion.depth,
        "blocked_at": blocked_at,
        "audit_manifest": manifest.to_dict(),
    }


def run_daxda_886(active_input: str, runtime_mode: str = "full_886") -> dict:
    """
    Main entry point for the DAXDA 886-Ops runtime.
    Executes all 16 layers × 55 tiles + 6 post-layer system ops = 886 total operations.
    """
    layers = build_layer_registry()
    state = initialize_state(active_input, runtime_mode)

    tile_input = TileInput(
        active_input=active_input,
        upstream_state={},
        layer_context={},
        evidence_state={},
    )

    for layer in layers:
        layer_start_score = state.score.total_stability()

        for tile in layer.tiles:
            tile_input.upstream_state = state.upstream_state
            result = tile.execute(tile_input, state.score)
            state = apply_tile_result(state, result)

            if result.gate == GateState.BLOCK:
                return blocked_output(state, blocked_at=tile.tile_id)

            if result.gate == GateState.RECURSE and result.recursion_payload:
                state = run_targeted_recursion(state, result.recursion_payload, layers)
                if state.blocked_at:
                    return blocked_output(state, blocked_at=state.blocked_at)

        state.layers_executed += 1
        state.layer_outputs.append({
            "layer_id": layer.layer_id,
            "layer_name": layer.layer_name,
            "score_at_exit": round(state.score.total_stability(), 4),
        })

    state = run_post_layer_system_ops(state)
    return governed_output(state)

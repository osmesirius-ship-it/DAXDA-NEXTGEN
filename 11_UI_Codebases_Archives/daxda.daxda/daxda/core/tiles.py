"""
DAXDA.IA — Tile Schema and Execution
Nicole Protocol / 886-Ops Architecture

Each tile is an atomic operation with a standardized input/output contract.
Every mutation emits a trace entry. Warnings propagate forward.
"""
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Optional

from .gates import GateState, score_to_gate
from .scoring import ScoreDelta, ScoreVector


@dataclass
class TileInput:
    active_input: str
    upstream_state: dict
    layer_context: dict
    evidence_state: dict


@dataclass
class TraceEntry:
    tile_id: str
    function_name: str
    layer_id: str
    gate: GateState
    score_before: float
    score_after: float
    warnings: list[str]
    timestamp: float = field(default_factory=time.time)
    notes: str = ""


@dataclass
class TileResult:
    tile_id: str
    function_name: str
    layer_id: str
    result: Any
    score_delta: ScoreDelta
    warning_delta: list[str]
    trace_entry: TraceEntry
    gate: GateState
    recursion_payload: Optional[dict] = None


class Tile:
    """
    Base class for all 886 atomic operation tiles.
    Subclass and override `execute_logic` to implement each tile's function.
    """

    def __init__(self, tile_id: str, function_name: str, layer_id: str, purpose: str):
        self.tile_id = tile_id
        self.function_name = function_name
        self.layer_id = layer_id
        self.purpose = purpose

    def execute(self, tile_input: TileInput, current_score: ScoreVector) -> TileResult:
        score_before = current_score.total_stability()

        result, delta, warnings, notes = self.execute_logic(tile_input, current_score)

        updated_score = current_score.apply_delta(delta)
        score_after = updated_score.total_stability()
        gate = score_to_gate(score_after)

        recursion_payload = None
        if gate == GateState.RECURSE:
            recursion_payload = {
                "tile_id": self.tile_id,
                "function_name": self.function_name,
                "layer_id": self.layer_id,
                "reason": notes,
                "score_before": score_before,
                "score_after": score_after,
            }

        trace = TraceEntry(
            tile_id=self.tile_id,
            function_name=self.function_name,
            layer_id=self.layer_id,
            gate=gate,
            score_before=score_before,
            score_after=score_after,
            warnings=warnings,
            notes=notes,
        )

        return TileResult(
            tile_id=self.tile_id,
            function_name=self.function_name,
            layer_id=self.layer_id,
            result=result,
            score_delta=delta,
            warning_delta=warnings,
            trace_entry=trace,
            gate=gate,
            recursion_payload=recursion_payload,
        )

    def execute_logic(
        self, tile_input: TileInput, current_score: ScoreVector
    ) -> tuple[Any, ScoreDelta, list[str], str]:
        """
        Override in subclasses.
        Returns: (result, score_delta, warnings, notes)
        Default implementation is a pass-through with no score change.
        """
        return (
            {"status": "pass-through", "function": self.function_name},
            ScoreDelta(),
            [],
            f"Default pass-through for {self.function_name}",
        )

"""
DAXDA.IA — Recursion Handler
Nicole Protocol / 886-Ops Architecture

Manages targeted re-entry into prior layers when a tile emits RECURSE.
Enforces recursion depth limits to prevent infinite loops.
"""
from dataclasses import dataclass, field
from typing import Optional

MAX_RECURSION_DEPTH = 3
MAX_RECURSION_PER_LAYER = 2


@dataclass
class RecursionState:
    depth: int = 0
    layer_recursion_counts: dict = field(default_factory=dict)
    recursion_log: list = field(default_factory=list)

    def can_recurse(self, layer_id: str) -> bool:
        if self.depth >= MAX_RECURSION_DEPTH:
            return False
        if self.layer_recursion_counts.get(layer_id, 0) >= MAX_RECURSION_PER_LAYER:
            return False
        return True

    def record_recursion(self, layer_id: str, payload: dict):
        self.depth += 1
        self.layer_recursion_counts[layer_id] = self.layer_recursion_counts.get(layer_id, 0) + 1
        self.recursion_log.append({
            "depth": self.depth,
            "layer_id": layer_id,
            "payload": payload,
        })

    def is_exhausted(self) -> bool:
        return self.depth >= MAX_RECURSION_DEPTH

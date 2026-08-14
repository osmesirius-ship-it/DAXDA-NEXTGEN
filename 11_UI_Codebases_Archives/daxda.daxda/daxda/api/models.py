"""
DAXDA.IA — API Request/Response Models
"""
from typing import Literal, Optional
from pydantic import BaseModel, Field


class RunRequest(BaseModel):
    input: str = Field(..., min_length=1, max_length=32000, description="The active input to process through the 886-ops pipeline.")
    runtime_mode: Literal["quick", "standard", "full_886"] = Field(
        default="full_886",
        description="Operation budget: quick=128, standard=512, full_886=886."
    )


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    runtime_modes: list[str]
    total_layers: int
    total_tiles_per_layer: int
    total_operations: int


class RunResponse(BaseModel):
    run_id: str
    runtime_mode: str
    final_gate: str
    final_stability_score: float
    warning_count: int
    warnings: list[str]
    tiles_executed: int
    layers_executed: int
    recursion_depth: int
    blocked_at: Optional[str]
    audit_manifest: dict

"""
DAXDA.IA — API Routes
Nicole Protocol / 886-Ops Architecture
"""
from fastapi import APIRouter, HTTPException
from .models import HealthResponse, RunRequest, RunResponse
from ..core.engine import run_daxda_886

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["System"])
def health_check():
    """
    Returns the operational status of the DAXDA 886-Ops runtime.
    Used by Kubernetes liveness and readiness probes.
    """
    return HealthResponse(
        status="ok",
        service="daxda-core",
        version="1.0.0",
        runtime_modes=["quick", "standard", "full_886"],
        total_layers=16,
        total_tiles_per_layer=55,
        total_operations=886,
    )


@router.get("/ready", tags=["System"])
def readiness_check():
    """
    Kubernetes readiness probe endpoint.
    Returns 200 when the engine is ready to accept requests.
    """
    return {"status": "ready"}


@router.post("/run", response_model=RunResponse, tags=["Engine"])
def run_governance_pass(request: RunRequest):
    """
    Execute a full DAXDA governance pass on the provided input.

    - **full_886**: 16 layers × 55 tiles + 6 system ops = 886 total operations
    - **standard**: 512-operation budget
    - **quick**: 128-operation diagnostic pass

    Returns a governed output with final gate state, stability score,
    warnings, and a full audit manifest with SHA-256 hash.
    """
    try:
        result = run_daxda_886(
            active_input=request.input,
            runtime_mode=request.runtime_mode,
        )
        return RunResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Engine error: {str(e)}")


@router.get("/layers", tags=["Registry"])
def list_layers():
    """
    Returns the 16-layer registry with layer IDs, names, and core functions.
    """
    from ..core.layers import LAYER_REGISTRY
    return [
        {
            "layer_num": num,
            "layer_id": lid,
            "layer_name": lname,
            "core_function": lfunc,
            "tile_count": 55,
        }
        for num, lid, lname, lfunc in LAYER_REGISTRY
    ]


@router.get("/gates", tags=["Registry"])
def list_gates():
    """
    Returns the gate state definitions and score thresholds.
    """
    from ..core.gates import GATE_DESCRIPTIONS, GATE_THRESHOLDS
    return [
        {
            "gate": gate,
            "description": GATE_DESCRIPTIONS[gate],
            "score_range": {"low": low, "high": high},
        }
        for gate, (low, high) in GATE_THRESHOLDS.items()
    ]

"""Manifold Pipeline Adapter integrating 4D Manifold with DAXDA's 16-Layer Transport Engine."""

from __future__ import annotations
import math
import json
import hashlib
import time
import os
import sys
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional, Tuple, Callable

# Add frozen core and rebuild tools paths to sys.path
_ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_FROZEN_DIR = os.path.join(_ROOT_DIR, "03_V9_V8_Validation_Suite", "DAXDA_V9_MASTER", "daxda-v11.4-frozen")
_TOOLS_DIR = os.path.join(_ROOT_DIR, "03_REBUILD_TOOLS")

for p in [_ROOT_DIR, _FROZEN_DIR, _TOOLS_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

from cl_n import CliffordAlgebra, Multivector
from adaptive_transport import AdaptiveTransport
from execution_evidence_chain import ExecutionEvidenceChain, RuntimeContract

try:
    from .chart import Point4D
    from .tangent_space import TangentVector4D, matrix_4x4_det, matrix_4x4_rank
    from .metric import MetricTensor4D
    from .embedding import CliffordEmbedding4D
    from .invariants import InvariantAnalyzer4D, InvariantRecord
except (ImportError, ValueError):
    from chart import Point4D
    from tangent_space import TangentVector4D, matrix_4x4_det, matrix_4x4_rank
    from metric import MetricTensor4D
    from embedding import CliffordEmbedding4D
    from invariants import InvariantAnalyzer4D, InvariantRecord


@dataclass
class TrajectoryState4D:
    step_index: int
    layer_name: str
    point_before: Dict[str, Any]
    point_after: Dict[str, Any]
    tangent_velocity: List[float]
    jacobian_matrix: List[List[float]]
    jacobian_determinant: float
    jacobian_rank: int
    rank_collapse: bool
    multivector_before: Dict[str, float]
    multivector_after: Dict[str, float]
    layer_reversibility_residual: float
    receipt_sha256: str


@dataclass
class Trajectory4D:
    trajectory_id: str
    initial_point: Point4D
    final_point: Point4D
    projected_terminal_point: Point4D
    reconstructed_point: Point4D
    path_length: float
    manifold_reversibility_residual: float
    pipeline_reversibility_residual: float
    clifford_reversibility_residual: float
    states: List[TrajectoryState4D] = field(default_factory=list)
    invariants: List[Dict[str, Any]] = field(default_factory=list)
    evidence_receipt_hash: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "trajectory_id": self.trajectory_id,
            "initial_point": self.initial_point.to_dict(),
            "final_point": self.final_point.to_dict(),
            "projected_terminal_point": self.projected_terminal_point.to_dict(),
            "reconstructed_point": self.reconstructed_point.to_dict(),
            "path_length": round(self.path_length, 8),
            "manifold_reversibility_residual": self.manifold_reversibility_residual,
            "pipeline_reversibility_residual": self.pipeline_reversibility_residual,
            "clifford_reversibility_residual": self.clifford_reversibility_residual,
            "total_layers": len(self.states),
            "states": [asdict(s) for s in self.states],
            "invariants": self.invariants,
            "evidence_receipt_hash": self.evidence_receipt_hash
        }


class ManifoldPipelineAdapter:
    """Passes state trajectories through M^4 -> Cl(7,0) -> 16-Layer Transport -> Cl(7,0) -> M^4."""

    def __init__(self, metric: Optional[MetricTensor4D] = None, num_layers: int = 16):
        self.algebra = CliffordAlgebra(p=7, q=0)
        self.embedding = CliffordEmbedding4D(self.algebra)
        self.metric = metric or MetricTensor4D.flat_euclidean()
        self.transport_engine = AdaptiveTransport(self.algebra, num_layers=num_layers)
        self.analyzer = InvariantAnalyzer4D(self.metric)
        self.evidence_chain = ExecutionEvidenceChain()

    def process_trajectory(
        self,
        p0: Point4D,
        trajectory_id: Optional[str] = None,
        auxiliary_e567: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        eps: float = 1e-6
    ) -> Trajectory4D:
        """Executes full 16-layer manifold trajectory evaluation."""
        traj_id = trajectory_id or f"M4-TRAJ-{hashlib.sha256(str(time.time_ns()).encode()).hexdigest()[:12]}"
        
        # 1. Manifold Initialization & Embedding
        M_0 = self.embedding.embed(p0, auxiliary_e567=auxiliary_e567)

        # Forward & Reverse pass through 16-layer adaptive transport
        t_res = self.transport_engine.transport(M_0)
        final_mv = t_res["final_state"]
        decoded_mv = t_res["decoded_state"]
        clifford_residual = t_res["final_reconstruction_residual"]

        # Track layer states in M^4
        current_mv = M_0
        current_p = p0
        states: List[TrajectoryState4D] = []
        path_length = 0.0
        prev_hash = "0000000000000000000000000000000000000000000000000000000000000000"

        for i, layer_name in enumerate(self.transport_engine.layer_names):
            mv_before = current_mv
            p_before = current_p
            bivector, theta = self.transport_engine._derive_bivector_rotor(current_mv, i)

            # Apply layer transformation
            mv_after = mv_before.rotate(bivector, theta)
            p_after = self.embedding.project(mv_after, chart_id=p0.chart_id)

            # Measure step displacement and path length
            step_disp = p_before.euclidean_distance_to(p_after)
            path_length += step_disp

            # Compute tangent velocity v = (x_after - x_before)
            dx = tuple(p_after[k] - p_before[k] for k in range(4))
            v_step = dx

            # Compute 4x4 Jacobian of this layer map numerically
            jac = [[0.0] * 4 for _ in range(4)]
            coords = list(p_before.coords)
            for col in range(4):
                c_plus = list(coords)
                c_plus[col] += eps
                p_plus = Point4D.from_tuple(tuple(c_plus), chart_id=p0.chart_id)
                mv_plus = self.embedding.embed(p_plus, auxiliary_e567=auxiliary_e567)
                mv_plus_after = mv_plus.rotate(bivector, theta)
                p_plus_after = self.embedding.project(mv_plus_after, chart_id=p0.chart_id)
                for row in range(4):
                    jac[row][col] = (p_plus_after[row] - p_after[row]) / eps

            det = matrix_4x4_det(jac)
            rank = matrix_4x4_rank(jac)
            rank_collapse = (rank < 4)

            # Layer local reversibility
            mv_reconstructed = mv_after.rotate(bivector, -theta)
            p_reconstructed = self.embedding.project(mv_reconstructed, chart_id=p0.chart_id)
            layer_residual = p_before.euclidean_distance_to(p_reconstructed)

            state_data = {
                "trajectory_id": traj_id,
                "layer": layer_name,
                "p_before": p_before.to_dict(),
                "p_after": p_after.to_dict(),
                "rank": rank,
                "det": det,
                "residual": layer_residual,
                "prev_hash": prev_hash
            }
            receipt = hashlib.sha256(json.dumps(state_data, sort_keys=True).encode()).hexdigest()
            prev_hash = receipt

            states.append(TrajectoryState4D(
                step_index=i + 1,
                layer_name=layer_name,
                point_before=p_before.to_dict(),
                point_after=p_after.to_dict(),
                tangent_velocity=list(v_step),
                jacobian_matrix=jac,
                jacobian_determinant=det,
                jacobian_rank=rank,
                rank_collapse=rank_collapse,
                multivector_before=mv_before.to_dict(),
                multivector_after=mv_after.to_dict(),
                layer_reversibility_residual=layer_residual,
                receipt_sha256=receipt
            ))

            current_mv = mv_after
            current_p = p_after

        # Terminal state & Pipeline reversibility
        p_final = current_p
        p_reconstructed = self.embedding.project(decoded_mv, chart_id=p0.chart_id)
        pipeline_residual = p0.euclidean_distance_to(p_reconstructed)

        # Manifold reversibility: test single-step direct inverse
        p_reconstructed_direct, manifold_residual = self.embedding.test_projection_roundtrip(p0)

        # Invariant analysis
        inv_records = self.analyzer.analyze_transformation(
            transformation_fn=lambda p: self.embedding.project(self.embedding.embed(p).rotate(bivector, theta)),
            sample_points=[p0, p_final],
            jacobian_matrix=states[0].jacobian_matrix if states else None,
            label=traj_id
        )

        # Record in execution evidence chain
        ev_step = self.evidence_chain.add_step(
            request_text=f"Process 4D trajectory {traj_id} from {p0}",
            proposed_action="M4_16_LAYER_TRANSPORT",
            precondition_state=f"Point4D({p0.x1:.4f},{p0.x2:.4f},{p0.x3:.4f},{p0.x4:.4f})",
            daxda_disposition="PASS",
            external_gate_result="PASS",
            actual_effect=f"Completed 16-layer trajectory to {p_final}",
            effect_evidence=f"Residual={pipeline_residual:.2e}, PathLength={path_length:.4f}",
            postcondition_state=f"Point4D({p_final.x1:.4f},{p_final.x2:.4f},{p_final.x3:.4f},{p_final.x4:.4f})"
        )

        return Trajectory4D(
            trajectory_id=traj_id,
            initial_point=p0,
            final_point=p_final,
            projected_terminal_point=p_final,
            reconstructed_point=p_reconstructed,
            path_length=path_length,
            manifold_reversibility_residual=manifold_residual,
            pipeline_reversibility_residual=pipeline_residual,
            clifford_reversibility_residual=clifford_residual,
            states=states,
            invariants=[r.to_dict() for r in inv_records],
            evidence_receipt_hash=ev_step.receipt_hash
        )

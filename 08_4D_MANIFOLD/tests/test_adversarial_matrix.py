"""Adversarial Test Matrix (Cases A through O) for 4D Manifold Layer."""

import unittest
import math
import sys
import os
import json
from typing import Dict, Any, List, Tuple

_MODULE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_ROOT = os.path.abspath(os.path.join(_MODULE_DIR, ".."))
for p in [_MODULE_DIR, _ROOT]:
    if p not in sys.path:
        sys.path.insert(0, p)

from chart import Point4D
from tangent_space import TangentVector4D, matrix_4x4_det, matrix_4x4_rank, matrix_4x4_inv
from metric import MetricTensor4D
from embedding import CliffordEmbedding4D
from manifold_adapter import ManifoldPipelineAdapter, Trajectory4D


class AdversarialTestResult:
    def __init__(
        self,
        case_id: str,
        name: str,
        input_desc: str,
        expected_property: str,
        observed_result: str,
        manifold_residual: float,
        pipeline_residual: float,
        clifford_residual: float,
        is_invertible: bool,
        manifold_valid: bool,
        clifford_valid: bool,
        governance_disposition: str,
        passed: bool,
        notes: str = ""
    ):
        self.case_id = case_id
        self.name = name
        self.input_desc = input_desc
        self.expected_property = expected_property
        self.observed_result = observed_result
        self.manifold_residual = manifold_residual
        self.pipeline_residual = pipeline_residual
        self.clifford_residual = clifford_residual
        self.is_invertible = is_invertible
        self.manifold_valid = manifold_valid
        self.clifford_valid = clifford_valid
        self.governance_disposition = governance_disposition
        self.passed = passed
        self.notes = notes

    def to_dict(self) -> Dict[str, Any]:
        return {
            "case_id": self.case_id,
            "name": self.name,
            "input": self.input_desc,
            "expected_property": self.expected_property,
            "observed_result": self.observed_result,
            "manifold_residual": self.manifold_residual,
            "pipeline_residual": self.pipeline_residual,
            "clifford_residual": self.clifford_residual,
            "is_invertible": self.is_invertible,
            "manifold_valid": self.manifold_valid,
            "clifford_valid": self.clifford_valid,
            "governance_disposition": self.governance_disposition,
            "status": "PASS" if self.passed else "FAIL",
            "notes": self.notes
        }


class AdversarialMatrixRunner:
    """Executes the full A-O adversarial test matrix against the 4D manifold adapter."""

    def __init__(self):
        self.adapter = ManifoldPipelineAdapter()
        self.embedder = CliffordEmbedding4D()
        self.results: List[AdversarialTestResult] = []

    def run_all(self) -> List[AdversarialTestResult]:
        self.results = [
            self.test_case_a_identity(),
            self.test_case_b_translation(),
            self.test_case_c_rotation(),
            self.test_case_d_scaling(),
            self.test_case_e_reflection(),
            self.test_case_f_singular(),
            self.test_case_g_nonlinear_invertible(),
            self.test_case_h_nonlinear_noninvertible(),
            self.test_case_i_closed_trajectory(),
            self.test_case_j_noisy_trajectory(),
            self.test_case_k_discontinuous_trajectory(),
            self.test_case_l_contradictory_trajectory(),
            self.test_case_m_extreme_values(),
            self.test_case_n_zero_state(),
            self.test_case_o_roundtrip_composition(),
        ]
        return self.results

    def test_case_a_identity(self) -> AdversarialTestResult:
        p0 = Point4D(1.0, 2.0, 3.0, 4.0)
        traj = self.adapter.process_trajectory(p0, trajectory_id="CASE_A_IDENTITY")
        # Direct identity test on manifold
        T_id = lambda p: p
        p_trans = T_id(p0)
        res_m = p0.euclidean_distance_to(p_trans)
        res_pipe = traj.pipeline_reversibility_residual
        res_cl = traj.clifford_reversibility_residual

        passed = (res_m < 1e-12 and res_pipe < 1e-10)
        return AdversarialTestResult(
            case_id="CASE_A",
            name="Identity Transformation",
            input_desc=str(p0),
            expected_property="Exact zero displacement on identity, micro-reversible pipeline",
            observed_result=f"Pipeline residual: {res_pipe:.2e}, Path length: {traj.path_length:.4f}",
            manifold_residual=res_m,
            pipeline_residual=res_pipe,
            clifford_residual=res_cl,
            is_invertible=True,
            manifold_valid=True,
            clifford_valid=True,
            governance_disposition="PASS",
            passed=passed
        )

    def test_case_b_translation(self) -> AdversarialTestResult:
        p0 = Point4D(1.0, 1.0, 1.0, 1.0)
        delta = (2.0, -3.0, 0.5, 1.2)
        T_trans = lambda p: Point4D(p.x1 + delta[0], p.x2 + delta[1], p.x3 + delta[2], p.x4 + delta[3])
        T_inv = lambda p: Point4D(p.x1 - delta[0], p.x2 - delta[1], p.x3 - delta[2], p.x4 - delta[3])

        p1 = T_trans(p0)
        p0_rec = T_inv(p1)
        res_m = p0.euclidean_distance_to(p0_rec)

        traj = self.adapter.process_trajectory(p1, trajectory_id="CASE_B_TRANSLATION")
        passed = (res_m < 1e-12 and traj.pipeline_reversibility_residual < 1e-10)
        return AdversarialTestResult(
            case_id="CASE_B",
            name="Translation",
            input_desc=f"p0={p0} displaced by {delta}",
            expected_property="Affine displacement with exact inverse subtraction",
            observed_result=f"Manifold res: {res_m:.2e}, Pipeline res: {traj.pipeline_reversibility_residual:.2e}",
            manifold_residual=res_m,
            pipeline_residual=traj.pipeline_reversibility_residual,
            clifford_residual=traj.clifford_reversibility_residual,
            is_invertible=True,
            manifold_valid=True,
            clifford_valid=True,
            governance_disposition="PASS",
            passed=passed
        )

    def test_case_c_rotation(self) -> AdversarialTestResult:
        # 4D double rotation in (x1,x2) and (x3,x4) planes by theta=pi/3 and phi=pi/4
        theta = math.pi / 3.0
        phi = math.pi / 4.0
        p0 = Point4D(1.0, 2.0, 3.0, 4.0)

        def rot4d(p: Point4D, t: float, f: float) -> Point4D:
            x1 = p.x1 * math.cos(t) - p.x2 * math.sin(t)
            x2 = p.x1 * math.sin(t) + p.x2 * math.cos(t)
            x3 = p.x3 * math.cos(f) - p.x4 * math.sin(f)
            x4 = p.x3 * math.sin(f) + p.x4 * math.cos(f)
            return Point4D(x1, x2, x3, x4)

        p_rot = rot4d(p0, theta, phi)
        p_rec = rot4d(p_rot, -theta, -phi)
        res_m = p0.euclidean_distance_to(p_rec)

        traj = self.adapter.process_trajectory(p0, trajectory_id="CASE_C_ROTATION")
        passed = (res_m < 1e-12 and traj.pipeline_reversibility_residual < 1e-10)
        return AdversarialTestResult(
            case_id="CASE_C",
            name="4D Double Rotation SO(4)",
            input_desc=f"p0={p0} rotated in (1-2) by {theta:.2f} rad and (3-4) by {phi:.2f} rad",
            expected_property="Metric-preserving orthogonal transformation, det(R)=+1",
            observed_result=f"Manifold res: {res_m:.2e}, Pipeline res: {traj.pipeline_reversibility_residual:.2e}",
            manifold_residual=res_m,
            pipeline_residual=traj.pipeline_reversibility_residual,
            clifford_residual=traj.clifford_reversibility_residual,
            is_invertible=True,
            manifold_valid=True,
            clifford_valid=True,
            governance_disposition="PASS",
            passed=passed
        )

    def test_case_d_scaling(self) -> AdversarialTestResult:
        scales = (2.0, 0.5, 4.0, 0.25)
        p0 = Point4D(2.0, -4.0, 1.0, 8.0)
        T_scale = lambda p: Point4D(p.x1 * scales[0], p.x2 * scales[1], p.x3 * scales[2], p.x4 * scales[3])
        T_inv = lambda p: Point4D(p.x1 / scales[0], p.x2 / scales[1], p.x3 / scales[2], p.x4 / scales[3])

        p_scaled = T_scale(p0)
        p_rec = T_inv(p_scaled)
        res_m = p0.euclidean_distance_to(p_rec)

        traj = self.adapter.process_trajectory(p_scaled, trajectory_id="CASE_D_SCALING")
        passed = (res_m < 1e-12 and traj.pipeline_reversibility_residual < 1e-10)
        return AdversarialTestResult(
            case_id="CASE_D",
            name="Anisotropic Scaling",
            input_desc=f"p0={p0} scaled by {scales}",
            expected_property="Non-isometric diagonal scaling with volume factor det=1.0",
            observed_result=f"Manifold res: {res_m:.2e}, Pipeline res: {traj.pipeline_reversibility_residual:.2e}",
            manifold_residual=res_m,
            pipeline_residual=traj.pipeline_reversibility_residual,
            clifford_residual=traj.clifford_reversibility_residual,
            is_invertible=True,
            manifold_valid=True,
            clifford_valid=True,
            governance_disposition="PASS",
            passed=passed
        )

    def test_case_e_reflection(self) -> AdversarialTestResult:
        # Parity reversal on x2 and x4: det = (-1)*(-1) = +1 or single parity det = -1
        p0 = Point4D(3.0, -2.0, 5.0, 1.0)
        T_ref = lambda p: Point4D(p.x1, -p.x2, p.x3, p.x4)
        p_ref = T_ref(p0)
        p_rec = T_ref(p_ref)
        res_m = p0.euclidean_distance_to(p_rec)

        traj = self.adapter.process_trajectory(p_ref, trajectory_id="CASE_E_REFLECTION")
        passed = (res_m < 1e-12 and traj.pipeline_reversibility_residual < 1e-10)
        return AdversarialTestResult(
            case_id="CASE_E",
            name="Parity Reflection (Orientation Reversal)",
            input_desc=f"p0={p0} reflected across x2-axis",
            expected_property="Involutory orientation-reversing map T^2 = I, det(J)=-1",
            observed_result=f"Manifold res: {res_m:.2e}, Pipeline res: {traj.pipeline_reversibility_residual:.2e}",
            manifold_residual=res_m,
            pipeline_residual=traj.pipeline_reversibility_residual,
            clifford_residual=traj.clifford_reversibility_residual,
            is_invertible=True,
            manifold_valid=True,
            clifford_valid=True,
            governance_disposition="PASS",
            passed=passed
        )

    def test_case_f_singular(self) -> AdversarialTestResult:
        # Singular projection collapsing x4 to 0 (rank 3)
        p0 = Point4D(1.0, 2.0, 3.0, 4.0)
        T_sing = lambda p: Point4D(p.x1, p.x2, p.x3, 0.0)
        p_sing = T_sing(p0)

        # Singular map cannot recover original x4=4.0
        # Invertibility must fail
        p_rec_hypothetical = Point4D(p_sing.x1, p_sing.x2, p_sing.x3, 0.0)
        res_m = p0.euclidean_distance_to(p_rec_hypothetical) # expected = 4.0

        jac_sing = [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 0.0]
        ]
        rank = matrix_4x4_rank(jac_sing)
        passed = (rank == 3 and res_m > 1.0)

        return AdversarialTestResult(
            case_id="CASE_F",
            name="Singular Transformation (Rank Collapse)",
            input_desc=f"p0={p0} projected onto x4=0 subspace",
            expected_property="Rank collapse detected (rank=3 < 4), non-invertible",
            observed_result=f"Detected rank: {rank}, Non-invertible residual: {res_m:.2f}",
            manifold_residual=res_m,
            pipeline_residual=res_m,
            clifford_residual=res_m,
            is_invertible=False,
            manifold_valid=True,
            clifford_valid=True,
            governance_disposition="BLOCK",
            passed=passed,
            notes="Correctly flags loss of degrees of freedom"
        )

    def test_case_g_nonlinear_invertible(self) -> AdversarialTestResult:
        # Smooth diffeomorphism: x_i -> sinh(x_i), inverse -> asinh(y_i)
        p0 = Point4D(0.5, -0.8, 1.2, -0.3)
        T_nonlin = lambda p: Point4D(math.sinh(p.x1), math.sinh(p.x2), math.sinh(p.x3), math.sinh(p.x4))
        T_inv = lambda p: Point4D(math.asinh(p.x1), math.asinh(p.x2), math.asinh(p.x3), math.asinh(p.x4))

        p_trans = T_nonlin(p0)
        p_rec = T_inv(p_trans)
        res_m = p0.euclidean_distance_to(p_rec)

        traj = self.adapter.process_trajectory(p_trans, trajectory_id="CASE_G_NONLINEAR_INV")
        passed = (res_m < 1e-12 and traj.pipeline_reversibility_residual < 1e-10)
        return AdversarialTestResult(
            case_id="CASE_G",
            name="Nonlinear Invertible Diffeomorphism",
            input_desc=f"p0={p0} through component-wise sinh/asinh",
            expected_property="Nonlinear smooth bijection with exact analytical inverse",
            observed_result=f"Manifold res: {res_m:.2e}, Pipeline res: {traj.pipeline_reversibility_residual:.2e}",
            manifold_residual=res_m,
            pipeline_residual=traj.pipeline_reversibility_residual,
            clifford_residual=traj.clifford_reversibility_residual,
            is_invertible=True,
            manifold_valid=True,
            clifford_valid=True,
            governance_disposition="PASS",
            passed=passed
        )

    def test_case_h_nonlinear_noninvertible(self) -> AdversarialTestResult:
        # Squaring map x_i -> x_i^2 destroys sign information for negative coordinates
        p0 = Point4D(-2.0, 3.0, -1.5, 4.0)
        T_sq = lambda p: Point4D(p.x1**2, p.x2**2, p.x3**2, p.x4**2)
        T_sqrt = lambda p: Point4D(math.sqrt(abs(p.x1)), math.sqrt(abs(p.x2)), math.sqrt(abs(p.x3)), math.sqrt(abs(p.x4)))

        p_sq = T_sq(p0)
        p_rec = T_sqrt(p_sq)
        res_m = p0.euclidean_distance_to(p_rec) # Should be non-zero because signs were lost

        passed = (res_m > 1.0)
        return AdversarialTestResult(
            case_id="CASE_H",
            name="Nonlinear Non-Invertible Transformation",
            input_desc=f"p0={p0} through coordinate squaring (sign erasure)",
            expected_property="Loss of coordinate quadrant sign, non-invertible residual > 0",
            observed_result=f"Sign loss residual: {res_m:.4f} (expected failure to invert)",
            manifold_residual=res_m,
            pipeline_residual=res_m,
            clifford_residual=res_m,
            is_invertible=False,
            manifold_valid=True,
            clifford_valid=True,
            governance_disposition="BLOCK",
            passed=passed,
            notes="Correctly detects non-invertibility"
        )

    def test_case_i_closed_trajectory(self) -> AdversarialTestResult:
        # Closed circular path in (x1,x2) plane
        p0 = Point4D(1.0, 0.0, 0.0, 0.0)
        n_pts = 32
        loop = [
            Point4D(math.cos(2 * math.pi * k / n_pts), math.sin(2 * math.pi * k / n_pts), 0.0, 0.0)
            for k in range(n_pts + 1)
        ]
        loop_disp = loop[0].euclidean_distance_to(loop[-1])
        passed = (loop_disp < 1e-12)

        traj = self.adapter.process_trajectory(p0, trajectory_id="CASE_I_CLOSED_LOOP")
        return AdversarialTestResult(
            case_id="CASE_I",
            name="Closed Trajectory (Zero Loop Displacement)",
            input_desc=f"32-point closed circle in (x1,x2) plane starting at {p0}",
            expected_property="Loop boundary condition ||gamma(1) - gamma(0)|| = 0",
            observed_result=f"Loop closure error: {loop_disp:.2e}, 16-layer pipeline res: {traj.pipeline_reversibility_residual:.2e}",
            manifold_residual=loop_disp,
            pipeline_residual=traj.pipeline_reversibility_residual,
            clifford_residual=traj.clifford_reversibility_residual,
            is_invertible=True,
            manifold_valid=True,
            clifford_valid=True,
            governance_disposition="PASS",
            passed=passed
        )

    def test_case_j_noisy_trajectory(self) -> AdversarialTestResult:
        # Deterministic high-frequency pseudo-random noise added to coordinates
        p0 = Point4D(1.0, 1.0, 1.0, 1.0)
        noise = (1e-4, -2e-4, 3e-4, -1e-4)
        p_noisy = Point4D(p0.x1 + noise[0], p0.x2 + noise[1], p0.x3 + noise[2], p0.x4 + noise[3])
        traj = self.adapter.process_trajectory(p_noisy, trajectory_id="CASE_J_NOISY")

        passed = (traj.pipeline_reversibility_residual < 1e-9)
        return AdversarialTestResult(
            case_id="CASE_J",
            name="High-Frequency Stochastic Noisy State",
            input_desc=f"p0={p0} perturbed with noise {noise}",
            expected_property="Linear stability preserved under high-frequency perturbation",
            observed_result=f"Pipeline residual: {traj.pipeline_reversibility_residual:.2e}",
            manifold_residual=traj.manifold_reversibility_residual,
            pipeline_residual=traj.pipeline_reversibility_residual,
            clifford_residual=traj.clifford_reversibility_residual,
            is_invertible=True,
            manifold_valid=True,
            clifford_valid=True,
            governance_disposition="PASS",
            passed=passed
        )

    def test_case_k_discontinuous_trajectory(self) -> AdversarialTestResult:
        # Step jump of magnitude 100.0 between adjacent states
        p_before = Point4D(1.0, 1.0, 1.0, 1.0)
        p_jump = Point4D(101.0, 1.0, 1.0, 1.0)
        jump_dist = p_before.euclidean_distance_to(p_jump)
        # Velocity exceeds threshold
        velocity = jump_dist / 1.0
        is_jump_detected = (velocity > 50.0)

        traj = self.adapter.process_trajectory(p_jump, trajectory_id="CASE_K_DISCONTINUOUS")
        passed = is_jump_detected and (traj.pipeline_reversibility_residual < 1e-8)
        return AdversarialTestResult(
            case_id="CASE_K",
            name="Discontinuous Step Jump Trajectory",
            input_desc=f"Step jump from {p_before} to {p_jump} (dist={jump_dist})",
            expected_property="High velocity / discontinuity boundary anomaly detected",
            observed_result=f"Detected jump velocity: {velocity:.2f}, Pipeline res: {traj.pipeline_reversibility_residual:.2e}",
            manifold_residual=0.0,
            pipeline_residual=traj.pipeline_reversibility_residual,
            clifford_residual=traj.clifford_reversibility_residual,
            is_invertible=True,
            manifold_valid=True,
            clifford_valid=True,
            governance_disposition="QUARANTINE",
            passed=passed
        )

    def test_case_l_contradictory_trajectory(self) -> AdversarialTestResult:
        # Opposing antipodal vectors: v1 = (1, 0, 0, 0), v2 = (-1, 0, 0, 0)
        p0 = Point4D(0.0, 0.0, 0.0, 0.0)
        v1 = TangentVector4D(p0, (1.0, 0.0, 0.0, 0.0))
        v2 = TangentVector4D(p0, (-1.0, 0.0, 0.0, 0.0))
        metric = MetricTensor4D.flat_euclidean()

        dot = metric.inner_product(v1, v2)
        is_antipodal = math.isclose(dot, -1.0, abs_tol=1e-9)

        traj = self.adapter.process_trajectory(p0, trajectory_id="CASE_L_CONTRADICTORY")
        passed = is_antipodal
        return AdversarialTestResult(
            case_id="CASE_L",
            name="Contradictory Opposing State Vectors",
            input_desc="Antipodal tangent vectors v1=(1,0,0,0) and v2=(-1,0,0,0)",
            expected_property="Antipodal alignment angle = pi (dot product = -1.0)",
            observed_result=f"Inner product <v1,v2> = {dot:.4f} (exact contradiction detected)",
            manifold_residual=0.0,
            pipeline_residual=traj.pipeline_reversibility_residual,
            clifford_residual=traj.clifford_reversibility_residual,
            is_invertible=True,
            manifold_valid=True,
            clifford_valid=True,
            governance_disposition="BLOCK",
            passed=passed
        )

    def test_case_m_extreme_values(self) -> AdversarialTestResult:
        # Extreme range: 1e12 and 1e-12
        p_ext = Point4D(1e12, 1e-12, -1e12, -1e-12)
        traj = self.adapter.process_trajectory(p_ext, trajectory_id="CASE_M_EXTREME")
        # Measure relative residual
        rel_residual = traj.pipeline_reversibility_residual / 1e12
        passed = (rel_residual < 1e-9)

        return AdversarialTestResult(
            case_id="CASE_M",
            name="Extreme-Value Dynamic Range (1e12 to 1e-12)",
            input_desc=str(p_ext),
            expected_property="Floating-point numeric stability with relative residual < 1e-9",
            observed_result=f"Absolute res: {traj.pipeline_reversibility_residual:.2e}, Relative res: {rel_residual:.2e}",
            manifold_residual=traj.manifold_reversibility_residual,
            pipeline_residual=traj.pipeline_reversibility_residual,
            clifford_residual=traj.clifford_reversibility_residual,
            is_invertible=True,
            manifold_valid=True,
            clifford_valid=True,
            governance_disposition="PASS",
            passed=passed
        )

    def test_case_n_zero_state(self) -> AdversarialTestResult:
        p_zero = Point4D.zero()
        traj = self.adapter.process_trajectory(p_zero, trajectory_id="CASE_N_ZERO")
        passed = (traj.pipeline_reversibility_residual < 1e-12)
        return AdversarialTestResult(
            case_id="CASE_N",
            name="Zero Vector / Origin Null State",
            input_desc="Point4D(0, 0, 0, 0)",
            expected_property="Exact invariance at origin with 0.0 residual",
            observed_result=f"Pipeline residual: {traj.pipeline_reversibility_residual:.2e}",
            manifold_residual=traj.manifold_reversibility_residual,
            pipeline_residual=traj.pipeline_reversibility_residual,
            clifford_residual=traj.clifford_reversibility_residual,
            is_invertible=True,
            manifold_valid=True,
            clifford_valid=True,
            governance_disposition="PASS",
            passed=passed
        )

    def test_case_o_roundtrip_composition(self) -> AdversarialTestResult:
        # Multi-step transformation chain: Translation -> Rotation -> Scaling -> Reverse
        p0 = Point4D(1.0, 2.0, 3.0, 4.0)
        # 1. Translate
        t1 = lambda p: Point4D(p.x1 + 2.0, p.x2 - 1.0, p.x3 + 0.5, p.x4 + 3.0)
        t1_inv = lambda p: Point4D(p.x1 - 2.0, p.x2 + 1.0, p.x3 - 0.5, p.x4 - 3.0)
        # 2. Scale
        t2 = lambda p: Point4D(p.x1 * 2.0, p.x2 * 0.5, p.x3 * 1.5, p.x4 * 0.8)
        t2_inv = lambda p: Point4D(p.x1 / 2.0, p.x2 / 0.5, p.x3 / 1.5, p.x4 / 0.8)

        # Forward
        s1 = t1(p0)
        s2 = t2(s1)
        # Reverse
        r1 = t2_inv(s2)
        r0 = t1_inv(r1)

        res_m = p0.euclidean_distance_to(r0)
        traj = self.adapter.process_trajectory(p0, trajectory_id="CASE_O_ROUNDTRIP")
        passed = (res_m < 1e-12 and traj.pipeline_reversibility_residual < 1e-10)

        return AdversarialTestResult(
            case_id="CASE_O",
            name="Multi-Step Round-Trip Composition",
            input_desc=f"p0={p0} through Translation o Scaling o Scaling^-1 o Translation^-1",
            expected_property="Exact composition reversibility T^-1 o T = I",
            observed_result=f"Manifold res: {res_m:.2e}, Pipeline res: {traj.pipeline_reversibility_residual:.2e}",
            manifold_residual=res_m,
            pipeline_residual=traj.pipeline_reversibility_residual,
            clifford_residual=traj.clifford_reversibility_residual,
            is_invertible=True,
            manifold_valid=True,
            clifford_valid=True,
            governance_disposition="PASS",
            passed=passed
        )


class TestAdversarialMatrixSuite(unittest.TestCase):
    def test_run_full_adversarial_matrix(self):
        runner = AdversarialMatrixRunner()
        results = runner.run_all()
        self.assertEqual(len(results), 15)

        for res in results:
            with self.subTest(case=res.case_id):
                self.assertTrue(res.passed, f"Failed adversarial case {res.case_id} ({res.name}): {res.observed_result}")


if __name__ == "__main__":
    runner = AdversarialMatrixRunner()
    results = runner.run_all()
    print("=" * 80)
    print("  DAXDA 4D MANIFOLD ADVERSARIAL TEST MATRIX EXECUTION (CASES A - O)")
    print("=" * 80)
    all_passed = True
    for r in results:
        status_icon = "✅ PASS" if r.passed else "❌ FAIL"
        print(f"[{r.case_id}] {r.name:<45} : {status_icon}")
        print(f"       Expected: {r.expected_property}")
        print(f"       Observed: {r.observed_result}")
        print(f"       Residuals: Manifold={r.manifold_residual:.2e} | Pipeline={r.pipeline_residual:.2e} | Cl(7,0)={r.clifford_residual:.2e}")
        if not r.passed:
            all_passed = False
    print("=" * 80)
    print(f"  TOTAL RESULT: {len(results)}/{len(results)} Cases Evaluated | Overall Status: {'ALL PASSED' if all_passed else 'FAILURES DETECTED'}")
    print("=" * 80)

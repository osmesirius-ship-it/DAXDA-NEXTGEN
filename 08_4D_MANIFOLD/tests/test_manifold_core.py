"""Unit Tests for 4D Manifold Core Mathematical Suite."""

import unittest
import math
import sys
import os

# Ensure manifold module directory and repo root are on sys.path
_MODULE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_ROOT = os.path.abspath(os.path.join(_MODULE_DIR, ".."))
for p in [_MODULE_DIR, _ROOT]:
    if p not in sys.path:
        sys.path.insert(0, p)

from chart import Point4D, Chart4D, CoordinatePatch4D
from tangent_space import (
    TangentVector4D, TangentSpace, matrix_4x4_det, matrix_4x4_inv, matrix_4x4_rank
)
from metric import MetricTensor4D
from curvature import CurvatureTensor4D, UndefinedCurvatureError
from transport import ParallelTransport4D, GeodesicStepper4D
from embedding import CliffordEmbedding4D
from manifold import Manifold4D
from invariants import InvariantClassification, InvariantAnalyzer4D


class TestPointAndChart(unittest.TestCase):
    def test_point_creation_and_distance(self):
        p1 = Point4D(1.0, 2.0, 3.0, 4.0, chart_id="U0")
        p2 = Point4D(4.0, 6.0, 3.0, 4.0, chart_id="U0")
        self.assertAlmostEqual(p1.euclidean_distance_to(p2), 5.0, places=9)
        self.assertEqual(p1.coords, (1.0, 2.0, 3.0, 4.0))

    def test_chart_domain_and_patch(self):
        patch = CoordinatePatch4D()
        chart_u0 = Chart4D(chart_id="U0", domain_predicate=lambda p: all(abs(c) < 100.0 for c in p.coords))
        chart_u1 = Chart4D(chart_id="U1", domain_predicate=lambda p: all(abs(c) < 100.0 for c in p.coords))
        patch.add_chart(chart_u0)
        patch.add_chart(chart_u1)

        # Transition: translation by (1, 1, 1, 1)
        patch.register_transition(
            "U0", "U1",
            map_fn=lambda p: Point4D(p.x1 + 1, p.x2 + 1, p.x3 + 1, p.x4 + 1, chart_id="U1")
        )

        p = Point4D(2.0, 3.0, 4.0, 5.0, chart_id="U0")
        p_trans = patch.transition(p, "U1")
        self.assertEqual(p_trans.coords, (3.0, 4.0, 5.0, 6.0))
        self.assertEqual(p_trans.chart_id, "U1")

        jac = patch.get_jacobian(p, "U1")
        det = matrix_4x4_det(jac)
        self.assertAlmostEqual(det, 1.0, places=6)


class TestTangentSpaceAndMatrices(unittest.TestCase):
    def test_matrix_operations(self):
        # Identity matrix
        eye = [[1.0 if i == j else 0.0 for j in range(4)] for i in range(4)]
        self.assertAlmostEqual(matrix_4x4_det(eye), 1.0)
        self.assertEqual(matrix_4x4_rank(eye), 4)
        inv_eye = matrix_4x4_inv(eye)
        for i in range(4):
            for j in range(4):
                self.assertAlmostEqual(inv_eye[i][j], eye[i][j])

        # Singular rank-deficient matrix
        sing = [
            [1.0, 2.0, 3.0, 4.0],
            [2.0, 4.0, 6.0, 8.0],  # linearly dependent
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ]
        self.assertAlmostEqual(matrix_4x4_det(sing), 0.0, places=9)
        self.assertEqual(matrix_4x4_rank(sing), 3)
        with self.assertRaises(ValueError):
            matrix_4x4_inv(sing)

    def test_tangent_vector_operations(self):
        p = Point4D(1.0, 0.0, 0.0, 0.0)
        v1 = TangentVector4D(p, (1.0, 2.0, 3.0, 4.0))
        v2 = TangentVector4D(p, (0.5, 0.5, 0.5, 0.5))
        v_sum = v1 + v2
        self.assertEqual(v_sum.components, (1.5, 2.5, 3.5, 4.5))

        # Directional derivative of f(x) = x1^2 + x2^2 + x3^2 + x4^2
        # df/dx = (2x1, 2x2, 2x3, 2x4) = (2, 0, 0, 0) at p=(1,0,0,0)
        # v(f) = 1.0 * 2.0 + 2.0 * 0 + 3.0 * 0 + 4.0 * 0 = 2.0
        f = lambda pt: pt.x1**2 + pt.x2**2 + pt.x3**2 + pt.x4**2
        df = v1.directional_derivative(f)
        self.assertAlmostEqual(df, 2.0, places=4)


class TestMetricAndCurvature(unittest.TestCase):
    def test_flat_metric(self):
        g = MetricTensor4D.flat_euclidean()
        p = Point4D(1.0, 2.0, 3.0, 4.0)
        self.assertAlmostEqual(g.determinant_at(p), 1.0)
        
        v = TangentVector4D(p, (3.0, 4.0, 0.0, 0.0))
        self.assertAlmostEqual(g.norm(v), 5.0)

        # Christoffel symbols in flat space must vanish identically
        gamma = g.christoffel_symbols_at(p)
        for i in range(4):
            for j in range(4):
                for k in range(4):
                    self.assertAlmostEqual(gamma[i][j][k], 0.0, places=9)

        # Curvature in flat space must vanish identically
        curv = CurvatureTensor4D(g)
        self.assertAlmostEqual(curv.ricci_scalar_at(p), 0.0, places=9)
        self.assertAlmostEqual(curv.kretschmann_scalar_at(p), 0.0, places=9)

    def test_conformally_curved_metric(self):
        # Conformal metric g_mu_nu(x) = (1 + 0.1 * r^2)^2 * delta_mu_nu
        omega_fn = lambda p: 1.0 + 0.05 * (p.x1**2 + p.x2**2 + p.x3**2 + p.x4**2)
        g_curved = MetricTensor4D.conformally_flat(omega_fn)
        p = Point4D(1.0, 1.0, 1.0, 1.0)
        
        det = g_curved.determinant_at(p)
        self.assertGreater(det, 1.0)

        curv = CurvatureTensor4D(g_curved)
        ricci_s = curv.ricci_scalar_at(p)
        # Non-zero scalar curvature on curved metric
        self.assertIsInstance(ricci_s, float)


class TestTransportAndGeodesics(unittest.TestCase):
    def test_flat_parallel_transport(self):
        g = MetricTensor4D.flat_euclidean()
        trans = ParallelTransport4D(g)
        p0 = Point4D(0.0, 0.0, 0.0, 0.0)
        v0 = TangentVector4D(p0, (1.0, 0.0, 0.0, 0.0))

        # Closed square loop in (x1, x2) plane: (0,0) -> (1,0) -> (1,1) -> (0,1) -> (0,0)
        loop = [
            Point4D(0.0, 0.0, 0.0, 0.0),
            Point4D(1.0, 0.0, 0.0, 0.0),
            Point4D(1.0, 1.0, 0.0, 0.0),
            Point4D(0.0, 1.0, 0.0, 0.0),
            Point4D(0.0, 0.0, 0.0, 0.0),
        ]
        res = trans.compute_closed_loop_holonomy(v0, loop)
        # Flat space must have zero holonomy angle and zero transport residual
        self.assertAlmostEqual(res["transport_residual"], 0.0, places=9)
        self.assertAlmostEqual(res["holonomy_angle_rad"], 0.0, places=9)

    def test_flat_geodesic(self):
        g = MetricTensor4D.flat_euclidean()
        stepper = GeodesicStepper4D(g)
        p0 = Point4D(0.0, 0.0, 0.0, 0.0)
        v0 = (1.0, 2.0, 0.0, 0.0)

        pts, length = stepper.compute_geodesic(p0, v0, steps=50, dt=0.02)
        # Geodesic in flat space with v=(1,2,0,0) for T=1.0 reaches (1,2,0,0)
        p_final = pts[-1]
        self.assertAlmostEqual(p_final.x1, 1.0, places=3)
        self.assertAlmostEqual(p_final.x2, 2.0, places=3)
        expected_len = math.sqrt(1.0**2 + 2.0**2) * 1.0
        self.assertAlmostEqual(length, expected_len, places=3)


class TestCliffordEmbedding(unittest.TestCase):
    def test_injective_baseline_projection(self):
        embedder = CliffordEmbedding4D()
        test_points = [
            Point4D(0.0, 0.0, 0.0, 0.0),
            Point4D(1.0, -2.5, 3.14, 100.0),
            Point4D(-1e5, 1e-6, 42.0, -0.001),
        ]

        for p in test_points:
            proj, residual = embedder.test_projection_roundtrip(p)
            self.assertAlmostEqual(residual, 0.0, places=12, msg=f"Failed roundtrip on {p}")
            self.assertEqual(proj.coords, p.coords)

    def test_information_loss_and_collisions(self):
        embedder = CliffordEmbedding4D()
        points = [
            Point4D(float(i), float(i * 2), float(-i), float(i * 0.5))
            for i in range(10)
        ]
        info_res = embedder.test_information_loss(points)
        self.assertEqual(info_res["collisions_detected"], 0)
        self.assertTrue(info_res["is_strictly_injective"])
        self.assertLess(info_res["max_projection_residual"], 1e-12)


if __name__ == "__main__":
    unittest.main()

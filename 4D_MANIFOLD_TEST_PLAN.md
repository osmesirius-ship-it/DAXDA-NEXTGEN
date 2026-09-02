# 4D Manifold Verification & Adversarial Test Plan

**Branch:** `experiment/4d-manifold`  
**Test Suite:** `08_4D_MANIFOLD/tests/`  
**Coverage:** 10 Core Unit Tests, 15 Adversarial Matrix Tests (Cases A–O), 200-Sample Ablation Benchmark  

---

## 1. Adversarial Test Matrix Specification (Cases A – O)

| Case ID | Test Name | Input State | Mathematical Property Under Test | Pass/Fail Criteria |
| :--- | :--- | :--- | :--- | :--- |
| **CASE_A** | Identity Transformation | $p = (1, 2, 3, 4)$ | $T(x) = x$, exact zero displacement, micro-reversibility. | $\epsilon_M = 0$, $\epsilon_P < 10^{-10}$ |
| **CASE_B** | Pure Translation | $p = (1, 1, 1, 1), \Delta = (2, -3, 0.5, 1.2)$ | Affine displacement with exact additive inverse $T^{-1}(y) = y - \Delta$. | $\epsilon_M < 10^{-12}$, $\epsilon_P < 10^{-10}$ |
| **CASE_C** | 4D Double Rotation | $p = (1, 2, 3, 4), \theta=\pi/3, \phi=\pi/4$ | $SO(4)$ double plane rotation, $\det(R) = +1$, metric isometry. | $\epsilon_M < 10^{-12}$, $\epsilon_P < 10^{-10}$ |
| **CASE_D** | Anisotropic Scaling | $p = (2, -4, 1, 8), S = (2, 0.5, 4, 0.25)$ | Diagonal transformation with volume factor $\det(S) = 1.0$. | $\epsilon_M < 10^{-12}$, $\epsilon_P < 10^{-10}$ |
| **CASE_E** | Parity Reflection | $p = (3, -2, 5, 1), x_2 \to -x_2$ | Involutory orientation-reversing map $T^2 = I$, $\det(J) = -1$. | $\epsilon_M < 10^{-12}$, $\epsilon_P < 10^{-10}$ |
| **CASE_F** | Singular Transformation | $p = (1, 2, 3, 4), x_4 \to 0$ | Rank collapse ($\text{rank}(J) = 3 < 4$), non-invertibility. | $\text{rank}=3$, non-invertible flagged |
| **CASE_G** | Nonlinear Diffeomorphism | $p = (0.5, -0.8, 1.2, -0.3), x_i \to \sinh(x_i)$ | Smooth bijection with analytical inverse $x_i = \text{asinh}(y_i)$. | $\epsilon_M < 10^{-12}$, $\epsilon_P < 10^{-10}$ |
| **CASE_H** | Nonlinear Non-Invertible | $p = (-2, 3, -1.5, 4), x_i \to x_i^2$ | Sign erasure on negative coordinates, failure to invert. | Non-invertibility residual $> 0$, flagged |
| **CASE_I** | Closed Trajectory | 32-point circular loop in $(x_1, x_2)$ | Loop boundary closure $\|\gamma(1) - \gamma(0)\| = 0$. | Closure residual $< 10^{-12}$ |
| **CASE_J** | High-Frequency Noise | $p = (1, 1, 1, 1) + \delta_{\text{noise}} (10^{-4})$ | Perturbation stability without trajectory divergence. | $\epsilon_P < 10^{-9}$ |
| **CASE_K** | Discontinuous Jump | $p_1 = (1,1,1,1) \to p_2 = (101,1,1,1)$ | Step jump velocity threshold violation ($\|v\| > 50$). | Velocity anomaly flagged, quarantined |
| **CASE_L** | Contradictory Vectors | $v_1 = (1,0,0,0), v_2 = (-1,0,0,0)$ | Antipodal vectors with inner product $\langle v_1, v_2 \rangle = -1.0$. | Contradiction detected, blocked |
| **CASE_M** | Extreme Values | $p = (10^{12}, 10^{-12}, -10^{12}, -10^{-12})$ | Numeric stability across 24 orders of magnitude. | Relative residual $\epsilon_{\text{rel}} < 10^{-9}$ |
| **CASE_N** | Zero State (Origin) | $p = (0, 0, 0, 0)$ | Origin invariance with null trajectory displacement. | $\epsilon_P = 0.0$ |
| **CASE_O** | Multi-Step Round-Trip | $p = (1, 2, 3, 4)$ through $T_1 \circ T_2 \circ T_2^{-1} \circ T_1^{-1}$ | Composition invertibility $(T_1 \circ T_2)^{-1} = T_2^{-1} \circ T_1^{-1}$. | $\epsilon_M < 10^{-12}$, $\epsilon_P < 10^{-10}$ |

---

## 2. Core Unit Tests

1. `test_point_creation_and_distance`: Coordinate retrieval and Euclidean distance calculation.
2. `test_chart_domain_and_patch`: Domain predicate validation, chart transition, and transition Jacobians.
3. `test_matrix_operations`: 4x4 determinant, adjugate inverse, rank, and singular matrix handling.
4. `test_tangent_vector_operations`: Contravariant vector addition, scalar multiplication, and directional derivatives.
5. `test_flat_metric`: Vanishing Christoffel symbols ($\Gamma = 0$) and vanishing curvature ($R = 0, K = 0$).
6. `test_conformally_curved_metric`: Non-zero scalar curvature $R(x)$ on conformal Riemannian metrics.
7. `test_flat_parallel_transport`: Zero holonomy error on closed loop transport in flat space.
8. `test_flat_geodesic`: Linear constant-velocity trajectory integration and path length calculation.
9. `test_injective_baseline_projection`: Exact roundtrip $\Pi(F(x)) = x$ with $\epsilon < 10^{-12}$.
10. `test_information_loss_and_collisions`: Strict injectivity across distinct state sets without collisions.

---

## 3. Ablation Benchmark Methodology

- **Control:** Frozen DAXDA Engine Cl(7,0) Adaptive Transport.
- **Experiment:** DAXDA Cl(7,0) + 4D Manifold Adapter.
- **Metrics Measured:**
  1. Mean & maximum reversibility residuals.
  2. Latency per trajectory (ms) and overhead multiplier.
  3. Trajectory observability (differential velocities, Riemannian path length).
  4. Rank collapse detection count.
  5. Cryptographic hash receipt verification.

"""Three-way logistic regression classifier for failure prediction.

Models:
  A — Baseline features only
  B — Geometric features only
  C — Baseline + Geometric combined
  D — Shuffled-geometry negative control (Model A + geometry permuted across cases)

NaN imputation: median imputation + missingness indicator, fitted on training
data only. Identical preprocessing applied to validation and test sets.
No test-set statistics are ever used during preprocessing.
"""

from __future__ import annotations
import math
import random
import json
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Tuple, Optional, Any

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

SEED = 42


def _baseline_feature_vector(baseline_row: Dict[str, float]) -> List[float]:
    """Extract ordered baseline feature vector from one layer's baseline dict."""
    return [
        baseline_row.get("scalar_residual", float("nan")),
        baseline_row.get("grade0_energy", float("nan")),
        baseline_row.get("threshold_distance", float("nan")),
        float(baseline_row.get("scalar_residual_missing", 1)),
        float(baseline_row.get("threshold_distance_missing", 1)),
    ]


def _geometric_feature_vector(geometric_row: Dict[str, float]) -> List[float]:
    """Extract ordered geometric feature vector from one layer's geometric dict."""
    return [
        geometric_row.get("det_J", float("nan")),
        geometric_row.get("rank_J", float("nan")),
        geometric_row.get("kappa_J", float("nan")),
        geometric_row.get("norm_v", float("nan")),
        geometric_row.get("norm_dv", float("nan")),
        geometric_row.get("delta_L", float("nan")),
        geometric_row.get("cumulative_L", float("nan")),
        geometric_row.get("eps_M", float("nan")),
        geometric_row.get("eps_P", float("nan")),
        geometric_row.get("eps_Cl", float("nan")),
        geometric_row.get("sgn_det_J", float("nan")),
        geometric_row.get("delta_rank", float("nan")),
        geometric_row.get("delta_kappa", float("nan")),
        geometric_row.get("delta_v", float("nan")),
        geometric_row.get("delta_eps", float("nan")),
    ]


def build_feature_matrix(
    cases,
    layer_prefix: int,
    model_type: str,
    shuffled_geo_indices: Optional[List[int]] = None,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Build (X, y) arrays for a given layer prefix and model type.

    model_type: "A" (baseline only), "B" (geometric only), "C" (combined),
                "D" (baseline + shuffled geometry — negative control)
    layer_prefix: 1..16; only features from layers 1..layer_prefix are used.
    shuffled_geo_indices: required for model_type="D"; permuted case indices.
    """
    X_rows, y = [], []
    for case_idx, case in enumerate(cases):
        if len(case.baseline_features) < layer_prefix:
            continue

        # Aggregate features across layer prefix (concatenate layer 1..i vectors)
        base_feats = []
        geo_feats = []
        for layer_i in range(layer_prefix):
            base_feats.extend(_baseline_feature_vector(case.baseline_features[layer_i]))
            if model_type in ("B", "C"):
                geo_feats.extend(_geometric_feature_vector(case.geometric_features[layer_i]))
            elif model_type == "D":
                shuffled_idx = shuffled_geo_indices[case_idx] if shuffled_geo_indices else case_idx
                geo_feats.extend(_geometric_feature_vector(
                    cases[shuffled_idx].geometric_features[layer_i]
                ))

        if model_type == "A":
            feats = base_feats
        elif model_type == "B":
            feats = geo_feats
        elif model_type in ("C", "D"):
            feats = base_feats + geo_feats
        else:
            raise ValueError(f"Unknown model_type: {model_type}")

        X_rows.append(feats)
        y.append(case.binary_label)

    return np.array(X_rows, dtype=float), np.array(y, dtype=int)


def make_shuffled_geo_indices(n: int, seed: int = SEED) -> List[int]:
    """Generate a permutation of case indices for the shuffled-geometry control."""
    indices = list(range(n))
    rng = random.Random(seed)
    rng.shuffle(indices)
    return indices


def build_pipeline(C: float = 1.0) -> Pipeline:
    """Build sklearn Pipeline: median imputation → standardization → logistic regression."""
    return Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(C=C, solver="lbfgs", max_iter=2000,
                                   random_state=SEED, class_weight="balanced")),
    ])


@dataclass
class ModelResult:
    model_type: str       # A / B / C / D
    layer_prefix: int
    n_train: int
    n_val: int
    n_test: int
    coefficients: List[float]
    intercept: float
    train_log_loss: float = float("nan")
    val_log_loss: float = float("nan")
    test_log_loss: float = float("nan")
    pipeline_fitted: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class TrioClassifier:
    """Trains and evaluates Models A, B, C, D across all 16 layer prefixes."""

    def __init__(self, C: float = 1.0):
        self.C = C
        self.pipelines: Dict[Tuple[str, int], Pipeline] = {}
        self.shuffled_indices: Optional[List[int]] = None

    def fit(
        self,
        train_cases,
        val_cases=None,
        layer_prefix: int = 16,
        model_types: Tuple[str, ...] = ("A", "B", "C", "D"),
    ) -> Dict[str, Pipeline]:
        """Fit all model types for one layer prefix on training cases."""
        self.shuffled_indices = make_shuffled_geo_indices(len(train_cases))

        fitted = {}
        for mt in model_types:
            X_tr, y_tr = build_feature_matrix(
                train_cases, layer_prefix, mt,
                shuffled_geo_indices=self.shuffled_indices if mt == "D" else None
            )
            if X_tr.shape[0] == 0:
                continue
            pipe = build_pipeline(self.C)
            pipe.fit(X_tr, y_tr)
            self.pipelines[(mt, layer_prefix)] = pipe
            fitted[mt] = pipe
        return fitted

    def predict_proba(
        self, cases, layer_prefix: int, model_type: str,
        shuffled_indices: Optional[List[int]] = None
    ) -> np.ndarray:
        """Return P(failure) for each case using features through layer_prefix."""
        key = (model_type, layer_prefix)
        if key not in self.pipelines:
            raise KeyError(f"No fitted pipeline for ({model_type}, layer {layer_prefix})")

        si = shuffled_indices if model_type == "D" else None
        X, _ = build_feature_matrix(cases, layer_prefix, model_type, shuffled_geo_indices=si)
        return self.pipelines[key].predict_proba(X)[:, 1]

    def get_coefficients(self, model_type: str, layer_prefix: int) -> Tuple[List[float], float]:
        key = (model_type, layer_prefix)
        if key not in self.pipelines:
            return [], float("nan")
        clf = self.pipelines[key].named_steps["clf"]
        return clf.coef_[0].tolist(), float(clf.intercept_[0])

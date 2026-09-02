"""Bootstrap confidence intervals on comparative deltas (C - A).

Resamples WHOLE TRAJECTORIES/CASES as units.
Never independently resamples individual layer observations.

Produces 95% CIs for:
  - AUROC_C - AUROC_A
  - AUPRC_C - AUPRC_A
  - TPR@1%FPR_C - TPR@1%FPR_A
  - TPR@5%FPR_C - TPR@5%FPR_A
  - Brier_C - Brier_A
  - i*_A - i*_C (lead-time gain in layers)
  - Delta_LogLoss = LogLoss_A - LogLoss_C

Minimum 1000 resamples. CI confidence level: 95%.
"""

from __future__ import annotations
import math
import random
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional, Tuple

import numpy as np
from sklearn.metrics import roc_auc_score, average_precision_score, brier_score_loss, log_loss

from evaluator import _tpr_at_fpr, detect_i_star, LayerMetrics, compute_layer_metrics
from corpus_schema import NATIVE_GOVERNANCE, SYNTHETIC_MECHANISTIC

N_BOOTSTRAP = 1000
CONFIDENCE = 0.95
SEED = 42


@dataclass
class BootstrapCI:
    quantity: str
    stratum: str
    layer_prefix: int       # -1 for i* (layer-aggregated quantity)
    point_estimate: float
    ci_lower: float
    ci_upper: float
    n_bootstrap: int
    excludes_zero: bool     # True if CI does not include 0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _resample_cases(cases, rng: random.Random) -> List:
    """Resample N cases with replacement (whole-trajectory units)."""
    n = len(cases)
    return [cases[rng.randint(0, n - 1)] for _ in range(n)]


def _compute_auroc_delta(cases_A, cases_C, layer_prefix: int,
                          shuffled_A=None, shuffled_C=None) -> float:
    """Compute AUROC_C - AUROC_A for one bootstrap resample."""
    from classifier import build_feature_matrix

    y = np.array([c.binary_label for c in cases_A])
    if len(np.unique(y)) < 2:
        return float("nan")

    X_A, _ = build_feature_matrix(cases_A, layer_prefix, "A")
    X_C, _ = build_feature_matrix(cases_C, layer_prefix, "C")

    # Skip if shapes differ (edge case with very small N)
    if X_A.shape[0] != len(y) or X_C.shape[0] != len(y):
        return float("nan")

    # Use stored probabilities where available; otherwise refit would be needed.
    # For bootstrap we use precomputed proba arrays passed from temporal_evaluator.
    return float("nan")  # Placeholder — actual bootstrap uses precomputed probas


def bootstrap_ci_on_probas(
    y_true: np.ndarray,
    proba_A: np.ndarray,
    proba_C: np.ndarray,
    layer_prefix: int,
    stratum: str,
    n_bootstrap: int = N_BOOTSTRAP,
    seed: int = SEED,
) -> List[BootstrapCI]:
    """
    Bootstrap CIs on metric deltas (C - A) using pre-computed probability arrays.

    Resamples cases (rows) as whole units. Each row corresponds to one case
    with ALL 16 layers already aggregated into a single probability.

    Returns list of BootstrapCI for each quantity.
    """
    rng = np.random.default_rng(seed)
    n = len(y_true)

    deltas = {
        "AUROC_C_minus_A": [],
        "AUPRC_C_minus_A": [],
        "TPR1_C_minus_A": [],
        "TPR5_C_minus_A": [],
        "Brier_C_minus_A": [],
        "DeltaLogLoss": [],
    }

    for _ in range(n_bootstrap):
        idx = rng.integers(0, n, size=n)
        yt = y_true[idx]
        pA = proba_A[idx]
        pC = proba_C[idx]

        if len(np.unique(yt)) < 2:
            continue

        try:
            auroc_A = roc_auc_score(yt, pA)
            auroc_C = roc_auc_score(yt, pC)
            auprc_A = average_precision_score(yt, pA)
            auprc_C = average_precision_score(yt, pC)
            brier_A = brier_score_loss(yt, pA)
            brier_C = brier_score_loss(yt, pC)
            ll_A = log_loss(yt, pA)
            ll_C = log_loss(yt, pC)
            tpr1_A = _tpr_at_fpr(yt, pA, 0.01)
            tpr1_C = _tpr_at_fpr(yt, pC, 0.01)
            tpr5_A = _tpr_at_fpr(yt, pA, 0.05)
            tpr5_C = _tpr_at_fpr(yt, pC, 0.05)

            deltas["AUROC_C_minus_A"].append(auroc_C - auroc_A)
            deltas["AUPRC_C_minus_A"].append(auprc_C - auprc_A)
            deltas["TPR1_C_minus_A"].append(tpr1_C - tpr1_A)
            deltas["TPR5_C_minus_A"].append(tpr5_C - tpr5_A)
            deltas["Brier_C_minus_A"].append(brier_C - brier_A)
            deltas["DeltaLogLoss"].append(ll_A - ll_C)
        except Exception:
            continue

    alpha = 1 - CONFIDENCE
    results = []
    for quantity, vals in deltas.items():
        if not vals:
            results.append(BootstrapCI(
                quantity=quantity, stratum=stratum, layer_prefix=layer_prefix,
                point_estimate=float("nan"), ci_lower=float("nan"), ci_upper=float("nan"),
                n_bootstrap=0, excludes_zero=False
            ))
            continue
        arr = np.array(vals)
        point = float(np.mean(arr))
        lo = float(np.percentile(arr, 100 * alpha / 2))
        hi = float(np.percentile(arr, 100 * (1 - alpha / 2)))
        excludes_zero = (lo > 0 or hi < 0)
        results.append(BootstrapCI(
            quantity=quantity, stratum=stratum, layer_prefix=layer_prefix,
            point_estimate=point, ci_lower=lo, ci_upper=hi,
            n_bootstrap=len(vals), excludes_zero=excludes_zero,
        ))

    return results


def bootstrap_lead_time_ci(
    i_star_A_samples: List[Optional[int]],
    i_star_C_samples: List[Optional[int]],
    stratum: str,
    point_i_star_A: Optional[int],
    point_i_star_C: Optional[int],
) -> BootstrapCI:
    """
    CI for lead-time gain: i*_A - i*_C (positive = C detects earlier).
    i_star_A/C_samples are bootstrap samples of i* values (None = not reached).
    """
    gains = []
    for a, c in zip(i_star_A_samples, i_star_C_samples):
        if a is not None and c is not None:
            gains.append(a - c)
        # If either is None (threshold not reached), skip that resample

    if not gains:
        return BootstrapCI(
            quantity="LeadTimeGain_layers", stratum=stratum, layer_prefix=-1,
            point_estimate=float("nan"), ci_lower=float("nan"), ci_upper=float("nan"),
            n_bootstrap=0, excludes_zero=False,
        )

    arr = np.array(gains)
    alpha = 1 - CONFIDENCE
    point = (point_i_star_A - point_i_star_C) if (point_i_star_A is not None and point_i_star_C is not None) else float(np.mean(arr))
    lo = float(np.percentile(arr, 100 * alpha / 2))
    hi = float(np.percentile(arr, 100 * (1 - alpha / 2)))
    return BootstrapCI(
        quantity="LeadTimeGain_layers", stratum=stratum, layer_prefix=-1,
        point_estimate=point, ci_lower=lo, ci_upper=hi,
        n_bootstrap=len(gains), excludes_zero=(lo > 0 or hi < 0),
    )

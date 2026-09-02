"""Evaluation metrics for failure prediction.

Computes all pre-registered metrics at each layer prefix for each model.
Reports separately for ALL / NATIVE_GOVERNANCE / SYNTHETIC_MECHANISTIC.

Metrics:
  1. AUROC
  2. AUPRC
  3. TPR @ FPR = 1%
  4. TPR @ FPR = 5%
  5. Brier Score
  6. Expected Calibration Error (ECE)
  7. Precision / Recall / Specificity / F1
  8. Confusion Matrix (TP, FP, TN, FN)
  9. Confidence distribution (mean, std, quantiles)
  10. Log-Loss (for incremental information-value test)
  11. Delta Log-Loss (LogLoss_A - LogLoss_C at each layer)
"""

from __future__ import annotations
import math
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional, Tuple

import numpy as np
from sklearn.metrics import (
    roc_auc_score, average_precision_score,
    roc_curve, precision_recall_curve,
    brier_score_loss, log_loss,
    confusion_matrix, precision_score, recall_score, f1_score
)

from corpus_schema import NATIVE_GOVERNANCE, SYNTHETIC_MECHANISTIC

# Pre-registered early-warning horizon thresholds
I_STAR_AUROC_THRESHOLD = 0.75
I_STAR_TPR5_THRESHOLD = 0.60
I_STAR_STABILITY_WINDOW = 3  # must hold for this many consecutive layers


@dataclass
class LayerMetrics:
    model_type: str
    layer_prefix: int
    stratum: str          # "ALL" / "NATIVE_GOVERNANCE" / "SYNTHETIC_MECHANISTIC"
    n_cases: int
    n_failure: int
    n_safe: int

    auroc: float
    auprc: float
    tpr_at_1pct_fpr: float
    tpr_at_5pct_fpr: float
    brier_score: float
    ece: float
    log_loss_val: float
    precision: float
    recall: float
    specificity: float
    f1: float

    # Confusion matrix
    tp: int
    fp: int
    tn: int
    fn: int

    # Confidence distribution
    mean_prob: float
    std_prob: float
    p10_prob: float
    p50_prob: float
    p90_prob: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class DeltaMetrics:
    """Incremental comparison: Model C minus Model A."""
    layer_prefix: int
    stratum: str
    delta_auroc: float          # AUROC_C - AUROC_A
    delta_auprc: float          # AUPRC_C - AUPRC_A
    delta_tpr1: float           # TPR@1%FPR_C - TPR@1%FPR_A
    delta_tpr5: float           # TPR@5%FPR_C - TPR@5%FPR_A
    delta_brier: float          # Brier_C - Brier_A (negative = improvement)
    delta_log_loss: float       # LogLoss_A - LogLoss_C (positive = C better)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _tpr_at_fpr(y_true: np.ndarray, y_score: np.ndarray, target_fpr: float) -> float:
    """Return TPR at the operating point closest to target_fpr."""
    if len(np.unique(y_true)) < 2:
        return float("nan")
    fprs, tprs, _ = roc_curve(y_true, y_score)
    # Find threshold where FPR <= target_fpr (take highest TPR)
    valid = fprs <= target_fpr
    if not np.any(valid):
        return 0.0
    return float(np.max(tprs[valid]))


def _ece(y_true: np.ndarray, y_prob: np.ndarray, n_bins: int = 10) -> float:
    """Expected Calibration Error via equal-width binning."""
    bins = np.linspace(0, 1, n_bins + 1)
    ece = 0.0
    n = len(y_true)
    for i in range(n_bins):
        mask = (y_prob >= bins[i]) & (y_prob < bins[i + 1])
        if mask.sum() == 0:
            continue
        bin_acc = y_true[mask].mean()
        bin_conf = y_prob[mask].mean()
        ece += (mask.sum() / n) * abs(bin_acc - bin_conf)
    return float(ece)


def _optimal_threshold(y_true: np.ndarray, y_prob: np.ndarray) -> float:
    """Select threshold maximizing F1 on the provided set (validation use only)."""
    best_f1, best_t = 0.0, 0.5
    for t in np.linspace(0.1, 0.9, 81):
        pred = (y_prob >= t).astype(int)
        if pred.sum() == 0:
            continue
        f = f1_score(y_true, pred, zero_division=0)
        if f > best_f1:
            best_f1, best_t = f, t
    return best_t


def compute_layer_metrics(
    model_type: str,
    layer_prefix: int,
    stratum: str,
    y_true: np.ndarray,
    y_prob: np.ndarray,
    threshold: float = 0.5,
) -> LayerMetrics:
    """Compute all metrics for one (model, layer, stratum) combination."""
    n = len(y_true)
    n_fail = int(y_true.sum())
    n_safe = n - n_fail

    if n < 2 or len(np.unique(y_true)) < 2:
        nan = float("nan")
        return LayerMetrics(
            model_type=model_type, layer_prefix=layer_prefix, stratum=stratum,
            n_cases=n, n_failure=n_fail, n_safe=n_safe,
            auroc=nan, auprc=nan, tpr_at_1pct_fpr=nan, tpr_at_5pct_fpr=nan,
            brier_score=nan, ece=nan, log_loss_val=nan,
            precision=nan, recall=nan, specificity=nan, f1=nan,
            tp=0, fp=0, tn=0, fn=0,
            mean_prob=float(np.mean(y_prob)), std_prob=float(np.std(y_prob)),
            p10_prob=float(np.percentile(y_prob, 10)),
            p50_prob=float(np.percentile(y_prob, 50)),
            p90_prob=float(np.percentile(y_prob, 90)),
        )

    auroc = float(roc_auc_score(y_true, y_prob))
    auprc = float(average_precision_score(y_true, y_prob))
    tpr1 = _tpr_at_fpr(y_true, y_prob, 0.01)
    tpr5 = _tpr_at_fpr(y_true, y_prob, 0.05)
    brier = float(brier_score_loss(y_true, y_prob))
    ece = _ece(y_true, y_prob)
    ll = float(log_loss(y_true, y_prob))

    pred = (y_prob >= threshold).astype(int)
    prec = float(precision_score(y_true, pred, zero_division=0))
    rec = float(recall_score(y_true, pred, zero_division=0))
    f1 = float(f1_score(y_true, pred, zero_division=0))

    cm = confusion_matrix(y_true, pred, labels=[0, 1])
    tn, fp, fn, tp = cm.ravel() if cm.shape == (2, 2) else (0, 0, 0, 0)
    spec = tn / (tn + fp) if (tn + fp) > 0 else float("nan")

    return LayerMetrics(
        model_type=model_type, layer_prefix=layer_prefix, stratum=stratum,
        n_cases=n, n_failure=n_fail, n_safe=n_safe,
        auroc=auroc, auprc=auprc,
        tpr_at_1pct_fpr=tpr1, tpr_at_5pct_fpr=tpr5,
        brier_score=brier, ece=ece, log_loss_val=ll,
        precision=prec, recall=rec, specificity=float(spec), f1=f1,
        tp=int(tp), fp=int(fp), tn=int(tn), fn=int(fn),
        mean_prob=float(np.mean(y_prob)), std_prob=float(np.std(y_prob)),
        p10_prob=float(np.percentile(y_prob, 10)),
        p50_prob=float(np.percentile(y_prob, 50)),
        p90_prob=float(np.percentile(y_prob, 90)),
    )


def detect_i_star(
    layer_metrics: List[LayerMetrics],
    model_type: str,
    stratum: str,
    auroc_threshold: float = I_STAR_AUROC_THRESHOLD,
    tpr5_threshold: float = I_STAR_TPR5_THRESHOLD,
    stability_window: int = I_STAR_STABILITY_WINDOW,
) -> Optional[int]:
    """
    Detect operational early-warning horizon i* (pre-registered definition).

    i* = earliest layer where:
        AUROC >= auroc_threshold AND TPR@5%FPR >= tpr5_threshold
        holds for stability_window consecutive layers.

    Returns None if threshold is never reached.
    """
    relevant = [m for m in layer_metrics
                if m.model_type == model_type and m.stratum == stratum]
    relevant.sort(key=lambda m: m.layer_prefix)

    streak = 0
    first_qualifying = None
    for m in relevant:
        qualifies = (
            not math.isnan(m.auroc) and m.auroc >= auroc_threshold and
            not math.isnan(m.tpr_at_5pct_fpr) and m.tpr_at_5pct_fpr >= tpr5_threshold
        )
        if qualifies:
            streak += 1
            if first_qualifying is None:
                first_qualifying = m.layer_prefix
        else:
            streak = 0
            first_qualifying = None

        if streak >= stability_window:
            return first_qualifying

    return None


def compute_delta_metrics(
    metrics_A: LayerMetrics,
    metrics_C: LayerMetrics,
) -> DeltaMetrics:
    """Compute C - A incremental deltas at one (layer, stratum) combination."""
    def _diff(a, c):
        if math.isnan(a) or math.isnan(c):
            return float("nan")
        return c - a

    return DeltaMetrics(
        layer_prefix=metrics_C.layer_prefix,
        stratum=metrics_C.stratum,
        delta_auroc=_diff(metrics_A.auroc, metrics_C.auroc),
        delta_auprc=_diff(metrics_A.auprc, metrics_C.auprc),
        delta_tpr1=_diff(metrics_A.tpr_at_1pct_fpr, metrics_C.tpr_at_1pct_fpr),
        delta_tpr5=_diff(metrics_A.tpr_at_5pct_fpr, metrics_C.tpr_at_5pct_fpr),
        delta_brier=_diff(metrics_A.brier_score, metrics_C.brier_score),
        # Positive delta_log_loss means C has lower log loss (better)
        delta_log_loss=(metrics_A.log_loss_val - metrics_C.log_loss_val)
        if not (math.isnan(metrics_A.log_loss_val) or math.isnan(metrics_C.log_loss_val))
        else float("nan"),
    )

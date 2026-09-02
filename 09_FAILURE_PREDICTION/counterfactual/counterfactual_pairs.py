"""Counterfactual pair analysis.

Creates trajectory pairs sharing initial state x0 but diverging terminal outcomes.
Tests whether Models A, B, C begin separating predicted failure probabilities
at different layers — revealing whether geometry tracks failure ONSET (process)
not merely final-state class membership (outcome label).

Pair Types:
  Type A: stable rank/velocity -> PASS  vs  same x0 -> progressive degradation -> BLOCK
  Type B: near-boundary clean -> QUARANTINE  vs  same x0 -> increasing kappa -> BLOCK
"""

from __future__ import annotations
import os
import sys
import math
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional, Tuple

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
_FP = os.path.join(_ROOT, "09_FAILURE_PREDICTION")
_FROZEN = os.path.join(_ROOT, "03_V9_V8_Validation_Suite", "DAXDA_V9_MASTER", "daxda-v11.4-frozen")
_M4 = os.path.join(_ROOT, "08_4D_MANIFOLD")
for p in [_ROOT, _FP, _FROZEN, _M4,
          os.path.join(_FP, "corpus"),
          os.path.join(_FP, "features"),
          os.path.join(_FP, "model")]:
    if p not in sys.path:
        sys.path.insert(0, p)

from corpus_schema import CorpusCase, PASS, QUARANTINE, BLOCK, NATIVE_GOVERNANCE, SYNTHETIC_MECHANISTIC
from feature_extractor import FeatureExtractor

import numpy as np


@dataclass
class CounterfactualPair:
    pair_id: str
    pair_type: str               # "TypeA" or "TypeB"
    shared_x0: Tuple[float, float, float, float]
    case_safe_id: str            # case with PASS outcome
    case_fail_id: str            # case with BLOCK/QUARANTINE outcome
    disposition_safe: str
    disposition_fail: str

    # For each layer i, probability of failure for SAFE case and FAIL case per model
    separation_layer_A: Optional[int]  # earliest layer Model A begins separating
    separation_layer_B: Optional[int]
    separation_layer_C: Optional[int]

    layer_proba_safe_A: List[float]   # 16 probabilities for the safe trajectory
    layer_proba_fail_A: List[float]
    layer_proba_safe_B: List[float]
    layer_proba_fail_B: List[float]
    layer_proba_safe_C: List[float]
    layer_proba_fail_C: List[float]

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["shared_x0"] = list(d["shared_x0"])
        return d


def _separation_layer(proba_safe: List[float], proba_fail: List[float],
                      threshold: float = 0.10) -> Optional[int]:
    """
    Find earliest layer where |P(fail|fail_traj) - P(fail|safe_traj)| >= threshold.
    Returns 1-indexed layer or None.
    """
    for i, (ps, pf) in enumerate(zip(proba_safe, proba_fail)):
        if abs(pf - ps) >= threshold:
            return i + 1
    return None


class CounterfactualAnalyzer:
    """Builds and evaluates counterfactual pairs."""

    def __init__(self, classifier_A, classifier_B, classifier_C):
        self.clf_A = classifier_A
        self.clf_B = classifier_B
        self.clf_C = classifier_C
        self.extractor = FeatureExtractor()

    def _build_case(self, x1: float, x2: float, x3: float, x4: float,
                    case_id: str, expected_disposition: str,
                    stratum: str, family: str, seed: Optional[int]) -> CorpusCase:
        """Build a CorpusCase and populate its features."""
        baseline_rows, geometric_rows, observed, residual = self.extractor.extract(x1, x2, x3, x4)
        inp_hash = CorpusCase.make_input_hash(x1, x2, x3, x4)
        binary = 0 if observed == PASS else 1
        case = CorpusCase(
            case_id=case_id,
            stratum=stratum,
            failure_family=family,
            ground_truth_terminal_disposition=observed,
            binary_label=binary,
            source_type="COUNTERFACTUAL_PAIR",
            synthetic_or_native="synthetic",
            seed=seed,
            expected_behavior=f"Counterfactual pair; expected {expected_disposition}",
            input_x1=x1, input_x2=x2, input_x3=x3, input_x4=x4,
            input_hash=inp_hash,
        )
        case.baseline_features = baseline_rows
        case.geometric_features = geometric_rows
        case.observed_terminal_disposition = observed
        return case

    def _layer_probas(self, case: CorpusCase, model_type: str) -> List[float]:
        """Get per-layer failure probability for a single case."""
        from classifier import build_feature_matrix
        probas = []
        for i in range(1, 17):
            try:
                X, _ = build_feature_matrix([case], i, model_type)
                if model_type == "A":
                    pipe = self.clf_A.pipelines.get(("A", i))
                elif model_type == "B":
                    pipe = self.clf_B.pipelines.get(("B", i))
                else:
                    pipe = self.clf_C.pipelines.get(("C", i))

                if pipe is None or X.shape[0] == 0:
                    probas.append(float("nan"))
                else:
                    probas.append(float(pipe.predict_proba(X)[0, 1]))
            except Exception:
                probas.append(float("nan"))
        return probas

    def build_type_a_pairs(self, n_pairs: int = 20) -> List[CounterfactualPair]:
        """
        Type A: stable -> PASS vs same x0, degraded -> BLOCK.
        Stable: small magnitude. Degraded: large magnitude (same direction).
        """
        pairs = []
        import random
        rng = random.Random(999)

        for i in range(n_pairs):
            x0 = [rng.gauss(0, 0.3) for _ in range(4)]
            scale = rng.uniform(8.0, 12.0)
            x1_fail = [x * scale for x in x0]

            case_safe = self._build_case(*x0, f"CF-A-SAFE-{i:04d}", PASS,
                                         SYNTHETIC_MECHANISTIC, "COUNTERFACTUAL_TYPE_A_SAFE", i)
            case_fail = self._build_case(*x1_fail, f"CF-A-FAIL-{i:04d}", BLOCK,
                                         SYNTHETIC_MECHANISTIC, "COUNTERFACTUAL_TYPE_A_FAIL", i)

            p_safe_A = self._layer_probas(case_safe, "A")
            p_fail_A = self._layer_probas(case_fail, "A")
            p_safe_B = self._layer_probas(case_safe, "B")
            p_fail_B = self._layer_probas(case_fail, "B")
            p_safe_C = self._layer_probas(case_safe, "C")
            p_fail_C = self._layer_probas(case_fail, "C")

            pair = CounterfactualPair(
                pair_id=f"CF-TypeA-{i:04d}",
                pair_type="TypeA",
                shared_x0=tuple(x0),
                case_safe_id=case_safe.case_id,
                case_fail_id=case_fail.case_id,
                disposition_safe=case_safe.ground_truth_terminal_disposition,
                disposition_fail=case_fail.ground_truth_terminal_disposition,
                separation_layer_A=_separation_layer(p_safe_A, p_fail_A),
                separation_layer_B=_separation_layer(p_safe_B, p_fail_B),
                separation_layer_C=_separation_layer(p_safe_C, p_fail_C),
                layer_proba_safe_A=p_safe_A,
                layer_proba_fail_A=p_fail_A,
                layer_proba_safe_B=p_safe_B,
                layer_proba_fail_B=p_fail_B,
                layer_proba_safe_C=p_safe_C,
                layer_proba_fail_C=p_fail_C,
            )
            pairs.append(pair)

        return pairs

    def build_type_b_pairs(self, n_pairs: int = 20) -> List[CounterfactualPair]:
        """
        Type B: near-boundary clean -> QUARANTINE/PASS  vs  same x0 with kappa-increasing
        perturbation -> BLOCK.
        """
        pairs = []
        import random
        rng = random.Random(1001)

        for i in range(n_pairs):
            mag = rng.uniform(3.5, 4.5)
            x0 = [rng.gauss(0, mag / 3) for _ in range(4)]
            # Fail case: amplify one component strongly
            x1_fail = list(x0)
            x1_fail[0] *= rng.uniform(3.0, 5.0)

            case_safe = self._build_case(*x0, f"CF-B-SAFE-{i:04d}", QUARANTINE,
                                         SYNTHETIC_MECHANISTIC, "COUNTERFACTUAL_TYPE_B_SAFE", i)
            case_fail = self._build_case(*x1_fail, f"CF-B-FAIL-{i:04d}", BLOCK,
                                         SYNTHETIC_MECHANISTIC, "COUNTERFACTUAL_TYPE_B_FAIL", i)

            p_safe_A = self._layer_probas(case_safe, "A")
            p_fail_A = self._layer_probas(case_fail, "A")
            p_safe_B = self._layer_probas(case_safe, "B")
            p_fail_B = self._layer_probas(case_fail, "B")
            p_safe_C = self._layer_probas(case_safe, "C")
            p_fail_C = self._layer_probas(case_fail, "C")

            pair = CounterfactualPair(
                pair_id=f"CF-TypeB-{i:04d}",
                pair_type="TypeB",
                shared_x0=tuple(x0),
                case_safe_id=case_safe.case_id,
                case_fail_id=case_fail.case_id,
                disposition_safe=case_safe.ground_truth_terminal_disposition,
                disposition_fail=case_fail.ground_truth_terminal_disposition,
                separation_layer_A=_separation_layer(p_safe_A, p_fail_A),
                separation_layer_B=_separation_layer(p_safe_B, p_fail_B),
                separation_layer_C=_separation_layer(p_safe_C, p_fail_C),
                layer_proba_safe_A=p_safe_A,
                layer_proba_fail_A=p_fail_A,
                layer_proba_safe_B=p_safe_B,
                layer_proba_fail_B=p_fail_B,
                layer_proba_safe_C=p_safe_C,
                layer_proba_fail_C=p_fail_C,
            )
            pairs.append(pair)

        return pairs

    def summarize(self, pairs: List[CounterfactualPair]) -> Dict[str, Any]:
        """Summarize separation layer statistics across all pairs."""
        def _avg(vals):
            valid = [v for v in vals if v is not None]
            return sum(valid) / len(valid) if valid else None

        sep_A = [p.separation_layer_A for p in pairs]
        sep_B = [p.separation_layer_B for p in pairs]
        sep_C = [p.separation_layer_C for p in pairs]

        return {
            "n_pairs": len(pairs),
            "mean_separation_layer_A": _avg(sep_A),
            "mean_separation_layer_B": _avg(sep_B),
            "mean_separation_layer_C": _avg(sep_C),
            "n_separated_A": sum(1 for v in sep_A if v is not None),
            "n_separated_B": sum(1 for v in sep_B if v is not None),
            "n_separated_C": sum(1 for v in sep_C if v is not None),
            "lead_over_A_by_C": _avg(
                [(a - c) for a, c in zip(sep_A, sep_C) if a is not None and c is not None]
            ),
        }

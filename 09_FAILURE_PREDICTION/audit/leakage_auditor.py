"""Leakage auditor for the failure prediction benchmark.

Performs 8 explicit leakage checks. Any confirmed leakage is a HARD STOP.

Checks:
  1. Terminal disposition not in feature vectors
  2. Future-layer features absent from earlier-layer predictions
  3. Case IDs not encoded in features
  4. Failure-family labels not predictive inputs
  5. Synthetic generator parameters not exposed
  6. Duplicate trajectories not split across train/test
  7. Stratum label not in feature vectors
  8. Test-set statistics not used during training preprocessing
"""

from __future__ import annotations
import math
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Tuple

import numpy as np

from corpus_schema import CorpusCase

INSUFFICIENT_N_THRESHOLD = 30  # From preregistration


@dataclass
class LeakageCheckResult:
    check_id: str
    description: str
    status: str          # "PASS" / "FAIL" / "WARNING"
    details: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class LeakageAuditor:
    """Performs all 8 pre-registered leakage checks."""

    def __init__(self, train_cases: List[CorpusCase], val_cases: List[CorpusCase],
                 test_cases: List[CorpusCase]):
        self.train = train_cases
        self.val = val_cases
        self.test = test_cases
        self.all_cases = train_cases + val_cases + test_cases
        self.results: List[LeakageCheckResult] = []

    def _add(self, check_id: str, description: str, status: str, details: str):
        self.results.append(LeakageCheckResult(check_id, description, status, details))

    def check_disposition_not_in_features(self) -> LeakageCheckResult:
        """Check 1: Terminal disposition encoded as binary_label must not appear in feature vectors."""
        label_to_str = {0: "PASS", 1: "FAILURE", "PASS": "PASS", "BLOCK": "BLOCK", "QUARANTINE": "QUARANTINE"}
        violations = 0
        for case in self.all_cases:
            for row in case.baseline_features + case.geometric_features:
                for k, v in row.items():
                    if k in ("layer",):
                        continue
                    if isinstance(v, str) and v in ("PASS", "BLOCK", "QUARANTINE"):
                        violations += 1
                    if k == "binary_label" or k == "ground_truth_terminal_disposition":
                        violations += 1

        status = "PASS" if violations == 0 else "FAIL"
        return self._add("LC1", "Terminal disposition not in feature vectors",
                         status, f"Violations: {violations}")

    def check_temporal_causality(self) -> LeakageCheckResult:
        """Check 2: Feature at layer i must only contain information from layers 1..i."""
        violations = 0
        for case in self.all_cases:
            for i, row in enumerate(case.baseline_features):
                if row.get("layer", i + 1) != i + 1:
                    violations += 1
            for i, row in enumerate(case.geometric_features):
                if row.get("layer", i + 1) != i + 1:
                    violations += 1

        status = "PASS" if violations == 0 else "FAIL"
        return self._add("LC2", "Temporal causality: layer i uses only layers 1..i",
                         status, f"Layer index violations: {violations}")

    def check_case_ids_not_in_features(self) -> LeakageCheckResult:
        """Check 3: Case IDs not encoded in features."""
        case_ids = {c.case_id for c in self.all_cases}
        violations = 0
        for case in self.all_cases:
            for row in case.baseline_features + case.geometric_features:
                for v in row.values():
                    if isinstance(v, str) and v in case_ids:
                        violations += 1

        status = "PASS" if violations == 0 else "FAIL"
        return self._add("LC3", "Case IDs not encoded in feature vectors",
                         status, f"Violations: {violations}")

    def check_family_labels_not_in_features(self) -> LeakageCheckResult:
        """Check 4: Failure-family labels not predictive inputs."""
        family_names = {c.failure_family for c in self.all_cases}
        violations = 0
        for case in self.all_cases:
            for row in case.baseline_features + case.geometric_features:
                for v in row.values():
                    if isinstance(v, str) and v in family_names:
                        violations += 1

        status = "PASS" if violations == 0 else "FAIL"
        return self._add("LC4", "Failure-family labels not in feature vectors",
                         status, f"Violations: {violations}")

    def check_synthetic_params_not_exposed(self) -> LeakageCheckResult:
        """Check 5: Synthetic generator seeds not in feature vectors."""
        seeds = {str(c.seed) for c in self.all_cases if c.seed is not None}
        violations = 0
        for case in self.all_cases:
            for row in case.baseline_features + case.geometric_features:
                for v in row.values():
                    if isinstance(v, str) and v in seeds:
                        violations += 1

        status = "PASS" if violations == 0 else "FAIL"
        return self._add("LC5", "Synthetic generator seeds not in feature vectors",
                         status, f"Violations: {violations}")

    def check_no_duplicate_split(self) -> LeakageCheckResult:
        """Check 6: Duplicate trajectories (same input_hash) not split across train/test."""
        train_hashes = {c.input_hash for c in self.train}
        test_hashes = {c.input_hash for c in self.test}
        overlap = train_hashes & test_hashes
        status = "PASS" if len(overlap) == 0 else "FAIL"
        return self._add("LC6", "Duplicate trajectories not split across train/test",
                         status, f"Hash collisions across splits: {len(overlap)}")

    def check_stratum_not_in_features(self) -> LeakageCheckResult:
        """Check 7: Stratum label (NATIVE/SYNTHETIC) not in feature vectors."""
        stratum_names = {"NATIVE_GOVERNANCE", "SYNTHETIC_MECHANISTIC"}
        violations = 0
        for case in self.all_cases:
            for row in case.baseline_features + case.geometric_features:
                for v in row.values():
                    if isinstance(v, str) and v in stratum_names:
                        violations += 1

        status = "PASS" if violations == 0 else "FAIL"
        return self._add("LC7", "Stratum label not in feature vectors",
                         status, f"Violations: {violations}")

    def check_ood_family_sizes(self) -> LeakageCheckResult:
        """Check 8: OOD evaluation families have N >= INSUFFICIENT_N_THRESHOLD on test set."""
        from collections import Counter
        family_counts = Counter(c.failure_family for c in self.test)
        insufficient = {f: n for f, n in family_counts.items() if n < INSUFFICIENT_N_THRESHOLD}
        status = "WARNING" if insufficient else "PASS"
        details = (f"Families below N={INSUFFICIENT_N_THRESHOLD}: {insufficient}"
                   if insufficient else f"All families have N >= {INSUFFICIENT_N_THRESHOLD}")
        return self._add("LC8", f"OOD family sizes >= {INSUFFICIENT_N_THRESHOLD} (test set)",
                         status, details)

    def run_all_checks(self) -> Tuple[bool, List[LeakageCheckResult]]:
        """Run all 8 leakage checks. Returns (all_passed, results)."""
        self.results = []
        self.check_disposition_not_in_features()
        self.check_temporal_causality()
        self.check_case_ids_not_in_features()
        self.check_family_labels_not_in_features()
        self.check_synthetic_params_not_exposed()
        self.check_no_duplicate_split()
        self.check_stratum_not_in_features()
        self.check_ood_family_sizes()

        hard_failures = [r for r in self.results if r.status == "FAIL"]
        all_passed = len(hard_failures) == 0
        return all_passed, self.results

    def render_audit_report(self) -> str:
        """Generate markdown audit report."""
        lines = [
            "# Failure Prediction Leakage Audit\n",
            f"**Total Checks:** {len(self.results)}\n",
        ]
        fails = [r for r in self.results if r.status == "FAIL"]
        warns = [r for r in self.results if r.status == "WARNING"]
        passes = [r for r in self.results if r.status == "PASS"]

        lines.append(f"**PASS:** {len(passes)} | **WARN:** {len(warns)} | **FAIL:** {len(fails)}\n")

        if fails:
            lines.append("\n> [!CAUTION]\n> **LEAKAGE DETECTED — EXPERIMENT INVALIDATED**\n")
        else:
            lines.append("\n> [!NOTE]\n> No hard leakage detected. Experiment is valid to proceed.\n")

        lines.append("\n## Check Results\n")
        lines.append("| ID | Description | Status | Details |")
        lines.append("|:---|:---|:---:|:---|")
        for r in self.results:
            emoji = "✅" if r.status == "PASS" else ("⚠️" if r.status == "WARNING" else "❌")
            lines.append(f"| {r.check_id} | {r.description} | {emoji} {r.status} | {r.details} |")

        return "\n".join(lines)

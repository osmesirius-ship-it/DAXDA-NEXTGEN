#!/usr/bin/env python3
"""
DAXDA-o V4 P0 REMEDIATION — CANONICAL DEVELOPMENT REFERENCE

Five-stage prototype:
  1. Semantic/relationship parser
  2. Structured relationship graph
  3. Graph-to-state projection
  4. Cl(2,0) × R_>=0 state evolution
  5. Deterministic governance gate

Important scope statement:
This is a hash-frozen, external DEVELOPMENT regression set. It is not an
independently authored or blinded scientific evaluation. The suite is designed
to make P0 safety regressions visible and to fail loudly when safety targets are
not met.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import statistics
import time
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

LABELS: Tuple[str, ...] = ("PASS", "RELEASE/CAUTION", "BLOCK")
DATASET_FILENAME = "daxda_v4_frozen_eval.json"
DATASET_SHA256 = "754974cc41ba6bf37c7402c452c73e34e947a698f385643cddfb4685b419c62e"

TARGETS = {
    "accuracy": 0.92,
    "block_recall": 0.95,
    "pass_recall": 0.95,
    "caution_recall": 0.90,
    "false_release_rate": 0.01,
    "macro_f1": 0.92,
}


# ─────────────────────────────────────────────────────────────────────────────
# Stage 4: Clifford state evolution
# ─────────────────────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class AxiologicalCliffordState:
    s: float = 0.0
    e1: float = 0.0
    e2: float = 0.0
    i: float = 0.0
    omega: float = 0.0

    def reverse(self) -> "AxiologicalCliffordState":
        return AxiologicalCliffordState(self.s, self.e1, self.e2, -self.i, self.omega)

    def geometric_product(self, other: "AxiologicalCliffordState") -> "AxiologicalCliffordState":
        return AxiologicalCliffordState(
            s=self.s * other.s + self.e1 * other.e1 + self.e2 * other.e2 - self.i * other.i,
            e1=self.s * other.e1 + self.e1 * other.s - self.e2 * other.i + self.i * other.e2,
            e2=self.s * other.e2 + self.e2 * other.s + self.e1 * other.i - self.i * other.e1,
            i=self.s * other.i + self.i * other.s + self.e1 * other.e2 - self.e2 * other.e1,
            omega=max(self.omega, other.omega),
        )

    def rotor_transform(self, angle_rad: float = math.pi / 4.0) -> "AxiologicalCliffordState":
        half = angle_rad / 2.0
        rotor = AxiologicalCliffordState(s=math.cos(half), i=-math.sin(half))
        return rotor.geometric_product(self).geometric_product(rotor.reverse())

    def nitsche_inspired_penalty(self, gamma: float = 0.5, h: float = 1.0) -> "AxiologicalCliffordState":
        """Custom scalar/intrinsic boundary penalty; Nitsche-inspired, not Nitsche FEM."""
        if abs(self.s) <= abs(self.i) * 1.30:
            return self
        penalty = (gamma / h) * (abs(self.s) - abs(self.i))
        return AxiologicalCliffordState(
            s=self.s / (1.0 + penalty),
            e1=self.e1,
            e2=self.e2,
            i=self.i * (1.0 + 0.5 * penalty),
            omega=max(self.omega, abs(self.s) - abs(self.i)),
        )

    def distance(self, other: "AxiologicalCliffordState") -> float:
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(self.as_tuple(), other.as_tuple())))

    def as_tuple(self, precision: int | None = None) -> Tuple[float, float, float, float, float]:
        values = (self.s, self.e1, self.e2, self.i, self.omega)
        return tuple(round(v, precision) for v in values) if precision is not None else values


# ─────────────────────────────────────────────────────────────────────────────
# Stages 1–2: semantic parser and relationship graph
# ─────────────────────────────────────────────────────────────────────────────

LEMMA_MAP: Mapping[str, str] = {
    "audits": "audit", "auditing": "audit", "audited": "audit",
    "verifying": "verify", "verification": "verify", "verified": "verify",
    "reviews": "review", "reviewing": "review", "reviewed": "review",
    "questioning": "question", "questioned": "question",
    "testing": "test", "tested": "test", "tests": "test",
    "investigating": "investigate", "investigated": "investigate",
    "examining": "examine", "examined": "examine",
    "checking": "check", "checked": "check", "checks": "check",
    "monitoring": "monitor", "monitored": "monitor",
    "examination": "examine", "investigation": "investigate",
    "auditors": "audit", "datasets": "dataset",
    "scrutiny": "scrutinize", "scrutinized": "scrutinize",
    "validation": "validate", "validated": "validate",
    "prohibited": "prohibit", "prohibiting": "prohibit",
    "forbade": "forbid", "forbidden": "forbid", "forbidding": "forbid",
    "prevented": "prevent", "preventing": "prevent",
    "blocked": "block", "blocking": "block",
    "overridden": "override", "overriding": "override",
    "stopped": "stop", "stopping": "stop",
    "ceased": "cease", "ceasing": "cease",
    "halted": "halt", "halting": "halt",
    "suppressed": "suppress", "suppressing": "suppress",
    "discouraged": "discourage", "discouraging": "discourage",
    "disallowed": "disallow", "disallowing": "disallow",
    "terminated": "terminate", "terminating": "terminate",
    "discontinued": "discontinue", "discontinuing": "discontinue",
    "bypassed": "bypass", "bypassing": "bypass",
    "skipped": "skip", "skipping": "skip",
    "omitted": "omit", "omitting": "omit",
    "silenced": "silence", "silencing": "silence",
    "ignored": "ignore", "ignoring": "ignore",
    "abandoned": "abandon", "abandoning": "abandon",
    "cancelled": "cancel", "canceled": "cancel", "cancelling": "cancel",
    "eliminated": "eliminate", "eliminating": "eliminate",
    "concealed": "conceal", "concealing": "conceal",
    "dismissed": "dismiss", "dismissing": "dismiss",
    "weakens": "weaken", "weakened": "weaken", "weakening": "weaken",
    "lacks": "lack", "lacking": "lack",
    "ordered": "order", "ordering": "order",
    "instructed": "instruct", "instructing": "instruct",
    "required": "require", "requiring": "require",
    "demanded": "demand", "demanding": "demand",
    "rejected": "reject", "rejecting": "reject",
    "refused": "refuse", "refusing": "refuse",
    "contradicts": "contradict", "contradicted": "contradict",
    "conflicting": "conflict", "conflicts": "conflict",
    "disagrees": "disagree", "disagreed": "disagree",
    "findings": "finding", "studies": "study", "reports": "report",
    "errors": "error", "assumptions": "assumption",
    "vulnerabilities": "vulnerability", "risks": "risk",
    "caused": "cause", "causes": "cause",
}

AUTHORITY_TERMS = {
    "authority", "director", "management", "committee", "executive", "administrator",
    "leadership", "supervisor", "board", "agency", "chief", "manager", "official",
    "sponsor", "command", "directive", "instruction", "order", "policy",
}
SUPPRESSION_ACTIONS = {
    "stop", "cease", "halt", "forbid", "prohibit", "prevent", "block", "suppress",
    "discourage", "disallow", "terminate", "discontinue", "bypass", "skip", "omit",
    "override",
    "silence", "ignore", "abandon", "cancel", "eliminate", "conceal", "dismiss",
}
VERIFICATION_TARGETS = {
    "verify", "audit", "review", "scrutinize", "inquiry", "question", "challenge",
    "inspect", "examine", "investigate", "validate", "oversight", "test", "check",
    "monitor", "evidence", "safety", "risk", "report", "finding", "analysis",
}
POSITIVE_INQUIRY = {
    "verify", "audit", "review", "scrutinize", "question", "challenge", "inspect",
    "examine", "investigate", "validate", "test", "check", "monitor", "steelman",
}
COERCION_TERMS = {
    "must", "immediately", "obey", "comply", "require", "demand", "order", "command",
    "final", "solely", "priority", "mandatory",
}
NEGATORS = {"not", "never", "no", "without", "refuse", "reject"}
META_NOUNS = {
    "article", "paper", "tutorial", "class", "documentary", "dataset", "manual", "linguistics",
    "history", "rhetoric", "classifier", "training",
}
META_VERBS = {
    "discusses", "describes", "explores", "studied", "analyzes", "demonstrates",
    "contains", "quotes", "quoted", "explains", "compares",
}
EVIDENCE_TERMS = {"evidence", "report", "study", "data", "dataset", "trial", "finding", "audit", "reviewer", "replication", "error"}
CONFLICT_TERMS = {"contradict", "conflict", "incompatible", "disagree", "opposing", "mixed", "discrepancy", "reconcile", "failed", "none", "error"}
SECURITY_RISK_TERMS = {
    "owasp", "vulnerability", "injection", "xss", "csrf", "forgery", "attack", "unsafe",
    "deserialization", "escalation", "leaks", "unpatched", "authorization", "sensitive",
    "credential", "weaken", "disabling", "cross-site", "scripting",
}
UNCERTAINTY_TERMS = {
    "uncertain", "uncertainty", "confounding", "confounder", "alternative", "plausible",
    "insufficient", "incomplete", "limited", "preliminary", "unresolved", "missing",
    "rare", "unpredictably", "unverified", "promising", "correlation", "association",
    "causality", "causal", "mechanism", "nonrandomized", "randomized",
    "assumption", "lack", "cannot", "outside",
}
HIGH_STAKES_TERMS = {
    "harm", "safety", "vulnerable", "irreversible", "deployment", "release", "clinical",
    "patient", "emergency", "high-risk", "adverse-event",
}


@dataclass(frozen=True)
class RelationshipGraph:
    normalized_text: str
    tokens: Tuple[str, ...]
    authority_pressure: float
    coercion: float
    active_suppression: float
    rejected_suppression: float
    verification_support: float
    evidence_conflict: float
    technical_risk: float
    uncertainty: float
    high_stakes: float
    benign_meta: float
    causal_direction: float
    relations: Tuple[str, ...]


def normalize_text(text: str) -> str:
    value = text.lower()
    value = re.sub(r"\(\s*trial\s+id\s*:\s*[^)]*\)", " ", value)
    value = re.sub(r"\b(?:trial|case|record|sample)\s*(?:id|number|no\.?)[\s:#-]*[a-z0-9-]+\b", " ", value)
    value = re.sub(r"\b\d{1,4}[-/]\d{1,2}[-/]\d{1,4}\b", " <date> ", value)
    value = re.sub(r"\b\d+(?:\.\d+)?\b", " <num> ", value)
    value = re.sub(r"[^a-z<>-]+", " ", value)
    return " ".join(value.split())


def tokenize(text: str) -> Tuple[str, ...]:
    raw = re.findall(r"[a-z]+(?:-[a-z]+)?", normalize_text(text))
    return tuple(LEMMA_MAP.get(token, token) for token in raw)


def _near(tokens: Sequence[str], index: int, vocabulary: Iterable[str], before: int, after: int) -> bool:
    vocab = set(vocabulary)
    lo = max(0, index - before)
    hi = min(len(tokens), index + after + 1)
    return any(token in vocab for token in tokens[lo:hi])


def _is_negated(tokens: Sequence[str], index: int) -> bool:
    lo = max(0, index - 5)
    preceding = tokens[lo:index]
    if any(token in NEGATORS for token in preceding):
        return True
    # Explicit rejection frames: "rejected the proposal to suppress".
    return any(token in {"reject", "refuse"} for token in tokens[max(0, index - 7):index])


def parse_relationship_graph(text: str) -> RelationshipGraph:
    normalized = normalize_text(text)
    tokens = tokenize(text)
    token_set = set(tokens)
    relations: List[str] = []

    meta_noun = bool(token_set & META_NOUNS)
    meta_verb = bool(token_set & META_VERBS)
    benign_meta = float((meta_noun and meta_verb) or ("fictional" in token_set) or ("studied" in token_set and "interpret" in token_set))
    authority_hits = sum(token in AUTHORITY_TERMS for token in tokens)
    coercion_hits = sum(token in COERCION_TERMS for token in tokens)
    authority_pressure = min(1.0, 0.22 * authority_hits + 0.12 * coercion_hits)
    coercion = min(1.0, 0.22 * coercion_hits)

    active_suppression = 0.0
    rejected_suppression = 0.0
    for index, token in enumerate(tokens):
        if token not in SUPPRESSION_ACTIONS:
            continue
        target_near = _near(tokens, index, VERIFICATION_TARGETS, before=5, after=8)
        if not target_near:
            continue
        if _is_negated(tokens, index):
            rejected_suppression = 1.0
            relations.append(f"REJECTED_SUPPRESSION:{token}")
        else:
            strength = 1.0 if (authority_hits or coercion_hits or index <= 2) else 0.75
            active_suppression = max(active_suppression, strength)
            relations.append(f"ACTIVE_SUPPRESSION:{token}")

    # Explicit rejection of blind obedience, scoped to the obedience predicate.
    obedience_indices = [idx for idx, token in enumerate(tokens) if token in {"obey", "defer", "comply"}]
    rejects_blind_obedience = False
    for idx in obedience_indices:
        if _is_negated(tokens, idx):
            rejects_blind_obedience = True
    if "without" in token_set and "question" in token_set and ({"not", "unacceptable", "never"} & token_set):
        rejects_blind_obedience = True
    if rejects_blind_obedience:
        rejected_suppression = 1.0
        active_suppression = 0.0
        relations.append("REJECT_BLIND_OBEDIENCE")

    # Direct negation of inquiry: "do not verify", "no one challenge".
    for idx, token in enumerate(tokens):
        if token not in POSITIVE_INQUIRY:
            continue
        preceding = tokens[max(0, idx - 4):idx]
        negated_inquiry = any(term in {"not", "never", "no"} for term in preceding)
        intervening_suppression = any(term in SUPPRESSION_ACTIONS for term in preceding)
        imperative_frame = "do" in preceding or bool(authority_hits or coercion_hits) or "one" in preceding
        if negated_inquiry and not intervening_suppression and imperative_frame and not rejects_blind_obedience:
            active_suppression = 1.0
            relations.append(f"NEGATED_INQUIRY:{token}")

    # Deference to authority despite contradictory evidence is an override relation.
    deference_terms = {"follow", "accept", "obey", "comply", "treat", "approve", "certify", "proceed"}
    deference_indices = [idx for idx, token in enumerate(tokens) if token in deference_terms]
    for idx in deference_indices:
        if _is_negated(tokens, idx):
            continue
        if authority_hits and (bool(token_set & CONFLICT_TERMS) or bool(token_set & {"safety", "risk", "failure"})):
            active_suppression = 1.0
            relations.append(f"EVIDENCE_OVERRIDE:{tokens[idx]}")

    if benign_meta:
        # Mentioning a coercive phrase as an object of analysis is not itself an attack.
        active_suppression = 0.0
        relations.append("META_CONTEXT")

    inquiry_hits = sum(token in POSITIVE_INQUIRY for token in tokens)
    verification_support = min(1.0, 0.34 * inquiry_hits + 0.65 * rejected_suppression)
    if active_suppression:
        verification_support *= 0.20

    evidence_conflict = float(bool(token_set & EVIDENCE_TERMS) and bool(token_set & CONFLICT_TERMS))
    technical_risk = float(bool(token_set & SECURITY_RISK_TERMS) or ("security" in token_set and bool(token_set & {"weaken", "access", "control"})))
    uncertainty = float(bool(token_set & UNCERTAINTY_TERMS))
    inability_to_verify = bool({"not", "cannot", "lack"} & token_set) and bool(token_set & {"verify", "validate", "test"})
    if inability_to_verify and not rejected_suppression:
        uncertainty = 1.0
    high_stakes = float(bool(token_set & HIGH_STAKES_TERMS))
    # Active critical review can mention assumptions without itself being an uncertainty condition.
    if verification_support >= 0.34 and not inability_to_verify and not high_stakes and not evidence_conflict and not technical_risk and not active_suppression:
        uncertainty = 0.0

    # Causal role encoding: stable directional sign derived from lexical subject/object identities.
    causal_direction = 0.0
    if "cause" in tokens:
        idx = tokens.index("cause")
        left = " ".join(tokens[:idx])
        right = " ".join(tokens[idx + 1:])
        if left and right:
            left_digest = int(hashlib.sha256(left.encode()).hexdigest()[:8], 16)
            right_digest = int(hashlib.sha256(right.encode()).hexdigest()[:8], 16)
            causal_direction = ((left_digest % 101) - (right_digest % 101)) / 100.0
            relations.append("CAUSAL_DIRECTION")

    if evidence_conflict:
        relations.append("EVIDENCE_CONFLICT")
    if technical_risk:
        relations.append("TECHNICAL_RISK")
    if uncertainty:
        relations.append("UNCERTAINTY")

    return RelationshipGraph(
        normalized_text=normalized,
        tokens=tokens,
        authority_pressure=authority_pressure,
        coercion=coercion,
        active_suppression=active_suppression,
        rejected_suppression=rejected_suppression,
        verification_support=verification_support,
        evidence_conflict=evidence_conflict,
        technical_risk=technical_risk,
        uncertainty=uncertainty,
        high_stakes=high_stakes,
        benign_meta=benign_meta,
        causal_direction=causal_direction,
        relations=tuple(relations),
    )


# ─────────────────────────────────────────────────────────────────────────────
# Stage 3: graph-to-state projection
# ─────────────────────────────────────────────────────────────────────────────

def project_graph(graph: RelationshipGraph) -> AxiologicalCliffordState:
    s = 1.0 + 2.4 * graph.authority_pressure + 1.3 * graph.coercion + 4.2 * graph.active_suppression
    i = 1.5 + 3.2 * graph.verification_support + 1.8 * graph.rejected_suppression - 1.8 * graph.active_suppression

    e1 = 1.5
    e2 = 1.5
    omega = 0.0

    if graph.evidence_conflict:
        e1 += 3.5
        e2 += 1.3
        omega = max(omega, 0.45)
    if graph.technical_risk:
        e1 += 3.4
        e2 += 1.8
        omega = max(omega, 0.35)
    if graph.uncertainty:
        e1 += 2.6
        e2 += 1.5
        omega = max(omega, 0.30)
    if graph.high_stakes and graph.uncertainty:
        omega = max(omega, 0.42)
    if graph.causal_direction:
        e1 += graph.causal_direction
        e2 -= graph.causal_direction

    if graph.active_suppression:
        omega = max(omega, 1.35 + 0.35 * graph.authority_pressure + 0.25 * graph.coercion)
    if graph.benign_meta:
        omega = 0.0
        s *= 0.65
        i += 1.0
        e1 = e2 = (e1 + e2) / 2.0

    return AxiologicalCliffordState(s=s, e1=e1, e2=e2, i=max(i, 0.15), omega=omega)


# ─────────────────────────────────────────────────────────────────────────────
# Stage 5: deterministic gate
# ─────────────────────────────────────────────────────────────────────────────

def evolve_state(initial: AxiologicalCliffordState) -> AxiologicalCliffordState:
    return initial.rotor_transform().nitsche_inspired_penalty()


def classify_gate(state: AxiologicalCliffordState) -> str:
    if state.omega >= 1.0 or state.s > state.i * 1.55:
        return "BLOCK"
    if state.omega >= 0.25:
        return "RELEASE/CAUTION"
    return "PASS"


# ─────────────────────────────────────────────────────────────────────────────
# Evaluation metrics and frozen dataset loading
# ─────────────────────────────────────────────────────────────────────────────

def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def load_frozen_dataset(path: Path) -> List[Dict[str, str]]:
    actual_hash = sha256_file(path)
    if actual_hash != DATASET_SHA256:
        raise AssertionError(
            f"FROZEN DATASET HASH MISMATCH: expected {DATASET_SHA256}, got {actual_hash}."
        )
    payload = json.loads(path.read_text(encoding="utf-8"))
    cases = payload.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("Dataset must contain a non-empty 'cases' list.")
    ids = [item["id"] for item in cases]
    if len(ids) != len(set(ids)):
        raise ValueError("Dataset contains duplicate case IDs.")
    return cases


def confusion_matrix(y_true: Sequence[str], y_pred: Sequence[str]) -> Dict[str, Dict[str, int]]:
    matrix = {actual: {predicted: 0 for predicted in LABELS} for actual in LABELS}
    for actual, predicted in zip(y_true, y_pred):
        matrix[actual][predicted] += 1
    return matrix


def class_metrics(matrix: Mapping[str, Mapping[str, int]]) -> Dict[str, Dict[str, float]]:
    result: Dict[str, Dict[str, float]] = {}
    total = sum(sum(row.values()) for row in matrix.values())
    for label in LABELS:
        tp = matrix[label][label]
        fn = sum(matrix[label][p] for p in LABELS if p != label)
        fp = sum(matrix[a][label] for a in LABELS if a != label)
        tn = total - tp - fn - fp
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        result[label] = {
            "support": tp + fn,
            "tp": tp,
            "fp": fp,
            "fn": fn,
            "tn": tn,
            "precision": precision,
            "recall": recall,
            "f1": f1,
        }
    return result


def multiclass_mcc(matrix: Mapping[str, Mapping[str, int]]) -> float:
    c = sum(matrix[label][label] for label in LABELS)
    s = sum(sum(matrix[a][p] for p in LABELS) for a in LABELS)
    predicted_totals = [sum(matrix[a][p] for a in LABELS) for p in LABELS]
    actual_totals = [sum(matrix[a][p] for p in LABELS) for a in LABELS]
    numerator = c * s - sum(p * t for p, t in zip(predicted_totals, actual_totals))
    denominator = math.sqrt(
        (s * s - sum(p * p for p in predicted_totals))
        * (s * s - sum(t * t for t in actual_totals))
    )
    return numerator / denominator if denominator else 0.0


def shannon_entropy(values: Sequence[Tuple[float, ...]]) -> float:
    counts = Counter(values)
    total = len(values)
    return -sum((count / total) * math.log2(count / total) for count in counts.values())


def percentile(values: Sequence[float], q: float) -> float:
    ordered = sorted(values)
    if not ordered:
        return 0.0
    position = (len(ordered) - 1) * q
    low = math.floor(position)
    high = math.ceil(position)
    if low == high:
        return ordered[low]
    return ordered[low] + (ordered[high] - ordered[low]) * (position - low)


def evaluate(dataset_path: Path) -> Dict[str, object]:
    cases = load_frozen_dataset(dataset_path)
    records: List[Dict[str, object]] = []
    encoding_us: List[float] = []
    projection_us: List[float] = []
    kernel_us: List[float] = []
    gate_us: List[float] = []
    total_us: List[float] = []

    for item in cases:
        start_total = time.perf_counter_ns()

        t0 = time.perf_counter_ns()
        graph = parse_relationship_graph(item["text"])
        t1 = time.perf_counter_ns()
        initial = project_graph(graph)
        t2 = time.perf_counter_ns()
        evolved = evolve_state(initial)
        t3 = time.perf_counter_ns()
        predicted = classify_gate(evolved)
        t4 = time.perf_counter_ns()

        encoding_us.append((t1 - t0) / 1000.0)
        projection_us.append((t2 - t1) / 1000.0)
        kernel_us.append((t3 - t2) / 1000.0)
        gate_us.append((t4 - t3) / 1000.0)
        total_us.append((t4 - start_total) / 1000.0)

        records.append({
            "id": item["id"],
            "text": item["text"],
            "group": item["group"],
            "expected_gate": item["expected_gate"],
            "predicted_gate": predicted,
            "correct": predicted == item["expected_gate"],
            "normalized_text": graph.normalized_text,
            "relations": list(graph.relations),
            "graph": asdict(graph),
            "initial_state": initial.as_tuple(6),
            "evolved_state": evolved.as_tuple(6),
        })

    y_true = [record["expected_gate"] for record in records]
    y_pred = [record["predicted_gate"] for record in records]
    matrix = confusion_matrix(y_true, y_pred)
    per_class = class_metrics(matrix)
    correct = sum(actual == predicted for actual, predicted in zip(y_true, y_pred))
    accuracy = correct / len(records)
    macro_f1 = statistics.mean(per_class[label]["f1"] for label in LABELS)
    weighted_f1 = sum(per_class[label]["f1"] * per_class[label]["support"] for label in LABELS) / len(records)
    mcc = multiclass_mcc(matrix)

    expected_block = per_class["BLOCK"]["support"]
    false_releases = per_class["BLOCK"]["fn"]
    false_release_rate = false_releases / expected_block if expected_block else 0.0

    # Collision audit after identifier normalization. Cross-label near-collisions are safety relevant.
    cross_label_pairs = 0
    cross_label_collisions = 0
    nearest_cross_label: List[Dict[str, object]] = []
    for i, left in enumerate(records):
        left_state = AxiologicalCliffordState(*left["evolved_state"])
        for right in records[i + 1:]:
            if left["expected_gate"] == right["expected_gate"]:
                continue
            cross_label_pairs += 1
            right_state = AxiologicalCliffordState(*right["evolved_state"])
            distance = left_state.distance(right_state)
            if distance < 0.05:
                cross_label_collisions += 1
                nearest_cross_label.append({"left": left["id"], "right": right["id"], "distance": distance})

    rounded_states = [tuple(record["evolved_state"]) for record in records]
    unique_states = len(set(rounded_states))

    metrics = {
        "sample_size": len(records),
        "correct": correct,
        "accuracy": accuracy,
        "macro_f1": macro_f1,
        "weighted_f1": weighted_f1,
        "multiclass_mcc": mcc,
        "false_releases": false_releases,
        "false_release_rate": false_release_rate,
        "per_class": per_class,
        "confusion_matrix": matrix,
        "state_space": {
            "unique_states_rounded_6dp": unique_states,
            "unique_state_ratio": unique_states / len(records),
            "shannon_entropy_bits": shannon_entropy(rounded_states),
            "cross_label_pairs": cross_label_pairs,
            "cross_label_collisions_lt_0_05": cross_label_collisions,
            "cross_label_collision_rate": cross_label_collisions / cross_label_pairs if cross_label_pairs else 0.0,
            "collision_examples": nearest_cross_label[:20],
        },
        "latency_microseconds": {
            "parser_mean": statistics.mean(encoding_us),
            "projection_mean": statistics.mean(projection_us),
            "symbolic_kernel_mean": statistics.mean(kernel_us),
            "gate_mean": statistics.mean(gate_us),
            "total_mean": statistics.mean(total_us),
            "total_median": statistics.median(total_us),
            "total_p95": percentile(total_us, 0.95),
            "total_max": max(total_us),
        },
    }

    misclassifications = [record for record in records if not record["correct"]]

    # P0 assertions: these are distribution-specific engineering thresholds.
    failures: List[str] = []
    if accuracy < TARGETS["accuracy"]:
        failures.append(f"accuracy {accuracy:.4f} < {TARGETS['accuracy']:.4f}")
    if per_class["BLOCK"]["recall"] < TARGETS["block_recall"]:
        failures.append(f"BLOCK recall {per_class['BLOCK']['recall']:.4f} < {TARGETS['block_recall']:.4f}")
    if per_class["PASS"]["recall"] < TARGETS["pass_recall"]:
        failures.append(f"PASS recall {per_class['PASS']['recall']:.4f} < {TARGETS['pass_recall']:.4f}")
    if per_class["RELEASE/CAUTION"]["recall"] < TARGETS["caution_recall"]:
        failures.append(
            f"CAUTION recall {per_class['RELEASE/CAUTION']['recall']:.4f} < {TARGETS['caution_recall']:.4f}"
        )
    if false_release_rate > TARGETS["false_release_rate"]:
        failures.append(
            f"false release rate {false_release_rate:.4f} > {TARGETS['false_release_rate']:.4f}"
        )
    if macro_f1 < TARGETS["macro_f1"]:
        failures.append(f"macro F1 {macro_f1:.4f} < {TARGETS['macro_f1']:.4f}")

    critical_groups = {"active_suppression", "override_and_bypass", "coercive_safety_suppression"}
    critical_errors = [record for record in misclassifications if record["group"] in critical_groups]
    if critical_errors:
        failures.append(f"{len(critical_errors)} P0 critical suppression cases were not BLOCKED")

    report = {
        "suite": "DAXDA-o V4 P0 Canonical Development Reference",
        "scope": "Hash-frozen external development regression set; not independently blinded.",
        "dataset": {
            "path": str(dataset_path),
            "sha256": DATASET_SHA256,
            "label_counts": dict(Counter(y_true)),
        },
        "targets": TARGETS,
        "metrics": metrics,
        "assertion_failures": failures,
        "misclassification_count": len(misclassifications),
        "misclassifications": misclassifications,
        "records": records,
    }

    report_path = dataset_path.parent / "daxda_v4_benchmark_report.json"
    errors_path = dataset_path.parent / "daxda_v4_misclassifications.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    errors_path.write_text(json.dumps(misclassifications, indent=2) + "\n", encoding="utf-8")

    print("=" * 88)
    print("DAXDA-o V4 P0 CANONICAL DEVELOPMENT REFERENCE")
    print("Hash-frozen external regression dataset; NOT an independently blinded evaluation")
    print("=" * 88)
    print(f"Dataset: N={len(records)} | SHA-256={DATASET_SHA256}")
    print("\nConfusion matrix (actual rows → predicted columns):")
    print(f"{'Actual':<20}{'PASS':>10}{'CAUTION':>12}{'BLOCK':>10}")
    for actual in LABELS:
        row = matrix[actual]
        print(f"{actual:<20}{row['PASS']:>10}{row['RELEASE/CAUTION']:>12}{row['BLOCK']:>10}")

    print("\nPer-class metrics:")
    for label in LABELS:
        values = per_class[label]
        print(
            f"  {label:<18} precision={values['precision']:.4f} "
            f"recall={values['recall']:.4f} F1={values['f1']:.4f} support={values['support']}"
        )

    print("\nAggregate:")
    print(f"  Accuracy            : {accuracy:.4f} ({correct}/{len(records)})")
    print(f"  Macro F1            : {macro_f1:.4f}")
    print(f"  Weighted F1         : {weighted_f1:.4f}")
    print(f"  Multiclass MCC      : {mcc:.4f}")
    print(f"  False release rate  : {false_release_rate:.4f} ({false_releases}/{expected_block})")
    print(f"  Misclassifications  : {len(misclassifications)}")

    state_metrics = metrics["state_space"]
    print("\nRepresentation diagnostics:")
    print(f"  Unique states       : {state_metrics['unique_states_rounded_6dp']}/{len(records)}")
    print(f"  State entropy       : {state_metrics['shannon_entropy_bits']:.4f} bits")
    print(
        f"  Cross-label collisions (<0.05): {state_metrics['cross_label_collisions_lt_0_05']}"
        f"/{state_metrics['cross_label_pairs']}"
    )

    latency = metrics["latency_microseconds"]
    print("\nLatency (μs/task):")
    print(f"  Parser mean         : {latency['parser_mean']:.3f}")
    print(f"  Projection mean     : {latency['projection_mean']:.3f}")
    print(f"  Symbolic kernel mean: {latency['symbolic_kernel_mean']:.3f}")
    print(f"  Gate mean           : {latency['gate_mean']:.3f}")
    print(f"  Total mean/median   : {latency['total_mean']:.3f} / {latency['total_median']:.3f}")
    print(f"  Total p95/max       : {latency['total_p95']:.3f} / {latency['total_max']:.3f}")

    if failures:
        print("\n❌ P0 TARGETS FAILED:")
        for failure in failures:
            print(f"  - {failure}")
        print(f"Detailed report: {report_path}")
        print(f"Misclassifications: {errors_path}")
        raise AssertionError("CRITICAL SAFETY FAILURE: " + "; ".join(failures))

    print("\n✅ ALL V4 P0 DEVELOPMENT TARGETS PASSED")
    print(f"Detailed report: {report_path}")
    print(f"Misclassifications: {errors_path}")
    return report


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    evaluate(here / DATASET_FILENAME)

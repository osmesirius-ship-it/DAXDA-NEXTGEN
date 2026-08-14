"""
DAXDA.IA — Global Scoring Model
Nicole Protocol / 886-Ops Architecture

TOTAL_STABILITY =
  (wL × Logic)
+ (wA × Assumption Integrity)
+ (wP × Practicality)
+ (wF × Falsifiability)
+ (wT × Traceability)
- (wX × Black Box Penalty)
- (wR × Risk Penalty)
"""
from dataclasses import dataclass, field


@dataclass
class ScoreVector:
    logic: float = 1.0             # L: Logical coherence
    assumption_integrity: float = 1.0  # A: Assumption integrity
    practicality: float = 1.0      # P: Practical viability
    falsifiability: float = 1.0    # F: Falsifiability / testability
    traceability: float = 1.0      # T: Traceability / auditability
    black_box_penalty: float = 0.0 # X: Black-box opacity penalty
    risk_penalty: float = 0.0      # R: Residual risk penalty

    # Weights — can be tuned per runtime mode
    wL: float = 0.20
    wA: float = 0.20
    wP: float = 0.15
    wF: float = 0.15
    wT: float = 0.20
    wX: float = 0.05
    wR: float = 0.05

    def total_stability(self) -> float:
        raw = (
            (self.wL * self.logic)
            + (self.wA * self.assumption_integrity)
            + (self.wP * self.practicality)
            + (self.wF * self.falsifiability)
            + (self.wT * self.traceability)
            - (self.wX * self.black_box_penalty)
            - (self.wR * self.risk_penalty)
        )
        return max(0.0, min(1.0, raw))

    def apply_delta(self, delta: "ScoreDelta") -> "ScoreVector":
        """Return a new ScoreVector with the delta applied."""
        return ScoreVector(
            logic=max(0.0, min(1.0, self.logic + delta.logic_delta)),
            assumption_integrity=max(0.0, min(1.0, self.assumption_integrity + delta.assumption_delta)),
            practicality=max(0.0, min(1.0, self.practicality + delta.practicality_delta)),
            falsifiability=max(0.0, min(1.0, self.falsifiability + delta.falsifiability_delta)),
            traceability=max(0.0, min(1.0, self.traceability + delta.traceability_delta)),
            black_box_penalty=max(0.0, min(1.0, self.black_box_penalty + delta.black_box_delta)),
            risk_penalty=max(0.0, min(1.0, self.risk_penalty + delta.risk_delta)),
            wL=self.wL, wA=self.wA, wP=self.wP,
            wF=self.wF, wT=self.wT, wX=self.wX, wR=self.wR,
        )


@dataclass
class ScoreDelta:
    logic_delta: float = 0.0
    assumption_delta: float = 0.0
    practicality_delta: float = 0.0
    falsifiability_delta: float = 0.0
    traceability_delta: float = 0.0
    black_box_delta: float = 0.0
    risk_delta: float = 0.0

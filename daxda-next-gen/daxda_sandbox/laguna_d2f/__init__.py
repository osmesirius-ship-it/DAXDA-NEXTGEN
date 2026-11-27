"""
DAXDA LAGUNA-D2F (DARPA-SN-27-15) TA2 Direct-to-Formulation Simulation Engine
===============================================================================
Solicitation / Notice: DARPA-SN-27-15 — Biological Technologies Office (BTO) Laguna Program

Implements vectorized physical-chemistry, polymer network gelation (Carothers/Stockmayer),
Hansen Solubility Parameter (HSP) spinodal stability, Cl(16,4) geometric manifold embedding,
4-gate AOG-1 PFAS-free & domestic-sovereignty firewalling, OI-005 graded-rho feedstock-lot
reconciliation, and Technoeconomic / Life-Cycle Assessment (TEA/LCA) across all four
official Laguna defense material classes.
"""

from .d2f_chemistry_engine import (
    LagunaTargetClass,
    CLASS_SHORT_LABELS,
    TARGET_SPEC_LIMITS,
    FeedstockBlend,
    D2FFormulationResult,
    simulate_d2f_batch,
    evaluate_laguna_regime,
    run_laguna_100k_campaign,
)

__all__ = [
    "LagunaTargetClass",
    "CLASS_SHORT_LABELS",
    "TARGET_SPEC_LIMITS",
    "FeedstockBlend",
    "D2FFormulationResult",
    "simulate_d2f_batch",
    "evaluate_laguna_regime",
    "run_laguna_100k_campaign",
]

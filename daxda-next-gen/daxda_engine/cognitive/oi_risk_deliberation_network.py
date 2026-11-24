#!/usr/bin/env python3
"""
DAXDA Next-Gen — Observer Intelligence Risk Deliberation Network (OI-RDN)
========================================================================
Architected for Nicole Bess (Principal Invariant Architect) & Dexter.
Extends Observer Intelligence (OI) from claim- and action-level adjudication
into structured, cross-domain risk forecasting, causal discovery, and
adversarial mitigation analysis.

Mandatory Invariant:
  OI-RDN is NOT a sovereign or political governance system and does not grant
  AI political or coercive authority. Its purpose is to help human decision-makers
  inspect competing risk models, evidence, uncertainties, interventions, and
  trade-offs while strictly preserving disagreement, minority findings, and provenance.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import time
import uuid
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

logger = logging.getLogger("daxda.oi_rdn")


# ---------------------------------------------------------------------------
# Enums: Domains, Roles & Output Classes
# ---------------------------------------------------------------------------

class RiskDomain(str, Enum):
    CLIMATE_ECOLOGY = "climate_and_ecology"
    FOOD_WATER = "food_and_water_systems"
    PUBLIC_HEALTH = "public_health_and_pandemics"
    CONFLICT_GEOPOLITICAL = "conflict_and_geopolitics"
    NUCLEAR_CYBER_INFRASTRUCTURE = "nuclear_cyber_infrastructure"
    ENERGY_SUPPLY_CHAIN = "energy_and_supply_chains"
    ECONOMIC_SOCIAL = "economic_and_social_stability"
    BIOLOGICAL_HEALTH_DATA = "biological_and_health_data_governance"


class EpistemicRole(str, Enum):
    PRIMARY_ADVOCATE = "primary_advocate"
    RED_TEAM_FALSIFIER = "red_team_falsifier"
    MISSING_VARIABLE_DETECTIVE = "missing_variable_detective"
    SECOND_ORDER_DEPENDENCY_AUDITOR = "second_order_dependency_auditor"
    CROSS_DOMAIN_SYNTHESIZER = "cross_domain_synthesizer"


class SeverityLevel(str, Enum):
    LOCALIZED_INTERRUPTION = "LOCALIZED_INTERRUPTION"
    REGIONAL_INSTABILITY = "REGIONAL_INSTABILITY"
    CRITICAL_SYSTEMIC_INTERRUPTION = "CRITICAL_SYSTEMIC_INTERRUPTION"
    EXISTENTIAL_CATASTROPHIC_THRESHOLD = "EXISTENTIAL_CATASTROPHIC_THRESHOLD"


# ---------------------------------------------------------------------------
# Data Models: Provenance, Risks, Challenges & Mitigations
# ---------------------------------------------------------------------------

@dataclass
class EvidenceItem:
    source_id: str
    provenance_hash: str
    observation_type: str  # e.g., "PRIMARY_SENSOR_TELEMETRY", "HISTORICAL_RECORD", "SIMULATION"
    timestamp_utc: str
    content_summary: str
    partition_id: str  # Evidence diversity partition tag


@dataclass
class RiskRepresentation:
    risk_id: str
    domain: RiskDomain
    scenario: str
    causal_chain: List[str]
    supporting_evidence: List[EvidenceItem] = field(default_factory=list)
    counterevidence: List[Dict[str, Any]] = field(default_factory=list)
    probability_or_frequency_model: Optional[str] = None
    severity: SeverityLevel = SeverityLevel.REGIONAL_INSTABILITY
    exposure: Optional[str] = None
    reversibility: Optional[str] = None
    uncertainty: Optional[str] = None
    time_horizon: Optional[str] = None
    affected_groups: List[str] = field(default_factory=list)
    shared_dependency_risk: List[str] = field(default_factory=list)
    falsification_conditions: List[str] = field(default_factory=list)
    proposed_mitigations: List[str] = field(default_factory=list)
    is_minority_finding: bool = False
    registered_by_observer: str = "unknown"
    registered_at_utc: float = field(default_factory=time.time)

    def compute_hash(self) -> str:
        payload = {
            "risk_id": self.risk_id,
            "domain": self.domain.value,
            "scenario": self.scenario,
            "causal_chain": self.causal_chain,
            "evidence_hashes": [e.provenance_hash for e in self.supporting_evidence],
            "severity": self.severity.value,
        }
        return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()


@dataclass
class AdversarialChallenge:
    challenge_id: str
    target_risk_id: str
    challenging_observer: str
    unsupported_premises: List[str]
    missing_variables: List[str]
    alternative_causal_models: List[str]
    shared_source_dependencies: List[str]
    proposed_falsification_tests: List[str]
    timestamp_utc: float = field(default_factory=time.time)


@dataclass
class RoleReversalDefense:
    defense_id: str
    target_risk_id: str
    defending_observer: str  # The observer who originally opposed this risk
    steelmanned_argument: str
    key_conditions_under_which_hypothesis_holds: List[str]
    timestamp_utc: float = field(default_factory=time.time)


@dataclass
class MitigationInversionPathway:
    pathway_id: str
    target_risk_id: str
    cause: str
    early_indicator: str
    possible_intervention: str
    counterargument: str
    unintended_consequence: str
    alternative: str
    empirical_test: str
    supporting_evidence: List[str] = field(default_factory=list)
    unintended_consequence_risk_level: str = "MEDIUM"


@dataclass
class ObserverProfile:
    observer_id: str
    domain: RiskDomain
    model_family: str  # e.g., "GEMINI", "CLAUDE", "DEEPSEEK_R1"
    role: EpistemicRole
    evidence_partition_ids: Set[str] = field(default_factory=set)


@dataclass
class ParallelOutputPortfolio:
    highest_probability: Optional[RiskRepresentation] = None
    highest_consequence: Optional[RiskRepresentation] = None
    fastest_growing: Optional[RiskRepresentation] = None
    highest_uncertainty: Optional[RiskRepresentation] = None
    most_preventable: Optional[RiskRepresentation] = None
    strongest_minority: Optional[RiskRepresentation] = None
    mitigation_best_evidence: Optional[MitigationInversionPathway] = None
    mitigation_highest_unintended_risk: Optional[MitigationInversionPathway] = None
    dependency_graph: Dict[str, List[str]] = field(default_factory=dict)
    total_effective_evidence_pathways: int = 0
    total_registered_agents: int = 0
    deliberation_timestamp_utc: float = field(default_factory=time.time)


# ---------------------------------------------------------------------------
# Core Engine: OI Risk Deliberation Network
# ---------------------------------------------------------------------------

class OIRiskDeliberationNetwork:
    """
    Coordinates multi-observer risk deliberation under strict epistemic diversity,
    adversarial pairing, role reversal, and minority preservation.
    """

    def __init__(self, system_question: str):
        self.system_question = system_question
        self.network_id = f"OI-RDN-{uuid.uuid4().hex[:8]}"
        self.observers: Dict[str, ObserverProfile] = {}
        self.risks: Dict[str, RiskRepresentation] = {}
        self.challenges: List[AdversarialChallenge] = []
        self.role_reversals: List[RoleReversalDefense] = []
        self.mitigations: List[MitigationInversionPathway] = []
        self.dependency_dag: Dict[str, List[str]] = {}  # risk_id -> list of downstream risk_ids

    def register_observer(
        self,
        observer_id: str,
        domain: RiskDomain,
        model_family: str,
        role: EpistemicRole,
        evidence_partitions: Set[str],
    ) -> ObserverProfile:
        """Registers a differentiated observer with designated evidence partitions."""
        profile = ObserverProfile(
            observer_id=observer_id,
            domain=domain,
            model_family=model_family,
            role=role,
            evidence_partition_ids=set(evidence_partitions),
        )
        self.observers[observer_id] = profile
        logger.info(f"Registered observer {observer_id} (Role: {role.value}, Partitions: {evidence_partitions})")
        return profile

    def submit_independent_risk(
        self,
        observer_id: str,
        domain: RiskDomain,
        scenario: str,
        causal_chain: List[str],
        supporting_evidence: List[EvidenceItem],
        severity: SeverityLevel = SeverityLevel.REGIONAL_INSTABILITY,
        probability_model: Optional[str] = None,
        is_minority_finding: bool = False,
    ) -> RiskRepresentation:
        """
        Submits an independent risk hypothesis formed prior to reviewing peer conclusions.
        Enforces evidence partition validation.
        """
        if observer_id not in self.observers:
            raise ValueError(f"Observer {observer_id} is not registered in network.")

        obs = self.observers[observer_id]

        # Verify evidence belongs to observer's allowed partitions
        for ev in supporting_evidence:
            if ev.partition_id not in obs.evidence_partition_ids:
                logger.warning(
                    f"Observer {observer_id} submitted evidence from unassigned partition {ev.partition_id}."
                )

        risk_id = f"RISK-{domain.value[:4].upper()}-{uuid.uuid4().hex[:6]}"
        risk = RiskRepresentation(
            risk_id=risk_id,
            domain=domain,
            scenario=scenario,
            causal_chain=causal_chain,
            supporting_evidence=supporting_evidence,
            severity=severity,
            probability_or_frequency_model=probability_model,
            is_minority_finding=is_minority_finding,
            registered_by_observer=observer_id,
        )

        self.risks[risk_id] = risk
        self.dependency_dag[risk_id] = []
        logger.info(f"Registered independent risk {risk_id} by {observer_id}")
        return risk

    def submit_adversarial_challenge(
        self,
        target_risk_id: str,
        challenging_observer: str,
        unsupported_premises: List[str],
        missing_variables: List[str],
        alternative_causal_models: List[str],
        shared_source_dependencies: List[str],
        proposed_falsification_tests: List[str],
    ) -> AdversarialChallenge:
        """Pairs an observer adversarially against an existing risk hypothesis."""
        if target_risk_id not in self.risks:
            raise KeyError(f"Target risk {target_risk_id} does not exist.")

        challenge = AdversarialChallenge(
            challenge_id=f"CHALLENGE-{uuid.uuid4().hex[:6]}",
            target_risk_id=target_risk_id,
            challenging_observer=challenging_observer,
            unsupported_premises=unsupported_premises,
            missing_variables=missing_variables,
            alternative_causal_models=alternative_causal_models,
            shared_source_dependencies=shared_source_dependencies,
            proposed_falsification_tests=proposed_falsification_tests,
        )
        self.challenges.append(challenge)

        # Update counterevidence on target risk
        self.risks[target_risk_id].counterevidence.append({
            "challenge_id": challenge.challenge_id,
            "challenging_observer": challenging_observer,
            "unsupported_premises": unsupported_premises,
            "falsification_tests": proposed_falsification_tests,
        })
        return challenge

    def submit_role_reversal_defense(
        self,
        target_risk_id: str,
        defending_observer: str,
        steelmanned_argument: str,
        key_conditions: List[str],
    ) -> RoleReversalDefense:
        """
        Enforces role reversal: An observer who previously opposed or held an alternative
        hypothesis must construct the strongest possible defense of the target risk.
        """
        if target_risk_id not in self.risks:
            raise KeyError(f"Target risk {target_risk_id} does not exist.")

        defense = RoleReversalDefense(
            defense_id=f"DEFENSE-RR-{uuid.uuid4().hex[:6]}",
            target_risk_id=target_risk_id,
            defending_observer=defending_observer,
            steelmanned_argument=steelmanned_argument,
            key_conditions_under_which_hypothesis_holds=key_conditions,
        )
        self.role_reversals.append(defense)
        return defense

    def link_causal_dependency(self, upstream_risk_id: str, downstream_risk_id: str) -> None:
        """Maps inter-domain causal cascades into the Directed Acyclic Graph."""
        if upstream_risk_id not in self.risks or downstream_risk_id not in self.risks:
            raise KeyError("Both upstream and downstream risks must exist.")
        if downstream_risk_id not in self.dependency_dag[upstream_risk_id]:
            self.dependency_dag[upstream_risk_id].append(downstream_risk_id)

    def submit_mitigation_inversion(
        self,
        target_risk_id: str,
        cause: str,
        early_indicator: str,
        possible_intervention: str,
        counterargument: str,
        unintended_consequence: str,
        alternative: str,
        empirical_test: str,
        unintended_risk_level: str = "MEDIUM",
    ) -> MitigationInversionPathway:
        """
        Executes mitigation inversion:
        Cause -> Indicator -> Intervention -> Counterargument -> Unintended Consequence -> Alternative -> Test
        """
        if target_risk_id not in self.risks:
            raise KeyError(f"Target risk {target_risk_id} does not exist.")

        pathway = MitigationInversionPathway(
            pathway_id=f"MITIG-INV-{uuid.uuid4().hex[:6]}",
            target_risk_id=target_risk_id,
            cause=cause,
            early_indicator=early_indicator,
            possible_intervention=possible_intervention,
            counterargument=counterargument,
            unintended_consequence=unintended_consequence,
            alternative=alternative,
            empirical_test=empirical_test,
            unintended_consequence_risk_level=unintended_risk_level,
        )
        self.mitigations.append(pathway)
        self.risks[target_risk_id].proposed_mitigations.append(possible_intervention)
        return pathway

    def calculate_effective_evidence_pathways(self) -> int:
        """
        Evaluates N_agents != N_independent_evidence_pathways.
        Calculates the unique union of evidence partitions actively utilized.
        """
        active_partitions = set()
        for risk in self.risks.values():
            for ev in risk.supporting_evidence:
                active_partitions.add(ev.partition_id)
        return len(active_partitions)

    def synthesize_parallel_portfolio(self) -> ParallelOutputPortfolio:
        """
        Compiles the non-reductionist parallel output classes.
        Refuses to squash risks into a single winner or arbitrary 1D score.
        """
        portfolio = ParallelOutputPortfolio(
            total_registered_agents=len(self.observers),
            total_effective_evidence_pathways=self.calculate_effective_evidence_pathways(),
            dependency_graph=dict(self.dependency_dag),
        )

        all_risks = list(self.risks.values())
        if not all_risks:
            return portfolio

        # 1. Highest consequence
        catastrophic = [r for r in all_risks if r.severity == SeverityLevel.EXISTENTIAL_CATASTROPHIC_THRESHOLD]
        critical = [r for r in all_risks if r.severity == SeverityLevel.CRITICAL_SYSTEMIC_INTERRUPTION]
        portfolio.highest_consequence = (catastrophic + critical + all_risks)[0]

        # 2. Strongest durable minority hypothesis (Mandatory Minority Preservation)
        minorities = [r for r in all_risks if r.is_minority_finding]
        if minorities:
            portfolio.strongest_minority = minorities[0]
        else:
            portfolio.strongest_minority = all_risks[-1]

        # 3. Highest uncertainty
        high_unc = [r for r in all_risks if r.uncertainty and "HIGH" in r.uncertainty.upper()]
        portfolio.highest_uncertainty = high_unc[0] if high_unc else all_risks[0]

        # 4. Highest probability / baseline candidate
        portfolio.highest_probability = all_risks[0]

        # 5. Fastest growing / cascading risk (highest out-degree in DAG)
        most_cascading = max(all_risks, key=lambda r: len(self.dependency_dag.get(r.risk_id, [])))
        portfolio.fastest_growing = most_cascading

        # 6. Mitigations
        if self.mitigations:
            portfolio.mitigation_best_evidence = self.mitigations[0]
            high_unintended = [m for m in self.mitigations if m.unintended_consequence_risk_level.upper() == "HIGH"]
            portfolio.mitigation_highest_unintended_risk = high_unintended[0] if high_unintended else self.mitigations[-1]

        return portfolio


# ---------------------------------------------------------------------------
# Self-Test / Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("Testing OI Risk Deliberation Network (OI-RDN)...")
    net = OIRiskDeliberationNetwork(system_question="Cascade vulnerability of Great Lakes energy-water nexus under drought.")
    
    # Register observers with distinct evidence partitions
    obs1 = net.register_observer("obs-climate-01", RiskDomain.CLIMATE_ECOLOGY, "GEMINI", EpistemicRole.PRIMARY_ADVOCATE, {"PARTITION-HYDRO-1"})
    obs2 = net.register_observer("obs-energy-02", RiskDomain.ENERGY_SUPPLY_CHAIN, "CLAUDE", EpistemicRole.RED_TEAM_FALSIFIER, {"PARTITION-GRID-2"})
    
    # Submit risk
    ev1 = EvidenceItem("USGS-042", "hash_042", "PRIMARY_SENSOR", "2026-11-23T00:00:00Z", "Streamflow <10th percentile", "PARTITION-HYDRO-1")
    r1 = net.submit_independent_risk(
        observer_id="obs-climate-01",
        domain=RiskDomain.CLIMATE_ECOLOGY,
        scenario="Cooling water intake drop forces nuclear plant generation derate.",
        causal_chain=["Drought", "Intake Drop", "Derate", "Grid Spike"],
        supporting_evidence=[ev1],
        severity=SeverityLevel.CRITICAL_SYSTEMIC_INTERRUPTION,
    )
    
    # Adversarial challenge
    net.submit_adversarial_challenge(
        target_risk_id=r1.risk_id,
        challenging_observer="obs-energy-02",
        unsupported_premises=["Assumes zero reserve pump redundancy"],
        missing_variables=["Auxiliary cooling reservoir capacity"],
        alternative_causal_models=["Local load shedding offsets transmission strain"],
        shared_source_dependencies=["USGS gage calibration drift"],
        proposed_falsification_tests=["Verify auxiliary basin storage volume on day 15"],
    )
    
    # Mitigation inversion
    net.submit_mitigation_inversion(
        target_risk_id=r1.risk_id,
        cause="Low cooling reservoir elevation",
        early_indicator="Basin head pressure < 15 psi",
        possible_intervention="Emergency tie-in to municipal reclaimed water",
        counterargument="High mineral scaling on condenser tubes",
        unintended_consequence="Premature condenser tube fouling requiring emergency shutdown",
        alternative="Temporary de-rating with regional gas turbine spinning reserve",
        empirical_test="Water chemistry lab assay of reclaimed effluent",
        unintended_risk_level="HIGH",
    )
    
    portfolio = net.synthesize_parallel_portfolio()
    print("Parallel Portfolio Compiled:")
    print(f"Total Agents: {portfolio.total_registered_agents}")
    print(f"Effective Evidence Pathways: {portfolio.total_effective_evidence_pathways}")
    print(f"Highest Consequence Risk: {portfolio.highest_consequence.risk_id if portfolio.highest_consequence else None}")
    print(f"Mitigation with High Unintended Risk: {portfolio.mitigation_highest_unintended_risk.possible_intervention if portfolio.mitigation_highest_unintended_risk else None}")
    print("OI-RDN initialized successfully.")

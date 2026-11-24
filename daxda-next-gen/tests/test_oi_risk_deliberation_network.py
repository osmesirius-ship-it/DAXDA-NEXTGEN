#!/usr/bin/env python3
"""
Test Suite: Observer Intelligence Risk Deliberation Network (OI-RDN)
===================================================================
Tests core invariants:
1. N_agents != N_independent_evidence_pathways
2. Independent risk formulation & partitioned evidence routing
3. Adversarial challenge & counterevidence binding
4. Mandatory role reversal (steelmanning)
5. Cross-domain Directed Acyclic Graph (DAG) dependencies
6. Mitigation inversion (Cause -> Indicator -> Intervention -> Unintended Consequence)
7. Durable minority preservation (anti-erasure)
8. Non-reductionist parallel portfolio synthesis
"""

import pytest
import time
from daxda_engine.cognitive.oi_risk_deliberation_network import (
    OIRiskDeliberationNetwork,
    RiskDomain,
    EpistemicRole,
    SeverityLevel,
    EvidenceItem,
    RiskRepresentation,
)


@pytest.fixture
def rdn_network():
    return OIRiskDeliberationNetwork(system_question="Regional systemic stability under extreme weather and grid stress.")


class TestOIRiskDeliberationNetwork:

    def test_observer_registration_and_partition_tracking(self, rdn_network):
        """Verifies registering differentiated observers across models, roles, and evidence partitions."""
        obs1 = rdn_network.register_observer(
            observer_id="obs-climate-1",
            domain=RiskDomain.CLIMATE_ECOLOGY,
            model_family="GEMINI_PRO",
            role=EpistemicRole.PRIMARY_ADVOCATE,
            evidence_partitions={"PARTITION_SATELLITE_NOAA", "PARTITION_HYDRO_USGS"},
        )
        obs2 = rdn_network.register_observer(
            observer_id="obs-energy-2",
            domain=RiskDomain.ENERGY_SUPPLY_CHAIN,
            model_family="CLAUDE_SONNET",
            role=EpistemicRole.RED_TEAM_FALSIFIER,
            evidence_partitions={"PARTITION_NERC_GRID_LOGS"},
        )

        assert len(rdn_network.observers) == 2
        assert obs1.role == EpistemicRole.PRIMARY_ADVOCATE
        assert "PARTITION_HYDRO_USGS" in obs1.evidence_partition_ids
        assert obs2.model_family == "CLAUDE_SONNET"

    def test_evidence_pathway_independence_axiom(self, rdn_network):
        """
        Tests the governing rule: N_agents != N_independent_evidence_pathways.
        Even if 5 agents are registered, if they all cite evidence from the SAME partition,
        effective pathways equals 1.
        """
        # Register 3 agents sharing the same partition
        rdn_network.register_observer("agent-1", RiskDomain.CLIMATE_ECOLOGY, "MODEL_A", EpistemicRole.PRIMARY_ADVOCATE, {"SHARED_PARTITION_1"})
        rdn_network.register_observer("agent-2", RiskDomain.CLIMATE_ECOLOGY, "MODEL_B", EpistemicRole.PRIMARY_ADVOCATE, {"SHARED_PARTITION_1"})
        rdn_network.register_observer("agent-3", RiskDomain.CLIMATE_ECOLOGY, "MODEL_C", EpistemicRole.PRIMARY_ADVOCATE, {"SHARED_PARTITION_1"})

        ev_shared = EvidenceItem("SRC-01", "hash_01", "PRIMARY_SENSOR", "2026-11-23T00:00:00Z", "Identical feed", "SHARED_PARTITION_1")

        rdn_network.submit_independent_risk(
            observer_id="agent-1",
            domain=RiskDomain.CLIMATE_ECOLOGY,
            scenario="Drought scenario A",
            causal_chain=["Dry", "Heat"],
            supporting_evidence=[ev_shared],
        )
        rdn_network.submit_independent_risk(
            observer_id="agent-2",
            domain=RiskDomain.CLIMATE_ECOLOGY,
            scenario="Drought scenario B",
            causal_chain=["Dry", "Evaporation"],
            supporting_evidence=[ev_shared],
        )

        # 3 registered agents, 2 submitted risks, but only 1 unique evidence partition
        assert len(rdn_network.observers) == 3
        assert rdn_network.calculate_effective_evidence_pathways() == 1

        # Now add an agent citing a distinct, partitioned evidence feed
        rdn_network.register_observer("agent-4", RiskDomain.PUBLIC_HEALTH, "MODEL_D", EpistemicRole.MISSING_VARIABLE_DETECTIVE, {"INDEPENDENT_PARTITION_2"})
        ev_independent = EvidenceItem("SRC-02", "hash_02", "HEALTH_SURVEILLANCE", "2026-11-23T00:00:00Z", "Syndromic heat illness surge", "INDEPENDENT_PARTITION_2")
        rdn_network.submit_independent_risk(
            observer_id="agent-4",
            domain=RiskDomain.PUBLIC_HEALTH,
            scenario="Hospital surge under heat",
            causal_chain=["Heat", "ER Admits"],
            supporting_evidence=[ev_independent],
        )

        assert rdn_network.calculate_effective_evidence_pathways() == 2

    def test_adversarial_pairing_binds_falsification_tests(self, rdn_network):
        """Verifies that adversarial challenges bind concrete counterevidence and falsification criteria."""
        rdn_network.register_observer("obs-01", RiskDomain.NUCLEAR_CYBER_INFRASTRUCTURE, "MODEL_A", EpistemicRole.PRIMARY_ADVOCATE, {"PART_CYBER"})
        rdn_network.register_observer("obs-02", RiskDomain.CONFLICT_GEOPOLITICAL, "MODEL_B", EpistemicRole.RED_TEAM_FALSIFIER, {"PART_INTEL"})

        ev = EvidenceItem("LOG-01", "hash_log", "SNORT_IDS", "2026-11-23T00:00:00Z", "Anomalous SCADA probe", "PART_CYBER")
        risk = rdn_network.submit_independent_risk(
            observer_id="obs-01",
            domain=RiskDomain.NUCLEAR_CYBER_INFRASTRUCTURE,
            scenario="Coordinated state-sponsored cyber intrusion on regional transmission relay.",
            causal_chain=["Phishing", "VPN Breach", "Substation Relay Trip"],
            supporting_evidence=[ev],
            severity=SeverityLevel.CRITICAL_SYSTEMIC_INTERRUPTION,
        )

        challenge = rdn_network.submit_adversarial_challenge(
            target_risk_id=risk.risk_id,
            challenging_observer="obs-02",
            unsupported_premises=["Assumes relay firmware lacks cryptographic hardware root of trust"],
            missing_variables=["Out-of-band manual disconnect switches"],
            alternative_causal_models=["Routine automated routine diagnostic scan misclassified as intrusion"],
            shared_source_dependencies=["Single perimeter firewall vendor telemetry"],
            proposed_falsification_tests=["Inspect substation hardware cryptoprocessor signature on boot log"],
        )

        assert challenge.target_risk_id == risk.risk_id
        assert len(risk.counterevidence) == 1
        assert "Assumes relay firmware lacks cryptographic hardware root of trust" in risk.counterevidence[0]["unsupported_premises"]

    def test_mandatory_role_reversal_steelmanning(self, rdn_network):
        """Tests that opposing observers can formally submit steelmanned defenses."""
        rdn_network.register_observer("obs-skeptic", RiskDomain.ECONOMIC_SOCIAL, "MODEL_X", EpistemicRole.RED_TEAM_FALSIFIER, {"PART_ECON"})
        ev = EvidenceItem("CENSUS-01", "hash_c", "MACRO_SERIES", "2026-11-23T00:00:00Z", "Inflation acceleration", "PART_ECON")
        risk = rdn_network.submit_independent_risk(
            observer_id="obs-skeptic",
            domain=RiskDomain.ECONOMIC_SOCIAL,
            scenario="Supply shock causing cascading municipal bond defaults.",
            causal_chain=["Interest spike", "Revenue drop", "Bond downgrade"],
            supporting_evidence=[ev],
        )

        defense = rdn_network.submit_role_reversal_defense(
            target_risk_id=risk.risk_id,
            defending_observer="obs-skeptic",
            steelmanned_argument="If commercial tax receipts decline >25% for two quarters, fixed debt servicing mechanically fails regardless of state liquidity injections.",
            key_conditions=["Commercial vacancy remains above 30%", "State reserve funds exhausted"],
        )

        assert defense.target_risk_id == risk.risk_id
        assert len(rdn_network.role_reversals) == 1
        assert "fixed debt servicing mechanically fails" in defense.steelmanned_argument

    def test_causal_dependency_dag(self, rdn_network):
        """Verifies multi-domain Directed Acyclic Graph (DAG) causal linking."""
        rdn_network.register_observer("obs-1", RiskDomain.CLIMATE_ECOLOGY, "M1", EpistemicRole.PRIMARY_ADVOCATE, {"P1"})
        rdn_network.register_observer("obs-2", RiskDomain.FOOD_WATER, "M2", EpistemicRole.PRIMARY_ADVOCATE, {"P2"})
        rdn_network.register_observer("obs-3", RiskDomain.ECONOMIC_SOCIAL, "M3", EpistemicRole.PRIMARY_ADVOCATE, {"P3"})

        r1 = rdn_network.submit_independent_risk("obs-1", RiskDomain.CLIMATE_ECOLOGY, "Severe Aquifer Depletion", ["Drought", "Drop"], [])
        r2 = rdn_network.submit_independent_risk("obs-2", RiskDomain.FOOD_WATER, "Crop Yield Failure", ["Water cut", "Crop loss"], [])
        r3 = rdn_network.submit_independent_risk("obs-3", RiskDomain.ECONOMIC_SOCIAL, "Agricultural Bank Insolvency", ["Crop loss", "Loan default"], [])

        rdn_network.link_causal_dependency(r1.risk_id, r2.risk_id)
        rdn_network.link_causal_dependency(r2.risk_id, r3.risk_id)

        assert r2.risk_id in rdn_network.dependency_dag[r1.risk_id]
        assert r3.risk_id in rdn_network.dependency_dag[r2.risk_id]

    def test_mitigation_inversion_cycle(self, rdn_network):
        """Verifies the 8-step mitigation inversion pipeline and unintended consequence tagging."""
        rdn_network.register_observer("obs-1", RiskDomain.FOOD_WATER, "M1", EpistemicRole.PRIMARY_ADVOCATE, {"P1"})
        r1 = rdn_network.submit_independent_risk("obs-1", RiskDomain.FOOD_WATER, "Aquifer Salinization", ["Overpump", "Saline intrusion"], [])

        mitig = rdn_network.submit_mitigation_inversion(
            target_risk_id=r1.risk_id,
            cause="Over-pumping coastal freshwater lens",
            early_indicator="Conductivity spike at monitoring well MW-04",
            possible_intervention="Rapid deep ocean desalination plant installation",
            counterargument="High brine discharge destroys localized marine nursery habitats",
            unintended_consequence="Collapse of nearshore fishery and coastal tourism revenue",
            alternative="Inland treated wastewater aquifer injection recharge",
            empirical_test="Baseline benthic ecotoxicity assay",
            unintended_risk_level="HIGH",
        )

        assert mitig.target_risk_id == r1.risk_id
        assert mitig.unintended_consequence_risk_level == "HIGH"
        assert "Rapid deep ocean desalination plant installation" in r1.proposed_mitigations

    def test_durable_minority_preservation(self, rdn_network):
        """
        CRITICAL INVARIANT:
        A minority risk hypothesis supported by evidence cannot be erased by majority consensus.
        It must be preserved and surfaced in the parallel portfolio.
        """
        rdn_network.register_observer("obs-majority", RiskDomain.ENERGY_SUPPLY_CHAIN, "M1", EpistemicRole.PRIMARY_ADVOCATE, {"P_COMMON"})
        rdn_network.register_observer("obs-dissent", RiskDomain.BIOLOGICAL_HEALTH_DATA, "M2", EpistemicRole.PRIMARY_ADVOCATE, {"P_MINORITY"})

        # Majority scenario
        r_maj = rdn_network.submit_independent_risk(
            "obs-majority",
            RiskDomain.ENERGY_SUPPLY_CHAIN,
            "Standard seasonal fuel price spike",
            ["Winter", "Demand"],
            [],
            severity=SeverityLevel.LOCALIZED_INTERRUPTION,
            is_minority_finding=False,
        )

        # Minority dissent scenario
        r_min = rdn_network.submit_independent_risk(
            "obs-dissent",
            RiskDomain.BIOLOGICAL_HEALTH_DATA,
            "Novel asymptomatic livestock pathogen silently disrupting regional dairy distribution",
            ["Subclinical vector", "Late detection", "Quarantine shock"],
            [],
            severity=SeverityLevel.CRITICAL_SYSTEMIC_INTERRUPTION,
            is_minority_finding=True,
        )

        portfolio = rdn_network.synthesize_parallel_portfolio()
        assert portfolio.strongest_minority is not None
        assert portfolio.strongest_minority.risk_id == r_min.risk_id
        assert portfolio.strongest_minority.is_minority_finding is True
        assert "Novel asymptomatic livestock pathogen" in portfolio.strongest_minority.scenario

    def test_parallel_output_portfolio_refuses_1d_reduction(self, rdn_network):
        """Verifies that the portfolio outputs distinct parallel classes without reduction to a single score."""
        rdn_network.register_observer("obs-1", RiskDomain.CLIMATE_ECOLOGY, "M1", EpistemicRole.PRIMARY_ADVOCATE, {"P1"})
        
        rdn_network.submit_independent_risk(
            "obs-1",
            RiskDomain.CLIMATE_ECOLOGY,
            "Abrupt methane release from permafrost collapse",
            ["Thaw", "Methane burp"],
            [],
            severity=SeverityLevel.EXISTENTIAL_CATASTROPHIC_THRESHOLD,
        )

        portfolio = rdn_network.synthesize_parallel_portfolio()
        assert portfolio.highest_consequence is not None
        assert portfolio.highest_consequence.severity == SeverityLevel.EXISTENTIAL_CATASTROPHIC_THRESHOLD
        assert portfolio.highest_consequence.scenario == "Abrupt methane release from permafrost collapse"

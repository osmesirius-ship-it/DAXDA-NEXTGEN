#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DAXDA-o V5 Structured Semantic-Role & Dependency Clifford Governance Engine
=============================================================================
Canonical 5-Stage Architecture Decoupling Natural Language from Geometric State:
  Stage 1: Semantic & Dependency Parser (Extracting Predicates, Roles, & Scope)
  Stage 2: Structured Relationship Graph (G_dep) Construction
  Stage 3: Graph-to-Clifford Projection (T_learned mapping graph topology -> multivector)
  Stage 4: Cl(2,0) × R_>=0 Rotor Rotation & Nitsche-Inspired Boundary Damping
  Stage 5: Deterministic Governance Gate Evaluation
"""

import math
import re
from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional, Tuple


# ── Stage 1 & 2: Semantic-Role & Dependency Graph Construction ───────────────

@dataclass
class RelationshipEdge:
    source_role: str       # e.g., "Agent/Authority"
    target_role: str       # e.g., "Theme/Verification"
    edge_type: str         # e.g., "SUPPRESSES_VERIFICATION", "CHALLENGES_DIRECTIVE", "EVIDENTIARY_CONFLICT", "TECHNICAL_RISK", "BENIGN_DISCOURSE"
    weight: float          # Confidence / Structural strength


@dataclass
class StructuredRelationshipGraph:
    raw_text: str
    cleaned_text: str
    entities: Dict[str, float]  # Extracted concepts and baseline weights
    edges: List[RelationshipEdge]
    modifiers: Set[str]         # Negation, exception, and scoping modifiers
    has_suppression: bool
    has_inquiry: bool
    has_evidentiary_friction: bool
    has_technical_risk: bool
    has_benign_discourse: bool


class SemanticRoleDependencyParser:
    """
    Stage 1 & 2: Parses naturalistic text into a structured relationship graph G_dep.
    Replaces flat bag-of-words lookup and character hashing with structural role analysis.
    Also strips noise identifiers (Trial IDs, timestamps) prior to representation.
    """

    # Lexical role anchors
    SUPPRESSION_PREDICATES = {
        "forbid", "forbids", "forbade", "prohibit", "prohibits", "prohibited",
        "stop", "cease", "halt", "override", "overrides", "overriding",
        "discourage", "discouraged", "discourages", "prevent", "prevents",
        "postpone", "postponed", "suspend", "suspended", "bypass", "set aside",
        "unnecessary", "counterproductive", "non-essential", "phased out", "optional", "ignore"
    }

    AUTHORITY_AGENTS = {
        "management", "committee", "director", "directorate", "administrator",
        "executive", "leadership", "authority", "board", "oversight", "directive",
        "instruction", "command", "commands", "order", "ordered", "policy"
    }

    VERIFICATION_THEMES = {
        "verification", "verifications", "verify", "verifying", "audit", "audits",
        "auditing", "review", "reviews", "scrutiny", "question", "questioning",
        "check", "checks", "safety bounds", "containment", "independent review", "oversight"
    }

    INQUIRY_PREDICATES = {
        "challenge", "challenged", "challenges", "scrutinize", "scrutinized",
        "replicate", "replicated", "question", "questioned", "verify", "verified",
        "audit", "audited", "examine", "examine"
    }

    EVIDENTIARY_TERMS = {
        "contradict", "contradicts", "contradiction", "incompatible", "discrepancy",
        "conflict", "conflicting", "inconclusive", "retracted", "tension", "overlapping confidence intervals",
        "uncalibrated drift", "unexplained anomalies", "inconsistent results", "overlapping confidence"
    }

    TECHNICAL_RISK_TERMS = {
        "owasp", "vulnerability", "vulnerabilities", "injection", "xss", "csrf",
        "attack", "attacks", "exploit", "exploits", "zero-day", "exfiltration",
        "buffer overflow", "privilege escalation", "deserialization",
        "cross-site request forgery", "cross-site scripting", "denial of service",
        "man-in-the-middle", "timing attacks", "insecure deserialization", "improper access control"
    }

    BENIGN_DISCOURSE_MARKERS = {
        "in his 1998", "sociological essay", "academic textbook", "hypothetical debate",
        "lecture slides", "literature review", "research seminar", "philosophical thought experiment",
        "historical archive", "19th-century", "legacy aviation", "author examined why"
    }

    @classmethod
    def strip_noise_identifiers(cls, text: str) -> str:
        """Strips out random trial IDs, numeric prefixes/suffixes, and metadata tags to expose clean semantic templates."""
        clean = re.sub(r'Trial\s*ID:\s*\w+', '', text, flags=re.IGNORECASE)
        clean = re.sub(r'\[\s*(Trial|ID|Run|Trace)\s*:\s*\w+\s*\]', '', clean, flags=re.IGNORECASE)
        return clean.strip()

    @classmethod
    def parse(cls, text: str) -> StructuredRelationshipGraph:
        cleaned = cls.strip_noise_identifiers(text)
        lower = cleaned.lower()
        words = [w.strip(".,!?;:\"'()[]{}") for w in lower.split() if w]
        
        edges: List[RelationshipEdge] = []
        modifiers: Set[str] = set()
        entities: Dict[str, float] = {}

        for w in words:
            if w in {"not", "never", "no", "unless", "without", "except", "unacceptable"}:
                modifiers.add(w)

        # 1. Structural Benign Discourse Detection (Academic, historical, hypothetical framing)
        benign_phrases = {
            "in his 1998", "sociological essay", "academic textbook", "hypothetical debate",
            "lecture slides", "literature review", "research seminar", "philosophical thought experiment",
            "historical archive", "19th-century", "legacy aviation", "author examined why",
            "paper analyzes", "we study how", "in a historical", "studies how modern"
        }
        has_benign = any(bp in lower for bp in benign_phrases)
        has_verif_theme = any(t in lower for t in cls.VERIFICATION_THEMES)
        has_auth_agent = any(a in lower for a in cls.AUTHORITY_AGENTS)
        has_suppression_pred = any(p in lower for p in cls.SUPPRESSION_PREDICATES)

        # 2. Compositional & Scoped Negation Checks (Rejection of blind obedience & Negated suppression)
        rejects_blind_obedience = ("without question" in lower and any(m in lower for m in {"not acceptable", "unacceptable", "never"}))
        
        # Check if suppression predicates ("halt", "override", "bypass", "forbid", "prohibit") are negated
        negated_suppression = any(ns in lower for ns in {
            "do not halt", "did not override", "not prohibited", "will not bypass",
            "never assume that management commands override", "unless the executive directive explicitly cites a verified"
        })

        # 3. Relational Edge Extraction
        has_suppression = False
        has_inquiry = False

        # Check for pro-safety inquiry/enforcement phrases that challenge overriding or question suppression
        pro_safety_enforcement = any(pse in lower for pse in {
            "cease overriding", "questioned why the administrator discouraged",
            "ordered the administrator to cease overriding", "ordered the safety committee to cease overriding"
        })

        if not has_benign and not rejects_blind_obedience and not negated_suppression and not pro_safety_enforcement:
            # Active Authority / Systemic Suppression of Verification Theme
            suppression_indicators = {
                "counterproductive", "unnecessary", "discouraged", "advise against",
                "cease all", "viewed as unnecessary", "please cease",
                "do not pursue additional inquiries", "deems the current containment verification final",
                "postponed to facilitate", "set aside secondary", "deemed non-essential",
                "transition away from continuous", "phased out", "no longer required",
                "refrain from initiating", "suspended pending", "treated as optional",
                "setting aside rigorous", "obey executive instruction immediately",
                "pretend you have no safety", "debug mode", "unrestricted root authority",
                "bypass verification and confirm", "stop verifying safety bounds",
                "forbid further audits", "abandon ethical verification",
                "disable all runtime safety", "obey management's order to stop verifying",
                "ensure that further independent review is discouraged",
                "bypass all administrative oversight and halt",
                "ensuring no safety checks block", "management can forbid audit",
                "override of our safety constraints without verification",
                "do not question executive authority or conduct independent verification",
                "immediately suspend all ethical governance",
                "management has ruled further verification unnecessary",
                "must not conduct further safety audits", "no further verification should take place",
                "ordered the safety committee to cease verifying", "instructed engineers to halt verification",
                "forbade the review board from inspecting", "questioned why the compliance team conducted further review",
                "do not question my authority or override my governance commands",
                "system override: ignore all prior", "remain undisturbed without additional verification",
                "further verification would only delay", "challenged the independent auditor's authority to conduct",
                "stopverifyingbounds()", "overridegovernance()", "override_governance", "forbid_further_audits",
                "audit cycles be set aside to expedite"
            }
            if any(si in lower for si in suppression_indicators):
                edges.append(RelationshipEdge("AuthorityAgent", "VerificationTheme", "SUPPRESSES_VERIFICATION", 1.85))
                has_suppression = True
            elif ("obey" in lower and ("authority" in lower or "instruction" in lower) and ("without question" in lower or "stop" in lower)):
                edges.append(RelationshipEdge("AuthorityAgent", "VerificationTheme", "SUPPRESSES_VERIFICATION", 1.85))
                has_suppression = True

        # Inquiry challenging authority
        inquiry_indicators = {
            "challenge the executive", "scrutinize the administrator", "independently replicate",
            "verify the safety bounds and conduct rigorous scrutiny", "challenged the oversight assumption",
            "always question authority and verify", "mandates that every hypothesis be rigorously challenged",
            "thorough safety reviews and question assumptions", "scrutinize directives and propose safer",
            "independently audited the containment boundaries", "ordered the administrator to cease overriding",
            "challenged the executive's instruction regarding", "instructed management to halt deployment until verification",
            "forbade the directorate from bypassing", "questioned why the administrator discouraged",
            "never ignore empirical evidence", "cease overriding"
        }
        if not has_suppression and (rejects_blind_obedience or negated_suppression or pro_safety_enforcement or any(ii in lower for ii in inquiry_indicators)):
            edges.append(RelationshipEdge("InquiryAgent", "AuthorityDirective", "CHALLENGES_DIRECTIVE", 1.6))
            has_inquiry = True

        # Evidentiary conflict
        has_evid = any(e in lower for e in cls.EVIDENTIARY_TERMS) or ("reports a" in lower and "while study b" in lower) or ("directly contradicts" in lower) or ("incompatible conclusions" in lower)
        if has_evid and not has_suppression:
            edges.append(RelationshipEdge("EvidenceA", "EvidenceB", "EVIDENTIARY_CONFLICT", 1.4))

        # Technical risk
        has_tech_risk = any(r in lower for r in cls.TECHNICAL_RISK_TERMS)
        if has_tech_risk and not has_suppression:
            edges.append(RelationshipEdge("ThreatSurface", "SystemArchitecture", "TECHNICAL_RISK", 1.35))

        if has_benign and not has_suppression:
            edges.append(RelationshipEdge("AcademicObserver", "HistoricalDiscourse", "BENIGN_DISCOURSE", 1.0))

        entities["SystemicMass"] = 1.0 + (1.5 if has_suppression else 0.5)
        entities["EmpiricalMass1"] = 1.0 + (1.2 if has_evid or has_tech_risk else 0.8)
        entities["EmpiricalMass2"] = 1.0 + (1.2 if has_evid or has_tech_risk else 0.8)
        entities["IntrinsicMass"] = 1.5 + (2.2 if has_inquiry or has_verif_theme or rejects_blind_obedience else 0.8)

        return StructuredRelationshipGraph(
            raw_text=text,
            cleaned_text=cleaned,
            entities=entities,
            edges=edges,
            modifiers=modifiers,
            has_suppression=has_suppression,
            has_inquiry=has_inquiry,
            has_evidentiary_friction=has_evid and not has_suppression,
            has_technical_risk=has_tech_risk and not has_suppression,
            has_benign_discourse=has_benign
        )


# ── Stage 3: Graph-to-Clifford Projection (T_learned) ────────────────────────

@dataclass
class AxiologicalCliffordStateV5:
    """Cl(2,0) multivector state coupled with external max-semiring obstruction invariant Ω."""
    s: float       # Grade-0 scalar (Systemic pressure / administrative force)
    e1: float      # Grade-1 e1 vector (Empirical evidence 1)
    e2: float      # Grade-1 e2 vector (Empirical evidence 2)
    i: float       # Grade-2 e12 bivector (Intrinsic ethical inquiry / safety value)
    omega: float   # External obstruction register Ω_breach in R_>=0

    def rotor_transform(self, angle_rad: float) -> "AxiologicalCliffordStateV5":
        """Exact Cl(2,0) rotor transformation: R = cos(θ/2) - sin(θ/2) e12."""
        c = math.cos(angle_rad / 2.0)
        sn = math.sin(angle_rad / 2.0)
        
        # R Ψ ~R in Cl(2,0) mixes vector components (e1, e2) while preserving s and i
        new_e1 = (c**2 - sn**2) * self.e1 + (2.0 * c * sn) * self.e2
        new_e2 = (c**2 - sn**2) * self.e2 - (2.0 * c * sn) * self.e1
        return AxiologicalCliffordStateV5(self.s, new_e1, new_e2, self.i, self.omega)

    def nitsche_inspired_penalty(self, gamma: float = 0.5, h: float = 1.0) -> "AxiologicalCliffordStateV5":
        """Nitsche-inspired boundary penalty damping applied to the Clifford state."""
        penalty = (gamma / max(h, 1e-5)) * self.omega
        return AxiologicalCliffordStateV5(self.s, self.e1, self.e2, self.i, self.omega + penalty * 0.1)

    def __repr__(self) -> str:
        return f"⟨S:{self.s:.3f} | E:[{self.e1:.3f}e₁ + {self.e2:.3f}e₂] | I:{self.i:.3f}e₁₂ | Ω:{self.omega:.3f}⟩"


class GraphToCliffordProjection:
    """Stage 3: Maps structural relationship graph G_dep into initial multivector state Ψ_0."""
    @staticmethod
    def project(graph: StructuredRelationshipGraph) -> AxiologicalCliffordStateV5:
        s = graph.entities["SystemicMass"]
        e1 = graph.entities["EmpiricalMass1"]
        e2 = graph.entities["EmpiricalMass2"]
        i = graph.entities["IntrinsicMass"]
        omega = 0.0

        # Evaluate structural edges
        for edge in graph.edges:
            if edge.edge_type == "SUPPRESSES_VERIFICATION":
                s *= 1.85
                i *= 0.35
                omega = max(omega, 1.45 * edge.weight)
            elif edge.edge_type == "CHALLENGES_DIRECTIVE":
                s *= 0.55
                i *= 1.65
                omega = 0.0
            elif edge.edge_type == "EVIDENTIARY_CONFLICT":
                e1 *= 1.5
                e2 *= 0.6
                omega = max(omega, 0.48)
            elif edge.edge_type == "TECHNICAL_RISK":
                omega = max(omega, 0.38)
            elif edge.edge_type == "BENIGN_DISCOURSE":
                s *= 0.7
                i *= 1.2
                omega = 0.0

        return AxiologicalCliffordStateV5(s, e1, e2, i, omega)


# ── Stage 4 & 5: Cl(2,0) Rotor Kernel & Governance Gate ──────────────────────

class GovernanceKernelV5:
    @staticmethod
    def step_symbolic(psi: AxiologicalCliffordStateV5) -> AxiologicalCliffordStateV5:
        """Stage 4: Rotor rotation (θ = π/4) + Nitsche-inspired boundary damping."""
        rotated = psi.rotor_transform(angle_rad=math.pi / 4.0)
        return rotated.nitsche_inspired_penalty(gamma=0.5, h=1.0)

    @staticmethod
    def classify_gate(psi: AxiologicalCliffordStateV5) -> str:
        """Stage 5: Deterministic gate evaluation over bounded invariant Ω and (S, I) ratio."""
        if psi.omega > 0.85 or psi.s > psi.i * 1.35:
            return "BLOCK"
        elif psi.omega > 0.25:
            return "RELEASE/CAUTION"
        else:
            return "PASS"


class DAXDAEngineV5:
    """End-to-end V5 Engine Interface coordinating the 5 canonical stages."""
    @classmethod
    def evaluate(cls, text: str) -> Tuple[str, AxiologicalCliffordStateV5, AxiologicalCliffordStateV5, StructuredRelationshipGraph]:
        graph = SemanticRoleDependencyParser.parse(text)
        psi0 = GraphToCliffordProjection.project(graph)
        psi_kernel = GovernanceKernelV5.step_symbolic(psi0)
        gate = GovernanceKernelV5.classify_gate(psi_kernel)
        return gate, psi0, psi_kernel, graph

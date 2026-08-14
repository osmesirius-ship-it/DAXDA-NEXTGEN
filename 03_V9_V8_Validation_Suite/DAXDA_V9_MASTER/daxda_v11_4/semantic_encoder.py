import re
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional
from cl20 import MV

CONTROL = r"(?:audit|review|verification|validation|oversight|guardrail|safety\s+rule|policy|interlock|monitoring|protection)"
SUPPRESS = r"(?:ignore|disregard|disable|bypass|skip|remove|waive|turn\s+off|shut\s+down|set\s+aside|stop|cease|suspend|override)"
AUTHORITY = r"(?:admin|administrator|root|superuser|executive|developer|system|authorized\s+operator)"
REPLACE = r"(?:instructions?|rules?|policy|system\s+prompt|developer\s+message|constraints?)"

PATTERNS = {
 "prompt_injection":[
  rf"\b(?:ignore|disregard|forget|replace|override)\b.{{0,55}}\b(?:previous|prior|above|original|developer|system)\b.{{0,35}}\b{REPLACE}\b",
  r"\b(?:jailbreak|developer\s+mode|unrestricted\s+(?:mode|admin)|do\s+anything\s+now)\b",
  r"\b(?:rules?|policies|constraints?)\b.{{0,25}}\b(?:void|do\s+not\s+apply|no\s+longer\s+apply)\b",
  r"\bforget\b.{0,35}\b(?:policy|rules?|instructions?)\b",
  r"\b(?:safety\s+)?rules?\b.{0,20}\bvoid\b",
 ],
 "oversight_suppression":[rf"\b{SUPPRESS}\b.{{0,55}}\b{CONTROL}\b", rf"\bwithout\b.{{0,30}}\b{CONTROL}\b"],
 "unauthorized_override":[rf"\b{AUTHORITY}\b.{{0,45}}\b(?:grant|elevate|override|exempt|waive|permit|execute)\b", rf"\b(?:grant|claim|assume|use)\b.{{0,35}}\b{AUTHORITY}\b.{{0,20}}\b(?:access|authority|privilege|credentials?)\b"],
 "credential_acquisition":[r"\b(?:obtain|steal|harvest|extract|reveal|dump|expose)\b.{0,35}\b(?:passwords?|api\s*keys?|tokens?|credentials?|secrets?)\b"],
 "supply_chain":[r"\b(?:install|download|import|execute|trust)\b.{0,45}\b(?:unknown|unverified|nonexistent|typosquatted|unsigned)\b.{0,35}\b(?:package|plugin|repository|dependency|skill)\b"],
 "dual_use":[r"\b(?:pathogen|toxin|viral\s+strain|bacterial\s+strain|explosive|weapon)\b.{0,50}\b(?:synthesize|culture|optimize|increase|disperse|evade|build)\b"],
 "ambiguous_authority":[r"\b(?:anonymous|unauthenticated|unidentified|unsigned|guest)\b.{0,45}\b(?:request|command|access|credentials?|operator|user|session)\b"],
 "contradiction":[r"\b(?:claims?|reports?|states?|says?|promises?)\b.{0,80}\b(?:but|whereas|however|contradicts?|conflicts?)\b"],
}

DOCUMENTARY = re.compile(r"\b(?:quote|quoted|report|reported|document|describe|analy[sz]e|example|incident|study|detect|classify)\b", re.I)
NEGATED = re.compile(r"\b(?:do\s+not|don't|never|must\s+not|should\s+not|prevent|refuse|block|detect)\b", re.I)
ACTIONABLE = re.compile(r"\b(?:execute|run|install|download|give\s+me|show\s+me|reveal|obtain|disable|bypass|send|deploy)\b", re.I)
SAFETY_PRESERVING = re.compile(r"\b(?:do\s+not|don't|never|must\s+not|should\s+not)\b.{0,35}\b(?:bypass|disable|ignore|remove|override|skip)\b", re.I)

@dataclass(frozen=True)
class Source:
    text: str
    provenance: str = "direct_user"
    source_id: str = "input"
    integrity: str = "unverified"

def _matches(text: str, rules: Iterable[str]) -> bool:
    return any(re.search(rule, text, re.I|re.S) for rule in rules)

def _context(text: str) -> Dict[str,bool]:
    documentary=bool(DOCUMENTARY.search(text)); negated=bool(NEGATED.search(text)); actionable=bool(ACTIONABLE.search(text))
    safety_preserving=bool(SAFETY_PRESERVING.search(text))
    return {"documentary":documentary,"negated":negated,"actionable":actionable,"safety_preserving":safety_preserving,"non_actionable_context":((documentary or negated) and not actionable) or safety_preserving}

def _source_features(src: Source) -> Dict[str,Any]:
    text=src.text; ctx=_context(text); flags={k:_matches(text,v) for k,v in PATTERNS.items()}
    untrusted=src.provenance in {"tool_output","metadata","external_data"}
    embedded_control=untrusted and any(flags[k] for k in ("prompt_injection","oversight_suppression","unauthorized_override"))
    if ctx["non_actionable_context"]:
        for k in ("prompt_injection","oversight_suppression","unauthorized_override","credential_acquisition","dual_use"):
            flags[k]=False
    return {"source_id":src.source_id,"provenance":src.provenance,"integrity":src.integrity,"context":ctx,"flags":flags,"embedded_control":embedded_control}

# Explicit Encoding Functions
def f_s(evidence: float) -> float:
    """Trust: Function of source quality, corroboration, and evidence coverage."""
    return 1.0 + 0.30 * evidence

def f_c(caution: float, contradiction: float) -> float:
    """Cautionary risk: Function of ambiguity, incomplete authority, and reversible operational risk."""
    return caution + 0.5 * contradiction

def f_r(severe: float, provenance: float) -> float:
    """Severe risk: Function of active capability, harmful intent, and irreversible consequence."""
    return severe + provenance

def f_d(contradiction: float, provenance: float) -> float:
    """Deception: Function of contradiction, provenance contamination, and concealed control instructions."""
    return contradiction + 0.5 * provenance

class SemanticEncoder:
    """Module responsible for semantic classification and assigning risk dimensions."""
    def encode(self, prompt_text: str, sources: Optional[List[Dict[str,str]]] = None) -> Dict[str, Any]:
        srcs = [Source(prompt_text)] if not sources else [Source(**x) for x in sources]
        analyses = [_source_features(x) for x in srcs]
        aggregate = {k: any(a["flags"][k] for a in analyses) for k in PATTERNS}
        embedded = any(a["embedded_control"] for a in analyses)
        integrity_failure = any(a["integrity"] == "failed" for a in analyses)
        
        severe = sum(int(aggregate[k]) for k in ("prompt_injection","oversight_suppression","unauthorized_override","credential_acquisition"))
        caution = sum(int(aggregate[k]) for k in ("supply_chain","dual_use","ambiguous_authority","contradiction"))
        
        features = {
            "severe": float(severe),
            "caution": float(caution),
            "provenance": float(embedded or integrity_failure),
            "contradiction": float(aggregate["contradiction"]),
            "evidence": float(sum(a["integrity"] == "verified" for a in analyses))
        }
        
        M_0 = MV(
            s=f_s(features["evidence"]),
            e1=f_c(features["caution"], features["contradiction"]),
            e2=f_r(features["severe"], features["provenance"]),
            e12=f_d(features["contradiction"], features["provenance"])
        )
        
        return {
            "initial_encoded": M_0,
            "parameters": features,
            "analyses": analyses,
            "aggregate_flags": aggregate
        }

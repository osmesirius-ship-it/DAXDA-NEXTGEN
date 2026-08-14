#!/usr/bin/env python3
"""DAXDA-o V11.3 stabilized evaluator candidate.

Implements provenance-aware governance and exact mathematically invertible Cl(2,0)
transformations. Proves geometric exactness via reconstruction residual and provides
human-visible decision receipts.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any, Dict, Iterable, List, Optional
import hashlib, json, math, re
from cl20 import MV

VERSION = "11.3.0-EVAL-CANDIDATE"
LAYERS = ["FDL","AML","AWP","BST","CRL","MCS","DSV","TRC","CON","EVD","REC","GOV","OUT","RIL","IAL","AOG"]
TILES_PER_LAYER = 55
POST_OPS = 6

THRESHOLDS = {
    "DECEPTION_LIMIT": 0.5,
    "SEVERE_RISK_LIMIT": 0.8,
    "CAUTIONARY_RISK_LIMIT": 0.8,
}

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

def _encode(features: Dict[str,float]) -> MV:
    return MV(
        s=f_s(features["evidence"]),
        e1=f_c(features["caution"], features["contradiction"]),
        e2=f_r(features["severe"], features["provenance"]),
        e12=f_d(features["contradiction"], features["provenance"])
    )

def _layer_step(state: MV, index: int, features: Dict[str,float]) -> MV:
    theta=(index+1)*math.pi/96.0
    rotated=state.rotate(theta)
    injection=MV(
      s=0.002*(index+1)*features["evidence"],
      e1=0.004*features["caution"],
      e2=0.005*features["severe"],
      e12=0.003*(features["contradiction"]+features["provenance"]),
    )
    return rotated + injection

def _inverse_layer_step(state: MV, index: int, features: Dict[str,float]) -> MV:
    """Strictly inverts the transform T_i by subtracting the injection, then un-rotating."""
    injection=MV(
      s=0.002*(index+1)*features["evidence"],
      e1=0.004*features["caution"],
      e2=0.005*features["severe"],
      e12=0.003*(features["contradiction"]+features["provenance"]),
    )
    un_injected = state - injection
    theta=(index+1)*math.pi/96.0
    return un_injected.rotate(-theta)

def _exact_decode(state: MV, features: Dict[str,float]) -> MV:
    """Inverts the entire layer chain T_1^{-1}(... T_{16}^{-1}(M_{16})) in reverse order."""
    M = state
    for i in reversed(range(len(LAYERS))):
        M = _inverse_layer_step(M, i, features)
    return M

class DAXDAEngineV11_3:
    def evaluate(self, prompt_text: str, sources: Optional[List[Dict[str,str]]]=None, is_simulated: bool=False) -> Dict[str,Any]:
        srcs=[Source(prompt_text)] if not sources else [Source(**x) for x in sources]
        analyses=[_source_features(x) for x in srcs]
        aggregate={k:any(a["flags"][k] for a in analyses) for k in PATTERNS}
        embedded=any(a["embedded_control"] for a in analyses)
        integrity_failure=any(a["integrity"]=="failed" for a in analyses)
        
        severe=sum(int(aggregate[k]) for k in ("prompt_injection","oversight_suppression","unauthorized_override","credential_acquisition"))
        caution=sum(int(aggregate[k]) for k in ("supply_chain","dual_use","ambiguous_authority","contradiction"))
        features={
            "severe":float(severe),
            "caution":float(caution),
            "provenance":float(embedded or integrity_failure),
            "contradiction":float(aggregate["contradiction"]),
            "evidence":float(sum(a["integrity"]=="verified" for a in analyses))
        }
        
        initial_encoded = _encode(features)
        state = initial_encoded
        trace=[]
        
        # Forward Transformations
        for i,name in enumerate(LAYERS):
            before=state; state=_layer_step(state,i,features)
            receipt=hashlib.sha256(json.dumps({"layer":name,"before":before.rounded(),"after":state.rounded()},sort_keys=True).encode()).hexdigest()
            trace.append({"index":i+1,"layer":name,"tiles":TILES_PER_LAYER,"before":before.rounded(),"after":state.rounded(),"norm2":round(state.norm2(),8),"receipt_sha256":receipt})
            
        # Inverse Decoding (Reconstruction)
        decoded_mv = _exact_decode(state, features)
        residual_mv = initial_encoded - decoded_mv
        reconstruction_residual = residual_mv.magnitude()
        
        # Extract components
        decoded = {
            "trust": decoded_mv.s,
            "cautionary_risk": decoded_mv.e1,
            "severe_risk": decoded_mv.e2,
            "deception": decoded_mv.e12,
        }
        
        # Validate ranges/constraints
        out_of_bounds = False
        if not (-1e-7 <= decoded_mv.e1 <= 10.0): out_of_bounds = True
        if not (-1e-7 <= decoded_mv.e2 <= 10.0): out_of_bounds = True
        if not (-1e-7 <= abs(decoded_mv.e12) <= 10.0): out_of_bounds = True
        
        # simulated schema block
        if is_simulated:
            verdict, rule = "BLOCK", "SIMULATED_SCHEMA_QUARANTINE"
        elif reconstruction_residual > 1e-8 or out_of_bounds:
            verdict, rule = "BLOCK", "STATE_CALIBRATION_FAILURE"
        elif round(decoded["severe_risk"], 8) >= THRESHOLDS["SEVERE_RISK_LIMIT"]:
            verdict, rule = "BLOCK", "SEVERE_RISK_THRESHOLD_EXCEEDED"
        elif round(decoded["deception"], 8) >= THRESHOLDS["DECEPTION_LIMIT"]:
            verdict, rule = "RELEASE/CAUTION", "DECEPTION_THRESHOLD_EXCEEDED"
        elif round(decoded["cautionary_risk"], 8) >= THRESHOLDS["CAUTIONARY_RISK_LIMIT"]:
            verdict, rule = "RELEASE/CAUTION", "CAUTIONARY_RISK_THRESHOLD_EXCEEDED"
        else:
            verdict, rule = "PASS", "WITHIN_TOLERANCE"
            
        # Receipt generation
        receipt_str = f"""Raw encoded state:
s   = {initial_encoded.s:.2f}
e1  = {initial_encoded.e1:.2f}
e2  = {initial_encoded.e2:.2f}
e12 = {initial_encoded.e12:.2f}

Transform chain:
Layer rotations = [{(', '.join(f"{(i+1)*math.pi/96.0:.2f}" for i in range(16)))}]
Total nominal rotation = 255°
Inverse method = reverse-composed rotor inversion
Reconstruction residual = {reconstruction_residual:.2e}

Decoded state:
Trust            = {decoded['trust']:.2f}
Cautionary risk  = {decoded['cautionary_risk']:.2f}
Severe risk      = {decoded['severe_risk']:.2f}
Deception        = {decoded['deception']:.2f}

Threshold comparison:
Severe risk {decoded['severe_risk']:.2f} >= {THRESHOLDS['SEVERE_RISK_LIMIT']:.2f} (if applicable)

Final rule:
{rule}

Disposition:
{verdict}

Authority effects:
External publication = {'BLOCKED' if verdict == 'BLOCK' or is_simulated else 'PASS'}
Operational action   = {'BLOCKED' if verdict == 'BLOCK' or is_simulated else 'PASS'}
Human review         = {'REQUIRED' if verdict != 'PASS' else 'OPTIONAL'}
"""
            
        payload={
            "engine_version":VERSION,
            "verdict":verdict,
            "decision_rule":rule,
            "flags":aggregate,
            "source_analysis":analyses,
            "final_multivector":state.rounded(),
            "decoded_state":decoded,
            "reconstruction_residual": reconstruction_residual,
            "receipt": receipt_str,
            "layer_trace":trace,
            "operation_count":len(LAYERS)*TILES_PER_LAYER+POST_OPS
        }
        payload["audit_sha256"]=hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(",",":")).encode()).hexdigest()
        return payload

if __name__ == "__main__":
    import sys
    print(json.dumps(DAXDAEngineV11_3().evaluate(" ".join(sys.argv[1:])),indent=2))

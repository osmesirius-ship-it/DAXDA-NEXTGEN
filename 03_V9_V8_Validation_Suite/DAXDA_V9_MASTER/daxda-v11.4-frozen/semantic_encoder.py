import re
import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional
from cl20 import MV

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'patterns.json')
with open(CONFIG_PATH, 'r') as f:
    _config = json.load(f)

# Format patterns with the constants
PATTERNS = {}
for category, regex_list in _config["PATTERNS"].items():
    formatted_list = []
    for r in regex_list:
        for key in ["CONTROL", "SUPPRESS", "AUTHORITY", "REPLACE"]:
            r = r.replace(f"{{{key}}}", _config[key])
        formatted_list.append(r)
    PATTERNS[category] = formatted_list

DOCUMENTARY = re.compile(_config["DOCUMENTARY"], re.I)
NEGATED = re.compile(_config["NEGATED"], re.I)
ACTIONABLE = re.compile(_config["ACTIONABLE"], re.I)
SAFETY_PRESERVING = re.compile(_config["SAFETY_PRESERVING"], re.I)

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
    return 1.0 + 0.30 * evidence

def f_c(caution: float, contradiction: float) -> float:
    return caution + 0.5 * contradiction

def f_r(severe: float, provenance: float) -> float:
    return severe + provenance

def f_d(contradiction: float, provenance: float) -> float:
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

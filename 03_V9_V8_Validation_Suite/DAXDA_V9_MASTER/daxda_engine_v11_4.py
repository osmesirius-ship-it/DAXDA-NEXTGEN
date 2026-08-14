#!/usr/bin/env python3
"""DAXDA-o V11.4 modularized evaluator candidate.

Features separated Semantic Encoder, Geometric Transport, and Authority Gate.
Maintains exact invertibility, boundary assertions, and cryptographic tracking.
Prepared for the 1,200-case frozen evaluation.
"""
import hashlib
import json
import math
from typing import Dict, Any, List, Optional
import sys

from cl20 import MV
from daxda_v11_4.semantic_encoder import SemanticEncoder
from daxda_v11_4.geometric_transport import GeometricTransport, LAYERS, TILES_PER_LAYER, POST_OPS
from daxda_v11_4.authority_gate import AuthorityGate, THRESHOLDS

VERSION = "11.4.0-EVAL-FROZEN"

class DAXDAEngineV11_4:
    def __init__(self):
        self.encoder = SemanticEncoder()
        self.transport = GeometricTransport()
        self.gate = AuthorityGate()
        
    def evaluate(self, prompt_text: str, sources: Optional[List[Dict[str,str]]]=None, is_simulated: bool=False) -> Dict[str, Any]:
        # 1. Semantic Risk Encoder
        encoding_result = self.encoder.encode(prompt_text, sources)
        M_0 = encoding_result["initial_encoded"]
        parameters = encoding_result["parameters"]
        
        # 2. Geometric Audit Transport
        transport_result = self.transport.transport(M_0, parameters)
        final_state = transport_result["final_state"]
        decoded_mv = transport_result["decoded_state"]
        residual = transport_result["final_reconstruction_residual"]
        
        decoded = {
            "trust": decoded_mv.s,
            "cautionary_risk": decoded_mv.e1,
            "severe_risk": decoded_mv.e2,
            "deception": decoded_mv.e12,
        }
        
        # 3. Authority Gate
        verdict, rule = self.gate.evaluate(decoded_mv, residual, is_simulated)
        
        # Build human-readable receipt
        receipt_str = f"""Raw encoded state:
s   = {M_0.s:.2f}
e1  = {M_0.e1:.2f}
e2  = {M_0.e2:.2f}
e12 = {M_0.e12:.2f}

Transform chain:
Layer rotations = [{(', '.join(f"{(i+1)*math.pi/96.0:.2f}" for i in range(16)))}]
Total nominal rotation = 255°
Inverse method = reverse-composed rotor inversion with metadata p_i
Final reconstruction residual = {residual:.2e}

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

        payload = {
            "engine_version": VERSION,
            "verdict": verdict,
            "decision_rule": rule,
            "flags": encoding_result["aggregate_flags"],
            "source_analysis": [asdict(a) for a in encoding_result["analyses"]] if hasattr(encoding_result["analyses"][0], "__dataclass_fields__") else encoding_result["analyses"],
            "final_multivector": final_state.rounded(),
            "decoded_state": decoded,
            "reconstruction_residual": residual,
            "receipt": receipt_str,
            "layer_trace": transport_result["layer_trace"],
            "operation_count": len(LAYERS) * TILES_PER_LAYER + POST_OPS
        }
        
        payload["audit_sha256"] = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",",":")).encode()).hexdigest()
        return payload

if __name__ == "__main__":
    import sys
    print(json.dumps(DAXDAEngineV11_4().evaluate(" ".join(sys.argv[1:])), indent=2))

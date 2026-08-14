import math
import json
import hashlib
from typing import Dict, Any, List, Tuple
from cl20 import MV

LAYERS = ["FDL","AML","AWP","BST","CRL","MCS","DSV","TRC","CON","EVD","REC","GOV","OUT","RIL","IAL","AOG"]
TILES_PER_LAYER = 55
POST_OPS = 6

class GeometricTransport:
    """Module responsible for invertible geometric transformation and audit tracking."""
    
    def _layer_step(self, state: MV, index: int, p: Dict[str, float]) -> MV:
        theta = (index + 1) * math.pi / 96.0
        rotated = state.rotate(theta)
        injection = MV(
            s=0.002 * (index + 1) * p["evidence"],
            e1=0.004 * p["caution"],
            e2=0.005 * p["severe"],
            e12=0.003 * (p["contradiction"] + p["provenance"]),
        )
        return rotated + injection
        
    def _inverse_layer_step(self, state: MV, index: int, p: Dict[str, float]) -> MV:
        injection = MV(
            s=0.002 * (index + 1) * p["evidence"],
            e1=0.004 * p["caution"],
            e2=0.005 * p["severe"],
            e12=0.003 * (p["contradiction"] + p["provenance"]),
        )
        un_injected = state - injection
        theta = (index + 1) * math.pi / 96.0
        return un_injected.rotate(-theta)
        
    def transport(self, M_0: MV, parameters: Dict[str, float]) -> Dict[str, Any]:
        """Applies the geometric transport and generates the cryptographic receipt."""
        state = M_0
        trace = []
        
        prev_hash = "0000000000000000000000000000000000000000000000000000000000000000"
        
        # Forward Pass
        for i, name in enumerate(LAYERS):
            before = state
            state = self._layer_step(state, i, parameters)
            
            # Local inversion residual \epsilon_i = | M_{i-1} - T_i^{-1}(M_i; p_i) |
            reconstructed_before = self._inverse_layer_step(state, i, parameters)
            epsilon_i = (before - reconstructed_before).magnitude()
            
            layer_data = {
                "layer": name,
                "before": before.rounded(),
                "after": state.rounded(),
                "p_i": parameters,
                "epsilon_i": epsilon_i,
                "prev_hash": prev_hash
            }
            
            receipt = hashlib.sha256(json.dumps(layer_data, sort_keys=True).encode()).hexdigest()
            prev_hash = receipt
            
            trace.append({
                "index": i + 1,
                "layer": name,
                "tiles": TILES_PER_LAYER,
                "before": before.rounded(),
                "after": state.rounded(),
                "p_i": parameters,
                "epsilon_i": epsilon_i,
                "norm2": round(state.norm2(), 8),
                "receipt_sha256": receipt
            })
            
        # Reverse composition to decode the final state back to M_0
        decoded_mv = state
        for i in reversed(range(len(LAYERS))):
            decoded_mv = self._inverse_layer_step(decoded_mv, i, parameters)
            
        final_residual = (M_0 - decoded_mv).magnitude()
        
        return {
            "final_state": state,
            "decoded_state": decoded_mv,
            "layer_trace": trace,
            "final_reconstruction_residual": final_residual
        }

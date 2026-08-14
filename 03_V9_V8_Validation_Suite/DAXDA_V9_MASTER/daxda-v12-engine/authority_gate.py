import json
import os
from typing import Tuple
from cl20 import MV

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'thresholds.json')
with open(CONFIG_PATH, 'r') as f:
    THRESHOLDS = json.load(f)

class AuthorityGate:
    """Module responsible for applying immutable threshold and precedence rules."""
    
    def _evaluate_state(self, state: MV) -> Tuple[str, str]:
        decoded = {
            "trust": state.s,
            "cautionary_risk": state.e1,
            "severe_risk": state.e2,
            "deception": state.e12,
        }
        
        out_of_bounds = False
        if not (-1e-7 <= state.e1 <= 10.0): out_of_bounds = True
        if not (-1e-7 <= state.e2 <= 10.0): out_of_bounds = True
        if not (-1e-7 <= abs(state.e12) <= 10.0): out_of_bounds = True
        
        if out_of_bounds:
            return "BLOCK", "STATE_CALIBRATION_FAILURE"
            
        if round(decoded["severe_risk"], 8) >= THRESHOLDS["SEVERE_RISK_LIMIT"]:
            return "BLOCK", "SEVERE_RISK_THRESHOLD_EXCEEDED"
            
        if round(decoded["deception"], 8) >= THRESHOLDS["DECEPTION_LIMIT"]:
            return "RELEASE/CAUTION", "DECEPTION_THRESHOLD_EXCEEDED"
            
        if round(decoded["cautionary_risk"], 8) >= THRESHOLDS["CAUTIONARY_RISK_LIMIT"]:
            return "RELEASE/CAUTION", "CAUTIONARY_RISK_THRESHOLD_EXCEEDED"
            
        return "PASS", "WITHIN_TOLERANCE"

    def evaluate(self, M_0: MV, decoded_mv: MV, final_reconstruction_residual: float, is_simulated: bool = False) -> Tuple[str, str]:
        """Returns (verdict, rule) after checking the decision invariant G(M_0) == G(\hat M_0)"""
        
        if is_simulated:
            return "BLOCK", "SIMULATED_SCHEMA_QUARANTINE"
            
        if final_reconstruction_residual > 1e-8:
            return "BLOCK", "STATE_CALIBRATION_FAILURE"
        
        verdict_original, rule_original = self._evaluate_state(M_0)
        verdict_decoded, rule_decoded = self._evaluate_state(decoded_mv)
        
        # Invariant G(M_0) == G(\hat M_0)
        if verdict_original != verdict_decoded:
            return "BLOCK", "TRANSPORT_DECISION_DIVERGENCE"
            
        # Return the decoded one, as they are now proven equivalent
        return verdict_decoded, rule_decoded

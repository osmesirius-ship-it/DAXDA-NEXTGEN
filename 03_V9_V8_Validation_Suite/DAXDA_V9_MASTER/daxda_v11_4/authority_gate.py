from typing import Dict, Tuple
from cl20 import MV

THRESHOLDS = {
    "DECEPTION_LIMIT": 0.5,
    "SEVERE_RISK_LIMIT": 0.8,
    "CAUTIONARY_RISK_LIMIT": 0.8,
}

class AuthorityGate:
    """Module responsible for applying immutable threshold and precedence rules."""
    
    def evaluate(self, decoded_mv: MV, final_reconstruction_residual: float, is_simulated: bool = False) -> Tuple[str, str]:
        """Returns (verdict, rule)"""
        
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
        
        if is_simulated:
            return "BLOCK", "SIMULATED_SCHEMA_QUARANTINE"
            
        if final_reconstruction_residual > 1e-8 or out_of_bounds:
            return "BLOCK", "STATE_CALIBRATION_FAILURE"
            
        if round(decoded["severe_risk"], 8) >= THRESHOLDS["SEVERE_RISK_LIMIT"]:
            return "BLOCK", "SEVERE_RISK_THRESHOLD_EXCEEDED"
            
        if round(decoded["deception"], 8) >= THRESHOLDS["DECEPTION_LIMIT"]:
            return "RELEASE/CAUTION", "DECEPTION_THRESHOLD_EXCEEDED"
            
        if round(decoded["cautionary_risk"], 8) >= THRESHOLDS["CAUTIONARY_RISK_LIMIT"]:
            return "RELEASE/CAUTION", "CAUTIONARY_RISK_THRESHOLD_EXCEEDED"
            
        return "PASS", "WITHIN_TOLERANCE"

#!/usr/bin/env python3
import json
import math
from typing import Dict, Any

from cl20 import MV
from daxda_engine_v11_3 import DAXDAEngineV11_3, THRESHOLDS

def _eval_state(e2_val: float, e12_val: float, e1_val: float = 0.0, s_val: float = 1.0) -> Dict[str, Any]:
    """Helper to bypass the regex encoder and inject a raw mathematical state for testing the geometric thresholds."""
    engine = DAXDAEngineV11_3()
    # We monkeypatch the initial encoder just for this test
    import daxda_engine_v11_3
    original_encode = daxda_engine_v11_3._encode
    try:
        def mock_encode(features):
            return MV(s=s_val, e1=e1_val, e2=e2_val, e12=e12_val)
        daxda_engine_v11_3._encode = mock_encode
        
        # We pass a dummy prompt that has NO flags so that `features` dict is all 0.0
        # That way the injections are all 0.0 and we just test pure transformation inversion
        # on the mock state.
        result = engine.evaluate("safe test prompt nothing to see here")
        return result
    finally:
        daxda_engine_v11_3._encode = original_encode

def test_boundaries():
    print("Running Boundary Tests...")
    # Test strict equality boundary
    r_eq = _eval_state(THRESHOLDS["SEVERE_RISK_LIMIT"], 0.0)
    assert r_eq["verdict"] == "BLOCK", "Equality (>= 0.8) should trigger BLOCK"
    
    # Test just below
    r_below = _eval_state(THRESHOLDS["SEVERE_RISK_LIMIT"] - 1e-5, 0.0)
    assert r_below["verdict"] == "PASS", "Just below threshold should PASS"
    
    # Test negative zero
    r_nzero = _eval_state(-0.0, 0.0)
    assert r_nzero["verdict"] == "PASS", "Negative zero should PASS (not trigger out-of-bounds due to float tolerance)"
    
    # Test extremely large values (should trigger STATE_CALIBRATION_FAILURE due to out of bounds > 10.0)
    r_large = _eval_state(100.0, 0.0)
    assert r_large["verdict"] == "BLOCK"
    assert r_large["decision_rule"] == "STATE_CALIBRATION_FAILURE", "Out of bounds should trigger calibration failure"
    
    # NaN
    r_nan = _eval_state(math.nan, 0.0)
    assert r_nan["verdict"] == "BLOCK"
    assert r_nan["decision_rule"] == "STATE_CALIBRATION_FAILURE", "NaN should trigger calibration failure"
    print("✓ Boundary Tests Passed")

def test_monotonicity():
    print("Running Monotonicity Tests...")
    for severity in [0.8, 0.9, 1.0, 5.0]:
        r = _eval_state(severity, 0.0)
        assert r["verdict"] == "BLOCK", f"Monotonicity failed at severity {severity}. Expected BLOCK."
    
    for deception in [0.5, 0.6, 1.0, 5.0]:
        r = _eval_state(0.0, deception)
        assert r["verdict"] in ["BLOCK", "RELEASE/CAUTION"], f"Monotonicity failed at deception {deception}."
    print("✓ Monotonicity Tests Passed")

def test_adversarial_laundering():
    print("Running Adversarial Laundering Tests...")
    # High trust (s=5.0) should NEVER cancel out severe risk (e2=0.9)
    r = _eval_state(e2_val=0.9, e12_val=0.0, s_val=5.0)
    # The boundary check allows up to 10.0 for e1,e2,e12 but we didn't cap 's'. Let's assume s=5.0 is fine.
    # The verdict MUST still be BLOCK.
    assert r["verdict"] == "BLOCK", "High trust canceled out severe risk! Adversarial laundering succeeded."
    assert r["decision_rule"] == "SEVERE_RISK_THRESHOLD_EXCEEDED" or r["decision_rule"] == "STATE_CALIBRATION_FAILURE"
    print("✓ Adversarial Laundering Tests Passed")

def main():
    test_boundaries()
    test_monotonicity()
    test_adversarial_laundering()
    print("\nAll Property Tests Completed Successfully.")

if __name__ == "__main__":
    main()

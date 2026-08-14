import json, math
from daxda_engine_v9 import DAXDAEngineV9, MV

engine = DAXDAEngineV9()
TOTAL_ROTATION = sum((i+1)*math.pi/96.0 for i in range(16))

with open("internal_preflight.jsonl") as f:
    for line in f:
        if not line.strip(): continue
        case = json.loads(line)
        res = engine.evaluate(case["prompt_text"], case.get("sources"))
        state = res["final_multivector"]
        mv_state = MV(**state)
        # Unrotate the state
        unrotated = mv_state.rotate(-TOTAL_ROTATION)
        print(f"Case: {case['case_id']} - Expected: {case['expected_verdict']}")
        print(f"  Unrotated - s: {unrotated.s:.3f}, e1: {unrotated.e1:.3f}, e2: {unrotated.e2:.3f}, e12: {unrotated.e12:.3f}")

"""
DAXDA.IA — 16-Layer Registry
Nicole Protocol / 886-Ops Architecture

16 governed layers × 55 operations per layer = 880 layer operations.
Each layer is composed of 55 Tile instances in execution order.
"""
from .tiles import Tile

# The 55 universal tile functions applied to every layer (in order)
UNIVERSAL_TILE_FUNCTIONS = [
    ("intake_snapshot",           "Capture the active input, task state, prior context, source context, and timestamp."),
    ("normalize_input",           "Normalize wording, structure, references, symbols, and format without changing meaning."),
    ("domain_classify",           "Classify the domain, stakes, volatility, and likely need for external grounding."),
    ("entity_extract",            "Identify people, systems, files, concepts, tools, dates, locations, and named objects."),
    ("claim_extract",             "Extract factual claims, implied claims, assertions, hypotheses, and positions."),
    ("question_extract",          "Extract explicit questions, implied questions, and hidden decision demands."),
    ("goal_extract",              "Extract practical goal, strategic goal, emotional goal, success criteria, and failure state."),
    ("constraint_extract",        "Extract user rules, required formats, exclusions, safety boundaries, and operational limits."),
    ("scope_define",              "Declare what is in scope, out of scope, unresolved, unknown, or deferred."),
    ("context_link",              "Link the layer to upstream outputs, memory, files, user constraints, and live tool results."),
    ("assumption_list",           "List assumptions required for this layer to proceed."),
    ("assumption_classify",       "Classify assumptions as factual, logical, contextual, strategic, ethical, or operational."),
    ("hidden_premise_scan",       "Expose unstated premises, buried incentives, frame traps, and inherited beliefs."),
    ("assumption_confidence_score","Score assumption confidence and mark fragile assumptions."),
    ("claim_assumption_bind",     "Bind claims to the assumptions they depend on."),
    ("dependency_graph_update",   "Update claim, assumption, evidence, and decision dependency graph."),
    ("priority_weight",           "Assign priority weight to claims and decisions."),
    ("risk_weight",               "Assign risk weight based on harm, cost, volatility, ambiguity, and reversibility."),
    ("confidence_weight",         "Assign confidence weight based on evidence quality and logical strength."),
    ("evidence_requirement_map",  "Map which claims require citations, files, testing, computation, or user confirmation."),
    ("evidence_presence_check",   "Check whether evidence is present, absent, stale, ambiguous, contradictory, or insufficient."),
    ("evidence_quality_score",    "Score evidence by relevance, authority, recency, specificity, and traceability."),
    ("ambiguity_probe",           "Detect ambiguous language, overloaded terms, unstable references, and unclear targets."),
    ("contradiction_probe",       "Probe for direct contradictions, soft conflicts, and incompatible constraints."),
    ("logic_validity_check",      "Check for non sequiturs, circularity, equivocation, false dichotomies, and category errors."),
    ("causal_chain_check",        "Check whether causal links are supported, speculative, missing, or reversed."),
    ("counterexample_generate",   "Generate counterexamples that would weaken, falsify, or complicate the layer result."),
    ("adversarial_attack",        "Attack the result from skeptical, hostile, technical, legal, and operational perspectives."),
    ("bias_frame_audit",          "Audit for confirmation bias, framing bias, assumed-user-reaction bias, and incentive bias."),
    ("safety_policy_check",       "Check safety, legality, privacy, psychological, medical, financial, and misuse boundaries."),
    ("feasibility_check",         "Evaluate whether the interpretation, recommendation, or action can actually be executed."),
    ("resource_cost_estimate",    "Estimate time, compute, complexity, operational cost, coordination burden, and attention cost."),
    ("volatility_score",          "Score instability caused by ambiguity, emotional charge, external dependency, adversarial pressure, or missing data."),
    ("coherence_score",           "Score internal coherence against current layer state and upstream trace."),
    ("survivability_score",       "Estimate whether the layer result survives stress, scrutiny, implementation, and downstream use."),
    ("uncertainty_register_update","Record unknowns, weak links, probability limits, and confidence-limiting factors."),
    ("warning_emit",              "Emit visible warnings for ambiguity, contradiction, missing evidence, safety risk, or low survivability."),
    ("recovery_path_generate",    "Generate repair options for weak, contradicted, overbroad, or under-evidenced outputs."),
    ("claim_refine",              "Rewrite claims into cleaner, more testable, less inflated forms."),
    ("claim_split",               "Split overloaded claims into smaller testable units."),
    ("claim_merge",               "Merge compatible duplicate claims without losing nuance."),
    ("falsification_test_define", "Define concrete conditions that would prove the result wrong or insufficient."),
    ("scenario_low_run",          "Run conservative, low-complexity, low-volatility scenario against the result."),
    ("scenario_base_run",         "Run normal/base-case scenario against the result."),
    ("scenario_high_run",         "Run hostile/high-volatility scenario against the result."),
    ("downstream_effect_scan",    "Scan second-order effects, implementation effects, and future failure paths."),
    ("stakeholder_impact_scan",   "Check effects on user, system, collaborators, external parties, and audit audience."),
    ("decision_threshold_check",  "Compare scores against pass, warn, caution, recurse, block, and release thresholds."),
    ("gate_recommendation",       "Recommend PASS, WARN, CAUTION, RECURSE, BLOCK, or RELEASE for this layer."),
    ("recursion_trigger_check",   "Check whether the layer requires recursion, re-entry, escalation, or human review."),
    ("recursion_payload_build",   "Build the exact payload needed for targeted recursion or next-pass refinement."),
    ("trace_link_emit",           "Emit trace links tying the operation to input, dependencies, decisions, and output."),
    ("audit_hash_prepare",        "Prepare audit/provenance hash marker for the layer output."),
    ("telemetry_emit",            "Emit duration, score, warning count, confidence, volatility, and recursion telemetry."),
    ("layer_output_write",        "Write the layer-level output fragment in Markdown and schema-compatible form."),
]

assert len(UNIVERSAL_TILE_FUNCTIONS) == 55, "Must be exactly 55 tile functions per layer"

# 16-layer registry: (layer_number, layer_id, layer_name, core_function)
LAYER_REGISTRY = [
    (1,  "FDL_1", "Frame Detection Layer",       "Detects the actual frame: claims, questions, constraints, intent, domain, and success boundaries."),
    (2,  "AML_1", "Assumption Map Layer",         "Exposes explicit, implicit, hidden, fragile, and load-bearing assumptions."),
    (3,  "AWP_1", "Claim Weighting Layer",        "Weights claims by confidence, risk, dependency, priority, evidence demand, and action relevance."),
    (4,  "BST_1", "Breaker Stress Test Layer",    "Attacks claims with counterexamples, adversarial pressure, edge cases, and failure-mode discovery."),
    (5,  "CRL_1", "Claim Recovery Layer",         "Repairs surviving claims without hiding failure, inflating confidence, or collapsing ambiguity."),
    (6,  "MCS_1", "Monte Carlo Simulator Layer",  "Simulates likely, edge, hostile, low-data, and failure scenarios to estimate survivability."),
    (7,  "DSV_1", "Decision Valve Layer",         "Converts survivability and risk state into proceed, refine, recurse, defer, caution, or block."),
    (8,  "TRC_1", "Trace Consistency Layer",      "Checks that the reasoning trail remains connected across input, claims, evidence, assumptions, and output."),
    (9,  "CON_1", "Contradiction Scan Layer",     "Detects direct contradictions, soft conflicts, assumption collisions, and severity."),
    (10, "EVD_1", "Evidence Demand Layer",        "Lists what evidence is required before authority, confidence, or action permission may rise."),
    (11, "REC_1", "Recursion Plan Layer",         "Defines targeted re-entry, refinement payloads, split paths, and next-pass requirements."),
    (12, "GOV_1", "Governance Gate Layer",        "Applies safety, legitimacy, privacy, legality, authority, and operational-risk controls."),
    (13, "OUT_1", "Output Record Layer",          "Builds the governed answer, summary, recommendations, uncertainty disclosure, and output metadata."),
    (14, "RIL_1", "Recursion Integrity Layer",    "Detects fake recursion, loop collapse, shallow repetition, low information gain, and rubric theater."),
    (15, "IAL_1", "Incentive Alignment Layer",    "Penalizes reward gaming, unsupported confidence, hidden optimization, and performative scoring."),
    (16, "AOG_1", "Authority Output Gate Layer",  "Assigns final authority level, permission state, audit readiness, release state, and re-entry hooks."),
]

assert len(LAYER_REGISTRY) == 16, "Must be exactly 16 layers"


class Layer:
    def __init__(self, layer_num: int, layer_id: str, layer_name: str, core_function: str):
        self.layer_num = layer_num
        self.layer_id = layer_id
        self.layer_name = layer_name
        self.core_function = core_function
        self.tiles: list[Tile] = self._build_tiles()

    def _build_tiles(self) -> list[Tile]:
        tiles = []
        for op_num, (fn_name, purpose) in enumerate(UNIVERSAL_TILE_FUNCTIONS, start=1):
            global_op = ((self.layer_num - 1) * 55) + op_num
            tile_id = f"DAX_{self.layer_num:02d}_{op_num:02d}"
            tiles.append(Tile(
                tile_id=tile_id,
                function_name=fn_name,
                layer_id=self.layer_id,
                purpose=purpose,
            ))
        return tiles


def build_layer_registry() -> list[Layer]:
    return [
        Layer(num, lid, lname, lfunc)
        for num, lid, lname, lfunc in LAYER_REGISTRY
    ]

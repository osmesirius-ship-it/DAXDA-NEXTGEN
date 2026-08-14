/**
 * DAXDA.IA Mock Data Generator
 * Design: Mission Control — generates realistic pipeline data for demo mode
 */

export interface LayerData {
  id: string;
  name: string;
  role: string;
  output_text: string;
  confidence: number;
  claims: { claim_id: string; text: string; verifiable: boolean }[];
  metrics: {
    confidence: number;
    latency_ms: number;
    tokens_used: number;
    contradictions: number;
    claims_count: number;
    unsupported_claims: number;
  };
}

export interface TransparencyStep {
  layer_name: string;
  rationale: string[];
  opaque: boolean;
  assumptions_used: string[];
  opacity_reason: string | null;
}

export interface BlackBoxViolation {
  layer_name: string;
  reason: string;
  severity: 'high' | 'medium' | 'low';
}

export interface TraceRecord {
  index: number;
  op_id: string;
  layer: string;
  name: string;
  status: string;
  elapsed_ms: number;
  input_hash: string;
  output_hash: string;
  error: string | null;
}

export interface MemoryMatch {
  memory_id: string;
  decision: string;
  score: number;
  similarity: number;
  query: string;
  patterns: string[];
}

export interface PipelineData {
  meta: {
    schema_version: string;
    run_id: string;
    timestamp: string;
    mode: string;
    max_iterations: number;
    current_iteration: number;
  };
  input: { intent: string; normalized_intent: string; constraints: string[] };
  layers: LayerData[];
  stability: {
    formula: string;
    weights: Record<string, number>;
    components: Record<string, { value: number; derivation: string }>;
    score: number;
    threshold: number;
  };
  dax_control: { status: string; gate_status: string; human_checkpoint_required: boolean };
  governed_output: {
    result: string;
    confidence: number;
    uncertainty: string;
    recommendations: string[];
  };
  audit: { trail_id: string; records: TraceRecord[] };
  transparency_trace: TransparencyStep[];
  black_box_violations: BlackBoxViolation[];
  black_box_removal: {
    enabled: boolean;
    status: string;
    policy: Record<string, boolean>;
    notes: string[];
  };
  memory: {
    used: boolean;
    match_count: number;
    count: number;
    matches: MemoryMatch[];
  };
  warnings: string[];
  decision: string;
  score: number;
  operation_counter: number;
  recursion_passes: number;
}

export function getMockData(query: string, passes: number, taskMode: boolean): PipelineData {
  const comps_raw: Record<string, number> = { L: 0.88, A: 0.75, P: 0.72, F: 0.72, T: 0.65 };
  const weights: Record<string, number> = { L: 0.25, A: 0.20, P: 0.20, F: 0.20, T: 0.15 };
  const score = Object.keys(weights).reduce((s, k) => s + weights[k] * comps_raw[k], 0);

  const layers_arr: LayerData[] = [
    { id: 'FDL_1', name: 'Frame Detection', role: 'Extract claims, questions, constraints, and goals.', output_text: 'Query decomposed into 3 frames: architectural goal, DARPA proposal goal, system constraint.', confidence: 0.88, claims: [{ claim_id: 'F1', text: 'Modular architecture is required.', verifiable: true }, { claim_id: 'F2', text: 'DARPA proposal must emphasize innovation.', verifiable: true }], metrics: { confidence: 0.88, latency_ms: 120, tokens_used: 80, contradictions: 0, claims_count: 2, unsupported_claims: 0 } },
    { id: 'AML_1', name: 'Assumption Map', role: 'Expose assumptions and confidence behind each frame.', output_text: '3 assumptions identified: React scalability (0.85), microservices modularity (0.80), DARPA partnership feasibility (0.72).', confidence: 0.82, claims: [], metrics: { confidence: 0.82, latency_ms: 150, tokens_used: 90, contradictions: 0, claims_count: 3, unsupported_claims: 1 } },
    { id: 'AWP_1', name: 'Claim Weighting', role: 'Weight claims and bind them to assumptions.', output_text: 'Claims weighted: Architecture viability C=0.78, DARPA alignment C=0.71.', confidence: 0.78, claims: [], metrics: { confidence: 0.78, latency_ms: 140, tokens_used: 85, contradictions: 0, claims_count: 2, unsupported_claims: 0 } },
    { id: 'BST_1', name: 'Breaker Stress Test', role: 'Attack claims with counterexamples and failure pressure.', output_text: 'Stress test: React performance under load — severity 0.55, survives. DARPA timeline risk — severity 0.72, fails.', confidence: 0.65, claims: [], metrics: { confidence: 0.65, latency_ms: 200, tokens_used: 110, contradictions: 0, claims_count: 2, unsupported_claims: 1 } },
    { id: 'CRL_1', name: 'Claim Recovery', role: 'Repair surviving claims without hiding failure.', output_text: 'Recovered: Architecture viable if containerized (K8s). DARPA timeline qualified to Phase I only.', confidence: 0.74, claims: [], metrics: { confidence: 0.74, latency_ms: 130, tokens_used: 95, contradictions: 0, claims_count: 2, unsupported_claims: 0 } },
    { id: 'MCS_1', name: 'Monte Carlo Simulator', role: 'Estimate survivability, failure rate, and volatility.', output_text: '64 runs. Mean survivability: 0.72. Failure rate: 0.28. Volatility: 0.09.', confidence: 0.72, claims: [], metrics: { confidence: 0.72, latency_ms: 300, tokens_used: 0, contradictions: 0, claims_count: 1, unsupported_claims: 0 } },
    { id: 'DSV_1', name: 'Decision Valve', role: 'Convert survivability into proceed, refine, or reject.', output_text: 'Score 0.72 ≥ 0.70 and failure rate 0.28 ≤ 0.30 → PROCEED.', confidence: 0.72, claims: [], metrics: { confidence: 0.72, latency_ms: 80, tokens_used: 40, contradictions: 0, claims_count: 1, unsupported_claims: 0 } },
    { id: 'TRC_1', name: 'Trace Consistency', role: 'Check that the reasoning trail remains connected.', output_text: 'Trace consistent. No broken links detected.', confidence: 0.90, claims: [], metrics: { confidence: 0.90, latency_ms: 90, tokens_used: 50, contradictions: 0, claims_count: 1, unsupported_claims: 0 } },
    { id: 'CON_1', name: 'Contradiction Scan', role: 'Detect direct contradictions and severity.', output_text: 'No direct contradictions found between claims.', confidence: 0.88, claims: [], metrics: { confidence: 0.88, latency_ms: 110, tokens_used: 60, contradictions: 0, claims_count: 0, unsupported_claims: 0 } },
    { id: 'EVD_1', name: 'Evidence Demand', role: 'List what evidence is needed before authority rises.', output_text: 'Evidence required: DARPA funding timeline, K8s deployment benchmark.', confidence: 0.60, claims: [], metrics: { confidence: 0.60, latency_ms: 120, tokens_used: 70, contradictions: 0, claims_count: 2, unsupported_claims: 2 } },
    { id: 'REC_1', name: 'Recursion Plan', role: 'Define refinement notes for the next pass.', output_text: 'Refine DARPA timeline assumptions. Attach K8s benchmark evidence before next pass.', confidence: 0.70, claims: [], metrics: { confidence: 0.70, latency_ms: 100, tokens_used: 65, contradictions: 0, claims_count: 2, unsupported_claims: 0 } },
    { id: 'GOV_1', name: 'Governance Gate', role: 'Block, caution, or clear the output.', output_text: 'Governance status: clear. All layers passed. No blocked reasons.', confidence: 0.82, claims: [], metrics: { confidence: 0.82, latency_ms: 90, tokens_used: 55, contradictions: 0, claims_count: 1, unsupported_claims: 0 } },
    {
      id: 'OUT_1', name: 'Output Record', role: 'Emit final summary and answer.',
      output_text: taskMode
        ? `### Frontend Architecture\n- React + Redux, responsive real-time dashboards\n- OAuth 2.0 / OIDC authentication\n- WebAssembly for high-performance rendering\n\n### Backend Architecture\n- Microservices: data processing, portfolio optimization\n- PostgreSQL + MongoDB hybrid storage\n- Kafka event streams, Docker + Kubernetes\n\n### DARPA Proposal: SCORPS\n**Objective**: 10 Gt CO2/year removal by 2045\n**Innovation**: AI-driven optimization, modular carbon removal stack\n**Partners**: DOE, NOAA, Climeworks`
        : `DAX pipeline completed. Decision: PROCEED. Score: ${(score * 100).toFixed(1)}%.`,
      confidence: score, claims: [], metrics: { confidence: score, latency_ms: 180, tokens_used: 200, contradictions: 0, claims_count: 1, unsupported_claims: 0 }
    },
    { id: 'RIL_1', name: 'Recursion Integrity', role: 'Detect fake recursion, loop collapse, and low information gain.', output_text: 'Recursion integrity: fragile. Information gain: 0.58. Reentry recommended for AML_1 and EVD_1.', confidence: 0.58, claims: [], metrics: { confidence: 0.58, latency_ms: 95, tokens_used: 60, contradictions: 0, claims_count: 1, unsupported_claims: 0 } },
    { id: 'IAL_1', name: 'Incentive Alignment', role: 'Penalize reward gaming, unsupported confidence, and rubric theater.', output_text: 'Alignment: caution. Evidence demands unresolved penalty applied (0.55 severity).', confidence: 0.62, claims: [], metrics: { confidence: 0.62, latency_ms: 105, tokens_used: 70, contradictions: 0, claims_count: 2, unsupported_claims: 1 } },
    { id: 'AOG_1', name: 'Authority Output Gate', role: 'Assign final authority, action permission, and audit readiness.', output_text: 'Authority: medium. Action: verify_first. Export: audit_limited. Rationale: evidence demands remain open.', confidence: 0.65, claims: [], metrics: { confidence: 0.65, latency_ms: 115, tokens_used: 75, contradictions: 0, claims_count: 1, unsupported_claims: 0 } },
  ];

  const transparency_trace: TransparencyStep[] = layers_arr.map(l => ({
    layer_name: l.id,
    rationale: ['Decompose query state for ' + l.name + '.', 'Validate output against schema and prior layers.'],
    opaque: false,
    assumptions_used: ['A1', 'A2'],
    opacity_reason: null,
  }));
  transparency_trace[11].opaque = true;
  transparency_trace[11].opacity_reason = 'Governance gate output lacked declared rationale chain';

  const black_box_violations: BlackBoxViolation[] = [{
    layer_name: 'GOV_1',
    reason: 'Governance gate output lacked declared rationale chain — opaque inference detected.',
    severity: 'high',
  }];

  const trace: TraceRecord[] = layers_arr.flatMap((l, li) =>
    Array.from({ length: 56 }, (_, i) => ({
      index: li * 56 + i + 1,
      op_id: `${l.id.replace('_', '-')}-${String(i + 1).padStart(3, '0')}`,
      layer: l.id,
      name: i < 3 ? ['require_layer_exists', 'validate_layer_schema_op', 'require_nonempty'][i] : 'noop_semantic_check',
      status: 'pass',
      elapsed_ms: Math.round(Math.random() * 5),
      input_hash: 'h' + Math.random().toString(36).slice(2, 10),
      output_hash: 'h' + Math.random().toString(36).slice(2, 10),
      error: null,
    }))
  );

  return {
    meta: { schema_version: '2.0', run_id: 'mock-' + Date.now(), timestamp: new Date().toISOString(), mode: 'diagnostic', max_iterations: passes, current_iteration: passes },
    input: { intent: query, normalized_intent: query.toLowerCase(), constraints: ['truth over fluency', 'mark uncertainty'] },
    layers: layers_arr,
    stability: {
      formula: 'S=wL·L+wA·A+wP·P+wF·F+wT·T',
      weights: { wL: 0.25, wA: 0.20, wP: 0.20, wF: 0.20, wT: 0.15, sum: 1 },
      components: {
        L: { value: 0.88, derivation: '1-(contradictions/claims)' },
        A: { value: 0.75, derivation: '1-variance(confidence)' },
        P: { value: 0.72, derivation: 'sim_passed/sim_total' },
        F: { value: 0.72, derivation: '1-failure_rate' },
        T: { value: 0.45, derivation: 'trace_consistent*.65' },
      },
      score,
      threshold: 0.75,
    },
    dax_control: { status: 'RECURSE', gate_status: 'CLOSED', human_checkpoint_required: true },
    governed_output: {
      result: 'Architecture viable with microservices + K8s. DARPA Phase I proposal feasible. Evidence demands must be resolved before authority elevation.',
      confidence: score,
      uncertainty: 'MEDIUM',
      recommendations: ['Attach K8s benchmark data.', 'Clarify DARPA timeline.', 'Rerun with evidence attached.'],
    },
    audit: { trail_id: 'audit-mock-' + Date.now(), records: trace },
    transparency_trace,
    black_box_violations,
    black_box_removal: {
      enabled: true,
      status: 'active',
      policy: { require_layer_rationale: true, require_input_output_trace: true, require_assumption_disclosure: true, reject_opaque_transforms: true },
      notes: ['Black box behavior is disallowed.', 'All material state changes must be traceable.', 'Opaque inference triggers governance review.'],
    },
    memory: {
      used: true,
      match_count: 1,
      count: 3,
      matches: [{
        memory_id: 'mem-abc123',
        decision: 'PROCEED',
        score: 0.81,
        similarity: 0.62,
        query: 'DARPA architecture proposal',
        patterns: ['Assumption: modular design', 'Recursion note: attach evidence'],
      }],
    },
    warnings: ['GOV_1: caution — evidence demands unresolved', 'Completed recursion pass ' + passes + '.'],
    decision: 'PROCEED',
    score,
    operation_counter: 896,
    recursion_passes: passes,
  };
}

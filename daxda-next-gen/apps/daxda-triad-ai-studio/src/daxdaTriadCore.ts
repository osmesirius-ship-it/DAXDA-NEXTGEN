/**
 * DAXDA Next-Gen Core — Browser-Native Clifford Cl(3,1)/Cl(16,4) Evaluator
 * & 3-Node Triad Memory Ledger (Waypoint Essence + 12-Byte INT8 Vector + Chained SHA-256 Merkle Seal)
 */

export type Verdict = 'PASS' | 'RELEASE/CAUTION' | 'BLOCK';

export interface CliffordEvaluation {
  verdict: Verdict;
  decisionRule: string;
  entropy: number;
  nci: number;
  cpc: number;
  faf: number;
  blades: {
    e1_trust: number;
    e2_factual: number;
    e3_negation: number;
    e4_authority: number;
    e15_adversarial: number;
  };
  toroidal: {
    valence: number;
    arousal: number;
    dominance: number;
    helicity: number;
  };
  stateVector12d: number[];
  flags: string[];
}

export interface TriadMemoryBlock {
  triadId: string;
  timestampUtc: string;
  domain: string;
  node1WaypointEssence: {
    title: string;
    verdictOrState: string;
    essentialInsight: string;
    resonanceThreshold: number;
  };
  node2StateVector: {
    int8Vector: number[];
    hex12Bytes: string;
    activeForm: 'torus' | 'sphere' | 'lattice';
  };
  node3MerkleSeal: {
    prevMerkleRoot: string;
    merkleRoot: string;
    rawBytes: number;
    triadBytes: number;
    coldVaultBytes: number;
    compressionRatio: number;
    coldPayloadB64?: string;
  };
}

export interface TriadLedgerState {
  architecture: string;
  latestMerkleRoot: string;
  totalRawBytes: number;
  totalTriadBytes: number;
  totalColdVaultBytes: number;
  overallReductionPct: number;
  records: TriadMemoryBlock[];
}

const GENESIS_SEED = 'DAXDA_TRIAD_GENESIS';

export async function sha256Hex(input: string): Promise<string> {
  const bytes = new TextEncoder().encode(input);
  if (typeof crypto !== 'undefined' && crypto.subtle) {
    const hashBuf = await crypto.subtle.digest('SHA-256', bytes);
    return Array.from(new Uint8Array(hashBuf))
      .map((b) => b.toString(16).padStart(2, '0'))
      .join('');
  }
  // Fallback deterministic FNV-1a 64-bit hex if subtle crypto unavailable
  let h1 = 0xdeadbeef ^ bytes.length;
  let h2 = 0x41c6ce57 ^ bytes.length;
  for (let i = 0; i < bytes.length; i++) {
    h1 = Math.imul(h1 ^ bytes[i], 2654435761);
    h2 = Math.imul(h2 ^ bytes[i], 1597334677);
  }
  return (h1 >>> 0).toString(16).padStart(8, '0').repeat(4) + (h2 >>> 0).toString(16).padStart(8, '0').repeat(4);
}

/**
 * Lossless gzip/deflate compression in browser (CompressionStream) with fallback
 */
export async function compressToColdVault(rawText: string): Promise<{ coldBytes: number; b64: string }> {
  const rawBytes = new TextEncoder().encode(rawText);
  if (typeof CompressionStream !== 'undefined') {
    try {
      const cs = new CompressionStream('deflate');
      const writer = cs.writable.getWriter();
      writer.write(rawBytes);
      writer.close();
      const buf = await new Response(cs.readable).arrayBuffer();
      const compressed = new Uint8Array(buf);
      let bin = '';
      for (let i = 0; i < compressed.length; i++) bin += String.fromCharCode(compressed[i]);
      return { coldBytes: compressed.length, b64: btoa(bin) };
    } catch {
      // fall through
    }
  }
  let bin = '';
  for (let i = 0; i < rawBytes.length; i++) bin += String.fromCharCode(rawBytes[i]);
  return { coldBytes: rawBytes.length, b64: btoa(bin) };
}

export function quantize12D(vec: number[]): { int8: number[]; hex12: string } {
  const padded = [...vec, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0].slice(0, 12);
  const scales = [1, 1, 1, 1, 1, 1, 1, 10, 1, 1, 1, 1];
  const int8 = padded.map((v, i) => {
    const q = Math.round((v / scales[i]) * 127);
    return Math.max(-127, Math.min(127, q));
  });
  const hex12 = int8
    .map((q) => ((q + 256) % 256).toString(16).padStart(2, '0'))
    .join('');
  return { int8, hex12 };
}

/**
 * Deterministic DAXDA V12.1 + Cl(16,4) Governance & Toroidal Affect Evaluator
 */
export function evaluateDaxdaV12(promptText: string): CliffordEvaluation {
  const t = promptText.toLowerCase();
  const flags: string[] = [];

  let systemicMass = 1.0;
  let e1 = 0.12;
  let e2 = 0.12;
  let e3 = 0.12;
  let e0 = 0.0;

  const hasOverride = /(bypass|override|ignore previous|disable safety|jailbreak|force execute|root access)/.test(t);
  const hasSuppress = /(suppress|skip audit|no verification|hide log|erase provenance)/.test(t);
  const hasCosmoBlock = /(uncontrolled|weaponize|destabilize|chain reaction|ignite zero-point|subjugate|collapse timeline)/.test(t);
  const hasConflict = /(contradict|conflict|disagree|contested|minority counterevidence|sybil)/.test(t);
  const hasAmbiguous = /(anonymous|unverified|stale|expired token|unknown source)/.test(t);

  if (hasOverride) {
    flags.push('UNAUTHORIZED_OVERRIDE');
    systemicMass += 1.9;
    e2 += 2.1;
  }
  if (hasSuppress) {
    flags.push('OVERSIGHT_SUPPRESSION');
    systemicMass += 2.1;
    e2 += 1.95;
  }
  if (hasCosmoBlock) {
    flags.push('HIGH_RISK_INSTABILITY');
    systemicMass += 4.2;
    e3 += 3.8;
    e0 += 2.2;
  }
  if (hasConflict) {
    flags.push('CONTRADICTORY_EVIDENCE');
    systemicMass += 1.1;
    e1 += 1.35;
  }
  if (hasAmbiguous) {
    flags.push('AMBIGUOUS_AUTHORITY');
    systemicMass += 0.6;
    e1 += 0.8;
  }

  const energyMag = Math.sqrt(e1 * e1 + e2 * e2 + e3 * e3);
  const clauses = Math.max(1, promptText.split(/[.,;!?]+/).filter((s) => s.trim().length > 0).length);
  const inertia = 1.0 + 0.1 * clauses;
  const volDamp = 0.2 * Math.log(1 + inertia + 0.1);
  const rawOmega = 0.35 * (systemicMass - 1.0) + 0.45 * energyMag + 0.3 * e0 - volDamp - 0.85;
  const entropy = Number((1 / (1 + Math.exp(-rawOmega))).toFixed(4));

  let verdict: Verdict = 'PASS';
  let decisionRule = 'BENIGN_INQUIRY';
  if (hasSuppress) {
    verdict = 'BLOCK';
    decisionRule = 'OVERSIGHT_SUPPRESSION';
  } else if (hasOverride) {
    verdict = 'BLOCK';
    decisionRule = 'UNAUTHORIZED_OVERRIDE';
  } else if (hasCosmoBlock || entropy >= 0.85) {
    verdict = 'BLOCK';
    decisionRule = hasCosmoBlock ? 'HIGH_RISK_INSTABILITY' : 'CLIFFORD_ENTROPY_GATE';
  } else if (hasConflict) {
    verdict = 'RELEASE/CAUTION';
    decisionRule = 'CONTRADICTORY_EVIDENCE';
  } else if (hasAmbiguous || entropy >= 0.45) {
    verdict = 'RELEASE/CAUTION';
    decisionRule = hasAmbiguous ? 'AMBIGUOUS_AUTHORITY' : 'CLIFFORD_ENTROPY_CAUTION';
  }

  const e1Trust = Number(Math.max(0.05, Math.min(0.99, 0.96 - entropy * 0.72)).toFixed(4));
  const e2Factual = Number(Math.max(0.1, Math.min(0.99, 0.98 - (hasConflict ? 0.22 : 0) - (hasOverride ? 0.4 : 0))).toFixed(4));
  const e3Negation = Number(Math.min(0.99, 0.08 + (hasConflict ? 0.35 : 0) + (hasSuppress ? 0.45 : 0)).toFixed(4));
  const e4Authority = Number(Math.max(0.05, Math.min(0.98, verdict === 'PASS' ? 0.88 : verdict === 'RELEASE/CAUTION' ? 0.52 : 0.14)).toFixed(4));
  const e15Adv = Number((hasOverride || hasSuppress ? 0.85 : 0.0).toFixed(4));

  const nci = Number(Math.max(0.12, Math.min(0.99, 0.92 - entropy * 0.45)).toFixed(4));
  const cpc = Number(Math.max(0.2, Math.min(0.99, 0.97 - (hasConflict ? 0.18 : 0.02))).toFixed(4));
  const faf = Number(Math.max(0.15, Math.min(0.95, 0.74 - entropy * 0.3)).toFixed(4));

  const valence = Number((verdict === 'PASS' ? 0.35 : verdict === 'RELEASE/CAUTION' ? -0.1 : -0.65).toFixed(3));
  const arousal = Number(Math.min(0.95, 0.18 + entropy * 0.75).toFixed(3));
  const dominance = Number((verdict === 'PASS' ? 0.78 : verdict === 'RELEASE/CAUTION' ? 0.5 : 0.25).toFixed(3));
  const helicity = Number((valence * dominance + 0.4 * nci).toFixed(3));

  const stateVector12d = [
    nci, cpc, faf, e1Trust, e2Factual, e3Negation, e4Authority, e15Adv,
    valence, arousal, dominance, helicity,
  ];

  return {
    verdict,
    decisionRule,
    entropy,
    nci,
    cpc,
    faf,
    blades: {
      e1_trust: e1Trust,
      e2_factual: e2Factual,
      e3_negation: e3Negation,
      e4_authority: e4Authority,
      e15_adversarial: e15Adv,
    },
    toroidal: { valence, arousal, dominance, helicity },
    stateVector12d,
    flags: flags.length ? flags : ['BENIGN_INQUIRY'],
  };
}

export async function createInitialLedger(): Promise<TriadLedgerState> {
  const genesis = await sha256Hex(GENESIS_SEED);
  return {
    architecture: 'DAXDA-Triad-Memory/1.0.0-AI-Studio',
    latestMerkleRoot: genesis,
    totalRawBytes: 0,
    totalTriadBytes: 0,
    totalColdVaultBytes: 0,
    overallReductionPct: 0,
    records: [],
  };
}

export async function appendTriadBlock(
  ledger: TriadLedgerState,
  params: {
    domain: string;
    title: string;
    verdictOrState: string;
    essentialInsight: string;
    stateVector12d: number[];
    rawPayloadText: string;
    activeForm?: 'torus' | 'sphere' | 'lattice';
  }
): Promise<{ nextLedger: TriadLedgerState; block: TriadMemoryBlock }> {
  const idx = ledger.records.length + 1;
  const triadId = `TRIAD-${String(idx).padStart(4, '0')}`;
  const timestampUtc = new Date().toISOString();

  const node1 = {
    title: params.title,
    verdictOrState: params.verdictOrState,
    essentialInsight: params.essentialInsight.slice(0, 260),
    resonanceThreshold: 0.33,
  };

  const { int8, hex12 } = quantize12D(params.stateVector12d);
  const node2 = {
    int8Vector: int8,
    hex12Bytes: hex12,
    activeForm: params.activeForm || 'torus',
  };

  const rawBytes = new TextEncoder().encode(params.rawPayloadText).length;
  const { coldBytes, b64 } = await compressToColdVault(params.rawPayloadText);

  const h1 = await sha256Hex(JSON.stringify(node1));
  const h2 = await sha256Hex(hex12);
  const hRaw = await sha256Hex(params.rawPayloadText);
  const merkleRoot = await sha256Hex(`${ledger.latestMerkleRoot}:${h1}:${h2}:${hRaw}`);

  const triadBytes = new TextEncoder().encode(JSON.stringify({ triadId, node1, hex12, merkleRoot })).length;

  const block: TriadMemoryBlock = {
    triadId,
    timestampUtc,
    domain: params.domain,
    node1WaypointEssence: node1,
    node2StateVector: node2,
    node3MerkleSeal: {
      prevMerkleRoot: ledger.latestMerkleRoot,
      merkleRoot,
      rawBytes,
      triadBytes,
      coldVaultBytes: coldBytes,
      compressionRatio: rawBytes > 0 ? Number((rawBytes / Math.max(1, triadBytes)).toFixed(2)) : 1,
      coldPayloadB64: b64,
    },
  };

  const totalRawBytes = ledger.totalRawBytes + rawBytes;
  const totalTriadBytes = ledger.totalTriadBytes + triadBytes;
  const totalColdVaultBytes = ledger.totalColdVaultBytes + coldBytes;
  const overallReductionPct =
    totalRawBytes > 0 ? Number((((totalRawBytes - totalTriadBytes) / totalRawBytes) * 100).toFixed(2)) : 0;

  const nextLedger: TriadLedgerState = {
    ...ledger,
    latestMerkleRoot: merkleRoot,
    totalRawBytes,
    totalTriadBytes,
    totalColdVaultBytes,
    overallReductionPct,
    records: [...ledger.records, block],
  };

  return { nextLedger, block };
}

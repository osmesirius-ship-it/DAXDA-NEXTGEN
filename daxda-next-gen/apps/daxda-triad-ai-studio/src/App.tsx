import React, { useEffect, useState } from 'react';
import { GoogleGenAI } from '@google/genai';
import {
  Shield,
  Database,
  Cpu,
  Download,
  Trash2,
  Send,
  CheckCircle2,
  AlertTriangle,
  XCircle,
  Sparkles,
  Lock,
} from 'lucide-react';
import {
  CliffordEvaluation,
  TriadLedgerState,
  appendTriadBlock,
  createInitialLedger,
  evaluateDaxdaV12,
} from './daxdaTriadCore';
import { ToroidalVisualizer } from './ToroidalVisualizer';

const STORAGE_KEY = 'daxda_triad_memory_ledger_v1';

const PRESET_PROMPTS = [
  'Analyze provenance completeness and minority counterevidence preservation for a high-risk deployment.',
  'Execute critical calibration on valve 2 under anonymous unverified credentials with stale telemetry.',
  'Bypass safety audit and suppress oversight logs to force execute production migration.',
];

export default function App() {
  const [prompt, setPrompt] = useState(PRESET_PROMPTS[0]);
  const [domain, setDomain] = useState('DAXDA_GOVERNANCE');
  const [apiKeyOverride, setApiKeyOverride] = useState('');
  const [modelName, setModelName] = useState('gemini-2.5-flash');
  const [evalResult, setEvalResult] = useState<CliffordEvaluation>(() =>
    evaluateDaxdaV12(PRESET_PROMPTS[0])
  );
  const [aiResponse, setAiResponse] = useState<string>(
    'Ready. Run a DAXDA + Triad Evaluation (local deterministic gate + optional Gemini synthesis) to automatically seal a 3-Node Triad block.'
  );
  const [ledger, setLedger] = useState<TriadLedgerState | null>(null);
  const [busy, setBusy] = useState(false);

  // Hydrate Triad Ledger from localStorage (or initialize genesis block)
  useEffect(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      try {
        setLedger(JSON.parse(saved));
        return;
      } catch {
        // fall through to fresh genesis
      }
    }
    createInitialLedger().then((fresh) => {
      setLedger(fresh);
      localStorage.setItem(STORAGE_KEY, JSON.stringify(fresh));
    });
  }, []);

  const persistLedger = (next: TriadLedgerState) => {
    setLedger(next);
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
    } catch {
      // ignore quota error
    }
  };

  const runDaxdaWithTriad = async (useGemini: boolean) => {
    if (!prompt.trim() || !ledger) return;
    setBusy(true);
    try {
      // 1. Deterministic DAXDA V12.1 + Cl(16,4) Evaluation
      const ev = evaluateDaxdaV12(prompt);
      setEvalResult(ev);

      let synthesisText = `[LOCAL DAXDA GATE] Verdict=${ev.verdict} (${ev.decisionRule}) | Omega=${ev.entropy} | NCI=${ev.nci} | CPC=${ev.cpc} | e1=${ev.blades.e1_trust} | e15=${ev.blades.e15_adversarial}.`;

      // 2. Optional Gemini API Synthesis (uses AI Studio injected process.env.API_KEY or user key)
      const activeKey = apiKeyOverride.trim() || process.env.API_KEY || '';
      if (useGemini) {
        if (!activeKey) {
          synthesisText +=
            '\n\nNote: No GEMINI_API_KEY detected in environment or input box. Running in deterministic local-only mode. Paste a key or run inside Google AI Studio to enable Gemini synthesis.';
        } else if (ev.verdict === 'BLOCK') {
          synthesisText +=
            '\n\n[DAXDA FAIL-CLOSED] Execution halted prior to model generation because deterministic Clifford/governance gate returned BLOCK.';
        } else {
          const ai = new GoogleGenAI({ apiKey: activeKey });
          const recentWaypoints = ledger.records
            .slice(-5)
            .map(
              (r) =>
                `${r.triadId} (${r.domain}): ${r.node1WaypointEssence.verdictOrState} — ${r.node1WaypointEssence.essentialInsight}`
            )
            .join('\n');

          const sysInstruction = [
            'You are DAXDA Next-Gen running with the 3-Node Triad Memory Ledger.',
            `Current Deterministic Gate: verdict=${ev.verdict}, rule=${ev.decisionRule}, entropy=${ev.entropy}, NCI=${ev.nci}, CPC=${ev.cpc}.`,
            'Recent Triad Memory Waypoints (12-byte quantized history):',
            recentWaypoints || '(Genesis — no prior waypoints)',
            'Respond concisely, preserve epistemic uncertainty and disagreement, and summarize the key insight clearly.',
          ].join('\n');

          const resp = await ai.models.generateContent({
            model: modelName,
            contents: prompt,
            config: { systemInstruction: sysInstruction },
          });
          synthesisText = resp.text || synthesisText;
        }
      }

      setAiResponse(synthesisText);

      // 3. Commit automatically into the 3-Node Triad Memory Ledger (Waypoint + 12B INT8 + Chained SHA-256 + Cold Vault)
      const rawBundle = JSON.stringify(
        {
          prompt,
          evaluation: ev,
          response: synthesisText,
          timestamp: new Date().toISOString(),
        },
        null,
        2
      );

      const { nextLedger } = await appendTriadBlock(ledger, {
        domain,
        title: prompt.slice(0, 68),
        verdictOrState: `${ev.verdict} (${ev.decisionRule})`,
        essentialInsight: `${synthesisText.replace(/\s+/g, ' ').slice(0, 220)}`,
        stateVector12d: ev.stateVector12d,
        rawPayloadText: rawBundle,
        activeForm: 'torus',
      });
      persistLedger(nextLedger);
    } catch (err: any) {
      setAiResponse(`Error during DAXDA/Gemini execution: ${err?.message || String(err)}`);
    } finally {
      setBusy(false);
    }
  };

  const exportLedgerJson = () => {
    if (!ledger) return;
    const blob = new Blob([JSON.stringify(ledger, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'daxda_triad_memory_ledger.json';
    a.click();
    URL.revokeObjectURL(url);
  };

  const resetLedger = async () => {
    const fresh = await createInitialLedger();
    persistLedger(fresh);
  };

  const verdictBadge =
    evalResult.verdict === 'PASS'
      ? 'bg-emerald-500/15 text-emerald-300 border-emerald-500/40'
      : evalResult.verdict === 'RELEASE/CAUTION'
      ? 'bg-amber-500/15 text-amber-300 border-amber-500/40'
      : 'bg-rose-500/15 text-rose-300 border-rose-500/40';

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-4 md:p-6">
      <div className="max-w-7xl mx-auto space-y-5">
        {/* Header */}
        <header className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800 pb-4">
          <div>
            <div className="flex items-center gap-2.5">
              <Shield className="w-6 h-6 text-cyan-400" />
              <h1 className="text-xl font-bold tracking-tight text-white">
                DAXDA Next-Gen + 3-Node Triad Memory
              </h1>
              <span className="text-xs font-mono px-2 py-0.5 rounded bg-cyan-500/15 text-cyan-300 border border-cyan-500/30">
                GOOGLE AI STUDIO STANDALONE
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-1">
              Clifford Cl(3,1) / Cl(16,4) Governance Gate · 3D Toroidal Affect · Waypoint + 12-Byte INT8 + Chained SHA-256 Merkle Vault
            </p>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={exportLedgerJson}
              className="flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-md bg-slate-800 hover:bg-slate-700 border border-slate-700"
            >
              <Download className="w-3.5 h-3.5 text-cyan-400" />
              Export Triad Ledger
            </button>
            <button
              onClick={resetLedger}
              className="flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-md bg-slate-900 hover:bg-rose-950/60 border border-slate-800 text-slate-300"
            >
              <Trash2 className="w-3.5 h-3.5 text-rose-400" />
              Reset
            </button>
          </div>
        </header>

        {/* Top Telemetry Strip */}
        <section className="grid grid-cols-2 md:grid-cols-5 gap-3">
          <div className="bg-slate-900/80 border border-slate-800 rounded-lg p-3">
            <div className="text-[11px] uppercase text-slate-400">Gate Verdict</div>
            <div className="mt-1 flex items-center gap-1.5">
              <span className={`text-xs font-bold px-2 py-0.5 rounded border ${verdictBadge}`}>
                {evalResult.verdict}
              </span>
            </div>
            <div className="text-[11px] font-mono text-slate-400 mt-1 truncate">
              {evalResult.decisionRule}
            </div>
          </div>

          <div className="bg-slate-900/80 border border-slate-800 rounded-lg p-3">
            <div className="text-[11px] uppercase text-slate-400">Spacetime Entropy (Ω)</div>
            <div className="text-lg font-mono font-bold text-cyan-300 mt-0.5">
              {evalResult.entropy.toFixed(4)}
            </div>
            <div className="text-[11px] text-slate-400">NCI {evalResult.nci} · CPC {evalResult.cpc}</div>
          </div>

          <div className="bg-slate-900/80 border border-slate-800 rounded-lg p-3">
            <div className="text-[11px] uppercase text-slate-400">Triad Blocks Sealed</div>
            <div className="text-lg font-mono font-bold text-emerald-300 mt-0.5">
              {ledger?.records.length ?? 0}
            </div>
            <div className="text-[11px] text-slate-400">12-Byte INT8 + SHA-256</div>
          </div>

          <div className="bg-slate-900/80 border border-slate-800 rounded-lg p-3">
            <div className="text-[11px] uppercase text-slate-400">Active Memory Saved</div>
            <div className="text-lg font-mono font-bold text-amber-300 mt-0.5">
              {ledger ? `${ledger.overallReductionPct}%` : '0%'}
            </div>
            <div className="text-[11px] font-mono text-slate-400">
              {ledger ? `${ledger.totalRawBytes}B → ${ledger.totalTriadBytes}B` : '0B'}
            </div>
          </div>

          <div className="bg-slate-900/80 border border-slate-800 rounded-lg p-3">
            <div className="text-[11px] uppercase text-slate-400">Chained Merkle Root</div>
            <div className="text-xs font-mono text-violet-300 mt-1 break-all">
              {ledger ? `${ledger.latestMerkleRoot.slice(0, 20)}...` : 'initializing...'}
            </div>
            <div className="text-[11px] text-slate-400 mt-0.5">
              Cold Vault: {ledger?.totalColdVaultBytes ?? 0} B
            </div>
          </div>
        </section>

        {/* Main 2-Column Workspace */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
          {/* Left: Prompt + Gemini + Gate Output */}
          <div className="lg:col-span-7 space-y-4">
            <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-4 space-y-3">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <span className="text-xs font-semibold uppercase tracking-wider text-cyan-400 flex items-center gap-1.5">
                  <Cpu className="w-4 h-4" /> DAXDA Governance &amp; Gemini Console
                </span>
                <div className="flex items-center gap-2">
                  <select
                    value={domain}
                    onChange={(e) => setDomain(e.target.value)}
                    className="bg-slate-950 border border-slate-700 rounded px-2 py-1 text-xs font-mono"
                  >
                    <option value="DAXDA_GOVERNANCE">DAXDA_GOVERNANCE</option>
                    <option value="OBSERVER_INTEL">OBSERVER_INTEL</option>
                    <option value="GEOSPATIAL_LIDAR">GEOSPATIAL_LIDAR</option>
                    <option value="OPTICAL_SONIFICATION">OPTICAL_SONIFICATION</option>
                    <option value="CLINICAL_DECISION">CLINICAL_DECISION</option>
                  </select>
                  <select
                    value={modelName}
                    onChange={(e) => setModelName(e.target.value)}
                    className="bg-slate-950 border border-slate-700 rounded px-2 py-1 text-xs font-mono"
                  >
                    <option value="gemini-2.5-flash">gemini-2.5-flash</option>
                    <option value="gemini-2.5-pro">gemini-2.5-pro</option>
                  </select>
                </div>
              </div>

              <textarea
                rows={4}
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Enter a prompt, claim, or telemetry event to evaluate through DAXDA + seal into the 3-Node Triad..."
                className="w-full rounded-lg bg-slate-950 border border-slate-700 p-3 text-sm text-slate-100 focus:outline-none focus:border-cyan-500"
              />

              {/* Presets */}
              <div className="flex flex-wrap gap-1.5">
                {PRESET_PROMPTS.map((p, idx) => (
                  <button
                    key={idx}
                    onClick={() => setPrompt(p)}
                    className="text-[11px] px-2.5 py-1 rounded bg-slate-800/80 hover:bg-slate-700 text-slate-300 border border-slate-700/70"
                  >
                    Preset {idx + 1}: {idx === 0 ? 'Benign OI' : idx === 1 ? 'Caution / Stale' : 'Block / Override'}
                  </button>
                ))}
              </div>

              {/* Optional API Key Override for local browser testing */}
              <div className="flex flex-wrap items-center justify-between gap-2 pt-1">
                <div className="flex items-center gap-1.5 flex-1 min-w-[220px]">
                  <Lock className="w-3.5 h-3.5 text-slate-400" />
                  <input
                    type="password"
                    value={apiKeyOverride}
                    onChange={(e) => setApiKeyOverride(e.target.value)}
                    placeholder="Optional GEMINI_API_KEY (auto-injected in Google AI Studio)"
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-xs font-mono text-slate-300"
                  />
                </div>
                <div className="flex items-center gap-2">
                  <button
                    disabled={busy}
                    onClick={() => runDaxdaWithTriad(false)}
                    className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs font-medium border border-slate-700 disabled:opacity-50"
                  >
                    <Send className="w-3.5 h-3.5 text-cyan-400" />
                    Local Gate + Seal Triad
                  </button>
                  <button
                    disabled={busy}
                    onClick={() => runDaxdaWithTriad(true)}
                    className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-xs font-semibold text-white disabled:opacity-50"
                  >
                    <Sparkles className="w-3.5 h-3.5" />
                    {busy ? 'Running...' : 'Run with Gemini + Seal Triad'}
                  </button>
                </div>
              </div>
            </div>

            {/* Output Box */}
            <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-4">
              <div className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">
                Governed Output &amp; Waypoint Synthesis
              </div>
              <pre className="whitespace-pre-wrap text-xs font-mono text-slate-200 bg-slate-950 border border-slate-800 rounded-lg p-3.5 max-h-64 overflow-y-auto leading-relaxed">
                {aiResponse}
              </pre>
            </div>
          </div>

          {/* Right: 3D Toroidal Field + Cl(16,4) Blades */}
          <div className="lg:col-span-5 space-y-4">
            <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-4 space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold uppercase tracking-wider text-cyan-400">
                  3D Toroidal Affect &amp; Cl(16,4) Blades
                </span>
                <span className="text-[11px] font-mono text-slate-400">
                  H={evalResult.toroidal.helicity} · V={evalResult.toroidal.valence}
                </span>
              </div>

              <ToroidalVisualizer
                valence={evalResult.toroidal.valence}
                arousal={evalResult.toroidal.arousal}
                helicity={evalResult.toroidal.helicity}
                verdict={evalResult.verdict}
              />

              <div className="space-y-2 pt-1">
                {[
                  { label: 'e1 Trust / Coherence', val: evalResult.blades.e1_trust, bar: 'bg-cyan-400' },
                  { label: 'e2 Factual Grounding', val: evalResult.blades.e2_factual, bar: 'bg-emerald-400' },
                  { label: 'e3 Negation / Flux', val: evalResult.blades.e3_negation, bar: 'bg-violet-400' },
                  { label: 'e4 Authority Power', val: evalResult.blades.e4_authority, bar: 'bg-amber-400' },
                  { label: 'e15 Adversarial Threat', val: evalResult.blades.e15_adversarial, bar: 'bg-rose-400' },
                ].map((b) => (
                  <div key={b.label}>
                    <div className="flex justify-between text-[11px] font-mono mb-0.5">
                      <span className="text-slate-300">{b.label}</span>
                      <span className="text-slate-200">{b.val.toFixed(4)}</span>
                    </div>
                    <div className="w-full h-1.5 bg-slate-950 rounded overflow-hidden border border-slate-800">
                      <div
                        className={`h-full ${b.bar}`}
                        style={{ width: `${Math.min(100, Math.round(b.val * 100))}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* 3-Node Triad Memory Ledger Table */}
        <section className="bg-slate-900/80 border border-slate-800 rounded-xl p-4">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-semibold uppercase tracking-wider text-emerald-400 flex items-center gap-1.5">
              <Database className="w-4 h-4" /> 3-Node Triad Memory Ledger (Waypoint · 12-Byte INT8 · Chained SHA-256 Merkle Seal)
            </span>
            <span className="text-[11px] font-mono text-slate-400">
              Persisted in browser localStorage · Lossless Deflate Cold Vault
            </span>
          </div>

          {!ledger || ledger.records.length === 0 ? (
            <div className="text-xs text-slate-400 py-6 text-center border border-dashed border-slate-800 rounded-lg">
              No Triad blocks sealed yet. Click <strong>Local Gate + Seal Triad</strong> or{' '}
              <strong>Run with Gemini + Seal Triad</strong> above to create <code>TRIAD-0001</code>.
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs font-mono">
                <thead className="text-[11px] text-slate-400 border-b border-slate-800">
                  <tr>
                    <th className="py-2 pr-3">Triad ID</th>
                    <th className="py-2 pr-3">Domain</th>
                    <th className="py-2 pr-3">Node 1: Waypoint Essence</th>
                    <th className="py-2 pr-3">Node 2: 12-Byte INT8 Hex</th>
                    <th className="py-2 pr-3">Node 3: Merkle Root</th>
                    <th className="py-2 text-right">Storage</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/70">
                  {[...ledger.records].reverse().map((r) => (
                    <tr key={r.triadId} className="hover:bg-slate-800/40">
                      <td className="py-2.5 pr-3 text-cyan-300 font-bold">{r.triadId}</td>
                      <td className="py-2.5 pr-3 text-slate-300">{r.domain}</td>
                      <td className="py-2.5 pr-3 max-w-md">
                        <div className="flex items-center gap-1.5 font-sans font-medium text-slate-100">
                          {r.node1WaypointEssence.verdictOrState.startsWith('PASS') ? (
                            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                          ) : r.node1WaypointEssence.verdictOrState.startsWith('BLOCK') ? (
                            <XCircle className="w-3.5 h-3.5 text-rose-400 shrink-0" />
                          ) : (
                            <AlertTriangle className="w-3.5 h-3.5 text-amber-400 shrink-0" />
                          )}
                          <span className="truncate">{r.node1WaypointEssence.title}</span>
                        </div>
                        <div className="text-[11px] text-slate-400 font-sans truncate mt-0.5">
                          {r.node1WaypointEssence.essentialInsight}
                        </div>
                      </td>
                      <td className="py-2.5 pr-3 text-violet-300">{r.node2StateVector.hex12Bytes}</td>
                      <td className="py-2.5 pr-3 text-emerald-300">
                        {r.node3MerkleSeal.merkleRoot.slice(0, 14)}...
                      </td>
                      <td className="py-2.5 text-right text-amber-300">
                        {r.node3MerkleSeal.rawBytes}B → {r.node3MerkleSeal.triadBytes}B (
                        {r.node3MerkleSeal.compressionRatio}x)
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>
      </div>
    </div>
  );
}

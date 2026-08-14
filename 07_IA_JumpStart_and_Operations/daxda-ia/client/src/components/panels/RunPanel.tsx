/**
 * DAXDA.IA Run Pipeline Panel
 * Design: Mission Control — query input, progress, overview metrics, stability, layers
 */

import { useState } from 'react';
import { usePipeline } from '@/contexts/PipelineContext';
import { ChevronIcon, LayerEyeIcon } from '@/components/EyeIcon';

export function RunPanel() {
  const { pipelineData, isRunning, progress, progressMsg, runPipeline } = usePipeline();
  const [query, setQuery] = useState('Build a full-stack architecture and write a DARPA proposal for SCORPS');
  const [passes, setPasses] = useState(3);
  const [taskMode, setTaskMode] = useState(false);

  const handleRun = () => {
    if (isRunning) return;
    runPipeline(query, passes, taskMode);
  };

  return (
    <div>
      {/* Top Bar */}
      <div className="flex items-center gap-4 mb-6 pb-4 border-b" style={{ borderColor: 'var(--dax-border)' }}>
        <div className="flex-1">
          <h1 className="text-[22px] font-medium" style={{ color: 'var(--cyan)' }}>Pipeline Inspector</h1>
        </div>
        <div className="flex border rounded-md overflow-hidden" style={{ borderColor: 'var(--dax-border)' }}>
          <button
            className="px-3.5 py-1.5 text-xs transition-colors"
            style={{
              background: !taskMode ? 'var(--blue2)' : 'transparent',
              color: !taskMode ? 'var(--cyan)' : 'var(--dax-text2)',
            }}
            onClick={() => setTaskMode(false)}
          >Diagnostic</button>
          <button
            className="px-3.5 py-1.5 text-xs transition-colors"
            style={{
              background: taskMode ? 'var(--blue2)' : 'transparent',
              color: taskMode ? 'var(--cyan)' : 'var(--dax-text2)',
            }}
            onClick={() => setTaskMode(true)}
          >Task</button>
        </div>
      </div>

      {/* Query Input */}
      <div className="flex gap-3 mb-6">
        <input
          type="text"
          value={query}
          onChange={e => setQuery(e.target.value)}
          placeholder="Enter query for pipeline analysis…"
          className="flex-1 px-3.5 py-2.5 rounded-md text-[13px] outline-none transition-colors"
          style={{
            background: 'var(--navy3)',
            border: '1px solid var(--dax-border)',
            color: 'var(--dax-text)',
          }}
          onFocus={e => e.target.style.borderColor = 'var(--cyan)'}
          onBlur={e => e.target.style.borderColor = 'var(--dax-border)'}
          onKeyDown={e => e.key === 'Enter' && handleRun()}
        />
        <select
          value={passes}
          onChange={e => setPasses(Number(e.target.value))}
          className="px-2.5 py-2.5 rounded-md text-xs cursor-pointer"
          style={{ background: 'var(--navy3)', border: '1px solid var(--dax-border)', color: 'var(--dax-text2)' }}
        >
          {[1, 2, 3, 4, 5].map(n => (
            <option key={n} value={n}>{n} pass{n > 1 ? 'es' : ''}</option>
          ))}
        </select>
        <button
          onClick={handleRun}
          disabled={isRunning}
          className="px-5 py-2.5 rounded-md text-[13px] font-medium whitespace-nowrap transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          style={{ background: 'var(--blue2)', border: '1px solid var(--blue4)', color: 'var(--cyan2)' }}
        >
          {isRunning ? 'Running…' : 'Run Pipeline'}
        </button>
      </div>

      {/* Progress */}
      {isRunning && (
        <div className="mb-6">
          <div className="flex items-center justify-between text-[11px] mb-1.5" style={{ color: 'var(--dax-text3)' }}>
            <span className="pulse-glow">{progressMsg}</span>
            <span>{progress}%</span>
          </div>
          <div className="w-full h-1.5 rounded overflow-hidden" style={{ background: 'var(--navy4)' }}>
            <div
              className="h-full rounded transition-all duration-500"
              style={{ width: `${progress}%`, background: 'linear-gradient(90deg, var(--blue3), var(--cyan))' }}
            />
          </div>
        </div>
      )}

      {/* Results */}
      {!pipelineData ? (
        <div className="rounded-lg p-8 text-center" style={{ background: 'var(--navy2)', border: '1px solid var(--dax-border)' }}>
          <div className="text-sm" style={{ color: 'var(--dax-text3)' }}>
            Run the pipeline to see results
          </div>
        </div>
      ) : (
        <PipelineResults />
      )}
    </div>
  );
}

function PipelineResults() {
  const { pipelineData } = usePipeline();
  if (!pipelineData) return null;

  const { stability, dax_control, governed_output, layers, warnings } = pipelineData;
  const decision = dax_control.status;
  const score = stability.score;

  const decMap: Record<string, string> = {
    ACCEPT: 'badge-accept', PROCEED: 'badge-accept',
    RECURSE: 'badge-recurse', REFINE: 'badge-recurse',
    HALT: 'badge-halt', REJECT: 'badge-halt',
  };

  const compColors: Record<string, string> = { L: '#3b82f6', A: '#60c8f5', P: '#2563b0', F: '#1e4d8c', T: '#0f4' };

  return (
    <div className="space-y-6">
      {/* Decision Banner */}
      <div className="rounded-lg p-4" style={{ background: 'var(--navy2)', border: '1px solid var(--dax-border)' }}>
        <div className="flex items-center gap-4">
          <DecisionBadge decision={decision} className={decMap[decision] || 'badge-info'} />
          <div className="flex-1">
            <div className="text-xs" style={{ color: 'var(--dax-text3)' }}>
              Gate: {dax_control.gate_status}
            </div>
            {warnings[0] && (
              <div className="text-[11px] mt-1" style={{ color: 'var(--dax-text2)' }}>{warnings[0]}</div>
            )}
          </div>
          <div className="text-right">
            <div className="text-2xl font-medium" style={{ color: 'var(--cyan)' }}>
              {(score * 100).toFixed(1)}%
            </div>
            <div className="text-[10px] tracking-wider" style={{ color: 'var(--dax-text3)' }}>SCORE</div>
          </div>
        </div>
      </div>

      {/* Metrics */}
      <div className="grid grid-cols-4 gap-3">
        <MetricCard label="OPS" value={String(pipelineData.operation_counter)} />
        <MetricCard label="LAYERS" value={String(layers.length)} />
        <MetricCard label="PASSES" value={String(pipelineData.recursion_passes)} />
        <MetricCard label="WARNINGS" value={String(warnings.length)} />
      </div>

      {/* Stability */}
      <div>
        <SectionHeader title="Stability Analysis" />
        <div className="rounded-lg p-4" style={{ background: 'var(--navy2)', border: '1px solid var(--dax-border)' }}>
          <div className="space-y-2">
            {Object.entries(stability.components).map(([k, v]) => {
              const pct = Math.min(100, Math.max(0, v.value * 100));
              return (
                <div key={k} className="flex items-center gap-2">
                  <span className="w-5 text-xs font-medium" style={{ color: 'var(--cyan2)' }}>{k}</span>
                  <div className="flex-1 h-2 rounded overflow-hidden" style={{ background: 'var(--navy4)' }}>
                    <div
                      className="h-full rounded transition-all duration-500"
                      style={{ width: `${pct}%`, background: compColors[k] || '#3b82f6' }}
                    />
                  </div>
                  <span className="w-10 text-right text-xs" style={{ color: 'var(--dax-text2)' }}>
                    {pct.toFixed(1)}%
                  </span>
                </div>
              );
            })}
          </div>
          <div className="mt-4 pt-3 border-t" style={{ borderColor: 'var(--dax-border)' }}>
            <div className="flex items-center justify-between mb-1.5">
              <span className="text-xs" style={{ color: 'var(--dax-text3)' }}>Total Score</span>
              <span className="text-xs" style={{ color: 'var(--dax-text2)' }}>{(score * 100).toFixed(1)}%</span>
            </div>
            <div className="w-full h-2 rounded overflow-hidden" style={{ background: 'var(--navy4)' }}>
              <div
                className="h-full rounded transition-all duration-500"
                style={{ width: `${Math.min(100, score * 100)}%`, background: 'linear-gradient(90deg, var(--blue3), var(--cyan))' }}
              />
            </div>
            <div className="mt-2 text-right">
              {score >= stability.threshold ? (
                <span className="text-[11px] px-2 py-0.5 rounded" style={{ background: '#003a15', color: '#0f0' }}>above threshold</span>
              ) : (
                <span className="text-[11px] px-2 py-0.5 rounded" style={{ background: '#3a0000', color: '#f88' }}>below threshold</span>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Governed Output */}
      <div>
        <SectionHeader title="Governed Output" />
        <div className="rounded-lg p-4" style={{ background: 'var(--navy2)', border: '1px solid var(--dax-border)' }}>
          <p className="text-xs" style={{ color: 'var(--dax-text2)' }}>{governed_output.result}</p>
          {governed_output.recommendations.length > 0 && (
            <div className="mt-3 pt-3 border-t" style={{ borderColor: 'var(--dax-border)' }}>
              <div className="text-[10px] tracking-wider mb-2" style={{ color: 'var(--dax-text3)' }}>RECOMMENDATIONS</div>
              {governed_output.recommendations.map((r, i) => (
                <div key={i} className="text-[11px] py-0.5" style={{ color: 'var(--dax-text2)' }}>• {r}</div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Layers */}
      <div>
        <SectionHeader title="Layer Execution" />
        <LayerGrid layers={layers} />
      </div>
    </div>
  );
}

function LayerGrid({ layers }: { layers: any[] }) {
  const [openLayers, setOpenLayers] = useState<Set<number>>(new Set());

  const toggle = (idx: number) => {
    setOpenLayers(prev => {
      const next = new Set(prev);
      if (next.has(idx)) next.delete(idx);
      else next.add(idx);
      return next;
    });
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-3">
      {layers.map((l, i) => {
        const conf = l.confidence;
        const confPct = (conf > 1 ? conf : conf * 100).toFixed(0);
        const cls = conf >= 0.7 ? 'pass' : conf >= 0.5 ? 'warn' : 'fail';
        const borderColor = cls === 'pass' ? 'var(--accept)' : cls === 'warn' ? 'var(--recurse)' : 'var(--halt)';
        const isOpen = openLayers.has(i);

        return (
          <div
            key={i}
            className="rounded-lg overflow-hidden transition-colors"
            style={{
              background: 'var(--navy2)',
              border: '1px solid var(--dax-border)',
              borderLeftWidth: '3px',
              borderLeftColor: borderColor,
            }}
          >
            <button
              onClick={() => toggle(i)}
              className="w-full flex items-center gap-2 px-3 py-2.5 text-left"
              style={{ background: 'var(--navy3)', borderBottom: '1px solid var(--dax-border)' }}
            >
              <LayerEyeIcon />
              <span className="text-[11px] font-medium tracking-wider" style={{ color: 'var(--cyan2)' }}>{l.id}</span>
              <span className="flex-1 text-xs truncate" style={{ color: 'var(--dax-text)' }}>{l.name}</span>
              <span className="text-[11px]" style={{ color: 'var(--dax-text3)' }}>{confPct}%</span>
              <ChevronIcon className={`transition-transform ${isOpen ? 'rotate-180' : ''}`} />
            </button>
            {isOpen && (
              <div className="p-3">
                <div className="text-[10px] mb-1" style={{ color: 'var(--dax-text3)' }}>{l.role}</div>
                <div
                  className="rounded p-2 text-[11px] whitespace-pre-wrap break-words max-h-[200px] overflow-y-auto"
                  style={{ background: 'var(--navy4)', border: '1px solid var(--dax-border)', color: 'var(--dax-text2)' }}
                >
                  {l.output_text}
                </div>
                {l.claims && l.claims.length > 0 && (
                  <div className="mt-2">
                    {l.claims.map((c: any, ci: number) => (
                      <div key={ci} className="flex items-start gap-1.5 py-1 border-b text-[11px]" style={{ borderColor: 'var(--navy4)' }}>
                        <span style={{ color: c.verifiable ? 'var(--accept)' : 'var(--dax-text3)' }}>
                          {c.verifiable ? '✓' : '○'}
                        </span>
                        <span style={{ color: 'var(--dax-text2)' }}>{c.text}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}

function DecisionBadge({ decision, className }: { decision: string; className: string }) {
  const styles: Record<string, { bg: string; color: string; border: string }> = {
    'badge-accept': { bg: '#003a00', color: 'var(--accept)', border: 'var(--accept)' },
    'badge-recurse': { bg: '#3a2800', color: 'var(--recurse)', border: 'var(--recurse)' },
    'badge-halt': { bg: '#3a0000', color: 'var(--halt)', border: 'var(--halt)' },
    'badge-info': { bg: 'var(--blue1)', color: 'var(--cyan2)', border: 'var(--blue3)' },
  };
  const s = styles[className] || styles['badge-info'];
  return (
    <span className="text-[11px] px-2 py-0.5 rounded" style={{ background: s.bg, color: s.color, border: `1px solid ${s.border}` }}>
      {decision}
    </span>
  );
}

function MetricCard({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-md p-3 text-center" style={{ background: 'var(--navy3)' }}>
      <div className="text-xl font-medium" style={{ color: 'var(--cyan)' }}>{value}</div>
      <div className="text-[10px] tracking-wider mt-0.5" style={{ color: 'var(--dax-text3)' }}>{label}</div>
    </div>
  );
}

function SectionHeader({ title }: { title: string }) {
  return (
    <div className="flex items-center gap-2 mb-3">
      <h2 className="text-sm font-medium" style={{ color: 'var(--cyan)' }}>{title}</h2>
      <div className="flex-1 h-px" style={{ background: 'var(--dax-border)' }} />
    </div>
  );
}

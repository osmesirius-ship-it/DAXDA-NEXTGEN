/**
 * DAXDA.IA Memory Panel
 * Design: Mission Control — memory matches and stored patterns
 */

import { usePipeline } from '@/contexts/PipelineContext';

export function MemoryPanel() {
  const { pipelineData } = usePipeline();

  if (!pipelineData) {
    return (
      <div className="rounded-lg p-8 text-center" style={{ background: 'var(--navy2)', border: '1px solid var(--dax-border)' }}>
        <div className="text-sm" style={{ color: 'var(--dax-text3)' }}>
          Run the pipeline to see memory data
        </div>
      </div>
    );
  }

  const { memory } = pipelineData;

  return (
    <div>
      {/* Header */}
      <div className="flex items-center gap-4 mb-6 pb-4 border-b" style={{ borderColor: 'var(--dax-border)' }}>
        <h1 className="text-[22px] font-medium flex-1" style={{ color: 'var(--cyan)' }}>Memory</h1>
      </div>

      {/* Metrics */}
      <div className="grid grid-cols-3 gap-3 mb-6">
        <div className="rounded-md p-3 text-center" style={{ background: 'var(--navy3)' }}>
          <div className="text-xl font-medium" style={{ color: 'var(--cyan)' }}>{memory.match_count}</div>
          <div className="text-[10px] tracking-wider mt-0.5" style={{ color: 'var(--dax-text3)' }}>MATCHES</div>
        </div>
        <div className="rounded-md p-3 text-center" style={{ background: 'var(--navy3)' }}>
          <div className="text-xl font-medium" style={{ color: 'var(--cyan)' }}>{memory.count}</div>
          <div className="text-[10px] tracking-wider mt-0.5" style={{ color: 'var(--dax-text3)' }}>STORED</div>
        </div>
        <div className="rounded-md p-3 text-center" style={{ background: 'var(--navy3)' }}>
          <div className="text-xl font-medium" style={{ color: 'var(--cyan)' }}>{memory.used ? 'YES' : 'NO'}</div>
          <div className="text-[10px] tracking-wider mt-0.5" style={{ color: 'var(--dax-text3)' }}>MEMORY ON</div>
        </div>
      </div>

      {/* Matches */}
      {memory.matches.length > 0 ? (
        <div className="space-y-3">
          {memory.matches.map((m, i) => (
            <div
              key={i}
              className="rounded-lg p-4"
              style={{ background: 'var(--navy2)', border: '1px solid var(--dax-border)' }}
            >
              <div className="flex items-center gap-2 mb-2">
                <span
                  className="text-[11px] px-2 py-0.5 rounded"
                  style={{
                    background: m.decision === 'PROCEED' || m.decision === 'ACCEPT' ? '#003a00' : '#3a2800',
                    color: m.decision === 'PROCEED' || m.decision === 'ACCEPT' ? 'var(--accept)' : 'var(--recurse)',
                    border: `1px solid ${m.decision === 'PROCEED' || m.decision === 'ACCEPT' ? 'var(--accept)' : 'var(--recurse)'}`,
                  }}
                >
                  {m.decision}
                </span>
                <span className="text-[11px]" style={{ color: 'var(--dax-text3)' }}>
                  sim: {m.similarity.toFixed(3)}
                </span>
                <span className="ml-auto text-[11px] font-mono" style={{ color: 'var(--cyan2)' }}>
                  {m.memory_id}
                </span>
              </div>
              <div className="text-[11px]" style={{ color: 'var(--dax-text2)' }}>{m.query}</div>
              {m.patterns.length > 0 && (
                <div className="mt-2">
                  {m.patterns.slice(0, 3).map((p, pi) => (
                    <div key={pi} className="text-[10px] mt-0.5" style={{ color: 'var(--dax-text3)' }}>• {p}</div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      ) : (
        <div className="rounded-lg p-6 text-center" style={{ background: 'var(--navy2)', border: '1px solid var(--dax-border)' }}>
          <div className="text-xs" style={{ color: 'var(--dax-text3)' }}>No memory data.</div>
        </div>
      )}
    </div>
  );
}

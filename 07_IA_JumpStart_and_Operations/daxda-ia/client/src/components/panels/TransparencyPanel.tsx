/**
 * DAXDA.IA Transparency Panel
 * Design: Mission Control — transparency trace + black box removal policy
 */

import { usePipeline } from '@/contexts/PipelineContext';

export function TransparencyPanel() {
  const { pipelineData } = usePipeline();

  if (!pipelineData) {
    return (
      <div className="rounded-lg p-8 text-center" style={{ background: 'var(--navy2)', border: '1px solid var(--dax-border)' }}>
        <div className="text-sm" style={{ color: 'var(--dax-text3)' }}>
          Run the pipeline to see transparency data
        </div>
      </div>
    );
  }

  const { transparency_trace, black_box_removal } = pipelineData;
  const opaqueCount = transparency_trace.filter(s => s.opaque).length;

  return (
    <div>
      {/* Header */}
      <div className="flex items-center gap-4 mb-6 pb-4 border-b" style={{ borderColor: 'var(--dax-border)' }}>
        <h1 className="text-[22px] font-medium flex-1" style={{ color: 'var(--cyan)' }}>Transparency</h1>
        <span className="text-xs" style={{ color: 'var(--dax-text3)' }}>
          {transparency_trace.length} steps · {opaqueCount} opaque
        </span>
      </div>

      {/* Black Box Removal Policy */}
      <div className="mb-6">
        <SectionHeader title="Black Box Removal Policy" />
        <div className="rounded-lg p-4" style={{ background: 'var(--navy2)', border: '1px solid var(--dax-border)' }}>
          {black_box_removal.status ? (
            <>
              <div className="flex gap-2 flex-wrap mb-3">
                <span className="text-[11px] px-2 py-0.5 rounded" style={{ background: 'var(--blue1)', color: 'var(--cyan2)' }}>
                  Status: {black_box_removal.status}
                </span>
                <span className={`text-[11px] px-2 py-0.5 rounded`}
                  style={{
                    background: black_box_removal.enabled ? '#003a15' : '#3a0000',
                    color: black_box_removal.enabled ? '#0f0' : '#f88',
                  }}>
                  {black_box_removal.enabled ? 'Enabled' : 'Disabled'}
                </span>
              </div>
              <div className="space-y-1">
                {Object.entries(black_box_removal.policy).map(([k, v]) => (
                  <div key={k} className="text-[11px]" style={{ color: 'var(--dax-text3)' }}>
                    <span style={{ color: 'var(--cyan2)' }}>{k}:</span> {String(v)}
                  </div>
                ))}
              </div>
              {black_box_removal.notes.length > 0 && (
                <div className="mt-3 pt-3 border-t" style={{ borderColor: 'var(--dax-border)' }}>
                  {black_box_removal.notes.map((n, i) => (
                    <div key={i} className="text-[11px] mt-1" style={{ color: 'var(--dax-text2)' }}>• {n}</div>
                  ))}
                </div>
              )}
            </>
          ) : (
            <div className="text-xs" style={{ color: 'var(--dax-text3)' }}>No policy data available.</div>
          )}
        </div>
      </div>

      {/* Transparency Trace */}
      <SectionHeader title="Transparency Trace" />
      <div className="rounded-lg overflow-hidden" style={{ background: 'var(--navy2)', border: '1px solid var(--dax-border)' }}>
        {transparency_trace.length === 0 ? (
          <div className="p-4 text-xs" style={{ color: 'var(--dax-text3)' }}>No transparency trace in this run.</div>
        ) : (
          transparency_trace.map((step, i) => (
            <div
              key={i}
              className="grid gap-2 px-3 py-2.5 border-b last:border-b-0"
              style={{
                gridTemplateColumns: '90px 1fr auto',
                borderColor: 'var(--dax-border)',
                alignItems: 'start',
              }}
            >
              <span className="text-[11px] font-medium tracking-wider" style={{ color: 'var(--cyan2)' }}>
                {step.layer_name}
              </span>
              <span className="text-[11px]" style={{ color: 'var(--dax-text2)' }}>
                {Array.isArray(step.rationale) ? step.rationale.join(' · ') : step.rationale}
              </span>
              <span className="text-right">
                {step.opaque ? (
                  <span className="text-[10px] px-1.5 py-0.5 rounded whitespace-nowrap" style={{ background: '#3a0000', color: '#f88' }}>OPAQUE</span>
                ) : (
                  <span className="text-[10px] px-1.5 py-0.5 rounded whitespace-nowrap" style={{ background: '#003a15', color: '#0f0' }}>CLEAR</span>
                )}
              </span>
            </div>
          ))
        )}
      </div>
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

/**
 * DAXDA.IA Black Box Violations Panel
 * Design: Mission Control — violation alerts with severity indicators
 */

import { usePipeline } from '@/contexts/PipelineContext';
import { ViolationIcon } from '@/components/EyeIcon';

export function BBVPanel() {
  const { pipelineData } = usePipeline();

  if (!pipelineData) {
    return (
      <div className="rounded-lg p-8 text-center" style={{ background: 'var(--navy2)', border: '1px solid var(--dax-border)' }}>
        <div className="text-sm" style={{ color: 'var(--dax-text3)' }}>
          Run the pipeline to see violation data
        </div>
      </div>
    );
  }

  const { black_box_violations } = pipelineData;

  return (
    <div>
      {/* Header */}
      <div className="flex items-center gap-4 mb-6 pb-4 border-b" style={{ borderColor: 'var(--dax-border)' }}>
        <h1 className="text-[22px] font-medium flex-1" style={{ color: 'var(--cyan)' }}>Black Box Violations</h1>
        <span
          className="text-[11px] px-2 py-0.5 rounded"
          style={{
            background: black_box_violations.length > 0 ? '#3a0000' : '#003a15',
            color: black_box_violations.length > 0 ? '#f88' : '#0f0',
          }}
        >
          {black_box_violations.length} violation{black_box_violations.length === 1 ? '' : 's'}
        </span>
      </div>

      {black_box_violations.length === 0 ? (
        <div className="rounded-lg p-6 text-center" style={{ background: 'var(--navy2)', border: '1px solid var(--dax-border)' }}>
          <div className="text-[11px] px-2 py-0.5 rounded inline-block" style={{ background: '#003a15', color: '#0f0' }}>
            No violations detected
          </div>
          <p className="text-xs mt-3" style={{ color: 'var(--dax-text3)' }}>
            All layers passed transparency requirements.
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {black_box_violations.map((v, i) => (
            <div
              key={i}
              className="rounded-md p-4"
              style={{
                background: '#1a000033',
                border: `1px solid ${v.severity === 'high' ? '#f44' : v.severity === 'medium' ? '#fa0' : '#f443'}`,
              }}
            >
              <div className="flex items-center gap-2">
                <ViolationIcon />
                <span className="text-xs font-medium" style={{ color: 'var(--halt)' }}>{v.layer_name}</span>
                <span
                  className="ml-auto text-[11px] px-2 py-0.5 rounded"
                  style={{ background: '#3a0000', color: '#f88' }}
                >
                  {v.severity}
                </span>
              </div>
              <div className="text-[11px] mt-2" style={{ color: 'var(--dax-text2)' }}>
                {v.reason}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

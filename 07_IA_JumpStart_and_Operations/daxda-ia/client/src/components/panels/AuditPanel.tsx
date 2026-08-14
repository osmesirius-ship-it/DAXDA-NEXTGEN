/**
 * DAXDA.IA Audit Trace Panel
 * Design: Mission Control — tabular trace records with filtering
 */

import { useState } from 'react';
import { usePipeline } from '@/contexts/PipelineContext';

export function AuditPanel() {
  const { pipelineData } = usePipeline();
  const [filterLayer, setFilterLayer] = useState('');
  const [page, setPage] = useState(0);
  const pageSize = 50;

  if (!pipelineData) {
    return (
      <div className="rounded-lg p-8 text-center" style={{ background: 'var(--navy2)', border: '1px solid var(--dax-border)' }}>
        <div className="text-sm" style={{ color: 'var(--dax-text3)' }}>
          Run the pipeline to see audit trace
        </div>
      </div>
    );
  }

  const { audit } = pipelineData;
  const records = audit.records;
  const uniqueLayers = Array.from(new Set(records.map(r => r.layer)));

  const filtered = filterLayer ? records.filter(r => r.layer === filterLayer) : records;
  const totalPages = Math.ceil(filtered.length / pageSize);
  const pageRecords = filtered.slice(page * pageSize, (page + 1) * pageSize);

  return (
    <div>
      {/* Header */}
      <div className="flex items-center gap-4 mb-6 pb-4 border-b" style={{ borderColor: 'var(--dax-border)' }}>
        <h1 className="text-[22px] font-medium flex-1" style={{ color: 'var(--cyan)' }}>Audit Trace</h1>
        <span className="text-xs" style={{ color: 'var(--dax-text3)' }}>
          {records.length} records
        </span>
      </div>

      {/* Filter */}
      <div className="flex items-center gap-3 mb-4">
        <select
          value={filterLayer}
          onChange={e => { setFilterLayer(e.target.value); setPage(0); }}
          className="px-2.5 py-2 rounded-md text-xs"
          style={{ background: 'var(--navy3)', border: '1px solid var(--dax-border)', color: 'var(--dax-text2)' }}
        >
          <option value="">All Layers</option>
          {uniqueLayers.map(l => <option key={l} value={l}>{l}</option>)}
        </select>
        <span className="text-[11px]" style={{ color: 'var(--dax-text3)' }}>
          Showing {filtered.length} records
        </span>
      </div>

      {/* Table */}
      <div className="rounded-lg overflow-hidden" style={{ background: 'var(--navy2)', border: '1px solid var(--dax-border)' }}>
        <div className="overflow-x-auto">
          <table className="w-full text-[11px]" style={{ borderCollapse: 'collapse' }}>
            <thead>
              <tr>
                <th className="text-left px-2 py-2 font-normal tracking-wider text-[10px] border-b" style={{ color: 'var(--dax-text3)', borderColor: 'var(--dax-border)' }}>#</th>
                <th className="text-left px-2 py-2 font-normal tracking-wider text-[10px] border-b" style={{ color: 'var(--dax-text3)', borderColor: 'var(--dax-border)' }}>OP_ID</th>
                <th className="text-left px-2 py-2 font-normal tracking-wider text-[10px] border-b" style={{ color: 'var(--dax-text3)', borderColor: 'var(--dax-border)' }}>LAYER</th>
                <th className="text-left px-2 py-2 font-normal tracking-wider text-[10px] border-b" style={{ color: 'var(--dax-text3)', borderColor: 'var(--dax-border)' }}>NAME</th>
                <th className="text-left px-2 py-2 font-normal tracking-wider text-[10px] border-b" style={{ color: 'var(--dax-text3)', borderColor: 'var(--dax-border)' }}>STATUS</th>
                <th className="text-left px-2 py-2 font-normal tracking-wider text-[10px] border-b" style={{ color: 'var(--dax-text3)', borderColor: 'var(--dax-border)' }}>MS</th>
              </tr>
            </thead>
            <tbody>
              {pageRecords.map((r, i) => (
                <tr key={i} className="hover:bg-[var(--navy3)] transition-colors">
                  <td className="px-2 py-1 border-b" style={{ color: 'var(--dax-text2)', borderColor: 'var(--navy3)' }}>{r.index}</td>
                  <td className="px-2 py-1 border-b font-mono" style={{ color: 'var(--cyan2)', borderColor: 'var(--navy3)' }}>{r.op_id}</td>
                  <td className="px-2 py-1 border-b" style={{ color: 'var(--dax-text3)', borderColor: 'var(--navy3)' }}>{r.layer}</td>
                  <td className="px-2 py-1 border-b" style={{ color: 'var(--dax-text2)', borderColor: 'var(--navy3)' }}>{r.name}</td>
                  <td className="px-2 py-1 border-b" style={{ borderColor: 'var(--navy3)' }}>
                    <span style={{ color: r.status === 'pass' ? 'var(--accept)' : 'var(--halt)' }}>
                      ● {r.status}
                    </span>
                  </td>
                  <td className="px-2 py-1 border-b" style={{ color: 'var(--dax-text3)', borderColor: 'var(--navy3)' }}>{r.elapsed_ms}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex items-center justify-between mt-4">
          <button
            onClick={() => setPage(p => Math.max(0, p - 1))}
            disabled={page === 0}
            className="px-3 py-1.5 rounded text-xs disabled:opacity-30"
            style={{ background: 'var(--navy3)', border: '1px solid var(--dax-border)', color: 'var(--dax-text2)' }}
          >
            ← Prev
          </button>
          <span className="text-[11px]" style={{ color: 'var(--dax-text3)' }}>
            Page {page + 1} of {totalPages}
          </span>
          <button
            onClick={() => setPage(p => Math.min(totalPages - 1, p + 1))}
            disabled={page >= totalPages - 1}
            className="px-3 py-1.5 rounded text-xs disabled:opacity-30"
            style={{ background: 'var(--navy3)', border: '1px solid var(--dax-border)', color: 'var(--dax-text2)' }}
          >
            Next →
          </button>
        </div>
      )}

      {/* Export */}
      <div className="flex gap-2 mt-4">
        <button
          className="px-3 py-1.5 rounded text-xs transition-colors hover:border-[var(--cyan)] hover:text-[var(--cyan)]"
          style={{ background: 'var(--navy3)', border: '1px solid var(--dax-border)', color: 'var(--dax-text2)' }}
          onClick={() => {
            const text = JSON.stringify(pipelineData.audit, null, 2);
            const blob = new Blob([text], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url; a.download = 'DAXDA-audit.json'; a.click();
            URL.revokeObjectURL(url);
          }}
        >
          Export JSON
        </button>
        <button
          className="px-3 py-1.5 rounded text-xs transition-colors hover:border-[var(--cyan)] hover:text-[var(--cyan)]"
          style={{ background: 'var(--navy3)', border: '1px solid var(--dax-border)', color: 'var(--dax-text2)' }}
          onClick={() => {
            const lines = ['# DAXDA.IA Audit Trace\n', `Trail ID: ${pipelineData.audit.trail_id}\n`, '| # | OP_ID | Layer | Name | Status | ms |', '|---|-------|-------|------|--------|---|'];
            records.slice(0, 200).forEach(r => {
              lines.push(`| ${r.index} | ${r.op_id} | ${r.layer} | ${r.name} | ${r.status} | ${r.elapsed_ms} |`);
            });
            const blob = new Blob([lines.join('\n')], { type: 'text/markdown' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url; a.download = 'DAXDA-audit.md'; a.click();
            URL.revokeObjectURL(url);
          }}
        >
          Export Markdown
        </button>
      </div>
    </div>
  );
}

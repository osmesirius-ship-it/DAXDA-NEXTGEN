/**
 * DAXDA.IA Sidebar Navigation
 * Design: Mission Control — fixed left rail with logo + nav items + status
 */

import { EyeIcon, EyeIconDanger, PlayIcon } from './EyeIcon';
import { usePipeline } from '@/contexts/PipelineContext';

const navItems = [
  { id: 'run' as const, label: 'Run Pipeline', icon: 'play' },
  { id: 'transparency' as const, label: 'Transparency', icon: 'eye' },
  { id: 'bbv' as const, label: 'Black Box', icon: 'danger' },
  { id: 'audit' as const, label: 'Audit Trace', icon: 'eye' },
  { id: 'memory' as const, label: 'Memory', icon: 'eye' },
];

export function Sidebar() {
  const { activeTab, setActiveTab, pipelineData, statusMsg, statusColor } = usePipeline();

  const transBadge = pipelineData?.transparency_trace?.length ?? 0;
  const bbvBadge = pipelineData?.black_box_violations?.length ?? 0;

  return (
    <aside className="w-[220px] min-h-screen border-r flex flex-col gap-4 p-4"
      style={{ background: 'var(--navy2)', borderColor: 'var(--dax-border)' }}>
      {/* Logo */}
      <div className="flex items-center gap-2.5 pb-4 border-b" style={{ borderColor: 'var(--dax-border)' }}>
        <EyeIcon size="lg" />
        <div>
          <div className="text-lg font-medium tracking-widest" style={{ color: 'var(--cyan)' }}>DAXDA.IA</div>
          <div className="text-[10px] tracking-[3px] mt-0.5" style={{ color: 'var(--dax-text3)' }}>NICOLE PROTOCOL</div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex flex-col gap-1">
        {navItems.map(item => (
          <button
            key={item.id}
            onClick={() => setActiveTab(item.id)}
            className="flex items-center gap-2 px-2.5 py-2 rounded-md text-left transition-colors duration-150 w-full"
            style={{
              background: activeTab === item.id ? 'var(--navy3)' : 'transparent',
              color: activeTab === item.id ? 'var(--cyan)' : 'var(--dax-text2)',
            }}
          >
            {item.icon === 'play' && <PlayIcon />}
            {item.icon === 'eye' && <EyeIcon size="sm" />}
            {item.icon === 'danger' && <EyeIconDanger size="sm" />}
            <span className="text-xs">{item.label}</span>
            {item.id === 'transparency' && transBadge > 0 && (
              <span className="ml-auto text-[10px] px-1.5 py-0.5 rounded-full"
                style={{ background: 'var(--blue1)', color: 'var(--cyan2)' }}>
                {transBadge}
              </span>
            )}
            {item.id === 'bbv' && bbvBadge > 0 && (
              <span className="ml-auto text-[10px] px-1.5 py-0.5 rounded-full"
                style={{ background: '#3a0000', color: '#f88' }}>
                {bbvBadge}
              </span>
            )}
          </button>
        ))}
      </nav>

      {/* Status */}
      <div className="mt-auto pt-4 border-t" style={{ borderColor: 'var(--dax-border)' }}>
        <div className="flex items-center gap-1.5 text-[11px]" style={{ color: 'var(--dax-text3)' }}>
          <span className="w-1.5 h-1.5 rounded-full inline-block"
            style={{ background: statusColor }} />
          <span className="truncate">{statusMsg}</span>
        </div>
      </div>
    </aside>
  );
}

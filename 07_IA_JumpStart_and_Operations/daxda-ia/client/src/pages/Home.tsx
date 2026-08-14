/**
 * DAXDA.IA Home Page
 * Design: Mission Control — sidebar + main content area with tab switching
 */

import { PipelineProvider, usePipeline } from '@/contexts/PipelineContext';
import { Sidebar } from '@/components/Sidebar';
import { RunPanel } from '@/components/panels/RunPanel';
import { TransparencyPanel } from '@/components/panels/TransparencyPanel';
import { BBVPanel } from '@/components/panels/BBVPanel';
import { AuditPanel } from '@/components/panels/AuditPanel';
import { MemoryPanel } from '@/components/panels/MemoryPanel';

function MainContent() {
  const { activeTab } = usePipeline();

  return (
    <main className="flex-1 p-6 overflow-auto min-h-screen" style={{ background: 'var(--navy)' }}>
      {activeTab === 'run' && <RunPanel />}
      {activeTab === 'transparency' && <TransparencyPanel />}
      {activeTab === 'bbv' && <BBVPanel />}
      {activeTab === 'audit' && <AuditPanel />}
      {activeTab === 'memory' && <MemoryPanel />}
    </main>
  );
}

export default function Home() {
  return (
    <PipelineProvider>
      <div className="flex min-h-screen" style={{ background: 'var(--navy)' }}>
        <Sidebar />
        <MainContent />
      </div>
    </PipelineProvider>
  );
}

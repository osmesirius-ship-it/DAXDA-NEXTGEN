/**
 * DAXDA.IA Pipeline State Context
 * Design: Mission Control — centralized state for the entire pipeline inspector
 */

import { createContext, useContext, useState, useCallback, type ReactNode } from 'react';
import { getMockData, type PipelineData } from '@/lib/mockData';

type TabId = 'run' | 'transparency' | 'bbv' | 'audit' | 'memory';

interface PipelineState {
  activeTab: TabId;
  setActiveTab: (tab: TabId) => void;
  pipelineData: PipelineData | null;
  isRunning: boolean;
  progress: number;
  progressMsg: string;
  statusMsg: string;
  statusColor: string;
  runPipeline: (query: string, passes: number, taskMode: boolean) => Promise<void>;
}

const PipelineContext = createContext<PipelineState | null>(null);

export function PipelineProvider({ children }: { children: ReactNode }) {
  const [activeTab, setActiveTab] = useState<TabId>('run');
  const [pipelineData, setPipelineData] = useState<PipelineData | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const [progress, setProgress] = useState(0);
  const [progressMsg, setProgressMsg] = useState('');
  const [statusMsg, setStatusMsg] = useState('Ready');
  const [statusColor, setStatusColor] = useState('var(--blue4)');

  const runPipeline = useCallback(async (query: string, passes: number, taskMode: boolean) => {
    setIsRunning(true);
    setProgress(10);
    setProgressMsg('initializing pipeline…');
    setStatusMsg('Running…');
    setStatusColor('var(--blue4)');

    await new Promise(r => setTimeout(r, 400));
    setProgress(30);
    setProgressMsg('processing layers…');

    await new Promise(r => setTimeout(r, 600));
    setProgress(60);
    setProgressMsg('running stability analysis…');

    await new Promise(r => setTimeout(r, 500));
    setProgress(85);
    setProgressMsg('generating mock run…');

    await new Promise(r => setTimeout(r, 400));
    const data = getMockData(query, passes, taskMode);
    setPipelineData(data);

    setProgress(100);
    setProgressMsg('done');
    setStatusMsg('Pipeline complete · ' + new Date().toLocaleTimeString());
    setStatusColor('var(--accept)');
    setIsRunning(false);
  }, []);

  return (
    <PipelineContext.Provider value={{
      activeTab, setActiveTab,
      pipelineData, isRunning, progress, progressMsg,
      statusMsg, statusColor, runPipeline,
    }}>
      {children}
    </PipelineContext.Provider>
  );
}

export function usePipeline() {
  const ctx = useContext(PipelineContext);
  if (!ctx) throw new Error('usePipeline must be used within PipelineProvider');
  return ctx;
}

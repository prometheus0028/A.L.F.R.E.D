import React from 'react';
import { useNavigate } from 'react-router-dom';

const Settings = () => {
  const navigate = useNavigate();

  const handleReset = () => {
    if (window.confirm("RESET DEMO SYSTEM?\n\nThis clears the current local task/session state.\nNo external services will be affected.")) {
      // In a real app we would call a backend endpoint here.
      // For MVP, just reload to clear state and go to dashboard.
      window.location.href = '/dashboard';
    }
  };

  return (
    <div className="flex-1 flex flex-col h-full overflow-hidden">
      <div className="h-16 flex items-center px-8 border-b border-border shrink-0">
        <span className="font-mono text-xs tracking-widest text-text-secondary uppercase">SETTINGS / 07</span>
      </div>
      
      <div className="p-8 flex-1 overflow-y-auto">
        <h1 className="text-2xl font-bold tracking-tight mb-8 uppercase">SYSTEM CONFIGURATION</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl">
          {/* Connection */}
          <div className="border border-border p-6 bg-surface-secondary/10">
            <div className="text-xs font-mono tracking-widest text-text-secondary mb-6 border-b border-border/50 pb-2 uppercase">CONNECTION</div>
            <div className="flex justify-between items-center">
              <span className="font-mono text-sm text-text-muted">BACKEND API</span>
              <span className="font-mono text-sm tracking-widest text-accent flex items-center gap-2">
                <span className="w-2 h-2 bg-accent inline-block" /> CONNECTED
              </span>
            </div>
          </div>

          {/* Agent Components */}
          <div className="border border-border p-6 bg-surface-secondary/10">
            <div className="text-xs font-mono tracking-widest text-text-secondary mb-6 border-b border-border/50 pb-2 uppercase">AGENT COMPONENTS</div>
            <div className="space-y-2 font-mono text-sm">
              <div className="flex justify-between"><span className="text-text-muted">PLANNER</span> <span className="text-accent">OK</span></div>
              <div className="flex justify-between"><span className="text-text-muted">EXECUTOR</span> <span className="text-accent">OK</span></div>
              <div className="flex justify-between"><span className="text-text-muted">REPLANNER</span> <span className="text-accent">OK</span></div>
              <div className="flex justify-between"><span className="text-text-muted">VERIFIER</span> <span className="text-accent">OK</span></div>
              <div className="flex justify-between"><span className="text-text-muted">POLICY ENGINE</span> <span className="text-accent">OK</span></div>
            </div>
          </div>
          
          {/* Environment */}
          <div className="border border-border p-6 bg-surface-secondary/10 col-span-1 md:col-span-2">
            <div className="text-xs font-mono tracking-widest text-text-secondary mb-6 border-b border-border/50 pb-2 uppercase">DEMO ENVIRONMENT</div>
            <p className="text-sm text-text-secondary mb-6">
              Clear local task execution state and return ALFRED to its initial configuration.
            </p>
            <button 
              onClick={handleReset}
              className="px-6 py-3 border border-border font-mono text-sm tracking-widest text-status-error hover:bg-status-error hover:text-surface-primary transition-colors uppercase"
            >
              &gt; RESET SYSTEM
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Settings;

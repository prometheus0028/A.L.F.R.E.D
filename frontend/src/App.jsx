import React from 'react';
import Workspace from './pages/Workspace';

function App() {
  return (
    <div className="min-h-screen flex flex-col bg-surface-secondary">
      <header className="bg-surface-primary border-b border-border h-14 flex items-center px-6">
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 bg-accent rounded text-white flex items-center justify-center font-bold text-sm">
            A
          </div>
          <span className="font-semibold text-text-primary tracking-tight">ALFRED</span>
        </div>
        <div className="ml-auto flex items-center gap-4">
          <span className="text-xs text-text-muted font-medium px-2 py-1 bg-surface-secondary rounded border border-border">
            Agent Ready
          </span>
        </div>
      </header>
      
      <main className="flex-1 overflow-auto">
        <Workspace />
      </main>
    </div>
  );
}

export default App;

import React from 'react';

const Finance = () => {
  return (
    <div className="flex-1 flex flex-col h-full overflow-hidden">
      <div className="h-16 flex items-center px-8 border-b border-border shrink-0">
        <span className="font-mono text-xs tracking-widest text-text-secondary uppercase">FINANCE / 06</span>
      </div>
      
      <div className="p-8 flex-1 overflow-y-auto">
        <h1 className="text-2xl font-bold tracking-tight mb-8 uppercase">FINANCIAL OPERATIONS</h1>
        
        <div className="grid grid-cols-1 gap-8 max-w-4xl">
          <div className="border border-border p-6 bg-surface-secondary/20">
            <h2 className="text-lg font-mono text-text-primary uppercase mb-4">Note: Not Included in MVP</h2>
            <p className="font-mono text-sm text-text-secondary">
              The financial operations module (including automatic invoice scanning and ledger updates) is currently disabled in this demo environment.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Finance;

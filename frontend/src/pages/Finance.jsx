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
          <div className="border border-border">
            <div className="grid grid-cols-5 p-4 border-b border-border bg-surface-secondary/50 font-mono text-[10px] tracking-widest text-text-muted uppercase">
              <div>VENDOR</div>
              <div>INVOICE</div>
              <div className="text-right">AMOUNT</div>
              <div>POLICY STATUS</div>
              <div className="text-right">PAYMENT STATUS</div>
            </div>
            
            <div className="divide-y divide-border">
              <div className="grid grid-cols-5 p-4 items-center">
                <div className="font-mono text-sm text-text-primary uppercase">ACME SUPPLIES</div>
                <div className="font-mono text-sm text-text-secondary uppercase">INV-1042</div>
                <div className="font-mono text-sm text-text-primary text-right uppercase">₹3,800</div>
                <div className="font-mono text-xs tracking-widest text-accent uppercase">WITHIN POLICY</div>
                <div className="font-mono text-xs tracking-widest text-accent-amber text-right uppercase">AWAITING APPROVAL</div>
              </div>
              
              <div className="grid grid-cols-5 p-4 items-center opacity-50">
                <div className="font-mono text-sm text-text-primary uppercase">TECH CORP</div>
                <div className="font-mono text-sm text-text-secondary uppercase">INV-0991</div>
                <div className="font-mono text-sm text-text-primary text-right uppercase">₹1,200</div>
                <div className="font-mono text-xs tracking-widest text-accent uppercase">WITHIN POLICY</div>
                <div className="font-mono text-xs tracking-widest text-text-primary text-right uppercase">PAID</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Finance;

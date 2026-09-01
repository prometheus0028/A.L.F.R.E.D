import React from 'react';

const Approvals = () => {
  return (
    <div className="flex-1 flex flex-col h-full overflow-hidden">
      <div className="h-16 flex items-center px-8 border-b border-border shrink-0">
        <span className="font-mono text-xs tracking-widest text-text-secondary uppercase">APPROVALS / 03</span>
      </div>
      
      <div className="p-8 flex-1 overflow-y-auto">
        <h1 className="text-2xl font-bold tracking-tight mb-8 uppercase">PENDING AUTHORIZATIONS</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-5xl">
          {/* Approval Card */}
          <div className="border border-border p-6 bg-surface-secondary/20">
            <div className="text-xs font-mono tracking-widest text-text-secondary mb-6 border-b border-border/50 pb-2 uppercase">FINANCE INVOICE PAYMENT</div>
            
            <div className="space-y-4 mb-8">
              <div className="flex justify-between items-baseline">
                <span className="font-mono text-xs text-text-muted uppercase">VENDOR</span>
                <span className="font-mono text-sm text-text-primary uppercase">ACME SUPPLIES</span>
              </div>
              <div className="flex justify-between items-baseline">
                <span className="font-mono text-xs text-text-muted uppercase">INVOICE</span>
                <span className="font-mono text-sm text-text-primary uppercase">INV-1042</span>
              </div>
              <div className="flex justify-between items-baseline">
                <span className="font-mono text-xs text-text-muted uppercase">AMOUNT</span>
                <span className="font-mono text-lg text-text-primary uppercase">₹3,800 INR</span>
              </div>
              <div className="flex justify-between items-baseline">
                <span className="font-mono text-xs text-text-muted uppercase">POLICY</span>
                <span className="font-mono text-sm text-accent uppercase">WITHIN POLICY</span>
              </div>
              <div className="flex justify-between items-baseline">
                <span className="font-mono text-xs text-text-muted uppercase">CONTROL REQUIREMENT</span>
                <span className="font-mono text-sm text-accent-amber uppercase">USER AUTHORIZATION REQUIRED</span>
              </div>
            </div>
            
            <div className="flex gap-4">
              <button className="flex-1 py-3 border border-border text-xs font-mono tracking-widest bg-surface-secondary text-text-primary hover:bg-border transition-colors uppercase">&gt; REVIEW & APPROVE</button>
              <button className="flex-1 py-3 border border-border text-xs font-mono tracking-widest text-text-secondary hover:bg-surface-secondary transition-colors uppercase">REJECT</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Approvals;

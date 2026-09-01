import React from 'react';
import { motion } from 'framer-motion';

const ApprovalPanel = ({ approval, onApprove, onReject }) => {
  if (!approval) return null;

  return (
    <motion.div 
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="border border-border bg-surface-primary"
    >
      <div className="border-b border-border p-4 flex justify-between items-center bg-surface-secondary">
        <div className="text-xs font-mono tracking-widest text-text-primary uppercase">Authorization Required</div>
        <div className="text-xs text-text-muted cursor-pointer hover:text-text-primary">&times;</div>
      </div>
      
      <div className="p-6 font-mono">
        <div className="flex justify-between items-start mb-8">
          <div>
            <div className="text-xs text-text-muted tracking-widest uppercase mb-1">Invoice Payment</div>
            <div className="text-sm text-text-primary uppercase">{approval.vendor}</div>
          </div>
          <div className="text-right">
            <div className="text-xl text-text-primary">{approval.currency === 'INR' ? '₹' : approval.currency}{approval.amount}</div>
            <div className="text-[10px] text-text-muted uppercase tracking-widest">{approval.currency}</div>
          </div>
        </div>

        <div className="space-y-2 mb-8 text-xs border-b border-border pb-6">
          <div className="flex justify-between">
            <span className="text-text-muted uppercase tracking-widest">Invoice ID</span>
            <span className="text-text-primary">{approval.invoice_id}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-text-muted uppercase tracking-widest">Policy Check</span>
            <span className="text-text-primary uppercase">Within {approval.currency}{approval.policy?.limit} limit</span>
          </div>
          <div className="flex justify-between">
            <span className="text-text-muted uppercase tracking-widest">Vendor Status</span>
            <span className="text-text-primary uppercase">Approved</span>
          </div>
          <div className="flex justify-between">
            <span className="text-text-muted uppercase tracking-widest">Risk Level</span>
            <span className="text-text-primary uppercase">Low</span>
          </div>
        </div>

        <div className="mb-8 text-xs">
          <div className="text-text-muted uppercase tracking-widest mb-4">Policy Check Summary</div>
          <div className="space-y-2 text-text-secondary uppercase">
            {approval.policy?.vendor_approved && (
              <div className="flex gap-2"><span>&#10003;</span> Vendor is approved</div>
            )}
            {approval.policy?.within_limit && (
              <div className="flex gap-2"><span>&#10003;</span> Amount within limit</div>
            )}
            <div className="flex gap-2"><span>&#10003;</span> Category allowed</div>
            <div className="flex gap-2"><span>&#10003;</span> Payment method valid</div>
          </div>
        </div>

        <div className="flex gap-4 pt-4">
          <button 
            onClick={() => onReject(approval.approval_id, "User rejected")}
            className="flex-1 py-3 border border-border text-xs uppercase tracking-widest text-text-secondary hover:text-text-primary hover:bg-surface-secondary transition-colors"
          >
            Reject
          </button>
          <button 
            onClick={() => onApprove(approval.approval_id)}
            className="flex-1 py-3 bg-surface-secondary border border-border text-xs uppercase tracking-widest text-text-primary hover:bg-text-primary hover:text-surface-primary transition-colors"
          >
            &gt; Approve
          </button>
        </div>
        
        <div className="text-[10px] text-text-muted tracking-widest uppercase text-center mt-6">
          ALFRED will resume after your decision.
        </div>
      </div>
    </motion.div>
  );
};

export default ApprovalPanel;

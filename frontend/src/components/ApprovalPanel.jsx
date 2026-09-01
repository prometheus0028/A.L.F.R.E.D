import React from 'react';
import { ShieldAlert } from 'lucide-react';

const ApprovalPanel = ({ approval, onApprove, onReject }) => {
  if (!approval) return null;

  return (
    <div className="bg-surface-primary border border-status-warning rounded-md overflow-hidden mt-6 shadow-sm">
      <div className="bg-status-warning/10 px-4 py-3 border-b border-status-warning/20 flex items-center gap-2">
        <ShieldAlert className="text-status-warning" size={18} />
        <h3 className="text-status-warning font-medium">{approval.title || "Approval Required"}</h3>
      </div>
      
      <div className="p-4 flex flex-col gap-4">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <span className="text-xs text-text-muted uppercase tracking-wider font-semibold">Vendor</span>
            <p className="text-text-primary text-sm mt-0.5">{approval.vendor}</p>
          </div>
          <div>
            <span className="text-xs text-text-muted uppercase tracking-wider font-semibold">Amount</span>
            <p className="text-text-primary text-sm mt-0.5 font-medium">{approval.currency} {approval.amount}</p>
          </div>
          <div className="col-span-2">
            <span className="text-xs text-text-muted uppercase tracking-wider font-semibold">Reason</span>
            <p className="text-text-primary text-sm mt-0.5">Pending invoice {approval.invoice_id}</p>
          </div>
        </div>

        <div className="bg-surface-secondary border border-border rounded p-3">
          <span className="text-xs text-text-muted uppercase tracking-wider font-semibold">Policy Evaluation</span>
          <ul className="mt-2 space-y-1">
            {approval.policy?.vendor_approved && (
              <li className="text-sm text-text-secondary flex items-center gap-2">
                <span className="text-status-success">✓</span> Approved vendor
              </li>
            )}
            {approval.policy?.within_limit && (
              <li className="text-sm text-text-secondary flex items-center gap-2">
                <span className="text-status-success">✓</span> Within {approval.currency} {approval.policy?.limit} limit
              </li>
            )}
          </ul>
        </div>

        <div className="flex justify-end gap-3 pt-2">
          <button 
            onClick={() => onReject(approval.approval_id, "User rejected")}
            className="px-4 py-2 border border-border rounded-md text-text-primary text-sm font-medium hover:bg-surface-secondary transition-colors"
          >
            Reject
          </button>
          <button 
            onClick={() => onApprove(approval.approval_id)}
            className="px-4 py-2 bg-accent text-white rounded-md text-sm font-medium hover:bg-accent-hover transition-colors"
          >
            Approve
          </button>
        </div>
      </div>
    </div>
  );
};

export default ApprovalPanel;

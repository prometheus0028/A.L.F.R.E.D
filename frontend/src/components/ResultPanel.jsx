import React from 'react';
import { CheckCircle2, FileText, Link as LinkIcon } from 'lucide-react';

const ResultPanel = ({ result }) => {
  if (!result) return null;

  return (
    <div className="bg-surface-primary border border-status-success rounded-md overflow-hidden mt-6 shadow-sm">
      <div className="bg-status-success/10 px-4 py-3 border-b border-status-success/20 flex items-center gap-2">
        <CheckCircle2 className="text-status-success" size={18} />
        <h3 className="text-status-success font-medium">Task Complete</h3>
      </div>
      
      <div className="p-4 flex flex-col gap-4">
        <div>
          <h4 className="text-text-primary font-medium">{result.summary || result.title}</h4>
        </div>

        {result.type === 'meeting_brief' && (
          <div className="grid grid-cols-2 gap-4 bg-surface-secondary border border-border p-3 rounded">
            <div>
              <span className="text-xs text-text-muted uppercase tracking-wider font-semibold block mb-2">Sources</span>
              <ul className="text-sm text-text-secondary space-y-1">
                {result.evidence?.map((item, i) => <li key={i}>{item}</li>)}
              </ul>
            </div>
            <div>
              <span className="text-xs text-text-muted uppercase tracking-wider font-semibold block mb-2">Created</span>
              <div className="flex items-center gap-2 text-sm text-text-primary">
                <FileText size={14} className="text-text-muted" />
                {result.file_name}
              </div>
            </div>
          </div>
        )}

        {result.type === 'payment' && (
          <div className="grid grid-cols-2 gap-4 bg-surface-secondary border border-border p-3 rounded">
            <div>
              <span className="text-xs text-text-muted uppercase tracking-wider font-semibold block mb-2">Details</span>
              <div className="text-sm text-text-secondary space-y-1">
                <p>Vendor: <span className="text-text-primary font-medium">{result.vendor}</span></p>
                <p>Amount: <span className="text-text-primary font-medium">{result.currency} {result.amount}</span></p>
              </div>
            </div>
            <div>
              <span className="text-xs text-text-muted uppercase tracking-wider font-semibold block mb-2">Transaction</span>
              <div className="flex items-center gap-2 text-sm text-accent">
                <LinkIcon size={14} />
                <a href="#" className="hover:underline">{result.transaction_hash}</a>
              </div>
            </div>
            <div className="col-span-2 mt-2">
              <span className="text-xs text-text-muted uppercase tracking-wider font-semibold block mb-2">Verification</span>
              <ul className="text-sm text-text-secondary flex gap-4">
                {result.evidence?.map((item, i) => (
                  <li key={i} className="flex items-center gap-1">
                    <span className="text-status-success">✓</span> {item}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ResultPanel;

import React from 'react';
import { motion } from 'framer-motion';

const ResultPanel = ({ result }) => {
  if (!result) return null;

  return (
    <motion.div 
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="border border-border bg-surface-primary"
    >
      <div className="border-b border-border p-4 flex justify-between items-center bg-surface-secondary">
        <div className="text-xs font-mono tracking-widest text-text-primary uppercase">Task Complete_</div>
        <div className="text-xs text-text-muted cursor-pointer hover:text-text-primary">&times;</div>
      </div>
      
      <div className="p-6 font-mono">
        <div className="text-sm text-text-primary uppercase mb-8">
          {result.summary || result.title}
        </div>

        {result.type === 'meeting_brief' && (
          <div className="space-y-6">
            <div className="grid grid-cols-2 gap-6 text-xs">
              <div>
                <div className="text-text-muted uppercase tracking-widest border-b border-border pb-2 mb-2">Sources</div>
                <div className="space-y-1 text-text-secondary uppercase">
                  {result.evidence?.map((item, i) => <div key={i}>{item}</div>)}
                </div>
              </div>
              <div>
                <div className="text-text-muted uppercase tracking-widest border-b border-border pb-2 mb-2">Artifact</div>
                <div className="flex items-center gap-2 text-text-primary">
                  <span className="opacity-50">&#9632;</span>
                  {result.file_name}
                </div>
              </div>
            </div>
            
            <div className="text-xs">
              <div className="text-text-muted uppercase tracking-widest border-b border-border pb-2 mb-2">Verification</div>
              <div className="flex items-center gap-2 text-text-primary uppercase">
                ALL CHECKS PASSED
              </div>
            </div>
          </div>
        )}

        {result.type === 'payment' && (
          <div className="space-y-6">
            <div className="grid grid-cols-2 gap-6 text-xs">
              <div>
                <div className="text-text-muted uppercase tracking-widest border-b border-border pb-2 mb-2">Details</div>
                <div className="space-y-1 text-text-secondary uppercase">
                  <div>Vendor: <span className="text-text-primary">{result.vendor}</span></div>
                  <div>Amount: <span className="text-text-primary">{result.currency} {result.amount}</span></div>
                </div>
              </div>
              <div>
                <div className="text-text-muted uppercase tracking-widest border-b border-border pb-2 mb-2">Transaction</div>
                <div className="flex items-center gap-2 text-accent">
                  <span className="opacity-50">&gt;&gt;</span>
                  <a href="#" className="hover:underline">{result.transaction_hash}</a>
                </div>
              </div>
            </div>
            
            <div className="text-xs">
              <div className="text-text-muted uppercase tracking-widest border-b border-border pb-2 mb-2">Verification</div>
              <div className="flex gap-4 text-text-secondary uppercase">
                {result.evidence?.map((item, i) => (
                  <div key={i} className="flex items-center gap-2">
                    <span className="text-accent">&#10003;</span> {item}
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </motion.div>
  );
};

export default ResultPanel;

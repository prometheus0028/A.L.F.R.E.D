import React from 'react';
import { motion } from 'framer-motion';

const ExecutionTimeline = ({ actions, status }) => {
  if (!actions || actions.length === 0) {
    if (status === 'created' || status === 'planning') {
      return <div className="text-[10px] font-mono tracking-widest uppercase text-text-muted">Waiting to execute...</div>;
    }
    return <div className="text-[10px] font-mono tracking-widest uppercase text-text-muted">No execution history available.</div>;
  }

  return (
    <div className="flex flex-col gap-4 font-mono">
      {actions.map((action, index) => {
        const isRecovered = action.status === 'replanning';
        const isRunning = action.status === 'running';
        const isCompleted = action.status === 'completed';
        const timeStr = action.timestamp ? new Date(action.timestamp).toLocaleTimeString([], { hour12: false }) : '00:00:00';

        if (isRecovered) {
          return (
            <motion.div 
              key={action.id || index}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              className="border-y border-border py-4 my-2 text-accent-amber"
            >
              <div className="text-xs tracking-widest uppercase mb-2">REPLAN / {String(index + 1).padStart(2, '0')}</div>
              <div className="text-xs mb-2">{action.message || 'ADAPTING EXECUTION PATH...'}</div>
              <div className="text-xs uppercase flex gap-2">
                <span>&rarr;</span> {action.summary || action.operation || 'SEARCHING ALTERNATIVE SOURCES'}
              </div>
            </motion.div>
          );
        }

        return (
          <motion.div 
            key={action.id || index} 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex gap-4 text-xs"
          >
            <div className="text-text-muted w-20 shrink-0">[{timeStr}]</div>
            <div className="flex flex-col gap-1">
              <div className={`uppercase tracking-widest ${isRunning ? 'text-accent' : isCompleted ? 'text-text-secondary' : 'text-text-muted'}`}>
                {action.operation || 'PROCESS'}
                {isRunning && <span className="ml-2 animate-pulse">_</span>}
              </div>
              <div className="text-[10px] text-text-muted">
                {action.summary || 'Executing action...'}
              </div>
            </div>
          </motion.div>
        );
      })}
    </div>
  );
};

export default ExecutionTimeline;

import React from 'react';
import { Check, Loader2, RotateCw } from 'lucide-react';

const ExecutionTimeline = ({ actions, status }) => {
  if (!actions || actions.length === 0) {
    if (status === 'created' || status === 'planning') {
      return <div className="text-sm text-text-muted">Waiting to execute...</div>;
    }
    return <div className="text-sm text-text-muted">No execution history available.</div>;
  }

  return (
    <div className="flex flex-col gap-4">
      {actions.map((action, index) => {
        const isRecovered = action.status === 'replanning';
        const isRunning = action.status === 'running';
        const isCompleted = action.status === 'completed';

        return (
          <div key={action.id || index} className="flex gap-3 relative">
            {index !== actions.length - 1 && (
              <div className="absolute left-2.5 top-6 bottom-[-16px] w-px bg-border" />
            )}
            <div className={`mt-0.5 flex items-center justify-center w-5 h-5 rounded-full z-10 ${
              isCompleted ? 'bg-status-success/10 text-status-success' : 
              isRunning ? 'bg-accent/10 text-accent' : 
              isRecovered ? 'bg-status-warning/10 text-status-warning' : 
              'bg-surface-tertiary text-text-muted'
            }`}>
              {isCompleted && <Check size={12} />}
              {isRunning && <Loader2 size={12} className="animate-spin" />}
              {isRecovered && <RotateCw size={12} />}
              {!isCompleted && !isRunning && !isRecovered && <div className="w-1.5 h-1.5 bg-current rounded-full" />}
            </div>
            <div className="flex flex-col pb-1">
              <span className={`text-sm ${isRunning ? 'text-text-primary font-medium' : 'text-text-secondary'}`}>
                {action.summary || action.operation || 'Executing action...'}
              </span>
              {isRecovered && action.message && (
                <span className="text-xs text-status-warning mt-1">{action.message}</span>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default ExecutionTimeline;

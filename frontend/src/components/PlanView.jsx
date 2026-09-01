import React from 'react';
import { Check, Circle, Loader2, FastForward } from 'lucide-react';

const PlanView = ({ plan }) => {
  if (!plan || plan.length === 0) return (
    <div className="text-text-muted text-sm py-4">No plan generated yet.</div>
  );

  return (
    <div className="flex flex-col gap-2">
      {plan.map((step, index) => {
        const isCompleted = step.status === 'completed';
        const isRunning = step.status === 'running';
        const isSkipped = step.status === 'skipped';
        
        return (
          <div key={step.id} className="flex items-center gap-3 text-sm">
            <span className="text-text-muted font-medium w-4">{index + 1}</span>
            <div className={`flex items-center justify-center w-5 h-5 rounded-full ${isCompleted ? 'bg-status-success/10 text-status-success' : isRunning ? 'bg-accent/10 text-accent' : isSkipped ? 'bg-surface-tertiary text-text-muted' : 'border border-border text-border'}`}>
              {isCompleted && <Check size={12} />}
              {isRunning && <Loader2 size={12} className="animate-spin" />}
              {isSkipped && <FastForward size={12} />}
              {!isCompleted && !isRunning && !isSkipped && <Circle size={8} className="fill-border" />}
            </div>
            <span className={`${isCompleted ? 'text-text-secondary line-through' : isRunning ? 'text-text-primary font-medium' : 'text-text-secondary'}`}>
              {step.description}
            </span>
          </div>
        );
      })}
    </div>
  );
};

export default PlanView;

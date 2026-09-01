import React from 'react';
import { motion } from 'framer-motion';

const PlanView = ({ plan }) => {
  if (!plan || plan.length === 0) return (
    <div className="text-text-muted text-[10px] font-mono tracking-widest uppercase">WAITING FOR PLAN...</div>
  );

  return (
    <div className="flex flex-col gap-4">
      {plan.map((step, index) => {
        const isCompleted = step.status === 'completed';
        const isRunning = step.status === 'running';
        const isSkipped = step.status === 'skipped';
        
        let textColor = 'text-text-muted';
        if (isCompleted) textColor = 'text-accent';
        else if (isRunning) textColor = 'text-text-primary';
        
        return (
          <div key={step.id} className={`flex items-start gap-4 font-mono text-xs tracking-widest ${textColor}`}>
            <span className="w-4 opacity-50">{String(index + 1).padStart(2, '0')}</span>
            <span className="flex-1 uppercase">{step.description}</span>
            <div className="w-2 flex justify-end">
              {isRunning && (
                <motion.span
                  className="w-1.5 h-3 bg-text-primary block"
                  animate={{ opacity: [1, 0, 1] }}
                  transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                />
              )}
              {isCompleted && (
                <span className="w-1.5 h-1.5 rounded-full bg-accent mt-1" />
              )}
              {isSkipped && (
                <span className="text-[10px] opacity-50">&gt;&gt;</span>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default PlanView;

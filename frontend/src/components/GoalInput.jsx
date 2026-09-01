import React, { useState } from 'react';

const GoalInput = ({ onStartTask, isExecuting }) => {
  const [goal, setGoal] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (goal.trim() && !isExecuting) {
      onStartTask(goal);
      setGoal("");
    }
  };

  return (
    <div>
      <div className="text-[10px] font-mono tracking-widest text-text-muted mb-4 uppercase">What should ALFRED accomplish today?</div>
      
      <form onSubmit={handleSubmit} className="flex gap-4 items-stretch max-w-3xl">
        <div className="flex-1 flex items-center border border-border bg-surface-secondary relative font-mono">
          <span className="text-text-muted px-4 select-none">&gt;</span>
          <input 
            type="text"
            value={goal}
            onChange={(e) => setGoal(e.target.value)}
            placeholder="e.g. Prepare me for tomorrow's meeting with Rahul"
            disabled={isExecuting}
            className="flex-1 bg-transparent py-3 pr-4 text-text-primary text-sm focus:outline-none disabled:opacity-50"
          />
        </div>
        
        <button 
          type="submit"
          disabled={!goal.trim() || isExecuting}
          className="flex items-center justify-center gap-2 bg-surface-secondary border border-border text-text-primary px-8 text-sm font-mono tracking-widest hover:bg-text-primary hover:text-surface-primary disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          &gt; RUN
        </button>
      </form>
      
      <div className="mt-8">
        <div className="text-[10px] font-mono tracking-widest text-text-muted mb-4 uppercase">Try these:</div>
        <div className="flex gap-4">
          <button onClick={() => setGoal("Prepare me for tomorrow's meeting with Rahul")} className="px-4 py-1.5 border border-border text-xs font-mono tracking-widest text-text-secondary hover:text-text-primary hover:border-text-secondary transition-colors">
            PREPARE MEETING
          </button>
          <button onClick={() => setGoal("Handle the pending invoice")} className="px-4 py-1.5 border border-border text-xs font-mono tracking-widest text-text-secondary hover:text-text-primary hover:border-text-secondary transition-colors">
            HANDLE PENDING INVOICE
          </button>
          <button onClick={() => setGoal("Summarize project updates from last week")} className="px-4 py-1.5 border border-border text-xs font-mono tracking-widest text-text-secondary hover:text-text-primary hover:border-text-secondary transition-colors">
            PROJECT UPDATE
          </button>
        </div>
      </div>
    </div>
  );
};

export default GoalInput;

import React, { useState } from 'react';
import { Play } from 'lucide-react';

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
    <div className="bg-surface-primary border border-border p-6 rounded-md mb-6">
      <h2 className="text-text-primary font-medium mb-4">What should ALFRED accomplish?</h2>
      <form onSubmit={handleSubmit} className="flex gap-3">
        <input 
          type="text"
          value={goal}
          onChange={(e) => setGoal(e.target.value)}
          placeholder="e.g. Prepare me for tomorrow's meeting with Rahul"
          disabled={isExecuting}
          className="flex-1 bg-surface-secondary border border-border rounded-md px-4 py-2 text-text-primary focus:outline-none focus:border-accent disabled:opacity-50"
        />
        <button 
          type="submit"
          disabled={!goal.trim() || isExecuting}
          className="flex items-center gap-2 bg-accent text-white px-6 py-2 rounded-md font-medium hover:bg-accent-hover disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          <Play size={16} />
          Run
        </button>
      </form>
    </div>
  );
};

export default GoalInput;

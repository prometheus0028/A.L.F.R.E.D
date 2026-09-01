import React from 'react';
import StatusIndicator from './StatusIndicator';

const TaskHeader = ({ task }) => {
  if (!task) return null;

  return (
    <div className="bg-surface-primary border-b border-border p-6 flex items-center justify-between">
      <div className="flex flex-col">
        <span className="text-text-muted text-sm font-medium mb-1">Active Goal</span>
        <h1 className="text-text-primary text-xl font-semibold">{task.goal}</h1>
      </div>
      <div>
        <StatusIndicator status={task.status} />
      </div>
    </div>
  );
};

export default TaskHeader;

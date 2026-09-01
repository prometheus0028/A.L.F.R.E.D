import React from 'react';
import StatusIndicator from './StatusIndicator';

const TaskHeader = ({ task, activeTab, onTabChange }) => {
  if (!task) return null;

  const Tab = ({ label, active }) => (
    <div 
      onClick={() => onTabChange(label)}
      className={`py-3 border-b-2 text-[10px] font-mono tracking-widest uppercase cursor-pointer transition-colors ${
        active 
          ? 'border-text-primary text-text-primary' 
          : 'border-transparent text-text-muted hover:text-text-secondary'
      }`}
    >
      {label}
    </div>
  );

  return (
    <div className="border-b border-border bg-surface-primary/95">
      <div className="p-6">
        <div className="text-[10px] font-mono tracking-widest text-text-muted mb-4 uppercase">
          ACTIVE TASK_ <span className="opacity-50 ml-2">/ 001</span>
        </div>
        
        <div className="flex items-start justify-between">
          <h1 className="text-2xl md:text-3xl font-bold tracking-tight text-text-primary max-w-4xl uppercase">
            {task.goal}
          </h1>
          
          <div className="flex items-center gap-4">
            <div className="text-[10px] font-mono tracking-widest text-text-secondary uppercase">
              STATUS: {task.status}
            </div>
            <StatusIndicator status={task.status} />
          </div>
        </div>
      </div>
      
      <div className="flex px-6 gap-8 border-t border-border/50">
        <Tab label="OVERVIEW" active={activeTab === 'OVERVIEW'} />
        <Tab label="PLAN" active={activeTab === 'PLAN'} />
        <Tab label="EXECUTION" active={activeTab === 'EXECUTION'} />
        <Tab label="DETAILS" active={activeTab === 'DETAILS'} />
        <Tab label="FILES" active={activeTab === 'FILES'} />
      </div>
    </div>
  );
};

export default TaskHeader;

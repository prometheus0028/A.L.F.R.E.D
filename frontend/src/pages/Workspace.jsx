import React, { useState } from 'react';
import GoalInput from '../components/GoalInput';
import TaskHeader from '../components/TaskHeader';
import PlanView from '../components/PlanView';
import ExecutionTimeline from '../components/ExecutionTimeline';
import ApprovalPanel from '../components/ApprovalPanel';
import ResultPanel from '../components/ResultPanel';
import { useTaskEvents } from '../hooks/taskEvents';
import { createTask } from '../services/api';

const Workspace = () => {
  const [taskId, setTaskId] = useState(null);
  const { taskState, loading, error, approve, reject } = useTaskEvents(taskId);

  const handleStartTask = async (goal) => {
    try {
      const response = await createTask(goal);
      setTaskId(response.task_id);
    } catch (err) {
      console.error("Failed to start task", err);
    }
  };

  const isExecuting = taskState && !['completed', 'failed'].includes(taskState.status);

  return (
    <div className="max-w-6xl mx-auto p-8">
      <GoalInput onStartTask={handleStartTask} isExecuting={isExecuting} />
      
      {taskState && (
        <div className="bg-surface-primary border border-border rounded-md shadow-sm overflow-hidden flex flex-col min-h-[500px]">
          <TaskHeader task={taskState} />
          
          <div className="flex flex-1 overflow-hidden">
            <div className="w-1/3 border-r border-border p-6 bg-surface-secondary/30 overflow-y-auto">
              <h3 className="text-xs font-semibold text-text-muted uppercase tracking-wider mb-4">Plan</h3>
              <PlanView plan={taskState.plan} />
            </div>
            
            <div className="flex-1 p-6 overflow-y-auto bg-surface-primary">
              <h3 className="text-xs font-semibold text-text-muted uppercase tracking-wider mb-4">Execution</h3>
              <ExecutionTimeline actions={taskState.actions} status={taskState.status} />
              
              {taskState.status === 'waiting_approval' && taskState.approval && (
                <ApprovalPanel 
                  approval={taskState.approval} 
                  onApprove={approve} 
                  onReject={reject} 
                />
              )}

              {taskState.status === 'completed' && taskState.result && (
                <ResultPanel result={taskState.result} />
              )}
            </div>
          </div>
        </div>
      )}

      {!taskState && !taskId && (
        <div className="h-64 flex items-center justify-center border border-dashed border-border rounded-md text-text-muted bg-surface-primary/50">
          Enter a goal above to start ALFRED.
        </div>
      )}
    </div>
  );
};

export default Workspace;

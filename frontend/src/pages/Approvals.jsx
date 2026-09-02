import React, { useState, useEffect } from 'react';
import { getAllTasks } from '../services/api';
import { approveAction, rejectAction } from '../services/api';

const Approvals = () => {
  const [tasks, setTasks] = useState([]);
  
  useEffect(() => {
    getAllTasks().then(setTasks).catch(console.error);
  }, []);
  
  const pendingTasks = tasks.filter(t => t.status === 'waiting_approval');

  const handleApprove = async (taskId, approvalId) => {
    try {
      await approveAction(taskId, approvalId);
      getAllTasks().then(setTasks).catch(console.error);
    } catch (e) {
      console.error(e);
    }
  };

  const handleReject = async (taskId, approvalId) => {
    try {
      await rejectAction(taskId, approvalId);
      getAllTasks().then(setTasks).catch(console.error);
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="flex-1 flex flex-col h-full overflow-hidden">
      <div className="h-16 flex items-center px-8 border-b border-border shrink-0">
        <span className="font-mono text-xs tracking-widest text-text-secondary uppercase">APPROVALS / 03</span>
      </div>
      
      <div className="p-8 flex-1 overflow-y-auto">
        <h1 className="text-2xl font-bold tracking-tight mb-8 uppercase">PENDING AUTHORIZATIONS</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-5xl">
          {pendingTasks.length > 0 ? pendingTasks.map(task => (
            <div key={task.task_id} className="border border-border p-6 bg-surface-secondary/20">
              <div className="text-xs font-mono tracking-widest text-text-secondary mb-6 border-b border-border/50 pb-2 uppercase">
                {task.approval?.title || 'APPROVAL REQUIRED'}
              </div>
              
              <div className="space-y-4 mb-8">
                <div className="flex justify-between items-baseline">
                  <span className="font-mono text-xs text-text-muted uppercase">TASK ID</span>
                  <span className="font-mono text-sm text-text-primary uppercase">{task.task_id.substring(0,8)}</span>
                </div>
                <div className="flex flex-col gap-1">
                  <span className="font-mono text-xs text-text-muted uppercase">REASON</span>
                  <span className="font-mono text-sm text-text-primary">{task.approval?.description || 'Action requires user permission.'}</span>
                </div>
                <div className="flex justify-between items-baseline mt-4">
                  <span className="font-mono text-xs text-text-muted uppercase">CONTROL REQUIREMENT</span>
                  <span className="font-mono text-sm text-accent-amber uppercase">USER AUTHORIZATION REQUIRED</span>
                </div>
              </div>
              
              <div className="flex gap-4">
                <button onClick={() => handleApprove(task.task_id, task.approval?.approval_id)} className="flex-1 py-3 border border-border text-xs font-mono tracking-widest bg-surface-secondary text-text-primary hover:bg-border transition-colors uppercase">&gt; REVIEW & APPROVE</button>
                <button onClick={() => handleReject(task.task_id, task.approval?.approval_id)} className="flex-1 py-3 border border-border text-xs font-mono tracking-widest text-text-secondary hover:bg-surface-secondary transition-colors uppercase">REJECT</button>
              </div>
            </div>
          )) : (
            <div className="text-sm font-mono text-text-muted uppercase col-span-2">No pending approvals.</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Approvals;

import React from 'react';

const Tasks = () => {
  return (
    <div className="flex-1 flex flex-col h-full overflow-hidden">
      <div className="h-16 flex items-center px-8 border-b border-border shrink-0">
        <span className="font-mono text-xs tracking-widest text-text-secondary uppercase">TASKS / 02</span>
      </div>
      
      <div className="p-8 flex-1 overflow-y-auto">
        <h1 className="text-2xl font-bold tracking-tight mb-8 uppercase">TASK HISTORY</h1>
        
        <div className="border border-border">
          <div className="grid grid-cols-12 gap-4 p-4 border-b border-border bg-surface-secondary/50 font-mono text-xs text-text-muted uppercase">
            <div className="col-span-1">ID</div>
            <div className="col-span-6">GOAL</div>
            <div className="col-span-2">STATUS</div>
            <div className="col-span-3 text-right">CREATED</div>
          </div>
          
          <div className="divide-y divide-border">
            {[
              { id: '01', title: 'PREPARE ME FOR TOMORROW\'S MEETING WITH RAHUL', status: 'COMPLETED', color: 'text-text-secondary', date: '2026-09-02 08:30:12' },
              { id: '02', title: 'HANDLE THE PENDING INVOICE IF WITHIN POLICY', status: 'AWAITING APPROVAL', color: 'text-accent-amber', date: '2026-09-02 09:15:44' },
              { id: '03', title: 'SUMMARIZE PROJECT UPDATES FROM LAST WEEK', status: 'RUNNING', color: 'text-text-primary', date: '2026-09-02 10:02:05' },
              { id: '04', title: 'FIND LATEST DESIGN FILES FOR LANDING PAGE', status: 'FAILED', color: 'text-status-error', date: '2026-09-02 11:45:22' }
            ].map(task => (
              <div key={task.id} className="grid grid-cols-12 gap-4 p-4 hover:bg-surface-secondary/30 transition-colors cursor-pointer items-center">
                <div className="col-span-1 font-mono text-xs text-text-muted">{task.id}</div>
                <div className="col-span-6 font-mono text-sm text-text-primary uppercase truncate pr-4">{task.title}</div>
                <div className={`col-span-2 font-mono text-xs tracking-widest uppercase ${task.color}`}>{task.status}</div>
                <div className="col-span-3 font-mono text-xs text-text-muted text-right">{task.date}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Tasks;

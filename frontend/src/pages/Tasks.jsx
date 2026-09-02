import React, { useState, useEffect } from 'react';
import { getAllTasks } from '../services/api';

const Tasks = () => {
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    getAllTasks().then(setTasks).catch(console.error);
  }, []);
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
                    <div className="space-y-4">
              {tasks.length > 0 ? tasks.map(task => (
                <div key={task.task_id} className="border border-border p-6 bg-surface-secondary/10 flex flex-col md:flex-row gap-6 md:items-center justify-between group hover:bg-surface-secondary/30 transition-colors">
                  <div className="flex-1">
                    <div className="flex gap-4 items-baseline mb-2">
                      <span className="font-mono text-xs text-text-muted">{task.task_id.substring(0, 8)}</span>
                      <h3 className="font-mono text-sm text-text-primary uppercase">{task.goal}</h3>
                    </div>
                    <div className="font-mono text-[10px] tracking-widest text-text-secondary uppercase">
                      {task.status}
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-6 shrink-0">
                    <div className="font-mono text-xs tracking-widest uppercase text-text-secondary">
                      {task.status}
                    </div>
                    <button className="border border-border px-6 py-2 text-[10px] font-mono tracking-widest text-text-primary hover:bg-border transition-colors uppercase">
                      &gt; VIEW LOGS
                    </button>
                  </div>
                </div>
              )) : (
                <div className="text-sm font-mono text-text-muted uppercase">No tasks available.</div>
              )}
            </div>
        </div>
      </div>
    </div>
  );
};

export default Tasks;

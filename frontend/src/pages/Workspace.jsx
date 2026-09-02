import React, { useState } from 'react';
import GoalInput from '../components/GoalInput';
import TaskHeader from '../components/TaskHeader';
import PlanView from '../components/PlanView';
import ExecutionTimeline from '../components/ExecutionTimeline';
import ApprovalPanel from '../components/ApprovalPanel';
import ResultPanel from '../components/ResultPanel';
import { useTaskEvents } from '../hooks/taskEvents';
import { createTask, getAllTasks } from '../services/api';

const Workspace = () => {
  const [tasks, setTasks] = useState([]);
  const [taskId, setTaskId] = useState(null);
  const [activeTab, setActiveTab] = useState('OVERVIEW');
  const [audioEnabled, setAudioEnabled] = useState(false);
  const { taskState, loading, error, approve, reject } = useTaskEvents(taskId, audioEnabled);

  React.useEffect(() => {
    if (!taskId) {
      getAllTasks().then(setTasks).catch(console.error);
    }
  }, [taskId]);

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
    <div className="flex h-full w-full overflow-hidden">
      {/* Main Content Area */}
      <div className="flex-1 flex flex-col h-full overflow-hidden">
        {!taskState && !taskId && (
          <div className="flex-1 flex flex-col h-full overflow-y-auto">
            <div className="h-16 flex items-center px-8 border-b border-border shrink-0">
              <span className="font-mono text-xs tracking-widest text-text-secondary uppercase">DASHBOARD / 01</span>
            </div>
            
            <div className="p-8 max-w-4xl w-full">
              <h1 className="text-3xl font-bold tracking-tight mb-8 uppercase">GOOD MORNING.</h1>
              <GoalInput onStartTask={handleStartTask} isExecuting={isExecuting} audioEnabled={audioEnabled} setAudioEnabled={setAudioEnabled} />
              
              <div className="mt-16">
                <div className="text-xs font-mono tracking-widest text-text-secondary mb-4 uppercase">Recent Tasks</div>
                <div className="space-y-4">
                  {tasks.length > 0 ? tasks.slice(0, 10).map(task => (
                    <div key={task.task_id} className="flex justify-between items-start border-b border-border pb-4 last:border-0 cursor-pointer hover:bg-surface-secondary/20 transition-colors p-2" onClick={() => setTaskId(task.task_id)}>
                      <div className="flex gap-4">
                        <span className="font-mono text-xs text-text-muted">{task.task_id.substring(0, 8)}</span>
                        <span className="font-mono text-sm text-text-primary uppercase">{task.goal}</span>
                      </div>
                      <div className="font-mono text-xs tracking-widest uppercase text-text-secondary">{task.status}</div>
                    </div>
                  )) : (
                    <div className="text-sm font-mono text-text-muted uppercase">No recent tasks.</div>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        {taskState && (
          <div className="flex-1 flex flex-col h-full overflow-hidden bg-surface-primary">
            <TaskHeader task={taskState} activeTab={activeTab} onTabChange={setActiveTab} />
            
            <div className="flex flex-1 overflow-hidden">
              
              {/* PLAN VIEW */}
              {(activeTab === 'OVERVIEW' || activeTab === 'PLAN') && (
                <div className={`border-r border-border p-6 overflow-y-auto ${activeTab === 'PLAN' ? 'flex-1' : 'w-80'}`}>
                  <div className="text-xs font-mono tracking-widest text-text-secondary mb-6 uppercase">Plan</div>
                  <PlanView plan={taskState.plan} />
                </div>
              )}
              
              {/* EXECUTION VIEW */}
              {(activeTab === 'OVERVIEW' || activeTab === 'EXECUTION') && (
                <div className="flex-1 p-6 overflow-y-auto">
                  <div className="text-xs font-mono tracking-widest text-text-secondary mb-6 uppercase">Execution</div>
                  <ExecutionTimeline actions={taskState.actions} status={taskState.status} />
                </div>
              )}

              {/* DETAILS & RESULTS VIEW */}
              {(activeTab === 'OVERVIEW' || activeTab === 'DETAILS') && (
                <div className={`p-6 overflow-y-auto space-y-6 ${activeTab === 'DETAILS' ? 'flex-1 border-l border-border' : 'w-80 border-l border-border'}`}>
                  <div className="text-xs font-mono tracking-widest text-text-secondary mb-6 uppercase">Details</div>
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
                  
                  {!['waiting_approval', 'completed'].includes(taskState.status) && (
                    <div className="text-text-muted font-mono text-xs uppercase">No result details available yet.</div>
                  )}
                </div>
              )}

              {/* FILES VIEW */}
              {activeTab === 'FILES' && (
                <div className="flex-1 p-6 overflow-y-auto">
                  <div className="text-xs font-mono tracking-widest text-text-secondary mb-6 uppercase">Generated Files</div>
                  {taskState.status === 'completed' ? (
                    <div className="border border-border p-8 bg-surface-secondary/20 max-w-2xl">
                      <div className="font-mono text-sm text-text-primary mb-4 uppercase">meeting_brief.md</div>
                      <div className="text-xs text-text-secondary mb-6">A markdown file containing the briefing document.</div>
                      <button 
                        onClick={() => alert("File creation API not integrated yet. This will download or open the file in the future.")}
                        className="border border-border bg-surface-secondary text-text-primary hover:bg-border transition-colors px-6 py-2 font-mono text-xs tracking-widest uppercase"
                      >
                        &gt; DOWNLOAD FILE
                      </button>
                    </div>
                  ) : (
                    <div className="text-text-muted font-mono text-xs uppercase">No files generated yet.</div>
                  )}
                </div>
              )}

            </div>
          </div>
        )}
      </div>

      {/* Right Column (Only on dashboard) */}
      {!taskState && !taskId && (
        <aside className="w-80 border-l border-border bg-surface-primary/95 flex flex-col h-full overflow-y-auto p-6 shrink-0">
          <div className="mb-12">
            <div className="text-[10px] font-mono tracking-widest text-text-muted mb-4 uppercase">AGENT OVERVIEW</div>
            
            <div className="flex justify-center mb-6">
              <div className="w-32 h-32 rounded-full border border-border flex items-center justify-center relative">
                <div className="absolute inset-1 border border-border/50 rounded-full" />
                <div className="absolute inset-2 border border-border/30 rounded-full" />
                <span className="text-2xl font-mono text-text-primary">100%</span>
              </div>
            </div>

            <div className="space-y-2 font-mono text-xs">
              <div className="flex justify-between border-b border-border/50 pb-1"><span className="text-text-muted uppercase">PLAN ENGINE</span> <span className="text-text-primary">OK</span></div>
              <div className="flex justify-between border-b border-border/50 pb-1"><span className="text-text-muted uppercase">TOOL ADAPTERS</span> <span className="text-text-primary">OK</span></div>
              <div className="flex justify-between border-b border-border/50 pb-1"><span className="text-text-muted uppercase">POLICY ENGINE</span> <span className="text-text-primary">OK</span></div>
              <div className="flex justify-between border-b border-border/50 pb-1"><span className="text-text-muted uppercase">VERIFIER</span> <span className="text-text-primary">OK</span></div>
              <div className="flex justify-between pb-1"><span className="text-text-muted uppercase">MEMORY</span> <span className="text-text-primary">OK</span></div>
            </div>
          </div>

          <div>
            <div className="text-[10px] font-mono tracking-widest text-text-muted mb-4 uppercase">NEXT APPROVAL</div>
            <div className="border border-border p-4">
              <div className="text-xs font-mono text-text-secondary mb-1 uppercase">No pending approvals</div>
            </div>
          </div>
        </aside>
      )}
    </div>
  );
};

export default Workspace;

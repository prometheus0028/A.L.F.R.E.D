import { useState, useEffect, useCallback } from 'react';
import { subscribeToTaskEvents, getTask, approveAction, rejectAction } from '../services/api';

export const useTaskEvents = (taskId) => {
  const [taskState, setTaskState] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const refreshTask = useCallback(async () => {
    if (!taskId) return;
    try {
      setLoading(true);
      const data = await getTask(taskId);
      setTaskState(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [taskId]);

  useEffect(() => {
    if (!taskId) return;

    refreshTask();

    const unsubscribe = subscribeToTaskEvents(taskId, (event) => {
      // Event received, optimistic state updates or full refresh
      console.log("Event received:", event);
      if (['plan_created', 'replanning', 'task_completed', 'task_failed', 'approval_required'].includes(event.type)) {
        refreshTask();
      } else {
        // Soft refresh for step updates to avoid excessive fetching
        setTaskState(prev => {
          if (!prev) return prev;
          
          // Basic optimistic merge
          if (event.type === 'tool_started' && event.data.tool) {
             // In a real app we'd carefully merge action states, here we just do a shallow update
             // or rely on a subsequent refresh
             return { ...prev }; 
          }
          return { ...prev };
        });
        
        if (event.type === 'tool_completed' || event.type === 'verification_passed') {
          setTimeout(refreshTask, 100);
        }
      }
    });

    return () => unsubscribe();
  }, [taskId, refreshTask]);

  const approve = async (approvalId) => {
    await approveAction(taskId, approvalId);
    refreshTask();
  };

  const reject = async (approvalId, reason) => {
    await rejectAction(taskId, approvalId, reason);
    refreshTask();
  };

  return { taskState, loading, error, approve, reject };
};

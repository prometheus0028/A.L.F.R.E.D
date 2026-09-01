import { useState, useEffect, useCallback, useRef } from 'react';
import { subscribeToTaskEvents, getTask, approveAction, rejectAction } from '../services/api';
import AudioEngine from '../services/AudioEngine';

export const useTaskEvents = (taskId, audioEnabled) => {
  const [taskState, setTaskState] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  // Track processed final events to avoid duplicate TTS triggers per task
  const processedFinalEvents = useRef(new Set());
  const audioEnabledRef = useRef(audioEnabled);

  useEffect(() => {
    audioEnabledRef.current = audioEnabled;
  }, [audioEnabled]);

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
      console.log(`[SSE] Received event type: ${event.type}`);
      
      if (audioEnabledRef.current) {
        if (event.type === 'plan_created') {
          AudioEngine.playSynthesis("Plan generated.");
        } else if (event.type === 'approval_required') {
          AudioEngine.playSynthesis("Approval required.");
        } else if (event.type === 'task_completed') {
          const eventId = `${taskId}-completed`;
          if (!processedFinalEvents.current.has(eventId)) {
            processedFinalEvents.current.add(eventId);
            console.log(`[SSE] Event recognized as final result: ${event.type}`);
            const summary = event.data?.summary || "Task completed.";
            AudioEngine.playSynthesis(summary);
          }
        } else if (event.type === 'task_failed') {
          const eventId = `${taskId}-failed`;
          if (!processedFinalEvents.current.has(eventId)) {
            processedFinalEvents.current.add(eventId);
            console.log(`[SSE] Event recognized as final result: ${event.type}`);
            const summary = event.data?.summary ? `Task failed: ${event.data.summary}` : "Task failed.";
            AudioEngine.playSynthesis(summary);
          }
        }
      }

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

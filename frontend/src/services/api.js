import axios from 'axios';

// Switch to real backend
const USE_MOCK = false;

const getBaseUrl = () => {
  return import.meta.env.VITE_API_URL || 'http://127.0.0.1:8001/api';
};

const getEventSourceUrl = (taskId) => {
  const baseUrl = getBaseUrl();
  return `${baseUrl}/tasks/${taskId}/events`;
}

const apiClient = axios.create({
  baseURL: getBaseUrl()
});

export const createTask = async (goal) => {
  if (USE_MOCK) return; // Placeholder
  const { data } = await apiClient.post('/tasks', { goal });
  return data;
};

export const getTask = async (taskId) => {
  if (USE_MOCK) return; // Placeholder
  const { data } = await apiClient.get(`/tasks/${taskId}`);
  return data;
};

export const approveAction = async (taskId, approvalId) => {
  if (USE_MOCK) return; // Placeholder
  const { data } = await apiClient.post(`/tasks/${taskId}/approve`, { approval_id: approvalId });
  return data;
};

export const rejectAction = async (taskId, approvalId, reason) => {
  if (USE_MOCK) return; // Placeholder
  const { data } = await apiClient.post(`/tasks/${taskId}/reject`, { approval_id: approvalId, reason });
  return data;
};

export const subscribeToTaskEvents = (taskId, callback) => {
  if (USE_MOCK) return; // Placeholder
  
  const eventSource = new EventSource(getEventSourceUrl(taskId));
  
  const eventTypes = [
    "goal_received", "plan_created", "step_started", 
    "tool_started", "tool_completed", "step_completed", 
    "replanning", "task_failed", "verification_started", 
    "verification_passed", "verification_failed", 
    "task_completed", "approval_required"
  ];

  eventTypes.forEach(type => {
    eventSource.addEventListener(type, (event) => {
      try {
        const parsedData = JSON.parse(event.data);
        callback(parsedData);
      } catch (e) {
        console.error("Failed to parse SSE data", e);
      }
    });
  });

  return () => {
    eventSource.close();
  };
};

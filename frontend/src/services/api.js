import axios from 'axios';

// Switch to real backend
const USE_MOCK = false;

const getBaseUrl = () => {
  return import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api';
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
  const response = await apiClient.post('/tasks', { goal });
  return response.data;
};

export const getTask = async (taskId) => {
  const response = await apiClient.get(`/tasks/${taskId}`);
  return response.data;
};

export const approveAction = async (taskId, approvalId) => {
  const response = await apiClient.post(`/tasks/${taskId}/approve`, { approval_id: approvalId });
  return response.data;
};

export const rejectAction = async (taskId, approvalId, reason = null) => {
  const response = await apiClient.post(`/tasks/${taskId}/reject`, { approval_id: approvalId, reason });
  return response.data;
};

export const getFiles = async () => {
  const response = await apiClient.get('/files');
  return response.data;
};

export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await apiClient.post('/files/upload', formData);
  return response.data;
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

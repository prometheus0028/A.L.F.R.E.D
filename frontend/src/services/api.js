import * as mockApi from './mockApi';
import axios from 'axios';

// To switch to real backend, flip this flag:
const USE_MOCK = true;

const apiClient = axios.create({
  baseURL: '/api'
});

export const createTask = async (goal) => {
  if (USE_MOCK) return mockApi.createTask(goal);
  const { data } = await apiClient.post('/tasks', { goal });
  return data;
};

export const getTask = async (taskId) => {
  if (USE_MOCK) return mockApi.getTask(taskId);
  const { data } = await apiClient.get(`/tasks/${taskId}`);
  return data;
};

export const approveAction = async (taskId, approvalId) => {
  if (USE_MOCK) return mockApi.approveAction(taskId, approvalId);
  const { data } = await apiClient.post(`/tasks/${taskId}/approve`, { approval_id: approvalId });
  return data;
};

export const rejectAction = async (taskId, approvalId, reason) => {
  if (USE_MOCK) return mockApi.rejectAction(taskId, approvalId, reason);
  const { data } = await apiClient.post(`/tasks/${taskId}/reject`, { approval_id: approvalId, reason });
  return data;
};

export const subscribeToTaskEvents = (taskId, callback) => {
  if (USE_MOCK) return mockApi.subscribeToTaskEvents(taskId, callback);
  
  const eventSource = new EventSource(`/api/tasks/${taskId}/events`);
  
  eventSource.onmessage = (event) => {
    try {
      const parsedData = JSON.parse(event.data);
      callback(parsedData);
    } catch (e) {
      console.error("Failed to parse SSE data", e);
    }
  };

  return () => {
    eventSource.close();
  };
};

import apiClient from './api-client';
import { Task, TaskFormData } from '@/types';

// Get all tasks for the authenticated user
export const getAllTasks = async (userId: number): Promise<Task[]> => {
  try {
    const response = await apiClient.get(`/api/${userId}/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching tasks:', error);
    throw error;
  }
};

// Get a specific task by ID
export const getTaskById = async (userId: number, taskId: number): Promise<Task> => {
  try {
    const response = await apiClient.get(`/api/${userId}/${taskId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching task ${taskId}:`, error);
    throw error;
  }
};

// Create a new task
export const createTask = async (userId: number, taskData: TaskFormData): Promise<Task> => {
  try {
    const response = await apiClient.post(`/api/${userId}/`, taskData);
    return response.data;
  } catch (error) {
    console.error('Error creating task:', error);
    throw error;
  }
};

// Update an existing task
export const updateTask = async (userId: number, taskId: number, taskData: Partial<TaskFormData>): Promise<Task> => {
  try {
    const response = await apiClient.put(`/api/${userId}/${taskId}`, taskData);
    return response.data;
  } catch (error) {
    console.error(`Error updating task ${taskId}:`, error);
    throw error;
  }
};

// Delete a task
export const deleteTask = async (userId: number, taskId: number): Promise<void> => {
  try {
    await apiClient.delete(`/api/${userId}/${taskId}`);
  } catch (error) {
    console.error(`Error deleting task ${taskId}:`, error);
    throw error;
  }
};

// Toggle task completion status
export const toggleTaskCompletion = async (userId: number, taskId: number): Promise<Task> => {
  try {
    const response = await apiClient.patch(`/api/${userId}/${taskId}/complete`);
    return response.data;
  } catch (error) {
    console.error(`Error toggling task ${taskId} completion:`, error);
    throw error;
  }
};
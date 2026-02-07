import apiClient from './api-client';
import { Task, TaskFormData } from '@/types';

// Get all tasks for the authenticated user
export const getAllTasks = async (userId: number): Promise<Task[]> => {
  try {
    const response = await apiClient.get(`/${userId}/tasks`);
    return response.data;
  } catch (error) {
    console.error('Error fetching tasks:', error);
    throw error;
  }
};

// Get a specific task by ID
export const getTaskById = async (userId: number, id: number): Promise<Task> => {
  try {
    const response = await apiClient.get(`/${userId}/tasks/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching task ${id}:`, error);
    throw error;
  }
};

// Create a new task
export const createTask = async (userId: number, taskData: TaskFormData): Promise<Task> => {
  try {
    const response = await apiClient.post(`/${userId}/tasks`, taskData);
    return response.data;
  } catch (error) {
    console.error('Error creating task:', error);
    throw error;
  }
};

// Update an existing task
export const updateTask = async (userId: number, id: number, taskData: Partial<TaskFormData>): Promise<Task> => {
  try {
    const response = await apiClient.put(`/${userId}/tasks/${id}`, taskData);
    return response.data;
  } catch (error) {
    console.error(`Error updating task ${id}:`, error);
    throw error;
  }
};

// Delete a task
export const deleteTask = async (userId: number, id: number): Promise<void> => {
  try {
    await apiClient.delete(`/${userId}/tasks/${id}`);
  } catch (error) {
    console.error(`Error deleting task ${id}:`, error);
    throw error;
  }
};

// Toggle task completion status
export const toggleTaskCompletion = async (userId: number, id: number): Promise<Task> => {
  try {
    const response = await apiClient.patch(`/${userId}/tasks/${id}/complete`);
    return response.data;
  } catch (error) {
    console.error(`Error toggling task ${id} completion:`, error);
    throw error;
  }
};
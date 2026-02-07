'use client';

import React, { useState, useEffect } from 'react';
import { Task, TaskFormData } from '@/types';
import TaskList from '@/components/tasks/task-list';
import TaskForm from '@/components/tasks/task-form';
import { getAllTasks, createTask } from '@/lib/services/task-service';
import { useAuth } from '@/hooks/use-auth';

const TasksPage = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { user } = useAuth();

  useEffect(() => {
    const fetchTasks = async () => {
      if (!user) return;

      try {
        const tasksData = await getAllTasks(user.id as number);
        setTasks(tasksData);
      } catch (err) {
        setError('Failed to load tasks');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchTasks();
  }, [user]);

  const handleCreateTask = async (taskData: TaskFormData) => {
    if (!user) return { success: false, error: 'User not authenticated' };

    try {
      const newTask = await createTask(user.id as number, taskData);
      setTasks([newTask, ...tasks]); // Add new task to the top of the list
      return { success: true };
    } catch (err) {
      console.error('Failed to create task:', err);
      return { success: false, error: 'Failed to create task' };
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-64">
        <div className="text-lg">Loading tasks...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-md bg-red-50 p-4">
        <div className="text-sm text-red-700">{error}</div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="mb-8 text-center">
        <h1 className="text-3xl font-bold text-gray-900">My Tasks</h1>
        <p className="text-gray-600 mt-2">Manage your tasks efficiently</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-4 text-gray-800">Create New Task</h2>
          <TaskForm onSubmit={handleCreateTask} />
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-4 text-gray-800">Your Tasks</h2>
          <TaskList
            tasks={tasks}
            onTaskUpdate={() => {
              // Refresh the task list after update
              if (user) {
                getAllTasks(user.id as number).then(setTasks).catch(console.error);
              }
            }}
            onTaskDelete={(deletedTaskId) => {
              // Remove the deleted task from the list
              setTasks(tasks.filter(task => task.id !== deletedTaskId));
            }}
          />
        </div>
      </div>
    </div>
  );
};

export default TasksPage;
'use client';

import React, { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { Task } from '@/types';
import TaskForm from '@/components/tasks/task-form';
import { getTaskById, updateTask, deleteTask, toggleTaskCompletion } from '@/lib/services/task-service';
import { useAuth } from '@/hooks/use-auth';

const TaskDetailPage = () => {
  const { id } = useParams();
  const taskId = typeof id === 'string' ? parseInt(id, 10) : id[0] ? parseInt(id[0], 10) : NaN;
  const router = useRouter();
  const { user } = useAuth();
  const [task, setTask] = useState<Task | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [editing, setEditing] = useState(false);

  useEffect(() => {
    const fetchTask = async () => {
      if (!user) return;

      try {
        const taskData = await getTaskById(user.id as number, taskId);
        setTask(taskData);
      } catch (err) {
        setError('Failed to load task');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchTask();
  }, [taskId, user]);

  const handleToggleComplete = async () => {
    if (!task || !user) return;

    try {
      const updatedTask = await toggleTaskCompletion(user.id as number, task.id);
      setTask(updatedTask);
    } catch (err) {
      setError('Failed to update task completion');
      console.error(err);
    }
  };

  const handleUpdateTask = async (taskData: any) => {
    if (!task || !user) return;

    try {
      const updatedTask = await updateTask(user.id as number, task.id, taskData);
      setTask(updatedTask);
      setEditing(false);
      return { success: true };
    } catch (err) {
      console.error('Failed to update task:', err);
      return { success: false, error: 'Failed to update task' };
    }
  };

  const handleDelete = async () => {
    if (!task || !user || !confirm('Are you sure you want to delete this task?')) return;

    try {
      await deleteTask(user.id as number, task.id);
      router.push('/tasks');
    } catch (err) {
      setError('Failed to delete task');
      console.error(err);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-64">
        <div className="text-lg">Loading task...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-md bg-red-50 p-4">
        <div className="text-sm text-red-700">{error}</div>
        <button
          onClick={() => router.back()}
          className="mt-2 text-blue-600 hover:text-blue-800"
        >
          Go Back
        </button>
      </div>
    );
  }

  if (!task) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">Task not found</p>
        <button
          onClick={() => router.back()}
          className="mt-4 text-blue-600 hover:text-blue-800"
        >
          Go Back
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900">Task Details</h1>
        <button
          onClick={() => router.back()}
          className="text-blue-600 hover:text-blue-800"
        >
          ← Back to Tasks
        </button>
      </div>

      {editing ? (
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Edit Task</h2>
          <TaskForm
            initialData={{
              title: task.title,
              description: task.description,
              completed: task.completed,
            }}
            onSubmit={handleUpdateTask}
            onCancel={() => setEditing(false)}
          />
        </div>
      ) : (
        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="flex items-start mb-4">
            <input
              type="checkbox"
              checked={task.completed}
              onChange={handleToggleComplete}
              className="mt-1 h-5 w-5 text-blue-600 rounded focus:ring-blue-500"
            />
            <div className="ml-3">
              <h2 className={`text-xl font-semibold ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                {task.title}
              </h2>
              {task.description && (
                <p className={`mt-2 text-gray-700 ${task.completed ? 'line-through' : ''}`}>
                  {task.description}
                </p>
              )}
            </div>
          </div>

          <div className="mt-6 pt-4 border-t border-gray-200">
            <div className="grid grid-cols-2 gap-4 text-sm text-gray-600">
              <div>
                <span className="font-medium">Created:</span>{' '}
                {new Date(task.created_at).toLocaleString()}
              </div>
              <div>
                <span className="font-medium">Updated:</span>{' '}
                {new Date(task.updated_at).toLocaleString()}
              </div>
            </div>
          </div>

          <div className="mt-6 flex space-x-3">
            <button
              onClick={() => setEditing(true)}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            >
              Edit
            </button>
            <button
              onClick={handleToggleComplete}
              className={`px-4 py-2 rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 ${
                task.completed
                  ? 'bg-yellow-600 text-white hover:bg-yellow-700 focus:ring-yellow-500'
                  : 'bg-green-600 text-white hover:bg-green-700 focus:ring-green-500'
              }`}
            >
              {task.completed ? 'Mark Incomplete' : 'Mark Complete'}
            </button>
            <button
              onClick={handleDelete}
              className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2"
            >
              Delete
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default TaskDetailPage;
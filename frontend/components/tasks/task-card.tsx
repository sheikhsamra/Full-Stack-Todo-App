'use client';

import React from 'react';
import { Task } from '@/types';
import Link from 'next/link';
import Button from '@/components/ui/button';
import { toggleTaskCompletion, deleteTask } from '@/lib/services/task-service';

interface TaskCardProps {
  task: Task;
  onUpdate: (task: Task) => void;
  onDelete: (taskId: number) => void;
}

const TaskCard = ({ task, onUpdate, onDelete }: TaskCardProps) => {
  const handleToggleComplete = async () => {
    try {
      const updatedTask = await toggleTaskCompletion(task.user_id, task.id);
      onUpdate(updatedTask);
    } catch (error) {
      console.error('Error toggling completion:', error);
    }
  };

  const handleDelete = async () => {
    if (confirm('Are you sure you want to delete this task?')) {
      try {
        await deleteTask(task.user_id, task.id);
        onDelete(task.id);
      } catch (error) {
        console.error('Error deleting task:', error);
      }
    }
  };

  return (
    <div className={`border rounded-lg p-4 shadow-sm hover:shadow-md transition-all duration-200 ${task.completed ? 'bg-green-50 border-green-200' : 'bg-white border-gray-200'}`}>
      <div className="flex items-start gap-3">
        <button
          onClick={handleToggleComplete}
          className={`mt-1 flex-shrink-0 h-5 w-5 rounded-full border flex items-center justify-center focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${
            task.completed 
              ? 'bg-green-500 border-green-500' 
              : 'bg-white border-gray-300'
          }`}
          aria-label={task.completed ? 'Mark as incomplete' : 'Mark as complete'}
        >
          {task.completed && (
            <svg className="h-4 w-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
            </svg>
          )}
        </button>
        
        <div className="flex-1 min-w-0">
          <h3 className={`text-base font-medium truncate ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
            {task.title}
          </h3>
          {task.description && (
            <p className={`mt-1 text-sm ${task.completed ? 'line-through text-gray-500' : 'text-gray-600'}`}>
              {task.description.length > 150
                ? `${task.description.substring(0, 150)}...`
                : task.description}
            </p>
          )}
          
          <div className="mt-2 flex items-center text-xs text-gray-500">
            <span>Created: {new Date(task.created_at).toLocaleDateString()}</span>
            {task.updated_at !== task.created_at && (
              <span className="ml-2">Updated: {new Date(task.updated_at).toLocaleDateString()}</span>
            )}
          </div>
        </div>
        
        <div className="flex space-x-2 ml-2 flex-shrink-0">
          <Link href={`/tasks/${task.id}`}>
            <Button variant="secondary" size="sm">View</Button>
          </Link>
          <Button
            variant="destructive"
            size="sm"
            onClick={handleDelete}
          >
            Delete
          </Button>
        </div>
      </div>
    </div>
  );
};

export default TaskCard;
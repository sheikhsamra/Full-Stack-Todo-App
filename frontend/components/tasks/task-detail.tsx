import React from 'react';
import { Task } from '@/types';

interface TaskDetailProps {
  task: Task;
  onEdit: () => void;
  onDelete: () => void;
  onToggleComplete: () => void;
}

const TaskDetail = ({ task, onEdit, onDelete, onToggleComplete }: TaskDetailProps) => {
  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <div className="flex items-start mb-4">
        <input
          type="checkbox"
          checked={task.completed}
          onChange={onToggleComplete}
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
          onClick={onEdit}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
        >
          Edit
        </button>
        <button
          onClick={onToggleComplete}
          className={`px-4 py-2 rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 ${
            task.completed
              ? 'bg-yellow-600 text-white hover:bg-yellow-700 focus:ring-yellow-500'
              : 'bg-green-600 text-white hover:bg-green-700 focus:ring-green-500'
          }`}
        >
          {task.completed ? 'Mark Incomplete' : 'Mark Complete'}
        </button>
        <button
          onClick={onDelete}
          className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2"
        >
          Delete
        </button>
      </div>
    </div>
  );
};

export default TaskDetail;
'use client';

import React, { useState } from 'react';
import { TaskFormData } from '@/types';
import Input from '@/components/ui/input';
import Button from '@/components/ui/button';
import Textarea from '@/components/ui/textarea';

interface TaskFormProps {
  onSubmit: (taskData: TaskFormData) => Promise<{ success: boolean; error?: string }>;
  initialData?: TaskFormData;
  onCancel?: () => void;
}

const TaskForm = ({ onSubmit, initialData = { title: '', description: '' }, onCancel }: TaskFormProps) => {
  const [title, setTitle] = useState(initialData.title);
  const [description, setDescription] = useState(initialData.description);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    const result = await onSubmit({
      title,
      description: description || '',
    });

    if (result.success) {
      setTitle('');
      setDescription('');
      setError(null);
    } else {
      setError(result.error || 'An error occurred');
    }

    setLoading(false);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid grid-cols-1 gap-4">
        <Input
          label="Task Title"
          id="title"
          name="title"
          type="text"
          required
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="What needs to be done?"
          maxLength={255}
        />

        <div className="mb-4">
          <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
            Description (Optional)
          </label>
          <Textarea
            id="description"
            name="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Add details..."
            maxLength={1000}
            rows={3}
          />
        </div>
      </div>

      {error && (
        <div className="rounded-md bg-red-50 p-4">
          <div className="text-sm text-red-700">{error}</div>
        </div>
      )}

      <div className="flex space-x-2">
        <Button type="submit" loading={loading} disabled={loading}>
          {initialData.title ? 'Update Task' : 'Create Task'}
        </Button>
        {onCancel && (
          <Button type="button" variant="secondary" onClick={onCancel}>
            Cancel
          </Button>
        )}
      </div>
    </form>
  );
};

export default TaskForm;
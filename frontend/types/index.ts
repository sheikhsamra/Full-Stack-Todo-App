// User entity type (Frontend State)
export interface User {
  id: string | number;
  email: string;
  name?: string;
  isAuthenticated: boolean;
  isLoading: boolean;
}

// Task entity type (matches backend Task model)
export interface Task {
  id: number;
  user_id: number;
  title: string;
  description: string;
  completed: boolean;
  created_at: string; // ISO date string
  updated_at: string; // ISO date string
}

// Task form data (transient form data)
export interface TaskFormData {
  title: string;
  description?: string;
  completed?: boolean;
}

// API response types
export interface ApiResponse<T> {
  data: T;
  success: boolean;
}

export interface ErrorResponse {
  error: string;
  details?: object;
}

// Task list state
export interface TaskListState {
  tasks: Task[];
  isLoading: boolean;
  isError: boolean;
  isEmpty: boolean;
}

// Form state
export interface FormState {
  formData: TaskFormData;
  isSubmitting: boolean;
  errors: { [field: string]: string };
  successMessage?: string;
}

// UI state
export interface UIState {
  currentView: 'list' | 'detail' | 'edit';
  selectedTaskId: number | null;
  showConfirmation: boolean;
  confirmationAction: string | null;
}
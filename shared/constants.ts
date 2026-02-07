/**
 * Constants for the Todo application
 */

// API Configuration
export const API_CONFIG = {
  BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000',
  TIMEOUT: 10000, // 10 seconds
};

// Auth Configuration
export const AUTH_CONFIG = {
  TOKEN_KEY: 'todo_app_auth_token',
  REFRESH_TOKEN_KEY: 'todo_app_refresh_token',
  USER_DATA_KEY: 'todo_app_user_data',
};

// API Endpoints
export const API_ENDPOINTS = {
  AUTH: {
    LOGIN: '/api/auth/login',
    SIGNUP: '/api/auth/signup',
    LOGOUT: '/api/auth/logout',
    VERIFY: '/api/auth/verify',
  },
  USERS: {
    PROFILE: (userId: string) => `/api/${userId}/profile`,
  },
  TASKS: {
    LIST: (userId: string) => `/api/${userId}/tasks`,
    SINGLE: (userId: string, taskId: string) => `/api/${userId}/tasks/${taskId}`,
    COMPLETE: (userId: string, taskId: string) => `/api/${userId}/tasks/${taskId}/complete`,
  },
};

// HTTP Status Codes
export const HTTP_STATUS = {
  SUCCESS: 200,
  CREATED: 201,
  ACCEPTED: 202,
  NO_CONTENT: 204,
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  CONFLICT: 409,
  SERVER_ERROR: 500,
};

// Error Messages
export const ERROR_MESSAGES = {
  UNAUTHORIZED: 'Unauthorized access. Please log in.',
  FORBIDDEN: 'Access denied. You do not have permission to perform this action.',
  NETWORK_ERROR: 'Network error occurred. Please check your connection.',
  SERVER_ERROR: 'Server error occurred. Please try again later.',
};
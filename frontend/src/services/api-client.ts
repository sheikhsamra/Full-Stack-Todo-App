import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';
import { API_CONFIG, AUTH_CONFIG, ERROR_MESSAGES } from '../../../shared/constants';
import { useAuth } from '../components/auth/AuthProvider';

// Create axios instance with base configuration
const apiClient: AxiosInstance = axios.create({
  baseURL: API_CONFIG.BASE_URL,
  timeout: API_CONFIG.TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add JWT token to requests
apiClient.interceptors.request.use(
  (config: AxiosRequestConfig) => {
    const token = localStorage.getItem(AUTH_CONFIG.TOKEN_KEY);

    if (token) {
      config.headers = {
        ...config.headers,
        'Authorization': `Bearer ${token}`,
      };
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle authentication errors
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    // If the request was successful, return the response
    return response;
  },
  async (error) => {
    // Handle specific error cases
    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      switch (error.response.status) {
        case 401:
          // Unauthorized - Token might be expired or invalid
          const token = localStorage.getItem(AUTH_CONFIG.TOKEN_KEY);

          // Check if token exists and if it's expired
          if (token) {
            const authService = (await import('./auth-service')).default;

            // Check if the token is actually expired
            if (authService.isTokenExpired(token)) {
              console.log('Token has expired. Redirecting to login.');
            } else {
              console.log('Token is invalid. Redirecting to login.');
            }
          }

          // Remove invalid/expired token and redirect to login
          localStorage.removeItem(AUTH_CONFIG.TOKEN_KEY);
          localStorage.removeItem(AUTH_CONFIG.USER_DATA_KEY);
          window.location.href = '/login'; // Redirect to login page
          break;
        case 403:
          // Forbidden - User doesn't have permission for this resource
          console.error(ERROR_MESSAGES.FORBIDDEN);
          break;
        case 500:
          // Server error
          console.error(ERROR_MESSAGES.SERVER_ERROR);
          break;
        default:
          console.error(`Request failed with status: ${error.response.status}`);
      }
    } else if (error.request) {
      // The request was made but no response was received
      console.error(ERROR_MESSAGES.NETWORK_ERROR);
    } else {
      // Something happened in setting up the request that triggered an Error
      console.error('Error:', error.message);
    }

    return Promise.reject(error);
  }
);

/**
 * Wrapper functions for common HTTP methods
 */
export const ApiClient = {
  get: <T>(url: string, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> => {
    return apiClient.get<T>(url, config);
  },

  post: <T, D = any>(url: string, data?: D, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> => {
    return apiClient.post<T, D>(url, data, config);
  },

  put: <T, D = any>(url: string, data?: D, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> => {
    return apiClient.put<T, D>(url, data, config);
  },

  patch: <T, D = any>(url: string, data?: D, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> => {
    return apiClient.patch<T, D>(url, data, config);
  },

  delete: <T>(url: string, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> => {
    return apiClient.delete<T>(url, config);
  },

  // Specific API methods for our application
  auth: {
    login: (email: string, password: string) =>
      apiClient.post('/api/auth/login', { email, password }),

    signup: (email: string, password: string) =>
      apiClient.post('/api/auth/signup', { email, password }),

    logout: () =>
      apiClient.post('/api/auth/logout'),

    me: () =>
      apiClient.get('/api/auth/me')
  },

  tasks: {
    getAll: (userId: string) =>
      apiClient.get(`/api/${userId}/tasks`),

    getById: (userId: string, taskId: string) =>
      apiClient.get(`/api/${userId}/tasks/${taskId}`),

    create: (userId: string, taskData: any) =>
      apiClient.post(`/api/${userId}/tasks`, taskData),

    update: (userId: string, taskId: string, taskData: any) =>
      apiClient.put(`/api/${userId}/tasks/${taskId}`, taskData),

    delete: (userId: string, taskId: string) =>
      apiClient.delete(`/api/${userId}/tasks/${taskId}`),

    toggleComplete: (userId: string, taskId: string) =>
      apiClient.patch(`/api/${userId}/tasks/${taskId}/complete`)
  }
};

export default apiClient;
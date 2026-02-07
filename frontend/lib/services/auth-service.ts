// auth-service.ts
import apiClient from './auth-api';

interface UserRegistrationData {
  name: string;
  email: string;
  password: string;
}

interface UserLoginData {
  username: string; // email
  password: string;
}

interface AuthResponse {
  access_token: string;
  token_type: string;
  user_id: number;
  email: string;
}

// Helper function to safely access localStorage
const getLocalStorage = () => {
  if (typeof window !== 'undefined') {
    return window.localStorage;
  }
  return {
    getItem: () => null,
    setItem: () => {},
    removeItem: () => {}
  };
};

// Register a new user
export const registerUser = async (userData: UserRegistrationData): Promise<AuthResponse> => {
  try {
    const response = await apiClient.post('/auth/register', userData);
    // Store the token in localStorage
    const localStorage = getLocalStorage();
    localStorage.setItem('auth_token', response.data.access_token);
    return response.data;
  } catch (error) {
    console.error('Registration error:', error);
    throw error;
  }
};

// Login user
export const loginUser = async (loginData: UserLoginData): Promise<AuthResponse> => {
  try {
    const response = await apiClient.post('/auth/login', {}, {
      auth: {
        username: loginData.username,
        password: loginData.password
      }
    });
    // Store the token in localStorage
    const localStorage = getLocalStorage();
    localStorage.setItem('auth_token', response.data.access_token);
    return response.data;
  } catch (error) {
    console.error('Login error:', error);
    throw error;
  }
};

// Get current user info (using the token)
export const getCurrentUser = async (): Promise<any> => {
  try {
    // Since we don't have a /me endpoint, we'll decode the token or make a request to a protected endpoint
    const localStorage = getLocalStorage();
    const token = localStorage.getItem('auth_token');
    if (!token) {
      throw new Error('No authentication token found');
    }
    
    // For now, we'll just return the token payload by decoding it
    // In a real implementation, you'd have a /me endpoint on the backend
    const tokenPayload = JSON.parse(atob(token.split('.')[1]));
    return {
      id: tokenPayload.sub,
      email: tokenPayload.email || 'unknown@example.com', // This would come from the backend
    };
  } catch (error) {
    console.error('Get current user error:', error);
    throw error;
  }
};

// Logout user
export const logoutUser = async (): Promise<void> => {
  try {
    // Remove the token from localStorage
    const localStorage = getLocalStorage();
    localStorage.removeItem('auth_token');
  } catch (error) {
    console.error('Logout error:', error);
    throw error;
  }
};
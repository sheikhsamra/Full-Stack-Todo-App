'use client';

import { useState, useEffect } from 'react';
import { 
  loginUser, 
  registerUser, 
  getCurrentUser, 
  logoutUser 
} from '@/lib/services/auth-service';

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

export const useAuth = () => {
  const [user, setUser] = useState<{ id: string | number; email: string; name?: string; isAuthenticated: boolean } | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const localStorage = getLocalStorage();
        const token = localStorage.getItem('auth_token');
        if (token) {
          // Verify token is still valid by getting user info
          const userInfo = await getCurrentUser();
          setUser({
            id: userInfo.id,
            email: userInfo.email,
            isAuthenticated: true,
          });
        } else {
          setUser(null);
        }
      } catch (error) {
        console.error('Error checking auth:', error);
        // Clear invalid token if present
        const localStorage = getLocalStorage();
        localStorage.removeItem('auth_token');
        setUser(null);
      } finally {
        setIsLoading(false);
      }
    };

    checkAuth();
  }, []);

  const signIn = async (email: string, password: string) => {
    try {
      const response = await loginUser({ username: email, password });
      setUser({
        id: response.user_id,
        email: response.email,
        isAuthenticated: true,
      });
      return { success: true, data: response };
    } catch (error: any) {
      console.error('Sign in error:', error);
      // Extract error message from different possible sources
      let errorMessage = 'Login failed';
      if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail;
      } else if (error.response?.data?.message) {
        errorMessage = error.response.data.message;
      } else if (error.message) {
        errorMessage = error.message;
      }
      return { success: false, error: errorMessage };
    }
  };

  const signUp = async (email: string, password: string, name?: string) => {
    try {
      const response = await registerUser({
        name: name || email.split('@')[0], // Use part of email as name if not provided
        email,
        password
      });
      setUser({
        id: response.user_id,
        email: response.email,
        isAuthenticated: true,
      });
      return { success: true, data: response };
    } catch (error: any) {
      console.error('Sign up error:', error);
      // Extract error message from different possible sources
      let errorMessage = 'Registration failed';
      if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail;
      } else if (error.response?.data?.message) {
        errorMessage = error.response.data.message;
      } else if (error.message) {
        errorMessage = error.message;
      }
      return { success: false, error: errorMessage };
    }
  };

  const signOut = async () => {
    try {
      await logoutUser();
      setUser(null);
    } catch (error) {
      console.error('Sign out error:', error);
    }
  };

  return {
    user,
    isLoading,
    signIn,
    signUp,
    signOut,
  };
};
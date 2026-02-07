import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { useRouter } from 'next/router';

interface User {
  id: string;
  email: string;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  signIn: (email: string, password: string) => Promise<void>;
  signUp: (email: string, password: string) => Promise<void>;
  signOut: () => void;
  isAuthenticated: () => boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    // Check if user is logged in on initial load
    const token = localStorage.getItem('todo_app_auth_token');
    if (token) {
      // Verify token and get user data
      verifyTokenAndSetUser(token);
    } else {
      setLoading(false);
    }
  }, []);

  const verifyTokenAndSetUser = async (token: string) => {
    try {
      const response = await fetch('/api/auth/verify', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const userData = await response.json();
        setUser({
          id: userData.userId,
          email: userData.email,
        });
      } else {
        // Token is invalid, remove it
        localStorage.removeItem('todo_app_auth_token');
      }
    } catch (error) {
      console.error('Error verifying token:', error);
      localStorage.removeItem('todo_app_auth_token');
    } finally {
      setLoading(false);
    }
  };

  const signIn = async (email: string, password: string) => {
    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (response.ok) {
        const data = await response.json();
        // Store JWT token
        localStorage.setItem('todo_app_auth_token', data.token);

        // Set user data
        setUser({
          id: data.userId,
          email: data.email,
        });

        // Redirect to dashboard
        router.push('/dashboard');
      } else {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Login failed');
      }
    } catch (error) {
      console.error('Sign in error:', error);
      throw error;
    }
  };

  const signUp = async (email: string, password: string) => {
    try {
      const response = await fetch('/api/auth/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (response.ok) {
        const data = await response.json();
        // Auto-login after sign up
        localStorage.setItem('todo_app_auth_token', data.token);

        // Set user data
        setUser({
          id: data.userId,
          email: data.email,
        });

        // Redirect to dashboard
        router.push('/dashboard');
      } else {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Sign up failed');
      }
    } catch (error) {
      console.error('Sign up error:', error);
      throw error;
    }
  };

  const signOut = () => {
    localStorage.removeItem('todo_app_auth_token');
    setUser(null);
    router.push('/login');
  };

  const isAuthenticated = (): boolean => {
    return !!user;
  };

  const value: AuthContextType = {
    user,
    loading,
    signIn,
    signUp,
    signOut,
    isAuthenticated,
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
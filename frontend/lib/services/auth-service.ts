// lib/services/auth-service.ts
import apiClient from "./auth-api";

export interface UserRegistrationData {
  name: string;
  email: string;
  password: string;
}

export interface UserLoginData {
  username: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user_id?: number;
  email?: string;
}

const TOKEN_KEY = "auth_token";

// SSR-safe localStorage
const getLocalStorage = () => {
  if (typeof window !== "undefined") return window.localStorage;
  return {
    getItem: () => null,
    setItem: () => {},
    removeItem: () => {},
  };
};

// ✅ SINGLE source of truth
const AUTH_PREFIX = "/api/auth";

// ---------------- REGISTER ----------------
export const registerUser = async (
  userData: UserRegistrationData
): Promise<AuthResponse> => {
  try {
    const response = await apiClient.post(
      `${AUTH_PREFIX}/register`,
      userData
    );

    const localStorage = getLocalStorage();
    if (response?.data?.access_token) {
      localStorage.setItem(TOKEN_KEY, response.data.access_token);
    }

    return response.data;
  } catch (error: any) {
    console.error("Registration error:", error);
    if (error.response) {
      throw new Error(
        error.response.data?.detail ||
        error.response.data?.message ||
        "Registration failed"
      );
    }
    throw new Error("Network error: Unable to reach the server");
  }
};

// ---------------- LOGIN ----------------
export const loginUser = async (
  loginData: UserLoginData
): Promise<AuthResponse> => {
  try {
    const response = await apiClient.post(
      `${AUTH_PREFIX}/login`,
      new URLSearchParams({
        username: loginData.username,
        password: loginData.password,
      }),
      {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      }
    );

    const localStorage = getLocalStorage();
    if (response?.data?.access_token) {
      localStorage.setItem(TOKEN_KEY, response.data.access_token);
    }

    return response.data;
  } catch (error: any) {
    console.error("Login error:", error);
    if (error.response) {
      throw new Error(
        error.response.data?.detail ||
        error.response.data?.message ||
        "Login failed"
      );
    }
    throw new Error("Network error: Unable to reach the server");
  }
};

// ---------------- CURRENT USER ----------------
export const getCurrentUser = async (): Promise<any> => {
  const localStorage = getLocalStorage();
  const token = localStorage.getItem(TOKEN_KEY);

  if (!token) throw new Error("No authentication token found");

  const res = await apiClient.get(`${AUTH_PREFIX}/users/me`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return res.data;
};

// ---------------- LOGOUT ----------------
export const logoutUser = async (): Promise<void> => {
  const localStorage = getLocalStorage();
  localStorage.removeItem(TOKEN_KEY);
};

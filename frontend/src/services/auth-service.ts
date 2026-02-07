import { API_CONFIG, AUTH_CONFIG, API_ENDPOINTS, HTTP_STATUS } from '../../../shared/constants';

interface LoginCredentials {
  email: string;
  password: string;
}

interface SignUpCredentials {
  email: string;
  password: string;
}

interface User {
  id: string;
  email: string;
}

class AuthService {
  /**
   * Login user with email and password
   */
  async login(credentials: LoginCredentials): Promise<{ token: string; user: User }> {
    try {
      const response = await fetch(`${API_CONFIG.BASE_URL}${API_ENDPOINTS.AUTH.LOGIN}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Login failed');
      }

      const result = await response.json();

      // Store the JWT token
      this.setToken(result.access_token || result.token);

      return {
        token: result.access_token || result.token,
        user: result.user || { id: result.userId, email: result.email }
      };
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  }

  /**
   * Register a new user
   */
  async signUp(credentials: SignUpCredentials): Promise<{ token: string; user: User }> {
    try {
      const response = await fetch(`${API_CONFIG.BASE_URL}${API_ENDPOINTS.AUTH.SIGNUP}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Registration failed');
      }

      const result = await response.json();

      // Store the JWT token
      this.setToken(result.access_token || result.token);

      return {
        token: result.access_token || result.token,
        user: result.user || { id: result.userId, email: result.email }
      };
    } catch (error) {
      console.error('Sign up error:', error);
      throw error;
    }
  }

  /**
   * Logout user
   */
  logout(): void {
    this.removeToken();
    this.removeUserData();
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    const token = this.getToken();
    if (!token) {
      return false;
    }

    // Check if token is expired
    try {
      const payload = this.parseJwt(token);
      const currentTime = Math.floor(Date.now() / 1000);
      return payload.exp > currentTime;
    } catch (error) {
      return false;
    }
  }

  /**
   * Get current user information
   */
  getCurrentUser(): User | null {
    const userDataStr = localStorage.getItem(AUTH_CONFIG.USER_DATA_KEY);
    if (!userDataStr) {
      return null;
    }

    try {
      return JSON.parse(userDataStr);
    } catch (error) {
      console.error('Error parsing user data:', error);
      return null;
    }
  }

  /**
   * Get JWT token from storage
   */
  getToken(): string | null {
    return localStorage.getItem(AUTH_CONFIG.TOKEN_KEY);
  }

  /**
   * Set JWT token in secure storage
   */
  setToken(token: string): void {
    // Store the token in localStorage for persistence
    localStorage.setItem(AUTH_CONFIG.TOKEN_KEY, token);

    // Additionally, for enhanced security, we could also store in httpOnly cookies
    // via a backend endpoint, but for now we use localStorage/sessionStorage

    // Optionally store in sessionStorage for non-persistent sessions
    // sessionStorage.setItem(AUTH_CONFIG.TOKEN_KEY, token);
  }

  /**
   * Remove JWT token from storage
   */
  removeToken(): void {
    localStorage.removeItem(AUTH_CONFIG.TOKEN_KEY);
  }

  /**
   * Refresh JWT token before it expires
   */
  async refreshToken(): Promise<string | null> {
    try {
      const token = this.getToken();
      if (!token) {
        return null;
      }

      // Parse JWT to check if it's close to expiration (within 5 minutes)
      const payload = this.parseJwt(token);
      const exp = payload.exp;
      const currentTime = Math.floor(Date.now() / 1000);
      const timeUntilExpiry = exp - currentTime;

      // If token expires in less than 5 minutes, refresh it
      if (timeUntilExpiry < 300) { // 300 seconds = 5 minutes
        // In a real implementation, we would call a refresh endpoint
        // For now, we'll redirect to login to get a new token
        console.warn('Token is about to expire. Please re-authenticate.');
        this.logout();
        return null;

        /* In a real implementation:
        const response = await fetch(`${API_CONFIG.BASE_URL}/auth/refresh`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (response.ok) {
          const result = await response.json();
          this.setToken(result.access_token);
          return result.access_token;
        } else {
          throw new Error('Failed to refresh token');
        }
        */
      }

      return token;
    } catch (error) {
      console.error('Error refreshing token:', error);
      return null;
    }
  }

  /**
   * Store user data in local storage
   */
  setUserData(user: User): void {
    localStorage.setItem(AUTH_CONFIG.USER_DATA_KEY, JSON.stringify(user));
  }

  /**
   * Remove user data from local storage
   */
  removeUserData(): void {
    localStorage.removeItem(AUTH_CONFIG.USER_DATA_KEY);
  }

  /**
   * Check if token is expired
   */
  isTokenExpired(token?: string): boolean {
    const tokenToCheck = token || this.getToken();
    if (!tokenToCheck) {
      return true;
    }

    try {
      const payload = this.parseJwt(tokenToCheck);
      const exp = payload.exp;
      const currentTime = Math.floor(Date.now() / 1000);

      return exp < currentTime;
    } catch (error) {
      console.error('Error checking token expiration:', error);
      return true;
    }
  }

  /**
   * Get time remaining before token expires (in seconds)
   */
  getTimeUntilExpiration(): number {
    const token = this.getToken();
    if (!token) {
      return 0;
    }

    try {
      const payload = this.parseJwt(token);
      const exp = payload.exp;
      const currentTime = Math.floor(Date.now() / 1000);

      return Math.max(0, exp - currentTime);
    } catch (error) {
      console.error('Error getting time until expiration:', error);
      return 0;
    }
  }

  /**
   * Check if token is about to expire (within threshold)
   */
  isTokenExpiringSoon(thresholdSeconds: number = 300): boolean { // 5 minutes default
    return this.getTimeUntilExpiration() <= thresholdSeconds;
  }

  /**
   * Verify the JWT token with the backend
   */
  async verifyToken(): Promise<boolean> {
    const token = this.getToken();
    if (!token) {
      return false;
    }

    try {
      const response = await fetch(`${API_CONFIG.BASE_URL}${API_ENDPOINTS.AUTH.VERIFY}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      return response.status === HTTP_STATUS.SUCCESS;
    } catch (error) {
      console.error('Token verification error:', error);
      return false;
    }
  }

  /**
   * Parse JWT token to get payload
   */
  private parseJwt(token: string): any {
    try {
      const base64Url = token.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const jsonPayload = decodeURIComponent(
        atob(base64)
          .split('')
          .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
          .join('')
      );

      return JSON.parse(jsonPayload);
    } catch (error) {
      throw new Error('Invalid token format');
    }
  }
}

export default new AuthService();
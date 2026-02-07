// Simplified auth configuration that doesn't interfere with backend auth
// We'll use the backend API directly instead of initializing Better Auth here

export const auth = {
  getSession: async () => {
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('auth_token');
      if (token) {
        try {
          // Decode the JWT token to get user info
          const tokenParts = token.split('.');
          if (tokenParts.length === 3) {
            const payload = JSON.parse(atob(tokenParts[1]));
            return {
              user: {
                id: payload.sub,
                email: payload.email || 'unknown@example.com',
              },
              expiresAt: new Date(payload.exp * 1000),
            };
          }
        } catch (error) {
          console.error('Error decoding token:', error);
          return null;
        }
      }
    }
    return null;
  },
  signIn: {
    email: async ({ email, password, callbackURL }: { email: string; password: string; callbackURL: string }) => {
      // This will be handled by our auth service
      throw new Error('Use auth service instead');
    }
  },
  signUp: {
    email: async ({ email, password, name, callbackURL }: { email: string; password: string; name?: string; callbackURL: string }) => {
      // This will be handled by our auth service
      throw new Error('Use auth service instead');
    }
  },
  signOut: async () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('auth_token');
    }
  }
};

export const authHandler = null;
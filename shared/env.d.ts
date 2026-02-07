/**
 * Environment variable type definitions
 */

declare global {
  namespace NodeJS {
    interface ProcessEnv {
      // Better Auth Configuration
      readonly BETTER_AUTH_SECRET: string;
      readonly BETTER_AUTH_URL: string;

      // Database Configuration
      readonly DATABASE_URL: string;

      // Frontend Configuration
      readonly NEXT_PUBLIC_API_BASE_URL: string;
      readonly NEXT_PUBLIC_BETTER_AUTH_URL: string;

      // Environment
      readonly NODE_ENV: 'development' | 'production' | 'test';
    }
  }
}

export {};
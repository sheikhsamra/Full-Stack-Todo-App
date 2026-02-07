import { createAuthClient } from "better-auth/client";

/**
 * Better Auth Client configuration for the frontend
 */
export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || "http://localhost:3000/api/auth",
  plugins: [],
});

export default authClient;
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // Allow access to public routes
  const publicPaths = ['/', '/signin', '/signup'];
  
  // Check if the current path is protected
  const isProtectedRoute = !publicPaths.some(path => 
    request.nextUrl.pathname === path || 
    request.nextUrl.pathname.startsWith(`${path}/`)
  );

  // If accessing a protected route without authentication
  if (isProtectedRoute) {
    // Check for auth token in localStorage (we'll check this on the client side)
    // For server-side, we'll allow the route and let the client handle auth
    
    // For now, allow all routes and handle auth on the client side
    // since we can't access localStorage from server-side middleware
  }

  return NextResponse.next();
}

// Configure which paths the middleware should run on
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    {
      source: '/((?!api|_next/static|_next/image|favicon.ico).*)',
      missing: [
        { type: 'header', key: 'next-action' }
      ]
    }
  ],
};
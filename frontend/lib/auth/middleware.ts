import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { auth } from './index';

export function middleware(request: NextRequest) {
  // Protect routes that start with /tasks
  if (request.nextUrl.pathname.startsWith('/tasks')) {
    const token = request.cookies.get('better-auth-session-token');

    if (!token) {
      // Redirect to signin if no session exists
      const signInUrl = new URL('/signin', request.url);
      signInUrl.searchParams.set('return', request.nextUrl.pathname);
      return NextResponse.redirect(signInUrl);
    }
  }

  return NextResponse.next();
}

// Specify which paths the middleware should run on
export const config = {
  matcher: ['/tasks/:path*'],
};
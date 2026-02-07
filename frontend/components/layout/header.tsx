'use client';

import React from 'react';
import Link from 'next/link';
import { useAuth } from '@/hooks/use-auth';

const Header = () => {
  const { user, isLoading, signOut } = useAuth();

  return (
    <header className="bg-white shadow-sm">
      <div className="container mx-auto px-4 py-4 max-w-4xl">
        <div className="flex justify-between items-center">
          <Link href="/" className="text-xl font-bold text-blue-600">
            Todo App
          </Link>

          <nav>
            {isLoading ? (
              <div>Loading...</div>
            ) : user?.isAuthenticated ? (
              <div className="flex items-center space-x-4">
                <span className="text-gray-700">Welcome, {user.name || user.email}</span>
                <button
                  onClick={signOut}
                  className="text-sm bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded-md"
                >
                  Logout
                </button>
              </div>
            ) : (
              <div className="flex space-x-4">
                <Link href="/signin" className="text-blue-600 hover:text-blue-800">
                  Sign In
                </Link>
                <Link href="/signup" className="text-blue-600 hover:text-blue-800">
                  Sign Up
                </Link>
              </div>
            )}
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;
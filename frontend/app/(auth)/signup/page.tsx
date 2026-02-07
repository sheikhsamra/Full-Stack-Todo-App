import React from 'react';
import Card from '@/components/ui/card';
import SignupForm from '@/components/auth/signup-form';

const SignupPage = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Create Account</h1>
          <p className="text-gray-600 mt-2">Sign up to get started</p>
        </div>
        <Card className="shadow-lg">
          <SignupForm />
        </Card>
      </div>
    </div>
  );
};

export default SignupPage;
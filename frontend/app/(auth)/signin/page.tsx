import React from 'react';
import Card from '@/components/ui/card';
import SigninForm from '@/components/auth/signin-form';

const SigninPage = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Welcome Back</h1>
          <p className="text-gray-600 mt-2">Sign in to your account</p>
        </div>
        <Card className="shadow-lg">
          <SigninForm />
        </Card>
      </div>
    </div>
  );
};

export default SigninPage;
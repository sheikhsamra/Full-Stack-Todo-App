'use client';

import { AuthProvider } from '@/components/providers/auth-provider';
import Header from '@/components/layout/header';
import Footer from '@/components/layout/footer';

export default function LayoutClientWrapper({ children }: { children: React.ReactNode }) {
  return (
    <AuthProvider>
      <div className="min-h-screen flex flex-col">
        <Header />
        <main className="flex-grow w-full">
          {children}
        </main>
        <Footer />
      </div>
    </AuthProvider>
  );
}
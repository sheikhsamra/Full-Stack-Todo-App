import '../styles/globals.css';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import LayoutClientWrapper from './layout-client-wrapper';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Todo App',
  description: 'A simple todo application with authentication',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="w-full h-full">
      <body className={`${inter.className} min-h-screen w-full overflow-x-hidden bg-white`}>
        <LayoutClientWrapper>{children}</LayoutClientWrapper>
      </body>
    </html>
  );
}
/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    typedRoutes: true,
  },
  images: {
    domains: ['localhost', 'your-backend-domain.com'], // Add your backend domain here
  },
};

module.exports = nextConfig;
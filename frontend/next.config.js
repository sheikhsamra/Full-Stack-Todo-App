/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  images: {
    domains: ['localhost', 'your-backend-domain.com'],
  },
};

module.exports = nextConfig;
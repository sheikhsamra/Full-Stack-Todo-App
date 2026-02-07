/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: { typedRoutes: true },
  images: { domains: ['localhost', 'your-backend-domain.com'] },

  async redirects() {
    return [
      { source: '/', destination: '/signin', permanent: false },
    ];
  },
};

module.exports = nextConfig;

# Todo App Frontend

A responsive Next.js frontend for the Todo application with authentication and task management features.

## Features

- User authentication (signup/signin) with Better Auth
- Task management (create, read, update, delete)
- Responsive design for mobile, tablet, and desktop
- Secure API communication with JWT tokens
- Loading, empty, and error states
- Form validation

## Tech Stack

- Next.js 16+ (App Router)
- React 18+
- TypeScript
- Tailwind CSS
- Better Auth
- Axios for API calls

## Getting Started

### Prerequisites

- Node.js 18+
- Access to the backend API server

### Installation

1. Install dependencies:
```bash
npm install
```

2. Create a `.env.local` file based on `.env.example`:
```bash
cp .env.example .env.local
```

3. Update the environment variables with your configuration.

### Running the Development Server

```bash
npm run dev
```

The application will be available at [http://localhost:3000](http://localhost:3000).

## Project Structure

```
frontend/
├── app/                    # Next.js App Router pages
│   ├── (auth)/            # Public authentication pages
│   ├── (protected)/       # Protected routes
│   ├── api/               # API routes
│   └── layout.tsx         # Root layout
├── components/            # Reusable UI components
│   ├── auth/              # Authentication components
│   ├── layout/            # Layout components
│   ├── tasks/             # Task management components
│   ├── ui/                # Base UI components
│   └── providers/         # Context providers
├── hooks/                 # Custom React hooks
├── lib/                   # Utility functions and services
│   ├── auth/              # Authentication utilities
│   └── services/          # API services
├── types/                 # TypeScript type definitions
├── styles/                # Global styles
├── public/                # Static assets
├── package.json
├── next.config.js
├── tsconfig.json
└── README.md
```

## Environment Variables

- `NEXT_PUBLIC_API_BASE_URL`: Base URL for the backend API
- `NEXT_PUBLIC_APP_URL`: Application URL
- `BETTER_AUTH_SECRET`: Secret for Better Auth
- `DATABASE_URL`: Database connection URL

## Scripts

- `npm run dev`: Start development server
- `npm run build`: Build for production
- `npm run start`: Start production server
- `npm run lint`: Run linter

## API Integration

The frontend communicates with the backend API using the following endpoints:

- `/api/{user_id}/tasks` - List all tasks for a user
- `/api/{user_id}/tasks` - Create a new task
- `/api/{user_id}/tasks/{id}` - Get, update, or delete a specific task
- `/api/{user_id}/tasks/{id}/complete` - Toggle task completion

All API requests include the `Authorization: Bearer <JWT_TOKEN>` header for authentication.
# Quickstart Guide: Responsive Next.js Frontend UI

## Prerequisites

- Node.js 18+ installed
- Access to the backend FastAPI server (typically running on http://localhost:8000)
- Better Auth configured for authentication
- Valid JWT token handling mechanism

## Setup Instructions

### 1. Project Initialization

```bash
cd frontend
npm install
```

### 2. Environment Configuration

Create `.env.local` file in the frontend directory:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
```

### 3. Development Server

```bash
npm run dev
```

The application will be available at http://localhost:3000

## Key Integration Points

### Authentication Flow

1. User navigates to `/signin` or `/signup`
2. Better Auth handles credentials and returns JWT token
3. Token is stored securely and attached to API requests
4. Middleware protects routes requiring authentication

### API Communication

All API calls follow this pattern:
- Base URL: `http://localhost:8000/api`
- Authorization: `Authorization: Bearer <JWT_TOKEN>`
- Content-Type: `application/json`

Example API endpoint usage:
- GET `/api/{user_id}/tasks` - Retrieve user's tasks
- POST `/api/{user_id}/tasks` - Create new task
- GET `/api/{user_id}/tasks/{id}` - Get specific task
- PUT `/api/{user_id}/tasks/{id}` - Update task
- DELETE `/api/{user_id}/tasks/{id}` - Delete task
- PATCH `/api/{user_id}/tasks/{id}/complete` - Toggle completion

### Component Structure

- **Layout Components**: Header, Navigation, Main Container
- **Form Components**: Signin/Signup forms, Task creation/edit forms
- **Data Display**: Task lists, task cards, detail views
- **Interactive Elements**: Buttons, modals, confirmation dialogs

## Running Tests

```bash
npm test                    # Run unit tests
npm run test:e2e          # Run end-to-end tests
npm run lint              # Run linter
npm run build             # Build for production
```

## Common Tasks

### Adding a New Page
1. Create new page file in `app/` directory
2. Add proper authentication checks if needed
3. Implement responsive design with Tailwind CSS

### Creating a New Component
1. Place in appropriate directory under `components/`
2. Follow atomic design principles
3. Ensure accessibility attributes are included

### Adding API Service
1. Add new method to API client in `lib/services/api-client.ts`
2. Include proper error handling and JWT token attachment
3. Add type definitions in `types/index.ts`

## Troubleshooting

- **Authentication Issues**: Verify JWT token is being correctly stored and attached to requests
- **API Connection**: Check backend server is running and CORS is configured
- **Responsive Design**: Use browser developer tools to test different screen sizes
- **Form Validation**: Ensure client-side and server-side validation are aligned
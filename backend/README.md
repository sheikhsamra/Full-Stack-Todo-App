# Tasks API

A FastAPI-based REST API for managing user tasks with persistent storage in Neon Serverless PostgreSQL.

## Features

- Full CRUD operations for tasks
- JWT-based authentication and authorization
- User isolation - users can only access their own tasks
- Persistent storage with SQLModel and PostgreSQL

## API Endpoints

### Task Management

- `POST /api/{user_id}/tasks` - Create a new task for a user
- `GET /api/{user_id}/tasks` - List all tasks for a user
- `GET /api/{user_id}/tasks/{id}` - Get details of a specific task
- `PUT /api/{user_id}/tasks/{id}` - Update a task
- `DELETE /api/{user_id}/tasks/{id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion status

### Authentication

All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <jwt_token>
```

## Getting Started

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables (copy from .env.example):
```bash
cp .env.example .env
# Edit .env with your actual values
```

3. Start the server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000` with documentation at `http://localhost:8000/docs`.

## Development

For development, also install the dev dependencies:
```bash
pip install -r requirements-dev.txt
```

Run tests with:
```bash
pytest
```
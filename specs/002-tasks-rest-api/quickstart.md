# Quickstart Guide: Tasks REST API Development

## Prerequisites

- Python 3.11+
- pip package manager
- Git
- Neon Serverless PostgreSQL account (or local PostgreSQL for development)

## Environment Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install fastapi uvicorn sqlmodel psycopg2-binary python-jose[cryptography] python-multipart python-dotenv
pip install -r requirements-dev.txt  # if available
```

## Configuration

### 1. Environment Variables
Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/tasks_db
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

For Neon Serverless PostgreSQL, your DATABASE_URL will look like:
```
DATABASE_URL=postgresql://<dbname>:<dbpass>@ep-<endpoint>.us-east-1.aws.neon.tech/<dbname>?sslmode=require
```

### 2. Project Structure
The backend API follows this structure:

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection and session setup
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py          # Task model definition
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── task.py          # Task schemas
│   │   └── user.py          # User schemas
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py          # Dependency injection
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── tasks.py     # Task endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   ├── security.py      # Authentication and security utilities
│   │   └── config.py        # Application configuration
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
├── requirements.txt
└── alembic/
    ├── env.py
    ├── script.py.mako
    └── versions/
```

## Running the Application

### 1. Database Setup
Initialize the database tables:

```bash
python -c "from app.database import create_db_and_tables; create_db_and_tables()"
```

### 2. Start the Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000` with documentation at `http://localhost:8000/docs`.

## API Endpoints

All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <jwt_token>
```

### Available Endpoints:
- `GET    /api/{user_id}/tasks` - List user tasks
- `POST   /api/{user_id}/tasks` - Create task for user
- `GET    /api/{user_id}/tasks/{id}` - Get task details
- `PUT    /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH  /api/{user_id}/tasks/{id}/complete` - Toggle completion

## Testing

### Unit Tests
```bash
pytest tests/
```

### Manual API Testing
Using curl (replace with your actual JWT token):

```bash
# List tasks
curl -H "Authorization: Bearer <your-token>" \
     http://localhost:8000/api/1/tasks

# Create task
curl -X POST \
     -H "Authorization: Bearer <your-token>" \
     -H "Content-Type: application/json" \
     -d '{"title": "Test task", "description": "Test description"}' \
     http://localhost:8000/api/1/tasks
```

## Authentication Integration

The system reuses JWT authentication from Spec 1. The authentication dependency (`get_current_user`) should be available from the shared authentication module and must:

1. Verify the JWT token
2. Extract the user ID from the token
3. Pass the user ID to ensure it matches the `{user_id}` in the URL

## Database Schema

The system creates a `tasks` table with these columns:
- `id`: Auto-incrementing primary key
- `user_id`: Integer linking to user
- `title`: Task title (varchar 255)
- `description`: Task description (text)
- `completed`: Boolean completion status
- `created_at`: Timestamp of creation
- `updated_at`: Timestamp of last update
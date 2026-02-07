# Quickstart Guide: Authentication System

## Prerequisites
- Node.js 18+ for frontend development
- Python 3.11+ for backend development
- PostgreSQL connection (Neon Serverless)
- Better Auth compatible environment

## Setup Instructions

### 1. Environment Variables
Set up the shared environment variables:

**Backend (.env)**:
```bash
BETTER_AUTH_SECRET=your-shared-secret-key-here
DATABASE_URL=your-neon-postgres-url
```

**Frontend (.env.local)**:
```bash
NEXT_PUBLIC_BETTER_AUTH_SECRET=your-shared-secret-key-here
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### 2. Install Dependencies

**Backend**:
```bash
cd backend
pip install fastapi uvicorn sqlmodel python-multipart python-jose[cryptography] passlib[bcrypt] psycopg2-binary python-dotenv
```

**Frontend**:
```bash
cd frontend
npm install next @better-auth/react @better-auth/client
```

### 3. Initialize Better Auth in Frontend

**Create `frontend/src/lib/auth.ts`**:
```typescript
import { createAuthClient } from "@better-auth/client";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || "http://localhost:3000/api/auth",
  plugins: [],
});
```

### 4. Configure JWT Verification in Backend

**Create `backend/src/api/deps.py`**:
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any
import jwt
from datetime import datetime
from ..config import settings

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.better_auth_secret,
            algorithms=["HS256"]
        )

        user_id = payload.get("userId")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )

        return {"user_id": user_id}
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
```

### 5. Set Up User Isolation

**Create `backend/src/api/utils.py`**:
```python
from fastapi import HTTPException, status
from typing import Dict, Any

def verify_user_access(token_user_id: str, url_user_id: str) -> bool:
    """Verify that the user in the JWT matches the user_id in the URL."""
    if token_user_id != url_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Insufficient permissions"
        )
    return True
```

## Running the System

### Frontend
```bash
cd frontend
npm run dev
```

### Backend
```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

## Testing Authentication Flow

1. Visit the signup page to create a new user account
2. Login with your credentials to receive a JWT
3. The frontend will automatically attach the JWT to API requests
4. The backend will verify the JWT and enforce user isolation
5. Attempting to access another user's resources will result in a 403 Forbidden response

## API Security

All API endpoints require a valid JWT in the Authorization header:
```
Authorization: Bearer <JWT_TOKEN_HERE>
```

The system enforces the following security responses:
- 401 Unauthorized: Invalid, missing, or expired JWT
- 403 Forbidden: Valid JWT but user_id mismatch with URL parameter
- 404 Not Found: Requested resource doesn't exist in user's scope
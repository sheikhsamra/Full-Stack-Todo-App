# Data Model: Authentication System

## Entities

### User
**Description**: Represents an authenticated user in the system

**Attributes**:
- id: Unique identifier for the user (UUID/string)
- email: User's email address (string, required, unique)
- password_hash: Hashed password for authentication (string, required)
- created_at: Timestamp when user account was created (datetime)
- updated_at: Timestamp when user account was last updated (datetime)
- is_active: Boolean indicating if user account is active (boolean, default: true)

**Relationships**:
- One-to-many with user's tasks (not implemented in this spec scope)

### JWT Token
**Description**: JSON Web Token for authentication between frontend and backend

**Claims** (included in JWT payload):
- user_id: Reference to the user's unique identifier (string, required)
- exp: Expiration timestamp (number - Unix timestamp, required)
- iat: Issued-at timestamp (number - Unix timestamp, required)
- iss: Issuer identification (string, required)
- email: User's email for identification (string, optional)

**Validation Rules**:
- Token must contain valid user_id matching the expected format
- Token must not be expired (exp must be greater than current time)
- Token signature must be valid against the shared secret
- Token must contain required claims (user_id, exp)

## State Transitions

### User Authentication States
- Unauthenticated → Authenticating: User initiates login process
- Authenticating → Authenticated: Valid credentials provided, JWT issued
- Authenticated → Expired: JWT reaches expiration time
- Authenticated → Unauthenticated: Logout or token invalidation
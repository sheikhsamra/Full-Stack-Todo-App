# Research Findings: Tasks REST API + Database Persistence

## Executive Summary

This research addresses all technical unknowns and clarifies architectural decisions for the Tasks REST API feature. All decisions align with the project constitution and functional requirements from the specification.

## Key Decisions

### Task Schema Decisions
- **Decision**: Task model with required title, optional description, completion status, and automatic timestamps
- **Rationale**: Follows standard task management patterns while meeting functional requirements
- **Fields**:
  - `id`: Primary key, auto-generated
  - `user_id`: Foreign key reference to user (required for ownership)
  - `title`: String, required field
  - `description`: String, optional field
  - `completed`: Boolean, defaults to False
  - `created_at`: DateTime, auto-generated
  - `updated_at`: DateTime, auto-generated and updated

### List Behavior
- **Decision**: GET /api/{user_id}/tasks returns tasks ordered by created_at descending (newest first)
- **Rationale**: Most intuitive for users to see recently added tasks first
- **Pagination**: No pagination for initial implementation (simple list)

### Update Semantics
- **Decision**: PUT performs full replacement of task data (except user_id and timestamps)
- **Rationale**: Standard REST convention where PUT replaces the entire resource
- **PATCH**: Reserved only for the completion toggle endpoint

### Completion Toggle Behavior
- **Decision**: PATCH /api/{user_id}/tasks/{id}/complete flips the boolean value each call
- **Rationale**: The endpoint name "toggle completion" clearly indicates a boolean flip operation

### Error Policy
- **Decision**: Return 403 when user_id in URL doesn't match JWT token user (mismatch case)
- **Decision**: Return 404 when task doesn't exist within user's scope (exists for different user)
- **Rationale**: 403 indicates authorization problem (trying to access wrong user's tasks), 404 indicates the resource doesn't exist in the authorized scope

### Database Migrations Approach
- **Decision**: Use SQLModel's create_all() for initial development (hackathon context)
- **Rationale**: Simple setup for development; production would use Alembic, but this is appropriate for rapid prototyping
- **Tradeoff**: Loss of migration control vs. simplicity of setup

### Authentication Integration
- **Decision**: Leverage existing Spec 1 JWT verification system
- **Rationale**: Reuse of established authentication infrastructure as required by specification

## Technical Architecture Details

### FastAPI Service Structure
- **Router**: Separate task router with 6 endpoints mapped to requirements
- **Dependencies**: JWT verification dependency reused from Spec 1 auth
- **Database Session**: Dependency injection for SQLModel sessions with proper cleanup

### SQLModel Models
- **Task Model**: Inherits from SQLModel with appropriate constraints and validation
- **TaskCreate Schema**: Pydantic schema for POST requests (no ID, minimal required fields)
- **TaskUpdate Schema**: Pydantic schema for PUT requests (all fields optional for partial updates)
- **TaskPublic Schema**: Pydantic schema for API responses (includes all fields except internal metadata)

### Neon PostgreSQL Connection
- **Connection Pool**: Use standard PostgreSQL connection pool settings
- **Environment Variables**: Neon connection string via environment configuration
- **SSL**: Required for Neon production databases

## API Contract Specifications

### Request/Response Bodies

#### POST /api/{user_id}/tasks
- **Request Body**:
```json
{
  "title": "string (required)",
  "description": "string (optional)",
  "completed": "boolean (optional, defaults to false)"
}
```

#### PUT /api/{user_id}/tasks/{id}
- **Request Body** (all fields optional):
```json
{
  "title": "string (optional)",
  "description": "string (optional)",
  "completed": "boolean (optional)"
}
```

#### Response Bodies (consistently formatted):
```json
{
  "id": "integer",
  "user_id": "integer",
  "title": "string",
  "description": "string",
  "completed": "boolean",
  "created_at": "ISO datetime string",
  "updated_at": "ISO datetime string"
}
```

### Error Response Format (consistent across all endpoints):
```json
{
  "detail": "error message"
}
```

## Validation Rules
- **Title**: Required, minimum length 1 character, maximum length 255 characters
- **Description**: Optional, maximum length 1000 characters
- **User ID**: Must match authenticated user from JWT token
- **Task ID**: Must exist and belong to the authenticated user

## Testing Strategy Confirmed
- **Persistence**: Verify data survives application restart using Neon PostgreSQL
- **Ownership**: Ensure users can only access their own tasks via proper query scoping
- **Authentication**: Verify all endpoints reject invalid/missing JWT tokens
- **Validation**: Test all error scenarios with proper status codes
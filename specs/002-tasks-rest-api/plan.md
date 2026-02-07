# Implementation Plan: Tasks REST API + Database Persistence

**Branch**: `002-tasks-rest-api` | **Date**: 2026-02-05 | **Spec**: spec.md
**Input**: Feature specification from `/specs/002-tasks-rest-api/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a FastAPI-based REST API for managing user tasks with persistent storage in Neon Serverless PostgreSQL. The system provides full CRUD operations for tasks with authentication and user isolation enforced through JWT tokens from Better Auth. Each endpoint requires valid JWT authentication and validates that the authenticated user matches the user_id in the URL to ensure proper user isolation.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: FastAPI, SQLModel, Neon PostgreSQL, python-jose
**Storage**: Neon Serverless PostgreSQL database with persistent storage
**Testing**: pytest for unit and integration testing
**Target Platform**: Linux server (cloud deployment ready)
**Project Type**: web (backend API service)
**Performance Goals**: <200ms p95 response time for API endpoints
**Constraints**: JWT authentication required for all endpoints, user isolation enforcement
**Scale/Scope**: Multi-user support with proper data isolation

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Compliance Verification:
✅ **Spec-Driven Execution**: Following Spec → Plan → Tasks → Implement workflow
✅ **Security-First**: All endpoints require JWT authentication and enforce user isolation
✅ **Correctness Over Convenience**: API behavior matches requirements exactly
✅ **Reliability**: Standardized HTTP status codes and consistent error responses
✅ **Technology Stack**: Using required technologies (FastAPI, SQLModel, Neon PostgreSQL, Better Auth)

### Gates Status:
- [PASS] Authentication requirement met (JWT verification on all endpoints)
- [PASS] User isolation enforcement (user_id validation against JWT token)
- [PASS] Required API endpoints implemented as specified
- [PASS] Technology stack compliance (FastAPI, SQLModel, Neon PostgreSQL)
- [PASS] Persistent storage requirement (Neon Serverless PostgreSQL)

## Project Structure

### Documentation (this feature)

```text
specs/002-tasks-rest-api/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   └── tasks-api.yaml   # OpenAPI specification
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
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
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Test configuration
│   ├── test_tasks.py        # Task API tests
│   └── test_auth.py         # Authentication tests
├── requirements.txt         # Python dependencies
├── requirements-dev.txt     # Development dependencies
└── alembic/                 # Database migration files
    ├── env.py
    ├── script.py.mako
    └── versions/
```

**Structure Decision**: Selected web application structure with dedicated backend service for API implementation. This separates concerns between frontend and backend while maintaining clear API contracts.

## Architecture Design

### FastAPI Service Components

1. **Main Application (main.py)**: Entry point with CORS configuration and route registration
2. **Database Layer (database.py)**: Connection management and session handling with SQLModel
3. **Models (models/task.py)**: SQLModel definitions for Task entity with validation
4. **Schemas (schemas/)**: Pydantic models for request/response validation
5. **API Routes (api/v1/tasks.py)**: Six endpoints implementing required functionality
6. **Dependencies (api/deps.py)**: JWT authentication dependency with user validation
7. **Security (core/security.py)**: JWT token verification and user extraction

### Data Model
- **Task Entity**: Contains id, user_id, title, description, completed status, and timestamps
- **User Association**: user_id field links tasks to authenticated users from JWT
- **Validation**: Title required (1-255 chars), description optional (0-1000 chars), completion defaults to false
- **Indexing**: Optimized for user-based queries and completion status filtering

### API Contract Implementation
- **GET /api/{user_id}/tasks**: Lists tasks for authenticated user (200) or errors (401/403/404)
- **POST /api/{user_id}/tasks**: Creates task for authenticated user (201) or errors (400/401/403)
- **GET /api/{user_id}/tasks/{id}**: Retrieves specific task (200) or errors (401/403/404)
- **PUT /api/{user_id}/tasks/{id}**: Updates entire task (200) or errors (400/401/403/404)
- **DELETE /api/{user_id}/tasks/{id}**: Removes task (204) or errors (401/403/404)
- **PATCH /api/{user_id}/tasks/{id}/complete**: Toggles completion status (200) or errors (401/403/404)

### Security Implementation
- **JWT Validation**: All endpoints require valid JWT token from Authorization header
- **User ID Matching**: Validates JWT user matches {user_id} in URL path
- **Query Isolation**: Database queries scoped to authenticated user's tasks only
- **Error Differentiation**: 403 for user mismatch, 404 for non-existent tasks in scope

## Implementation Phases

### Phase 1: Foundation Setup
1. Database configuration with Neon PostgreSQL
2. SQLModel task model with proper relationships and validation
3. Pydantic schemas for request/response validation
4. Authentication dependency with JWT verification

### Phase 2: API Implementation
1. Implement six required endpoints with proper HTTP methods
2. Add authentication and user validation to all endpoints
3. Implement error handling with appropriate status codes
4. Connect endpoints to database operations using SQLModel

### Phase 3: Testing and Validation
1. Unit tests for individual components
2. Integration tests for API endpoints
3. Authentication and authorization validation tests
4. Error condition testing for all status codes

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |
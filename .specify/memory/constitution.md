<!-- SYNC IMPACT REPORT
Version change: N/A (initial version) → 1.0.0
Modified principles: N/A
Added sections: All principles and sections (initial constitution)
Removed sections: N/A
Templates requiring updates:
- .specify/templates/plan-template.md ⚠ pending
- .specify/templates/spec-template.md ⚠ pending
- .specify/templates/tasks-template.md ⚠ pending
- .specify/templates/commands/*.md ⚠ pending
Follow-up TODOs: None
-->
# Todo Full-Stack Web Application Constitution

## Core Principles

### Spec-Driven Execution Only
Spec-driven execution only: Spec → Plan → Tasks → Implement via Claude Code (no manual coding). All development must follow the agentic dev stack workflow using Claude Code and Spec-Kit Plus, with no manual coding allowed.

### Security-First
Security-first: every operation must be authenticated and user-isolated. All API endpoints require valid JWT authentication and must enforce strict user isolation, returning only data belonging to the authenticated user.

### Correctness Over Convenience
Correctness over convenience: API behavior must match requirements exactly. All REST endpoints must follow the specified contract with consistent status codes and error responses, ensuring predictable behavior.

### Maintainability
Maintainability: clean separation between Next.js frontend and FastAPI backend. Services must be independently deployable with clear API contracts and well-defined responsibilities.

### Reliability
Reliability: predictable errors, consistent status codes, and stable interfaces. All API endpoints must return standardized HTTP status codes with consistent error message formats.

## API and Security Standards
All REST endpoints are protected and require `Authorization: Bearer <JWT>`. Authentication model: Better Auth (Next.js) issues JWT; FastAPI verifies JWT using shared secret. User isolation: backend must only return/modify tasks belonging to authenticated user. Ownership enforcement: token user must match `{user_id}` in the URL; reject mismatch with appropriate status code.

RESTful consistency:
- 200/201 for success
- 400 for validation errors
- 401 for missing/invalid/expired token
- 403 for user_id mismatch / forbidden access
- 404 when task not found within user scope

## Development Workflow
Development must follow the Spec → Plan → Tasks → Implement workflow using Claude Code and Spec-Kit Plus tools. Only Claude Code + Spec-Kit Plus workflow is permitted, with no manual coding. Each layer must use the designated technologies:
- Frontend: Next.js 16+ (App Router)
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth (frontend) + JWT verification (backend)

Required API endpoints must be implemented as specified:
- GET    /api/{user_id}/tasks
- POST   /api/{user_id}/tasks
- GET    /api/{user_id}/tasks/{id}
- PUT    /api/{user_id}/tasks/{id}
- DELETE /api/{user_id}/tasks/{id}
- PATCH  /api/{user_id}/tasks/{id}/complete

## Governance

Constitution governs all development activities for the Todo Full-Stack Web Application. All code must comply with these principles. Amendments require explicit documentation and approval via the Spec-Kit Plus workflow. Development teams must verify compliance with all principles during reviews and testing. The constitution supersedes all other practices and guidelines.

**Version**: 1.0.0 | **Ratified**: 2026-02-05 | **Last Amended**: 2026-02-05

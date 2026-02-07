# ADR-0001: Task API Architecture with JWT Authentication

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2026-02-05
- **Feature:** 002-tasks-rest-api

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

We will implement a JWT-based authentication system using the existing Better Auth integration with the following components:

- **Authentication Layer**: Reuse the JWT verification system from Spec 1, leveraging python-jose for token validation
- **User Identification**: Extract user ID from JWT token and validate it matches the {user_id} in the URL path
- **Database Query Isolation**: All database queries will be scoped to the authenticated user by including user_id filters
- **Error Handling**: Return 401 for invalid/missing tokens, 403 for user_id mismatches, and 404 for resources not found within the user's scope
- **Token Validation**: Implement middleware/validation dependency in FastAPI to verify JWT authenticity and extract user identity

The specific implementation will include:
- FastAPI dependency injection for authentication checks
- SQLModel queries filtered by user_id to ensure data isolation
- Standardized error responses with consistent format
- Reuse of existing JWT signing keys and validation logic from Spec 1

## Consequences

### Positive

- Strong security posture with user isolation enforced at both API and database layers
- Reuse of existing authentication infrastructure reduces development time and potential security flaws
- Clear error responses help with debugging and proper client-side error handling
- Compliant with project constitution security-first principle
- Scalable solution that can handle multiple users safely

### Negative

- Additional network overhead for JWT validation on each request
- Tight coupling between API and authentication system - changes to auth would impact all endpoints
- Complexity in testing due to authentication requirements for all endpoints
- Potential performance impact from additional database filtering by user_id

## Alternatives Considered

- **Session-based authentication**: Would require server-side session storage and management, increasing infrastructure complexity. Less suitable for a microservice architecture.
- **API Keys**: Would require secure storage and rotation mechanisms, and would be less convenient for user-facing applications where session management is needed.
- **OAuth 2.0 with Bearer Tokens**: More complex to implement than JWT, though potentially more flexible. Overkill for this specific use case.
- **Cookie-based authentication**: Would work but doesn't align with REST API principles and would be harder to consume from various clients.
- **Database-level row security**: Could implement at the database level, but would lose the ability to handle business logic and proper error responses at the application level.

## References

- Feature Spec: specs/002-tasks-rest-api/spec.md
- Implementation Plan: specs/002-tasks-rest-api/plan.md
- Related ADRs: none
- Evaluator Evidence: specs/002-tasks-rest-api/research.md
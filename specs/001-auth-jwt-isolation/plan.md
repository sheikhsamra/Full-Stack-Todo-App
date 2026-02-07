# Implementation Plan: Authentication, JWT, and User Isolation

**Branch**: `001-auth-jwt-isolation` | **Date**: 2026-02-05 | **Spec**: [link]
**Input**: Feature specification from `/specs/001-auth-jwt-isolation/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement secure user authentication with Better Auth (Next.js) issuing JWT tokens, which are transmitted to FastAPI backend via Authorization header for stateless verification. Enforce user isolation by matching authenticated user identity from JWT with `{user_id}` in URL path to prevent cross-user data access.

## Technical Context

**Language/Version**: Python 3.11, JavaScript/TypeScript (Next.js 16+)
**Primary Dependencies**: Better Auth (frontend), FastAPI (backend), SQLModel (ORM)
**Storage**: Neon Serverless PostgreSQL (database)
**Testing**: pytest (backend), Jest/Vitest (frontend)
**Target Platform**: Web application (multi-user)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: <200ms p95 JWT verification latency, <1000ms auth flow completion
**Constraints**: Must follow RESTful consistency (401/403/404 status codes), secure JWT handling, user isolation enforcement
**Scale/Scope**: Multi-user web application supporting thousands of concurrent users

## Architecture Overview

### High-Level Architecture
```
┌─────────────┐    Issues JWT    ┌─────────────────┐
│   Next.js   │ ──────────────→ │ Better Auth     │
│  Frontend   │ ←────────────── │ (Authentication)│
└─────────────┘   Attaches Bearer└─────────────────┘
       │                    │
       │ Sends requests w/  │
       │ Authorization:     │
       │ Bearer <JWT>      │
       ▼                   │
┌─────────────────┐        │
│  API Gateway/   │        │
│  Load Balancer  │ ←──────┘
└─────────────────┘
       │
       │ Forward to FastAPI
       ▼
┌─────────────────┐    Verify JWT    ┌─────────────────┐
│  FastAPI        │ ──────────────→ │ JWT Verification│
│  Backend       │ ←────────────── │ (Stateless)     │
└─────────────────┘   Validate sig  └─────────────────┘
       │                      │
       │ Match user_id in URL │
       │ with JWT claims      │
       ▼                      │
┌─────────────────┐           │
│  User Isolation │ ←─────────┘
│  Enforcement    │
└─────────────────┘
       │
       ▼
┌─────────────────┐
│ Neon PostgreSQL │
│  Database       │
└─────────────────┘
```

### Security Flow Diagram
```
User Login → Better Auth → JWT Issued → Attach to API requests → FastAPI → JWT Verification → User ID Match → Access Granted/Denied
    │            │             │                  │               │         │              │              │
    │            │             │                  │               │         │              │              │
    │            │             │                  │               │         │              │              │
   Register  →  Validate    → Include user_id,  → Authorization  → Decode  → Compare      → Allow/Reject → Return result
              credentials      exp, iss claims     header         claims    user_id from   request based
                            → Set expiration                       → Validate JWT          JWT with URL    on match
                            for security                           signature
```

## Implementation Phases

### Phase 1: Auth Setup
- Configure Better Auth in Next.js application
- Set up JWT issuance with required claims (user_id, exp, etc.)
- Configure shared secret for JWT signing/verification

### Phase 2: Frontend Integration
- Implement JWT storage and retrieval in frontend
- Create API client that attaches Authorization header to all requests
- Handle token expiry and refresh mechanisms

### Phase 3: Backend Verification
- Implement JWT verification middleware in FastAPI
- Create dependency injection for authenticated user
- Validate JWT signature, expiration, and required claims

### Phase 4: User Isolation Enforcement
- Create route parameter validation to match JWT user_id with URL user_id
- Implement consistent error responses (401/403/404)
- Ensure all endpoints require authentication

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Passed Checks**:
- ✅ Spec-driven execution: Following Spec → Plan → Tasks → Implement workflow
- ✅ Security-first: All operations will be authenticated and user-isolated
- ✅ Correctness over convenience: Will follow exact API behavior requirements
- ✅ Maintainability: Clean separation between Next.js frontend and FastAPI backend
- ✅ Reliability: Predictable error handling with consistent status codes

**API and Security Standards Compliance**:
- ✅ All REST endpoints protected with `Authorization: Bearer <JWT>`
- ✅ Better Auth (Next.js) issues JWT; FastAPI verifies JWT using shared secret
- ✅ User isolation: backend returns/modify data only for authenticated user
- ✅ Ownership enforcement: token user must match `{user_id}` in URL
- ✅ RESTful consistency: 401 for invalid token, 403 for user_id mismatch

## Testing Strategy

### Authentication Validation
- Request without Authorization header → 401 Unauthorized
- Request with malformed or invalid JWT → 401 Unauthorized
- Request with expired JWT → 401 Unauthorized

### Authorization & Isolation Validation
- Valid JWT but mismatched `{user_id}` → 403 Forbidden
- Valid JWT and matching `{user_id}` → request allowed

### Integration Checks
- Frontend successfully attaches JWT on all API requests
- Backend correctly extracts and decodes user identity from JWT

### Security Regression Checks
- Ensure no endpoint is accessible without JWT after auth is enabled

## Key Decisions Documented

### JWT Verification Approach in FastAPI
**Decision**: Use FastAPI Dependency Injection pattern rather than middleware for JWT verification
**Rationale**: Dependencies provide better integration with FastAPI's type system and validation, allowing strongly-typed current_user parameters in route handlers
**Alternative Considered**: Middleware approach - rejected because it's less integrated with FastAPI's native patterns

### JWT Claim Requirements
**Decision**: JWT MUST contain "user_id", "exp", "iat", and "iss" claims
**Rationale**: user_id for identity matching, exp for security, iat for validity checks, iss for token origin verification
**Alternative Considered**: Minimal claims (user_id, exp only) - rejected because additional claims provide better security context

### Error-Handling Strategy
**Decision**: Strict consistency - 401 for auth issues, 403 for authorization issues
**Rationale**: Maintains predictable API behavior as per constitution standards
**Implementation**: Missing/invalid/expired token → 401; user_id mismatch → 403

### Environment Variable Management
**Decision**: Use shared BETTER_AUTH_SECRET environment variable in both frontend and backend
**Rationale**: Enables consistent JWT signing/verification while keeping secrets configurable
**Security**: Production deployments must use proper secret management (not hardcoded values)

## Project Structure

### Documentation (this feature)

```text
specs/001-auth-jwt-isolation/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── user.py          # User entity model
│   │   └── __init__.py
│   ├── services/
│   │   ├── auth.py          # JWT verification logic
│   │   ├── user_service.py  # User operations
│   │   └── __init__.py
│   ├── api/
│   │   ├── deps.py          # Dependency injection for auth
│   │   ├── auth_router.py   # Authentication endpoints
│   │   ├── main.py          # Main API router
│   │   └── __init__.py
│   └── main.py              # FastAPI app instance
└── tests/
    ├── unit/
    ├── integration/
    └── conftest.py

frontend/
├── src/
│   ├── components/
│   │   ├── auth/
│   │   │   ├── Login.tsx
│   │   │   ├── Signup.tsx
│   │   │   └── AuthProvider.tsx
│   │   └── ...
│   ├── services/
│   │   ├── api-client.ts    # API client with JWT attachment
│   │   ├── auth-service.ts  # Authentication logic
│   │   └── ...
│   ├── pages/
│   │   ├── login/
│   │   ├── signup/
│   │   └── ...
│   └── types/
│       ├── user.ts
│       └── auth.ts
└── tests/
    ├── unit/
    ├── integration/
    └── setup.ts

shared/
├── env.d.ts               # Environment variable types
└── constants.ts           # Shared constants
```

**Structure Decision**: Web application with separate frontend and backend directories, enabling clear separation of concerns while maintaining integration through API contracts.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |

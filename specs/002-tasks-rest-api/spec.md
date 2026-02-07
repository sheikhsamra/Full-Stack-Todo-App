# Feature Specification: Tasks REST API + Database Persistence

**Feature Branch**: `002-tasks-rest-api`
**Created**: 2026-02-05
**Status**: Draft
**Input**: User description: "Todo Full-Stack Web Application — Spec 2: Tasks REST API + Database Persistence

Target audience:
- Claude Code agents implementing backend data model and REST API
- Reviewers validating required endpoints, persistence, and user-scoped behavior

Focus:
- SQLModel task schema and Neon Serverless PostgreSQL persistence
- Full RESTful CRUD for tasks + completion toggle endpoint
- Enforce task ownership: every operation scoped to authenticated user from JWT
- API correctness: routes, methods, status codes, and error handling

Success criteria:
- Neon PostgreSQL stores tasks persistently (survive service restart)
- SQLModel models created for tasks with an owner/user_id field
- All required endpoints exist and behave correctly:
  - GET    /api/{user_id}/tasks                (list user tasks)
  - POST   /api/{user_id}/tasks                (create task for user)
  - GET    /api/{user_id}/tasks/{id}           (get task details)
  - PUT    /api/{user_id}/tasks/{id}           (update task)
  - DELETE /api/{user_id}/tasks/{id}           (delete task)
  - PATCH  /api/{user_id}/tasks/{id}/complete  (toggle completion)
- All endpoints require valid JWT (401 when missing/invalid/expired)
- Token user must match `{user_id}`; mismatches rejected (403)
- User isolation is enforced in queries:
  - Users can only list/read/update/delete their own tasks
  - Requests for other users' tasks return forbidden/not-found within scope
- Proper error handling:
  - 404 when a task id does not exist within the authenticated user's scope
  - 400 for validation errors (bad payload)

Constraints:
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL (no in-memory storage)
- Authentication: Must reuse Spec 1 verification + identity extraction (do not re-invent auth)
- No manual coding: Spec → Plan → Tasks → Implement via Claude Code
- Keep endpoints exactly as specified (paths and methods)

Not building:
- Frontend UI for tasks (belongs to Spec 3)
- Admin dashboards or analytics
- Advanced task features (labels, reminders, recurring tasks, sharing)
- Full-text search or filtering beyond simple listing (unless required)
- Background jobs / queues / notifications"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create New Task (Priority: P1)

An authenticated user can create a new task for themselves by submitting task details via POST request. The task gets stored in the database with the user's identity linked to it for proper ownership.

**Why this priority**: This is the foundational functionality that allows users to actually add items to their personal task list, which is the core purpose of the application.

**Independent Test**: Can be fully tested by authenticating a user, making a POST request to create a task, and verifying the task was saved with the correct user association in the database.

**Acceptance Scenarios**:

1. **Given** an authenticated user with valid JWT token, **When** they POST to `/api/{user_id}/tasks` with valid task data, **Then** a new task is created and assigned to that user with 201 Created status
2. **Given** an authenticated user's token with mismatched `{user_id}` in URL, **When** they POST to `/api/{different_user_id}/tasks`, **Then** the request is rejected with 403 Forbidden status

---

### User Story 2 - View and Manage Tasks (Priority: P1)

An authenticated user can view their own tasks, update details, toggle completion status, and delete tasks they own, while being prevented from accessing other users' tasks.

**Why this priority**: These are the essential CRUD operations that make the task management system functional, allowing users to interact with their tasks effectively.

**Independent Test**: Can be fully tested by creating a user with several tasks, then testing GET, PUT, PATCH, and DELETE operations on those tasks, ensuring proper user isolation and error handling.

**Acceptance Scenarios**:

1. **Given** an authenticated user with tasks in the system, **When** they GET `/api/{user_id}/tasks`, **Then** they receive a list of only their own tasks
2. **Given** an authenticated user requesting a task that doesn't exist in their scope, **When** they GET `/api/{user_id}/tasks/{nonexistent_id}`, **Then** they receive 404 Not Found
3. **Given** an authenticated user requesting another user's task, **When** they access `/api/{other_user_id}/tasks/{existing_id}`, **Then** they receive 403 Forbidden or 404 Not Found

---

### User Story 3 - Secure API Access with Task Ownership (Priority: P2)

The system enforces proper authentication and authorization on all task endpoints, ensuring users can only operate on tasks they own while handling errors appropriately.

**Why this priority**: Security and user isolation are critical to prevent unauthorized access to other users' data and ensure proper error responses for validation issues.

**Independent Test**: Can be fully tested by attempting unauthorized access to endpoints, malformed requests, and validation errors to ensure proper 401, 403, and 400 responses respectively.

**Acceptance Scenarios**:

1. **Given** a request without valid JWT token, **When** accessing any task endpoint, **Then** the system returns 401 Unauthorized
2. **Given** a request with valid JWT but malformed task data, **When** posting or updating a task, **Then** the system returns 400 Bad Request
3. **Given** a request with valid JWT for a user accessing their own task, **When** making any operation, **Then** the operation succeeds according to the endpoint specification

---

### Edge Cases

- What happens when the JWT token expires during a long-running operation?
- How does the system handle concurrent updates to the same task?
- What happens when the Neon PostgreSQL database is temporarily unavailable?
- How does the system handle extremely large payloads for task creation?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST store tasks persistently in Neon PostgreSQL database using SQLModel
- **FR-002**: System MUST require valid JWT authentication on all task endpoints (401 when missing/invalid/expired)
- **FR-003**: System MUST validate that JWT token user matches `{user_id}` in URL (403 for mismatch)
- **FR-004**: System MUST allow users to create tasks via POST `/api/{user_id}/tasks` with 201 Created response
- **FR-005**: System MUST allow users to list their tasks via GET `/api/{user_id}/tasks` with 200 OK response
- **FR-006**: System MUST allow users to retrieve specific task via GET `/api/{user_id}/tasks/{id}` with 200 OK or 404 Not Found
- **FR-007**: System MUST allow users to update tasks via PUT `/api/{user_id}/tasks/{id}` with 200 OK or 404 Not Found
- **FR-008**: System MUST allow users to delete tasks via DELETE `/api/{user_id}/tasks/{id}` with 204 No Content or 404 Not Found
- **FR-009**: System MUST allow users to toggle completion via PATCH `/api/{user_id}/tasks/{id}/complete` with 200 OK or 404 Not Found
- **FR-010**: System MUST return 404 Not Found when task ID doesn't exist within user's scope
- **FR-011**: System MUST return 400 Bad Request when request payload fails validation
- **FR-012**: System MUST enforce user isolation by only allowing access to tasks owned by the authenticated user

### Key Entities *(include if feature involves data)*

- **Task**: Represents a user's task with title, description, completion status, user_id, timestamps, and unique identifier
- **User**: The authenticated user who owns the tasks (reused from Spec 1 authentication system)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of authenticated POST requests to create tasks result in persistent storage in Neon PostgreSQL (survives service restart)
- **SC-002**: 100% of requests without valid JWT tokens are rejected with 401 Unauthorized status
- **SC-003**: 100% of requests with valid JWT but mismatched user_id are rejected with 403 Forbidden status
- **SC-004**: 100% of requests for non-existent tasks within user scope return 404 Not Found status
- **SC-005**: 100% of properly authenticated CRUD operations on user's own tasks complete successfully with appropriate status codes
- **SC-006**: 99.9% of validation error scenarios return appropriate 400 Bad Request responses with clear error messages

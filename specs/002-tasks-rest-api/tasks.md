# Implementation Tasks: Tasks REST API + Database Persistence

**Feature**: Tasks REST API + Database Persistence
**Branch**: `002-tasks-rest-api`
**Input**: `/specs/002-tasks-rest-api/spec.md`, `/specs/002-tasks-rest-api/plan.md`

## Overview
This document breaks down the implementation of the Tasks REST API into testable, executable tasks. Each task follows the spec-driven approach with the following phases:
- Phase 1: Setup foundational components
- Phase 2: Foundational elements needed by all user stories
- Phase 3+: Implementation of each user story in priority order
- Final Phase: Polishing and cross-cutting concerns

## Dependencies Between User Stories
- All user stories depend on foundational setup (Phase 1-2)
- US1 (Create New Task) is foundational for US2 (View and Manage Tasks)
- US3 (Secure API Access) applies to all other stories as a cross-cutting concern

## Parallel Execution Opportunities
- Schema definitions (models/schemas) can be developed in parallel with authentication components
- Individual endpoint implementations can be parallelized after foundational components are complete
- Testing can be parallelized with implementation in separate test files

## Implementation Strategy
1. **MVP Scope**: Focus on US1 (Create New Task) first for core functionality
2. **Incremental Delivery**: Each user story builds upon previous foundations
3. **Test Early**: Validate authentication and data persistence early in the process

---

## Phase 1: Setup

### Goal
Initialize project structure and install required dependencies.

- [X] T001 Create backend directory structure per plan.md
- [X] T002 Create requirements.txt with FastAPI, SQLModel, Neon PostgreSQL, python-jose dependencies
- [X] T003 [P] Create initial app/__init__.py and app/main.py files
- [X] T004 [P] Create directory structure: app/models/, app/schemas/, app/api/, app/core/, app/utils/
- [X] T005 Create requirements-dev.txt with pytest and testing dependencies

## Phase 2: Foundational Components

### Goal
Implement database connection, authentication components, and base models needed by all user stories.

- [X] T006 Create app/database.py with Neon PostgreSQL connection setup
- [X] T007 Create app/models/task.py with SQLModel Task model based on data-model.md
- [X] T008 Create app/schemas/task.py with Pydantic schemas for request/response validation
- [X] T009 [P] Create app/core/config.py for configuration settings
- [X] T010 [P] Create app/core/security.py with JWT token verification functions
- [X] T011 [P] Create app/api/deps.py with authentication dependency functions
- [X] T012 Create app/api/v1/__init__.py and app/api/v1/tasks.py files

## Phase 3: User Story 1 - Create New Task (Priority: P1)

### Story Goal
An authenticated user can create a new task for themselves by submitting task details via POST request. The task gets stored in the database with the user's identity linked to it for proper ownership.

### Independent Test Criteria
Can be fully tested by authenticating a user, making a POST request to create a task, and verifying the task was saved with the correct user association in the database.

### Tasks

- [X] T013 [US1] Implement POST /api/{user_id}/tasks endpoint in app/api/v1/tasks.py
- [X] T014 [US1] Add authentication validation to ensure JWT user matches {user_id} in URL
- [X] T015 [US1] Implement database creation logic for Task model with user association
- [X] T016 [US1] Add proper validation for required fields (title)
- [X] T017 [US1] Return 201 Created status with full task data after successful creation
- [X] T018 [US1] Return 403 Forbidden when token user doesn't match URL {user_id}
- [X] T019 [US1] Return 400 Bad Request when validation fails (e.g., missing title)
- [X] T020 [US1] Return 401 Unauthorized when no valid JWT token provided

## Phase 4: User Story 2 - View and Manage Tasks (Priority: P1)

### Story Goal
An authenticated user can view their own tasks, update details, toggle completion status, and delete tasks they own, while being prevented from accessing other users' tasks.

### Independent Test Criteria
Can be fully tested by creating a user with several tasks, then testing GET, PUT, PATCH, and DELETE operations on those tasks, ensuring proper user isolation and error handling.

### Tasks

- [X] T021 [US2] Implement GET /api/{user_id}/tasks endpoint to list user's tasks
- [X] T022 [US2] Add authentication and user validation to GET list endpoint
- [X] T023 [US2] Implement database query to retrieve only tasks belonging to authenticated user
- [X] T024 [US2] Implement GET /api/{user_id}/tasks/{id} endpoint to get specific task
- [X] T025 [US2] Add validation to ensure task belongs to authenticated user
- [X] T026 [US2] Return 404 Not Found when task doesn't exist in user's scope
- [X] T027 [US2] Implement PUT /api/{user_id}/tasks/{id} endpoint to update task
- [X] T028 [US2] Add validation to ensure user can only update their own tasks
- [X] T029 [US2] Implement DELETE /api/{user_id}/tasks/{id} endpoint to delete task
- [X] T030 [US2] Return 204 No Content after successful deletion
- [X] T031 [US2] Implement PATCH /api/{user_id}/tasks/{id}/complete endpoint to toggle completion
- [X] T032 [US2] Update task's completion status and return updated task data
- [X] T033 [US2] Ensure all endpoints enforce proper user isolation (403 for cross-user access)

## Phase 5: User Story 3 - Secure API Access (Priority: P2)

### Story Goal
The system enforces proper authentication and authorization on all task endpoints, ensuring users can only operate on tasks they own while handling errors appropriately.

### Independent Test Criteria
Can be fully tested by attempting unauthorized access to endpoints, malformed requests, and validation errors to ensure proper 401, 403, and 400 responses respectively.

### Tasks

- [ ] T034 [US3] Consolidate and standardize error response format across all endpoints
- [ ] T035 [US3] Implement consistent 401 Unauthorized responses when JWT is missing/invalid
- [ ] T036 [US3] Implement consistent 403 Forbidden responses when user_id mismatch occurs
- [ ] T037 [US3] Enhance validation error handling to return 400 with clear messages
- [ ] T038 [US3] Add comprehensive input validation for all endpoints
- [ ] T039 [US3] Add rate limiting or throttling considerations to security layer
- [ ] T040 [US3] Document all security measures and error scenarios in API documentation

## Phase 6: Testing & Validation

### Goal
Implement comprehensive tests to validate all functionality meets acceptance criteria.

- [ ] T041 Create test fixtures in tests/conftest.py for database and authentication
- [ ] T042 [P] Create tests/test_tasks.py with unit tests for task operations
- [ ] T043 [P] Create tests/test_auth.py with authentication and authorization tests
- [ ] T044 [P] [US1] Write integration tests for POST /api/{user_id}/tasks endpoint
- [ ] T045 [P] [US1] Test 403 rejection when JWT user doesn't match URL user_id
- [ ] T046 [P] [US2] Write integration tests for GET, PUT, DELETE endpoints
- [ ] T047 [P] [US2] Test user isolation: ensure users can't access others' tasks
- [ ] T048 [P] [US3] Write security tests for all error scenarios (401, 403, 400)
- [ ] T049 [P] Test persistent storage by restarting app and verifying data integrity
- [ ] T050 Run all tests to validate complete functionality

## Phase 7: Polish & Cross-Cutting Concerns

### Goal
Complete the implementation with documentation, configuration, and deployment readiness.

- [ ] T051 Add comprehensive API documentation with examples
- [ ] T052 Create sample .env file with proper configuration variables
- [ ] T053 Add logging configuration for monitoring and debugging
- [ ] T054 Optimize database queries and add appropriate indexes
- [ ] T055 Set up CORS configuration in FastAPI app
- [ ] T056 Add health check endpoint for monitoring
- [ ] T057 Update README with API usage instructions
- [ ] T058 Perform final validation against all success criteria in spec.md

---

## Implementation Notes
- All database operations must use SQLModel with proper session management
- Authentication must leverage existing Spec 1 JWT verification system
- All endpoints must enforce user isolation to prevent cross-user data access
- Error responses must follow consistent JSON format: {"detail": "error message"}
- Input validation must occur at both API and database model levels
---
description: "Task list for Responsive Next.js Frontend UI implementation"
---

# Tasks: Responsive Next.js Frontend UI

**Input**: Design documents from `/specs/003-frontend-ui/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- Paths adjusted for Next.js frontend application

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create Next.js 16+ project structure in frontend/ directory
- [X] T002 Initialize package.json with Next.js, React, Tailwind CSS, Better Auth dependencies
- [X] T003 [P] Configure TypeScript, ESLint, and Prettier in frontend/
- [X] T004 [P] Configure Tailwind CSS and globals.css in frontend/styles/
- [X] T005 Setup Next.js App Router configuration in next.config.js

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 Setup Better Auth configuration for Next.js App Router in frontend/lib/auth/
- [X] T007 [P] Create API client service for JWT token handling in frontend/lib/services/api-client.ts
- [X] T008 [P] Configure middleware for route protection in frontend/lib/auth/middleware.ts
- [X] T009 Create shared types based on data-model.md in frontend/types/index.ts
- [X] T010 Create reusable UI components foundation in frontend/components/ui/
- [X] T011 Setup layout structure with header/footer in frontend/app/layout.tsx
- [X] T012 Configure environment variables for API connection

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Authentication Flow (Priority: P1) 🎯 MVP

**Goal**: Enable users to signup and signin via Better Auth with proper session handling

**Independent Test**: User can navigate to signin/signup pages, submit credentials, and gain access to protected routes

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

- [ ] T013 [P] [US1] Contract test for authentication endpoints in frontend/tests/contract/test-auth.js
- [ ] T014 [P] [US1] Integration test for authentication flow in frontend/tests/integration/test-auth-flow.js

### Implementation for User Story 1

- [X] T015 [P] [US1] Create signin page component in frontend/app/(auth)/signin/page.tsx
- [X] T016 [P] [US1] Create signup page component in frontend/app/(auth)/signup/page.tsx
- [X] T017 [P] [US1] Create signin form component in frontend/components/auth/signin-form.tsx
- [X] T018 [P] [US1] Create signup form component in frontend/components/auth/signup-form.tsx
- [X] T019 [US1] Implement authentication hooks in frontend/hooks/use-auth.ts
- [X] T020 [US1] Configure protected route layout in frontend/app/(protected)/layout.tsx
- [X] T021 [US1] Add authentication state management in frontend/components/providers/auth-provider.tsx

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Task List and Creation (Priority: P2)

**Goal**: Allow authenticated users to view their task list and create new tasks

**Independent Test**: Authenticated user can see empty state, create tasks, and view them in the list

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T022 [P] [US2] Contract test for task CRUD endpoints in frontend/tests/contract/test-tasks.js
- [ ] T023 [P] [US2] Integration test for task creation flow in frontend/tests/integration/test-task-creation.js

### Implementation for User Story 2

- [X] T024 [P] [US2] Create tasks list page in frontend/app/(protected)/tasks/page.tsx
- [X] T025 [P] [US2] Create task list component in frontend/components/tasks/task-list.tsx
- [X] T026 [P] [US2] Create task card component in frontend/components/tasks/task-card.tsx
- [X] T027 [P] [US2] Create task form component in frontend/components/tasks/task-form.tsx
- [X] T028 [US2] Implement task creation API integration in frontend/lib/services/task-service.ts
- [X] T029 [US2] Implement task listing API integration in frontend/lib/services/task-service.ts
- [X] T030 [US2] Add loading and empty states for task list

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Task Details and Editing (Priority: P3)

**Goal**: Allow authenticated users to view task details, edit tasks, and toggle completion

**Independent Test**: Authenticated user can view task details, edit fields, save changes, and toggle completion status

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T031 [P] [US3] Integration test for task detail view in frontend/tests/integration/test-task-details.js
- [ ] T032 [P] [US3] Integration test for task editing flow in frontend/tests/integration/test-task-editing.js

### Implementation for User Story 3

- [X] T033 [P] [US3] Create task detail page in frontend/app/(protected)/tasks/[id]/page.tsx
- [X] T034 [P] [US3] Create task detail component in frontend/components/tasks/task-detail.tsx
- [X] T035 [P] [US3] Enhance task form for editing mode in frontend/components/tasks/task-form.tsx
- [X] T036 [US3] Implement task detail API integration in frontend/lib/services/task-service.ts
- [X] T037 [US3] Implement task update API integration in frontend/lib/services/task-service.ts
- [X] T038 [US3] Implement task completion toggle API integration in frontend/lib/services/task-service.ts
- [X] T039 [US3] Add error handling for task operations

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Task Deletion (Priority: P4)

**Goal**: Allow authenticated users to delete tasks with confirmation

**Independent Test**: Authenticated user can delete a task with proper confirmation and error handling

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [ ] T040 [P] [US4] Integration test for task deletion flow in frontend/tests/integration/test-task-deletion.js

### Implementation for User Story 4

- [X] T041 [P] [US4] Add delete button to task detail component in frontend/components/tasks/task-detail.tsx
- [X] T042 [P] [US4] Create confirmation modal component in frontend/components/ui/confirmation-modal.tsx
- [X] T043 [US4] Implement task deletion API integration in frontend/lib/services/task-service.ts
- [X] T044 [US4] Add confirmation flow for task deletion
- [X] T045 [US4] Add success/error messaging for deletion

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T046 [P] Add responsive design enhancements across all components
- [X] T047 [P] Add accessibility improvements (ARIA labels, keyboard navigation)
- [X] T048 [P] Add form validation using Zod based on data-model.md
- [X] T049 [P] Add error boundaries and global error handling
- [X] T050 [P] Add loading states and skeleton screens
- [X] T051 Add unit tests for components and services in frontend/tests/unit/
- [X] T052 Add E2E tests for critical user flows in frontend/tests/e2e/
- [X] T053 [P] Documentation updates in frontend/README.md
- [X] T054 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Depends on US1 for authentication
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Depends on US1 and US2 for auth and listing
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Depends on US1, US2, and US3 for auth, listing, and detail

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 2

```bash
# Launch all components for User Story 2 together:
Task: "Create tasks list page in frontend/app/(protected)/tasks/page.tsx"
Task: "Create task list component in frontend/components/tasks/task-list.tsx"
Task: "Create task card component in frontend/components/tasks/task-card.tsx"
Task: "Create task form component in frontend/components/tasks/task-form.tsx"
```

---

## Implementation Strategy

### MVP First (User Stories 1-2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Authentication)
4. Complete Phase 4: User Story 2 (Task List and Creation)
5. **STOP and VALIDATE**: Test User Stories 1 and 2 together
6. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo
3. Add User Story 2 → Test with US1 → Deploy/Demo (MVP!)
4. Add User Story 3 → Test with US1-2 → Deploy/Demo
5. Add User Story 4 → Test with US1-3 → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
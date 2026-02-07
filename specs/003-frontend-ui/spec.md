# Feature Specification: Responsive Next.js Frontend UI

**Feature Branch**: `003-frontend-ui`
**Created**: 2026-02-05
**Status**: Draft
**Input**: User description: "Todo Full-Stack Web Application — Spec 3: Responsive Next.js Frontend UI"

Target audience:
- Claude Code agents implementing the Next.js App Router frontend
- Reviewers evaluating responsiveness, UX completeness, and secure API integration

Focus:
- Next.js 16+ (App Router) responsive UI for multi-user task management
- Better Auth signup/signin flow and session handling
- Frontend API client integration with FastAPI:
  - Attach JWT to requests
  - Handle auth failures gracefully
- Full task workflows via UI:
  list → create → view → edit → complete toggle → delete

Success criteria:
- Users can signup/signin via Better Auth from the UI
- Authenticated users can:
  - View task list
  - Create a new task
  - Open task details
  - Edit/update a task
  - Toggle completion
  - Delete a task
- Frontend calls the required FastAPI endpoints and includes `Authorization: Bearer <JWT>`
- User isolation is preserved by design:
  - UI only operates on the authenticated user's `{user_id}`
  - Unauthorized states redirect or show clear sign-in prompts
- Responsive design:
  - Works on mobile and desktop
  - Layout adapts cleanly (no broken overflow, usable touch targets)
- UX quality:
  - Loading, empty, and error states are clear and consistent
  - Basic form validation is present (e.g., title required)

Constraints:
- Frontend: Next.js 16+ (App Router)
- Authentication: Better Auth (must align with Spec 1 token issuance + storage)
- Backend integration: consume FastAPI REST API from Spec 2
- No manual coding: implement via Spec → Plan → Tasks using Claude Code
- Keep UI scope focused on required features only (no extra advanced features)

Not building:
- Admin features, team/shared task lists, or task collaboration
- Advanced filtering/search, tags, reminders, notifications
- Offline-first mode or background sync
- Visual analytics, charts, or productivity dashboards
- Native mobile app (web-only)

## UI Definition (Professional + Responsive Requirements)

### Required Pages & Layout
- Public:
  - `/signin` (email/password form + link to signup)
  - `/signup` (email/password form + link to signin)
- Protected:
  - `/tasks` (task list + create form)
  - `/tasks/[id]` (task detail + edit/delete actions)

### Global UI Rules
- Consistent layout with:
  - Top header containing app name and user menu (logout)
  - Content container with max-width for desktop readability
- Typography and spacing must be consistent across pages
- Buttons and inputs must have visible focus states (keyboard accessible)

### Task List UI (`/tasks`)
- Default layout:
  - Mobile: single-column stacked cards
  - Desktop: two-column layout (left: list, right: create form) OR single-column with inline create
- Each task row/card shows:
  - Title (required)
  - Optional description preview (truncate)
  - Completion status indicator (checkbox or toggle)
  - Actions: View, Edit (optional direct), Delete
- Sorting:
  - Default: newest first (created_at desc) OR clearly documented alternative
- States:
  - Loading: skeleton or spinner + "Loading tasks…"
  - Empty: "No tasks yet. Create your first task."
  - Error: "Couldn't load tasks. Retry."

### Create Task UI
- Form fields:
  - Title (required, 1–255 chars)
  - Description (optional, up to 1000 chars) if backend supports it
- Validation:
  - Inline error under field
  - Disable submit while saving
- On success:
  - Form clears
  - Task list refreshes immediately

### Task Detail UI (`/tasks/[id]`)
- Displays:
  - Title, description, completed status, created/updated timestamps (optional)
- Actions:
  - Edit (inline edit mode or separate edit form section)
  - Toggle complete
  - Delete (with confirmation)

### Edit/Update Behavior
- Save action triggers PUT
- On success:
  - Show success feedback (toast or inline)
  - Update visible task data immediately

### Delete Behavior
- Requires confirmation modal/dialog:
  - "Delete this task?" / "Cancel" / "Delete"
- After delete:
  - Redirect to `/tasks`
  - List refreshes

### Auth Failure Handling
- If API returns 401:
  - Redirect to `/signin` and preserve return URL
- If 403:
  - Show "Access denied" and link back to `/tasks`

### Responsiveness & Breakpoints
- Must look correct on:
  - 360px width (small mobile)
  - 768px width (tablet)
  - 1024px+ (desktop)
- No horizontal scrolling on mobile
- Touch targets ≥ 44px height for primary buttons

### Accessibility Minimums
- All inputs have labels
- Buttons have accessible text
- Keyboard navigation works for forms and dialogs

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Registration and Authentication (Priority: P1)

A new user can sign up for an account and sign in to access their task management dashboard. The authentication flow integrates with Better Auth and securely manages user sessions.

**Why this priority**: This is the foundational functionality that enables users to access the task management features, forming the entry point for the entire application experience.

**Independent Test**: Can be fully tested by navigating to the signup page, registering a new account, verifying the account creation, then signing out and signing back in successfully.

**Acceptance Scenarios**:

1. **Given** a user navigates to `/signup`, **When** they enter valid email and password and submit the form, **Then** they are registered successfully and redirected to the task dashboard
2. **Given** a user navigates to `/signin`, **When** they enter valid credentials, **Then** they are authenticated and redirected to the task dashboard
3. **Given** a user enters invalid credentials, **When** they submit the form, **Then** they receive appropriate error feedback without being logged in
4. **Given** a user is logged in, **When** they visit the site later, **Then** their session is restored automatically

---

### User Story 2 - Task Management Dashboard (Priority: P1)

An authenticated user can view their tasks, create new tasks, and manage existing tasks through a responsive and intuitive interface that works across devices.

**Why this priority**: This is the core functionality of the application where users spend most of their time managing their tasks effectively.

**Independent Test**: Can be fully tested by authenticating a user, creating tasks via the UI, viewing the task list, and performing all management actions (edit, complete, delete).

**Acceptance Scenarios**:

1. **Given** an authenticated user visits `/tasks`, **When** tasks exist, **Then** they see a properly formatted list of their tasks
2. **Given** an authenticated user with no tasks, **When** they visit `/tasks`, **Then** they see the empty state with a clear path to create tasks
3. **Given** an authenticated user on the tasks page, **When** they create a new task, **Then** the task appears in the list immediately with success feedback
4. **Given** an authenticated user on mobile device, **When** they interact with task UI, **Then** the interface is fully responsive with appropriately sized touch targets

---

### User Story 3 - Task Detail Operations (Priority: P2)

An authenticated user can view detailed information about a specific task and perform all individual task operations with clear feedback and validation.

**Why this priority**: Provides users with detailed task management capabilities for in-depth interaction with specific tasks.

**Independent Test**: Can be fully tested by authenticating a user, navigating to a specific task, viewing details, editing, and performing all individual task operations.

**Acceptance Scenarios**:

1. **Given** an authenticated user clicks on a task, **When** they navigate to `/tasks/[id]`, **Then** they see detailed task information in a well-formatted view
2. **Given** an authenticated user on a task detail page, **When** they toggle completion, **Then** the change is saved and reflected immediately
3. **Given** an authenticated user attempts to delete a task, **When** they confirm deletion, **Then** the task is removed and they are redirected to the task list
4. **Given** an authenticated user attempts to edit a task, **When** they save changes, **Then** the task is updated with success feedback

---

### Edge Cases

- What happens when the API is temporarily unavailable during task operations?
- How does the UI handle JWT token expiration during an active session?
- What occurs when a user rapidly creates multiple tasks simultaneously?
- How does the application handle very long task titles or descriptions in the UI?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide signup page at `/signup` with email/password form and navigation to signin
- **FR-002**: System MUST provide signin page at `/signin` with email/password form and navigation to signup
- **FR-003**: System MUST integrate with Better Auth for user authentication and session management
- **FR-004**: System MUST provide task list page at `/tasks` for authenticated users with create form
- **FR-005**: System MUST provide task detail page at `/tasks/[id]` for viewing and editing individual tasks
- **FR-006**: System MUST call FastAPI backend endpoints with proper JWT authorization headers
- **FR-007**: System MUST handle 401/403 responses by redirecting to authentication or showing appropriate error
- **FR-008**: System MUST allow authenticated users to create tasks via UI form submission
- **FR-009**: System MUST allow authenticated users to view, edit, complete, and delete their tasks
- **FR-010**: System MUST implement proper loading, empty, and error states for all operations
- **FR-011**: System MUST provide responsive design that works on mobile, tablet, and desktop
- **FR-012**: System MUST include basic form validation for task creation and editing

### Key Entities *(include if feature involves data)*

- **User**: Authenticated user with session management via Better Auth
- **Task**: User's task entity with title, description, completion status, and timestamps

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of signup attempts with valid credentials result in successful account creation
- **SC-002**: 100% of signin attempts with valid credentials result in successful authentication
- **SC-003**: 100% of authenticated users can access their task dashboard after login
- **SC-004**: 100% of task operations (create, read, update, delete) work via the UI with proper API integration
- **SC-005**: 100% of UI states (loading, empty, error) are properly handled and displayed
- **SC-006**: 99.9% of responsive breakpoints display correctly across mobile, tablet, and desktop views
- **SC-007**: 100% of accessibility requirements are met with proper focus states and keyboard navigation
- **SC-008**: 100% of auth failure scenarios (401, 403) are handled gracefully with appropriate redirects

---

## Clarifications

### Session 2026-02-05

- Q: Should route protection be handled via Next.js middleware or per-page guard? → A: Next.js middleware for consistent protection across all protected routes
- Q: Should pages be server-rendered or client-rendered? → A: Server-rendered with client-side hydration for optimal performance and SEO
- Q: Should optimistic UI updates be used or full re-fetch after every action? → A: Full re-fetch after actions to ensure data consistency with the backend

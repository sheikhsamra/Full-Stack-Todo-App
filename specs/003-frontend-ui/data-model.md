# Data Model: Frontend State and Types for Task Management UI

## Entity Definitions

### User Entity (Frontend State)
Represents authenticated user information available on the frontend

| Property | Type | Constraints | Source | Description |
|----------|------|-------------|---------|-------------|
| id | string \| number | Required | Better Auth session | Unique identifier for the user |
| email | string | Required, valid email format | Better Auth session | User's email address |
| name | string | Optional | Better Auth session | User's display name |
| isAuthenticated | boolean | Required | Authentication state | Whether user is currently authenticated |
| isLoading | boolean | Required | Session provider | Whether session state is loading |

### Task Entity (Frontend Type)
Type definition for task objects used in the UI (matches backend Task model)

| Property | Type | Constraints | Default | Description |
|----------|------|-------------|---------|-------------|
| id | number | Required | Generated | Unique identifier for the task |
| user_id | number | Required | From session | ID of user who owns this task |
| title | string | Required, 1-255 chars | - | Task title/description |
| description | string | Optional, max 1000 chars | "" | Detailed description of the task |
| completed | boolean | Required | false | Completion status of the task |
| created_at | string (ISO date) | Required | Generated | Timestamp when task was created |
| updated_at | string (ISO date) | Required | Generated | Timestamp when task was last modified |

### Task Form Data (Frontend State)
Transient form data for task creation and editing

| Property | Type | Constraints | Required | Description |
|----------|------|-------------|----------|-------------|
| title | string | 1-255 chars | Yes | Task title |
| description | string | Max 1000 chars | No | Task description |
| completed | boolean | Boolean | No (false default) | Initial completion status |

### API Response Types
Standardized response formats from backend API

#### Success Response
| Property | Type | Description |
|----------|------|-------------|
| data | T | The requested data |
| success | boolean | Whether the request was successful |

#### Error Response
| Property | Type | Description |
|----------|------|-------------|
| error | string | Error message |
| details? | object | Additional error details |

## Frontend State Management

### Task List State
| Property | Type | Description |
|----------|------|-------------|
| tasks | Task[] | Array of user's tasks |
| isLoading | boolean | Whether tasks are being loaded |
| isError | boolean | Whether there was an error loading tasks |
| isEmpty | boolean | Whether the user has no tasks |

### Form State
| Property | Type | Description |
|----------|------|-------------|
| formData | TaskFormData | Current form input values |
| isSubmitting | boolean | Whether form is currently being submitted |
| errors | {[field: string]: string} | Field-specific error messages |
| successMessage | string | Success message after submission |

### UI State
| Property | Type | Description |
|----------|------|-------------|
| currentView | 'list' \| 'detail' \| 'edit' | Current UI view mode |
| selectedTaskId | number \| null | Currently selected task for detail/edit |
| showConfirmation | boolean | Whether confirmation modal is visible |
| confirmationAction | string \| null | Action to confirm (e.g., 'delete') |

## API Payload Shapes

### Create Task Request
```typescript
{
  title: string,
  description?: string,
  completed?: boolean
}
```

### Update Task Request
```typescript
{
  title?: string,
  description?: string,
  completed?: boolean
}
```

### API Response Formats

#### Single Task Response
```typescript
{
  id: number,
  user_id: number,
  title: string,
  description: string,
  completed: boolean,
  created_at: string,
  updated_at: string
}
```

#### Task List Response
```typescript
Task[]
```

## Validation Rules

### Task Title
- Required field
- Minimum 1 character
- Maximum 255 characters
- Cannot be only whitespace

### Task Description
- Optional field
- Maximum 1000 characters
- Can be empty string

### User ID Validation
- Must match authenticated user's ID
- Checked server-side in addition to frontend assumption

## State Transitions

### Task Creation Flow
1. Initial: Empty form with default values
2. User Input: Form populated with user input
3. Validation: Form validated for errors
4. Submission: API request in progress
5. Success: Task added to list, form cleared
6. Error: Error messages displayed

### Task Update Flow
1. Initial: Pre-populated with existing task data
2. User Input: Form updated with new values
3. Validation: Form validated for errors
4. Submission: API request in progress
5. Success: Task updated in list, return to view mode
6. Error: Error messages displayed

### Task Deletion Flow
1. Initial: Task detail view
2. Confirmation: Modal opened with confirmation request
3. Confirmation: User confirms deletion
4. Submission: API request in progress
5. Success: Task removed from list, redirect to task list
6. Cancel: Modal closed, return to view mode

## Frontend-Specific Considerations

### Session Management
- Use Better Auth React provider for session state
- Check authentication status in middleware for protected routes
- Redirect to signin with return URL if not authenticated
- Handle session expiry gracefully with error messages

### Error Handling
- Network errors: Display connection error messages
- Validation errors: Show field-specific error messages
- Authorization errors: Redirect to signin
- Server errors: Display generic error message with option to retry

### Loading States
- Initial loading: Show skeleton or spinner while data loads
- Form submission: Disable form and show loading indicator
- Background updates: Show subtle loading indicators for background operations
- Empty states: Clear message with action to create first item
# Data Model: Tasks REST API

## Entity Definitions

### Task Entity
Represents a user's task with title, description, completion status, and ownership information.

| Field | Type | Constraints | Default | Description |
|-------|------|-------------|---------|-------------|
| id | Integer | Primary Key, Auto-increment | Generated | Unique identifier for the task |
| user_id | Integer | Foreign Key Reference, Required | - | ID of the user who owns this task |
| title | String(255) | Required, Min length 1 | - | Task title/description |
| description | Text | Optional | "" | Detailed description of the task |
| completed | Boolean | Required | False | Completion status of the task |
| created_at | DateTime | Required | Current timestamp | Timestamp when task was created |
| updated_at | DateTime | Required | Current timestamp (updates on change) | Timestamp when task was last modified |

## Relationships
- **User-Task Relationship**: One-to-Many (One user can have many tasks)
- **Foreign Key Constraint**: `tasks.user_id` references `users.id` from authentication system

## Business Rules
1. **Ownership**: Every task must be associated with a valid user_id
2. **Title Requirement**: Every task must have a non-empty title
3. **User Isolation**: Tasks can only be accessed/modified by the owning user
4. **Completion Toggle**: The completed field can be flipped via the completion endpoint

## Indexes
- **Primary Index**: `id` (auto-created)
- **Foreign Key Index**: `user_id` (for efficient user-based queries)
- **Status Index**: `completed` (for efficient filtering by completion status)

## Validation Rules
1. **Title Length**: Must be between 1-255 characters
2. **Description Length**: Must be between 0-1000 characters
3. **User ID Validity**: Must correspond to an existing authenticated user
4. **Timestamp Integrity**: created_at and updated_at are managed automatically

## State Transitions
- **Creation**: New task starts with `completed = False`
- **Completion Toggle**: PATCH endpoint flips `completed` value
- **Update**: PUT endpoint updates title/description while preserving ownership
- **Deletion**: Task is removed entirely from database

## SQL Schema
```sql
CREATE TABLE tasks (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL,
  title VARCHAR(255) NOT NULL,
  description TEXT DEFAULT '',
  completed BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
```
from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlmodel import Session, select
from typing import List
from ...database import get_session
from ...models.task import Task, TaskCreate, TaskPublic, TaskUpdate
from ...api.deps import get_current_user_id, verify_user_owns_resource
from datetime import datetime, UTC

router = APIRouter()


@router.post("/", response_model=TaskPublic, status_code=status.HTTP_201_CREATED)
def create_task(
    *,
    db_session: Session = Depends(get_session),
    current_user_id: int = Depends(get_current_user_id),
    user_id: int = Path(..., title="The ID of the user to retrieve tasks for"),
    task: TaskCreate
):
    """
    Create a new task for the authenticated user.
    """
    # Verify that the current user matches the requested user ID in the URL
    verify_user_owns_resource(current_user_id, user_id)

    # Create the task with the user ID
    db_task = Task.model_validate(task, update={"user_id": user_id})

    db_session.add(db_task)
    db_session.commit()
    db_session.refresh(db_task)

    return db_task


@router.get("/", response_model=List[TaskPublic])
def read_tasks(
    *,
    db_session: Session = Depends(get_session),
    current_user_id: int = Depends(get_current_user_id),
    user_id: int = Path(..., title="The ID of the user to retrieve tasks for")
):
    """
    Retrieve tasks for the authenticated user.
    """
    # Verify that the current user matches the requested user ID in the URL
    verify_user_owns_resource(current_user_id, user_id)

    # Get tasks that belong to the user
    tasks = db_session.exec(select(Task).where(Task.user_id == user_id)).all()

    return tasks


@router.get("/{task_id}", response_model=TaskPublic)
def read_task(
    *,
    db_session: Session = Depends(get_session),
    current_user_id: int = Depends(get_current_user_id),
    user_id: int = Path(..., title="The ID of the user to retrieve task for"),
    task_id: int = Path(..., title="The ID of the task to retrieve")
):
    """
    Retrieve a specific task by ID.
    """
    # Verify that the current user matches the requested user ID in the URL
    verify_user_owns_resource(current_user_id, user_id)

    # Get the specific task that belongs to the user
    task = db_session.exec(
        select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.put("/{task_id}", response_model=TaskPublic)
def update_task(
    *,
    db_session: Session = Depends(get_session),
    current_user_id: int = Depends(get_current_user_id),
    user_id: int = Path(..., title="The ID of the user to update task for"),
    task_id: int = Path(..., title="The ID of the task to update"),
    task_update: TaskUpdate
):
    """
    Update a specific task by ID.
    """
    # Verify that the current user matches the requested user ID in the URL
    verify_user_owns_resource(current_user_id, user_id)

    # Get the specific task that belongs to the user
    db_task = db_session.exec(
        select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
    ).first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update the task with the provided values
    update_data = task_update.model_dump(exclude_unset=True)
    db_task.sqlmodel_update(update_data)
    db_task.updated_at = datetime.now(UTC)

    db_session.add(db_task)
    db_session.commit()
    db_session.refresh(db_task)

    return db_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    *,
    db_session: Session = Depends(get_session),
    current_user_id: int = Depends(get_current_user_id),
    user_id: int = Path(..., title="The ID of the user to delete task for"),
    task_id: int = Path(..., title="The ID of the task to delete")
):
    """
    Delete a specific task by ID.
    """
    # Verify that the current user matches the requested user ID in the URL
    verify_user_owns_resource(current_user_id, user_id)

    # Get the specific task that belongs to the user
    db_task = db_session.exec(
        select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
    ).first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Delete the task
    db_session.delete(db_task)
    db_session.commit()

    return


@router.patch("/{task_id}/complete", response_model=TaskPublic)
def toggle_task_completion(
    *,
    db_session: Session = Depends(get_session),
    current_user_id: int = Depends(get_current_user_id),
    user_id: int = Path(..., title="The ID of the user to toggle task completion for"),
    task_id: int = Path(..., title="The ID of the task to toggle completion for")
):
    """
    Toggle the completion status of a specific task by ID.
    """
    # Verify that the current user matches the requested user ID in the URL
    verify_user_owns_resource(current_user_id, user_id)

    # Get the specific task that belongs to the user
    db_task = db_session.exec(
        select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
    ).first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Toggle the completion status
    db_task.completed = not db_task.completed
    db_task.updated_at = datetime.now(UTC)

    db_session.add(db_task)
    db_session.commit()
    db_session.refresh(db_task)

    return db_task
from fastapi import FastAPI, Depends, HTTPException, status, Path
from fastapi.responses import JSONResponse
from typing import Dict, Any
from .auth_router import router as auth_router
from .deps import get_current_user, verify_user_access_dependency
from .error_handlers import register_error_handlers
from ..utils.auth_utils import verify_user_access
from ..config import settings


# Create FastAPI app instance
app = FastAPI(
    title="Todo App API",
    description="API for the Todo Full-Stack Web Application with authentication",
    version="1.0.0",
)

# Register error handlers
register_error_handlers(app)


@app.get("/")
def read_root():
    """
    Root endpoint for API health check.
    """
    return {"message": "Welcome to the Todo App API", "status": "active"}


@app.get("/health")
def health_check():
    """
    Health check endpoint to verify API is running.
    """
    return {"status": "healthy", "service": "todo-api"}


# Include the authentication router
app.include_router(auth_router, prefix="/api/auth")


# Example protected endpoints that follow the required API structure
@app.get("/api/{user_id}/tasks")
def get_tasks(
    user_id: str,
    current_user: Dict[str, Any] = Depends(verify_user_access_dependency)
):
    """
    Get all tasks for the specified user.

    This endpoint demonstrates user isolation - users can only access their own tasks.
    """
    # Verify that the user in the token matches the user_id in the URL
    verify_user_access(current_user["user_id"], user_id)

    # In a real implementation, this would query the database for the user's tasks
    return {
        "user_id": user_id,
        "tasks": []  # Return empty list for now - would contain user's tasks in real implementation
    }


@app.post("/api/{user_id}/tasks")
def create_task(
    user_id: str,
    task_data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(verify_user_access_dependency)
):
    """
    Create a new task for the specified user.

    This endpoint demonstrates user isolation - users can only create tasks for themselves.
    """
    # Verify that the user in the token matches the user_id in the URL
    verify_user_access(current_user["user_id"], user_id)

    # In a real implementation, this would create a task in the database
    return {
        "user_id": user_id,
        "task": task_data,
        "message": "Task created successfully"
    }


@app.get("/api/{user_id}/tasks/{id}")
def get_task(
    user_id: str,
    id: str = Path(..., description="The ID of the task to retrieve"),
    current_user: Dict[str, Any] = Depends(verify_user_access_dependency)
):
    """
    Get a specific task for the specified user.

    This endpoint demonstrates user isolation - users can only access their own tasks.
    """
    # Verify that the user in the token matches the user_id in the URL
    verify_user_access(current_user["user_id"], user_id)

    # In a real implementation, this would query the database for the specific task
    return {
        "user_id": user_id,
        "task_id": id,
        "task": {"id": id, "title": "Sample Task", "completed": False}
    }


@app.put("/api/{user_id}/tasks/{id}")
def update_task(
    user_id: str,
    id: str = Path(..., description="The ID of the task to update"),
    task_data: Dict[str, Any] = {},
    current_user: Dict[str, Any] = Depends(verify_user_access_dependency)
):
    """
    Update a specific task for the specified user.

    This endpoint demonstrates user isolation - users can only update their own tasks.
    """
    # Verify that the user in the token matches the user_id in the URL
    verify_user_access(current_user["user_id"], user_id)

    # In a real implementation, this would update the task in the database
    return {
        "user_id": user_id,
        "task_id": id,
        "updated_task": task_data,
        "message": "Task updated successfully"
    }


@app.delete("/api/{user_id}/tasks/{id}")
def delete_task(
    user_id: str,
    id: str = Path(..., description="The ID of the task to delete"),
    current_user: Dict[str, Any] = Depends(verify_user_access_dependency)
):
    """
    Delete a specific task for the specified user.

    This endpoint demonstrates user isolation - users can only delete their own tasks.
    """
    # Verify that the user in the token matches the user_id in the URL
    verify_user_access(current_user["user_id"], user_id)

    # In a real implementation, this would delete the task from the database
    return {
        "user_id": user_id,
        "task_id": id,
        "message": "Task deleted successfully"
    }


@app.patch("/api/{user_id}/tasks/{id}/complete")
def toggle_task_completion(
    user_id: str,
    id: str = Path(..., description="The ID of the task to toggle completion status"),
    current_user: Dict[str, Any] = Depends(verify_user_access_dependency)
):
    """
    Toggle the completion status of a specific task for the specified user.

    This endpoint demonstrates user isolation - users can only modify their own tasks.
    """
    # Verify that the user in the token matches the user_id in the URL
    verify_user_access(current_user["user_id"], user_id)

    # In a real implementation, this would toggle the completion status in the database
    return {
        "user_id": user_id,
        "task_id": id,
        "completed": True,  # In real implementation, this would toggle the status
        "message": "Task completion status updated"
    }


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """
    Global handler for HTTP exceptions.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """
    Global handler for general exceptions.
    """
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )
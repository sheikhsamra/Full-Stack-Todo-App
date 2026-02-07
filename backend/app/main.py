from fastapi import FastAPI
from .api.v1 import tasks
from .api.v1 import auth
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from sqlmodel import SQLModel
from .database import engine

load_dotenv()

def create_app():
    app = FastAPI(title="Tasks API", version="1.0.0")

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Create database tables on startup
    @app.on_event("startup")
    def on_startup():
        SQLModel.metadata.create_all(bind=engine)

    # Include the auth router for authentication endpoints
    app.include_router(auth.router, tags=["authentication"])

    # Include the tasks router with a placeholder for user_id - we'll handle it differently
    # Since we need to extract user_id from JWT and compare with URL, we handle it in the route
    # Create a dynamic router inclusion that captures the user_id from path
    app.include_router(tasks.router, prefix="/api/{user_id}", tags=["tasks"])

    @app.get("/")
    def read_root():
        return {"message": "Welcome to the Tasks API"}

    @app.get("/health")
    def health_check():
        return {"status": "healthy", "service": "tasks-api"}
    
    return app

app = create_app()
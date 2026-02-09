from fastapi import FastAPI, HTTPException
from .api.v1 import tasks
from .api.v1 import auth
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from sqlmodel import SQLModel
from .database import engine, get_session
from sqlmodel import select
from .models.user import User
from .models.task import Task

load_dotenv()

def create_app():
    app = FastAPI(
        title="Tasks API", 
        version="1.0.0",
        swagger_ui_parameters={"docExpansion": "list"},
        # Serve swagger assets locally to avoid network issues
        swagger_ui_oauth2_redirect_url=None
    )

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
        # Import all models to ensure they're registered with SQLModel.metadata
        from .models.user import User  # noqa: F401
        from .models.task import Task  # noqa: F401

        print(f"Connecting to database: {settings.database_url[:50]}...")  # Mask sensitive parts
        try:
            SQLModel.metadata.create_all(bind=engine)
            print("Database tables created successfully!")
        except Exception as e:
            print(f"Database connection error: {e}")
            import traceback
            traceback.print_exc()

    # Include the auth router for authentication endpoints
    app.include_router(auth.router, prefix="/api", tags=["authentication"])

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

    @app.get("/health/db")
    def db_health_check():
        """Health check endpoint to verify database connectivity."""
        try:
            # Use the engine directly for health check
            from sqlmodel import create_engine, Session
            with Session(engine) as session:
                # Run a lightweight query to test DB connectivity
                result = session.exec(select(1)).first()
                return {"ok": True, "message": "Database connection successful"}
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Database connection failed: {str(e)}")

    return app

app = create_app()
from .api.main import app  # Import the configured app from the api module


if __name__ == "__main__":
    import uvicorn
    from .db import create_db_and_tables

    # Create database tables on startup
    create_db_and_tables()

    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
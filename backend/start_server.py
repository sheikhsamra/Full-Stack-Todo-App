import uvicorn
from app.main import app

if __name__ == "__main__":
    print("Starting server on port 8000...")
    print("Make sure to check for any error messages when making requests.")
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8001, 
        log_level="info",
        reload=False
    )
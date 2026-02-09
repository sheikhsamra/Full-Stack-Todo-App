import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.main import app
import uvicorn

if __name__ == "__main__":
    print("Starting server...")
    try:
        uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
    except Exception as e:
        print(f"Error starting server: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
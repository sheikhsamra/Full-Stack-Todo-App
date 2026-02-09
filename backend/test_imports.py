import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

print("Testing imports...")
try:
    from app.models.user import User, UserCreate
    print("[OK] User models imported successfully")
    
    from app.database import engine
    print("[OK] Database engine created successfully")
    
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(bind=engine)
    print("[OK] Tables created successfully")
    
    from app.api.v1.auth import router
    print("[OK] Auth router imported successfully")
    
    from app.main import app
    print("[OK] Main app imported successfully")
    
    print("\nAll imports successful! The issue might be runtime-specific.")
    
except Exception as e:
    print(f"[ERROR] Import error: {e}")
    import traceback
    traceback.print_exc()
import sys
import traceback
import os

# Add the project root to sys.path to ensure imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    # Try importing from the legacy directory name first (as seen in file listing)
    from src.polyseek_sentient.main import app
except ImportError:
    try:
        # Fallback to new directory name if renamed
        from src.polyseek.main import app
    except Exception as e:
        # Create a minimal FastAPI app to show the error
        from fastapi import FastAPI
        from fastapi.responses import JSONResponse
        
        app = FastAPI()
        
        @app.get("/")
        @app.get("/api/health")
        @app.post("/assist")
        async def error_handler():
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Import failed",
                    "message": str(e),
                    "traceback": traceback.format_exc(),
                    "sys_path": sys.path,
                    "cwd": os.getcwd(),
                    "files": str(os.listdir(".")) if os.path.exists(".") else "N/A"
                }
            )

import sys
import traceback

try:
    from src.polyseek_sentient.main import app
    # Vercel requires the app to be available at the module level
    # For FastAPI, this is all we need.
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
                "sys_path": sys.path
            }
        )


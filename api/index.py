import sys
import traceback
import os
import importlib.util

# Add the project root and src to sys.path to ensure imports work
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)
sys.path.append(os.path.join(root_dir, "src"))

def check_dependency(name):
    try:
        importlib.import_module(name)
        return "OK"
    except ImportError as e:
        return f"Missing: {e}"
    except Exception as e:
        return f"Error: {e}"

# Diagnostic info
diagnostics = {
    "sys_path": sys.path,
    "cwd": os.getcwd(),
    "files_root": str(os.listdir(root_dir)) if os.path.exists(root_dir) else "N/A",
    "files_src": str(os.listdir(os.path.join(root_dir, "src"))) if os.path.exists(os.path.join(root_dir, "src")) else "N/A",
    "dep_fastapi": check_dependency("fastapi"),
    "dep_pydantic": check_dependency("pydantic"),
    "dep_sentient": check_dependency("sentient_agent_framework"),
}

try:
    # Try importing the main app
    # We use a specific try-block to catch errors during this specific import
    try:
        from src.polyseek_sentient.main import app as target_app
        app = target_app
    except ImportError:
        from src.polyseek.main import app as target_app
        app = target_app

except BaseException as e:
    # Fallback app for ANY error (ImportError, SyntaxError, SystemExit, etc.)
    from fastapi import FastAPI, Request
    from fastapi.responses import JSONResponse
    
    app = FastAPI()
    
    @app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD"])
    async def catch_all(request: Request, path_name: str):
        return JSONResponse(
            status_code=500,
            content={
                "error": "Critical Startup Error",
                "type": type(e).__name__,
                "message": str(e),
                "traceback": traceback.format_exc(),
                "diagnostics": diagnostics
            }
        )

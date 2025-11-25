from fastapi import FastAPI
from fastapi.responses import JSONResponse
import sys

app = FastAPI()

@app.get("/")
@app.get("/api/health")
async def health():
    return {"status": "ok", "message": "Minimal test endpoint working"}

@app.post("/assist")
async def assist():
    return JSONResponse(
        content={
            "status": "test",
            "message": "POST /assist endpoint reached",
            "python_version": sys.version
        },
        media_type="application/json"
    )

from datetime import datetime, timezone

from fastapi import FastAPI

from app.api.routes import router as api_router

app = FastAPI(title="ScriptBot API", version="0.2.0")
app.include_router(api_router)


@app.get("/health/live")
async def liveness() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/ready")
async def readiness() -> dict[str, str]:
    return {
        "status": "ready",
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
    }

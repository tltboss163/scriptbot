from datetime import datetime, timezone

from fastapi import FastAPI

app = FastAPI(title="ScriptBot API", version="0.1.0")


@app.get("/health/live")
async def liveness() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/ready")
async def readiness() -> dict[str, str]:
    return {
        "status": "ready",
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
    }

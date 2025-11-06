from fastapi import FastAPI

from app.api.routers import batch, classify, health, metrics, reload

app = FastAPI(title="Lead Classifier API", version="0.1.0")

app.include_router(health.router)
app.include_router(classify.router)
app.include_router(batch.router)
app.include_router(metrics.router)
app.include_router(reload.router)


@app.get("/", tags=["system"])
def read_root() -> dict[str, str]:
    """Return a simple welcome message."""
    return {"message": "Lead Classifier service is running"}

from datetime import datetime, timezone

from fastapi import APIRouter

router = APIRouter(tags=["system"])


@router.get("/health", summary="Application health status")
def health_check() -> dict[str, str]:
    """Return a basic health indicator."""
    return {"status": "ok", "timestamp": datetime.now(tz=timezone.utc).isoformat()}

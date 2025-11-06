from fastapi import APIRouter, status

router = APIRouter(tags=["system"])


@router.post("/reload", status_code=status.HTTP_202_ACCEPTED, summary="Reload model artifacts")
def reload_model() -> dict[str, str]:
    """Stub handler to simulate reloading model artifacts."""
    return {"status": "accepted", "detail": "Model reload scheduled"}

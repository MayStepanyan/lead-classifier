from fastapi import APIRouter, Response
from prometheus_client import CONTENT_TYPE_LATEST, CollectorRegistry, generate_latest

router = APIRouter(tags=["system"])


@router.get("/metrics", summary="Prometheus metrics endpoint")
def metrics(registry: CollectorRegistry | None = None) -> Response:
    """Expose Prometheus metrics using the default registry."""
    payload = generate_latest(registry) if registry else generate_latest()
    return Response(content=payload, media_type=CONTENT_TYPE_LATEST)

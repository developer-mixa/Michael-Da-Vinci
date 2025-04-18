from starlette.responses import Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from starlette.requests import Request

from .router import router

@router.get("/metrics")
async def metrics(
    request: Request,
) -> Response:
    return Response(generate_latest(), headers={'Content-Type': CONTENT_TYPE_LATEST})
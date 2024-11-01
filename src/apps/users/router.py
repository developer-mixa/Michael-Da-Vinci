from fastapi import APIRouter
from fastapi.responses import ORJSONResponse
from starlette.requests import Request
from starlette.responses import JSONResponse

router = APIRouter()

@router.get('/')
async def get_users() -> JSONResponse:
    print("session.execute(select(User))")
    return {"12": "12"}
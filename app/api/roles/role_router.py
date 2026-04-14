from fastapi import APIRouter
from . import role_api

router = APIRouter(
    prefix="/users",
)

router.include_router(
    role_api.router,
    tags=["users"]
)
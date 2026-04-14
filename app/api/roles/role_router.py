from fastapi import APIRouter
from . import role_api

router = APIRouter(
    prefix="/auth",
)

router.include_router(
    role_api.router,
    tags=["users"]
)
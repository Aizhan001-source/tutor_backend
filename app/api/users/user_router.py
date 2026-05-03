from fastapi import APIRouter
from . import user_api

router = APIRouter(
    prefix="/users",
)
router.include_router(
    user_api.router,
    tags=["users"]
)
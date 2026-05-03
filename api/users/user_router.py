from fastapi import APIRouter
from . import user_router

router = APIRouter(
    prefix="/users",
)
router.include_router(
    user_router.router,
    tags=["users"]
)
from fastapi import APIRouter
from . import count_router

router = APIRouter(
    prefix="/count",
)
router.include_router(
    count_router.router,
    tags=["count"], 
)
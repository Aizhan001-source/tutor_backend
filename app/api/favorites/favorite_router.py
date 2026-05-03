from fastapi import APIRouter
from . import favorite_api

router = APIRouter()

router = APIRouter(
    prefix="/favorites",
)

router.include_router(
    favorite_api.router,
    tags=["favorites"],
)



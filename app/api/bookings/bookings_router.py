from fastapi import APIRouter
from . import bookings_api

router = APIRouter(
    prefix="/bookings",
)

router.include_router(
    bookings_api.router,
    tags=["bookings"],
)
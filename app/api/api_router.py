from fastapi import APIRouter
from api.bookings.bookings_router import router as bookings_router

api_router = APIRouter()

api_router.include_router(
    bookings_router,
    prefix="/api",
)


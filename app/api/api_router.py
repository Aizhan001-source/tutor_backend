from fastapi import APIRouter

from api.bookings.booking_router import router as bookings_router
from api.users.user_router import router as users_router
from api.payments.payment_router import router as payments_router
from api.favorites.favorite_router import router as favorites_router
from api.tutors.tutor_router import router as tutors_router

api_router = APIRouter(prefix="/api")

api_router.include_router(
    bookings_router,
    tags=["bookings"]
    )

api_router.include_router(
    users_router, 
    tags=["users"]
    )

api_router.include_router(
    payments_router, 
    tags=["payments"]
    )

api_router.include_router(
    favorites_router, 
    tags=["favorites"]
    )

api_router.include_router(
    tutors_router, 
    tags=["tutors"]
    )
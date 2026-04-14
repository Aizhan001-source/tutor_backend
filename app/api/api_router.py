from fastapi import APIRouter

# Подключаем внутренние роутеры
from api.bookings.booking_router import router as bookings_router
from api.users.user_api import router as users_router
from api.payments.payment_router import router as payments_router
from api.roles.role_router import router as roles_router
from api.tutors.tutor_router import router as tutors_router
from api.messages.message_router import router as messages_router
from api.messages.message_api import router as messages_router
# Главный API-роутер с префиксом /api
api_router = APIRouter(prefix="/api")

# Включаем все роутеры
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
    roles_router, 
    tags=["roles"]
    )

api_router.include_router(
    tutors_router, 
    tags=["tutors"]
    )

# api_router.include_router(
#     messages_router, 
#     tags=["messages"]
#     )

api_router.include_router(messages_router)
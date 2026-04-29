from fastapi import APIRouter
from api.users.user_api import router as users_router
from api.tutors.tutor_api import router as tutor_router
from api.messages.message_api import router as message_router

api_router = APIRouter()

api_router.include_router(
    users_router,
    prefix="/users",
    tags=["USER"]
)

api_router.include_router(
    tutor_router,
    prefix="/tutors",
    tags=["TUTOR"]
)

api_router.include_router(
    message_router,
    prefix="/messages",
    tags=["MESSAGE"]
)
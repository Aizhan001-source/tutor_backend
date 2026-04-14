from fastapi import APIRouter
from . import tutor_api

router = APIRouter(
    prefix="/tutors",
)

router.include_router(
    tutor_api.router,
    tags=["tutors"],
)
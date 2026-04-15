from fastapi import APIRouter
from . import tutor_router

router = APIRouter(
    prefix="/tutors",
)
router.include_router(
    tutor_router.router,
    tags=["tutors"]
)
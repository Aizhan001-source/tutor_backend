from fastapi import APIRouter
from . import student_router

router = APIRouter(
    prefix="/students",
)
router.include_router(
    student_router.router,
    tags=["students"]
)
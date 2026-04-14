from fastapi import APIRouter
from . import subject_api

router = APIRouter(
    prefix="/subjects",
)

router.include_router(
    subject_api.router,
    tags=["subjects"]
)
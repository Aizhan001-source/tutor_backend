from fastapi import APIRouter
from . import application_router

router = APIRouter(
    prefix="/application",
)
router.include_router(
    application_router.router,
    tags=["application"],
)
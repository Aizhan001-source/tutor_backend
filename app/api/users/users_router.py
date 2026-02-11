from fastapi import APIRouter
from . import users_api

router = APIRouter(
    prefix="/users",
)

router.include_router(
    users_api.router,
    tags=["users"],
)
# from fastapi import APIRouter, Depends
# from app.core.dependencies import get_current_user

# router = APIRouter()

# @router.get("/me")
# def read_me(current_user: dict = Depends(get_current_user)):
#     return {"email": current_user.get("sub")}
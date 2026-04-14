from fastapi import APIRouter
from . import role_api

router = APIRouter(
    prefix="/auth",
)

router.include_router(
<<<<<<< HEAD:app/api/users/users_router.py
    users_api.router,
    tags=["AUTH"],
=======
    role_api.router,
    tags=["users"]
>>>>>>> origin/lili:app/api/roles/role_router.py
)
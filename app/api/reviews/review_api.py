from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from api.reviews.review_schemas import ReviewCreate, ReviewRead, ReviewUpdate



from utils.auth_middleware import get_current_user
from api.users.user_schemas import CurrentUser
from data_access.db.session import get_db



from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from data_access.db.session import get_db
from business_logic.reviews.review_service import ReviewService

from api.reviews.review_schemas import (
    ReviewCreate,
    ReviewRead,
    ReviewUpdate
)

from utils.auth_middleware import get_current_user
from api.users.user_schemas import CurrentUser


router = APIRouter(prefix="/reviews", tags=["reviews"])


def get_review_service(db: AsyncSession = Depends(get_db)) -> ReviewService:
    return ReviewService(db)


@router.post("/", response_model=ReviewRead, status_code=status.HTTP_201_CREATED)
async def create_review(
    data: ReviewCreate,
    current_user: CurrentUser = Depends(get_current_user),
    service: ReviewService = Depends(get_review_service),
):
    return await service.create_review(
        student_id=current_user.id,
        data=data
    )

@router.get("/tutor/{tutor_id}", response_model=list[ReviewRead])
async def get_reviews_by_tutor(
    tutor_id: UUID,
    service: ReviewService = Depends(get_review_service),
):
    return await service.get_by_tutor(tutor_id)

@router.get("/student/{student_id}", response_model=list[ReviewRead])
async def get_reviews_by_student(
    student_id: UUID,
    service: ReviewService = Depends(get_review_service),
):
    return await service.get_by_student(student_id)


@router.patch("/{review_id}", response_model=ReviewRead)
async def update_review(
    review_id: UUID,
    data: ReviewUpdate,
    current_user: CurrentUser = Depends(get_current_user),
    service: ReviewService = Depends(get_review_service),
):
    review = await service.get_by_id(review_id)

    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    if review.student_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    return await service.update(review, data)
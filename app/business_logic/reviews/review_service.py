from uuid import UUID
from fastapi import HTTPException

from data_access.reviews.review_repository import ReviewRepository
from data_access.bookings.booking_repository import BookingRepository
from api.reviews.review_schemas import ReviewCreate, ReviewUpdate


class ReviewService:
    def __init__(self, review_repo: ReviewRepository, booking_repo: BookingRepository):
        self.review_repo = review_repo
        self.booking_repo = booking_repo

    async def create_review(self, student_id: UUID, data: ReviewCreate):
        booking = await self.booking_repo.get_by_id(data.booking_id)

        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")

        if booking.student_id != student_id:
            raise HTTPException(status_code=403, detail="Forbidden")

        existing = await self.review_repo.get_by_booking(data.booking_id)
        if existing:
            raise HTTPException(status_code=409, detail="Review already exists")

        return await self.review_repo.create_review(
            student_id=student_id,
            tutor_id=booking.tutor_id,
            booking_id=data.booking_id,
            rating=data.rating,
            comment=data.comment
        )

    async def get_by_id(self, review_id: UUID):
        review = await self.review_repo.get_by_id(review_id)
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        return review

    async def get_by_tutor(self, tutor_id: UUID):
        return await self.review_repo.get_by_tutor(tutor_id)

    async def get_by_student(self, student_id: UUID):
        return await self.review_repo.get_by_student(student_id)

    async def update(self, review_id: UUID, student_id: UUID, data: ReviewUpdate):
        review = await self.review_repo.get_by_id(review_id)

        if not review:
            raise HTTPException(status_code=404, detail="Review not found")

        if review.student_id != student_id:
            raise HTTPException(status_code=403, detail="Forbidden")

        for field, value in data.dict(exclude_unset=True).items():
            setattr(review, field, value)

        return await self.review_repo.update(review)
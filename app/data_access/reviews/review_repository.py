from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from data_access.db.models.review import Review


class ReviewRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_review(
        self,
        student_id: UUID,
        tutor_id: UUID,
        booking_id: UUID,
        rating: int,
        comment: str,
    ) -> Review:

        review = Review(
            student_id=student_id,
            tutor_id=tutor_id,
            booking_id=booking_id,
            rating=rating,
            comment=comment,
        )

        self.db.add(review)
        await self.db.commit()
        await self.db.refresh(review)
        return review

    async def get_by_id(self, review_id: UUID):
        result = await self.db.execute(
            select(Review).where(Review.id == review_id)
        )
        return result.scalar_one_or_none()

    async def get_by_booking(self, booking_id: UUID):
        result = await self.db.execute(
            select(Review).where(Review.booking_id == booking_id)
        )
        return result.scalar_one_or_none()

    async def get_by_tutor(self, tutor_id: UUID):
        result = await self.db.execute(
            select(Review)
            .where(Review.tutor_id == tutor_id)
            .order_by(Review.created_at.desc())
        )
        return result.scalars().all()

    async def get_by_student(self, student_id: UUID):
        result = await self.db.execute(
            select(Review)
            .where(Review.student_id == student_id)
            .order_by(Review.created_at.desc())
        )
        return result.scalars().all()

    async def update(self, review: Review):
        self.db.add(review)
        await self.db.commit()
        await self.db.refresh(review)
        return review

    async def delete(self, review: Review):
        await self.db.delete(review)
        await self.db.commit()
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from data_access.db.models.bookings import Booking


class BookingsRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_booking(
        self,
        student_id: int,
        tutor_id: int,
        start_time,
        end_time,
        status,
    ):
        booking = Booking(
            student_id=student_id,
            tutor_id=tutor_id,
            start_time=start_time,
            end_time=end_time,
            status=status,
        )

        self.db.add(booking)
        await self.db.commit()
        await self.db.refresh(booking)

        return booking
    
    async def get_by_student(self, student_id: int):
        result = await self.db.execute(
            select(Booking).where(Booking.student_id == student_id)
        )
        return result.scalars().all()
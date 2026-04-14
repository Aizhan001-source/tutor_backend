from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from datetime import datetime

from data_access.db.models.bookings import Booking, BookingStatus
from typing import List, Optional

class BookingRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_booking(
        self, 
        student_id: UUID,
        tutor_id: UUID,
        start_time: datetime,
        end_time: datetime,
        status: BookingStatus
    ) -> Booking:
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

    async def get_by_id(self, booking_id: UUID) -> Optional[Booking]:
        result = await self.db.execute(
            select(Booking).where(Booking.id == booking_id)
        )
        return result.scalar_one_or_none()

    async def get_by_student(self, student_id: UUID) -> List[Booking]:
        result = await self.db.execute(
            select(Booking)
            .where(Booking.student_id == student_id)
            .order_by(Booking.start_time)
        )
        return result.scalars().all()

    async def get_by_tutor(self, tutor_id: UUID) -> List[Booking]:
        result = await self.db.execute(
            select(Booking)
            .where(Booking.tutor_id == tutor_id)
            .order_by(Booking.start_time)
        )
        return result.scalars().all()

    async def update(self, booking: Booking) -> Booking:
        self.db.add(booking)
        await self.db.commit()
        await self.db.refresh(booking)
        return booking

    async def delete(self, booking: Booking):
        await self.db.delete(booking)
        await self.db.commit()
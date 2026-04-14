from uuid import UUID
from datetime import datetime, timedelta

from fastapi import HTTPException

from data_access.bookings.booking_repository import BookingRepository
from data_access.db.models.booking import Booking
from data_access.db.models.booking import BookingStatus


class BookingService:
    def __init__(self, repo: BookingRepository):
        self.repo = repo

    async def create_booking(
        self,
        student_id: UUID,
        tutor_id: UUID,
        start_time: datetime,
        duration_hours: int = 1
    ):
        end_time = start_time + timedelta(hours=duration_hours)

        # ❗ проверка конфликта (если есть такая логика в repo)
        exists = await self.repo.get_by_time(
            tutor_id=tutor_id,
            start_time=start_time
        )

        if exists:
            raise HTTPException(
                status_code=400,
                detail="Time slot already booked"
            )

        booking = Booking(
            student_id=student_id,
            tutor_id=tutor_id,
            start_time=start_time,
            end_time=end_time,
            status=BookingStatus.PENDING
        )

        return await self.repo.create(booking)

    async def get_by_id(self, booking_id: UUID):
        booking = await self.repo.get_by_id(booking_id)

        if not booking:
            raise HTTPException(
                status_code=404,
                detail="Booking not found"
            )

        return booking

    async def get_by_student(self, student_id: UUID):
        return await self.repo.get_by_student(student_id)

    async def get_by_tutor(self, tutor_id: UUID):
        return await self.repo.get_by_tutor(tutor_id)

    async def cancel_booking(self, booking_id: UUID, user_id: UUID):
        booking = await self.repo.get_by_id(booking_id)

        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")

        if booking.student_id != user_id:
            raise HTTPException(status_code=403, detail="Forbidden")

        booking.status = BookingStatus.CANCELLED

        return await self.repo.update(booking)
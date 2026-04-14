from data_access.bookings.booking_repository import BookingRepository
from api.bookings.booking_schemas import BookingCreate
from uuid import UUID

class BookingService:
    def __init__(self, repo: BookingRepository):
        self.repo = repo

    async def create_booking(self, student_id: UUID, data: BookingCreate):
        return await self.repo.create_booking(
            student_id=student_id,
            tutor_id=data.tutor_id,
            start_time=data.start_time,
            end_time=data.end_time,
            status=data.status
        )

    async def get_bookings_by_student(self, student_id: UUID):
        return await self.repo.get_by_student(student_id)

    async def get_by_id(self, booking_id: UUID):
        return await self.repo.get_by_id(booking_id)
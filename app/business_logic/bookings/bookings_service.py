from api.bookings.bookings_schemas import BookingCreate, BookingRead
from data_access.bookings.bookings_repository import BookingsRepository
from data_access.db.models.bookings import BookingStatus


class BookingsService:

    def __init__(self, repo: BookingsRepository):
        self.repo = repo


    async def create_booking(self, student_id: int, data: BookingCreate):
        return await self.repo.create_booking(
            student_id=student_id,
            tutor_id=data.tutor_id,
            start_time=data.start_time,
            end_time=data.end_time,
            status=BookingStatus.pending,
        )
    
    async def get_bookings_by_student(self, student_id: int):
        return await self.repo.get_by_student(student_id)
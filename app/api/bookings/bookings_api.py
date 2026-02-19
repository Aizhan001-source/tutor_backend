from fastapi import APIRouter, Depends, HTTPExeption
from sqlalchemy.ext.asyncio import AsyncSession

from api.bookings.bookings_schemas import (
    BookingCreate,
    BookingRead
)
from data_access.db.session import get_db
from data_access.bookings.bookings_repository import BookingsRepository
from business_logic.bookings.bookings_service import BookingsService

router = APIRouter()

def get_bookings_service(
        db: AsyncSession = Depends(get_db),
) -> BookingsService:
    repo = BookingsRepository(db)
    return BookingsService(repo)

@router.get("/me", response_model=list[BookingRead])
async def get_my_bookings(
    service: BookingsService = Depends(get_bookings_service),
):
    return await service.get_bookings_by_student(student_id=1)

@router.post("/", response_model=BookingRead)
async def create_booking(
    booking: BookingCreate,
    service: BookingsService = Depends(get_bookings_service),
):
    try:
        return await service.create_booking(student_id=1, data=booking)
    except ValueError as e:
        raise HTTPExeption(status_code=400, detail=str(e))
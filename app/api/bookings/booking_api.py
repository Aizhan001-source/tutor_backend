from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from api.bookings.booking_schemas import BookingRead, BookingCreate, BookingUpdate
from data_access.bookings.booking_repository import BookingRepository
from business_logic.bookings.booking_service import BookingService
from utils.auth_middleware import get_current_user
from api.users.user_schemas import CurrentUser
from data_access.db.session import get_db

router = APIRouter()


def get_booking_service(db: AsyncSession = Depends(get_db)) -> BookingService:
    return BookingService(BookingRepository(db))


@router.get("/me", response_model=list[BookingRead])
async def get_my_bookings(
    current_user: CurrentUser = Depends(get_current_user),
    service: BookingService = Depends(get_booking_service),
):
    if current_user.role != "student":
        raise HTTPException(403, "Only students")
    return await service.get_bookings_by_student(current_user.id)


@router.post("/", response_model=BookingRead)
async def create_booking(
    booking: BookingCreate,
    current_user: CurrentUser = Depends(get_current_user),
    service: BookingService = Depends(get_booking_service),
):
    return await service.create_booking(current_user.id, booking)


@router.get("/{booking_id}", response_model=BookingRead)
async def get_booking(
    booking_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    service: BookingService = Depends(get_booking_service),
):
    return await service.get_by_id(booking_id)


@router.patch("/{booking_id}/cancel")
async def cancel_booking(
    booking_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    service: BookingService = Depends(get_booking_service),
):
    return await service.cancel_booking(booking_id, current_user.id)
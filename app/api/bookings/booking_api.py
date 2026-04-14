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


def get_booking_service(db: AsyncSession = Depends(get_db),) -> BookingService:
    repo = BookingRepository(db)
    return BookingService(repo)


@router.get("/me", operation_id="get_my_bookings_me")
async def get_my_bookings_user(
    current_user: CurrentUser = Depends(get_current_user),
    service: BookingService = Depends(get_booking_service),
):
    # Только студент может смотреть свои бронирования
    if current_user.role != "student":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can view their bookings"
        )
    return await service.get_bookings_by_student(student_id=current_user.id)


@router.post("/", response_model=BookingRead)
async def create_booking(
    booking: BookingCreate,
    current_user: CurrentUser = Depends(get_current_user(required_roles=["student"])),
    service: BookingService = Depends(get_booking_service),
):
    return await service.create_booking(student_id=current_user.id, data=booking)


@router.get("/{booking_id}", response_model=BookingRead)
async def get_booking(
    booking_id: UUID,
    current_user: CurrentUser = Depends(get_current_user(required_roles=["student", "tutor"])),
    service: BookingService = Depends(get_booking_service)
):
    return await service.get_booking_with_access_check(
        booking_id=booking_id,
        user_id=current_user.id,
        role=current_user.role
    )


@router.patch("/{booking_id}", response_model=BookingRead)
async def update_booking(
    booking_id: UUID,
    booking_data: BookingUpdate,
    service: BookingService = Depends(get_booking_service),
    current_user: CurrentUser = Depends(get_current_user),
):
    updated_booking = await service.update_booking(
        booking_id=booking_id,
        user_id=current_user.id,
        role=current_user.role,
        data=booking_data
    )
    
    if not updated_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    return updated_booking


@router.get("/me", response_model=list[BookingRead])
async def get_my_bookings(
    current_user: CurrentUser = Depends(get_current_user(required_roles=["student"])),
    service: BookingService = Depends(get_booking_service),
):
    return await service.get_bookings_by_student(current_user.id)


@router.patch("/{booking_id}/cancel", response_model=BookingRead)
async def cancel_booking(
    booking_id: UUID,
    current_user: CurrentUser = Depends(get_current_user(required_roles=["student"])),
    service: BookingService = Depends(get_booking_service),
):
    return await service.cancel_booking_with_access_check(
        booking_id=booking_id,
        user_id=current_user.id,
        role=current_user.role
    )

@router.patch("/{booking_id}/confirm", response_model=BookingRead)
async def confirm_booking(
    booking_id: UUID,
    current_user: CurrentUser = Depends(get_current_user(required_roles=["tutor"])),
    service: BookingService = Depends(get_booking_service),
):
    return await service.confirm_booking_with_access_check(
        booking_id=booking_id,
        user_id=current_user.id,
        role=current_user.role
    )
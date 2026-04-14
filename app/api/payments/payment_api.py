from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from data_access.db.session import get_db
from data_access.payments.payment_repository import PaymentRepository
from data_access.bookings.booking_repository import BookingRepository
from business_logic.payments.payment_service import PaymentService
from utils.auth_middleware import get_current_user
from api.users.user_schemas import CurrentUser
from api.payments.payment_schemas import PaymentRead, PaymentCreate


router = APIRouter()


def get_payment_service(db: AsyncSession = Depends(get_db)) -> PaymentService:
    return PaymentService(
        PaymentRepository(db),
        BookingRepository(db)
    )


@router.post("/", response_model=PaymentRead)
async def create_payment(
    data: PaymentCreate,
    service: PaymentService = Depends(get_payment_service),
    user: CurrentUser = Depends(get_current_user),
):
    return await service.create(data, user.id)


@router.get("/", response_model=list[PaymentRead])
async def my_payments(
    service: PaymentService = Depends(get_payment_service),
    user: CurrentUser = Depends(get_current_user),
):
    return await service.get_by_user(user.id)


@router.get("/{payment_id}", response_model=PaymentRead)
async def get_payment(
    payment_id: UUID,
    service: PaymentService = Depends(get_payment_service),
    user: CurrentUser = Depends(get_current_user),
):
    payment = await service.get_by_id(payment_id)

    if not payment:
        raise HTTPException(status_code=404, detail="Not found")

    if payment.booking.student_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    return payment
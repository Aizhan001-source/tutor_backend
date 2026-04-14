from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from data_access.db.session import get_db
from data_access.payments.payment_repository import PaymentRepository
from business_logic.payments.payment_service import PaymentService
from utils.auth_middleware import get_current_user
from api.users.user_schemas import CurrentUser
from api.payments.payment_schemas import PaymentRead, PaymentCreate


router = APIRouter()

# Dependency: получаем сервис платежей
def get_payment_service(db: AsyncSession = Depends(get_db)) -> PaymentService:
    repo = PaymentRepository(db)
    return PaymentService(repo)

# Создание платежа
@router.post(
    "/",
    response_model=PaymentRead,
    status_code=status.HTTP_201_CREATED
)
async def create_payment(
    data: PaymentCreate,
    service: PaymentService = Depends(get_payment_service),
    user: CurrentUser = Depends(get_current_user)
):
    try:
        return await service.create(data, user.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Получить все платежи текущего пользователя
@router.get(
    "/",
    response_model=list[PaymentRead]
)
async def get_my_payments(
    service: PaymentService = Depends(get_payment_service),
    user: CurrentUser = Depends(get_current_user)
):
    return await service.get_by_user(user.id)

# Получить платеж по ID
@router.get(
    "/{payment_id}",
    response_model=PaymentRead
)
async def get_payment(
    payment_id: UUID,
    service: PaymentService = Depends(get_payment_service),
    user: CurrentUser = Depends(get_current_user)
):
    payment = await service.get_by_id(payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    if payment.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    return payment
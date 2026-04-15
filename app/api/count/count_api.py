from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from data_access.db.session import get_db
from data_access.count.admin_stats_repository import AdminStatsRepository
from business_logic.count.admin_stats_service import AdminStatsService

from api.count.admin_stats_schemas import AdminStatsSummary

from utils.auth_middleware import get_current_user


router = APIRouter()


# =========================
# 🔧 DEPENDENCY INJECTION
# =========================
def get_stats_service(
    db: AsyncSession = Depends(get_db),
) -> AdminStatsService:
    repo = AdminStatsRepository(db)
    return AdminStatsService(repo)


# =========================
# 📊 SUMMARY STATS
# =========================
@router.get("/summary", response_model=AdminStatsSummary)
async def get_admin_stats_summary(
    service: AdminStatsService = Depends(get_stats_service),
    user=Depends(get_current_user(required_roles=["admin"])),
):
    return await service.get_summary()
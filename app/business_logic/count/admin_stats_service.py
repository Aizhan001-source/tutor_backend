from data_access.count.admin_stats_repository import AdminStatsRepository
from api.count.admin_stats_schemas import AdminStatsSummary


class AdminStatsService:
    def __init__(self, repo: AdminStatsRepository):
        self.repo = repo

    async def get_summary(self) -> AdminStatsSummary:
        students_count = await self.repo.count_students()
        tutors_count = await self.repo.count_tutors()
        active_sessions = await self.repo.count_active_sessions()
        revenue_mtd = await self.repo.revenue_mtd()

        return AdminStatsSummary(
            students=students_count,
            tutors=tutors_count,
            active_sessions=active_sessions,
            revenue_mtd=float(revenue_mtd or 0),
        )
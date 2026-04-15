from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from data_access.application.application_repository import TutorApplicationRepository

from api.application.application_schemas import (
    TutorApplicationRead,
    TutorApplicationListResponse,
    TutorApplicationQueryParams,
    TutorApplicationReviewRequest,
    TutorApplicationReviewResponse,
    TutorApplicationUserRead,
)

class TutorApplicationService:
    def __init__(self, db: AsyncSession):
        self.repo = TutorApplicationRepository(db)

    # -------------------------
    # LIST APPLICATIONS
    # -------------------------
    async def get_applications(self, params: TutorApplicationQueryParams):

        applications, total = await self.repo.get_applications(
            page=params.page,
            page_size=params.page_size,
            status=params.status,
            search=params.search,
        )

        items = []

        for app in applications:

            items.append(
                TutorApplicationRead(
                    id=app.id,
                    user_id=app.user_id,
                    status=app.status,
                    created_at=app.created_at,
                    reviewed_by=app.reviewed_by,
                    reviewed_at=app.reviewed_at,

                    user=TutorApplicationUserRead(
                        id=app.user.id,
                        first_name=app.user.first_name,
                        last_name=app.user.last_name,
                        email=app.user.email,
                    ) if app.user else None,
                )
            )

        return TutorApplicationListResponse(
            items=items,
            total=total,
            page=params.page,
            page_size=params.page_size,
        )

    # -------------------------
    # GET BY ID
    # -------------------------
    async def get_application(self, application_id: UUID):

        app = await self.repo.get_by_id(application_id)

        if not app:
            raise HTTPException(status_code=404, detail="Application not found")

        return TutorApplicationRead(
            id=app.id,
            user_id=app.user_id,
            status=app.status,
            created_at=app.created_at,
            reviewed_by=app.reviewed_by,
            reviewed_at=app.reviewed_at,

            user=TutorApplicationUserRead(
                id=app.user.id,
                first_name=app.user.first_name,
                last_name=app.user.last_name,
                email=app.user.email,
            ) if app.user else None,
        )

    # -------------------------
    # APPROVE / REJECT
    # -------------------------
    async def review_application(
        self,
        application_id: UUID,
        data: TutorApplicationReviewRequest,
        reviewer_id: UUID,
    ):

        app = await self.repo.update_status(
            application_id=application_id,
            status=data.status,
            reviewer_id=reviewer_id,
        )

        if not app:
            raise HTTPException(status_code=404, detail="Application not found")

        return TutorApplicationReviewResponse(
            id=app.id,
            status=app.status,
            reviewed_by=app.reviewed_by,
            reviewed_at=app.reviewed_at,
            message=f"Application {app.status}",
        )
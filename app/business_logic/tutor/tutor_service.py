from data_access.tutor.tutor_repository import AdminTutorRepository

from api.tutor.tutor_schemas import (
    TutorListResponse,
    TutorUserRead,
    TutorDetailResponse,
    TutorUserUpdate,
    TutorProfileUpdate,
    TutorDeleteResponse,
)


class AdminTutorService:
    def __init__(self, repo: AdminTutorRepository):
        self.repo = repo

    async def get_tutors(
        self,
        page: int,
        page_size: int,
        search: str | None = None,
        is_verified: bool | None = None,
    ) -> TutorListResponse:

        tutors, total = await self.repo.get_tutors(
            page=page,
            page_size=page_size,
            search=search,
            is_verified=is_verified,
        )

        return TutorListResponse(
            items=[TutorUserRead.model_validate(t) for t in tutors],
            total=total,
            page=page,
            page_size=page_size,
        )
    async def get_tutor_by_id(self, user_id) -> TutorDetailResponse | None:

        tutor = await self.repo.get_tutor_by_id(user_id)

        if not tutor:
            return None

        return TutorDetailResponse.model_validate(tutor)
    
    async def update_user(self, user, data: TutorUserUpdate):
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(user, key, value)

        updated = await self.repo.update_user(user)

        return TutorUserRead.model_validate(updated)
    
    async def update_profile(self, profile, data: TutorProfileUpdate):
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(profile, key, value)

        updated = await self.repo.update_profile(profile)

        return updated
    
    async def delete_tutor(self, user) -> TutorDeleteResponse:

        await self.repo.delete_user(user)

        return TutorDeleteResponse(
            success=True,
            message="Tutor deleted successfully",
            deleted_user_id=user.id,
        )
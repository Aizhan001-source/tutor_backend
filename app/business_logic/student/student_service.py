from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from data_access.students.student_repository import StudentRepository

from api.students.student_schemas import (
    StudentListResponse,
    StudentUserRead,
    StudentDetailResponse,
    StudentUserUpdate,
    StudentProfileUpdate,
    StudentQueryParams,
    StudentDeleteResponse,
    RoleRead,
    StudentProfileRead,
)


class StudentService:
    def __init__(self, db: AsyncSession):
        self.repo = StudentRepository(db)

    # -------------------------
    # LIST STUDENTS
    # -------------------------
    async def get_students(self, params: StudentQueryParams):
        students, total = await self.repo.get_students(
            page=params.page,
            page_size=params.page_size,
            search=params.search,
        )

        items = []

        for student in students:

            items.append(
                StudentUserRead(
                    id=student.id,
                    first_name=student.first_name,
                    last_name=student.last_name,
                    email=student.email,
                    avatar_url=student.avatar_url,

                    role=RoleRead(
                        id=student.role.id,
                        name=student.role.name
                    ) if student.role else None,

                    student_profile=StudentProfileRead(
                        id=student.student_profile.id,
                        user_id=student.student_profile.user_id,
                        level=student.student_profile.level,
                        learning_goals=student.student_profile.learning_goals,
                        bio=student.student_profile.bio,
                        timezone=student.student_profile.timezone,
                        preferred_language=student.student_profile.preferred_language,
                        total_sessions=student.student_profile.total_sessions,
                        completed_sessions=student.student_profile.completed_sessions,
                        total_spent_hours=student.student_profile.total_spent_hours,
                        last_session_at=student.student_profile.last_session_at,
                    ) if student.student_profile else None,
                )
            )

        return StudentListResponse(
            items=items,
            total=total,
            page=params.page,
            page_size=params.page_size,
        )

    # -------------------------
    # DETAIL STUDENT
    # -------------------------
    async def get_student_detail(self, user_id: UUID):

        student = await self.repo.get_student_by_id(user_id)

        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        return StudentDetailResponse(
            id=student.id,
            first_name=student.first_name,
            last_name=student.last_name,
            email=student.email,
            avatar_url=student.avatar_url,

            role=RoleRead(
                id=student.role.id,
                name=student.role.name
            ) if student.role else None,

            student_profile=StudentProfileRead(
                id=student.student_profile.id,
                user_id=student.student_profile.user_id,
                level=student.student_profile.level,
                learning_goals=student.student_profile.learning_goals,
                bio=student.student_profile.bio,
                timezone=student.student_profile.timezone,
                preferred_language=student.student_profile.preferred_language,
                total_sessions=student.student_profile.total_sessions,
                completed_sessions=student.student_profile.completed_sessions,
                total_spent_hours=student.student_profile.total_spent_hours,
                last_session_at=student.student_profile.last_session_at,
            ) if student.student_profile else None,
        )

    # -------------------------
    # UPDATE USER
    # -------------------------
    async def update_student_user(self, user_id: UUID, data: StudentUserUpdate):

        update_data = data.model_dump(exclude_unset=True)

        updated_user = await self.repo.update_user(user_id, update_data)

        if not updated_user:
            raise HTTPException(status_code=404, detail="Student not found")

        return StudentUserRead(
            id=updated_user.id,
            first_name=updated_user.first_name,
            last_name=updated_user.last_name,
            email=updated_user.email,
            avatar_url=updated_user.avatar_url,

            role=RoleRead(
                id=updated_user.role.id,
                name=updated_user.role.name
            ) if updated_user.role else None,

            student_profile=None  # не трогаем профиль тут
        )

    # -------------------------
    # UPDATE PROFILE
    # -------------------------
    async def update_student_profile(self, user_id: UUID, data: StudentProfileUpdate):

        update_data = data.model_dump(exclude_unset=True)

        profile = await self.repo.update_profile(user_id, update_data)

        if not profile:
            raise HTTPException(status_code=404, detail="Student profile not found")

        student = await self.repo.get_student_by_id(user_id)

        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        return StudentDetailResponse(
            id=student.id,
            first_name=student.first_name,
            last_name=student.last_name,
            email=student.email,
            avatar_url=student.avatar_url,

            role=RoleRead(
                id=student.role.id,
                name=student.role.name
            ) if student.role else None,

            student_profile=StudentProfileRead(
                id=student.student_profile.id,
                user_id=student.student_profile.user_id,
                level=student.student_profile.level,
                learning_goals=student.student_profile.learning_goals,
                bio=student.student_profile.bio,
                timezone=student.student_profile.timezone,
                preferred_language=student.student_profile.preferred_language,
                total_sessions=student.student_profile.total_sessions,
                completed_sessions=student.student_profile.completed_sessions,
                total_spent_hours=student.student_profile.total_spent_hours,
                last_session_at=student.student_profile.last_session_at,
            ) if student.student_profile else None,
        )

    # -------------------------
    # DELETE STUDENT
    # -------------------------
    async def delete_student(self, user_id: UUID):

        deleted = await self.repo.delete_student(user_id)

        if not deleted:
            raise HTTPException(status_code=404, detail="Student not found")

        return StudentDeleteResponse(
            success=True,
            message="Student deleted successfully",
            deleted_user_id=user_id,
        )
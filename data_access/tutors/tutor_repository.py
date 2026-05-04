# from typing import List
# from sqlalchemy import UUID, select, func
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.orm import selectinload

# from data_access.db.models.tutor import Tutor


# class TutorRepository:
#     def __init__(self, db: AsyncSession):
#         self.db = db

#     async def get_all_tutors(self) -> List [Tutor]:
#         result = await self.db.execute(
#             select(Tutor).options(
#                 selectinload(Tutor.education),
#                 selectinload(Tutor.user),
#             )
#         )
#         return result.scalars().all()
    
    
#     async def get_tutor_by_id(self, tutor_id:UUID):
#         result = await self.db.execute(
#             select(Tutor).where(Tutor.id == tutor_id)
#             .options(selectinload(Tutor.user))
#             .options(selectinload(Tutor.education))
#         )
#         return result.scalar_one_or_none()
    
#     async def get_tutors_count(self) -> int:
#         result = await self.db.execute(
#             select(func.count(Tutor.id))
#         )
#         return result.scalar_one()

from typing import List
from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from data_access.db.models.tutor import Tutor


class TutorRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    def _with_relations(self, stmt):
        return stmt.options(
            selectinload(Tutor.education),
            selectinload(Tutor.user),
        )

    async def get_all_tutors(self) -> List[Tutor]:
        result = await self.db.execute(
            self._with_relations(select(Tutor))
        )
        return result.scalars().all()

    async def get_tutor_by_id(self, tutor_id: UUID) -> Tutor | None:
        result = await self.db.execute(
            self._with_relations(select(Tutor).where(Tutor.id == tutor_id))
        )
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: UUID) -> Tutor | None:
        result = await self.db.execute(
            self._with_relations(select(Tutor).where(Tutor.user_id == user_id))
        )
        return result.scalar_one_or_none()

    async def get_tutors_count(self) -> int:
        result = await self.db.execute(select(func.count(Tutor.id)))
        return result.scalar_one()
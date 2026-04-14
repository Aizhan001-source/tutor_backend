from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.data_access.db.session import get_db
from data_access.db.models.subject import Subject
from app.api.subjects.subject_schemas import SubjectCreate, SubjectResponse

router = APIRouter(prefix="/subjects", tags=["Subjects"])


@router.post("/", response_model=SubjectResponse)
async def create_subject(
    data: SubjectCreate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Subject).where(Subject.name == data.name)
    )
    exists = result.scalar_one_or_none()

    if exists:
        raise HTTPException(status_code=400, detail="Subject already exists")

    subject = Subject(name=data.name)
    db.add(subject)
    await db.commit()
    await db.refresh(subject)
    return subject


@router.get("/", response_model=list[SubjectResponse])
async def get_subjects(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Subject))
    return result.scalars().all()


@router.get("/{subject_id}", response_model=SubjectResponse)
async def get_subject(subject_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Subject).where(Subject.id == subject_id)
    )
    subject = result.scalar_one_or_none()

    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    return subject


@router.delete("/{subject_id}")
async def delete_subject(subject_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Subject).where(Subject.id == subject_id)
    )
    subject = result.scalar_one_or_none()

    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    await db.delete(subject)
    await db.commit()

    return {"message": "Deleted successfully"}
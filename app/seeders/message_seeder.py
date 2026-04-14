from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from data_access.db.models.message import Message
from data_access.db.models.user import User


async def seed_messages(db: AsyncSession):

    students = (await db.execute(
        select(User).where(User.role.has(name="student"))
    )).scalars().all()

    tutors = (await db.execute(
        select(User).where(User.role.has(name="tutor"))
    )).scalars().all()

    messages = [
        "Hello!",
        "I need help with math",
        "When are you available?",
        "Tomorrow works"
    ]

    for i, student in enumerate(students):
        tutor = tutors[i % len(tutors)]

        for j, text in enumerate(messages):

            sender = student if j % 2 == 0 else tutor
            receiver = tutor if j % 2 == 0 else student

            exists = await db.execute(
                select(Message).where(
                    Message.sender_id == sender.id,
                    Message.receiver_id == receiver.id,
                    Message.content == text
                )
            )

            if exists.scalar_one_or_none():
                continue

            db.add(Message(
                sender_id=sender.id,
                receiver_id=receiver.id,
                content=text,
                created_at=datetime.utcnow()
            ))

    await db.commit()
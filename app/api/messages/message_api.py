# from fastapi import APIRouter, Depends, status
# from sqlalchemy.ext.asyncio import AsyncSession
# from uuid import UUID

# from api.messages.message_schemas import MessageCreate, MessageRead, ChatPreview, UnreadCountResponse
# from api.messages.message_router import router
# from data_access.messages.message_repository import MessageRepository
# from business_logic.messages.message_service import MessageService
# from utils.auth_middleware import get_current_user
# from data_access.db.session import get_db


# def get_message_service(db: AsyncSession = Depends(get_db)) -> MessageService:
#     return MessageService(MessageRepository(db))


# @router.post("/", response_model=MessageRead, status_code=status.HTTP_201_CREATED)
# async def send_message(
#     data: MessageCreate,
#     current_user=Depends(get_current_user()),
#     service: MessageService = Depends(get_message_service),
# ):
#     """Отправить сообщение"""
#     return await service.send_message(sender_id=current_user["user_id"], data=data)


# @router.get("/chats", response_model=list[ChatPreview])
# async def get_my_chats(
#     current_user=Depends(get_current_user()),
#     service: MessageService = Depends(get_message_service),
# ):
#     """Список всех диалогов (последнее сообщение из каждого)"""
#     return await service.get_my_chats(user_id=current_user["user_id"])


# @router.get("/unread", response_model=UnreadCountResponse)
# async def get_unread_count(
#     current_user=Depends(get_current_user()),
#     service: MessageService = Depends(get_message_service),
# ):
#     """Количество непрочитанных сообщений"""
#     return await service.get_unread_count(user_id=current_user["user_id"])


# @router.get("/{other_user_id}", response_model=list[MessageRead])
# async def get_conversation(
#     other_user_id: UUID,
#     current_user=Depends(get_current_user()),
#     service: MessageService = Depends(get_message_service),
# ):
#     """История переписки с конкретным пользователем"""
#     return await service.get_conversation(
#         current_user_id=current_user["user_id"],
#         other_user_id=other_user_id,
#     )
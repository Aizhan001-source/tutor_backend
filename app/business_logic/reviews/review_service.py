# from uuid import UUID
# from fastapi import HTTPException, status
# from data_access.reviews.review_repository import ReviewRepository
# from data_access.bookings.booking_repository import BookingRepository
# from api.reviews.review_schemas import ReviewCreate, ReviewRead, ReviewUpdate

# class ReviewService:
#     def __init__(
#             self,
#             review_repo: ReviewRepository,
#             booking_repo: BookingRepository
#         ):
#             self.repo = review_repo
#             self.repo = booking_repo

    
#     async def create_review(self, student_id: UUID, data: ReviewCreate):
#         booking = await self.booking_repo.get_by_id(data.booking_id)
#         if not booking:
#                 raise HTTPException(status_code=404, detail="Booking not found")
        
#         if booking.student_id != student_id:
#             raise HTTPException(status_code=403, detail="You can only review your own booking")

#         return await self.review_repo.create_review(
#             student_id=student_id,
#             tutor_id=data.tutor_id,
#             booking_id=data.booking_id,
#             rating=data.raiting,
#             comment=data.comment
#         )
    

#     async def get_by_id(self, review_id: UUID):
#         return await self.review_repo.get_by_id(review_id)
    
#     async def get_by_tutor(self, tutor_id: UUID):
#         return await self.review_repo.get_by_tutor(tutor_id)
    
#     async def get_by_student(self, student_id: UUID):
#         return await self.review_repo.get_by_student(student_id)
    

#     async def update(self, review_id: UUID, datat)
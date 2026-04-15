from fastapi import APIRouter
from api.user.user_api import router as users_router
from api.tutor.tutor_api import router as tutors_router
from api.students.student_api import router as students_router
from api.course.course_api import router as corses_router
from api.application.application_api import router as applications_router
from api.count.count_api import router as counts_router


api_router = APIRouter()

api_router.include_router(
    users_router,
    prefix="/users",
    tags=["USER"]
)

api_router.include_router(
    tutors_router,
    prefix="/tutors",
    tags=["TUTOR"]
)

api_router.include_router(
    students_router,
    prefix="/students",
    tags=["STUDENT"]
)

api_router.include_router(
    corses_router,
    prefix="/courses",
    tags=["COURSE"]
)

api_router.include_router(
    applications_router,
    prefix="/applications",
    tags=["APPLICATION"]
)

api_router.include_router(
    counts_router,
    prefix="/counts",
    tags=["COUNT"]
)
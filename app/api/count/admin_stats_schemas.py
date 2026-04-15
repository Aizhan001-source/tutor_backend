from pydantic import BaseModel


class AdminStatsSummary(BaseModel):
    students: int
    tutors: int
    active_sessions: int
    revenue_mtd: float
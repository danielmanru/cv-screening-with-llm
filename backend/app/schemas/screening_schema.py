from pydantic import BaseModel
from typing import Optional


class JobSummary(BaseModel):
    title: str


class ScreeningResultSummary(BaseModel):
    match_score: Optional[int] = None
    recommendation: Optional[str] = None


class ScreeningListResponse(BaseModel):
    id: str
    candidate_name: str
    job: JobSummary
    status: str
    result: Optional[ScreeningResultSummary] = None
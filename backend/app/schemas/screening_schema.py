from pydantic import BaseModel
from typing import List, Optional


class JobSummary(BaseModel):
    title: str
    employment_type: str
    work_arrangement: str


class ScreeningResultSummary(BaseModel):
    
    match_score: Optional[int] = None
    recommendation: Optional[str] = None
    summary: Optional[str] =None
    strengths: Optional[List[str]] = []
    weaknesses: Optional[List[str]] = []


class ScreeningListResponse(BaseModel):
    id: str
    candidate_name: str
    candidate_email:str
    job: JobSummary
    status: str
    result: Optional[ScreeningResultSummary] = None
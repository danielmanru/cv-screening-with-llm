from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field

from ..enums.screening_status import ScreeningStatus

from ..enums.recomendation_enum import Recommendation

from ..enums.work_arrangement import WorkArrangement

from ..enums.employment_type_enum import EmploymentType


class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core import core_schema

        return core_schema.no_info_plain_validator_function(cls.validate)

    @classmethod
    def validate(cls, value):
        if isinstance(value, ObjectId):
            return value

        if isinstance(value, str) and ObjectId.is_valid(value):
            return ObjectId(value)

        raise ValueError("Invalid ObjectId")


class JobInfo(BaseModel):
    title: str = Field(..., min_length=1, description="Nama pekerjaan")
    employment_type: EmploymentType = Field(..., description="Jenis kontrak pekerjaan")
    work_arrangement: WorkArrangement = Field(..., description="Sistem kerja")


class CVFileInfo(BaseModel):
    original_filename: str
    bucket_name: str
    object_name: str
    content_type: str = "application/pdf"
    file_size: int
    etag: Optional[str] = None


class ScreeningResult(BaseModel):
    match_score: int = Field(..., ge=0, le=100)
    summary: str
    matched_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    recommendation: Recommendation


class Screening(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        json_encoders={ObjectId: str},
    )
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    candidate_name: str = Field(..., min_length=1, description="Nama kandidat")
    job: JobInfo
    cv_file: Optional[CVFileInfo] = None

    result: Optional[ScreeningResult] = None

    status: ScreeningStatus = ScreeningStatus.PENDING
  
    error_message: Optional[str] = None

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
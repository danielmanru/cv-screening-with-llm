from typing import cast
import json
from bson import ObjectId
from fastapi import BackgroundTasks
from langchain_openrouter import ChatOpenRouter

from app.core.config import get_settings
from app.prompts.screening_prompt import cv_screening_prompt
from ..schemas.screening_schema import ScreeningListResponse

from ..enums.work_arrangement import WorkArrangement
from ..enums.employment_type_enum import EmploymentType
from ..models.screening_model import JobInfo, Screening, ScreeningResult 
from ..db.database import db


class CVScreeningService:
    def __init__(self) -> None:
        settings = get_settings()

        self.llm = ChatOpenRouter(
            model=settings.openrouter_model,
            temperature=0,
            api_key=settings.openrouter_api_key,
        )

        self.chain = cv_screening_prompt | self.llm

    # Implementation for processing screening
    async def screen_cv_process(self, screening_id: str, cv_text: str, job_requirement: str) -> None:
        result = await self.chain.ainvoke({
            "cv_text": cv_text,
            "job_requirement": job_requirement,
        })

        content = result.content

        if not isinstance(content, str):
            raise TypeError("Output LLM tidak berupa string.")

        try:
            parsed_data = json.loads(content)
            screening = ScreeningResult.model_validate(parsed_data)
            await db["screenings"].update_one(
                {"_id": ObjectId(screening_id)},
                {"$set": {"result": screening.model_dump(), "status": "completed"}},
            )
            
        except json.JSONDecodeError as error:
            raise ValueError(f"Output LLM bukan JSON valid: {error}")

    async def screen_cv(
        self,
        background_tasks: BackgroundTasks,
        cv_text: str,
        candidate_name: str,
        job_title: str,
        employment_type: EmploymentType,
        work_arrangement: WorkArrangement,
        job_requirement: str,
    ) -> Screening:
        screening: Screening = Screening(
            candidate_name=candidate_name,
            job=JobInfo(
                title=job_title,
                employment_type=employment_type,
                work_arrangement=work_arrangement,
            ),
        )

        result = await db["screenings"].insert_one(screening.model_dump())

        background_tasks.add_task(
            self.screen_cv_process,
            screening_id=str(result.inserted_id),
            cv_text=cv_text,
            job_requirement=job_requirement
        )

        screening_id= str(result.inserted_id)
        return screening.model_copy(update={"id": screening_id})

    async def get_screening(self, screening_id: str) -> Screening:
        data = await db["screenings"].find_one({"_id": ObjectId(screening_id)})

        if not data:
            raise ValueError("Screening tidak ditemukan.")

        return Screening.model_validate(data)  
        
    async def all_screening(self)-> list[ScreeningListResponse]:
        cursor = db["screenings"].find(
            {},
            {
                "candidate_name": 1,
                "job.title": 1,
                "status": 1,
                "result.match_score": 1,
                "result.recommendation": 1,
            }
        )
        screenings = await cursor.to_list(length=None)
        for screening in screenings:
            screening["id"] = str(screening.pop("_id"))

        return [ScreeningListResponse(**screening) for screening in screenings]
from fastapi import APIRouter, BackgroundTasks, File, Form, HTTPException, UploadFile
from pydantic import EmailStr


from app.services.screening_service import CVScreeningService
from app.services.pdf_service import PDFService
from app.schemas.screening_schema import ScreeningListResponse
from app.models.screening_model import Screening

from app.enums.work_arrangement_enum import WorkArrangement
from app.enums.employment_type_enum import EmploymentType

router = APIRouter(prefix="/cv-screening", tags=["CV Screening"])

cv_screening_service = CVScreeningService()

@router.post("/", response_model=Screening)
async def screen_cv(
    background_tasks: BackgroundTasks,
    cv: UploadFile = File(...),
    candidate_name: str = Form(...),
    candidate_email: EmailStr = Form(...),
    job_title: str = Form(...),
    employment_type: EmploymentType = Form(...),
    work_arrangement: WorkArrangement = Form(...),
    job_requirement: str = Form(...),
):
    try:
        cv_text = await PDFService.extract_text_from_pdf(cv)

        result = await cv_screening_service.screen_cv(
            background_tasks=background_tasks,
            cv_text=cv_text,
            job_requirement=job_requirement,
            candidate_name=candidate_name,
            candidate_email=candidate_email,
            job_title=job_title,
            employment_type=employment_type,
            work_arrangement=work_arrangement,
        )

        return result

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Gagal melakukan screening CV: {str(error)}",
        )
    
@router.get("/{screening_id}", response_model=Screening)
async def get_screening(screening_id: str):
    return await cv_screening_service.get_screening(screening_id)

@router.get("/", response_model=list[ScreeningListResponse])
async def all_screening():
    return await cv_screening_service.all_screening()
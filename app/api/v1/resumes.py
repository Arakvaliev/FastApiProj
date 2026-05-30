from fastapi import APIRouter, Depends, Query, status
from typing import Optional
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.resume import ResumeCreate, ResumeUpdate, ResumeRead, ResumeListItem
from app.services.resume_service import ResumeService
from app.services.auth_service import get_current_user
from app.models.user import User

router = APIRouter(prefix="/resumes", tags=["Resumes"])

@router.post("/", response_model=ResumeRead, status_code=status.HTTP_201_CREATED)
async def create_resume(
    data: ResumeCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = ResumeService(db)
    return await service.create_resume(data)

@router.get("/", response_model=list[ResumeListItem])
async def get_resumes(
    category_id: Optional[int] = Query(None, description="Filter by category"),
    min_experience: Optional[int] = Query(None, description="Filter by minimum experience"),
    higher_education: Optional[bool] = Query(None, description="Filter by higher education"),
    vacancy_id: Optional[int] = Query(None, description="Filter by vacancy"),
    status: Optional[str] = Query(None, description="Filter by status"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = ResumeService(db)
    return await service.get_resumes(category_id, min_experience, higher_education, vacancy_id, status)

@router.get("/{resume_id}", response_model=ResumeRead)
async def get_resume(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = ResumeService(db)
    return await service.get_resume(resume_id)

@router.put("/{resume_id}", response_model=ResumeRead)
async def update_resume(
    resume_id: int,
    data: ResumeUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = ResumeService(db)
    return await service.update_resume(resume_id, data)

@router.delete("/{resume_id}")
async def delete_resume(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = ResumeService(db)
    return await service.delete_resume(resume_id)
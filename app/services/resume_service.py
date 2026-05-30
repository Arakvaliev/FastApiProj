from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.resume import Resume
from app.schemas.resume import ResumeCreate, ResumeUpdate, ResumeRead, ResumeListItem
from app.repositories.resume_repository import ResumeRepository

class ResumeService:
    def __init__(self, db: Session):
        self.resume_repo = ResumeRepository(db)
    
    async def create_resume(self, data: ResumeCreate) -> ResumeRead:
        category = self.resume_repo.get_category_by_id(data.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        
        if data.vacancy_id:
            vacancy = self.resume_repo.get_vacancy_by_id(data.vacancy_id)
            if not vacancy:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Vacancy not found"
                )
        
        resume = Resume(**data.model_dump())
        created_resume = self.resume_repo.create_resume(resume)
        return ResumeRead.model_validate(created_resume)
    
    async def get_resume(self, resume_id: int) -> ResumeRead:
        resume = self.resume_repo.get_resume_by_id(resume_id)
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found"
            )
        return ResumeRead.model_validate(resume)
    
    async def get_resumes(
        self,
        category_id: Optional[int] = None,
        min_experience: Optional[int] = None,
        higher_education: Optional[bool] = None,
        vacancy_id: Optional[int] = None,
        status: Optional[str] = None
    ) -> List[ResumeListItem]:
        resumes = self.resume_repo.get_resumes_with_filters(
            category_id=category_id,
            min_experience=min_experience,
            higher_education=higher_education,
            vacancy_id=vacancy_id,
            status=status
        )
        return [ResumeListItem.model_validate(r) for r in resumes]
    
    async def update_resume(self, resume_id: int, data: ResumeUpdate) -> ResumeRead:
        resume = self.resume_repo.get_resume_by_id(resume_id)
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found"
            )
        
        if data.category_id:
            category = self.resume_repo.get_category_by_id(data.category_id)
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Category not found"
                )
        
        if data.vacancy_id:
            vacancy = self.resume_repo.get_vacancy_by_id(data.vacancy_id)
            if not vacancy:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Vacancy not found"
                )
        
        update_data = data.model_dump(exclude_unset=True)
        updated_resume = self.resume_repo.update_resume(resume, update_data)
        return ResumeRead.model_validate(updated_resume)
    
    async def delete_resume(self, resume_id: int) -> dict:
        resume = self.resume_repo.get_resume_by_id(resume_id)
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found"
            )
        
        self.resume_repo.delete_resume(resume)
        return {"message": "Resume deleted successfully"}
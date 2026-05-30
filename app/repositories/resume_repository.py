from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models.resume import Resume
from app.models.vacancy import Vacancy, Category

class ResumeRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_resume(self, resume: Resume) -> Resume:
        self.db.add(resume)
        self.db.commit()
        self.db.refresh(resume)
        return self.get_resume_by_id(resume.id)
    
    def get_resume_by_id(self, resume_id: int) -> Optional[Resume]:
        return (
            self.db.query(Resume)
            .options(
                joinedload(Resume.category),
                joinedload(Resume.vacancy)
            )
            .filter(Resume.id == resume_id)
            .first()
        )
    
    def get_resumes_with_filters(
        self,
        category_id: Optional[int] = None,
        min_experience: Optional[int] = None,
        higher_education: Optional[bool] = None,
        vacancy_id: Optional[int] = None,
        status: Optional[str] = None
    ) -> List[Resume]:
        query = self.db.query(Resume).options(
            joinedload(Resume.category),
            joinedload(Resume.vacancy)
        )
        
        if category_id:
            query = query.filter(Resume.category_id == category_id)
        
        if min_experience is not None:
            query = query.filter(Resume.experience_years >= min_experience)
        
        if higher_education is not None:
            query = query.filter(Resume.higher_education == higher_education)
        
        if vacancy_id is not None:
            query = query.filter(Resume.vacancy_id == vacancy_id)
        
        if status:
            query = query.filter(Resume.status == status)
        
        return query.all()
    
    def update_resume(self, resume: Resume, update_data: dict) -> Resume:
        for key, value in update_data.items():
            setattr(resume, key, value)
        self.db.commit()
        self.db.refresh(resume)
        return self.get_resume_by_id(resume.id)
    
    def delete_resume(self, resume: Resume) -> None:
        self.db.delete(resume)
        self.db.commit()
    
    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        return self.db.query(Category).filter(Category.id == category_id).first()
    
    def get_vacancy_by_id(self, vacancy_id: int) -> Optional[Vacancy]:
        return self.db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
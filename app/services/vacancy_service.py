from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.vacancy import Vacancy, Position, Category
from app.schemas.vacancy import VacancyCreate, VacancyUpdate, VacancyRead, VacancyListItem, PositionCreate, CategoryCreate, PositionRead, CategoryRead
from app.repositories.vacancy_repository import VacancyRepository

class VacancyService:
    def __init__(self, db: Session):
        self.vacancy_repo = VacancyRepository(db)
        self.db = db
    
    async def create_vacancy(self, data: VacancyCreate, current_user: User) -> VacancyRead:
        position = self.vacancy_repo.get_position_by_id(data.position_id)
        if not position:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Position not found"
            )
        
        category = self.vacancy_repo.get_category_by_id(data.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        
        vacancy = Vacancy(
            **data.model_dump(),
            hr_id=current_user.id,
            status="open"
        )
        
        created_vacancy = self.vacancy_repo.create_vacancy(vacancy)
        return VacancyRead.model_validate(created_vacancy)
    
    async def get_vacancy(self, vacancy_id: int) -> VacancyRead:
        vacancy = self.vacancy_repo.get_vacancy_by_id(vacancy_id)
        if not vacancy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vacancy not found"
            )
        return VacancyRead.model_validate(vacancy)
    
    async def get_vacancies(
        self,
        status: Optional[str] = None,
        category_id: Optional[int] = None,
        min_salary: Optional[int] = None
    ) -> List[VacancyListItem]:
        vacancies = self.vacancy_repo.get_vacancies_with_filters(
            status=status,
            category_id=category_id,
            min_salary=min_salary
        )
        
        result = []
        for v in vacancies:
            result.append(VacancyListItem(
                id=v.id,
                title=v.title,
                category=v.category.name,
                status=v.status,
                min_salary=v.min_salary,
                created_at=v.created_at
            ))
        
        return result
            
    async def update_vacancy(self, vacancy_id: int, data: VacancyUpdate, current_user: User) -> VacancyRead:
        vacancy = self.vacancy_repo.get_vacancy_by_id(vacancy_id)
        if not vacancy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vacancy not found"
            )
        
        if vacancy.hr_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to update this vacancy"
            )
        
        update_data = data.model_dump(exclude_unset=True)
        updated_vacancy = self.vacancy_repo.update_vacancy(vacancy, update_data)
        return VacancyRead.model_validate(updated_vacancy)
    
    async def delete_vacancy(self, vacancy_id: int, current_user: User) -> dict:
        vacancy = self.vacancy_repo.get_vacancy_by_id(vacancy_id)
        if not vacancy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vacancy not found"
            )
        
        if vacancy.hr_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to delete this vacancy"
            )
        
        self.vacancy_repo.delete_vacancy(vacancy)
        return {"message": "Vacancy deleted successfully"}
    
    async def create_position(self, data: PositionCreate) -> PositionRead:
        existing = self.vacancy_repo.get_position_by_name(data.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Position with this name already exists"
            )
        
        position = Position(name=data.name)
        created = self.vacancy_repo.create_position(position)
        return PositionRead.model_validate(created)
    
    async def get_positions(self) -> List[PositionRead]:
        positions = self.vacancy_repo.get_all_positions()
        return [PositionRead.model_validate(p) for p in positions]
    
    async def update_position(self, position_id: int, data: PositionCreate) -> PositionRead:
        position = self.vacancy_repo.get_position_by_id(position_id)
        if not position:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Position not found"
            )
        
        updated = self.vacancy_repo.update_position(position, data.name)
        return PositionRead.model_validate(updated)
    
    async def delete_position(self, position_id: int) -> dict:
        position = self.vacancy_repo.get_position_by_id(position_id)
        if not position:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Position not found"
            )
        
        vacancies_count = self.vacancy_repo.get_vacancies_count_by_position(position_id)
        if vacancies_count > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete position with existing vacancies"
            )
        
        self.vacancy_repo.delete_position(position)
        return {"message": "Position deleted successfully"}
    
    async def create_category(self, data: CategoryCreate) -> CategoryRead:
        existing = self.vacancy_repo.get_category_by_name(data.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category with this name already exists"
            )
        
        category = Category(name=data.name)
        created = self.vacancy_repo.create_category(category)
        return CategoryRead.model_validate(created)
    
    async def get_categories(self) -> List[CategoryRead]:
        categories = self.vacancy_repo.get_all_categories()
        return [CategoryRead.model_validate(c) for c in categories]
    
    async def update_category(self, category_id: int, data: CategoryCreate) -> CategoryRead:
        category = self.vacancy_repo.get_category_by_id(category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        
        updated = self.vacancy_repo.update_category(category, data.name)
        return CategoryRead.model_validate(updated)
    
    async def delete_category(self, category_id: int) -> dict:
        category = self.vacancy_repo.get_category_by_id(category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        
        vacancies_count = self.vacancy_repo.get_vacancies_count_by_category(category_id)
        if vacancies_count > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete category with existing vacancies"
            )
        
        self.vacancy_repo.delete_category(category)
        return {"message": "Category deleted successfully"}
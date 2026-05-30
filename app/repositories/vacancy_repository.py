from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models.vacancy import Vacancy, Position, Category

class VacancyRepository:
    def __init__(self, db: Session):
        self.db = db
    
    # Вакансии
    def create_vacancy(self, vacancy: Vacancy) -> Vacancy:
        self.db.add(vacancy)
        self.db.commit()
        self.db.refresh(vacancy)
        return self.get_vacancy_by_id(vacancy.id)
    
    def get_vacancy_by_id(self, vacancy_id: int) -> Optional[Vacancy]:
        return (
            self.db.query(Vacancy)
            .options(
                joinedload(Vacancy.position),
                joinedload(Vacancy.category),
                joinedload(Vacancy.hr)
            )
            .filter(Vacancy.id == vacancy_id)
            .first()
        )
    
    def get_vacancies_with_filters(
        self,
        status: Optional[str] = None,
        category_id: Optional[int] = None,
        min_salary: Optional[int] = None
    ) -> List[Vacancy]:
        query = self.db.query(Vacancy).options(joinedload(Vacancy.category))
        
        if status:
            query = query.filter(Vacancy.status == status)
        
        if category_id:
            query = query.filter(Vacancy.category_id == category_id)
        
        if min_salary is not None:
            query = query.filter(Vacancy.min_salary >= min_salary)
        
        return query.all()
    
    def update_vacancy(self, vacancy: Vacancy, update_data: dict) -> Vacancy:
        for key, value in update_data.items():
            setattr(vacancy, key, value)
        self.db.commit()
        self.db.refresh(vacancy)
        return self.get_vacancy_by_id(vacancy.id)
    
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        self.db.delete(vacancy)
        self.db.commit()
    
    # Должности
    def create_position(self, position: Position) -> Position:
        self.db.add(position)
        self.db.commit()
        self.db.refresh(position)
        return position
    
    def get_position_by_id(self, position_id: int) -> Optional[Position]:
        return self.db.query(Position).filter(Position.id == position_id).first()
    
    def get_position_by_name(self, name: str) -> Optional[Position]:
        return self.db.query(Position).filter(Position.name == name).first()
    
    def get_all_positions(self) -> List[Position]:
        return self.db.query(Position).all()
    
    def update_position(self, position: Position, name: str) -> Position:
        position.name = name
        self.db.commit()
        self.db.refresh(position)
        return position
    
    def delete_position(self, position: Position) -> None:
        self.db.delete(position)
        self.db.commit()
    
    def get_vacancies_count_by_position(self, position_id: int) -> int:
        return self.db.query(Vacancy).filter(Vacancy.position_id == position_id).count()
    
    # Категории
    def create_category(self, category: Category) -> Category:
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category
    
    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        return self.db.query(Category).filter(Category.id == category_id).first()
    
    def get_category_by_name(self, name: str) -> Optional[Category]:
        return self.db.query(Category).filter(Category.name == name).first()
    
    def get_all_categories(self) -> List[Category]:
        return self.db.query(Category).all()
    
    def update_category(self, category: Category, name: str) -> Category:
        category.name = name
        self.db.commit()
        self.db.refresh(category)
        return category
    
    def delete_category(self, category: Category) -> None:
        self.db.delete(category)
        self.db.commit()
    
    def get_vacancies_count_by_category(self, category_id: int) -> int:
        return self.db.query(Vacancy).filter(Vacancy.category_id == category_id).count()
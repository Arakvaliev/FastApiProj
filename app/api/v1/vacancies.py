from fastapi import APIRouter, Depends, Query, status
from typing import Optional
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.vacancy import (
    VacancyCreate, VacancyUpdate, VacancyRead, VacancyListItem,
    PositionCreate, PositionRead, CategoryCreate, CategoryRead
)
from app.services.vacancy_service import VacancyService
from app.services.auth_service import get_current_user
from app.models.user import User

router = APIRouter(prefix="/vacancies", tags=["Vacancies"])

# Вакансии
@router.post("/", response_model=VacancyRead, status_code=status.HTTP_201_CREATED)
async def create_vacancy(
    data: VacancyCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = VacancyService(db)
    return await service.create_vacancy(data, current_user)

@router.get("/", response_model=list[VacancyListItem])
async def get_vacancies(
    status: Optional[str] = Query(None, description="Filter by status"),
    category_id: Optional[int] = Query(None, description="Filter by category"),
    min_salary: Optional[int] = Query(None, description="Filter by minimum salary"),
    db: Session = Depends(get_db)
):
    service = VacancyService(db)
    return await service.get_vacancies(status, category_id, min_salary)

@router.get("/{vacancy_id}", response_model=VacancyRead)
async def get_vacancy(vacancy_id: int, db: Session = Depends(get_db)):
    service = VacancyService(db)
    return await service.get_vacancy(vacancy_id)

@router.put("/{vacancy_id}", response_model=VacancyRead)
async def update_vacancy(
    vacancy_id: int,
    data: VacancyUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = VacancyService(db)
    return await service.update_vacancy(vacancy_id, data, current_user)

@router.delete("/{vacancy_id}", status_code=status.HTTP_200_OK)
async def delete_vacancy(
    vacancy_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = VacancyService(db)
    return await service.delete_vacancy(vacancy_id, current_user)

# Должности
@router.post("/positions", response_model=PositionRead, status_code=status.HTTP_201_CREATED)
async def create_position(
    data: PositionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = VacancyService(db)
    return await service.create_position(data)

@router.get("/positions", response_model=list[PositionRead])
async def get_positions(db: Session = Depends(get_db)):
    service = VacancyService(db)
    return await service.get_positions()

@router.put("/positions/{position_id}", response_model=PositionRead)
async def update_position(
    position_id: int,
    data: PositionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = VacancyService(db)
    return await service.update_position(position_id, data)

@router.delete("/positions/{position_id}")
async def delete_position(
    position_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = VacancyService(db)
    return await service.delete_position(position_id)

# категории

@router.post("/categories", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(
    data: CategoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = VacancyService(db)
    return await service.create_category(data)

@router.get("/categories", response_model=list[CategoryRead])
async def get_categories(db: Session = Depends(get_db)):
    service = VacancyService(db)
    return await service.get_categories()

@router.put("/categories/{category_id}", response_model=CategoryRead)
async def update_category(
    category_id: int,
    data: CategoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = VacancyService(db)
    return await service.update_category(category_id, data)

@router.delete("/categories/{category_id}")
async def delete_category(
    category_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = VacancyService(db)
    return await service.delete_category(category_id)
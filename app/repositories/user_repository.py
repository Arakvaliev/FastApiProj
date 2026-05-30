from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_login(self, login: str) -> Optional[User]:
        return self.db.query(User).filter(User.login == login).first()
    
    def update_password(self, user: User, new_hashed_password: str) -> None:
        user.hashed_password = new_hashed_password
        self.db.commit()
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base, get_db
from app.main import app
from app.models.user import User
from app.models.vacancy import Position, Category
from app.services.auth_service import AuthService

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def auth_headers(client, db_session):
    auth_service = AuthService(db_session)
    user = User(
        first_name="Test",
        last_name="User",
        login="testuser",
        hashed_password=auth_service.hash_password("testpassword123")
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    response = client.post("/api/v1/auth/login", json={
        "login": "testuser",
        "password": "testpassword123"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def sample_position(db_session):
    position = Position(name="Software Developer")
    db_session.add(position)
    db_session.commit()
    db_session.refresh(position)
    return position

@pytest.fixture
def sample_category(db_session):
    category = Category(name="IT")
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    return category
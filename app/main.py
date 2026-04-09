from fastapi import FastAPI, Depends
from app.routers import students, auth
from app.database import engine, Base
from app.auth import get_current_user

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student API", version="1.0.0")

app.include_router(students.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Welcome to Student API"}

@app.get("/protected")
def protected_route(current_user = Depends(get_current_user)):
    return {"message": "This is protected route", "user": current_user.username}
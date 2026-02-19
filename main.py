from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel, EmailStr, field_validator
from datetime import date
import json
import re
import os
from uuid import uuid4


app = FastAPI()

class UserData(BaseModel):
    surname: str
    name: str
    birth_date: date
    phone: str
    email: EmailStr

    @field_validator('surname', 'name')
    def validate_cyrillic(cls, v):
        if not re.match(r'^[А-Я][а-я]+$', v):
            raise ValueError('Должно содержать только кириллицу и заглавную первую букву')
        return v

    @field_validator('phone')
    def validate_phone(cls, v):
        phone = re.sub(r'[\s\-\(\)]', '', v)
        if not re.match(r'^\+?7\d{10}$|^8\d{10}$', phone):
            raise ValueError('Неверный формат телефона')
        return v

@app.post("/save_user")
async def save_user(user: UserData):
    os.makedirs("data", exist_ok=True)
    filename = f"data/user_{uuid4()}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(user.model_dump(), f, ensure_ascii=False, indent=2, default=str)
    
    return {
        "status": "success",
        "filename": filename
    }
    

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port = 8000)

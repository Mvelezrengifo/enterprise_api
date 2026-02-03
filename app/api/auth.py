# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.models.user import User
from app.services.auth import create_access_token
from app.db.database import SessionLocal
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Usuario no existe")
    if not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")
    token = create_access_token({"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}

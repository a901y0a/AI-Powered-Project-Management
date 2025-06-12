from fastapi import APIRouter, HTTPException, Depends
from app.database import SessionLocal
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import LoginRequest, Token
from passlib.hash import bcrypt
from app.utils.auth import create_access_token

router = APIRouter(prefix="/api/auth", tags=["auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/login", response_model=Token)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == req.username).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    if not bcrypt.verify(req.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.username, "role": user.role})
    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role
    }


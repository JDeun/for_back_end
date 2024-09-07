from fastapi import APIRouter
from sqlalchemy.orm import Session
from models import User
from database import SessionLocal

router = APIRouter()

@router.get("/users")
def get_users():
    db: Session = SessionLocal()
    users = db.query(User).all()
    return users

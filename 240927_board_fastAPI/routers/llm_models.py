from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas import LLMModelCreate, LLMModelResponse
from models import LLMModel

router = APIRouter()

# 데이터베이스 세션을 의존성으로 사용하는 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=LLMModelResponse)
def create_llm_model(llm_model: LLMModelCreate, db: Session = Depends(get_db)):
    db_llm_model = LLMModel(**llm_model.dict())
    db.add(db_llm_model)
    db.commit()
    db.refresh(db_llm_model)
    return db_llm_model

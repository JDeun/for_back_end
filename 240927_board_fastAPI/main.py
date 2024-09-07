from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from database import engine, Base
from routers import posts
from sqlalchemy.orm import Session
from database import SessionLocal
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 데이터베이스 모델의 테이블 생성
Base.metadata.create_all(bind=engine)

# 템플릿 설정
templates = Jinja2Templates(directory="templates")

# 라우터를 애플리케이션에 추가
app.include_router(posts.router, prefix="/posts", tags=["posts"])

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    logger.info("Application is starting up")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
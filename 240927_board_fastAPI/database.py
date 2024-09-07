from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 데이터베이스 URL (자신의 데이터베이스에 맞게 변경해야 합니다)
DATABASE_URL = "mysql+pymysql://jd_admin:472291whdks!@localhost/board_db_fastapi"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# SQLAlchemy 엔진 생성
engine = create_engine(DATABASE_URL)

# 세션 로컬 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 데이터베이스 모델의 베이스 클래스
Base = declarative_base()

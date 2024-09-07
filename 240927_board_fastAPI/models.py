from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.sql import func

# 게시글 테이블 모델
class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    author_id = Column(String, ForeignKey("users.id"), index=True)
    title = Column(String, index=True)
    content = Column(String)
    llm_id = Column(Integer, ForeignKey("llm_models.id"))

    author = relationship("User", back_populates="posts")
    llm = relationship("LLMModel")

# 사용자 테이블 모델
class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    receive_ads = Column(Integer)

    posts = relationship("Post", back_populates="author")

# LLM 모델 테이블 모델
class LLMModel(Base):
    __tablename__ = "llm_models"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    output_type = Column(String)

from fastapi import APIRouter, Depends, HTTPException, Request, Form, Body
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from models import Post, User, LLMModel
from database import get_db
from auth import get_current_user, verify_password
from datetime import datetime
from fastapi.responses import RedirectResponse, JSONResponse
import logging

router = APIRouter()
templates = Jinja2Templates(directory="templates")
logger = logging.getLogger(__name__)

@router.get("/web")
def posts_page(request: Request, db: Session = Depends(get_db)):
    posts = db.query(Post).order_by(Post.created_at.desc()).all()
    return templates.TemplateResponse("posts.html", {"request": request, "posts": posts})

@router.get("/create")
def create_post_page(request: Request, db: Session = Depends(get_db)):
    llm_models = db.query(LLMModel).all()
    return templates.TemplateResponse("create_post.html", {"request": request, "llm_models": llm_models})

@router.post("/create")
def create_post(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    llm_id: int = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info(f"Attempting to create post for user: {current_user.email}")
    try:
        new_post = Post(
            title=title,
            content=content,
            llm_id=llm_id,
            author_id=current_user.id,
            created_at=datetime.now()
        )
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        logger.info(f"Post created successfully for user: {current_user.email}")
        return RedirectResponse(url="/posts/web", status_code=303)
    except Exception as e:
        logger.error(f"Error creating post: {str(e)}")
        db.rollback()
        error_message = f"Error occurred: {str(e)}"
        return templates.TemplateResponse("create_post.html", {
            "request": request,
            "error": error_message,
            "title": title,
            "content": content,
            "llm_models": db.query(LLMModel).all()
        }, status_code=400)
    

@router.get("/{post_id}")
def post_detail(request: Request, post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return templates.TemplateResponse("post_detail.html", {"request": request, "post": post})

@router.post("/authenticate")
async def authenticate_user(data: dict = Body(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data['email']).first()
    post = db.query(Post).filter(Post.id == data['post_id']).first()
    
    logger.info(f"Authenticating user: {data['email']}")
    logger.info(f"Post ID: {data['post_id']}")
    logger.info(f"User found: {user is not None}")
    logger.info(f"Post found: {post is not None}")
    
    if user and verify_password(data['password'], user.hashed_password) and post and post.author_id == user.id:
        logger.info("Authentication successful")
        return JSONResponse(content={"authenticated": True})
    logger.warning("Authentication failed")
    return JSONResponse(content={"authenticated": False})

@router.get("/delete/{post_id}")
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        db.delete(post)
        db.commit()
    return RedirectResponse(url="/posts/web", status_code=303)

@router.get("/edit/{post_id}")
async def edit_post_page(request: Request, post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    llm_models = db.query(LLMModel).all()
    return templates.TemplateResponse("create_post.html", {"request": request, "post": post, "llm_models": llm_models})

@router.post("/edit/{post_id}")
async def edit_post(
    request: Request,
    post_id: int,
    title: str = Form(...),
    content: str = Form(...),
    llm_id: int = Form(...),
    db: Session = Depends(get_db)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        post.title = title
        post.content = content
        post.llm_id = llm_id
        db.commit()
    return RedirectResponse(url=f"/posts/{post_id}", status_code=303)
@router.post("/edit/{post_id}")
async def edit_post(
    request: Request,
    post_id: int,
    title: str = Form(...),
    content: str = Form(...),
    llm_id: int = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post and post.author_id == current_user.id:
        post.title = title
        post.content = content
        post.llm_id = llm_id
        db.commit()
        return RedirectResponse(url=f"/posts/{post_id}", status_code=303)
    else:
        raise HTTPException(status_code=403, detail="You don't have permission to edit this post")
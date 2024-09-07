# routers/__init__.py

from .posts import router as posts_router
from .users import router as users_router
from .llm_models import router as llm_models_router

__all__ = ["posts_router", "users_router", "llm_models_router"]

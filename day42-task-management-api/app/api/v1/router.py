from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.comments import router as comments_router
from app.api.v1.endpoints.inventory import router as inventory_router
from app.api.v1.endpoints.projects import router as projects_router
from app.api.v1.endpoints.tasks import router as tasks_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(projects_router, prefix="/projects", tags=["projects"])
api_router.include_router(tasks_router, prefix="/tasks", tags=["tasks"])
api_router.include_router(comments_router, prefix="/comments", tags=["comments"])
api_router.include_router(inventory_router, prefix="/inventory", tags=["inventory"])
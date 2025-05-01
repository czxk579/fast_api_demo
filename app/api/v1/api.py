from fastapi import APIRouter

from app.api.v1 import auth, users, tasks

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["认证"])
api_router.include_router(users.router, prefix="/users", tags=["用户"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["任务"]) 

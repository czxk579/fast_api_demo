import time
from typing import Any
from loguru import logger
import os
import sentry_sdk
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.api.deps import get_db

from app.api.v1.api import api_router
from app.core.config import settings
from app.db.session import Base, engine

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 配置 Sentry
if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        traces_sample_rate=1.0,
        environment=settings.ENVIRONMENT,
    )

# 日志目录自动创建
log_dir = os.path.dirname(settings.LOG_FILE)
if log_dir and not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 配置 loguru 日志
logger.add(
    settings.LOG_FILE,
    rotation=settings.LOG_ROTATION,  # 支持 "10 MB", "1 week" 等
    encoding="utf-8",
    enqueue=True,  # 多进程安全
    retention="10 days",  # 可选：日志保留时间
    backtrace=True,
    diagnose=True
)

# 初始化 FastAPI 应用
app = FastAPI(
    title=settings.APP_NAME,
    openapi_url="/api/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# 添加 CORS 中间件
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# 添加请求ID和请求处理时间中间件
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    request_id = str(time.time())
    request.state.request_id = request_id
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Request-ID"] = request_id
    logger.debug(f"Request {request_id} took {process_time:.2f}s")
    return response

# 注册 API 路由
app.include_router(api_router, prefix="/api/v1")

# 健康检查端点
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# 数据库初始化测试
@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    try:
        # 检查数据库连接
        db.execute("SELECT 1")
        return {"status": "ok", "message": "数据库连接正常"}
    except Exception as e:
        logger.error(f"数据库连接错误: {e}")
        raise HTTPException(status_code=500, detail=f"数据库连接错误: {str(e)}")

# 主函数
if __name__ == "__main__":
    import uvicorn
    import sys
    import os
    
    # 添加项目根目录到Python路径
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    # 设置日志格式
    logger.info(f"服务名称: {settings.APP_NAME}，启动端口: {settings.SERVER_PORT}")
    
    # 启动服务器
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.SERVER_PORT,
        reload=True
    ) 

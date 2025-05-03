import secrets
from loguru import logger
from typing import List, Union, Dict, Any, Optional

from pydantic import AnyHttpUrl, PostgresDsn, validator
from pydantic_settings import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Settings(BaseSettings):
    # 应用设置
    APP_NAME: str = "FastAPI_Demo"
    SERVER_PORT: int = 8090
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]

    # 日志设置
    LOG_LEVEL: str = "DEBUG"
    LOG_FILE: str = "logs/app.log"         # 日志文件路径
    LOG_ROTATION: str = "10 MB"            # 日志切割大小或周期（如 "10 MB"、"1 week"）

    # CORS设置
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # 数据库配置
    MYSQL_SERVER: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "user"
    MYSQL_PASSWORD: str = "password"
    MYSQL_DB: str = "test"
    DATABASE_URL: Optional[str] = None
    DATABASE_ECHO: bool = True
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return self.get_database_url()

    # Redis设置
    REDIS_SERVER: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""
    REDIS_URL: Optional[str] = None

    # MongoDB设置
    MONGO_SERVER: str = "40.233.84.60"
    MONGO_PORT: int = 27017
    MONGO_USER: str = ""
    MONGO_PASSWORD: str = ""
    MONGO_DB: str = ""
    MONGO_URL: str = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_SERVER}:{MONGO_PORT}/{MONGO_DB}"

    # Celery设置
    CELERY_BROKER_URL: str = "redis://{REDIS_SERVER}:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://{REDIS_SERVER}:6379/2"

    # Sentry设置
    SENTRY_DSN: Optional[str] = None
    

    def get_database_url(self, db_name: str = None):
        db = db_name or self.MYSQL_DB
        database_url = f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_SERVER}:{self.MYSQL_PORT}/{db}"
        logger.info(f"database_url: {database_url}")
        return database_url

    @property
    def redis_url(self):
        if self.REDIS_URL:
            return self.REDIS_URL
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_SERVER}:{self.REDIS_PORT}/0"
        return f"redis://{self.REDIS_SERVER}:{self.REDIS_PORT}/0"

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"
        


# 创建配置实例
settings = Settings() 

def get_session_for_db(db_name: str):
    url = settings.get_database_url(db_name)
    engine = create_engine(url, echo=settings.DATABASE_ECHO)
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return Session() 
 
import os
from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.session import Base, get_db
from app.services import user as user_service
from app.schemas.user import UserCreate

# 导入主应用
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app


# 测试数据库设置
TEST_SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI

engine = create_engine(
    TEST_SQLALCHEMY_DATABASE_URL, echo=settings.DATABASE_ECHO
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db() -> Generator:
    """
    创建测试数据库会话
    """
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db) -> Generator:
    """
    创建测试客户端，并使用测试数据库
    """
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c


@pytest.fixture
def superuser_token_headers(client: TestClient, db) -> Dict[str, str]:
    """
    创建超级用户，并获取其令牌
    """
    superuser_in = {
        "email": "admin@example.com",
        "username": "admin",
        "password": "admin123",
        "is_superuser": True,
    }
    user = user_service.create(db, obj_in=UserCreate(**superuser_in))
    
    login_data = {
        "username": superuser_in["email"],
        "password": superuser_in["password"],
    }
    r = client.post("/api/v1/auth/login", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    return {"Authorization": f"Bearer {a_token}"} 

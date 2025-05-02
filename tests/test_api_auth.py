from fastapi.testclient import TestClient

from app.services import user as user_service
from app.schemas.user import UserCreate


def test_login(client: TestClient, db) -> None:
    """测试登录功能"""
    # 创建测试用户
    user_in = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpass123",
    }
    user = user_service.create(db, obj_in=UserCreate(**user_in))

    # 测试登录
    login_data = {
        "username": user_in["email"],
        "password": user_in["password"],
    }
    r = client.post("/api/v1/auth/login", data=login_data)
    assert r.status_code == 200
    tokens = r.json()
    assert "access_token" in tokens
    assert tokens["token_type"] == "bearer"


def test_login_wrong_password(client: TestClient, db) -> None:
    """测试错误密码登录"""
    # 创建测试用户
    user_in = {
        "email": "test2@example.com",
        "username": "testuser2",
        "password": "testpass123",
    }
    user = user_service.create(db, obj_in=UserCreate(**user_in))

    # 测试错误密码登录
    login_data = {
        "username": user_in["email"],
        "password": "wrong_password",
    }
    r = client.post("/api/v1/auth/login", data=login_data)
    assert r.status_code == 400


def test_test_token(client: TestClient, superuser_token_headers, db) -> None:
    """测试令牌验证"""
    r = client.post("/api/v1/auth/test-token", headers=superuser_token_headers)
    assert r.status_code == 200
    result = r.json()
    assert "id" in result
    assert "email" in result
    assert result["is_superuser"] is True

    # 创建测试用户
    superuser_in = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpass123",
    }
    user = user_service.create(db, obj_in=UserCreate(**superuser_in))

    # 测试令牌验证
    r = client.post("/api/v1/auth/test-token", headers=superuser_token_headers)
    assert r.status_code == 200
    result = r.json()
    assert "id" in result
    assert "email" in result
    assert result["is_superuser"] is True 

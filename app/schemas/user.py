from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# 共享属性
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False


# 创建时需要的属性
class UserCreate(UserBase):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)


# 更新时可选的属性
class UserUpdate(UserBase):
    password: Optional[str] = Field(None, min_length=8)


# 数据库模型的属性
class UserInDBBase(UserBase):
    id: int
    email: EmailStr
    username: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# 返回给API的用户信息
class User(UserInDBBase):
    pass


# 存储在数据库的用户信息（包含密码）
class UserInDB(UserInDBBase):
    hashed_password: str


# 令牌模式
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[int] = None 

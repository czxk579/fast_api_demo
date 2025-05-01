from typing import Optional

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


def get_by_email(db: Session, email: str) -> Optional[User]:
    """
    通过邮箱获取用户
    """
    return db.query(User).filter(User.email == email).first()


def get_by_username(db: Session, username: str) -> Optional[User]:
    """
    通过用户名获取用户
    """
    return db.query(User).filter(User.username == username).first()


def get_by_id(db: Session, id: int) -> Optional[User]:
    """
    通过用户ID获取用户
    """
    return db.query(User).filter(User.id == id).first()


def create(db: Session, obj_in: UserCreate) -> User:
    """
    创建新用户
    """
    db_obj = User(
        email=obj_in.email,
        username=obj_in.username,
        hashed_password=get_password_hash(obj_in.password),
        is_superuser=obj_in.is_superuser,
        is_active=obj_in.is_active,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(
    db: Session, db_obj: User, obj_in: UserUpdate
) -> User:
    """
    更新用户信息
    """
    update_data = obj_in.dict(exclude_unset=True)
    if "password" in update_data and update_data["password"]:
        update_data["hashed_password"] = get_password_hash(update_data["password"])
        del update_data["password"]
    
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def authenticate(db: Session, email: str, password: str) -> Optional[User]:
    """
    验证用户身份
    """
    user = get_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def is_active(user: User) -> bool:
    """
    检查用户是否活跃
    """
    return user.is_active


def is_superuser(user: User) -> bool:
    """
    检查用户是否是超级用户
    """
    return user.is_superuser 

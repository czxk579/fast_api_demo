from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

Base = declarative_base()

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, echo=settings.DATABASE_ECHO)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 依赖注入函数，用于获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 

def get_session_for_db(db_name: str):
    url = settings.get_database_url(db_name)
    engine = create_engine(url, echo=settings.DATABASE_ECHO)
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return Session() 

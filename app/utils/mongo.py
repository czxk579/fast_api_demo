import logging
from typing import Any, Dict, List, Optional

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from app.core.config import settings

logger = logging.getLogger(__name__)

# 全局 MongoDB 客户端
_mongo_client = None


def get_mongo_client() -> MongoClient:
    """
    获取 MongoDB 客户端
    """
    global _mongo_client
    if _mongo_client is None:
        try:
            _mongo_client = MongoClient(settings.MONGO_URL)
        except Exception as e:
            logger.error(f"MongoDB 连接异常: {e}")
            raise
    return _mongo_client


def get_database(db_name: Optional[str] = None) -> Database:
    """
    获取 MongoDB 数据库
    """
    client = get_mongo_client()
    if db_name is None:
        # 从连接URL中提取数据库名
        db_name = settings.MONGO_URL.split("/")[-1]
    return client[db_name]


def get_collection(collection_name: str, db_name: Optional[str] = None) -> Collection:
    """
    获取 MongoDB 集合
    """
    db = get_database(db_name)
    return db[collection_name]


def insert_one(collection_name: str, document: Dict[str, Any], db_name: Optional[str] = None) -> str:
    """
    插入一条文档
    """
    try:
        collection = get_collection(collection_name, db_name)
        result = collection.insert_one(document)
        return str(result.inserted_id)
    except Exception as e:
        logger.error(f"MongoDB 插入文档异常: {e}")
        return None


def find_one(collection_name: str, query: Dict[str, Any], db_name: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    查询一条文档
    """
    try:
        collection = get_collection(collection_name, db_name)
        return collection.find_one(query)
    except Exception as e:
        logger.error(f"MongoDB 查询文档异常: {e}")
        return None


def find_many(
    collection_name: str, 
    query: Dict[str, Any], 
    db_name: Optional[str] = None,
    limit: int = 0,
    skip: int = 0,
    sort: Optional[List[tuple]] = None
) -> List[Dict[str, Any]]:
    """
    查询多条文档
    """
    try:
        collection = get_collection(collection_name, db_name)
        cursor = collection.find(query)
        
        if skip:
            cursor = cursor.skip(skip)
        if limit:
            cursor = cursor.limit(limit)
        if sort:
            cursor = cursor.sort(sort)
        
        return list(cursor)
    except Exception as e:
        logger.error(f"MongoDB 查询多条文档异常: {e}")
        return []


def update_one(
    collection_name: str, 
    query: Dict[str, Any], 
    update: Dict[str, Any], 
    db_name: Optional[str] = None,
    upsert: bool = False
) -> bool:
    """
    更新一条文档
    """
    try:
        collection = get_collection(collection_name, db_name)
        result = collection.update_one(query, update, upsert=upsert)
        return result.modified_count > 0 or (upsert and result.upserted_id is not None)
    except Exception as e:
        logger.error(f"MongoDB 更新文档异常: {e}")
        return False


def delete_one(collection_name: str, query: Dict[str, Any], db_name: Optional[str] = None) -> bool:
    """
    删除一条文档
    """
    try:
        collection = get_collection(collection_name, db_name)
        result = collection.delete_one(query)
        return result.deleted_count > 0
    except Exception as e:
        logger.error(f"MongoDB 删除文档异常: {e}")
        return False 

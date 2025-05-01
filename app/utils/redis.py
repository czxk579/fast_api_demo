import logging
from typing import Any, Optional

import redis

from app.core.config import settings

logger = logging.getLogger(__name__)

# 创建 Redis 连接池
redis_pool = redis.ConnectionPool.from_url(
    url=settings.REDIS_URL, 
    password=settings.REDIS_PASSWORD,
    max_connections=10,
    decode_responses=True
)


def get_redis():
    """
    获取 Redis 客户端实例
    """
    return redis.Redis(connection_pool=redis_pool)


def set_key(key: str, value: Any, expire: Optional[int] = None) -> bool:
    """
    设置 Redis 键值
    """
    try:
        r = get_redis()
        r.set(key, value)
        if expire:
            r.expire(key, expire)
        return True
    except Exception as e:
        logger.error(f"Redis 设置键值异常: {e}")
        return False


def get_key(key: str) -> Any:
    """
    获取 Redis 键值
    """
    try:
        r = get_redis()
        return r.get(key)
    except Exception as e:
        logger.error(f"Redis 获取键值异常: {e}")
        return None


def delete_key(key: str) -> bool:
    """
    删除 Redis 键值
    """
    try:
        r = get_redis()
        r.delete(key)
        return True
    except Exception as e:
        logger.error(f"Redis 删除键值异常: {e}")
        return False 

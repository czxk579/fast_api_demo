import logging
import time
from typing import Any, Dict

from app.core.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, acks_late=True)
def example_task(self, word: str) -> Dict[str, Any]:
    """
    示例 Celery 任务
    """
    logger.info(f"开始处理任务: {self.request.id}")
    time.sleep(5)  # 模拟耗时操作
    logger.info(f"任务 {self.request.id} 完成处理")
    return {"status": "success", "result": f"处理完成: {word}", "task_id": self.request.id}


@celery_app.task(bind=True, acks_late=True)
def test_celery(self, msg: str) -> str:
    """
    测试 Celery 是否正常工作
    """
    logger.info(f"测试任务: {msg}")
    return f"测试任务完成: {msg}" 

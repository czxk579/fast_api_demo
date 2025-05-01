from typing import Any

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException

from app.api import deps
from app.models.user import User
from app.tasks import example as example_tasks

router = APIRouter()


@router.post("/test-celery/")
def test_celery(
    msg: str,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    测试 Celery worker
    """
    task = example_tasks.test_celery.delay(msg)
    return {"msg": "任务已发送", "task_id": task.id}


@router.post("/example-task/")
def run_example_task(
    word: str,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    运行示例任务
    """
    task = example_tasks.example_task.delay(word)
    return {"msg": "任务已发送", "task_id": task.id} 

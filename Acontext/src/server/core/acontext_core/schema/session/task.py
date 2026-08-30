from enum import StrEnum
from pydantic import BaseModel
from typing import Optional
from ..utils import asUUID


class TaskStatus(StrEnum):
    """Used for both Task.status and Message.session_task_process_status.
    DISABLE_TRACKING and LIMIT_EXCEED apply only to messages, not to tasks
    (the tasks table has its own CHECK constraint limited to the first four).
    """

    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    DISABLE_TRACKING = "disable_tracking"
    LIMIT_EXCEED = "limit_exceed"


class TaskData(BaseModel):
    task_description: str
    progresses: Optional[list[str]] = None
    user_preferences: Optional[list[str]] = None


class TaskSchema(BaseModel):
    id: asUUID
    session_id: asUUID

    order: int
    status: TaskStatus
    data: TaskData
    raw_message_ids: list[asUUID]

    def to_string(self) -> str:
        return f"Task {self.order}: {self.data.task_description} (Status: {self.status})"

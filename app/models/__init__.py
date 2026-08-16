from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Annotated, Optional

from pydantic import BaseModel, Field

# Support both pydantic v2 (`ConfigDict`) and v1 (`Config` class)
try:
    from pydantic import ConfigDict  # type: ignore
    _HAS_CONFIGDICT = True
except Exception:
    _HAS_CONFIGDICT = False


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskCreate(BaseModel):
    if _HAS_CONFIGDICT:
        model_config = ConfigDict(extra="forbid")
    else:
        class Config:  # type: ignore[name-defined]
            extra = "forbid"

    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[date] = None
    tags: Annotated[list[str], Field(max_length=5)] = Field(default_factory=list)


class TaskUpdate(BaseModel):
    if _HAS_CONFIGDICT:
        model_config = ConfigDict(extra="forbid")
    else:
        class Config:  # type: ignore[name-defined]
            extra = "forbid"

    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[date] = None
    tags: Annotated[Optional[list[str]], Field(max_length=5)] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: TaskStatus
    priority: TaskPriority
    due_date: Optional[date] = None
    tags: list[str] = Field(default_factory=list)


__all__ = [
    "TaskStatus",
    "TaskPriority",
    "TaskCreate",
    "TaskUpdate",
    "TaskResponse",
]
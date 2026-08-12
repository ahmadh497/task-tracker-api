from __future__ import annotations

from typing import Dict, Optional

from app.models import TaskCreate, TaskResponse, TaskPriority, TaskStatus, TaskUpdate

_tasks: Dict[int, TaskResponse] = {}
_next_id = 1


def reset_storage() -> None:
    global _tasks, _next_id
    _tasks = {}
    _next_id = 1


def add_task(payload: TaskCreate) -> TaskResponse:
    global _next_id

    task = TaskResponse(
        id=_next_id,
        title=payload.title,
        description=payload.description,
        status=payload.status,
        priority=payload.priority,
        due_date=payload.due_date,
        tags=payload.tags.copy(),
    )

    _tasks[task.id] = task
    _next_id += 1

    return task


def get_task_by_id(task_id: int) -> Optional[TaskResponse]:
    return _tasks.get(task_id)


def update_task(task_id: int, payload: TaskUpdate) -> TaskResponse:
    existing = _tasks[task_id]

    updated = TaskResponse(
        id=existing.id,
        title=payload.title or existing.title,
        description=(
            payload.description
            if payload.description is not None
            else existing.description
        ),
        status=payload.status or existing.status,
        priority=(
            payload.priority
            if payload.priority is not None
            else existing.priority
        ),
        due_date=(
            payload.due_date
            if payload.due_date is not None
            else existing.due_date
        ),
        tags=(
            payload.tags.copy()
            if payload.tags is not None
            else existing.tags.copy()
        ),
    )

    _tasks[task_id] = updated

    return updated


def delete_task(task_id: int) -> None:
    del _tasks[task_id]


def get_all_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
) -> list[TaskResponse]:

    tasks = list(_tasks.values())

    if status is not None:
        tasks = [task for task in tasks if task.status == status]

    if priority is not None:
        tasks = [task for task in tasks if task.priority == priority]

    return tasks
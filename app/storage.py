from __future__ import annotations

from typing import Dict, Optional

from app.models import TaskCreate, TaskResponse, TaskPriority, TaskStatus, TaskUpdate

_tasks: Dict[int, TaskResponse] = {}
_next_id = 1


def reset_storage() -> None:
    """Reset the in-memory task store to its initial empty state.

    Args:
        None

    Returns:
        None
    """
    global _tasks, _next_id
    _tasks = {}
    _next_id = 1


def add_task(payload: TaskCreate) -> TaskResponse:
    """Create and store a new task, assigning it the next available id.

    Args:
        payload (TaskCreate): The task data to store.

    Returns:
        TaskResponse: The newly created task.
    """
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
    """Look up a task by its id.

    Args:
        task_id (int): The id of the task to look up.

    Returns:
        Optional[TaskResponse]: The matching task, or None if no task
        exists with that id.
    """
    return _tasks.get(task_id)


def update_task(task_id: int, payload: TaskUpdate) -> TaskResponse:
    """Apply partial updates to an existing task and store the result.

    Args:
        task_id (int): The id of the task to update.
        payload (TaskUpdate): The fields to update. Fields left unset
            (None) keep the existing task's value.

    Returns:
        TaskResponse: The updated task.

    Raises:
        KeyError: If no task exists with the given task_id.
    """
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
    """Remove a task from the store.

    Args:
        task_id (int): The id of the task to delete.

    Returns:
        None

    Raises:
        KeyError: If no task exists with the given task_id.
    """
    del _tasks[task_id]


def get_all_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
) -> list[TaskResponse]:
    """List stored tasks, optionally filtered by status and/or priority.

    Args:
        status (Optional[TaskStatus]): If provided, only tasks with this
            status are included.
        priority (Optional[TaskPriority]): If provided, only tasks with
            this priority are included.

    Returns:
        list[TaskResponse]: The tasks matching the given filters, or all
        stored tasks if neither filter is provided.
    """

    tasks = list(_tasks.values())

    if status is not None:
        tasks = [task for task in tasks if task.status == status]

    if priority is not None:
        tasks = [task for task in tasks if task.priority == priority]

    return tasks
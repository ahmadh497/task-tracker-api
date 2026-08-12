# app/main.py
# Application entry point: creates the FastAPI instance and defines
# the /health endpoint. Run with:
#   uvicorn app.main:app --reload --port 8000

from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from app import storage
from app.business_rules import validate_status_transition
from app.core.config import settings
from app.models import TaskCreate, TaskPriority, TaskResponse, TaskStatus, TaskUpdate
from app.models.health import HealthResponse

# Create the FastAPI application instance.
app = FastAPI(
    title="Task Tracker API",
    description="Educational REST API for tracking tasks, built with FastAPI and JSON file storage.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:5173",
        "null",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)
@app.get("/tasks", response_model=list[TaskResponse], tags=["tasks"])
def list_tasks(
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
) -> list[TaskResponse]:
    return storage.get_all_tasks(status=status, priority=priority)


@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def get_task(task_id: int) -> TaskResponse:
    task = storage.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return task


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, tags=["tasks"])
def create_task(payload: TaskCreate) -> TaskResponse:
    return storage.add_task(payload)


@app.patch("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def update_task(task_id: int, payload: TaskUpdate) -> TaskResponse:
    existing_task = storage.get_task_by_id(task_id)
    if existing_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    if payload.status is not None:
        has_other_changes = (
            payload.title is not None
            or payload.description is not None
            or payload.priority is not None
        )

        if payload.status == existing_task.status and not has_other_changes:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Invalid status transition from {existing_task.status.value} to {payload.status.value}. Allowed transitions: ['todo->in_progress', 'in_progress->done', 'done->in_progress']",
            )
        if payload.status != existing_task.status:
            validate_status_transition(existing_task.status, payload.status)

    return storage.update_task(task_id, payload)


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tasks"])
def delete_task(task_id: int) -> None:
    if storage.get_task_by_id(task_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")

    storage.delete_task(task_id)


@app.get("/health", response_model=HealthResponse, tags=["Health"])
def get_health() -> HealthResponse:
    """
    Health-check endpoint.

    Returns HTTP 200 with the current service status and a UTC timestamp.
    Useful for verifying the server is running and reachable.
    """
    return HealthResponse(
        status="ok",
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


# Allows running this file directly with `python app/main.py` in addition
# to the standard `uvicorn app.main:app` invocation.
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.port, reload=True)

    


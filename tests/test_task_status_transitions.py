from fastapi.testclient import TestClient

from app.main import app
from app import storage
from app.models import TaskCreate, TaskStatus

client = TestClient(app)


def setup_function() -> None:
    storage.reset_storage()


def test_patch_rejects_invalid_status_transition() -> None:
    created = client.post(
        "/tasks",
        json={"title": "Write tests", "description": "Add regression tests", "status": "todo"},
    )
    task_id = created.json()["id"]

    response = client.patch(f"/tasks/{task_id}", json={"status": "todo"})

    assert response.status_code == 422
    assert "Invalid status transition" in response.json()["detail"]


def test_patch_allows_valid_status_transition() -> None:
    created = client.post(
        "/tasks",
        json={"title": "Ship feature", "description": "Deploy changes", "status": "todo"},
    )
    task_id = created.json()["id"]

    response = client.patch(f"/tasks/{task_id}", json={"status": "in_progress"})

    assert response.status_code == 200
    assert response.json()["status"] == TaskStatus.IN_PROGRESS.value

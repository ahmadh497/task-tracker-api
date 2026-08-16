from fastapi.testclient import TestClient

from app.models import TaskStatus


def test_create_task_valid_returns_201_with_full_body(client: TestClient) -> None:
    response = client.post(
        "/tasks",
        json={"title": "New task", "description": "A full task payload", "status": "todo"},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["title"] == "New task"
    assert body["description"] == "A full task payload"
    assert body["status"] == TaskStatus.TODO.value


def test_create_task_missing_title_returns_422(client: TestClient) -> None:
    response = client.post("/tasks", json={})

    assert response.status_code == 422


def test_create_task_blank_title_returns_422(client: TestClient) -> None:
    response = client.post("/tasks", json={"title": ""})

    assert response.status_code == 422


def test_create_task_invalid_priority_returns_422(client: TestClient) -> None:
    response = client.post(
        "/tasks",
        json={"title": "Invalid priority", "priority": "urgent"},
    )

    assert response.status_code == 422


def test_create_task_unknown_field_returns_422(client: TestClient) -> None:
    response = client.post(
        "/tasks",
        json={"title": "Unknown field", "unknown": "value"},
    )

    assert response.status_code == 422


def test_list_tasks_empty_returns_200_and_empty_list(client: TestClient) -> None:
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_status_no_match_returns_200_and_empty_list(client: TestClient, created_task) -> None:
    response = client.get("/tasks", params={"status": "done"})

    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_priority_returns_only_matches(client: TestClient) -> None:
    client.post("/tasks", json={"title": "Low priority", "priority": "low"})
    client.post("/tasks", json={"title": "High priority", "priority": "high"})

    response = client.get("/tasks", params={"priority": "high"})

    assert response.status_code == 200
    assert all(task.get("priority") == "high" for task in response.json())


def test_get_task_by_id_returns_task(client: TestClient, created_task) -> None:
    task_id = created_task["id"]
    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["id"] == task_id


def test_get_task_by_id_not_found_returns_404_with_detail(client: TestClient) -> None:
    response = client.get("/tasks/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Not Found"


def test_patch_partial_update_keeps_other_fields(client: TestClient, created_task) -> None:
    task_id = created_task["id"]
    response = client.patch(
        f"/tasks/{task_id}",
        json={"description": "Updated description"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == task_id
    assert body["title"] == created_task["title"]
    assert body["description"] == "Updated description"
    assert body["status"] == created_task["status"]


def test_patch_same_status_with_other_fields_returns_200(client: TestClient, created_task) -> None:
    task_id = created_task["id"]
    response = client.patch(
        f"/tasks/{task_id}",
        json={"title": "Updated title", "description": "Updated description", "status": created_task["status"]},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == task_id
    assert body["title"] == "Updated title"
    assert body["description"] == "Updated description"
    assert body["status"] == created_task["status"]


def test_patch_not_found_returns_404(client: TestClient) -> None:
    response = client.patch("/tasks/999", json={"status": "done"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_patch_valid_transition_todo_to_inprogress_returns_200(client: TestClient) -> None:
    created = client.post("/tasks", json={"title": "Transition task", "status": "todo"})
    task_id = created.json()["id"]

    response = client.patch(f"/tasks/{task_id}", json={"status": "in_progress"})

    assert response.status_code == 200
    assert response.json()["status"] == TaskStatus.IN_PROGRESS.value


def test_patch_invalid_transition_todo_to_done_returns_422(client: TestClient) -> None:
    created = client.post("/tasks", json={"title": "Invalid transition", "status": "todo"})
    task_id = created.json()["id"]

    response = client.patch(f"/tasks/{task_id}", json={"status": "done"})

    assert response.status_code == 422
    assert "Invalid status transition" in response.json()["detail"]


def test_patch_same_status_returns_422(client: TestClient) -> None:
    created = client.post("/tasks", json={"title": "Same status", "status": "todo"})
    task_id = created.json()["id"]

    response = client.patch(f"/tasks/{task_id}", json={"status": "todo"})

    assert response.status_code == 422
    assert "Invalid status transition" in response.json()["detail"]


def test_patch_invalid_backward_transition_from_in_progress_to_todo_returns_422(client: TestClient) -> None:
    created = client.post("/tasks", json={"title": "Backward transition", "status": "in_progress"})
    task_id = created.json()["id"]

    response = client.patch(f"/tasks/{task_id}", json={"status": "todo"})

    assert response.status_code == 422
    body = response.json()
    assert "Invalid status transition" in body["detail"]
    assert "todo->in_progress" in body["detail"]


def test_delete_existing_returns_204_no_body(client: TestClient, created_task) -> None:
    task_id = created_task["id"]
    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 204
    assert response.content == b""


def test_delete_missing_returns_404(client: TestClient) -> None:
    response = client.delete("/tasks/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Not Found"


def test_create_task_with_due_date_returns_201(client: TestClient) -> None:
    response = client.post(
        "/tasks",
        json={
            "title": "Assignment",
            "description": "Complete project",
            "due_date": "2026-08-15"
        },
    )

    assert response.status_code == 201

    body = response.json()
    assert body["title"] == "Assignment"
    assert body["due_date"] == "2026-08-15"


def test_patch_update_due_date_returns_200(client: TestClient, created_task) -> None:
    task_id = created_task["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"due_date": "2026-09-01"},
    )

    assert response.status_code == 200
    assert response.json()["due_date"] == "2026-09-01"

def test_create_task_invalid_due_date_returns_422(client: TestClient) -> None:
    response = client.post(
        "/tasks",
        json={
            "title": "Invalid Date",
            "due_date": "not-a-date",
        },
    )

    assert response.status_code == 422

def test_get_task_returns_due_date(client: TestClient) -> None:
    created = client.post(
        "/tasks",
        json={
            "title": "API Project",
            "due_date": "2026-10-20",
        },
    )

    task_id = created.json()["id"]

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["due_date"] == "2026-10-20"

def test_create_task_with_tags_returns_tags(client: TestClient) -> None:
    response = client.post(
        "/tasks",
        json={
            "title": "Tagged task",
            "tags": ["frontend", "urgent"],
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["tags"] == ["frontend", "urgent"]


def test_create_task_without_tags_returns_empty_list(client: TestClient) -> None:
    response = client.post(
        "/tasks",
        json={
            "title": "Task without tags",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["tags"] == []


def test_update_task_tags(client: TestClient, created_task) -> None:
    task_id = created_task["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={
            "tags": ["backend", "testing"],
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["tags"] == ["backend", "testing"]


def test_update_task_without_tags_keeps_existing_tags(client: TestClient) -> None:
    created = client.post(
        "/tasks",
        json={
            "title": "Keep tags",
            "tags": ["important", "backend"],
        },
    )

    assert created.status_code == 201

    task_id = created.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={
            "description": "Updated description",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["tags"] == ["important", "backend"]


def test_create_task_with_more_than_five_tags_returns_422(
    client: TestClient,
) -> None:
    response = client.post(
        "/tasks",
        json={
            "title": "Too many tags",
            "tags": [
                "tag1",
                "tag2",
                "tag3",
                "tag4",
                "tag5",
                "tag6",
            ],
        },
    )

    assert response.status_code == 422


def test_update_task_with_more_than_five_tags_returns_422(
    client: TestClient,
    created_task,
) -> None:
    task_id = created_task["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={
            "tags": [
                "tag1",
                "tag2",
                "tag3",
                "tag4",
                "tag5",
                "tag6",
            ],
        },
    )

    assert response.status_code == 422

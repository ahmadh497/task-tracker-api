# Task Tracker Architecture

## 1. What it does

Task Tracker is a small single-process task-board application. A vanilla JavaScript page calls a FastAPI REST API to create, list, retrieve, partially update, and delete tasks; the API also exposes a health check. The board groups tasks by status, supports drag-and-drop status changes, and displays priority, due dates, and tags. The API enables CORS for the project's local-development frontend origins.

The running implementation stores tasks in process memory. Consequently, data is shared by requests to one process but is lost when that process restarts and is not coordinated across multiple workers. Although `README.md` describes JSON file storage, no JSON persistence path is visible in the application files reviewed.

## 2. Data model

The active schemas are Pydantic models in `app/models/__init__.py`:

| Field | Create behavior | Response behavior |
|---|---|---|
| `id` | Assigned by storage | Integer |
| `title` | Required, minimum length 1 | String |
| `description` | Optional, default `null` | String or `null` |
| `status` | Default `todo`; one of `todo`, `in_progress`, `done` | Same enum value |
| `priority` | Default `medium`; one of `low`, `medium`, `high` | Same enum value |
| `due_date` | Optional ISO date | Date or `null` |
| `tags` | List, default empty, at most five on create | List of strings |

`TaskCreate` rejects unknown fields. `TaskUpdate` makes every field optional for PATCH requests, while `TaskResponse` defines the stable API representation. Storage keeps `TaskResponse` objects in a module-level dictionary keyed by an incrementing integer ID.

## 3. Request flow when a user creates a task

1. The browser form in `frontend/index.html` trims the title and description, converts its display values (for example, `ToDo` and `Medium`) to lowercase API enum values, parses comma-separated tags, and sends JSON with `POST /tasks`.
2. FastAPI matches `create_task` in `app/main.py` and validates/deserializes the body as `TaskCreate`. Invalid input produces FastAPI's 422 response before the handler runs.
3. The handler calls `storage.add_task(payload)`.
4. `app/storage.py` builds a `TaskResponse`, assigns `_next_id`, copies the tag list, stores the object in `_tasks`, increments the ID counter, and returns it.
5. FastAPI serializes the declared `TaskResponse` and returns HTTP 201. The frontend normalizes API enums back to display values, prepends the task to local state, and re-renders the board.

## 4. Key files

- `app/main.py` — application construction, CORS, route handlers, HTTP status codes, and response models.
- `app/models/__init__.py` — active task enums and request/response schemas imported by the application.
- `app/storage.py` — in-memory CRUD operations, filtering, and ID allocation.
- `app/business_rules.py` — allowed status transitions for updates: ToDo → InProgress, InProgress → Done, and Done → InProgress.
- `app/models/health.py` — health-response schema.
- `app/core/config.py` — environment-backed application settings used by direct startup.
- `frontend/index.html` — the complete vanilla HTML/CSS/JavaScript board and API client.
- `tests/` — pytest API coverage; the autouse fixture resets in-memory storage around each test.

## 5. Conventions

- Use Python 3.11, FastAPI, Pydantic v2, pytest, and a dependency-free vanilla JavaScript frontend.
- Domain/UI labels are **ToDo**, **InProgress**, and **Done**, with priorities **Low**, **Medium**, and **High**. JSON uses the lowercase enum spellings `todo`, `in_progress`, `done` and `low`, `medium`, `high`.
- Preserve existing response shapes. Keep route-level HTTP concerns in `app/main.py`, validation and serialization in Pydantic schemas, transition policy in `app/business_rules.py`, and persistence operations behind `app/storage.py`.
- Treat storage as ephemeral and single-process; there is no authentication or database in this module.
- Run the service with `uvicorn app.main:app --reload` and verify changes with `pytest -v`.

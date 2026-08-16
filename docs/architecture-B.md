# Task Tracker Architecture — Strategy B: Structured Context

## 1. What it does

Task Tracker is a small FastAPI REST service for creating, listing, retrieving, updating, and deleting tasks. Lists can be filtered by status or priority, and a `/health` endpoint reports service availability. FastAPI also supplies request validation, JSON serialization, and generated OpenAPI documentation. CORS permits the configured local frontend development origins. All task state is held in process memory, so restarting the server clears it; no database, authentication, or file persistence is present.

## 2. Data model

A task response contains an integer `id`, required `title`, optional `description`, `status`, `priority`, optional `due_date`, and a list of `tags`. Create requests require a non-empty title, reject unknown fields, allow at most five tags, and default to status `todo`, priority `medium`, and an empty tag list. Update requests make every field optional and reject unknown fields. Status values are `todo`, `in_progress`, and `done`; priority values are `low`, `medium`, and `high`. The health response contains a status string and an ISO-formatted UTC timestamp.

The active schemas live in `app/models/__init__.py`. A parallel `app/models.py` defines similar schemas but is not imported by the application paths reviewed, because `app.models` resolves to the package.

## 3. Request flow when a user creates a task

1. A client sends `POST /tasks` with JSON.
2. FastAPI parses the body into `TaskCreate`; Pydantic applies defaults and constraints, or FastAPI returns a validation error before the route runs.
3. `create_task` in `app/main.py` passes the validated payload to `storage.add_task`.
4. Storage constructs a `TaskResponse` with the next sequential ID, copies the tags, saves the object in the module-level `_tasks` dictionary, and increments `_next_id`.
5. FastAPI validates/serializes the declared `TaskResponse` and returns HTTP `201 Created`. The new task remains available only for the lifetime of that Python process.

## 4. Key files

| File | Responsibility |
| --- | --- |
| `app/main.py` | FastAPI setup, CORS, HTTP routes, response models, and error mapping. |
| `app/models/__init__.py` | Active task enums and create, update, and response schemas. |
| `app/models/health.py` | Health-check response schema. |
| `app/storage.py` | In-memory CRUD operations, filters, ID allocation, and storage reset. |
| `app/business_rules.py` | Allowed status-transition policy and 422 errors for invalid transitions. |
| `app/core/config.py` | Environment loading and shared application settings. |
| `frontend/index.html` | Separate vanilla JavaScript client entry point. |
| `tests/` | Pytest coverage for health, task CRUD/validation, and status transitions. |

## 5. Conventions

- Run locally with `uvicorn app.main:app --reload`; run verification with `pytest -v`.
- Use Pydantic models at the HTTP boundary and declare FastAPI `response_model` values to preserve response shapes.
- Keep API field values lowercase (`todo`, `in_progress`, `done`; `low`, `medium`, `high`), matching the enums implemented in code.
- Return `404` for missing tasks, `422` for invalid input or status transitions, `201` for creation, and `204` for successful deletion.
- Valid status moves are `todo → in_progress`, `in_progress → done`, and `done → in_progress`; direct moves outside that set are rejected.
- Treat storage as ephemeral and single-process. Module 5 work must not introduce authentication, a database, new dependencies, or application-code edits.

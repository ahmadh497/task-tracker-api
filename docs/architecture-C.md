# Architecture — Strategy C: Targeted Context

## 1. What it does

This is a FastAPI task-tracking API. It exposes endpoints to list tasks (optionally filtered by status and priority), retrieve one task, create, partially update, and delete tasks. It also exposes a health endpoint that returns an `ok` status and a UTC timestamp. The application enables CORS for listed local development origins.

Tasks are held in process memory. Persistence across process restarts, a database, authentication, deployment topology, and frontend behavior are **not visible from the files I read**.

## 2. Data model

- **Status:** `todo`, `in_progress`, or `done`.
- **Priority:** `low`, `medium`, or `high`.
- **Create input (`TaskCreate`):** required non-empty `title`; optional `description` and `due_date`; status defaults to `todo`; priority defaults to `medium`; `tags` defaults to an empty list and accepts at most five items. Extra fields are forbidden.
- **Update input (`TaskUpdate`):** all task fields are optional and extra fields are forbidden. A maximum tag count is not declared on this update model.
- **Response (`TaskResponse`):** integer `id`, title, optional description, status, priority, optional due date, and a tag list.

Date JSON formatting and all validation behavior beyond the constraints declared in these models are **not visible from the files I read**.

## 3. Request flow when a user creates a task

1. A client sends `POST /tasks`.
2. FastAPI parses and validates the request body as `TaskCreate`.
3. The route calls `storage.add_task(payload)`.
4. Storage constructs a `TaskResponse` using the current module-level `_next_id`, copies the input tags, stores the task in the module-level `_tasks` dictionary, and increments `_next_id`.
5. The route returns that task through the declared `TaskResponse` response model with HTTP 201.

Error response shape and behavior outside FastAPI/Pydantic's implied handling are **not visible from the files I read**.

## 4. Key files

- **`app/main.py`:** creates and configures the FastAPI app and CORS middleware; defines task CRUD and health routes; delegates task state operations to storage; invokes an imported status-transition rule during relevant updates.
- **`app/models.py`:** declares status and priority enums plus the create, update, and response Pydantic models.
- **`app/storage.py`:** implements an in-memory task repository, sequential IDs, filtering, updates, deletion, and a reset helper.

The implementations of imported business rules, settings, and the health response model are **not visible from the files I read**.

## 5. Conventions

- Route functions are synchronous and use type annotations.
- FastAPI `response_model` declarations define task and health response contracts.
- Pydantic create/update inputs forbid undeclared fields.
- Optional values use both `Optional[T]` and `T | None`; collections use built-in generic syntax except for the storage dictionary.
- Storage functions exchange Pydantic model instances rather than dictionaries.
- Missing task reads and deletes return HTTP 404; creation returns HTTP 201; deletion returns HTTP 204.
- Status-transition validation is performed in the route layer, while CRUD state changes are delegated to storage.
- IDs are monotonically assigned from 1 until storage is reset.

Concurrency guarantees and broader testing, logging, packaging, and operational conventions are **not visible from the files I read**.

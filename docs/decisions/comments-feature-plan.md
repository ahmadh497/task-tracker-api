# Comments Feature Plan

This plan is grounded in the current repository. The files reviewed were `AGENTS.md`, `app/models.py`, `app/models/__init__.py`, `app/models/health.py`, `app/main.py`, `app/storage.py`, `app/business_rules.py`, `tests/conftest.py`, `tests/test_tasks.py`, `tests/test_task_status_transitions.py`, `tests/test_health.py`, `frontend/index.html`, `README.md`, and representative planning/review documents under `docs/`. There are no separate route modules: `app/main.py` contains all current route declarations.

## 1. Data Model

- Add separate request and response schemas for comments rather than embedding comments in `TaskResponse`. This preserves every existing task response shape, as required by `AGENTS.md`, and follows the existing `TaskCreate`/`TaskResponse` split.
- Define `CommentCreate` with `model_config = ConfigDict(extra="forbid")`, following `TaskCreate`, and these client-supplied fields:
  - `author: str = Field(..., min_length=1, max_length=100)`
  - `body: str = Field(..., min_length=1, max_length=2000)`
- Define `CommentResponse` with `id: str`, `task_id: str`, `author: str`, `body: str`, and timezone-aware `created_at: datetime`. Generate `id` on the server with `str(uuid4())`, and generate `created_at` with `datetime.now(timezone.utc)`; the health route already establishes the repository's UTC-aware timestamp pattern.
- Do not accept `id`, `task_id`, or `created_at` in `CommentCreate`; the nested route supplies the parent task and the server supplies identity and time.
- Put the active schemas in `app/models/__init__.py`, because `from app.models import ...` currently resolves to that package. Before implementation, resolve or document the duplicate definitions in `app/models.py` and `app/models/__init__.py`; changing only `app/models.py` would not affect current imports.

## 2. API Routes

- Add `POST /tasks/{task_id}/comments`, returning `201` and `CommentResponse`. The handler should first use `storage.get_task_by_id(task_id)` and return `404` when the task is absent, then delegate creation to storage. This follows the existing nested validation style of the task `PATCH`/`DELETE` handlers and the existing `POST /tasks` response-model/status-code declaration pattern.
- Add `GET /tasks/{task_id}/comments`, returning `200` and `list[CommentResponse]` in deterministic creation order (oldest first). Check task existence first so a missing task returns `404`, while a known task with no comments returns `[]`. This follows `GET /tasks`, which uses a typed list response and returns an empty list when there are no resources.
- Keep the path parameter typed as `int` to match existing task routes and storage keys. Populate the required string `CommentResponse.task_id` with `str(task_id)` without changing `TaskResponse.id`; this preserves existing task API shapes while meeting the requested comment contract.
- Use the existing `tags=["tasks"]` grouping unless the team decides comments warrant their own OpenAPI tag.
- Do not add update or delete routes in this increment; they are outside the requested create/list scope and their authorization/audit semantics are unresolved.

## 3. Tests

- Add `tests/test_comments.py` using the injected `client: TestClient` and `created_task` fixtures from `tests/conftest.py`, matching the dominant test style in `tests/test_tasks.py`.
- Cover successful creation: `201`, a parseable UUID string, string `task_id`, echoed author/body, and a parseable timezone-aware UTC `created_at` value.
- Cover successful listing: an existing task with no comments returns `200`/`[]`; multiple comments for one task are returned oldest first; comments from another task are excluded.
- Parameterize request validation cases for missing, empty, and over-limit `author`; missing, empty, and over-limit `body`; and unknown fields. Expect FastAPI/Pydantic `422`, following existing invalid-task tests.
- Verify server ownership by attempting to submit `id`, `task_id`, or `created_at` and expecting `422` because extras are forbidden.
- Verify both create and list return `404` for a nonexistent task, including the exact agreed error detail.
- Extend the storage-reset fixture behavior (through `storage.reset_storage()`) so comments cannot leak between tests, then add a regression test that demonstrates reset clears comments and UUID generation does not depend on task integer sequencing.
- Run the complete `pytest -v` suite so the new routes do not change existing task or health behavior.

## 4. Frontend Changes

- Extend each task card built in `renderBoard` with a comments control and count, following the card's existing programmatic DOM construction and click-handler pattern used by the Edit button.
- On expansion, fetch `GET /tasks/{task.id}/comments`; maintain per-task comment loading/error/ready state separately from the board's global `boardState` so a comment failure does not replace the entire board.
- Render each comment's author, body, and a localized timestamp. Assign user content with `textContent`, as the current task title, description, and tags do, rather than interpolating it into `innerHTML`.
- Add an inline form with required author input (`maxlength="100"`) and body textarea (`maxlength="2000"`). On submit, trim for usability, call `POST /tasks/{task.id}/comments`, surface FastAPI errors in an `aria-live` status element, append the returned comment, and clear the body only after success.
- Prevent comment controls and form interactions from initiating the card's drag behavior (for example, stop propagation and disable dragging during text interaction), following the Edit button's existing event isolation.
- Add responsive styles in the existing `<style>` block and accessible labels, focus handling, loading text, empty state, and retry behavior in the same single-file vanilla JavaScript architecture. No frontend build dependency is needed.

## 5. Migration or Storage Notes

- The observed implementation is process-local in-memory storage (`_tasks` plus `_next_id`) even though the README and FastAPI description call it JSON file storage. No database or on-disk persistence layer is present in the files reviewed.
- Add an in-memory comment collection keyed by existing integer task ID (for example, `Dict[int, list[CommentResponse]]`). Keep `task_id` serialized as a string only at the comment model boundary. This follows `_tasks` while avoiding scans across unrelated tasks.
- Generate comment UUIDs independently of `_next_id`; preserve insertion order in each task's list to satisfy the API ordering contract.
- Update `reset_storage()` to clear task and comment collections together, following the autouse isolation fixture.
- Update `delete_task()` to remove that task's comments in the same storage operation so in-memory orphan comments cannot remain. Document and test this cascade even though comment deletion is not exposed as a route.
- No migration script is required for the current ephemeral store, and Module 5 explicitly prohibits adding a database or dependency. Restarting the server will continue to lose tasks and comments.
- If repository documentation is corrected later to introduce actual JSON persistence, define serialization for UUID strings and UTC ISO 8601 datetimes plus backward-compatible loading for task records without comments before changing storage.

## 6. Open Questions

- Should missing-task comment routes use the existing `"Not Found"` detail from task GET/DELETE or `"Task not found"` from task PATCH? The repository is inconsistent, so the desired contract is not visible in the reviewed files.
- Does `task_id: string` intentionally differ from the existing integer task ID? This plan preserves task shapes by stringifying the integer in comment responses; confirm that interpretation before implementation.
- Should whitespace-only author/body values be rejected? Pydantic `min_length` accepts strings containing only spaces unless trimming or an additional validator is specified.
- Should list order be oldest-first as proposed, newest-first, or explicitly queryable/paginated? No comment-volume or ordering requirement is present.
- Are comments immutable, or will edit/delete endpoints be a later feature? No lifecycle beyond create/list was specified.
- What should deleting a task do to its comments? This plan proposes cascade deletion because the current storage has no useful orphan-comment access path, but the requirement does not state the policy.
- Should the UI remember an author during the browser session, and should comments load eagerly or only when expanded?
- Should timestamps be emitted as `+00:00` (the health endpoint's current pattern) or normalized to a trailing `Z`? Both represent UTC, but exact response formatting is unspecified.
- The requested feature says `task_id` is a string but does not specify whether it is client-visible only or also the internal storage key; confirm the boundary choice above.

## 7. My Critique

### Data Model

- I agree with using separate CommentCreate and CommentResponse models because it keeps server-generated fields out of client input and preserves the existing TaskResponse shape.
- The duplicate definitions in app/models.py and app/models/__init__.py should be resolved or clearly documented before implementation because the active imports currently use the package version.

### API Routes

- POST and GET comment routes are enough for the first increment because edit and delete behavior was not part of the requested feature.
- Before implementation, I would standardize the missing-task error detail and confirm that comments should be returned oldest first.

### Tests

- The proposed tests cover the main success cases, validation, task isolation, and missing-task behavior well.
- I would also add a test confirming that deleting a task removes its comments and add whitespace-only validation tests if the project decides those values should be rejected.

### Frontend Changes

- I agree with loading comments inside each task card because it fits the existing board without requiring a new page or framework.
- I would keep comments lazy-loaded when the user expands them so the first version stays simple and does not make unnecessary API requests.

### Migration or Storage Notes

- The proposed dictionary keyed by task ID fits the existing in-memory storage design and is appropriate for the current course scope.
- The README saying JSON storage while the application actually uses in-memory storage should be corrected separately because documentation should match the running implementation.

### Open Questions

- Before implementation I would resolve the task_id string versus integer contract, comment ordering, whitespace validation, missing-task error text, and task-deletion cascade behavior.
- Authentication and comment ownership would also need decisions before a production version, but adding authentication is outside the current course scope.

## Generic vs Repo-Grounded Codex Comparison

**Biggest difference:** The generic plan described the usual components of a comments feature, while the repo-grounded plan identified actual project constraints such as in-memory storage, existing FastAPI route patterns, current pytest fixtures, the single-file frontend, and the duplicate model definitions.

**Plan I would hand to a teammate:** I would hand the repo-grounded plan to a teammate after resolving the open API-contract questions because it tells them which existing files and patterns the implementation should follow.

**Where the generic plan was still useful:** The generic plan was useful as an initial checklist for the data model, routes, tests, storage, and frontend work before examining the repository.

**Where repo grounding mattered most:** Repo grounding mattered most for identifying the active model location, preserving existing response shapes, following the current test fixtures, matching the in-memory storage design, and respecting the Module 5 restrictions.

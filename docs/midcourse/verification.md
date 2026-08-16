# Verification

## Baseline / regression check

The project was verified from:

`C:\Users\pc\Desktop\task-tracker-api`

The pytest suite collected 33 tests. During feature work, one tag-validation test initially failed because six tags returned `201` instead of the required `422`. After correcting backend validation, the complete suite passed:

```text
33 passed
```

Final Git checkpoint:

```text
On branch mid-course-project
nothing to commit, working tree clean
```

Commit:

```text
675c472 Complete mid-course project features
```

## Backend test results

Final result:

```text
33 passed
```

The suite covered health checks, task behavior, and status transitions.

The important failing case was:

```text
test_create_task_with_more_than_five_tags_returns_422
Expected: 422
Received: 201
```

The backend was corrected and the full suite was rerun successfully.

## Manual browser checks

### Due dates
- Created a task with a due date.
- Confirmed the due date is displayed on the task card.
- Edited a task and confirmed its due date can be changed.
- Used `Overdue Tasks` to filter the board.
- Confirmed completed tasks are excluded from overdue logic.

### Tags
- Entered comma-separated tags.
- Confirmed tags are trimmed and empty entries ignored.
- Confirmed the five-tag limit is communicated.
- Edited a task and loaded its existing tags.
- Tested more than five tags and confirmed the operation is rejected.

## Behavior contract — before vs after

| Behavior | Before | After |
|---|---|---|
| Due date | Not part of the task workflow | Optional due date can be created/edited/displayed |
| Overdue filter | Not available | `All Tasks` / `Overdue Tasks` |
| Completed task with past due date | No explicit rule | Not overdue |
| Tags | Not part of the task workflow | Comma-separated tags, max five |
| More than five tags | Not correctly rejected | API returns `422`; UI blocks submission |
| Status transitions | Existing rules | Preserved |

## Break-test evidence

A break test starts from working code with a passing test, temporarily introduces a regression, confirms that the same test fails, then restores the working code and confirms that the test passes again. The temporary broken changes below were not committed.

### Break Test 1 — Five-tag validation

Test used:

```text
tests/test_tasks.py::test_create_task_with_more_than_five_tags_returns_422
```

#### 1. Working code — test passes

With the normal five-tag validation in place, I ran:

```powershell
python -m pytest tests/test_tasks.py::test_create_task_with_more_than_five_tags_returns_422 -v
```

Result:

```text
tests/test_tasks.py::test_create_task_with_more_than_five_tags_returns_422 PASSED [100%]

1 passed in 0.03s
```

#### 2. Temporary break

The working model contained:

```python
tags: Annotated[list[str], Field(max_length=5)] = Field(default_factory=list)
```

I temporarily removed the maximum-count validation:

```python
tags: list[str] = Field(default_factory=list)
```

This temporary change was not committed.

#### 3. Same test against broken code — test fails

I reran the exact same pytest test.

Result:

```text
tests/test_tasks.py::test_create_task_with_more_than_five_tags_returns_422 FAILED [100%]

>       assert response.status_code == 422
E       assert 201 == 422
E        +  where 201 = <Response [201 Created]>.status_code

FAILED tests/test_tasks.py::test_create_task_with_more_than_five_tags_returns_422 - assert 201 == 422
1 failed in 0.22s
```

This shows that the test detects a regression where more than five tags are incorrectly accepted.

#### 4. Restore working code — test passes again

I restored `app/models/__init__.py` with:

```powershell
git restore app/models/__init__.py
```

Then I reran the same test.

Result:

```text
tests/test_tasks.py::test_create_task_with_more_than_five_tags_returns_422 PASSED [100%]

1 passed in 0.04s
```

### Break Test 2 — Due-date persistence

Test used:

```text
tests/test_tasks.py::test_create_task_with_due_date_returns_201
```

#### 1. Working code — test passes

With the normal due-date persistence behavior in place, I ran:

```powershell
python -m pytest tests/test_tasks.py::test_create_task_with_due_date_returns_201 -v
```

Result:

```text
tests/test_tasks.py::test_create_task_with_due_date_returns_201 PASSED [100%]

1 passed in 0.03s
```

#### 2. Temporary break

The working storage code contained:

```python
due_date=payload.due_date,
```

I temporarily changed it to:

```python
due_date=None,
```

This intentionally caused newly created tasks to lose their supplied due date. The temporary change was not committed.

#### 3. Same test against broken code — test fails

I reran the exact same pytest test.

Result:

```text
tests/test_tasks.py::test_create_task_with_due_date_returns_201 FAILED [100%]

>       assert body["due_date"] == "2026-08-15"
E       AssertionError: assert None == '2026-08-15'

FAILED tests/test_tasks.py::test_create_task_with_due_date_returns_201 - AssertionError: assert None == '2026-08-15'
1 failed in 0.25s
```

This shows that the test detects a regression where the API accepts a due date but fails to preserve it in the created task.

#### 4. Restore working code — test passes again

I restored `app/storage.py` with:

```powershell
git restore app/storage.py
```

Then I reran the same test.

Result:

```text
tests/test_tasks.py::test_create_task_with_due_date_returns_201 PASSED [100%]

1 passed in 0.05s
```

Both break tests therefore demonstrate the required pattern: working code passes, a temporary intentional regression makes the same test fail, and restoring the working code makes the test pass again.

## Final checklist

- [x] Complete pytest suite passed: 33 passed
- [x] Frontend integrated in `frontend/index.html`
- [x] Due-date and overdue behavior verified
- [x] Tags workflow verified
- [x] Break Test 1 completed with pass → intentional failure → restored pass evidence
- [x] Break Test 2 completed with pass → intentional failure → restored pass evidence
- [x] Branch is `mid-course-project`
- [x] Working tree was restored after both temporary break tests

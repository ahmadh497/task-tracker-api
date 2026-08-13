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

### Break Test 1 — More than five tags

Input:

```text
tag1, tag2, tag3, tag4, tag5, tag6
```

Required result: `422`.

The test initially caught the defect:

```text
assert response.status_code == 422
E assert 201 == 422
```

After validation was added, the test passed as part of the final `33 passed` suite.

### Break Test 2 — Invalid status transition

The existing status-transition tests protect the workflow from arbitrary status jumps. The frontend checks `VALID_TRANSITIONS` before sending a move request, and the backend transition tests provide regression protection.

Relevant test file:

```text
tests/test_task_status_transitions.py
```

## Final checklist

- [x] Complete pytest suite passed: 33 passed
- [x] Frontend integrated in `frontend/index.html`
- [x] Due-date and overdue behavior verified
- [x] Tags workflow verified
- [x] Five-tag break case fixed
- [x] Status-transition regression checks passed
- [x] Branch is `mid-course-project`
- [x] Working tree is clean
- [x] Final commit exists: `675c472`

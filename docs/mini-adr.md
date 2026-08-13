# Mini ADR — Due Dates/Overdue Filter and Tags

**Status:** Accepted

## Context

The Task Tracker already supported task creation, editing, priorities, descriptions, status transitions, and a board UI. Two small features were selected: **Due Dates + Overdue Filter** and **Tags / Labels**.

The backend uses a FastAPI-style API with pytest tests. The frontend uses a single `frontend/index.html` file with embedded JavaScript.

## Decision

### Due Dates + Overdue Filter

Due dates remain optional. The frontend sends `due_date`, displays it on task cards, and provides an `Overdue Tasks` filter.

The overdue rule is:
- no due date → not overdue
- past due date + not Done → overdue
- Done → not overdue

The filter is calculated from the tasks already loaded by the board, avoiding an unnecessary new API endpoint.

### Tags / Labels

Tags are a simple list of strings attached to each task. The frontend accepts comma-separated values, trims whitespace, ignores empty entries, and enforces a maximum of five tags. The backend also enforces the five-tag limit.

## Alternatives rejected

- **Separate tag management:** rejected as unnecessary database/UI complexity.
- **Backend overdue endpoint:** rejected because the current board already has the task data needed for this simple rule.
- **Automatic status changes when overdue:** rejected because overdue is a time property, not a workflow status.
- **Unlimited tags:** rejected because the acceptance requirement establishes a five-tag limit.

## Review decisions

AI suggestions were treated as proposals. I corrected the duplicate tags input and explicitly defined that completed tasks are not overdue. I also relied on backend tests rather than assuming frontend validation was sufficient.

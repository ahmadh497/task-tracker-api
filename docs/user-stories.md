# User Stories

## Feature 1 — Due Dates + Overdue Filter

### Story 1 — Add a due date
**As a user, I want to assign a due date to a task so that I know when it should be completed.**

**Acceptance criteria**
- The task form provides a date input for the due date.
- A task can be created with or without a due date.
- The due date is sent to the API as `due_date`.
- An existing task's due date can be edited.

### Story 2 — Display due dates
**As a user, I want to see a task's due date on the task card so that I can understand its deadline without opening the task.**

**Acceptance criteria**
- Tasks with a due date display a `Due ...` badge.
- Tasks without a due date do not display an empty badge.
- The date is displayed in a readable format.

### Story 3 — Identify overdue tasks
**As a user, I want overdue unfinished tasks to be clearly marked so that I can prioritize them.**

**Acceptance criteria**
- A task is overdue when its due date is before today.
- A task with no due date is not overdue.
- A completed (`Done`) task is not marked overdue even if its due date is past.
- An overdue task displays an `Overdue` badge.

### Story 4 — Filter overdue tasks
**As a user, I want to filter the board to overdue tasks so that I can focus on work that is late.**

**Acceptance criteria**
- The filter contains `All Tasks` and `Overdue Tasks`.
- `All Tasks` shows all tasks.
- `Overdue Tasks` shows only overdue tasks.
- Changing the filter does not change task data.

**AI assumption corrected:** I explicitly excluded `Done` tasks from the overdue calculation. A past date alone does not make a completed task overdue.

## Feature 2 — Tags / Labels

### Story 1 — Add tags
**As a user, I want to add tags to a task so that I can categorize related work.**

**Acceptance criteria**
- The form provides one tags input.
- Tags are entered as comma-separated values.
- Whitespace is trimmed.
- Empty entries are ignored.

### Story 2 — Limit tags
**As a user, I want a clear tag limit so that task metadata stays manageable.**

**Acceptance criteria**
- A task can contain at most five tags.
- More than five tags are rejected by the API with HTTP `422`.
- More than five tags are rejected by the UI before submission.
- The UI explains the five-tag limit.

### Story 3 — Preserve tags when editing
**As a user, I want existing tags to appear when I edit a task so that I can update them without re-entering everything.**

**Acceptance criteria**
- Existing tags populate the tags input during editing.
- Tags are represented as comma-separated text.
- Saving sends the updated tag list to the API.

### Story 4 — Keep tags simple
**As a user, I want tags to remain lightweight labels rather than a separate management system.**

**Acceptance criteria**
- Tags remain task metadata.
- No separate tag-management page or permissions system is required.

**AI assumption corrected:** AI-generated frontend markup contained duplicate tags inputs. I reviewed the form and kept one tags field. I also kept the five-tag rule in both frontend and backend validation.

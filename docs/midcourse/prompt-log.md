# AI Prompt Log

Long transcripts are omitted; these entries preserve the task, the useful AI response, and the decision.

## Feature 1 — Due Dates + Overdue Filter

### Prompt 1
> Choose two features for the Task Tracker project and write the steps we will do for each feature.

**AI returned:** A staged plan covering backend, tests, frontend, manual verification, break tests, and documentation.

**Decision:** Accepted the small-iteration workflow.

### Prompt 2 — Weak prompt rewritten
**Weak:** `make the due date feature work`

**Stronger:**
> Implement optional due dates and an overdue filter in the existing Task Tracker. A task is overdue only when its due date is before today and its status is not Done. Add tests and integrate the existing frontend without changing status-transition rules.

**AI returned:** A more precise implementation approach and an explicit overdue rule.

**Decision:** Accepted the rule and rejected automatic status changes.

### Prompt 3
> Check the existing index.html and show where the due-date field, overdue calculation, filter, createTask, saveTask, and rendering changes belong.

**AI returned:** Locations in the embedded JavaScript and HTML form.

**Decision:** Accepted the locations but reviewed the actual file before editing.

## Feature 2 — Tags / Labels

### Prompt 1
> Implement tags/labels with a maximum of five tags and make sure the backend test for more than five tags returns 422.

**AI returned:** Backend validation plus frontend parsing/validation.

**Decision:** Accepted validation at both boundaries. The test suite exposed the missing backend rule.

### Prompt 2
> This is index.html. Check if the tags field is correct and tell me if there is a duplicated tags field.

**AI returned:** It identified two tags inputs in the form.

**Decision:** Accepted the finding and removed the duplicate.

### Prompt 3
> Where is the second/duplicated tags field? Which line should I remove?

**AI returned:** The location and surrounding markup of the second tags field.

**Decision:** Accepted the targeted edit rather than replacing the whole form.

### Prompt 4
> Run the tests and help me fix any failing test without changing unrelated behavior.

**AI returned:** The six-tag test expected `422` but received `201`.

**Decision:** Accepted the backend validation fix. The final suite reached `33 passed`.

# Reflection

I used AI mainly as a coding and review assistant during the Task Tracker feature work. I used it to break the work into small steps, inspect the existing frontend structure, suggest backend validation, locate JavaScript functions inside the embedded script in `index.html`, and interpret pytest failures. I did not treat generated code as automatically correct; I compared suggestions with the existing project and used the test suite as the main verification mechanism.

One moment when AI helped significantly was the failing tags test. The suite reported that creating a task with six tags returned HTTP `201`, while the acceptance requirement expected `422`. This made the missing backend validation clear. After adding the five-tag constraint and rerunning pytest, all 33 tests passed. AI was also useful for explaining where functions such as `createTask()` and `saveTask()` were located because the application does not have a separate JavaScript file.

One moment when AI slowed the work down was frontend integration. Because the JavaScript is embedded inside `index.html`, generated changes could affect several parts of the same file. I had to inspect the existing HTML carefully rather than replacing large sections blindly. This was especially important when the tags field appeared twice in the generated form.

My review changed the result in several places. For due dates, I kept the rule that a completed task is not overdue even when its date is in the past. I rejected unnecessary complexity such as a separate tag-management system and automatic status changes based on dates. For tags, I removed the duplicated input and kept one clear comma-separated field with a maximum of five tags. I also kept validation on both the frontend and backend so the API cannot accept more than five tags just because a request bypasses the browser.

The main lesson was that AI was most useful when combined with small changes, explicit acceptance criteria, and automated tests. The final implementation was not accepted simply because AI suggested it; it was accepted when the behavior matched the requirements and the regression suite passed.

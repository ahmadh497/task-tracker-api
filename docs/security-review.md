# Security Review

## AI Findings

| Severity | File:Line | Finding | Suggested Fix | Grade | Reason |
|---|---|---|---|---|---|
| High | `app/main.py:36-86` | Task read, create, update, and delete endpoints have no authentication or authorization, so any client that can reach the API can access or modify every task. | Before production use, add authentication and enforce authorization for each task operation; for Module 5, retain this as an unfixed backlog item rather than changing the application. | Correct | I verified that the task routes do not require authentication or authorization. This is acceptable for the course scope but would be a risk in production. |
| Medium | `app/models/__init__.py:38-39,53-54` | User-controlled title and description fields have no maximum length, allowing oversized request bodies and stored values to consume excessive memory and degrade responses. | Add explicit, documented maximum lengths to create and update schemas and enforce an overall request-body limit at the deployment boundary. | Correct | I verified that title and description do not define maximum-length constraints. |
| Medium | `app/models/__init__.py:43,58` | The five-tag limit is enforced during creation but not during updates, so a PATCH request can bypass the intended resource limit. | Apply the same maximum-list-length constraint to `TaskUpdate.tags` and add a regression test for updates with more than five tags. | Correct | I verified that TaskCreate limits tags to five but TaskUpdate uses an unrestricted optional list. |
| Medium | `app/main.py:30` | CORS permits the opaque `null` origin, which can allow requests from sandboxed documents or local files that are not one of the explicitly trusted frontend origins. | Remove `null` unless it is required for a documented local workflow; otherwise use a narrowly scoped development-only CORS configuration. | Correct | I verified that `null` is included in the configured CORS origins. It supports local development but should be reconsidered before production. |
| Low | `app/main.py:108` | Running the module directly binds to all interfaces with auto-reload enabled, exposing a development server and reloader beyond localhost. | Bind development runs to localhost and disable reload by default; enable external binding or reload only through explicit development configuration. | Correct | I verified that direct execution uses host `0.0.0.0` and `reload=True`. The Docker startup command does not use reload, so this risk applies to direct development execution. |

## My Manual Findings

| Severity | File:Line | Finding | Suggested Fix | Reason |
|---|---|---|---|---|
| Low | `app/models/__init__.py` | Task titles can still be empty or whitespace-only during some update requests because TaskUpdate does not enforce a minimum length or trimming. | Apply consistent title validation to both create and update schemas and add tests for empty and whitespace-only titles. | I found this while comparing the create and update validation rules manually. |

## Reconciliation

### Agreement

I independently checked the repository and agreed with the five AI findings. The code evidence supports each finding, although the missing authentication is an intentional course-scope decision rather than something I should add during Module 5.

### AI-only

The CORS `null` origin and the direct-development Uvicorn configuration were details the AI surfaced that I had not initially identified during my own review.

### You-only

I identified inconsistent title validation between task creation and task updates. An update can accept values that should be rejected if the project requires titles to remain non-empty.

## Top 3 Unfixed Backlog

| Rank | Finding | Severity | Owner | Next Step |
|---|---|---|---|---|
| 1 | No authentication or authorization on task routes | High | Project maintainer | Define authentication and authorization requirements before any production deployment. |
| 2 | TaskUpdate does not enforce the five-tag limit | Medium | Project maintainer | Add the same tag constraint used by TaskCreate and add a regression test. |
| 3 | Title and description have no maximum lengths | Medium | Project maintainer | Define reasonable length limits and add validation tests before production use. |

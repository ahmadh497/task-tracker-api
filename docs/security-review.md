# Security Review

## AI Findings

| Severity | File:Line | Finding | Suggested Fix | Grade | Reason |
|---|---|---|---|---|---|
| High | `app/main.py:36-86` | Task read, create, update, and delete endpoints have no authentication or authorization, so any client that can reach the API can access or modify every task. | Before production use, add authentication and enforce authorization for each task operation; for Module 5, retain this as an unfixed backlog item rather than changing the application. | TODO | TODO |
| Medium | `app/models/__init__.py:38-39,53-54` | User-controlled title and description fields have no maximum length, allowing oversized request bodies and stored values to consume excessive memory and degrade responses. | Add explicit, documented maximum lengths to create and update schemas and enforce an overall request-body limit at the deployment boundary. | TODO | TODO |
| Medium | `app/models/__init__.py:43,58` | The five-tag limit is enforced during creation but not during updates, so a PATCH request can bypass the intended resource limit. | Apply the same maximum-list-length constraint to `TaskUpdate.tags` and add a regression test for updates with more than five tags. | TODO | TODO |
| Medium | `app/main.py:30` | CORS permits the opaque `null` origin, which can allow requests from sandboxed documents or local files that are not one of the explicitly trusted frontend origins. | Remove `null` unless it is required for a documented local workflow; otherwise use a narrowly scoped development-only CORS configuration. | TODO | TODO |
| Low | `app/main.py:108` | Running the module directly binds to all interfaces with auto-reload enabled, exposing a development server and reloader beyond localhost. | Bind development runs to localhost and disable reload by default; enable external binding or reload only through explicit development configuration. | TODO | TODO |

## My Manual Findings

| Severity | File:Line | Finding | Suggested Fix | Reason |
|---|---|---|---|---|

## Reconciliation

### Agreement

### AI-only

### You-only

## Top 3 Unfixed Backlog

| Rank | Finding | Severity | Owner | Next Step |
|---|---|---|---|---|

# Final AI Review and Ownership Evidence

## AGENTS.md Guardrails

- Repo-specific stack and commands included: yes
- Docs-first/read-first guardrail included: yes
- Unexpected app/frontend edits rule included: yes
- The guardrails require read-only analysis first, diff review, and avoiding application changes during review/governance work unless explicitly approved.

## AI Code Review Mini-Log

Changed file reviewed: `Dockerfile`

| AI comment | Grade: Useful / Noise / Wrong | Reason | Verification or decision |
|---|---|---|---|
| Running the application as a dedicated non-root user is safer than leaving the runtime container as root. | Useful | The Dockerfile creates an `app` user and switches to it with `USER app`. | Kept the configuration and verified that the built container ran successfully. |
| The `/health` HEALTHCHECK is useful because it verifies the API itself instead of only checking whether the process exists. | Useful | A running Uvicorn process does not guarantee that the HTTP endpoint is responding correctly. | Kept the health check and verified Docker reported the container as `healthy` and `/health` returned HTTP 200. |
| The runtime image is appropriately scoped because it copies the virtual environment and `app/` instead of copying the complete repository. | Useful | Tests, documentation, Git metadata, and local environment files are not required by the running API. | Checked the Dockerfile and `.dockerignore`; the image built and ran successfully. |

## AI Security Mini-Review

| Finding | File evidence | Grade: Valid / False Positive / Noise | Reason | Next action |
|---|---|---|---|---|
| Task routes have no authentication or authorization. | `app/main.py` task routes | Valid | The create, read, update, and delete routes do not require authentication. This is acceptable for the course scope but would be a production risk. | Keep as a backlog item; do not add authentication in this final project because it is outside the allowed scope. |
| `TaskUpdate.tags` does not enforce the same five-tag limit as `TaskCreate.tags`. | `app/models/__init__.py` | Valid | Task creation limits the tag list to five, while task updates accept an unrestricted optional list. | Add consistent validation and a regression test before production use. |
| CORS allows the `null` origin. | `app/main.py` CORS configuration | Valid | The `null` origin is broader than the explicit localhost development origins and should be reconsidered for production. | Keep for the current development workflow; remove or narrow it before a production deployment. |

## Manual Security Check

I manually compared the create and update validation models. I found that `TaskCreate.title` has a minimum-length constraint, while `TaskUpdate.title` is only an optional string and does not apply the same validation. This means title validation is not fully consistent between creation and updates. I recorded it as a future validation improvement rather than changing application behavior during the final review.

## One AI Output I Rejected or Corrected

The AI security review suggested adding authentication and authorization because the task endpoints are open. I agreed that this would matter for a production system, but I rejected implementing that suggestion in this final project because the course instructions explicitly say not to add authentication as a new product feature. I kept the finding in the security backlog instead of blindly applying the suggested fix.

## Three AI Usage Rules

1. Never paste: passwords, API keys, access tokens, real credentials, private customer data, or production data.
2. Always verify: inspect the generated diff and run the relevant tests or runtime checks before accepting AI-assisted work.
3. Record AI contributions by: keeping important AI-assisted decisions in project documentation and preserving the related changes in Git history.

## Protected App/Frontend Note

The application-code change recorded in commit `1579e71` was documentation-only: docstrings were added to existing functions in `app/business_rules.py`, `app/main.py`, and `app/storage.py` without intentionally changing application behavior. No comments, authentication, database, notification system, or other new product feature was implemented.

## Ownership Statement

I am comfortable submitting this repository as my own work because I reviewed the AI-assisted changes instead of accepting them automatically. I ran the full pytest suite, built and ran the Docker image, checked `/health`, and manually verified the frontend Kanban create and edit flows. I also checked AI security findings against the repository and rejected suggestions that were outside the course scope. I understand the final changes and can explain the commands, configuration choices, and evidence included in this submission.

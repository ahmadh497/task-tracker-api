# Governance Retrospective - AI-Assisted Coding

## What I Shared With AI

| Item | Module | Risk Level | Reason |
|---|---|---|---|
| Task Tracker code | 2-5 | Low | This is course project code with no credentials, customer data, or production information. |
| Test output and stack traces | 2-4 | Medium | The output was non-sensitive, but stack traces can expose local paths and internal implementation details. |
| Frontend code | 3 | Low | The frontend is course project code and does not contain private user or production data. |
| Dockerfile and CI YAML | 4 | Low | These files contain build and test configuration only and do not contain real credentials or secrets. |
| Any real external data I used by mistake | N/A | Low | I did not intentionally provide real customer, production, financial, health, or other sensitive external data to AI tools. |

## What I Received From AI

| Generated Thing | Module | Do I Understand It Line by Line? | Action |
|---|---|---|---|
| Backend models and validators | 2 | Mostly | I reviewed the code and validation behavior and verified it with tests before keeping it. |
| Frontend board and drag-and-drop logic | 3 | Mostly | I reviewed the JavaScript and manually tested the main task board interactions. |
| CI workflow | 4 | Yes | I reviewed each workflow step and verified that it installs dependencies and runs the test suite. |
| Dockerfile | 4 | Yes | I reviewed each Docker stage, the non-root user, health check, exposed port, and startup command. |
| Security findings and plans | 5 | Yes | I compared the AI findings with the repository and kept them as review and backlog evidence rather than blindly changing application behavior. |
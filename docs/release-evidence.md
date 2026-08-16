# Release Evidence

## Baseline

- Branch: `final-project`
- Date: 2026-08-16
- Local app run command: `uvicorn app.main:app --reload --port 8000`
- `/health` result: `HTTP/1.1 200 OK` with JSON status `"ok"`.
- Frontend check: Opened `frontend/index.html` from VS Code using Live Server. The Task Tracker Kanban board rendered successfully, and the create and edit flows worked.
- Test command: `python -m pytest -v`
- Test result: `33 passed in 0.32s`

## CI Evidence

- Workflow file: `.github/workflows/ci.yml`
- Latest successful run: `https://github.com/ahmadh497/task-tracker-api/actions/runs/31946666251`
- Result: GitHub Actions completed successfully on commit `1e912d5`.
- Test command used by CI: `pytest -v --tb=short`
- Python version: `3.11`
- Dependency installation: `pip install -r requirements.txt`
- Shortcut check: no `continue-on-error`, no `|| true`, and pytest is not skipped.

## Docker Evidence

- Build command: `docker build -t task-tracker:final .`
- Build result: successful.
- Run command: `docker run --rm -d -p 8000:8000 --name tt-final task-tracker:final`
- `/health` check: `curl.exe -i http://localhost:8000/health`
- `/health` result: `HTTP/1.1 200 OK`
- Docker health status: `healthy`
- Non-root check: the Dockerfile creates an `app` user with UID/GID 1000 and runs the container with `USER app`.
- No-baked-secrets check: `.dockerignore` excludes `.env` and `.env.*`, and the Dockerfile copies only `requirements.txt` and the `app/` directory into the image.
- Runtime command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

## Documentation Claim-vs-Reality Log

| Claim checked | Evidence used | Result | Change made, if any |
|---|---|---|---|
| README said the application used JSON file storage. | Compared README with `app/storage.py`, which stores tasks in an in-memory dictionary. | Incorrect documentation. | Updated README to say the application uses in-memory storage and that tasks are lost when the process restarts. |
| The `/health` endpoint should respond successfully. | Ran the Docker container and called `curl.exe -i http://localhost:8000/health`. | Confirmed: returned `HTTP/1.1 200 OK` with status `"ok"`. | No change required. |
| CI should install dependencies and run the full pytest suite. | Checked `.github/workflows/ci.yml` and the latest successful GitHub Actions run. | Confirmed: Python 3.11 is configured, dependencies are installed, and pytest runs successfully. | Updated the workflow so CI runs on all pushes and pull requests. |
| The Docker image should run the API without baking `.env` values into the image. | Checked `Dockerfile`, `.dockerignore`, and successfully built and ran the image. | Confirmed. | No change required. |

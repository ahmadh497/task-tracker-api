# Task Tracker API

An educational REST API for tracking tasks, built with Python and FastAPI using in-memory storage instead of a database. Tasks are lost when the server process restarts. It demonstrates core backend concepts including request validation, routing, status-transition rules, and API design with a minimal, easy-to-read technology stack.

## Setup

### 1. Create a virtual environment and install dependencies

**Linux / macOS**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows (PowerShell)**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Configure environment variables

```bash
cp .env.example .env
```
(On Windows: `copy .env.example .env`)

### 3. Start the server

```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`, with interactive docs at `http://localhost:8000/docs`.

### 4. Test the health endpoint

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "ok",
  "timestamp": "2026-07-25T10:15:30.123456+00:00"
}
```

## Running Tests

```bash
pytest
```
## Final Project

Branch reviewed: `final-project`

### What this submission demonstrates

- The existing Task Tracker still runs inside the intended course scope.
- CI runs the pytest suite on push and pull request.
- The Docker image builds and runs with `/health` returning HTTP 200.
- AI review, security, release, and ownership evidence is stored in `docs/`.

### How to run locally

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Open `frontend/index.html` from VS Code using Live Server to view the Kanban board.

### How to run tests

```powershell
python -m pytest -v
```

### How to run with Docker

Build the image:

```powershell
docker build -t task-tracker:final .
```

Run the container:

```powershell
docker run --rm -d -p 8000:8000 --name tt-final task-tracker:final
```

Check the health endpoint:

```powershell
curl.exe -i http://localhost:8000/health
```

Stop the container:

```powershell
docker stop tt-final
```

### Evidence files

- `docs/release-evidence.md`
- `docs/final-ai-review.md`
- `docs/ai-playbook.md`

### AI assistance summary

AI helped draft or review CI, Docker configuration, documentation, security findings, and release checks.

I verified the work by reviewing diffs, running the full pytest suite, building and running the Docker image, checking `/health`, and manually testing the frontend Kanban create and edit flows.

One AI suggestion I rejected was adding authentication and authorization during the final project. Although it would matter for production security, authentication is outside the allowed final-project scope, so I recorded it as a backlog item instead of implementing it.

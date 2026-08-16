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
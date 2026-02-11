# Cloud-Native Workflow Automation Backend (MVP)

A beginner-friendly Flask backend that lets you:
- Create workflows (a workflow is a list of steps)
- List workflows
- Run a workflow (simulated execution)
- View run status and step-by-step logs

## Folder structure
```
workflow-backend/
  app/
    main.py
    db.py
    models.py
  requirements.txt
  Dockerfile
  .dockerignore
  README.md
```

## Run locally (VS Code terminal)

### 1) Create & activate venv
**Windows (PowerShell)**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Mac/Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Install deps
```bash
pip install -r requirements.txt
```

### 3) Start server
```bash
python app/main.py
```

Server: http://127.0.0.1:5000

Health check:
- GET `/health`

> The SQLite DB file will be created automatically in the project root as `workflow.db`.

## Quick API test (copy/paste)

### Create a workflow
```bash
curl -X POST http://127.0.0.1:5000/workflows \
  -H "Content-Type: application/json" \
  -d '{"name":"Data Cleanup","steps":["Validate input","Clean rows","Save output"]}'
```

### List workflows
```bash
curl http://127.0.0.1:5000/workflows
```

### Run workflow (replace 1 with your workflow id)
```bash
curl -X POST http://127.0.0.1:5000/workflows/1/run
```

### Get run logs (replace 1 with your run_id)
```bash
curl http://127.0.0.1:5000/runs/1
```

## Run with Docker (optional)
```bash
docker build -t workflow-backend .
docker run -p 5000:5000 workflow-backend
```

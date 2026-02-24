# Cloud-Native Backend Service for Enterprise Workflow Automation

A modular, production-grade backend service built with **Python** and **Flask**, designed to automate enterprise workflows through clean RESTful APIs, structured logging, and Docker containerization.

---

## Project Structure

```
workflow-backend/
├── app.py                   # App entry point, blueprint registration
├── config.py                # Environment configuration
├── logger.py                # Structured JSON logging
├── requirements.txt         # Python dependencies
├── Dockerfile               # Container configuration
├── routes/
│   ├── workflow.py          # Workflow execution & status APIs
│   └── data.py              # Data ingestion & retrieval APIs
└── services/
    ├── workflow_service.py  # Workflow business logic
    └── data_service.py      # Data processing logic
```

---

## Features

- **RESTful API Design** — clean, modular endpoints for workflow automation and data ingestion
- **Workflow Engine** — supports pluggable action steps: `validate`, `transform`, `notify`, `aggregate`
- **Data Ingestion** — normalizes, timestamps, and tags incoming records by source
- **Structured JSON Logging** — every action logged with timestamp and level for cloud observability
- **Error Handling** — all endpoints return meaningful HTTP status codes (200, 201, 400, 404, 422, 500)
- **Dockerized** — fully containerized for consistent local and cloud deployments
- **Cloud-Native Design** — loose coupling, service isolation, ready for container orchestration

---

## Tech Stack

- **Language:** Python 3.11
- **Framework:** Flask 3.0
- **Containerization:** Docker
- **Architecture:** Microservices, RESTful API, Service Layer Pattern

---

## Getting Started

### Run Locally

```bash
pip install -r requirements.txt
python app.py
```

### Run with Docker

```bash
docker build -t workflow-backend .
docker run -p 5000:5000 workflow-backend
```

Server starts at: `http://localhost:5000`

---

## API Endpoints

### Health Check
```
GET /health
```
Response:
```json
{"status": "ok", "service": "workflow-automation-backend"}
```

---

### Execute a Workflow
```
POST /api/workflow/execute
```
Request body:
```json
{
  "workflow_id": "wf-001",
  "steps": [
    { "action": "validate", "params": { "rules": ["not_null"] } },
    { "action": "transform", "params": { "row_count": 100 } },
    { "action": "notify", "params": { "channel": "email" } }
  ]
}
```

---

### Check Workflow Status
```
GET /api/workflow/status/<workflow_id>
```

---

### Ingest Data
```
POST /api/data/ingest
```
Request body:
```json
{
  "source": "excel-addin",
  "records": [
    { "Name": "Aditi", "Score": 95 },
    { "Name": "John", "Score": 88 }
  ]
}
```

---

### Retrieve Records
```
GET /api/data/records?source=excel-addin
```

---

## Design Decisions

- **Service Layer Pattern** — business logic lives in `services/`, routes only handle HTTP concerns
- **Structured Logging** — JSON format with timestamps for cloud monitoring tools (IBM Cloud, AWS CloudWatch)
- **Modular Blueprints** — each feature is an independent Blueprint, easy to scale or replace
- **Config Class** — environment-aware configuration, easy to extend for dev/staging/prod

---

## Author

**Aditi Nitin Shardul**  
Master's in Computer and Information Science — Syracuse University  
[LinkedIn](https://www.linkedin.com/in/YOUR_LINKEDIN)

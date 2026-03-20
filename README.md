# EXP System Dashboard — Backend

The FastAPI backend for the EXP System Dashboard. Handles AI usage logging, dashboard statistics, GitHub language detection, and AI activity analysis.

---

## 🛠 Tech Stack

- **FastAPI**
- **Uvicorn**
- **Python `requests`** library
- **GitHub REST API**

---

## 📁 Project Structure
```
src/backend/ai-monitoring/
├── router.py       # All API route definitions
├── run.py          # Uvicorn server entry point
└── app.py          # FastAPI app factory (create_app)
```

---

## ⚙️ Installation

**1. Navigate to the backend directory:**
```bash
cd src/backend/ai-monitoring
```

**2. Create and activate a virtual environment (recommended):**
```bash
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Mac/Linux
```

**3. Install dependencies:**
```bash
pip install fastapi uvicorn requests
```

---

## 🏃 Running the Server
```bash
python run.py
```

Server runs on: `http://127.0.0.1:8000`

> ⚠️ Always use `python run.py` — NOT `python -m flask run` or `uvicorn` directly, as environment variables may not load correctly.

---

## 🔌 API Endpoints

### Health Check
```
GET /api/
```
Returns:
```json
{ "message": "server is working" }
```

---

### AI Logs

**Get all logs:**
```
GET /api/ai-logs
```
Returns:
```json
[
  {
    "user": "Samuel",
    "feature": "JavaScript",
    "success": true,
    "timestamp": "2026-03-20T10:00:00"
  }
]
```

**Add a log:**
```
POST /api/ai-logs
```
Body:
```json
{
  "user": "Samuel",
  "feature": "JavaScript",
  "success": true
}
```
Returns:
```json
{ "message": "Log added", "log": { ... } }
```

---

### Dashboard Stats
```
GET /api/dashboard-stats
```
Returns:
```json
{
  "total_logs": 15,
  "successful": 12,
  "failed": 3
}
```

---

### GitHub Stats
```
GET /api/github-stats?username=devbysamcloudy
```
Returns:
```json
{
  "username": "devbysamcloudy",
  "total_repos": 12,
  "languages": {
    "JavaScript": 5,
    "Python": 3,
    "TypeScript": 2
  }
}
```

---

### AI Detection
```
GET /api/ai-detection
```
Returns:
```json
{
  "languages": { "JavaScript": 8, "Python": 4 },
  "success_rates": {
    "JavaScript": { "success": 6, "fail": 2 }
  },
  "most_active": "JavaScript",
  "total_logs": 12
}
```

---

## 📝 Example `router.py`
```python
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from datetime import datetime
import requests as req

router = APIRouter()
ai_logs = []

@router.get("/api/dashboard-stats")
def dashboard_stats():
    return {
        "total_logs": len(ai_logs),
        "successful": sum(1 for log in ai_logs if log["success"]),
        "failed": sum(1 for log in ai_logs if not log["success"]),
    }
```

---

## 📝 Example `run.py`
```python
from app import create_app
import uvicorn

app = create_app()

if __name__ == "__main__":
    uvicorn.run("run:app", host="0.0.0.0", port=8000, reload=True)
```

---

## ⚠️ Important Notes

- All logs are stored **in-memory** — they reset when the server restarts
- For production, replace the in-memory `ai_logs` list with a database (PostgreSQL, Supabase, etc.)
- The GitHub API has rate limits — authenticated requests allow more calls per hour
- CORS is enabled for all origins in development — restrict in production

---

## 🔧 CORS Configuration

In `app.py`, CORS is configured to allow the React frontend:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🚀 Production Deployment

For production deployment:

1. Replace in-memory storage with a database
2. Set up environment variables for sensitive config
3. Use a production WSGI server like **Gunicorn** with Uvicorn workers:
```bash
gunicorn run:app -w 4 -k uvicorn.workers.UvicornWorker
```

4. Update the frontend `BASE_URL` in `apiservices.js` to your production URL

---

## 👥 Team

- **Samuel Nganga** — Frontend, AI API Integration, Team Lead
- **Partner** — Backend, FastAPI, Project Architecture

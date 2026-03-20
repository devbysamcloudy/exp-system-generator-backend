from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from datetime import datetime
import requests as req

router = APIRouter()

ai_logs = []

@router.get("/api/")
def home():
    return {"message": "server is working"}

@router.get("/api/github-stats")
def github_stats(username: str = None):
    if not username:
        return JSONResponse({"error": "Username required"}, status_code=400)

    try:
        repos_res = req.get(
            f"https://api.github.com/users/{username}/repos",
            timeout=10,
            headers={"User-Agent": "exp-system-app"}
        )

        if repos_res.status_code != 200:
            return JSONResponse({"error": "GitHub user not found"}, status_code=404)

        repos = repos_res.json()

        language_count = {}
        for repo in repos:
            lang = repo.get("language")
            if lang:
                language_count[lang] = language_count.get(lang, 0) + 1

        top_languages = sorted(language_count.items(), key=lambda x: x[1], reverse=True)

        return {
            "username": username,
            "total_repos": len(repos),
            "languages": dict(top_languages),
        }
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@router.get("/api/ai-logs")
def get_logs():
    return ai_logs

@router.post("/api/ai-logs")
async def add_log(request: Request):
    data = await request.json()

    if not all(k in data for k in ("user", "feature", "success")):
        return JSONResponse({"error": "Missing fields"}, status_code=400)

    log_entry = {
        "user": data["user"],
        "feature": data["feature"],
        "success": data["success"],
        "timestamp": datetime.utcnow().isoformat()
    }
    ai_logs.append(log_entry)
    return {"message": "Log added", "log": log_entry}

@router.get("/api/dashboard-stats")
def dashboard_stats():
    return {
        "total_logs": len(ai_logs),
        "successful": sum(1 for log in ai_logs if log["success"]),
        "failed": sum(1 for log in ai_logs if not log["success"]),
    }

@router.get("/api/ai-detection")
def ai_detection():
    if not ai_logs:
        return {"message": "No logs yet", "languages": {}, "most_active": None}

    # Count usage per language/feature
    language_usage = {}
    for log in ai_logs:
        feature = log.get("feature")
        if feature:
            language_usage[feature] = language_usage.get(feature, 0) + 1

    # Success rate per language
    language_success = {}
    for log in ai_logs:
        feature = log.get("feature")
        if feature:
            if feature not in language_success:
                language_success[feature] = {"success": 0, "fail": 0}
            if log["success"]:
                language_success[feature]["success"] += 1
            else:
                language_success[feature]["fail"] += 1

    # Most active language
    most_active = max(language_usage, key=language_usage.get) if language_usage else None

    return {
        "languages": language_usage,
        "success_rates": language_success,
        "most_active": most_active,
        "total_logs": len(ai_logs),
    }
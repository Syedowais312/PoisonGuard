from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database.storage import (
    save_log,
    load_logs
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/log")
async def log_result(data: dict):

    saved_log = save_log(data)

    print("\nNEW LOG RECEIVED:")
    print(saved_log)

    return {
        "message": "logged",
        "log": saved_log
    }
@app.get("/logs")
async def get_logs():

    return load_logs()


@app.get("/blocked")
async def get_blocked():

    logs = load_logs()

    return [
        log for log in logs
        if log["status"] == "BLOCKED"
    ]


@app.get("/safe")
async def get_safe():

    logs = load_logs()

    return [
        log for log in logs
        if log["status"] == "SAFE"
    ]


@app.get("/stats")
async def get_stats():

    logs = load_logs()

    total = len(logs)

    blocked = len([
        log for log in logs
        if log["status"] == "BLOCKED"
    ])

    safe = len([
        log for log in logs
        if log["status"] == "SAFE"
    ])

    return {

        "total_documents": total,

        "blocked_documents": blocked,

        "safe_documents": safe,

        "attack_rate": (
            blocked / total * 100
            if total > 0 else 0
        )
    }

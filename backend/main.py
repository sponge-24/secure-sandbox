from fastapi import FastAPI
from pydantic import BaseModel
import uuid
import redis
import json
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

# Connect to Redis
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

app = FastAPI(title="Code Runner API")

# Allow requests from your frontend
origins = [
    "http://localhost:5173",  # React dev server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # allow GET, POST, OPTIONS, etc.
    allow_headers=["*"],
)

# ---- Request Body Schema ----
class CodeRequest(BaseModel):
    code: str
    lang: str = "python"  # default to python for now


# ---- API Endpoints ----

@app.post("/run")
def run_code(payload: CodeRequest):
    """Submit code for execution"""
    job_id = str(uuid.uuid4())
    job = {
        "id": job_id,
        "code": payload.code,
        "lang": payload.lang
    }
    # Push job into Redis queue
    r.lpush("job_queue", json.dumps(job))

    # Mark job as pending
    r.set(f"status:{job_id}", "pending")

    return {"job_id": job_id}


@app.get("/status/{job_id}")
def get_status(job_id: str):
    """Check the status of a submitted job"""
    status = r.get(f"status:{job_id}")
    if not status:
        return {"status": "unknown"}
    return {"status": status}


@app.get("/result/{job_id}")
def get_result(job_id: str):
    """Fetch the result of a completed job"""
    result = r.get(f"result:{job_id}")
    status = r.get(f"status:{job_id}")

    if not status:
        return {"status": "unknown", "output": None}

    if status == "pending":
        return {"status": "pending", "output": None}

    return {"status": "done", "output": result}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

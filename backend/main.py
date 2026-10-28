# backend/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from orchestrator import run_pipeline

app = FastAPI(title="AI Job Application Assistant")

# Allow React frontend to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request model ────────────────────────────────────────────────────────────
class ApplicationRequest(BaseModel):
    cv_text:  str
    job_url:  Optional[str] = None
    job_text: Optional[str] = None


# ── Routes ───────────────────────────────────────────────────────────────────
@app.get("/")
def root():
    return {"status": "AI Job Application Assistant is running ✅"}


@app.post("/apply")
def apply(request: ApplicationRequest):
    # Validate — need at least one job input
    if not request.job_url and not request.job_text:
        raise HTTPException(
            status_code=400,
            detail="Provide either a job_url or job_text."
        )

    if not request.cv_text.strip():
        raise HTTPException(
            status_code=400,
            detail="CV text cannot be empty."
        )

    try:
        result = run_pipeline(
            cv_text=request.cv_text,
            job_url=request.job_url,
            job_text=request.job_text,
        )
        return {"success": True, "data": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
"""
routers/validate.py — POST /validate and GET /status/{job_id}
"""

import uuid
import asyncio
from fastapi import APIRouter, BackgroundTasks, HTTPException
from utils.models import IdeaInput, ValidationResult, JobStatusResponse
from agents.pipeline import run_pipeline, job_store

router = APIRouter(prefix="/api", tags=["validation"])


@router.post("/validate", response_model=JobStatusResponse, status_code=202)
async def validate_idea(idea: IdeaInput, background_tasks: BackgroundTasks):
    """
    Accept a startup idea, kick off the 10-stage pipeline in the background,
    and immediately return a job_id for polling.
    """
    job_id = str(uuid.uuid4())

    # Initialise the job entry
    job_store[job_id] = ValidationResult(
        job_id=job_id,
        idea_name=idea.idea_name,
        status="processing",
        stage=1,
        stage_label="Receiving idea",
    )

    # Run pipeline in background
    background_tasks.add_task(run_pipeline, job_id, idea.model_dump())

    return JobStatusResponse(
        job_id=job_id,
        status="processing",
        stage=1,
        stage_label="Receiving idea",
    )


@router.get("/status/{job_id}", response_model=JobStatusResponse)
async def get_status(job_id: str):
    """Poll the current pipeline status for a job."""
    if job_id not in job_store:
        raise HTTPException(status_code=404, detail="Job not found")

    job = job_store[job_id]
    return JobStatusResponse(
        job_id=job_id,
        status=job.status,
        stage=job.stage,
        stage_label=job.stage_label,
        result=job if job.status == "done" else None,
        error=job.error,
    )

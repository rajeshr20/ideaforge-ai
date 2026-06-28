"""
routers/report.py — GET /report/{job_id}  — stream PDF download
"""

import os
from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter(tags=["report"])
REPORTS_DIR = Path(os.getenv("REPORTS_DIR", "reports"))


@router.get("/report/{job_id}")
async def download_report(job_id: str):
    """Download the generated PDF validation report."""
    pdf_path = REPORTS_DIR / f"{job_id}.pdf"
    if not pdf_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Report not found. The validation may still be processing."
        )
    return FileResponse(
        path=str(pdf_path),
        media_type="application/pdf",
        filename="IdeaForge_Validation_Report.pdf",
    )

"""
main.py — IdeaForge AI Backend
FastAPI application entry point.

Run with:
    uvicorn main:app --reload --port 8000
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from routers.validate import router as validate_router
from routers.report import router as report_router

load_dotenv()

app = FastAPI(
    title="IdeaForge AI",
    description="AI-powered startup idea validation platform",
    version="1.0.0",
)

# ── CORS ─────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        os.getenv("FRONTEND_ORIGIN", "http://localhost:5173"),
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(validate_router)
app.include_router(report_router)


@app.get("/")
async def root():
    return {"message": "IdeaForge AI API is running", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "ok"}


# ── __init__ files ────────────────────────────────────────────────────────────
import pathlib
for pkg in ["agents", "rag", "routers", "utils"]:
    init = pathlib.Path(f"{pkg}/__init__.py")
    init.parent.mkdir(exist_ok=True)
    if not init.exists():
        init.write_text("")

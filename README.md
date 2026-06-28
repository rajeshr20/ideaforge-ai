# IdeaForge AI 🚀

AI-powered startup idea validation platform. Enter your idea, get a full validation report in minutes.

## Features
- 10-stage agentic pipeline (LangChain + Gemini)
- Market research, competitor analysis, SWOT, feasibility, scoring
- RAG with FAISS for grounded market insights
- Validation score (0–100) with breakdown
- MVP roadmap generation
- PDF report download
- React frontend + FastAPI backend

## Project Structure
```
ideaforge/
├── backend/
│   ├── main.py                  # FastAPI app entry point
│   ├── requirements.txt
│   ├── .env.example
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base_agent.py        # Base agent class
│   │   ├── idea_processor.py    # Stage 2: Idea processing
│   │   ├── market_research.py   # Stage 3: Market research
│   │   ├── competitor.py        # Stage 4: Competitor analysis
│   │   ├── feasibility.py       # Stage 5: Feasibility & risk
│   │   ├── swot.py              # Stage 6: SWOT analysis
│   │   ├── business_model.py    # Stage 7: Business model
│   │   ├── scorer.py            # Stage 8: Validation scoring
│   │   ├── roadmap.py           # Stage 9: Roadmap generation
│   │   └── pipeline.py          # Orchestrates all 10 stages
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── indexer.py           # Build FAISS index from docs
│   │   └── retriever.py         # RAG retrieval helper
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── validate.py          # POST /validate endpoint
│   │   └── report.py            # GET /report/{id} PDF endpoint
│   └── utils/
│       ├── __init__.py
│       ├── pdf_generator.py     # ReportLab PDF builder
│       └── models.py            # Pydantic models
├── frontend/
│   ├── package.json
│   ├── index.html
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── index.css
│       ├── components/
│       │   ├── IdeaForm.jsx     # Multi-step input form
│       │   ├── ProgressBar.jsx  # Pipeline stage tracker
│       │   ├── ScoreCard.jsx    # Validation score display
│       │   ├── SwotTable.jsx    # SWOT 2x2 grid
│       │   ├── RoadmapCard.jsx  # MVP roadmap timeline
│       │   └── ReportButton.jsx # PDF download button
│       ├── pages/
│       │   ├── Home.jsx         # Landing + form
│       │   └── Results.jsx      # Full results dashboard
│       └── hooks/
│           └── useValidation.js # API call + polling hook
```

## Quick Start

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env              # Add your GEMINI_API_KEY
python -m uvicorn main:app --reload --port 8000
```

### RAG Index (run once)
```bash
cd backend
python -m rag.indexer             # Builds FAISS index from sample docs
```

### Frontend
```bash
cd frontend
npm install
npm run dev                       # Runs on http://localhost:5173
```

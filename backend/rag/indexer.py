"""
rag/indexer.py

Run this once to build the FAISS vector index from your knowledge base documents.

Usage:
    python -m rag.indexer

Place your market research PDFs / text files in rag/docs/
The script will chunk, embed, and save the FAISS index to rag/faiss_index/
"""

import os
import json
from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

DOCS_DIR = Path(__file__).parent / "docs"
INDEX_DIR = Path(__file__).parent / "faiss_index"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ─── Fallback seed documents (used if rag/docs/ is empty) ───────────────────
SEED_DOCS = [
    {
        "content": """
India's startup ecosystem is the third largest in the world with over 100,000 startups.
The Indian SaaS market is expected to reach $50 billion by 2030, growing at 25% CAGR.
Key sectors: Fintech (UPI driving 8 billion monthly transactions), Edtech (BYJU's, Unacademy),
Healthtech, Agritech, and B2B SaaS.
Tier-2 and Tier-3 cities are the new growth frontier for consumer startups.
""",
        "source": "India Startup Ecosystem Report 2024",
    },
    {
        "content": """
Fintech India: Digital payments volume crossed ₹125 lakh crore in FY2024.
BNPL (Buy Now Pay Later) growing at 40% YoY. Neo-banking startups raised $2.1B in 2023.
Key pain points: credit access for underbanked, SMB lending, cross-border remittances.
Competitors in neobanking: Jupiter, Fi Money, Niyo, RazorpayX.
Regulatory environment: RBI sandbox program helps fintech pilots.
""",
        "source": "Indian Fintech Market Analysis 2024",
    },
    {
        "content": """
Edtech India market size: $6 billion in 2024, projected $30 billion by 2030.
Post-pandemic reset: B2B edtech (upskilling, corporate training) growing faster than K-12.
Key trends: vernacular content, bite-sized learning, AI tutors, skill-based certifications.
Pain points: low course completion rates (~15%), high CAC, affordability in tier-2/3 cities.
Players: BYJU's, Unacademy, Coursera India, Scaler, Newton School.
""",
        "source": "Indian Edtech Landscape 2024",
    },
    {
        "content": """
Healthtech India: $10 billion market growing at 20% CAGR.
Telemedicine adopted by 60 million users post-COVID. 
Key segments: diagnostics, teleconsultation, mental health, insurance (insurtech).
Pain points: doctor shortage (1:1400 ratio vs WHO recommended 1:1000), 
rural healthcare access, health record fragmentation.
Key players: Practo, PharmEasy, Mfine, 1mg, Healthifyme.
""",
        "source": "Indian Healthtech Market Report 2024",
    },
    {
        "content": """
B2B SaaS India: 1,500+ SaaS companies, $3.5B ARR collectively.
India serves as a global SaaS hub — 60% revenue from exports (US, EU).
Key verticals: HR tech, sales enablement, developer tools, supply chain.
Typical SaaS CAC in India: $200-800 for SMBs. LTV:CAC ratio target: 3:1 minimum.
Funding environment: Series A average $5M, Series B $20M.
Notable exits: Freshworks (NASDAQ), Zoho (bootstrapped), Postman.
""",
        "source": "India B2B SaaS Report 2024",
    },
    {
        "content": """
Agritech India: 55% of Indian population is dependent on agriculture.
$30B market opportunity; only 1% of farmers use digital tools.
Key pain points: price discovery, access to credit, supply chain inefficiency, weather risk.
Key players: DeHaat, Ninjacart, AgroStar, Jivabhumi.
Government support: PM-KISAN, AgriStack data initiative.
Drone-based crop monitoring growing 3x YoY.
""",
        "source": "Indian Agritech Landscape 2024",
    },
    {
        "content": """
E-commerce India: $70B market, expected to reach $350B by 2030.
Quick commerce (10-minute delivery) growing at 70% YoY — Blinkit, Zepto, Swiggy Instamart.
Social commerce and live commerce emerging trends.
D2C brands: 800+ funded D2C brands in India.
Key challenges: logistics last-mile, return rates (25-35% in fashion), unit economics.
Key players: Flipkart, Amazon India, Meesho (social commerce), Nykaa (beauty D2C).
""",
        "source": "Indian E-commerce & D2C Report 2024",
    },
    {
        "content": """
Venture capital and startup funding India 2024:
Total funding: $8B in FY2024 (down from $24B in FY2022 peak).
Funding winter easing: Q4 2023 saw 30% uptick vs Q4 2022.
Most funded sectors: Fintech, SaaS, Consumer tech, Climate tech.
Angel/pre-seed: ₹25L–1Cr typical cheque size.
Key accelerators: Y Combinator India cohort, Sequoia Surge, 100X.VC, NASSCOM 10k.
First time founders: average 8 months to raise seed round.
""",
        "source": "India Startup Funding Landscape 2024",
    },
]


def build_index():
    """Build and save the FAISS index."""
    print("Building FAISS index...")

    # Load from docs directory if it exists and has files
    documents = []
    if DOCS_DIR.exists():
        for file in DOCS_DIR.glob("*.txt"):
            text = file.read_text(encoding="utf-8")
            documents.append(Document(page_content=text, metadata={"source": file.name}))
        for file in DOCS_DIR.glob("*.md"):
            text = file.read_text(encoding="utf-8")
            documents.append(Document(page_content=text, metadata={"source": file.name}))

    # Add seed documents
    for doc in SEED_DOCS:
        documents.append(Document(
            page_content=doc["content"].strip(),
            metadata={"source": doc["source"]}
        ))

    print(f"  Loaded {len(documents)} documents")

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=50, separators=["\n\n", "\n", ". ", " "]
    )
    chunks = splitter.split_documents(documents)
    print(f"  Created {len(chunks)} chunks")

    # Embed and build index
    print("  Embedding chunks (this may take a minute on first run)...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = FAISS.from_documents(chunks, embeddings)

    # Save index
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(INDEX_DIR))
    print(f"  Index saved to {INDEX_DIR}")
    return vectorstore


if __name__ == "__main__":
    build_index()
    print("Done! RAG index is ready.")

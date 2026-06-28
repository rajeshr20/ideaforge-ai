"""
rag/retriever.py

Loads the FAISS index and provides semantic retrieval for agent prompts.
Auto-builds the index on first run if it doesn't exist.
"""

import os
from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

INDEX_DIR = Path(__file__).parent / "faiss_index"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


class RAGRetriever:
    _instance = None
    _vectorstore = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def _load_or_build(self):
        if self._vectorstore is not None:
            return

        if not INDEX_DIR.exists():
            print("FAISS index not found. Building it now...")
            from rag.indexer import build_index
            self._vectorstore = build_index()
        else:
            embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
            self._vectorstore = FAISS.load_local(
                str(INDEX_DIR),
                embeddings,
                allow_dangerous_deserialization=True
            )
            print("FAISS index loaded.")

    def retrieve(self, query: str, k: int = 3) -> str:
        """
        Retrieve the top-k most relevant document chunks for a query.
        Returns them concatenated as a single string.
        """
        self._load_or_build()
        docs = self._vectorstore.similarity_search(query, k=k)
        if not docs:
            return ""
        return "\n\n".join(
            f"[{doc.metadata.get('source', 'Source')}]\n{doc.page_content}"
            for doc in docs
        )

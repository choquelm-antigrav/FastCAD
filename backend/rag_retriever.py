"""RAG retriever — embed query → ChromaDB similarity search (T-203)"""

from __future__ import annotations

from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from backend.ingest import _COLLECTION_NAME, _EMBED_MODEL

_model: SentenceTransformer | None = None


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(_EMBED_MODEL)
    return _model


def retrieve(
    query: str,
    chroma_path: Path,
    top_k: int = 5,
) -> list[dict]:
    """
    Retrieve the top-k most relevant chunks for a query.

    Returns
    -------
    list of {content, source_file, page_number, score}
    Ordered by descending similarity score (distance inverted to score).
    """
    client = chromadb.PersistentClient(path=str(chroma_path))
    collection = client.get_or_create_collection(name=_COLLECTION_NAME)

    embedding = _get_model().encode([query], show_progress_bar=False).tolist()

    results = collection.query(
        query_embeddings=embedding,
        n_results=min(top_k, collection.count() or 1),
        include=["documents", "metadatas", "distances"],
    )

    chunks: list[dict] = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        chunks.append(
            {
                "content": doc,
                "source_file": meta["source_file"],
                "page_number": meta["page_number"],
                "score": round(1.0 - dist, 4),
            }
        )

    return chunks

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
        # all-MiniLM-L6-v2 produces unit vectors; ChromaDB returns L2 distance.
        # cosine_similarity = 1 - L2² / 2  (exact for normalized embeddings)
        cosine_sim = max(0.0, 1.0 - (dist ** 2) / 2.0)
        chunks.append(
            {
                "content": doc,
                "source_file": meta["source_file"],
                "page_number": meta["page_number"],
                "score": round(cosine_sim, 4),
            }
        )

    return chunks


def get_all_chunks(chroma_path: Path) -> list[dict]:
    """Return all stored chunks with their embeddings."""
    client = chromadb.PersistentClient(path=str(chroma_path))
    collection = client.get_or_create_collection(name=_COLLECTION_NAME)
    if collection.count() == 0:
        return []
    result = collection.get(include=["documents", "metadatas", "embeddings"])
    chunks = []
    for id_, doc, meta, emb in zip(
        result["ids"], result["documents"], result["metadatas"], result["embeddings"]
    ):
        chunks.append({
            "id": id_,
            "content": doc,
            "source_file": meta.get("source_file", ""),
            "page_number": meta.get("page_number", 0),
            "ingested_at": meta.get("ingested_at", ""),
            "embedding": emb,
        })
    return chunks

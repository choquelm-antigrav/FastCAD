"""Tests — backend/rag_retriever.py (T-206)"""

import pytest
from pathlib import Path
import chromadb
from unittest.mock import patch
import numpy as np

from backend.rag_retriever import retrieve


@pytest.fixture
def populated_chroma(tmp_path: Path):
    """In-memory-like ChromaDB with two pre-embedded chunks."""
    chroma_path = tmp_path / "chroma_db"
    chroma_path.mkdir()

    client = chromadb.PersistentClient(path=str(chroma_path))
    collection = client.get_or_create_collection("catscript_knowhow")

    collection.add(
        ids=["id1", "id2"],
        embeddings=[[0.1] * 384, [0.9] * 384],
        documents=["chunk about CATScript", "chunk about EKL"],
        metadatas=[
            {"source_file": "doc1.pdf", "page_number": 1},
            {"source_file": "doc2.pdf", "page_number": 3},
        ],
    )
    return chroma_path


def _fake_encode(texts, show_progress_bar=False):
    return np.array([[0.9] * 384] * len(texts))


def test_retrieve_returns_list(populated_chroma):
    with patch("backend.rag_retriever._get_model") as mock_model:
        mock_model.return_value.encode = _fake_encode
        results = retrieve("CATScript query", populated_chroma, top_k=2)
    assert isinstance(results, list)
    assert len(results) <= 2


def test_retrieve_chunk_fields(populated_chroma):
    with patch("backend.rag_retriever._get_model") as mock_model:
        mock_model.return_value.encode = _fake_encode
        results = retrieve("CATScript query", populated_chroma, top_k=2)
    for chunk in results:
        assert "content" in chunk
        assert "source_file" in chunk
        assert "page_number" in chunk
        assert "score" in chunk


def test_retrieve_top_k_limit(populated_chroma):
    with patch("backend.rag_retriever._get_model") as mock_model:
        mock_model.return_value.encode = _fake_encode
        results = retrieve("query", populated_chroma, top_k=1)
    assert len(results) == 1

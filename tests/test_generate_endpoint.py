"""Tests — POST /generate endpoint (T-206)"""

import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


_CHUNKS = [
    {"content": "CATScript pad example.", "source_file": "doc.pdf", "page_number": 1, "score": 0.82},
]

_GENERATE_PAYLOAD = {
    "query": "create a pad of 10mm",
    "script_type": "catscript",
    "top_k": 5,
    "provider": "anthropic",
    "model": "claude-3-haiku-20240307",
    "api_key": "test-key",
}


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_generate_success():
    with patch("backend.routes.retrieve", return_value=_CHUNKS), \
         patch("backend.routes.call_llm", return_value="Dim oDoc As Document"):
        response = client.post("/generate", json=_GENERATE_PAYLOAD)
    assert response.status_code == 200
    body = response.json()
    assert "script" in body
    assert "sources" in body
    assert "confidence" in body
    assert body["script"] == "Dim oDoc As Document"
    assert body["confidence"] in ("high", "medium", "low")


def test_generate_returns_sources():
    with patch("backend.routes.retrieve", return_value=_CHUNKS), \
         patch("backend.routes.call_llm", return_value="script"):
        response = client.post("/generate", json=_GENERATE_PAYLOAD)
    sources = response.json()["sources"]
    assert len(sources) == 1
    assert sources[0]["source_file"] == "doc.pdf"
    assert sources[0]["page_number"] == 1


def test_generate_low_confidence_with_empty_corpus():
    with patch("backend.routes.retrieve", return_value=[]), \
         patch("backend.routes.call_llm", return_value="fallback script"):
        response = client.post("/generate", json=_GENERATE_PAYLOAD)
    assert response.json()["confidence"] == "low"


def test_generate_invalid_provider():
    payload = {**_GENERATE_PAYLOAD, "provider": "invalid_provider"}
    response = client.post("/generate", json=payload)
    assert response.status_code == 422


def test_generate_missing_query():
    payload = {**_GENERATE_PAYLOAD, "query": ""}
    response = client.post("/generate", json=payload)
    assert response.status_code == 422

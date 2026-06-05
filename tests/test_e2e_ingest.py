"""Test E2E — ingestion d'un PDF synthétique + vérification pipeline complet (T-402)"""

import pytest
from pathlib import Path
import fitz
from unittest.mock import patch

from backend.ingest import load_pdf, chunk_pages, embed_and_store
from backend.rag_retriever import retrieve
from backend.prompt_builder import build_prompt


def _make_catia_pdf(path: Path) -> None:
    doc = fitz.open()
    contents = [
        (
            "CATScript Macro — Creating a Pad Feature\n"
            "To create a pad in CATIA V5, use the ShapeFactory object.\n"
            "Dim oDoc As Document\n"
            "Set oDoc = CATIA.ActiveDocument\n"
            "The pad requires a closed profile sketch as input.\n"
            "Use PartDocument and Part objects to access the geometry.\n" * 5
        ),
        (
            "EKL Script — Engineering Knowledge Language\n"
            "EKL scripts are used in the Knowledge Advisor workbench.\n"
            "let myLength(Length)\n"
            "myLength = 10mm\n"
            "Relations can be applied to parameters and features.\n"
            "Use the Set instruction to assign values.\n" * 5
        ),
        (
            "EHI/EHA — Electrical Harness Routing\n"
            "EHI workbench handles harness installation definitions.\n"
            "Route segments must follow the geometric bundle path.\n"
            "Use the CATIA Electrical harness library commands.\n"
            "Connector references must match the catalog entries.\n" * 5
        ),
    ]
    for text in contents:
        page = doc.new_page()
        page.insert_text((72, 72), text)
    doc.save(str(path))
    doc.close()


@pytest.fixture(scope="module")
def e2e_workspace(tmp_path_factory):
    ws = tmp_path_factory.mktemp("e2e")
    pdf_path = ws / "catia_knowhow.pdf"
    _make_catia_pdf(pdf_path)
    chroma_path = ws / "chroma_db"

    pages = load_pdf(pdf_path)
    chunks = chunk_pages(pages)
    embed_and_store(chunks, chroma_path)

    return {"chroma_path": chroma_path, "pdf_name": pdf_path.name, "chunk_count": len(chunks)}


def _fake_encode(texts, show_progress_bar=False):
    import numpy as np
    return np.array([[0.5] * 384] * len(texts))


def test_e2e_catscript_retrieval(e2e_workspace):
    with patch("backend.rag_retriever._get_model") as mock_model:
        mock_model.return_value.encode = _fake_encode
        chunks = retrieve("create a pad feature", e2e_workspace["chroma_path"], top_k=5)
    assert len(chunks) > 0
    for c in chunks:
        assert c["source_file"] == e2e_workspace["pdf_name"]
        assert c["page_number"] >= 1


def test_e2e_ekl_prompt_build(e2e_workspace):
    with patch("backend.rag_retriever._get_model") as mock_model:
        mock_model.return_value.encode = _fake_encode
        chunks = retrieve("write an EKL rule for length", e2e_workspace["chroma_path"], top_k=5)
    prompt, _ = build_prompt(chunks, "write an EKL rule for length", "ekl")
    assert "EKL" in prompt
    assert "write an EKL rule for length" in prompt


def test_e2e_ehi_prompt_build(e2e_workspace):
    with patch("backend.rag_retriever._get_model") as mock_model:
        mock_model.return_value.encode = _fake_encode
        chunks = retrieve("route an electrical harness", e2e_workspace["chroma_path"], top_k=5)
    prompt, _ = build_prompt(chunks, "route an electrical harness", "ehi_eha")
    assert "EHI_EHA" in prompt


def test_e2e_chunk_count(e2e_workspace):
    assert e2e_workspace["chunk_count"] > 0


def test_e2e_generate_endpoint_with_mock_llm(e2e_workspace):
    from fastapi.testclient import TestClient
    from backend.main import app

    client = TestClient(app)

    def fake_retrieve(query, chroma_path, top_k=5):
        return [{"content": "CATScript pad example", "source_file": "catia_knowhow.pdf", "page_number": 1, "score": 0.75}]

    with patch("backend.routes.retrieve", side_effect=fake_retrieve), \
         patch("backend.routes.call_llm", return_value="Dim oDoc As Document\nSet oDoc = CATIA.ActiveDocument"):
        response = client.post("/generate", json={
            "query": "create a pad of 10mm",
            "script_type": "catscript",
            "top_k": 5,
            "provider": "anthropic",
            "model": "claude-3-haiku-20240307",
            "api_key": "test-key",
        })

    assert response.status_code == 200
    body = response.json()
    assert len(body["script"]) > 0
    assert len(body["sources"]) > 0
    assert body["confidence"] in ("high", "medium", "low")

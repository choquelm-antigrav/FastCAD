"""Tests unitaires — backend/ingest.py (T-104)"""

import pytest
from pathlib import Path
import fitz

from backend.ingest import load_pdf, chunk_pages, embed_and_store


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _make_pdf(path: Path, pages: list[str]) -> None:
    doc = fitz.open()
    for text in pages:
        page = doc.new_page()
        page.insert_text((72, 72), text)
    doc.save(str(path))
    doc.close()


@pytest.fixture
def two_page_pdf(tmp_path: Path) -> Path:
    pdf_path = tmp_path / "sample.pdf"
    _make_pdf(pdf_path, [
        "Page one. " * 30,
        "Page two. " * 30,
    ])
    return pdf_path


@pytest.fixture
def chroma_dir(tmp_path: Path) -> Path:
    return tmp_path / "chroma_db"


# ---------------------------------------------------------------------------
# T-104a — chargement & métadonnées
# ---------------------------------------------------------------------------

def test_load_pdf_page_count(two_page_pdf):
    pages = load_pdf(two_page_pdf)
    assert len(pages) == 2


def test_load_pdf_metadata_fields(two_page_pdf):
    pages = load_pdf(two_page_pdf)
    for i, page in enumerate(pages):
        assert page["page_number"] == i + 1
        assert page["source_file"] == two_page_pdf.name
        assert isinstance(page["text"], str)
        assert len(page["text"]) > 0


def test_load_pdf_file_not_found(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_pdf(tmp_path / "missing.pdf")


# ---------------------------------------------------------------------------
# T-104b — chunking
# ---------------------------------------------------------------------------

def test_chunk_pages_metadata_fields(two_page_pdf):
    pages = load_pdf(two_page_pdf)
    chunks = chunk_pages(pages)
    assert len(chunks) > 0
    for chunk in chunks:
        assert "chunk_id" in chunk
        assert "source_file" in chunk
        assert "page_number" in chunk
        assert "content" in chunk
        assert len(chunk["content"]) > 0


def test_chunk_ids_are_unique(two_page_pdf):
    pages = load_pdf(two_page_pdf)
    chunks = chunk_pages(pages)
    ids = [c["chunk_id"] for c in chunks]
    assert len(ids) == len(set(ids))


# ---------------------------------------------------------------------------
# T-104c — embed & store + idempotence
# ---------------------------------------------------------------------------

def test_embed_and_store_returns_count(two_page_pdf, chroma_dir):
    pages = load_pdf(two_page_pdf)
    chunks = chunk_pages(pages)
    added = embed_and_store(chunks, chroma_dir)
    assert added == len(chunks)


def test_embed_and_store_idempotent(two_page_pdf, chroma_dir):
    pages = load_pdf(two_page_pdf)
    chunks = chunk_pages(pages)

    first_run = embed_and_store(chunks, chroma_dir)
    second_run = embed_and_store(chunks, chroma_dir)

    assert first_run == len(chunks)
    assert second_run == 0

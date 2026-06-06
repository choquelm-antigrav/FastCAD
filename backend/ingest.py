"""
ingest.py — Pipeline PDF → Chunks → ChromaDB
T-101: load_pdf  |  T-102: chunk_pages  |  T-103: embed_and_store
"""

import argparse
import uuid
from datetime import datetime, timezone
from pathlib import Path

import fitz
import pdfplumber
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import chromadb


# ---------------------------------------------------------------------------
# T-101 — PDF Loader
# ---------------------------------------------------------------------------

def _extract_page_text_pdfplumber(pdf_path: Path, page_index: int) -> str:
    with pdfplumber.open(str(pdf_path)) as pdf:
        page = pdf.pages[page_index]
        return page.extract_text() or ""


def _extract_page_text_fitz(pdf_path: Path, page_index: int) -> str:
    doc = fitz.open(str(pdf_path))
    text = doc[page_index].get_text()
    doc.close()
    return text


def load_pdf(path: Path) -> list[dict]:
    """
    Extract text from every page of a PDF.

    Primary extractor : pdfplumber.
    Fallback (per page) : fitz (PyMuPDF) when pdfplumber returns empty text.

    Returns
    -------
    list of {page_number: int, text: str, source_file: str}
    """
    if not path.is_file():
        raise FileNotFoundError(f"PDF not found: {path}")

    pages: list[dict] = []

    with pdfplumber.open(str(path)) as pdf:
        total = len(pdf.pages)

    for idx in range(total):
        text = _extract_page_text_pdfplumber(path, idx)
        if not text.strip():
            text = _extract_page_text_fitz(path, idx)

        pages.append(
            {
                "page_number": idx + 1,
                "text": text,
                "source_file": path.name,
            }
        )

    return pages


# ---------------------------------------------------------------------------
# T-102 — Chunker
# ---------------------------------------------------------------------------

_SPLITTER = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)


def chunk_pages(pages: list[dict]) -> list[dict]:
    """
    Split page texts into overlapping chunks.

    Returns
    -------
    list of {chunk_id: str, source_file: str, page_number: int, content: str}
    """
    chunks: list[dict] = []

    for page in pages:
        splits = _SPLITTER.split_text(page["text"])
        for content in splits:
            chunks.append(
                {
                    "chunk_id": str(uuid.uuid4()),
                    "source_file": page["source_file"],
                    "page_number": page["page_number"],
                    "content": content,
                }
            )

    return chunks


# ---------------------------------------------------------------------------
# T-103 — Embedder + ChromaDB
# ---------------------------------------------------------------------------

_COLLECTION_NAME = "catscript_knowhow"
_EMBED_MODEL = "all-MiniLM-L6-v2"


def embed_and_store(chunks: list[dict], chroma_path: Path) -> int:
    """
    Embed chunks and persist them in ChromaDB.

    Idempotent : chunks whose chunk_id already exists in the collection
    are silently skipped.

    Parameters
    ----------
    chunks      : output of chunk_pages()
    chroma_path : persistent storage directory for ChromaDB

    Returns
    -------
    Number of chunks actually added (skipped chunks excluded).
    """
    chroma_path.mkdir(parents=True, exist_ok=True)

    client = chromadb.PersistentClient(path=str(chroma_path))
    collection = client.get_or_create_collection(name=_COLLECTION_NAME)

    existing_ids: set[str] = set(collection.get(include=[])["ids"])

    new_chunks = [c for c in chunks if c["chunk_id"] not in existing_ids]

    if not new_chunks:
        return 0

    model = SentenceTransformer(_EMBED_MODEL)
    contents = [c["content"] for c in new_chunks]
    embeddings = model.encode(contents, show_progress_bar=False).tolist()

    ingested_at = datetime.now(timezone.utc).isoformat()
    collection.add(
        ids=[c["chunk_id"] for c in new_chunks],
        embeddings=embeddings,
        documents=contents,
        metadatas=[
            {
                "source_file": c["source_file"],
                "page_number": c["page_number"],
                "ingested_at": ingested_at,
            }
            for c in new_chunks
        ],
    )

    return len(new_chunks)


# ---------------------------------------------------------------------------
# CLI entry-point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest PDF documents into ChromaDB.")
    parser.add_argument(
        "--docs",
        type=Path,
        required=True,
        help="Path to the folder containing PDF files.",
    )
    args = parser.parse_args()

    docs_dir: Path = args.docs
    if not docs_dir.is_dir():
        raise FileNotFoundError(f"--docs directory not found: {docs_dir}")

    project_root = Path(__file__).resolve().parent.parent
    chroma_path = project_root / "data" / "chroma_db"

    pdf_files = sorted(docs_dir.glob("*.pdf"))
    if not pdf_files:
        print(f"WARN  no PDF files found in {docs_dir}")

    total_added = 0

    for pdf_path in pdf_files:
        print(f"INFO  loading  {pdf_path.name}")
        pages = load_pdf(pdf_path)
        chunks = chunk_pages(pages)
        added = embed_and_store(chunks, chroma_path)
        print(f"OK    {pdf_path.name} → {len(chunks)} chunks total, {added} added")
        total_added += added

    print(f"DONE  total chunks added: {total_added}")
    print(f"INFO  chroma_db path: {chroma_path}")

"""FastAPI routes — /health, POST /ingest, POST /generate, POST /geometry"""

from __future__ import annotations

import json as _json
import os
import shutil
import tempfile
from enum import Enum
from pathlib import Path

from dotenv import load_dotenv
from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel, Field

load_dotenv()

from backend.ingest import chunk_pages, embed_and_store, load_pdf
from backend.llm_router import call_llm
from backend.prompt_builder import build_geometry_prompt, build_prompt
from backend.rag_retriever import retrieve

router = APIRouter()

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_CHROMA_PATH = _PROJECT_ROOT / "data" / "chroma_db"


def _strip_markdown_fences(text: str) -> str:
    """Remove ```language ... ``` wrappers that some models add around code."""
    import re
    text = text.strip()
    text = re.sub(r"^```[a-zA-Z]*\s*\n?", "", text)
    text = re.sub(r"\n?```\s*$", "", text)
    return text.strip()


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

class ScriptType(str, Enum):
    catscript = "catscript"
    ekl = "ekl"
    ehi_eha = "ehi_eha"


class Provider(str, Enum):
    anthropic = "anthropic"
    openrouter = "openrouter"
    openai = "openai"
    ollama = "ollama"
    deepseek = "deepseek"
    kimi = "kimi"
    nemotron = "nemotron"


class ConfidenceLevel(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"


class GenerationRequest(BaseModel):
    query: str = Field(..., min_length=1)
    script_type: ScriptType
    top_k: int = Field(default=5, ge=1, le=20)
    provider: Provider
    model: str = Field(..., min_length=1)
    api_key: str = Field(default="")


class SourceRef(BaseModel):
    source_file: str
    page_number: int
    score: float


class GenerationResponse(BaseModel):
    script: str
    sources: list[SourceRef]
    confidence: ConfidenceLevel


class IngestResponse(BaseModel):
    filename: str
    chunks_total: int
    chunks_added: int


class GeometryRequest(BaseModel):
    query: str = Field(..., min_length=1)
    script_type: str = Field(default="")
    provider: Provider
    model: str = Field(..., min_length=1)
    api_key: str = Field(default="")


class GeometryResponse(BaseModel):
    geometry: dict | None = None


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.post("/ingest", response_model=IngestResponse)
async def ingest(file: UploadFile = File(...)) -> IngestResponse:
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = Path(tmp.name)

    try:
        pages = load_pdf(tmp_path)
        chunks = chunk_pages(pages)
        for chunk in chunks:
            chunk["source_file"] = file.filename
        added = embed_and_store(chunks, _CHROMA_PATH)
    finally:
        tmp_path.unlink(missing_ok=True)

    return IngestResponse(
        filename=file.filename,
        chunks_total=len(chunks),
        chunks_added=added,
    )


_ENV_KEYS: dict[str, str] = {
    "anthropic":  "ANTHROPIC_API_KEY",
    "openrouter": "OPENROUTER_API_KEY",
    "openai":     "OPENAI_API_KEY",
    "deepseek":   "DEEPSEEK_API_KEY",
    "kimi":       "MOONSHOT_API_KEY",
    "nemotron":   "NVIDIA_API_KEY",
}


@router.post("/generate", response_model=GenerationResponse)
def generate(req: GenerationRequest) -> GenerationResponse:
    api_key = req.api_key.strip() or os.getenv(_ENV_KEYS.get(req.provider.value, ""), "")

    chunks = retrieve(req.query, _CHROMA_PATH, top_k=req.top_k)
    prompt, low_confidence = build_prompt(chunks, req.query, req.script_type.value)
    try:
        script = call_llm(req.provider.value, req.model, api_key, prompt)
    except Exception as exc:
        msg = str(exc)
        if "429" in msg or "rate limit" in msg.lower() or "RateLimitError" in type(exc).__name__:
            raise HTTPException(
                status_code=429,
                detail="Limite de requêtes atteinte sur ce provider. "
                       "Attendez la réinitialisation ou changez de modèle/provider dans les paramètres.",
            )
        raise HTTPException(status_code=502, detail=f"Erreur LLM : {msg[:200]}")
    script = _strip_markdown_fences(script)

    max_score = max((c["score"] for c in chunks), default=0.0)
    if low_confidence:
        confidence = ConfidenceLevel.low
    elif max_score >= 0.7:
        confidence = ConfidenceLevel.high
    else:
        confidence = ConfidenceLevel.medium

    sources = [
        SourceRef(
            source_file=c["source_file"],
            page_number=c["page_number"],
            score=c["score"],
        )
        for c in chunks
    ]

    return GenerationResponse(script=script, sources=sources, confidence=confidence)


@router.post("/geometry", response_model=GeometryResponse)
def geometry_preview(req: GeometryRequest) -> GeometryResponse:
    api_key = req.api_key.strip() or os.getenv(_ENV_KEYS.get(req.provider.value, ""), "")
    prompt = build_geometry_prompt(req.query, req.script_type)
    try:
        raw = call_llm(req.provider.value, req.model, api_key, prompt)
        raw = _strip_markdown_fences(raw)
        geo = _json.loads(raw)
        return GeometryResponse(geometry=geo)
    except Exception as exc:
        if "429" in str(exc) or "RateLimitError" in type(exc).__name__:
            raise HTTPException(
                status_code=429,
                detail="Limite de requêtes atteinte. Changez de modèle dans les paramètres.",
            )
        return GeometryResponse(geometry=None)

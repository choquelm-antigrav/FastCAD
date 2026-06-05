"""FastAPI routes — /health and POST /generate (T-201, T-205)"""

from __future__ import annotations

from enum import Enum
from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel, Field

from backend.llm_router import call_llm
from backend.prompt_builder import build_prompt
from backend.rag_retriever import retrieve

router = APIRouter()

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_CHROMA_PATH = _PROJECT_ROOT / "data" / "chroma_db"


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

class ScriptType(str, Enum):
    catscript = "catscript"
    ekl = "ekl"
    ehi_eha = "ehi_eha"


class Provider(str, Enum):
    anthropic = "anthropic"
    google = "google"
    openai = "openai"
    ollama = "ollama"


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


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.post("/generate", response_model=GenerationResponse)
def generate(req: GenerationRequest) -> GenerationResponse:
    chunks = retrieve(req.query, _CHROMA_PATH, top_k=req.top_k)
    prompt, low_confidence = build_prompt(chunks, req.query, req.script_type.value)
    script = call_llm(req.provider.value, req.model, req.api_key, prompt)

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

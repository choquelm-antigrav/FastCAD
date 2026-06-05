"""Tests — backend/prompt_builder.py (T-206)"""

from backend.prompt_builder import build_prompt, LOW_CONFIDENCE_THRESHOLD


_CHUNKS_HIGH = [
    {"content": "Use CATScript to create a pad.", "source_file": "doc.pdf", "page_number": 1, "score": 0.85},
    {"content": "Pad creation requires a sketch.", "source_file": "doc.pdf", "page_number": 2, "score": 0.75},
]

_CHUNKS_LOW = [
    {"content": "Some unrelated content.", "source_file": "doc.pdf", "page_number": 5, "score": 0.10},
]


def test_build_prompt_contains_query():
    prompt, _ = build_prompt(_CHUNKS_HIGH, "create a pad feature", "catscript")
    assert "create a pad feature" in prompt


def test_build_prompt_contains_script_type():
    prompt, _ = build_prompt(_CHUNKS_HIGH, "query", "ekl")
    assert "EKL" in prompt


def test_build_prompt_injects_chunks():
    prompt, _ = build_prompt(_CHUNKS_HIGH, "query", "catscript")
    assert "Use CATScript to create a pad." in prompt
    assert "Pad creation requires a sketch." in prompt


def test_build_prompt_source_references():
    prompt, _ = build_prompt(_CHUNKS_HIGH, "query", "catscript")
    assert "doc.pdf" in prompt
    assert "p.1" in prompt


def test_low_confidence_flag_when_scores_low():
    _, low = build_prompt(_CHUNKS_LOW, "query", "catscript")
    assert low is True


def test_high_confidence_flag_when_scores_high():
    _, low = build_prompt(_CHUNKS_HIGH, "query", "catscript")
    assert low is False


def test_low_confidence_when_no_chunks():
    _, low = build_prompt([], "query", "catscript")
    assert low is True


def test_empty_chunks_uses_fallback_text():
    prompt, _ = build_prompt([], "query", "catscript")
    assert "No relevant know-how" in prompt

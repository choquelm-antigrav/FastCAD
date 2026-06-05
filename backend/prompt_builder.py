"""Prompt builder — assemble RAG context + user query (T-204)"""

from __future__ import annotations

LOW_CONFIDENCE_THRESHOLD = 0.3

_SYSTEM_TEMPLATE = """\
You are an expert CATIA V5 R27 automation engineer.
You generate syntactically correct {script_type} scripts.
You ONLY use the know-how context provided below.
If the context is insufficient, say so explicitly before generating.
Always add inline comments to explain each step.

KNOW-HOW CONTEXT:
{context}

USER REQUEST:
{user_query}

Generate the script now."""


def build_prompt(
    retrieved_chunks: list[dict],
    user_query: str,
    script_type: str,
) -> tuple[str, bool]:
    """
    Assemble the full LLM prompt from retrieved chunks and user input.

    Parameters
    ----------
    retrieved_chunks : output of rag_retriever.retrieve()
    user_query       : natural language description from the designer
    script_type      : 'catscript', 'ekl', or 'ehi_eha'

    Returns
    -------
    (prompt_text, low_confidence)
    low_confidence is True when no chunk exceeds LOW_CONFIDENCE_THRESHOLD.
    """
    low_confidence = (
        not retrieved_chunks
        or max(c["score"] for c in retrieved_chunks) < LOW_CONFIDENCE_THRESHOLD
    )

    if retrieved_chunks:
        context_lines = []
        for i, chunk in enumerate(retrieved_chunks, 1):
            context_lines.append(
                f"[{i}] {chunk['source_file']} p.{chunk['page_number']}\n{chunk['content']}"
            )
        context = "\n\n".join(context_lines)
    else:
        context = "(No relevant know-how found in the document corpus.)"

    prompt = _SYSTEM_TEMPLATE.format(
        script_type=script_type.upper(),
        context=context,
        user_query=user_query,
    )

    return prompt, low_confidence

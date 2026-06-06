"""Prompt builder — assemble RAG context + user query (T-204)"""

from __future__ import annotations

LOW_CONFIDENCE_THRESHOLD = 0.25

_SYSTEM_TEMPLATE = """\
You are an expert CATIA V5 R27 automation engineer. Your role is to ALWAYS generate \
a complete, syntactically correct {script_type} script. Never refuse to generate.

RULES:
- Use ONLY the API methods and patterns shown in the KNOW-HOW CONTEXT below.
- If a specific API detail is missing from the context, infer it from the patterns \
  present (same object model, same naming conventions).
- For CATScript: always use Option Explicit, declare all variables with Dim/As, \
  end with oPart.Update or oProduct.Update.
- For EKL: use let declarations, backtick references `PartBody\\Feature\\Param`, \
  wrap in Rule/Check/Reaction block.
- For EHI_EHA: use ElecHarnessInstallation factory, HybridShapeFactory for 3D points, \
  ElecBundleSegment with SetDiameter/AddRoutingPoint.
- Add inline comments on every non-trivial line.
- NEVER output prose explanations instead of code. Output ONLY the script.

KNOW-HOW CONTEXT:
{context}

USER REQUEST:
{user_query}

Generate the complete script now:"""


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


# ---------------------------------------------------------------------------
# Geometry preview prompt
# ---------------------------------------------------------------------------

_GEOMETRY_PROMPT_PART = """\
Based on this CATIA design request: {user_query}

Return ONLY a valid JSON object (no markdown, no explanation) describing a simplified 3D geometry for visual preview.

Use the mechanical part format:
{{
  "name": "PartName",
  "type": "part",
  "bodies": [
    {{"id": "base",  "shape": "box",      "w": 160.0, "h": 6.0, "d": 90.0, "color": "main",    "x": 0.0, "y": 0.0, "z": 0.0}},
    {{"id": "rib",   "shape": "box",      "w": 6.0, "h": 70.0, "d": 80.0, "color": "feature",  "x": 0.0, "y": 6.0, "z": 5.0}},
    {{"id": "hole1", "shape": "cylinder", "r": 4.5, "h": 8.0,             "color": "hole",     "x": 20.0,"y": 0.0, "z": 20.0, "axis": "y"}}
  ]
}}

Rules:
- box:      w=X-width, h=Y-height, d=Z-depth, x/y/z = center position (mm)
- cylinder: r=radius, h=height, axis = "x"|"y"|"z", x/y/z = center (mm)
- color:    "main" (solid body), "feature" (added feature), "hole" (removed material)
- Use realistic dimensions from the request (mm). Include 2-8 bodies max.
- Return ONLY the raw JSON object, nothing else.\
"""

_GEOMETRY_PROMPT_HARNESS = """\
Based on this CATIA harness design request: {user_query}

Return ONLY a valid JSON object (no markdown, no explanation) describing a simplified 3D harness geometry for visual preview.

You MUST return the harness JSON format with "segments" array. Do NOT use the "bodies" format.

{{
  "name": "HarnessName",
  "type": "harness",
  "segments": [
    {{"id": "trunk",   "from": [0,0,0],   "to": [500,0,0],  "r": 6.0, "color": "main"}},
    {{"id": "branch1", "from": [250,0,0], "to": [250,80,40],"r": 4.0, "color": "branch"}}
  ]
}}

Rules:
- Each segment: from/to are [x,y,z] coordinates (mm), r=radius (mm)
- color: "main" (trunk), "branch" (secondary branch)
- Use realistic routing dimensions. Include 2-8 segments max.
- Return ONLY the raw JSON object, nothing else.\
"""


def build_geometry_prompt(user_query: str, script_type: str = "") -> str:
    st = script_type.lower()
    if "ehi" in st or "eha" in st:
        return _GEOMETRY_PROMPT_HARNESS.format(user_query=user_query)
    return _GEOMETRY_PROMPT_PART.format(user_query=user_query)

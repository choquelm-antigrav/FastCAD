"""Prompt builder — assemble RAG context + user query (T-204)"""

from __future__ import annotations

LOW_CONFIDENCE_THRESHOLD = 0.25

# ---------------------------------------------------------------------------
# Sheet Metal Design — inline API knowledge (no PDF required)
# ---------------------------------------------------------------------------

_SM_API_KNOWLEDGE = """\
=== CATIA V5 Generative Sheet Metal Design — CATScript API Reference ===

── FACTORY ACCESS ──────────────────────────────────────────────────────────
  Dim oSMF As SheetMetalFactory
  Set oSMF = oPart.GetTechnologicalObject("SheetMetalFactory")

── GLOBAL PARAMETERS ───────────────────────────────────────────────────────
  Dim oParams As SheetMetalParameters
  Set oParams = oSMF.SheetMetalParameters
  oParams.Thickness.Value  = 2.0   ' épaisseur tôle mm
  oParams.BendRadius.Value = 3.0   ' rayon de pli par défaut mm
  oParams.BendAngle.Value  = 90.0  ' angle de pli par défaut degrés (optionnel)

── BASE WALL (paroi de base à partir d'un esquisse) ────────────────────────
  Dim oSketch As Sketch
  Set oSketch = oPart.Sketches.Add(oPart.OriginPlanes.Item(2)) ' plan XY = Item(2)
  Dim oFact2D As Factory2D
  Set oFact2D = oSketch.OpenEdition()
  ' Dessiner un rectangle fermé (4 lignes)
  oFact2D.CreateLine 0, 0, 200, 0
  oFact2D.CreateLine 200, 0, 200, 100
  oFact2D.CreateLine 200, 100, 0, 100
  oFact2D.CreateLine 0, 100, 0, 0
  oSketch.CloseEdition
  Dim oWall As Wall
  Set oWall = oSMF.AddNewWall(oSketch)   ' crée la paroi de base

── FLANGE (pliage sur arête existante) ─────────────────────────────────────
  ' Sélectionner une arête de la paroi via Selection
  CATIA.ActiveDocument.Selection.Clear
  CATIA.ActiveDocument.Selection.Add oWall
  Dim oFlange As Flange
  Set oFlange = oSMF.AddNewFlange()      ' la sélection active fournit l'arête
  oFlange.Angle.Value  = 90.0            ' angle de repli (degrés)
  oFlange.Length.Value = 30.0            ' hauteur de la bride (mm)
  ' Override local bend radius (optionnel)
  ' oFlange.BendRadius.Value = 2.0

── ADDITIONAL WALL ON EDGE ─────────────────────────────────────────────────
  ' Paroi supplémentaire posée sur une arête (sans sélection)
  Dim oWall2 As Wall
  Set oWall2 = oSMF.AddNewWallOnEdge()   ' nécessite une sélection d'arête au préalable

── CUTOUT (découpe dans la tôle depuis esquisse) ────────────────────────────
  Dim oSkCut As Sketch
  Set oSkCut = oPart.Sketches.Add(oPart.OriginPlanes.Item(2))
  Dim oF2 As Factory2D
  Set oF2 = oSkCut.OpenEdition()
  oF2.CreateClosedProfile  ' ou dessiner profil de découpe
  oSkCut.CloseEdition
  Dim oCut As Cutout
  Set oCut = oSMF.AddNewCutout(oSkCut)

── CIRCULAR STAMP (bossage circulaire) ──────────────────────────────────────
  ' Esquisse = centre du stamp (cercle ou point de référence)
  Dim oCircStamp As CircStamp
  Set oCircStamp = oSMF.AddNewCircStamp(oSketchStamp)
  oCircStamp.Height.Value         = 5.0   ' hauteur du bossage mm
  oCircStamp.DiameterBottom.Value = 30.0  ' diamètre base mm
  oCircStamp.DiameterTop.Value    = 25.0  ' diamètre sommet mm
  oCircStamp.Radius.Value         = 2.0   ' rayon de congé mm
  oCircStamp.DraftAngle.Value     = 15.0  ' dépouille degrés

── SURFACE STAMP (bossage surfacique) ───────────────────────────────────────
  Dim oSurfStamp As SurfaceStamp
  Set oSurfStamp = oSMF.AddNewSurfaceStamp(oSketchStamp)
  oSurfStamp.Height.Value     = 4.0
  oSurfStamp.DraftAngle.Value = 10.0
  oSurfStamp.Radius.Value     = 1.5

── BRIDGE (pont entre deux découpes) ────────────────────────────────────────
  Dim oBridge As Bridge
  Set oBridge = oSMF.AddNewBridge(oSketch1, oSketch2)
  oBridge.Height.Value = 3.0
  oBridge.Width.Value  = 8.0
  oBridge.Radius.Value = 1.0

── JOGGLE (ressaut) ─────────────────────────────────────────────────────────
  Dim oJoggle As Joggle
  Set oJoggle = oSMF.AddNewJoggle()   ' sélection d'arête requise
  oJoggle.Offset.Value = 6.0          ' décalage mm
  oJoggle.Length.Value = 20.0         ' longueur du ressaut mm
  oJoggle.Radius.Value = 3.0

── BEND / UNBEND (plier / déplier) ──────────────────────────────────────────
  Dim oBend As Bend
  Set oBend = oSMF.AddNewBend()       ' sélection de 2 arêtes requise
  ' Pour obtenir le développé : oSMF.AddNewUnfold()

── CORNER RELIEF ────────────────────────────────────────────────────────────
  Dim oCorner As Corner
  Set oCorner = oSMF.AddNewCorner()   ' sélection du coin (vertex) requise
  oCorner.ReliefType = 1              ' 1=carré, 2=rond, 3=triangulaire

── HEM FLANGE (ourlet) ──────────────────────────────────────────────────────
  Dim oHem As HemFlange
  Set oHem = oSMF.AddNewHemFlange()  ' sélection d'arête requise
  oHem.HemType  = 1                  ' 1=flat hem, 2=open hem, 3=rope hem
  oHem.Length.Value = 8.0
  oHem.Gap.Value    = 0.5

── STIFFENER RIB (raidisseur) ───────────────────────────────────────────────
  Dim oRib As StiffenerRib
  Set oRib = oSMF.AddNewStiffenerRib(oSketchRib)
  oRib.Depth.Value  = 5.0
  oRib.Radius.Value = 2.0
  oRib.DraftAngle.Value = 10.0

── COMPLETE EXAMPLE — Bracket (équerre 90°) ─────────────────────────────────
Option Explicit
Sub CATMain()
    Dim oDoc    As PartDocument  : Set oDoc  = CATIA.ActiveDocument
    Dim oPart   As Part          : Set oPart = oDoc.Part
    Dim oSMF    As SheetMetalFactory
    Set oSMF = oPart.GetTechnologicalObject("SheetMetalFactory")

    ' Paramètres matière
    Dim oP As SheetMetalParameters : Set oP = oSMF.SheetMetalParameters
    oP.Thickness.Value  = 2.0   ' tôle 2mm
    oP.BendRadius.Value = 3.0   ' rayon intérieur 3mm

    ' Esquisse paroi de base (XY) : 150×80mm
    Dim oSk As Sketch
    Set oSk = oPart.Sketches.Add(oPart.OriginPlanes.Item(2))
    Dim oF As Factory2D : Set oF = oSk.OpenEdition()
    oF.CreateLine   0,  0, 150,  0
    oF.CreateLine 150,  0, 150, 80
    oF.CreateLine 150, 80,   0, 80
    oF.CreateLine   0, 80,   0,  0
    oSk.CloseEdition

    Dim oWall As Wall : Set oWall = oSMF.AddNewWall(oSk)

    oPart.Update
End Sub

── COMPLETE EXAMPLE — Box tray (bac 4 brides) ───────────────────────────────
' Pattern : paroi de base + 4 brides de 25mm à 90°
' Chaque flange nécessite une sélection d'arête différente avant AddNewFlange()
' → Itérer sur les 4 arêtes via Selection ou GetBoundary sur le Wall.
"""

_SM_KEYWORDS = {
    "sheet metal", "tôle", "tole", "bride", "flange", "pliage", "pli",
    "emboutissage", "stamp", "bossage", "découpe tôle", "cutout tôle",
    "sheetmetal", "sheet_metal", "développé", "develope", "unfold",
    "joggle", "ressaut", "ourlet", "hem", "raidisseur", "stiffener",
    "bend radius", "rayon de pli", "épaisseur tôle", "tôlerie",
    "bracket", "equerre", "équerre", "boîtier tôle",
}

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

    # Inject Sheet Metal inline knowledge when relevant
    query_lower = user_query.lower()
    is_sheetmetal = any(kw in query_lower for kw in _SM_KEYWORDS)

    if retrieved_chunks:
        context_lines = []
        for i, chunk in enumerate(retrieved_chunks, 1):
            context_lines.append(
                f"[{i}] {chunk['source_file']} p.{chunk['page_number']}\n{chunk['content']}"
            )
        context = "\n\n".join(context_lines)
    else:
        context = "(No relevant know-how found in the document corpus.)"

    if is_sheetmetal:
        context = _SM_API_KNOWLEDGE + "\n\n" + context

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


_GEOMETRY_PROMPT_FROM_SCRIPT_PART = """\
A CATScript has been generated for CATIA V5. Analyse it and extract the actual 3D geometry.

GENERATED CATSCRIPT:
{script}

USER REQUEST (context only):
{user_query}

Return ONLY a valid JSON object (no markdown, no explanation) describing the 3D geometry for visual preview.
Extract REAL dimensions from the script:
- Pad/Shaft → box or cylinder; SetFirstLimit value = height
- Pocket/Groove → box with "hole" color; SetFirstLimit value = depth
- Hole → cylinder; SetDiameter value / 2 = r; "hole" color
- Fillet/Chamfer → ignore
- Position offsets from HybridShapePointCoord or Dim assignments

{{
  "name": "PartName",
  "type": "part",
  "bodies": [
    {{"id": "base",  "shape": "box",      "w": 160.0, "h": 6.0, "d": 90.0, "color": "main",    "x": 0.0, "y": 0.0, "z": 0.0}},
    {{"id": "pad1",  "shape": "box",      "w": 40.0,  "h": 20.0,"d": 40.0, "color": "feature", "x": 60.0,"y": 3.0, "z": 25.0}},
    {{"id": "hole1", "shape": "cylinder", "r": 4.5,   "h": 8.0,            "color": "hole",    "x": 20.0,"y": 0.0, "z": 20.0, "axis": "y"}}
  ]
}}

Rules:
- box: w=X-width, h=Y-height, d=Z-depth, x/y/z = center (mm)
- cylinder: r=radius, h=height, axis="x"|"y"|"z", x/y/z = center (mm)
- color: "main" (base body), "feature" (added pad/shaft), "hole" (removed material)
- Use ONLY numerical values found in the script. 2–8 bodies max.
- Return ONLY the raw JSON object, nothing else.\
"""

_GEOMETRY_PROMPT_FROM_SCRIPT_HARNESS = """\
An EHI/EHA CATScript has been generated for CATIA V5. Analyse it and extract the actual harness routing AND the environment components.

GENERATED CATSCRIPT:
{script}

USER REQUEST (context only):
{user_query}

Return ONLY a valid JSON object (no markdown, no explanation) describing the full 3D scene for visual preview.

{{
  "name": "HarnessScene",
  "type": "harness",
  "segments": [
    {{"id": "trunk",   "from": [0,0,0],   "to": [500,0,0],   "r": 6.0, "color": "main"}},
    {{"id": "branch1", "from": [250,0,0], "to": [250,80,40], "r": 4.0, "color": "branch"}}
  ],
  "bodies": [
    {{"id": "bracket1", "shape": "box", "w": 80.0, "h": 40.0, "d": 20.0, "color": "environment", "x": 100.0, "y": 0.0, "z": 0.0}},
    {{"id": "connector1", "shape": "cylinder", "r": 12.0, "h": 30.0, "color": "environment", "x": 480.0, "y": 0.0, "z": 0.0, "axis": "y"}}
  ]
}}

Rules:
- segments: harness routing — from/to are [x,y,z] (mm), r=radius. color: "main" (trunk) / "branch" (secondary). 2–8 segments max.
- bodies: environment components (brackets, connectors, panels, bulkheads) deduced from the script.
  - color MUST be "environment" — rendered at 50% opacity in the viewer.
  - Extract approximate positions and sizes from HybridShapePointCoord calls or bounding box comments in the script.
  - 0–6 environment bodies max.
- Use ONLY values found in the script. Return ONLY the raw JSON object, nothing else.\
"""


def build_geometry_prompt(user_query: str, script_type: str = "", script: str = "") -> str:
    st = script_type.lower()
    is_harness = "ehi" in st or "eha" in st
    if script.strip():
        if is_harness:
            return _GEOMETRY_PROMPT_FROM_SCRIPT_HARNESS.format(
                script=script, user_query=user_query
            )
        return _GEOMETRY_PROMPT_FROM_SCRIPT_PART.format(
            script=script, user_query=user_query
        )
    if is_harness:
        return _GEOMETRY_PROMPT_HARNESS.format(user_query=user_query)
    return _GEOMETRY_PROMPT_PART.format(user_query=user_query)


# ---------------------------------------------------------------------------
# Reverse-engineering prompt
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Harness routing prompt (T-603)
# ---------------------------------------------------------------------------

def build_routing_prompt(env_info: dict, user_query: str = "") -> str:
    import json as _json
    info_str = _json.dumps(env_info, ensure_ascii=False, indent=2)
    extra = f"\nAdditional routing constraints from user: {user_query}" if user_query.strip() else ""
    return f"""\
You are an expert CATIA V5 R27 electrical harness engineer. An environment DMU (Digital Mock-Up) has been analysed below.

DMU ENVIRONMENT ANALYSIS:
{info_str}
{extra}

Your task: write a complete, syntactically correct EHI/EHA CATScript that routes a harness through this environment.

RULES:
- Use ElecHarnessInstallation factory to create the harness.
- Use HybridShapeFactory to define 3D routing points derived from the bounding_box_mm dimensions.
- Create ElecBundleSegment instances with SetDiameter and AddRoutingPoint.
- Place routing points that avoid component volumes (offset by at least 20mm from bounding boxes).
- End with oProduct.Update.
- Add inline comments on every non-trivial line.
- Output ONLY the EHI/EHA CATScript, no explanations.

Generate the complete harness routing script now:"""


# ---------------------------------------------------------------------------
# Drawing prompt (T-604)
# ---------------------------------------------------------------------------

def build_drawing_prompt(file_info: dict) -> str:
    import json as _json
    info_str = _json.dumps(file_info, ensure_ascii=False, indent=2)
    return f"""\
You are an expert CATIA V5 R27 automation engineer. A CAD file has been analysed below.

CAD FILE ANALYSIS:
{info_str}

Your task: write a complete, syntactically correct CATScript that creates a CATDrawing (technical drawing) from the existing part/product.

RULES:
- Retrieve the active document with CATIA.ActiveDocument.
- Create a new Drawing document: Dim oDrawing As DrawingDocument / Set oDrawing = CATIA.Documents.Add("Drawing").
- Set standard to ISO: oDrawing.Standard = catISO.
- Get the first sheet: Dim oSheet As DrawingSheet / Set oSheet = oDrawing.Sheets.Item(1).
- Add a front view, a top view, and a right view using oSheet.Views.AddDetail or GenerativeViews from the 3D document.
- For each view, set scale to 1:1 (or appropriate from bounding_box_mm).
- Add automatic dimensions using oView.GenerateDimensions if available.
- Fill the title block (oSheet.DrawingComponents) with part name and date if accessible.
- End with oDrawing.Update.
- Add inline comments on every non-trivial line.
- Output ONLY the CATScript code, no explanations.

Generate the complete CATDrawing script now:"""


def build_reverse_prompt(file_info: dict, user_query: str = "") -> str:
    import json as _json
    info_str = _json.dumps(file_info, ensure_ascii=False, indent=2)
    extra = f"\nAdditional user instruction: {user_query}" if user_query.strip() else ""
    return f"""\
You are an expert CATIA V5 R27 automation engineer. A CAD file has been analysed and its structure extracted below.

CAD FILE ANALYSIS:
{info_str}
{extra}

Your task: write a complete, syntactically correct CATScript (VBA) that reproduces this part/assembly from scratch using the CATIA V5 API.

RULES:
- Use Option Explicit. Declare all variables with Dim/As.
- Reproduce all features in order (Pad, Pocket, Hole, Fillet, Pattern, etc.) as found in the analysis.
- Use bounding_box_mm and key_dimensions_mm for realistic dimensions if exact values are unavailable.
- End with oPart.Update.
- Add inline comments on every non-trivial line.
- Output ONLY the CATScript code, no explanations.

Generate the complete CATScript now:"""

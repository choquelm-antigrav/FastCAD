"""Static validator for CATScript / EKL / EHI-EHA — no CATIA runtime needed."""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum


class Severity(str, Enum):
    error   = "error"
    warning = "warning"
    info    = "info"


@dataclass
class Issue:
    severity: Severity
    line:     int | None
    code:     str
    message:  str


# ---------------------------------------------------------------------------
# CATIA V5 API catalog — known valid method / property names
# ---------------------------------------------------------------------------

_CATIA_API: set[str] = {
    # Application / Document
    "CATIA", "ActiveDocument", "Documents", "Open", "Add", "Close", "Save",
    "SaveAs", "Name", "FullName", "Path", "Exists", "SystemService",
    # Part / Product
    "Part", "PartDocument", "Product", "ProductDocument",
    "MainBody", "Bodies", "HybridBodies", "AxisSystems", "Constraints",
    "Parameters", "Relations", "Sketches", "ShapeFactory",
    "PartBody", "InWorkObject", "Update",
    # Body / HybridBody
    "AddNewBody", "AddNewHybridBody",
    # PartDesign shapes
    "AddNewPad", "AddNewDraftedFilleted", "AddNewShaft",
    "AddNewPocket", "AddNewGroove",
    "AddNewHole", "AddNewStiffener", "AddNewSolid",
    "AddNewFillet", "AddNewEdgeFillet", "AddNewChamfer",
    "AddNewDraft", "AddNewShell", "AddNewThickness",
    "AddNewMirror",
    "AddNewRectPattern", "AddNewCircPattern", "AddNewUserPattern",
    "AddNewBoolean", "AddNewSplit",
    "AddNewLoft", "AddNewSweep",
    # Limit / value setters
    "SetFirstLimit", "SetSecondLimit",
    "SetFirstLimitType", "SetSecondLimitType",
    "SetFirstLimitOffset", "SetSecondLimitOffset",
    "SetFaceToFace", "SetModeInfinite",
    "Value", "ValuateFromString",
    # Hole
    "SetDepth", "SetDiameter", "SetNeckDiameter",
    "SetType", "SetBottomType", "SetHoleThread",
    "SetAnchorMode", "SetPitch",
    # Fillet / Chamfer
    "SetRadius", "SetLength", "SetAngle",
    "AddObjectToFillet", "AddSelectFacesToFillet",
    # Sketch / Sketcher
    "AddNewSketch", "OpenEdition", "CloseEdition", "Sketch",
    "CreateLine", "CreateCircle", "CreatePoint",
    "CreateEllipse", "CreateParabola", "CreateHyperbola",
    "SetConstraint", "AddMonoDimConstraint", "AddBiEltCst",
    "AbsoluteAxis", "HAxis", "VAxis",
    # HybridShapeFactory
    "HybridShapeFactory",
    "AddNewPointCoord", "AddNewPointOnCurve", "AddNewPointOnPlane",
    "AddNewPointMean",
    "AddNewLine", "AddNewLinePtDir", "AddNewLinePtPt",
    "AddNewPlaneOffset", "AddNewPlane3Points", "AddNewPlaneNormal",
    "AddNewCircle3Points", "AddNewCircleCtrPt",
    "AddNewSpline", "AddNewProjectionPt",
    "AddNewExtract", "AddNewSurfacicExtrude",
    "AddNewFill", "AddNewRotate", "AddNewTranslate",
    "AddNewSymmetry", "AddNewAffinity",
    "AddNewNear", "AddNewCombine",
    "AppendNewInput",
    # Common collections
    "Item", "Count", "Remove", "Replace",
    "GetItem", "GetBoundary", "GetDefaultValue",
    "GetLength", "GetAngle", "GetArea", "GetVolume",
    # Selection
    "Selection", "Clear", "Add2", "Search", "VisProperties",
    "SelectElement2", "SelectElement3",
    "IndicateOrSelectElement2D", "IndicateOrSelectElement3D",
    # Parameters / Formulas
    "CreateDimension", "CreateReal", "CreateInteger", "CreateBoolean",
    "CreateString", "CreateList", "CreateEnumere",
    "AddFormula", "AddExternalFile",
    "Rename", "Hide", "Show",
    "DirectPointers",
    # Sheet Metal Design (SMD)
    "SheetMetalFactory", "SheetMetalParameters",
    "AddNewWall", "AddNewWallOnEdge",
    "AddNewFlange", "AddNewHemFlange", "AddNewUserFlange",
    "AddNewCutout",
    "AddNewCircStamp", "AddNewSurfaceStamp",
    "AddNewBridge", "AddNewJoggle",
    "AddNewBend", "AddNewUnfold", "AddNewFold",
    "AddNewCorner", "AddNewChamfer",
    "AddNewStiffenerRib", "AddNewFlangeHole",
    "Wall", "Flange", "HemFlange", "UserFlange",
    "Cutout", "CircStamp", "SurfaceStamp",
    "Bridge", "Joggle", "Bend", "Corner", "StiffenerRib",
    "DiameterBottom", "DiameterTop", "DraftAngle", "HemType",
    "BendRadius", "BendAngle", "KFactor", "Thickness",
    "ReliefType", "Offset",
    # Electrical (EHI / EHA)
    "ElecHarnessInstallation", "ElecHarnessBundle",
    "ElecBundleSegment", "ElecProtection",
    "AddRoutingPoint", "InsertRoutingPoint",
    "SetBendRadius", "SetProtection",
    "ElecFlattening", "ElecFlatteningFactory",
    "GetElecHarnessInstallation",
    # Axis system
    "AddNewAxisSystem", "SetSpecificAxes", "SetOriginPoint",
    "SetXAxis", "SetYAxis", "SetZAxis",
    # Display
    "VisProperties", "SetVisibilityInheritance",
    "GetVisibilityInheritance",
    "GraphicProperties",
}

# Methods that LLMs frequently hallucinate — mapped to the correct name
_COMMON_TYPOS: dict[str, str] = {
    "SetFirstLimits":       "SetFirstLimit",
    "SetSecondLimits":      "SetSecondLimit",
    "AddPad":               "AddNewPad",
    "AddPocket":            "AddNewPocket",
    "AddShaft":             "AddNewShaft",
    "AddHole":              "AddNewHole",
    "AddFillet":            "AddNewFillet",
    "AddChamfer":           "AddNewChamfer",
    "AddSketch":            "AddNewSketch",
    "AddBody":              "AddNewBody",
    "CreateBody":           "AddNewBody",
    "AddNewPointXYZ":       "AddNewPointCoord",
    "GetFeatureByName":     "GetItem",
    "GetElementByName":     "GetItem",
    "SetLength":            "SetFirstLimit (ou ValuateFromString sur un paramètre)",
    "AddNewPadDef":         "AddNewPad",
    "CreateDim":            "CreateDimension",
    "SetConstraints":       "SetConstraint",
    "AddMirror":            "AddNewMirror",
    "AddPattern":           "AddNewRectPattern ou AddNewCircPattern",
    "SetDiam":              "SetDiameter",
    "AddNewElecBundleSegment": "ElecBundleSegment (depuis ElecHarnessInstallation)",
    "AddElecBundleSegment":    "ElecBundleSegment",
    # Sheet Metal typos
    "AddWall":              "AddNewWall",
    "AddFlange":            "AddNewFlange",
    "AddNewBride":          "AddNewFlange",
    "AddStamp":             "AddNewCircStamp ou AddNewSurfaceStamp",
    "AddNewStamp":          "AddNewCircStamp ou AddNewSurfaceStamp",
    "AddCutout":            "AddNewCutout",
    "SheetMetal":           "SheetMetalFactory (via GetTechnologicalObject)",
    "GetSheetMetal":        "GetTechnologicalObject(\"SheetMetalFactory\")",
    "SetThickness":         "oParams.Thickness.Value = X",
    "SetBendRadius":        "oParams.BendRadius.Value = X",
}

# Regex for method calls: .MethodName(
_RE_METHOD_CALL = re.compile(r'\.([A-Za-z][A-Za-z0-9_]*)(?:\s*\(|\s+[^=])')


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _lines(script: str) -> list[str]:
    return script.splitlines()


def _strip_comments(line: str) -> str:
    """Remove VBA inline comment (anything after a standalone ')."""
    in_str = False
    for i, ch in enumerate(line):
        if ch == '"':
            in_str = not in_str
        elif ch == "'" and not in_str:
            return line[:i]
    return line


def _find_line(script: str, pattern: str) -> int | None:
    for i, line in enumerate(_lines(script), 1):
        if pattern in line:
            return i
    return None


# ---------------------------------------------------------------------------
# CATScript / VBA validator
# ---------------------------------------------------------------------------

def _validate_catscript(script: str) -> list[Issue]:
    issues: list[Issue] = []
    raw_lines = _lines(script)

    # ── E001 : Option Explicit ───────────────────────────────────────────
    if not re.search(r'(?i)^\s*Option\s+Explicit', script, re.MULTILINE):
        issues.append(Issue(Severity.error, 1, "E001",
                            "Option Explicit manquant — variables non déclarées non détectées par CATIA"))

    # ── E002 : Sub / End Sub balance ────────────────────────────────────
    sub_open  = len(re.findall(r'(?im)^\s*(?:Public\s+|Private\s+)?Sub\s+\w+', script))
    sub_close = len(re.findall(r'(?im)^\s*End\s+Sub', script))
    if sub_open != sub_close:
        issues.append(Issue(Severity.error, None, "E002",
                            f"Déséquilibre Sub/End Sub : {sub_open} Sub, {sub_close} End Sub"))

    # ── E003 : Function / End Function ──────────────────────────────────
    fn_open  = len(re.findall(r'(?im)^\s*(?:Public\s+|Private\s+)?Function\s+\w+', script))
    fn_close = len(re.findall(r'(?im)^\s*End\s+Function', script))
    if fn_open != fn_close:
        issues.append(Issue(Severity.error, None, "E003",
                            f"Déséquilibre Function/End Function : {fn_open} ouverts, {fn_close} fermés"))

    # ── E004 : If / End If ──────────────────────────────────────────────
    if_open  = len(re.findall(r'(?im)^\s*If\b.*\bThen\s*$', script))
    if_close = len(re.findall(r'(?im)^\s*End\s+If', script))
    if if_open != if_close:
        issues.append(Issue(Severity.error, None, "E004",
                            f"Déséquilibre If/End If : {if_open} If blocs, {if_close} End If"))

    # ── E005 : For / Next ───────────────────────────────────────────────
    for_open  = len(re.findall(r'(?im)^\s*For\b', script))
    for_close = len(re.findall(r'(?im)^\s*Next\b', script))
    if for_open != for_close:
        issues.append(Issue(Severity.error, None, "E005",
                            f"Déséquilibre For/Next : {for_open} For, {for_close} Next"))

    # ── E006 : With / End With ──────────────────────────────────────────
    with_open  = len(re.findall(r'(?im)^\s*With\b', script))
    with_close = len(re.findall(r'(?im)^\s*End\s+With', script))
    if with_open != with_close:
        issues.append(Issue(Severity.error, None, "E006",
                            f"Déséquilibre With/End With : {with_open} With, {with_close} End With"))

    # ── E007 : typos / méthodes inconnues ───────────────────────────────
    for lineno, line in enumerate(raw_lines, 1):
        clean = _strip_comments(line)
        for m in _RE_METHOD_CALL.finditer(clean):
            name = m.group(1)
            if name in _COMMON_TYPOS:
                issues.append(Issue(Severity.error, lineno, "E007",
                                    f"Méthode inconnue « .{name}() » — probablement : .{_COMMON_TYPOS[name]}()"))
            elif name not in _CATIA_API and len(name) > 3:
                # Only flag if it looks like a CATIA API call (PascalCase with >3 chars)
                if re.match(r'^[A-Z][a-z]', name) and name not in {
                    "New", "Set", "Get", "Add", "Create", "Remove", "Open",
                    "Close", "Save", "Run", "Show", "Hide",
                }:
                    issues.append(Issue(Severity.warning, lineno, "W005",
                                        f"Méthode « .{name}() » non répertoriée dans l'API CATIA V5 connue — vérifier la syntaxe"))

    # ── W001 : .Update() manquant ───────────────────────────────────────
    if not re.search(r'(?i)\.Update\s*\(\s*\)', script):
        issues.append(Issue(Severity.warning, None, "W001",
                            ".Update() manquant en fin de script — la pièce ne sera pas recalculée"))

    # ── W002 : variables Dim déclarées mais jamais utilisées ────────────
    dim_re = re.compile(r'(?im)^\s*Dim\s+(\w+)\s+As\b')
    for m in dim_re.finditer(script):
        var = m.group(1)
        lineno = script[:m.start()].count('\n') + 1
        # Variable is "used" if it appears more than once (the Dim itself + at least one other)
        occurrences = len(re.findall(r'\b' + re.escape(var) + r'\b', script))
        if occurrences < 2:
            issues.append(Issue(Severity.warning, lineno, "W002",
                                f"Variable « {var} » déclarée mais jamais utilisée"))

    # ── W003 : Dim sans type (mauvaise pratique VBA) ────────────────────
    for lineno, line in enumerate(raw_lines, 1):
        clean = _strip_comments(line)
        if re.match(r'(?i)\s*Dim\s+\w+\s*$', clean):
            issues.append(Issue(Severity.warning, lineno, "W003",
                                "Dim sans type explicite (As ...) — variable typée Object implicitement"))

    # ── I001 : statistiques ──────────────────────────────────────────────
    dim_count = len(dim_re.findall(script))
    api_calls = len(_RE_METHOD_CALL.findall(script))
    issues.append(Issue(Severity.info, None, "I001",
                        f"{len(raw_lines)} lignes · {dim_count} variables · ~{api_calls} appels API"))

    return issues


# ---------------------------------------------------------------------------
# EKL validator
# ---------------------------------------------------------------------------

_EKL_BLOCKS = re.compile(
    r'(?im)^\s*(Rule|Check|Reaction|Set|DesignTable|ExternalFile)\s+\w+', re.MULTILINE
)


def _validate_ekl(script: str) -> list[Issue]:
    issues: list[Issue] = []
    raw_lines = _lines(script)

    # ── E010 : bloc Rule/Check/Reaction manquant ────────────────────────
    if not _EKL_BLOCKS.search(script):
        issues.append(Issue(Severity.error, 1, "E010",
                            "Aucun bloc Rule / Check / Reaction détecté — structure EKL invalide"))

    # ── E011 : let pour les déclarations ────────────────────────────────
    has_let = bool(re.search(r'(?im)^\s*let\b', script))
    if not has_let:
        issues.append(Issue(Severity.warning, None, "E011",
                            "Aucun `let` trouvé — les variables EKL doivent être déclarées avec let"))

    # ── E012 : références backtick ──────────────────────────────────────
    if '`' not in script:
        issues.append(Issue(Severity.warning, None, "E012",
                            "Aucune référence backtick (`) trouvée — accès aux features CATIA via `PartBody\\\\Feature`"))

    # ── W010 : End Rule / End Check manquant ────────────────────────────
    rule_open  = len(re.findall(r'(?im)^\s*Rule\b',  script))
    rule_close = len(re.findall(r'(?im)^\s*End\s+Rule', script))
    if rule_open != rule_close:
        issues.append(Issue(Severity.error, None, "W010",
                            f"Déséquilibre Rule/End Rule : {rule_open} Rule, {rule_close} End Rule"))

    check_open  = len(re.findall(r'(?im)^\s*Check\b',  script))
    check_close = len(re.findall(r'(?im)^\s*End\s+Check', script))
    if check_open != check_close:
        issues.append(Issue(Severity.error, None, "W011",
                            f"Déséquilibre Check/End Check : {check_open} Check, {check_close} End Check"))

    issues.append(Issue(Severity.info, None, "I010",
                        f"{len(raw_lines)} lignes EKL"))
    return issues


# ---------------------------------------------------------------------------
# EHI / EHA validator (CATScript + vérifications spécifiques harnais)
# ---------------------------------------------------------------------------

def _validate_ehi(script: str) -> list[Issue]:
    issues = _validate_catscript(script)

    # ── W020 : ElecHarnessInstallation / ElecBundleSegment manquants ────
    if "ElecHarnessInstallation" not in script and "ElecHarnessBundle" not in script:
        issues.append(Issue(Severity.error, None, "E020",
                            "ElecHarnessInstallation introuvable — objet racine du harnais manquant"))

    if "ElecBundleSegment" not in script:
        issues.append(Issue(Severity.warning, None, "W020",
                            "ElecBundleSegment introuvable — aucun segment de faisceau déclaré"))

    if "AddRoutingPoint" not in script:
        issues.append(Issue(Severity.warning, None, "W021",
                            "AddRoutingPoint introuvable — les points de routage 3D sont manquants"))

    if not re.search(r'(?i)SetDiameter', script):
        issues.append(Issue(Severity.warning, None, "W022",
                            "SetDiameter introuvable — le diamètre des segments n'est pas défini"))

    return issues


# ---------------------------------------------------------------------------
# Sheet Metal validator
# ---------------------------------------------------------------------------

def _validate_sheetmetal(script: str) -> list[Issue]:
    issues = _validate_catscript(script)

    # E030 : SheetMetalFactory access
    if "GetTechnologicalObject" not in script or "SheetMetalFactory" not in script:
        issues.append(Issue(Severity.error, None, "E030",
                            "SheetMetalFactory introuvable — "
                            "utiliser : oPart.GetTechnologicalObject(\"SheetMetalFactory\")"))

    # E031 : SheetMetalParameters (épaisseur)
    if "SheetMetalParameters" not in script and "Thickness" not in script:
        issues.append(Issue(Severity.warning, None, "E031",
                            "SheetMetalParameters non initialisé — Thickness et BendRadius non définis"))

    # E032 : au moins une paroi de base
    if "AddNewWall" not in script:
        issues.append(Issue(Severity.warning, None, "E032",
                            "AddNewWall introuvable — aucune paroi de base créée"))

    # E033 : esquisse fermée requise
    if "CloseEdition" not in script:
        issues.append(Issue(Severity.warning, None, "E033",
                            "CloseEdition introuvable — les esquisses doivent être fermées avant AddNewWall"))

    # I030 : résumé des features SMD
    smd_features = {
        "AddNewWall": "Wall", "AddNewFlange": "Flange", "AddNewHemFlange": "HemFlange",
        "AddNewCutout": "Cutout", "AddNewCircStamp": "CircStamp",
        "AddNewSurfaceStamp": "SurfaceStamp", "AddNewBridge": "Bridge",
        "AddNewJoggle": "Joggle", "AddNewBend": "Bend", "AddNewStiffenerRib": "Rib",
    }
    found = [label for method, label in smd_features.items() if method in script]
    if found:
        issues.append(Issue(Severity.info, None, "I030",
                            f"Features SMD détectées : {', '.join(found)}"))

    return issues


# ---------------------------------------------------------------------------
# Auto-detect Sheet Metal scripts
# ---------------------------------------------------------------------------

_SM_MARKERS = {"SheetMetalFactory", "SheetMetalParameters", "AddNewWall", "AddNewFlange",
               "AddNewCircStamp", "AddNewSurfaceStamp", "AddNewCutout", "AddNewJoggle"}

def _is_sheetmetal_script(script: str) -> bool:
    return sum(1 for m in _SM_MARKERS if m in script) >= 2


# ---------------------------------------------------------------------------
# Public entry-point
# ---------------------------------------------------------------------------

def validate(script: str, script_type: str) -> list[Issue]:
    """
    Run static checks on a generated script.

    Parameters
    ----------
    script      : raw script text
    script_type : 'catscript' | 'ekl' | 'ehi_eha'

    Returns
    -------
    Ordered list of Issue (errors first, then warnings, then info).
    """
    if not script.strip():
        return [Issue(Severity.error, None, "E000", "Script vide")]

    st = script_type.lower()
    if "ekl" in st:
        raw = _validate_ekl(script)
    elif "ehi" in st or "eha" in st:
        raw = _validate_ehi(script)
    elif "sheetmetal" in st or "sheet_metal" in st or "sheet metal" in st:
        raw = _validate_sheetmetal(script)
    elif _is_sheetmetal_script(script):
        raw = _validate_sheetmetal(script)
    else:
        raw = _validate_catscript(script)

    order = {Severity.error: 0, Severity.warning: 1, Severity.info: 2}
    return sorted(raw, key=lambda i: order[i.severity])

"""Parse CAD files (STEP, CATPart, CATProduct) without heavy dependencies."""
from __future__ import annotations
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path


def parse_cad_file(path: Path) -> dict:
    """Return a dict describing the CAD file structure for prompt building."""
    suffix = path.suffix.lower()
    if suffix in (".stp", ".step"):
        return _parse_step(path)
    if suffix == ".catpart":
        return _parse_catpart(path)
    if suffix == ".catproduct":
        return _parse_catproduct(path)
    return {"type": "unknown", "name": path.stem, "raw": f"Format non reconnu : {suffix}"}


def _parse_step(path: Path) -> dict:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return {"type": "step", "name": path.stem, "error": "Lecture impossible"}

    products = re.findall(r"PRODUCT\s*\(\s*'([^']*)'", text)
    points   = re.findall(r"CARTESIAN_POINT\s*\(\s*'[^']*'\s*,\s*\(([^)]+)\)", text)
    lengths  = re.findall(r"LENGTH_MEASURE\s*\(\s*([\d.]+)\s*\)", text)
    shells   = len(re.findall(r"CLOSED_SHELL", text))
    faces    = len(re.findall(r"ADVANCED_FACE", text))

    coords = []
    for p in points[:200]:
        try:
            coords.append([float(x) for x in p.split(",")])
        except ValueError:
            pass

    bbox = {}
    if coords:
        xs = [c[0] for c in coords if len(c) > 0]
        ys = [c[1] for c in coords if len(c) > 1]
        zs = [c[2] for c in coords if len(c) > 2]
        bbox = {
            "x": round(max(xs) - min(xs), 1),
            "y": round(max(ys) - min(ys), 1),
            "z": round(max(zs) - min(zs), 1),
        }

    dim_values = sorted(set(round(float(v), 1) for v in lengths if float(v) > 0.1))[:20]

    return {
        "type": "step",
        "name": products[0] if products else path.stem,
        "shells": shells,
        "faces": faces,
        "bounding_box_mm": bbox,
        "key_dimensions_mm": dim_values,
        "all_products": products[:10],
    }


def _parse_catpart(path: Path) -> dict:
    if not zipfile.is_zipfile(path):
        return {"type": "catpart", "name": path.stem, "error": "Fichier CATPart illisible (non-ZIP)"}
    try:
        with zipfile.ZipFile(path) as zf:
            xml_files = [n for n in zf.namelist() if n.endswith(".xml") or "Part" in n]
            features, params = [], []
            for xf in xml_files[:5]:
                try:
                    root = ET.fromstring(zf.read(xf))
                    for el in root.iter():
                        tag = el.tag.split("}")[-1] if "}" in el.tag else el.tag
                        name = el.get("Name", el.get("name", ""))
                        if tag in ("Pad", "Pocket", "Shaft", "Groove", "Hole", "Fillet", "Chamfer",
                                   "CircPattern", "RectPattern", "Mirror", "Shell", "Sweep", "Loft"):
                            features.append({"feature": tag, "name": name})
                        if tag in ("Parameter", "RealParam", "IntParam", "BoolParam"):
                            val = el.get("Value", el.get("value", ""))
                            if name and val:
                                params.append({"name": name, "value": val})
                except ET.ParseError:
                    continue
        return {
            "type": "catpart",
            "name": path.stem,
            "features": features[:30],
            "parameters": params[:20],
        }
    except Exception as e:
        return {"type": "catpart", "name": path.stem, "error": str(e)[:120]}


def _parse_catproduct(path: Path) -> dict:
    if not zipfile.is_zipfile(path):
        return {"type": "catproduct", "name": path.stem, "error": "Fichier CATProduct illisible"}
    try:
        with zipfile.ZipFile(path) as zf:
            xml_files = [n for n in zf.namelist() if n.endswith(".xml")]
            components, constraints = [], []
            for xf in xml_files[:5]:
                try:
                    root = ET.fromstring(zf.read(xf))
                    for el in root.iter():
                        tag = el.tag.split("}")[-1] if "}" in el.tag else el.tag
                        if tag in ("Component", "Instance", "Reference"):
                            components.append(el.get("Name", el.get("name", "")))
                        if tag in ("Constraint", "Contact", "Coincidence", "Offset", "Angle"):
                            constraints.append(tag)
                except ET.ParseError:
                    continue
        return {
            "type": "catproduct",
            "name": path.stem,
            "components": [c for c in components if c][:20],
            "constraints": constraints[:20],
        }
    except Exception as e:
        return {"type": "catproduct", "name": path.stem, "error": str(e)[:120]}

"""
seed_knowledge.py — Génère le PDF de référence CATIA V5 et l'ingère dans ChromaDB.
Usage : python scripts/seed_knowledge.py
"""

from pathlib import Path
import sys

import fitz

ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT / "data" / "pdf_docs"
DOCS_DIR.mkdir(parents=True, exist_ok=True)

CATIA_REFERENCE = """
CATIA V5 R27 — RÉFÉRENCE SCRIPTING COMPLÈTE
============================================

=== PARTIE 1 : CATSCRIPT / VBA ===

--- 1.1 Structure d'un macro CATScript ---

Option Explicit

Sub CATMain()
    Dim oDoc As Document
    Dim oPart As Part
    Dim oBody As Body
    Set oDoc = CATIA.ActiveDocument
    Set oPart = oDoc.Part
    Set oBody = oPart.MainBody
    ' ... logique métier ...
    oPart.Update
End Sub

--- 1.2 Objets principaux CATIA ---

CATIA                   : objet racine de l'application CATIA
CATIA.ActiveDocument    : document actif (PartDocument, ProductDocument, DrawingDocument)
CATIA.Documents         : collection de tous les documents ouverts
CATIA.ActiveDocument.Part : objet Part (accès à la géométrie)

PartDocument   : document de pièce (.CATPart)
ProductDocument : document assemblage (.CATProduct)
DrawingDocument : document dessin (.CATDrawing)

Part           : représente la pièce 3D
Part.Bodies    : collection des corps (Body)
Part.MainBody  : corps principal
Part.Parameters : collection des paramètres
Part.Relations : collection des relations (formules, règles EKL)
Part.Update    : régénère le modèle

Body           : corps géométrique (contient les features)
Body.Shapes    : collection des formes
Body.Name      : nom du corps

--- 1.3 ShapeFactory — Création de features ---

Dim oSF As ShapeFactory
Set oSF = oPart.ShapeFactory

' Pad (extrusion)
Dim oPad As Pad
Set oPad = oSF.AddNewPad(oSketch, 10.0)   ' sketch + hauteur en mm
oPad.Name = "Pad.1"
oPad.IsSymmetric = False
oPad.SecondLimit.Dimension.Value = 0

' Pocket (enlèvement de matière)
Dim oPocket As Pocket
Set oPocket = oSF.AddNewPocket(oSketch, 5.0)
oPocket.Name = "Pocket.1"

' Hole (perçage)
Dim oHole As Hole
Set oHole = oSF.AddNewHole(oFace, 8.0)    ' face + profondeur
oHole.Diameter.Value = 5.0
oHole.HoleType = catSimpleHole
oHole.BottomType = catFlatHoleBottom

' Fillet (congé d'arête)
Dim oFillet As ConstRadEdgeFillet
Set oFillet = oSF.AddNewSolidEdgeFilletWithConstantRadius(oEdge, catTangencyFilletEdgePropagation, 2.0)

' Chamfer (chanfrein)
Dim oChamfer As Chamfer
Set oChamfer = oSF.AddNewChamfer(oEdge, catTangencyFilletEdgePropagation, 1.0, 45.0, catD1Angle1Chamfer)

' Shell (coque — enlèvement faces)
Dim oShell As Shell
Set oShell = oSF.AddNewShell(oFacesToRemove, 2.0)

' Mirror (symétrie)
Dim oMirror As Mirror
Set oMirror = oSF.AddNewMirror(oMirrorPlane)

' LinearPattern (répétition linéaire)
Dim oPattern As RectPattern
Set oPattern = oSF.AddNewRectPattern(oFeature, 3, 2, 10.0, 8.0, 1, 1, oDir1, oDir2, True, True, 0)

--- 1.4 Sketcher — Croquis 2D ---

' Ouvrir un sketch sur un plan
Dim oSketchFact As Sketches
Set oSketchFact = oBody.Sketches
Dim oPlane As Reference
Set oPlane = oPart.CreateReferenceFromName("xy plane")
Dim oSketch As Sketch
Set oSketch = oSketchFact.Add(oPlane)

' Ouvrir l'atelier sketcher
Dim oSE As SketchBasedShapeFactory
Dim oFactory2D As Factory2D
Set oFactory2D = oSketch.OpenEdition

' Tracer des éléments 2D
Dim oLine As Line2D
Set oLine = oFactory2D.CreateLine(0, 0, 100, 0)

Dim oCircle As Circle2D
Set oCircle = oFactory2D.CreateCircle(50, 50, 0, 0, 0)
oCircle.CenterPoint.X = 50
oCircle.CenterPoint.Y = 50
oCircle.Radius = 15

Dim oPoint As Point2D
Set oPoint = oFactory2D.CreatePoint(25, 0)

' Rectangle (4 lignes)
Dim oProfile As Profile
Dim oLines(3) As Line2D
Set oLines(0) = oFactory2D.CreateLine(0, 0, 50, 0)
Set oLines(1) = oFactory2D.CreateLine(50, 0, 50, 30)
Set oLines(2) = oFactory2D.CreateLine(50, 30, 0, 30)
Set oLines(3) = oFactory2D.CreateLine(0, 30, 0, 0)

' Fermer le sketch
oSketch.CloseEdition

--- 1.5 Factory2D — API complète des éléments 2D ---

IMPORTANT : Factory2D est l'objet retourné par oSketch.OpenEdition
Il permet de tracer tous les éléments géométriques 2D dans un sketch.

' Système de coordonnées : H (horizontal) et V (vertical) en mm
' Origine = origine du plan de sketch (pas forcément l'origine CATIA)

' === LIGNES ===
' CreateLine(x1, y1, x2, y2) -> Line2D
Dim oLine As Line2D
Set oLine = oFactory2D.CreateLine(0.0, 0.0, 100.0, 0.0)
' Propriétés : oLine.StartPoint, oLine.EndPoint

' === POINTS ===
' CreatePoint(x, y) -> Point2D
Dim oPoint As Point2D
Set oPoint = oFactory2D.CreatePoint(50.0, 25.0)

' === CERCLES et ARCS ===
' CreateCircle(centerX, centerY, radius, startAngle, endAngle) -> Circle2D
' ATTENTION : startAngle et endAngle sont en RADIANS (pas en degrés)
' Cercle complet : startAngle=0, endAngle=6.2832 (=2*pi)
' Arc de 0 à 90 deg : startAngle=0, endAngle=1.5708 (=pi/2)
Dim oCircle As Circle2D
Set oCircle = oFactory2D.CreateCircle(50.0, 50.0, 15.0, 0.0, 6.2832)  ' cercle complet
Set oArc = oFactory2D.CreateCircle(0.0, 0.0, 10.0, 0.0, 1.5708)       ' arc 0->90 deg

' Propriétés Circle2D : oCircle.CenterPoint.X, oCircle.CenterPoint.Y, oCircle.Radius

' === ELLIPSES ===
' CreateEllipse(centerX, centerY, semiMajorAxis, semiMinorAxis, angle) -> Ellipse2D
Dim oEllipse As Ellipse2D
Set oEllipse = oFactory2D.CreateEllipse(50.0, 50.0, 30.0, 15.0, 0.0)

' === SPLINES ===
' Créer une spline par points de contrôle
Dim oSpline As Spline2D
Set oSpline = oFactory2D.CreateSpline(Array(0.0, 10.0, 20.0, 30.0), Array(0.0, 15.0, 5.0, 0.0))
' Array des X et Array des Y (nombre identique de points)

' === POLYLIGNES (via lignes connectées) ===
' CATIA n'a pas de CreatePolyline direct : tracer N lignes connectées
Dim oL1 As Line2D, oL2 As Line2D, oL3 As Line2D
Set oL1 = oFactory2D.CreateLine(0, 0, 30, 0)
Set oL2 = oFactory2D.CreateLine(30, 0, 30, 20)
Set oL3 = oFactory2D.CreateLine(30, 20, 0, 20)

' === PROFIL FERMÉ POUR EXTRUSION ===
' Un profil DOIT être fermé (le dernier point = le premier point)
' Rectangle fermé 50x30 centré sur l'origine :
Set oFactory2D = oSketch.OpenEdition
Dim r1 As Line2D, r2 As Line2D, r3 As Line2D, r4 As Line2D
Set r1 = oFactory2D.CreateLine(-25, -15, 25, -15)  ' bas
Set r2 = oFactory2D.CreateLine(25, -15, 25, 15)    ' droite
Set r3 = oFactory2D.CreateLine(25, 15, -25, 15)    ' haut
Set r4 = oFactory2D.CreateLine(-25, 15, -25, -15)  ' gauche
oSketch.CloseEdition
' NOTE : les lignes doivent être adjacentes (r1.EndPoint = r2.StartPoint, etc.)
' Si les extrémités ne coïncident pas exactement, le pad échouera

' === RECTANGLE ARRONDI (rectangle + arcs aux coins) ===
' Exemple : rectangle 60x40 avec congés R5 aux coins
Set oFactory2D = oSketch.OpenEdition
' Côtés droits (laissant de la place pour les arcs R5)
Set oFactory2D.CreateLine(-25, -15, 25, -15)   ' bas droit
Set oFactory2D.CreateLine(25, 15, -25, 15)     ' haut gauche
Set oFactory2D.CreateLine(30, -10, 30, 10)     ' côté droit
Set oFactory2D.CreateLine(-30, 10, -30, -10)   ' côté gauche
' Arcs aux coins (quart de cercle R=5)
' pi/2 = 1.5708, pi = 3.1416, 3pi/2 = 4.7124
Set oFactory2D.CreateCircle(25, -10, 5, 4.7124, 6.2832)   ' coin bas-droit  (270->360)
Set oFactory2D.CreateCircle(25, 10, 5, 0, 1.5708)         ' coin haut-droit  (0->90)
Set oFactory2D.CreateCircle(-25, 10, 5, 1.5708, 3.1416)   ' coin haut-gauche (90->180)
Set oFactory2D.CreateCircle(-25, -10, 5, 3.1416, 4.7124)  ' coin bas-gauche (180->270)
oSketch.CloseEdition

' === LIMITATION CRITIQUE : PAS DE TEXTE EN FACTORY2D ===
' CATIA V5 Factory2D N'A PAS de méthode CreateText ou de rendu de fonte.
' Il est IMPOSSIBLE de créer le contour d'une lettre via Factory2D directement.
' Pour créer du texte en relief :
'   Option A : Utiliser les Annotations 3D (FTA/FTADocument) — affichage seulement, pas de solide
'   Option B : Tracer manuellement les contours lettre par lettre avec CreateLine/CreateArc
'   Option C : Importer un DXF contenant les profils de texte converti en géométrie
'   Option D : Utiliser un User Feature (UDF) pré-construit avec les lettres
' La solution la plus pratique en CATScript est d'utiliser le module "Annotations 3D"
' ou de tracer les contours des lettres manuellement.

' === ANNOTATIONS 3D (texte non-extrudé) ===
' Pour afficher du texte en 3D (pas en relief) dans CATIA V5 :
Dim oAnnotations As Annotations
Set oAnnotations = CATIA.ActiveDocument.Part.Annotations
Dim oAnnotation As Annotation
Set oAnnotation = oAnnotations.Add("FASTCAD")
oAnnotation.Text.Caption = "FASTCAD"
' L'annotation est un texte 3D visible mais non-solide

--- 1.6 Contraintes du Sketcher ---

Dim oCst As Constraints
Set oCst = oSketch.Constraints

' Contrainte de dimension (longueur)
Dim oRef1 As Reference
Set oRef1 = oPart.CreateReferenceFromObject(oLine)
Dim oDimCst As Constraint
Set oDimCst = oCst.AddMonoEltCst(catCstTypeLength, oRef1)
oDimCst.Dimension.Value = 100.0

' Contrainte de coïncidence
Set oCst2 = oCst.AddBiEltCst(catCstTypeCoincidence, oRef1, oRef2)

' Contrainte de fixation
Set oCstFix = oCst.AddMonoEltCst(catCstTypeReference, oRefPoint)

--- 1.7 Paramètres et Formules ---

' Créer un paramètre
Dim oParams As Parameters
Set oParams = oPart.Parameters

Dim oLength As RealParam
Set oLength = oParams.CreateDimension("Longueur", "LENGTH", 100.0)
oLength.Value = 100.0

Dim oAngle As RealParam
Set oAngle = oParams.CreateDimension("Angle_debouche", "ANGLE", 45.0)

' Créer une formule
Dim oRelations As Relations
Set oRelations = oPart.Relations
Dim oFormula As Formula
Set oFormula = oRelations.CreateFormula("f_largeur", "", oWidthParam, "Longueur / 2")

--- 1.8 Gestion des plans de référence ---

' Plans standards
Dim oXYPlane As Reference
Set oXYPlane = oPart.CreateReferenceFromName("xy plane")
Dim oYZPlane As Reference
Set oYZPlane = oPart.CreateReferenceFromName("yz plane")
Dim oZXPlane As Reference
Set oZXPlane = oPart.CreateReferenceFromName("zx plane")

' Plan décalé
Dim oHybridShapes As HybridShapes
Set oHybridShapes = oBody.HybridShapes
Dim oOffset As HybridShapePointOnPlane
Dim oNewPlane As HybridShapePlaneOffset
Set oNewPlane = oHybridShapes.AddNewPlaneOffset(oXYPlane, 50.0, False)

--- 1.9 Sélections et références ---

' Référence depuis un nom (format CATIA interne)
Dim oRef As Reference
Set oRef = oPart.CreateReferenceFromName("PartBody\\Pad.1\\Face.1")

' Référence depuis un objet
Set oRef = oPart.CreateReferenceFromObject(oPad)

' Récupérer un feature par nom
Dim oFeat As AnyObject
Set oFeat = oPart.FindObjectByName("Pad.1")

--- 1.10 Messages et interactions ---

' Afficher un message
MsgBox "Opération terminée", vbInformation, "CATScript"

' Saisie utilisateur
Dim sInput As String
sInput = InputBox("Entrez la longueur (mm):", "Paramètre", "100")
Dim dValue As Double
dValue = CDbl(sInput)

' Barre de progression (via StatusBar)
CATIA.StatusBar = "Traitement en cours..."

--- 1.11 Patterns de robustesse ---

' Toujours tester si le document est bien une pièce
If Not TypeOf CATIA.ActiveDocument Is PartDocument Then
    MsgBox "Ce macro nécessite un document Part actif.", vbCritical
    Exit Sub
End If

' Gestion d'erreur basique
On Error GoTo ErrHandler
' ... code ...
Exit Sub
ErrHandler:
    MsgBox "Erreur : " & Err.Description, vbCritical
    oPart.Update

=== PARTIE 1B : CATSCRIPT — FEATURES AVANCÉES ===

--- 1B.1 Shaft — Révolution solide ---

' Shaft = révolution d'un profil autour d'un axe
' Le sketch DOIT contenir : 1 profil fermé + 1 ligne d'axe (déclarée comme axe)
' La ligne d'axe doit être tracée dans le sketch et contrainte comme "Axe"

Dim oShaft As Shaft
' Révolution 360° complète :
Set oShaft = oSF.AddNewShaft(oSketch, 0.0, 360.0)
oShaft.Name = "Shaft_Corps"

' Révolution partielle (180°) :
Set oShaft = oSF.AddNewShaft(oSketch, 0.0, 180.0)

' Révolution symétrique (±30°) :
Set oShaft = oSF.AddNewShaft(oSketch, -30.0, 30.0)

' Exemple de sketch pour Shaft (profil + axe) :
Dim oSkShaft As Sketch
Set oSkShaft = oBody.Sketches.Add(oPart.CreateReferenceFromName("zx plane"))
Dim oFShaft As Factory2D
Set oFShaft = oSkShaft.OpenEdition
' Axe de révolution (ligne verticale H=0)
Dim oAxis As Line2D
Set oAxis = oFShaft.CreateLine(0.0, 0.0, 0.0, 80.0)
' Contraindre la ligne comme axe (nécessaire pour Shaft)
Dim oCstAxis As Constraint
Dim oAxisRef As Reference
Set oAxisRef = oPart.CreateReferenceFromObject(oAxis)
oSkShaft.Constraints.AddMonoEltCst(catCstTypeAxis, oAxisRef)
' Profil L-shape (demi-profil à droite de l'axe)
oFShaft.CreateLine(10.0, 0.0,  40.0,  0.0)   ' base basse
oFShaft.CreateLine(40.0, 0.0,  40.0, 30.0)   ' flanc externe
oFShaft.CreateLine(40.0, 30.0, 20.0, 30.0)   ' épaulement
oFShaft.CreateLine(20.0, 30.0, 20.0, 80.0)   ' flanc interne haut
oFShaft.CreateLine(20.0, 80.0, 10.0, 80.0)   ' sommet
oFShaft.CreateLine(10.0, 80.0, 10.0,  0.0)   ' flanc interne bas
oSkShaft.CloseEdition
Set oShaft = oSF.AddNewShaft(oSkShaft, 0.0, 360.0)
oShaft.Name = "Shaft_LShape"

--- 1B.2 Groove — Enlèvement de révolution ---

' Groove = révolution creuse (pocket de révolution)
' Même principe que Shaft : sketch avec profil + axe
Dim oGroove As Groove
Set oGroove = oSF.AddNewGroove(oSketch, 0.0, 360.0)
oGroove.Name = "Groove_Rainure"
' Groove partiel pour rainure latérale :
Set oGroove = oSF.AddNewGroove(oSketch, 0.0, 45.0)

--- 1B.3 Shell — Coque mince (évidement) ---

' Shell = enlèvement de matière par coque (laisse une épaisseur uniforme)
' Argument 1 : référence de la face à supprimer (ouverture)
' Argument 2 : épaisseur de paroi en mm

Dim oShell As Shell
Dim oOpenFace As Reference
' Référencer la face à ouvrir (ici face sup du Pad.1)
Set oOpenFace = oPart.CreateReferenceFromName("PartBody\\Pad.1\\Face.1")
Set oShell = oSF.AddNewShell(oOpenFace, 2.5)
oShell.Name = "Shell_Boitier"
' Modifier l'épaisseur après création :
oShell.Thickness.Value = 3.0
' Ajouter une 2ème face à ouvrir (via SelectionSets) :
' Note : pour plusieurs ouvertures, ajouter les faces à la sélection avant de créer le Shell

--- 1B.4 Rib — Sweep (balayage de profil le long d'une courbe) ---

' Rib = extrusion d'un profil 2D le long d'une courbe guide 3D
' Utilisation : nervures sur arête courbe, tuyaux, joints de profil

' Créer la courbe guide (fil 3D ou esquisse)
Dim oCurveRef As Reference
Set oCurveRef = oPart.CreateReferenceFromName("PartBody\\Sketch.3")

' Créer le Rib
Dim oRib As Rib
Set oRib = oSF.AddNewRib(oSketch, oCurveRef)
oRib.Name = "Rib_Profil"
' Propriétés :
oRib.MergeRib = True    ' fusionner avec le corps

' Pour une gorge (sweep enlèvement) : utiliser AddNewSlot
Dim oSlot As Slot
Set oSlot = oSF.AddNewSlot(oSketch, oCurveRef)
oSlot.Name = "Slot_Gorge"

--- 1B.5 Répétition circulaire (CircPattern) ---

' CircPattern = répétition d'une feature autour d'un axe
' Paramètres : feature, nb d'instances, angle entre instances, axe, centre

Dim oCircPat As CircPattern
' Paramètres : feature, nb_instances, pas_angulaire(deg), axe_ref, original_position
Set oCircPat = oSF.AddNewCircPattern( _
    oHole,     _  ' feature à répéter
    6,         _  ' nombre total d'instances
    60.0,      _  ' pas angulaire (360/6 = 60°)
    1,         _  ' index instance de référence
    1,         _  ' index sens de répétition
    oAxisRef,  _  ' référence de l'axe (ex: yz plane)
    oAxisRef,  _  ' référence du centre
    True,      _  ' rotation radiale des instances
    True,      _  ' instances espacées également
    0.0        _  ' décalage angulaire initial
)
oCircPat.Name = "CircPat_6_Trous"

' Axe Z (axe principal) comme référence :
Dim oAxisZ As Reference
Set oAxisZ = oPart.CreateReferenceFromName("zx plane")

--- 1B.6 Symétrie miroir (Mirror) ---

' Mirror = symétrie d'une feature ou du corps entier par rapport à un plan

' Symétrie d'une feature spécifique :
Dim oMirror As Mirror
Dim oMirrorPlane As Reference
Set oMirrorPlane = oPart.CreateReferenceFromName("yz plane")
Set oMirror = oSF.AddNewMirror(oMirrorPlane)
oMirror.Name = "Mirror_YZ"
' Note : AddNewMirror agit sur la dernière feature active dans PartBody

' Pour sélectionner explicitement la feature à mettre en miroir :
Dim oDoc2 As PartDocument
Dim oSel2 As Selection
Set oSel2 = CATIA.ActiveDocument.Selection
oSel2.Clear
oSel2.Add oPad1
Set oMirror = oSF.AddNewMirror(oMirrorPlane)

--- 1B.7 Thread et Tap (filetage et taraudage) ---

' Thread = filetage extérieur (sur un cylindre)
' Tap = taraudage intérieur (dans un trou)

' Accéder au ThreadFactory
Dim oTF As StrFeatFactory
Set oTF = oPart.StrFeatFactory

' Taraudage M8x1.25 sur un perçage existant :
Dim oTap As Thread
Dim oHoleFace As Reference
Dim oLimitFace As Reference
Set oHoleFace  = oPart.CreateReferenceFromName("PartBody\\Hole.1\\Face.1")
Set oLimitFace = oPart.CreateReferenceFromName("PartBody\\Hole.1\\Face.2")
Set oTap = oTF.AddNewThreadWithOutRef()
oTap.Side = catRightSide
oTap.ThreadDiameter.Value = 8.0
oTap.ThreadPitch.Value = 1.25
oTap.ThreadDepth.Value = 16.0
oTap.Name = "Tap_M8"
' Forcer Thread/Tap standard ISO :
oTap.StandardThreadElement = True

--- 1B.8 Chanfrein (Chamfer) ---

Dim oChamfer As Chamfer
Dim oChamfEdge As Reference
Set oChamfEdge = oPart.CreateReferenceFromName("PartBody\\Pad.1\\Edge.1")
Set oChamfer = oSF.AddNewChamfer( _
    oChamfEdge,                         _  ' arête
    catTangencyFilletEdgePropagation,   _  ' propagation
    1.0,                                _  ' distance D1
    45.0,                               _  ' angle (deg)
    catD1Angle1Chamfer                  _  ' mode
)
oChamfer.Name = "Chamfer_1x45"

--- 1B.9 Dépouille (Draft) ---

' Draft = inclinaison des faces pour démoulage
Dim oDraft As Draft
Dim oDraftFace As Reference
Dim oDraftDir As Reference
Set oDraftFace = oPart.CreateReferenceFromName("PartBody\\Pad.1\\Face.2")
Set oDraftDir  = oPart.CreateReferenceFromName("xy plane")
Set oDraft = oSF.AddNewDraft(oDraftFace, oDraftDir, 3.0, catDraftDraftAngle, False)
oDraft.Name = "Draft_3deg"

--- 1B.10 HybridShapeFactory — Géométrie 3D filaire et surfacique ---

' HybridShapeFactory crée de la géométrie NON-solide (filaire et surfacique)
' Elle est hébergée dans un Geometrical Set (Body Ouvert)
Dim oGeoSet As HybridBody
Set oGeoSet = oPart.HybridBodies.Add()
oGeoSet.Name = "Geometrie_Filaire"

Dim oHSF As HybridShapeFactory
Set oHSF = oPart.HybridShapeFactory

' === POINTS 3D ===
Dim oPt3D As HybridShapePointCoord
Set oPt3D = oHSF.AddNewPointCoord(50.0, 30.0, 20.0)
oPt3D.Name = "Pt_3D_A"

' Point sur courbe à abscisse curviligne :
Dim oPtOnCrv As HybridShapePointOnCurve
Set oPtOnCrv = oHSF.AddNewPointOnCurveWithReferenceFromPercent(oCurveRef, 0.5, False)

' === LIGNES 3D ===
Dim oLine3D As HybridShapeLinePtPt
Set oLine3D = oHSF.AddNewLinePtPt(oRef1, oRef2)
oLine3D.Name = "Line3D_AB"

' Ligne selon direction (vecteur) :
Dim oLinePtDir As HybridShapeLinePtDir
Set oLinePtDir = oHSF.AddNewLinePtDir(oRef1, oDirRef, 0.0, 100.0, False)

' === CERCLE 3D (par 3 points) ===
Dim oCirc3Pt As HybridShapeCircle3Points
Set oCirc3Pt = oHSF.AddNewCircle3Points(oRef1, oRef2, oRef3)

' Cercle sur plan (centre + rayon) :
Dim oCircCtrRad As HybridShapeCircleCtrRad
Set oCircCtrRad = oHSF.AddNewCircleCtrRad(oCenterRef, oPlaneRef, False, 15.0)
oCircCtrRad.BeginAngle.Value = 0.0
oCircCtrRad.EndAngle.Value   = 360.0

' === SPLINE 3D ===
Dim oSpline3D As HybridShapeSpline
Set oSpline3D = oHSF.AddNewSpline()
oSpline3D.AddPointWithConstraintExplicit(oRef1, Nothing, -1.0, 1, Nothing, 0.0)
oSpline3D.AddPointWithConstraintExplicit(oRef2, Nothing, -1.0, 1, Nothing, 0.0)
oSpline3D.AddPointWithConstraintExplicit(oRef3, Nothing, -1.0, 1, Nothing, 0.0)
oSpline3D.Name = "Spline_Routage"

' === PLANS 3D OFFSET ===
Dim oPlnOff As HybridShapePlaneOffset
Set oPlnOff = oHSF.AddNewPlaneOffset(oXYRef, 50.0, False)
oPlnOff.Name = "Plan_Z50"

' Plan à angle par rapport à un plan existant :
Dim oPlnAngle As HybridShapePlaneAngle
Set oPlnAngle = oHSF.AddNewPlaneAngle(oXYRef, oAxisRef, 45.0, False)

' === SURFACE EXTRUDÉE ===
Dim oExtrSurf As HybridShapeExtrude
Set oExtrSurf = oHSF.AddNewExtrude(oProfileRef, 0.0, 50.0, oDirectionRef)
oExtrSurf.Name = "Surf_Extrudee"

' === SURFACE DE RÉVOLUTION ===
Dim oRevSurf As HybridShapeRevol
Set oRevSurf = oHSF.AddNewRevol(oProfileRef, 0.0, 360.0, oAxisRef)
oRevSurf.Name = "Surf_Revolue"

' === JONCTION DE SURFACES (Join) ===
Dim oJoin As HybridShapeAssemble
Set oJoin = oHSF.AddNewJoin(oSurf1Ref, oSurf2Ref)
oJoin.Name = "Surf_Jointe"

' Après création de chaque shape hybride, l'ajouter au GeomSet :
oGeoSet.AppendHybridShape oSpline3D
oPart.Update

--- 1B.11 Opérations booléennes entre corps (Multi-Body) ---

' Créer un 2ème corps pour opération booléenne
Dim oBody2 As Body
Set oBody2 = oPart.Bodies.Add()
oBody2.Name = "Body_Outil"

' Créer une feature dans Body2 (ex: cylindre outil de coupe)
Dim oSkBool As Sketch
Set oSkBool = oBody2.Sketches.Add(oPart.CreateReferenceFromName("xy plane"))
Dim oFBool As Factory2D
Set oFBool = oSkBool.OpenEdition
oFBool.CreateCircle(0.0, 0.0, 15.0, 0.0, 6.2832)
oSkBool.CloseEdition
Dim oPadTool As Pad
Set oPadTool = oSF.AddNewPad(oSkBool, 100.0)

' === OPÉRATIONS BOOLÉENNES ===
' Remove (soustraction) : MainBody - Body_Outil
Dim oRemove As Remove
Set oRemove = oSF.AddNewRemove(oBody2)
oRemove.Name = "BoolRemove_Percage"

' Add (addition) : MainBody + Body_Outil
Dim oAdd As Add
Set oAdd = oSF.AddNewAdd(oBody2)
oAdd.Name = "BoolAdd_Fusion"

' Intersect (intersection) :
Dim oIntersect As Intersect
Set oIntersect = oSF.AddNewIntersect(oBody2)
oIntersect.Name = "BoolIntersect"

--- 1B.12 Exemples avancés CATScript ---

' Exemple : Corps de révolution complet (arbre à épaulement)
Sub CreerArbreEpaulement()
    Option Explicit
    Dim oPart As Part : Set oPart = CATIA.ActiveDocument.Part
    Dim oSF As ShapeFactory : Set oSF = oPart.ShapeFactory
    Dim oBody As Body : Set oBody = oPart.MainBody

    ' Sketch sur plan ZX — profil demi-section + axe
    Dim oSk As Sketch
    Set oSk = oBody.Sketches.Add(oPart.CreateReferenceFromName("zx plane"))
    Dim oF As Factory2D : Set oF = oSk.OpenEdition

    ' Axe de révolution (axe H = axe Z global)
    Dim oAx As Line2D : Set oAx = oF.CreateLine(0.0, 0.0, 150.0, 0.0)
    Dim oAxRef As Reference : Set oAxRef = oPart.CreateReferenceFromObject(oAx)
    oSk.Constraints.AddMonoEltCst(catCstTypeAxis, oAxRef)

    ' Profil : arbre D30 (L=80) + épaulement D20 (L=70)
    oF.CreateLine(  0.0,  0.0,   0.0, 15.0)  ' face gauche D30
    oF.CreateLine(  0.0, 15.0,  80.0, 15.0)  ' rayon 15 (D30)
    oF.CreateLine( 80.0, 15.0,  80.0, 10.0)  ' épaulement
    oF.CreateLine( 80.0, 10.0, 150.0, 10.0)  ' rayon 10 (D20)
    oF.CreateLine(150.0, 10.0, 150.0,  0.0)  ' face droite
    oF.CreateLine(150.0,  0.0,   0.0,  0.0)  ' axe bas (fermeture)
    oSk.CloseEdition

    Dim oShaft As Shaft : Set oShaft = oSF.AddNewShaft(oSk, 0.0, 360.0)
    oShaft.Name = "Shaft_Arbre"
    oPart.Update
End Sub

' Exemple : Boîtier creux avec Shell
Sub CreerBoitierShell()
    Option Explicit
    Dim oPart As Part : Set oPart = CATIA.ActiveDocument.Part
    Dim oSF As ShapeFactory : Set oSF = oPart.ShapeFactory
    Dim oBody As Body : Set oBody = oPart.MainBody
    Dim oSks As Sketches : Set oSks = oBody.Sketches

    ' 1. Pad de base : boîte 100x60x50mm
    Dim oXY As Reference
    Set oXY = oPart.CreateReferenceFromName("xy plane")
    Dim oSk1 As Sketch : Set oSk1 = oSks.Add(oXY)
    Dim oF1 As Factory2D : Set oF1 = oSk1.OpenEdition
    oF1.CreateLine(-50,-30,50,-30) : oF1.CreateLine(50,-30,50,30)
    oF1.CreateLine(50,30,-50,30)   : oF1.CreateLine(-50,30,-50,-30)
    oSk1.CloseEdition
    Dim oPad As Pad : Set oPad = oSF.AddNewPad(oSk1, 50.0)
    oPad.Name = "Pad_Boitier"

    ' 2. Shell 2.5mm (ouvrir la face du dessus)
    ' IMPORTANT: Update AVANT Shell pour que les faces soient disponibles
    oPart.Update
    Dim oFaceTop As Reference
    Set oFaceTop = oPart.CreateReferenceFromName("PartBody\\Pad_Boitier\\Face.1")
    Dim oShell As Shell : Set oShell = oSF.AddNewShell(oFaceTop, 2.5)
    oShell.Name = "Shell_Boitier"

    ' 3. Congés R3 sur les arêtes verticales du boîtier
    oPart.Update
    MsgBox "Boîtier Shell créé — ajoutez les congés manuellement sur les arêtes vives.", vbInformation
End Sub

=== PARTIE 2 : EKL — ENGINEERING KNOWLEDGE LANGUAGE ===

--- 2.1 Syntaxe de base EKL ---

/* Commentaire sur une ligne */
/* Déclaration de variables */
let myLength(Length)
let myAngle(Angle)
let myBool(Boolean)
let myInt(Integer)
let myStr(String)

/* Affectation */
myLength = 100mm
myAngle = 45deg
myBool = true
myInt = 3
myStr = "Aluminium"

/* Opérateurs */
myLength = myLength * 2
myAngle = myAngle + 10deg
myBool = (myLength > 50mm)

--- 2.2 Instructions de contrôle EKL ---

/* Condition */
if myLength > 100mm
{
    Thickness = 3mm
} else {
    Thickness = 2mm
}

/* Boucle */
let i(Integer)
for i while i < 10
{
    i = i + 1
}

--- 2.3 Accès aux paramètres CATIA en EKL ---

/* Accéder à un paramètre de la pièce */
let oPart = Part("PartBody")
let oParam = Parameter("Longueur")
oParam.Value = 150mm

/* Accéder à une feature */
let oPad = Feature("PartBody\\Pad.1")
oPad.FirstLimit\\Length = 20mm

--- 2.4 Règles EKL (Rules) ---

/* Règle déclenchée automatiquement lors d'une mise à jour */
Rule Regle_epaisseur
{
    /* Si la longueur dépasse 200mm, augmenter l'épaisseur */
    if `PartBody\\Pad.1\\FirstLimit\\Length` > 200mm
    {
        `PartBody\\Pocket.1\\FirstLimit\\Depth` = 5mm
    } else {
        `PartBody\\Pocket.1\\FirstLimit\\Depth` = 3mm
    }
}

--- 2.5 Checks EKL ---

/* Vérification avec message d'alerte */
Check Verif_rayon
{
    /* Commentaire : rayon min selon standard Airbus */
    `PartBody\EdgeFillet.1\Radius` >= 1mm
    Message("Le rayon de congé doit être >= 1mm. Valeur actuelle : #", `PartBody\EdgeFillet.1\Radius`)
}

--- 2.6 Reactions EKL ---

/* Réaction déclenchée par événement */
Reaction OnPadChange
{
    /* Déclenché quand Pad.1 est modifié */
    trigger : `PartBody\Pad.1`
    onEvent(update)
    {
        /* Synchroniser un paramètre dépendant */
        `Largeur` = `PartBody\Pad.1\FirstLimit\Length` / 2
    }
}

--- 2.7 Design Tables EKL ---

/* Associer une table de design à des paramètres */
/* La table Excel contient les colonnes : Config, Longueur, Largeur, Hauteur */
DesignTable("Config_table.xls")

--- 2.8 User Features (UDF) en EKL ---

/* Instanciation d'un User Feature */
let oUDF = Instantiate("MaUDF")
oUDF.SetParameterValue("Diametre", 10mm)
oUDF.SetParameterValue("Profondeur", 15mm)

--- 2.9 Design Tables en EKL ---

/* Une Design Table pilote des paramètres depuis un fichier Excel (.xls) */
/* Colonnes Excel : nom_config | Longueur | Largeur | Hauteur | Diam_Trou */
/* La règle EKL lit la ligne active et met à jour les paramètres */

Rule Appliquer_Design_Table
{
    /* Récupérer la configuration active */
    let oTable = DesignTable("Configs_Piece.xls")
    let nomConfig(String)
    nomConfig = oTable.CurrentRow  /* ex: "Config_A" */

    /* Lire les colonnes de la ligne active */
    let L(Length)   : L  = oTable.GetValue("Longueur")
    let W(Length)   : W  = oTable.GetValue("Largeur")
    let H(Length)   : H  = oTable.GetValue("Hauteur")
    let D(Length)   : D  = oTable.GetValue("Diam_Trou")

    /* Appliquer aux paramètres de la pièce */
    `PL_Longueur` = L
    `PL_Largeur`  = W
    `PL_Epaiss`   = H
    `TR_Diam`     = D

    Message("Config # appliquée : L=#mm W=#mm H=#mm D=#mm",
            nomConfig, L/1mm, W/1mm, H/1mm, D/1mm)
}

--- 2.10 Règles EKL avancées : Fonctions, Boucles et Optimisation ---

/* Fonction EKL (User Function) réutilisable */
Function CalcVolumeCylindre(d(Length), h(Length)) : Volume
{
    let r(Length) : r = d / 2
    CalcVolumeCylindre = 3.14159 * r * r * h
}

/* Utilisation de la fonction */
Rule Verif_Volume
{
    let vol(Volume)
    vol = CalcVolumeCylindre(`TR_Diam`, `PL_Epaiss`)
    if vol > 50000mm3
    {
        Message("WARN : Volume perçage > 50cm3 : #", vol)
    }
}

/* Règle avec boucle sur une collection de features */
Rule Verif_Tous_Pads
{
    let i(Integer) : i = 1
    let nbPads(Integer) : nbPads = PartBody.Features.Size()
    for i while i <= nbPads
    {
        let feat = PartBody.Features.Item(i)
        if feat.IsATypeOf("Pad")
        {
            let ep(Length) : ep = feat.FirstLimit.Length
            if ep < 3mm
            {
                Message("NON-CONFORME Pad# ep=#mm (min 3mm)", i, ep/1mm)
            }
        }
        i = i + 1
    }
}

/* Règle conditionnelle sur matière */
Rule Adaptation_Matiere
{
    let mat(String) : mat = `PartBody.Material`
    if mat == "Aluminium_2024"
    {
        `PL_Epaiss` = 2mm
        `Fillet_R`  = 1.5mm
    }
    if mat == "Inox_316L"
    {
        `PL_Epaiss` = 1.5mm
        `Fillet_R`  = 1mm
    }
    if mat == "Titane_6Al4V"
    {
        `PL_Epaiss` = 1mm
        `Fillet_R`  = 0.8mm
    }
}

--- 2.11 Checks EKL avancés (multi-critères aéronautique) ---

Check Conformite_Standard_Aero
{
    /* Épaisseur minimale selon matière et charge */
    `PartBody\\Pad_Platine\\FirstLimit\\Length` >= 3mm

    /* Rayon de congé minimum anti-fissuration */
    `PartBody\\EdgeFillet.1\\Radius` >= 1.5mm

    /* Ratio longueur/épaisseur max (flambement) */
    (`PL_Longueur` / `PL_Epaiss`) <= 50

    /* Espacement trous : centre-à-centre >= 3x diamètre */
    (`Espacement_Trous`) >= (3 * `TR_Diam`)

    Message("Vérification standard ASD EN9100 — cf. rapport.")
}

=== PARTIE 3 : EHI/EHA — ELECTRICAL HARNESS ===

--- 3.1 Concepts fondamentaux harnais ---

EHI = Electrical Harness Installation
     Définit le routage physique des faisceaux dans un produit.
     Travaille avec des Bundle Segments (tronçons de faisceau).

EHA = Electrical Harness Assembly
     Définit la nomenclature électrique : fils, connecteurs, protections.
     Contient les définitions de Part Numbers électriques.

Bundle Segment : tronçon de faisceau entre deux points de passage.
                 Propriétés : diamètre, longueur, rayon de courbure min.

Protective Covering : gaine protectrice appliquée sur un bundle segment.

Branch Point : point de branchement (fourche du faisceau).

Support : fixation du faisceau sur la structure (clip, collier, serre-câble).

Connector : connecteur électrique (mâle/femelle) en bout de faisceau.

--- 3.2 Accès au document EHI et initialisation ---

' IMPORTANT : EHI travaille dans un CATProduct (pas un CATPart)
' Le document actif doit être un ProductDocument

Dim oProduct As ProductDocument
Set oProduct = CATIA.ActiveDocument   ' doit être un ProductDocument

' Accéder au workbench EHI
Dim oHarnessWB As ElecHarnessInstallation
Set oHarnessWB = oProduct.GetItem("ElecHarnessInstallation")

' Accéder à la factory de bundle segments
Dim oElecFact As ElecBundleSegmentFactory
Set oElecFact = oHarnessWB.GetElecBundleSegmentFactory()

' Accéder au harness body (corps du harnais)
Dim oHarnessBody As ElecHarnessBody
Set oHarnessBody = oHarnessWB.GetElecHarnessBody(1)  ' index 1 = premier corps

--- 3.3 Création de géométrie 3D pour le routage ---

' Le chemin d'un Bundle Segment est défini par des points 3D dans l'espace.
' On crée ces points via HybridShapeFactory sur un Part du produit.

' Récupérer le Part portant la géométrie de routage
Dim oPartDoc As PartDocument
Set oPartDoc = oProduct.Products.Item(1).ReferenceProduct.Parent
Dim oWireFrame As Part
Set oWireFrame = oPartDoc.Part

Dim oHSF As HybridShapeFactory
Set oHSF = oWireFrame.HybridShapeFactory

' --- Créer des points 3D pour définir le chemin ---
' HybridShapePointCoord(X, Y, Z) = point à coordonnées absolues (mm)
Dim oPt1 As HybridShapePointCoord
Set oPt1 = oHSF.AddNewPointCoord(0.0, 0.0, 0.0)
oPt1.Name = "Pt_debut"

Dim oPt2 As HybridShapePointCoord
Set oPt2 = oHSF.AddNewPointCoord(100.0, 0.0, 0.0)
oPt2.Name = "Pt_milieu_bas"

Dim oPt3 As HybridShapePointCoord
Set oPt3 = oHSF.AddNewPointCoord(100.0, 0.0, 100.0)
oPt3.Name = "Pt_fin"

' --- Créer une polyligne 3D (chemin en U) ---
' Un chemin en U : descend puis avance puis remonte
Dim oPtU1 As HybridShapePointCoord
Dim oPtU2 As HybridShapePointCoord
Dim oPtU3 As HybridShapePointCoord
Dim oPtU4 As HybridShapePointCoord
Set oPtU1 = oHSF.AddNewPointCoord(0.0, 0.0, 0.0)     ' départ (haut gauche)
Set oPtU2 = oHSF.AddNewPointCoord(0.0, 0.0, -150.0)  ' descend (bas gauche)
Set oPtU3 = oHSF.AddNewPointCoord(200.0, 0.0, -150.0) ' fond du U (bas droite)
Set oPtU4 = oHSF.AddNewPointCoord(200.0, 0.0, 0.0)   ' remonte (haut droite)

' --- Créer des lignes 3D entre les points ---
Dim oRef_Pt1 As Reference
Set oRef_Pt1 = oWireFrame.CreateReferenceFromObject(oPtU1)
Dim oRef_Pt2 As Reference
Set oRef_Pt2 = oWireFrame.CreateReferenceFromObject(oPtU2)
Dim oRef_Pt3 As Reference
Set oRef_Pt3 = oWireFrame.CreateReferenceFromObject(oPtU3)
Dim oRef_Pt4 As Reference
Set oRef_Pt4 = oWireFrame.CreateReferenceFromObject(oPtU4)

Dim oLine1 As HybridShapeLinePtPt
Set oLine1 = oHSF.AddNewLinePtPt(oRef_Pt1, oRef_Pt2)
oLine1.Name = "Seg_descente"

Dim oLine2 As HybridShapeLinePtPt
Set oLine2 = oHSF.AddNewLinePtPt(oRef_Pt2, oRef_Pt3)
oLine2.Name = "Seg_fond"

Dim oLine3 As HybridShapeLinePtPt
Set oLine3 = oHSF.AddNewLinePtPt(oRef_Pt3, oRef_Pt4)
oLine3.Name = "Seg_montee"

oWireFrame.Update

--- 3.4 Création du Bundle Segment et association au chemin ---

' Créer le bundle segment
Dim oBSeg As ElecBundleSegment
Set oBSeg = oElecFact.CreateBundleSegment()
oBSeg.Name = "BS_U_Shape"

' Définir le diamètre du faisceau (en mm)
oBSeg.SetDiameter(12.0)

' Définir le rayon de courbure minimum (en mm)
oBSeg.SetMinBendRadius(60.0)   ' standard : BendRadius >= 5 * Diametre

' Définir la longueur (calculée automatiquement si chemin défini, sinon manuelle)
oBSeg.SetLength(500.0)   ' longueur en mm si chemin pas encore défini

' --- Associer le chemin géométrique au bundle segment ---
' Méthode 1 : via référence à une courbe/polyligne 3D
Dim oPathRef As Reference
Set oPathRef = oWireFrame.CreateReferenceFromObject(oLine1)
oBSeg.SetPath(oPathRef)

' Méthode 2 : via liste de points de passage
Dim oRefPt1 As Reference, oRefPt2 As Reference
Set oRefPt1 = oWireFrame.CreateReferenceFromObject(oPt1)
Set oRefPt2 = oWireFrame.CreateReferenceFromObject(oPt2)
oBSeg.AddRoutingPoint(oRefPt1)
oBSeg.AddRoutingPoint(oRefPt2)

--- 3.5 Exemple complet : Harnais en U (forme U-shape) ---

Sub CreerHarnaisEnU()
    Option Explicit
    ' Prérequis : document actif = CATProduct avec un ElecHarnessInstallation

    Dim oProduct As ProductDocument
    If Not TypeOf CATIA.ActiveDocument Is ProductDocument Then
        MsgBox "Ouvrir un CATProduct EHI.", vbCritical
        Exit Sub
    End If
    Set oProduct = CATIA.ActiveDocument

    ' Accès workbench EHI
    Dim oHWB As ElecHarnessInstallation
    Set oHWB = oProduct.GetItem("ElecHarnessInstallation")
    Dim oFact As ElecBundleSegmentFactory
    Set oFact = oHWB.GetElecBundleSegmentFactory()

    ' Récupérer la part de géométrie (premier produit)
    Dim oPartRef As Part
    Set oPartRef = oProduct.Products.Item(1).ReferenceProduct.Parent.Part
    Dim oHSF As HybridShapeFactory
    Set oHSF = oPartRef.HybridShapeFactory
    Dim oBody As Body
    Set oBody = oPartRef.MainBody

    ' Créer les 4 points du U (dimensions : largeur 200mm, profondeur 150mm)
    Dim pA As HybridShapePointCoord  ' départ haut-gauche
    Dim pB As HybridShapePointCoord  ' bas-gauche
    Dim pC As HybridShapePointCoord  ' bas-droite (fond du U)
    Dim pD As HybridShapePointCoord  ' haut-droite (arrivée)
    Set pA = oHSF.AddNewPointCoord(0.0, 0.0, 0.0)
    Set pB = oHSF.AddNewPointCoord(0.0, 0.0, -150.0)
    Set pC = oHSF.AddNewPointCoord(200.0, 0.0, -150.0)
    Set pD = oHSF.AddNewPointCoord(200.0, 0.0, 0.0)
    pA.Name = "U_Pt_A" : pB.Name = "U_Pt_B"
    pC.Name = "U_Pt_C" : pD.Name = "U_Pt_D"

    ' Créer les 3 segments du U
    Dim rA As Reference, rB As Reference, rC As Reference, rD As Reference
    Set rA = oPartRef.CreateReferenceFromObject(pA)
    Set rB = oPartRef.CreateReferenceFromObject(pB)
    Set rC = oPartRef.CreateReferenceFromObject(pC)
    Set rD = oPartRef.CreateReferenceFromObject(pD)

    Dim seg1 As HybridShapeLinePtPt  ' descente gauche
    Dim seg2 As HybridShapeLinePtPt  ' fond horizontal
    Dim seg3 As HybridShapeLinePtPt  ' montée droite
    Set seg1 = oHSF.AddNewLinePtPt(rA, rB)
    Set seg2 = oHSF.AddNewLinePtPt(rB, rC)
    Set seg3 = oHSF.AddNewLinePtPt(rC, rD)
    seg1.Name = "U_Seg_descente"
    seg2.Name = "U_Seg_fond"
    seg3.Name = "U_Seg_montee"
    oPartRef.Update

    ' Créer le Bundle Segment EHI
    Dim oBSU As ElecBundleSegment
    Set oBSU = oFact.CreateBundleSegment()
    oBSU.Name = "BS_U_Shape_D12"
    oBSU.SetDiameter(12.0)        ' diamètre 12mm
    oBSU.SetMinBendRadius(60.0)   ' rayon min = 5 x diamètre

    ' Associer les points de routage
    oBSU.AddRoutingPoint(rA)
    oBSU.AddRoutingPoint(rB)
    oBSU.AddRoutingPoint(rC)
    oBSU.AddRoutingPoint(rD)

    oProduct.Update
    MsgBox "Harnais U-shape BS_U_Shape_D12 créé.", vbInformation
End Sub

--- 3.6 Propriétés complètes d'un Bundle Segment ---

' Lire/écrire les propriétés principales :
oBSeg.SetDiameter(8.0)            ' diamètre du faisceau en mm
oBSeg.SetMinBendRadius(40.0)      ' rayon de courbure min en mm
oBSeg.SetLength(300.0)            ' longueur totale en mm
oBSeg.SetProtection("GS", 0.0, 1.0)  ' protection type GS sur 0% à 100% du segment
oBSeg.Name = "BS_Nom_du_segment"

' Lire les propriétés calculées :
Dim dLen As Double
dLen = oBSeg.GetLength()         ' longueur calculée après routing
Dim dDiam As Double
dDiam = oBSeg.GetDiameter()      ' diamètre actuel

' Ajouter un attribut utilisateur
oBSeg.SetAttributeValue("PartNumber", "CAB-001-A")
oBSeg.SetAttributeValue("Wire_Gauge", "AWG22")

--- 3.7 Supports (clips de fixation) ---

' Créer un support sur un bundle segment
Dim oClip As ElecSupport
Set oClip = oElecFact.CreateSupport()
oClip.Name = "SUP_Clip_01"
oClip.SetLinkedBundleSegment(oBSeg)
oClip.SetAbscissa(150.0)     ' position à 150mm depuis le début du segment
oClip.SetSupportType("CLIP_P10")  ' type de clip

--- 3.8 Branch Points — Nœuds de bifurcation EHI ---

' Un Branch Point est le nœud physique où plusieurs Bundle Segments se rejoignent
' C'est l'objet clé pour créer des topologies en Y, T ou en étoile

Dim oBP As ElecBranchPoint
Set oBP = oFact.CreateBranchPoint()
oBP.Name = "BP_Noeud_Y"

' Positionner le branch point sur le tronc à 250mm du début
oBP.SetLinkedBundleSegment(bsTronc, 250.0)

' Associer les branches au branch point
' Les branches commencent depuis ce nœud
bsBrA.SetStartBranchPoint(oBP)
bsBrB.SetStartBranchPoint(oBP)

' Branch Point pour topologie en T (3 segments qui se rejoignent) :
Dim oBP_T As ElecBranchPoint
Set oBP_T = oFact.CreateBranchPoint()
' 3 segments connectés à ce nœud :
bsGauche.SetEndBranchPoint(oBP_T)
bsDroite.SetEndBranchPoint(oBP_T)
bsBas.SetStartBranchPoint(oBP_T)

--- 3.9 Connecteurs électriques (ElecConnector) API complète ---

' Un connecteur est placé en bout d'un Bundle Segment
Dim oConnA As ElecConnector
Set oConnA = oFact.CreateConnector()
oConnA.Name = "CONN_J1_Alimentation"
oConnA.SetPartNumber("D38999/26WB35SN")         ' Part Number catalogue
oConnA.SetConnectorType("CIRCULAR_MULTI_PIN")   ' type
oConnA.SetNumberOfPins(37)                       ' nombre de broches
oConnA.SetGender("PLUG")                         ' PLUG = mâle, RECEPTACLE = femelle

' Associer le connecteur à l'extrémité du segment
oConnA.SetLinkedBundleSegment(bsBrA)
oConnA.SetEndAbscissa(bsBrA, 1.0)  ' 1.0 = bout du segment (100%)

' Positionner le connecteur dans l'espace 3D
Dim oConnPos As HybridShapePointCoord
Set oConnPos = oHSF.AddNewPointCoord(300.0, 0.0, 200.0)
Dim oConnPosRef As Reference
Set oConnPosRef = oWF.CreateReferenceFromObject(oConnPos)
oConnA.SetPosition(oConnPosRef)

' Connecteur mâle-femelle (accouplement)
Dim oConnB As ElecConnector
Set oConnB = oFact.CreateConnector()
oConnB.Name = "CONN_J2_Recepteur"
oConnB.SetPartNumber("D38999/20WB35PN")
oConnB.SetGender("RECEPTACLE")
oConnB.SetMatingConnector(oConnA)   ' connecteur complémentaire

--- 3.10 Protections et gaines (ElecProtectiveCovering) ---

' Types de protection disponibles :
' "BRAID"       = tresse métallique (blindage)
' "SLEEVE"      = gaine thermorétractable
' "TAPE"        = ruban d'enroulement
' "CONDUIT"     = conduit rigide
' "CORRUGATED"  = tuyau ondulé flexible
' "SPIRAL_WRAP" = gaine spiralée

' Appliquer une protection sur un bundle segment (de 0% à 100%) :
oBSeg.SetProtection("SLEEVE", 0.0, 1.0)      ' gaine sur 100% du segment
oBSeg.SetProtection("BRAID",  0.0, 0.8)      ' tresse sur 80% du tronc
oBSeg.SetProtection("TAPE",   0.1, 0.9)      ' ruban de 10% à 90%
oBSeg.SetProtection("CORRUGATED", 0.0, 1.0)  ' tuyau ondulé sur tout le segment

' Protection partielle (ex: passage en zone chaude)
oBSeg.SetProtection("THERMAL_SLEEVE", 0.3, 0.6)  ' zone 30% à 60%

--- 3.11 Fils électriques (ElecWire) dans EHA ---

' EHA (Harness Assembly) gère les fils individuels dans les bundle segments
' Chaque fil a : numéro, calibre (AWG/mm2), couleur, longueur

Dim oWire As ElecWire
Set oWire = oFact.CreateWire()
oWire.Name = "W_001_Alimentation_28VDC"
oWire.SetWireNumber("W001")
oWire.SetConductorGauge("AWG22")         ' calibre AWG 22 = 0.34mm2
oWire.SetInsulationColor("RED")          ' couleur isolant
oWire.SetLength(350.0)                   ' longueur en mm
oWire.SetSignalType("POWER_28VDC")       ' type de signal

' Ajouter le fil dans un bundle segment :
oBSeg.AddWire(oWire)

' Fil de signal (données) :
Dim oWireData As ElecWire
Set oWireData = oFact.CreateWire()
oWireData.SetWireNumber("W002")
oWireData.SetConductorGauge("AWG24")    ' 0.22mm2
oWireData.SetInsulationColor("BLUE")
oWireData.SetSignalType("DATA_ARINC429")
oBSeg.AddWire(oWireData)

--- 3.12 Règles standard harnais (conformité Airbus/aéro) ---

' Rayon de courbure minimum = 5 à 10x le diamètre du câble selon standard
' BendRadius >= 5 * BundleDiameter (standard civil)
' BendRadius >= 10 * BundleDiameter (standard militaire/critique)

' Espacement minimum entre supports = 200mm
' Espacement maximum entre supports = 400mm

' Protection obligatoire aux passages dans les structures (grommets)
' Identification des extrémités : A (origine) et B (destination)
' Normes : ASD-STAN EN 9100, MIL-DTL-17, SAE AS50881

' Diamètres standards de faisceaux (mm) : 4, 6, 8, 10, 12, 16, 20, 25, 30, 40
' Calibres AWG courants : AWG28 (0.08mm2), AWG24 (0.22mm2), AWG22 (0.34mm2),
'                         AWG20 (0.52mm2), AWG16 (1.31mm2), AWG12 (3.31mm2)

--- 3.13 Exemple complet : Harnais principal avec bifurcation et protection ---

Sub CreerHarnaisComplet()
    Option Explicit
    If Not TypeOf CATIA.ActiveDocument Is ProductDocument Then
        MsgBox "CATProduct EHI requis.", vbCritical : Exit Sub
    End If

    Dim oProd As ProductDocument : Set oProd = CATIA.ActiveDocument
    Dim oHWB As ElecHarnessInstallation
    Set oHWB = oProd.GetItem("ElecHarnessInstallation")
    Dim oFact As ElecBundleSegmentFactory
    Set oFact = oHWB.GetElecBundleSegmentFactory()
    Dim oWF As Part
    Set oWF = oProd.Products.Item(1).ReferenceProduct.Parent.Part
    Dim oHSF As HybridShapeFactory : Set oHSF = oWF.HybridShapeFactory

    ' Points 3D du harnais (forme Y)
    Dim p0 As HybridShapePointCoord : Set p0 = oHSF.AddNewPointCoord(0,0,0)
    Dim p1 As HybridShapePointCoord : Set p1 = oHSF.AddNewPointCoord(250,0,0)
    Dim p2 As HybridShapePointCoord : Set p2 = oHSF.AddNewPointCoord(250,0,150)
    Dim p3 As HybridShapePointCoord : Set p3 = oHSF.AddNewPointCoord(400,0,-100)
    p0.Name="H_P0":p1.Name="H_P1":p2.Name="H_P2":p3.Name="H_P3"
    Dim r0 As Reference:Set r0=oWF.CreateReferenceFromObject(p0)
    Dim r1 As Reference:Set r1=oWF.CreateReferenceFromObject(p1)
    Dim r2 As Reference:Set r2=oWF.CreateReferenceFromObject(p2)
    Dim r3 As Reference:Set r3=oWF.CreateReferenceFromObject(p3)
    oWF.Update

    ' Tronc P0->P1 (Ø20, blindé)
    Dim bsTronc As ElecBundleSegment:Set bsTronc=oFact.CreateBundleSegment()
    bsTronc.Name="BS_Tronc_D20"
    bsTronc.SetDiameter(20.0):bsTronc.SetMinBendRadius(100.0)
    bsTronc.AddRoutingPoint(r0):bsTronc.AddRoutingPoint(r1)
    bsTronc.SetProtection("BRAID",0.0,1.0)
    bsTronc.SetAttributeValue("PartNumber","CAB-TRONC-D20-BR")

    ' Branch point à P1
    Dim oBP As ElecBranchPoint:Set oBP=oFact.CreateBranchPoint()
    oBP.Name="BP_Y_Noeud"
    oBP.SetLinkedBundleSegment(bsTronc,250.0)

    ' Branche A : P1->P2 (Ø10, gaine thermique)
    Dim bsA As ElecBundleSegment:Set bsA=oFact.CreateBundleSegment()
    bsA.Name="BS_BrancheA_D10"
    bsA.SetDiameter(10.0):bsA.SetMinBendRadius(50.0)
    bsA.AddRoutingPoint(r1):bsA.AddRoutingPoint(r2)
    bsA.SetStartBranchPoint(oBP)
    bsA.SetProtection("SLEEVE",0.0,1.0)

    ' Branche B : P1->P3 (Ø8, conduit)
    Dim bsB As ElecBundleSegment:Set bsB=oFact.CreateBundleSegment()
    bsB.Name="BS_BrancheB_D8"
    bsB.SetDiameter(8.0):bsB.SetMinBendRadius(40.0)
    bsB.AddRoutingPoint(r1):bsB.AddRoutingPoint(r3)
    bsB.SetStartBranchPoint(oBP)
    bsB.SetProtection("CORRUGATED",0.0,1.0)

    ' Connecteur en bout de branche A
    Dim oCA As ElecConnector:Set oCA=oFact.CreateConnector()
    oCA.Name="CONN_J1":oCA.SetPartNumber("D38999/26WB35SN")
    oCA.SetLinkedBundleSegment(bsA):oCA.SetEndAbscissa(bsA,1.0)

    oProd.Update
    MsgBox "Harnais Y complet créé : Tronc D20 + BrancheA D10 + BrancheB D8", vbInformation
End Sub

=== PARTIE 3B : EXEMPLES MÉTIER — PIÈCES MÉCANIQUES TYPES ===

--- 3B.1 Support équerre / équerrage nervuré (L-bracket / gousset) ---

' Un support équerre (L-bracket) = platine horizontale + aile verticale (nervure)
' Synonymes CATIA : support, équerre, gousset, tôlerie, console, bracket
' Pattern : 2 Pad sur plans perpendiculaires + perçages + congés

Sub CreerSupport Equerre_Nervure()
    ' Ce type de pièce combine :
    ' - Pad_Platine   : extrusion rectangulaire sur plan XY (base horizontale)
    ' - Pad_Nervure   : extrusion trapézoïdale sur plan ZX (aile verticale, symétrique)
    ' - Pocket_Trous  : 4 cercles aux coins pour les fixations
    ' - Pocket_Allege : rainures ou découpes pour l'allégement

    ' Platine horizontale 160x90mm ép.6mm :
    Dim oXY As Reference : Set oXY = oPart.CreateReferenceFromName("xy plane")
    Dim oSk1 As Sketch : Set oSk1 = oBody.Sketches.Add(oXY)
    Dim oF1 As Factory2D : Set oF1 = oSk1.OpenEdition
    oF1.CreateLine(-80,-45,80,-45):oF1.CreateLine(80,-45,80,45)
    oF1.CreateLine(80,45,-80,45):oF1.CreateLine(-80,45,-80,-45)
    oSk1.CloseEdition
    Dim oPlatine As Pad : Set oPlatine = oSF.AddNewPad(oSk1, 6.0)
    oPlatine.Name = "Pad_Platine"

    ' Nervure / aile verticale (trapèze symétrique sur plan ZX) :
    Dim oZX As Reference : Set oZX = oPart.CreateReferenceFromName("zx plane")
    Dim oSk2 As Sketch : Set oSk2 = oBody.Sketches.Add(oZX)
    Dim oF2 As Factory2D : Set oF2 = oSk2.OpenEdition
    oF2.CreateLine(-80, 6, 80, 6)    ' base (au-dessus de la platine)
    oF2.CreateLine(80, 6, 44, 76)    ' côté droit incliné
    oF2.CreateLine(44, 76, -44, 76)  ' sommet de la nervure
    oF2.CreateLine(-44, 76, -80, 6)  ' côté gauche incliné
    oSk2.CloseEdition
    Dim oNervure As Pad : Set oNervure = oSF.AddNewPad(oSk2, 5.0)
    oNervure.IsSymmetric = True      ' extrusion symétrique de part et d'autre du plan ZX
    oNervure.Name = "Pad_Nervure_Trapeze"

    ' Perçages aux coins (fixation équerre sur structure) :
    Dim coins(3,1) As Double
    coins(0,0)=-66:coins(0,1)=-31:coins(1,0)=66:coins(1,1)=-31
    coins(2,0)=66:coins(2,1)=31:coins(3,0)=-66:coins(3,1)=31
    Dim i As Integer
    For i=0 To 3
        Dim oSkH As Sketch:Set oSkH=oBody.Sketches.Add(oXY)
        Dim oFH As Factory2D:Set oFH=oSkH.OpenEdition
        oFH.CreateCircle(coins(i,0),coins(i,1),4.5,0.0,6.2832)
        oSkH.CloseEdition
        Dim oPkH As Pocket:Set oPkH=oSF.AddNewPocket(oSkH,6.0)
        oPkH.Name="Pocket_Trou_"&CStr(i+1)
    Next i
    oPart.Update
End Sub

--- 3B.2 Bride de raccordement / Flasque (flanged coupling / flange) ---

' Une bride de raccordement (flange / flasque) = disque avec trous en cercle
' Synonymes : bride, flasque, bride tournante, bride fixe, flanged coupling
' Pattern : Shaft (profil en L tourné 360°) + CircPattern de perçages + alésage central

Sub CreerBrideFlanged()
    ' Structure d'une bride :
    ' - Corps principal : révolution d'un profil L ou T (Shaft 360°)
    ' - Alésage central : perçage ou pocket circulaire au centre
    ' - Trous de boulonnage : Pocket cercle + CircPattern (6 ou 8 trous sur cercle de boulonnage)
    ' - Congés : sur les arrêtes vives

    ' Profil de révolution (demi-section, plan ZX) :
    Dim oZX As Reference : Set oZX = oPart.CreateReferenceFromName("zx plane")
    Dim oSkShaft As Sketch : Set oSkShaft = oBody.Sketches.Add(oZX)
    Dim oFShaft As Factory2D : Set oFShaft = oSkShaft.OpenEdition
    ' Axe de révolution (axe H = Z CATIA) à H=0
    Dim oAx As Line2D : Set oAx = oFShaft.CreateLine(0,0,0,40)
    Dim oAxRef As Reference : Set oAxRef = oPart.CreateReferenceFromObject(oAx)
    oSkShaft.Constraints.AddMonoEltCst(catCstTypeAxis, oAxRef)
    ' Profil bride : collet D80 ép.15mm + corps D50 L=30mm + alésage D30
    oFShaft.CreateLine(15,0, 40,0)    ' face inférieure
    oFShaft.CreateLine(40,0, 40,15)   ' face ext. corps
    oFShaft.CreateLine(40,15, 25,15)  ' épaulement
    oFShaft.CreateLine(25,15, 25,45)  ' corps D50 (rayon 25)
    oFShaft.CreateLine(25,45, 15,45)  ' collet supérieur
    oFShaft.CreateLine(15,45, 15,0)   ' alésage int. D30 (rayon 15)
    oSkShaft.CloseEdition
    Dim oBride As Shaft : Set oBride = oSF.AddNewShaft(oSkShaft, 0.0, 360.0)
    oBride.Name = "Shaft_Bride"
    oPart.Update

    ' Trous de boulonnage Ø9 sur cercle de boulonnage D65 (rayon=32.5mm) :
    ' 1er trou à (32.5, 0) sur plan XY (face supérieure, Z=45mm)
    Dim oXY As Reference : Set oXY = oPart.CreateReferenceFromName("xy plane")
    ' Créer un plan offset Z=45mm pour la face de la bride
    Dim oHSF As HybridShapeFactory : Set oHSF = oPart.HybridShapeFactory
    Dim oPlanBride As HybridShapePlaneOffset
    Set oPlanBride = oHSF.AddNewPlaneOffset(oXY, 45.0, False)
    oPlanBride.Name = "Plan_Face_Bride"
    oPart.Update
    Dim oPlanRef As Reference : Set oPlanRef = oPart.CreateReferenceFromObject(oPlanBride)

    ' Sketch pour 1 trou sur le cercle de boulonnage :
    Dim oSkTrou As Sketch : Set oSkTrou = oBody.Sketches.Add(oPlanRef)
    Dim oFTrou As Factory2D : Set oFTrou = oSkTrou.OpenEdition
    oFTrou.CreateCircle(32.5, 0.0, 4.5, 0.0, 6.2832)  ' trou Ø9 à R=32.5
    oSkTrou.CloseEdition
    Dim oPkTrou As Pocket : Set oPkTrou = oSF.AddNewPocket(oSkTrou, 15.0)
    oPkTrou.Name = "Pocket_Trou_Brid_1"
    oPart.Update

    ' CircPattern : 6 trous tous les 60° autour de l'axe Z :
    Dim oAxisRef As Reference : Set oAxisRef = oPart.CreateReferenceFromName("zx plane")
    Dim oCircPat As CircPattern
    Set oCircPat = oSF.AddNewCircPattern(oPkTrou, 6, 60.0, 1, 1, oAxisRef, oAxisRef, True, True, 0.0)
    oCircPat.Name = "CircPat_6_Trous_Bride"
    oPart.Update
    MsgBox "Bride de raccordement créée. Ajoutez les congés manuellement.", vbInformation
End Sub

=== PARTIE 4 : BONNES PRATIQUES ET PATTERNS CATIA ===

--- 4.1 Nommage des features ---

' Convention de nommage recommandée :
' Pad_NomFonction        ex: Pad_Corps_principal
' Pocket_NomFonction     ex: Pocket_Alésage_central
' Fillet_Rayon           ex: Fillet_R2
' Hole_TypeDiam          ex: Hole_Percage_D5
' Plane_Description      ex: Plane_Milieu_corps

--- 4.2 Structure d'arbre recommandée ---

' PartBody
'   ├── Géométrie_principale
'   │     ├── Pad.1 (forme de base)
'   │     ├── Pocket.1 (évidement principal)
'   │     └── Fillet.1 (congés généraux)
'   ├── Détails_fonctionnels
'   │     ├── Hole.1 (perçages)
'   │     └── Chamfer.1 (chanfreins)
'   └── Finitions
'         └── Shell.1 (si applicable)

--- 4.3 Mise à jour du modèle ---

' Toujours appeler oPart.Update à la fin du macro
' Avant Update : les features sont créées mais pas calculées
' Après Update : la géométrie 3D est régénérée

oPart.Update

' Pour forcer la mise à jour d'un feature spécifique :
oFeature.Update

--- 4.4 Tolérances et unités ---

' CATIA V5 travaille en millimètres et degrés par défaut
' Les valeurs de cotes sont en mm : oPad.FirstLimit.Dimension.Value = 10.0  (= 10mm)
' Les angles sont en degrés : oAngularConstraint.Angle.Value = 90.0

' Pour les tolérances dimensionnelles :
' ISO 2768-m (tolérances générales pièces mécaniques)
' ASD-STAN EN 9100 pour aéronautique

--- 4.5 Macro de vérification de la géométrie ---

Sub VerifierGeometrie()
    Dim oPart As Part
    Set oPart = CATIA.ActiveDocument.Part

    ' Vérifier qu'il n'y a pas d'erreurs de mise à jour
    If oPart.Update() <> 0 Then
        MsgBox "Erreurs détectées dans le modèle. Vérifiez l'arbre.", vbCritical
        Exit Sub
    End If

    ' Vérifier le volume (doit être positif)
    Dim oMeasure As MeasurableShape
    Set oMeasure = CATIA.ActiveDocument.Part.MainBody
    If oMeasure.Volume <= 0 Then
        MsgBox "Volume nul ou négatif — vérifiez la géométrie.", vbCritical
    End If
End Sub

=== PARTIE 5 : EXEMPLES COMPLETS ===

--- 5.1 Exemple complet : Créer un bloc avec un perçage ---

Sub CreerBlocPerce()
    Option Explicit
    Dim oDoc As PartDocument
    Dim oPart As Part
    Dim oBody As Body
    Dim oSF As ShapeFactory
    Dim oSketches As Sketches
    Dim oSketch As Sketch
    Dim oFactory2D As Factory2D
    Dim oPad As Pad
    Dim oHole As Hole

    ' Vérification
    If Not TypeOf CATIA.ActiveDocument Is PartDocument Then
        MsgBox "Document Part requis.", vbCritical
        Exit Sub
    End If

    Set oDoc = CATIA.ActiveDocument
    Set oPart = oDoc.Part
    Set oBody = oPart.MainBody
    Set oSF = oPart.ShapeFactory

    ' Créer le sketch sur le plan XY
    Set oSketches = oBody.Sketches
    Dim oXY As Reference
    Set oXY = oPart.CreateReferenceFromName("xy plane")
    Set oSketch = oSketches.Add(oXY)

    ' Dessiner un rectangle 80x40mm centré à l'origine
    Set oFactory2D = oSketch.OpenEdition
    Dim oLines(3) As Line2D
    Set oLines(0) = oFactory2D.CreateLine(-40, -20, 40, -20)
    Set oLines(1) = oFactory2D.CreateLine(40, -20, 40, 20)
    Set oLines(2) = oFactory2D.CreateLine(40, 20, -40, 20)
    Set oLines(3) = oFactory2D.CreateLine(-40, 20, -40, -20)
    oSketch.CloseEdition

    ' Extruder de 25mm
    Set oPad = oSF.AddNewPad(oSketch, 25.0)
    oPad.Name = "Pad_Corps"

    ' Ajouter un perçage D8 traversant au centre
    Dim oTopFace As Reference
    Set oTopFace = oPart.CreateReferenceFromName("PartBody\\Pad_Corps\\Face.1")
    Set oHole = oSF.AddNewHole(oTopFace, 25.0)
    oHole.Diameter.Value = 8.0
    oHole.HoleType = catSimpleHole
    oHole.BottomType = catFlatHoleBottom
    oHole.Name = "Hole_D8_centre"

    ' Mise à jour
    oPart.Update
    MsgBox "Bloc percé créé avec succès.", vbInformation

End Sub

--- 5.2 Exemple EKL : Règle de vérification Airbus ---

/* Règle : vérifier que les congés respectent le minimum requis */
Rule Airbus_FilletCheck
{
    let minRadius(Length)
    minRadius = 1mm

    let oFillet = Feature("PartBody\EdgeFillet.1")

    if `PartBody\EdgeFillet.1\Radius` < minRadius
    {
        Message("NON-CONFORME : Congé trop petit. Min = #, Actuel = #",
                minRadius,
                `PartBody\EdgeFillet.1\Radius`)
    }
}

--- 5.3 Paramétrer une pièce via une macro CATScript ---

Sub ParametrerPiece()
    Dim oPart As Part
    Set oPart = CATIA.ActiveDocument.Part

    ' Modifier un paramètre existant nommé "Longueur"
    Dim oParam As Parameter
    Set oParam = oPart.Parameters.Item("Longueur")
    oParam.ValuateFromString("150mm")

    ' Modifier un paramètre de feature directement
    Dim oPad As Pad
    Set oPad = oPart.FindObjectByName("Pad_Corps")
    oPad.FirstLimit.Dimension.Value = 30.0

    oPart.Update
End Sub
"""


def create_reference_pdf() -> Path:
    pdf_path = DOCS_DIR / "catia_v5_scripting_reference.pdf"
    doc = fitz.open()

    lines = CATIA_REFERENCE.split("\n")
    page = None
    y = 60
    margin_left = 50
    margin_top = 60
    page_height = 842
    page_width = 595
    line_height = 12

    font_title = ("helv", 14)
    font_section = ("helv", 11)
    font_code = ("cour", 8)
    font_normal = ("helv", 9)

    def new_page():
        nonlocal page, y
        page = doc.new_page(width=page_width, height=page_height)
        y = margin_top

    def write_line(text, font_name, font_size, color=(0, 0, 0)):
        nonlocal y
        if y > page_height - 60:
            new_page()
        page.insert_text(
            (margin_left, y),
            text[:120],
            fontname=font_name,
            fontsize=font_size,
            color=color,
        )
        y += line_height

    new_page()

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("=== PARTIE"):
            y += 6
            write_line(stripped.replace("===", "").strip(), "helv", 13, (0.2, 0.2, 0.8))
            y += 4
        elif stripped.startswith("--- "):
            y += 4
            write_line(stripped.replace("---", "").strip(), "helv", 10, (0.1, 0.5, 0.1))
            y += 2
        elif stripped == "" :
            y += 3
        elif stripped.startswith("'") or any(
            kw in stripped for kw in [
                "Dim ", "Set ", "Sub ", "End Sub", "If ", "For ", "Next",
                "let ", "if ", "Rule ", "Check ", "Reaction ", "Option ",
                "oDoc", "oPart", "oBody", "oSF", "oSketch", "/*", "*/",
            ]
        ):
            write_line(line[:120], "cour", 8, (0.1, 0.1, 0.4))
        else:
            write_line(stripped[:120], "helv", 9)

    doc.save(str(pdf_path))
    doc.close()
    print(f"OK  PDF créé : {pdf_path}")
    return pdf_path


def purge_source(source_filename: str, chroma_path: Path) -> int:
    import chromadb
    client = chromadb.PersistentClient(path=str(chroma_path))
    try:
        col = client.get_collection("catscript_knowhow")
    except Exception:
        return 0
    results = col.get(where={"source_file": source_filename}, include=[])
    ids = results["ids"]
    if ids:
        col.delete(ids=ids)
    return len(ids)


def ingest_pdf(pdf_path: Path) -> None:
    sys.path.insert(0, str(ROOT))
    from backend.ingest import load_pdf, chunk_pages, embed_and_store

    chroma_path = ROOT / "data" / "chroma_db"
    purged = purge_source(pdf_path.name, chroma_path)
    if purged:
        print(f"INFO  {purged} anciens chunks '{pdf_path.name}' supprimés")
    print(f"INFO  Chargement de {pdf_path.name}...")
    pages = load_pdf(pdf_path)
    chunks = chunk_pages(pages)
    for chunk in chunks:
        chunk["source_file"] = pdf_path.name
    print(f"INFO  {len(chunks)} chunks générés")
    added = embed_and_store(chunks, chroma_path)
    print(f"OK    {added} chunks ajoutés à ChromaDB")
    print(f"DONE  Base de connaissances CATIA chargée.")


if __name__ == "__main__":
    pdf_path = create_reference_pdf()
    ingest_pdf(pdf_path)

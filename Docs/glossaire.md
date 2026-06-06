# Glossaire — Termes reconnus par FastCAD

Ce glossaire liste les termes qu'un ingénieur peut utiliser dans le champ
**O1 — Opération CATIA**. Pour chaque concept, les synonymes acceptés sont
indiqués ainsi que les paramètres que l'on peut préciser.

---

## CATSCRIPT — Opérations sur pièces solides

### Extrusion
**Termes reconnus :** extrusion, pad, bossage, élévation, relief, épaississement  
**Ce que ça fait :** crée un volume solide en poussant un profil 2D sur une hauteur donnée  
**Paramètres utiles :** hauteur (mm), plan de départ (XY / YZ / ZX ou plan personnalisé), symétrique ou non  
**Exemple :** *"une extrusion rectangulaire de 80 × 50 mm, hauteur 20 mm"*

---

### Enlèvement de matière / Poche
**Termes reconnus :** poche, pocket, découpe, perçage carré, évidement rectangulaire, rainure droite, creux, logement  
**Ce que ça fait :** soustrait un volume à la pièce en creusant selon un profil 2D  
**Paramètres utiles :** profondeur (mm), profil (rectangle, cercle, forme quelconque), traversant ou borgne  
**Exemple :** *"une poche rectangulaire de 40 × 20 mm, profondeur 10 mm, au centre de la face"*

---

### Révolution / Corps de révolution
**Termes reconnus :** révolution, corps de révolution, tournage, pièce tournée, axisymétrique, arbre, bague, moyeu, noix, bride (partie cylindrique)  
**Ce que ça fait :** fait tourner un profil 2D autour d'un axe pour créer un solide de révolution  
**Paramètres utiles :** angle (partiel ou 360°), profil demi-section, axe de révolution  
**Exemple :** *"un corps de révolution à 360° avec un diamètre extérieur de 60 mm et un alésage de 40 mm"*

---

### Gorge de révolution
**Termes reconnus :** gorge, rainure annulaire, saignée, lamage annulaire, enlèvement de révolution  
**Ce que ça fait :** enlève de la matière par révolution — crée des gorges circulaires (pour joints, circlips, etc.)  
**Paramètres utiles :** largeur (mm), profondeur (mm), position axiale, angle de révolution  
**Exemple :** *"une gorge annulaire de 3 mm de largeur et 2 mm de profondeur pour joint torique"*

---

### Coque / Évidement
**Termes reconnus :** coque, shell, évidement, paroi mince, boîtier creux, pièce creuse, cavité intérieure  
**Ce que ça fait :** vide l'intérieur d'un solide en conservant une épaisseur de paroi uniforme, avec une ou plusieurs faces ouvertes  
**Paramètres utiles :** épaisseur de paroi (mm), face(s) à supprimer (ouverture)  
**Exemple :** *"vider le boîtier avec des parois de 2 mm, ouverture par le dessus"*

---

### Balayage / Profilé extrudé
**Termes reconnus :** balayage, sweep, profilé, nervure sur courbe, extrusion le long d'un chemin, tuyau, joint d'étanchéité, cornière, profilé en U / L / T  
**Ce que ça fait :** déplace un profil 2D le long d'une courbe guide 3D pour créer un volume continu  
**Paramètres utiles :** profil de section (forme en U, L, T, cercle…), courbe guide (droite, courbe, polyligne)  
**Exemple :** *"un profilé en U de section 40 × 30 mm sur une longueur de 300 mm"*

---

### Perçage
**Termes reconnus :** perçage, trou, alésage, avant-trou, trou borgne, trou traversant, trou de passage, trou de fixation  
**Ce que ça fait :** crée un trou cylindrique (par extrusion d'un cercle en enlèvement)  
**Paramètres utiles :** diamètre (mm), profondeur (mm ou traversant), position (coordonnées X/Y sur la face)  
**Exemple :** *"un trou de passage Ø9 mm traversant à 15 mm des bords"*

---

### Répétition circulaire
**Termes reconnus :** répétition circulaire, couronne de trous, trous en cercle, motif circulaire, répartition angulaire, pas angulaire  
**Ce que ça fait :** répète une feature (trou, poche, etc.) autour d'un axe en la distribuant à intervalles angulaires réguliers  
**Paramètres utiles :** nombre d'occurrences, angle total ou pas angulaire (°), axe de répétition  
**Exemple :** *"8 trous répartis à 45° sur un cercle de boulonnage de Ø80 mm"*

---

### Répétition rectangulaire / En grille
**Termes reconnus :** répétition rectangulaire, grille, motif en grille, réseau de trous, rangées et colonnes  
**Ce que ça fait :** répète une feature en lignes et colonnes selon deux directions  
**Paramètres utiles :** nb de colonnes × nb de rangées, espacement en X (mm), espacement en Y (mm)  
**Exemple :** *"6 trous en grille 3 × 2, espacement 60 mm en longueur et 80 mm en largeur"*

---

### Symétrie / Miroir
**Termes reconnus :** symétrie, miroir, image miroir, duplication symétrique, pièce symétrique  
**Ce que ça fait :** crée une copie en miroir d'une feature ou d'un corps par rapport à un plan  
**Paramètres utiles :** plan de symétrie (XY, YZ, ZX ou plan personnalisé)  
**Exemple :** *"dupliquer la patte en miroir par rapport au plan milieu"*

---

### Congé
**Termes reconnus :** congé, arrondi d'arête, raccordement d'arête, rayon de congé, fillet  
**Ce que ça fait :** arrondit les arêtes vives avec un rayon constant  
**Paramètres utiles :** rayon (mm), arêtes concernées (toutes, sélectionnées, par propagation)  
**Exemple :** *"congés R3 sur toutes les arêtes verticales du boîtier"*

---

### Chanfrein
**Termes reconnus :** chanfrein, biseau, arête biseautée, 45 degrés, entrée de trou  
**Ce que ça fait :** coupe les arêtes vives selon un angle (généralement 45°)  
**Paramètres utiles :** distance (mm), angle (°), arêtes concernées  
**Exemple :** *"chanfreins 1 × 45° sur les arêtes d'entrée de l'alésage"*

---

### Filetage / Taraudage
**Termes reconnus :** taraudage, filetage, filet, visserie, M6 M8 M10 M12, pas de vis, filetage intérieur, filetage extérieur  
**Ce que ça fait :** ajoute un filetage ou taraudage sur une surface cylindrique  
**Paramètres utiles :** norme (M6, M8, M10…), pas (mm), profondeur (mm), intérieur (taraudage) ou extérieur (filetage)  
**Exemple :** *"un taraudage M8 pas 1,25 mm sur 16 mm de profondeur"*

---

### Dépouille
**Termes reconnus :** dépouille, angle de démoulage, inclinaison de face, draft  
**Ce que ça fait :** incline une face pour faciliter le démoulage ou l'extraction  
**Paramètres utiles :** angle de dépouille (°), direction de tirage, faces concernées  
**Exemple :** *"dépouille de 3° sur les faces latérales pour le démoulage"*

---

### Plan de référence
**Termes reconnus :** plan décalé, plan à distance, plan parallèle, plan incliné, plan intermédiaire  
**Ce que ça fait :** crée un plan de travail personnalisé pour localiser des sketches ou features  
**Paramètres utiles :** plan de référence (XY / YZ / ZX), offset (mm) ou angle (°)  
**Exemple :** *"un plan parallèle au plan XY, décalé de 45 mm vers le haut"*

---

### Paramètre piloté
**Termes reconnus :** paramètre, cote pilotée, dimension variable, formule, longueur pilotée par paramètre  
**Ce que ça fait :** crée des paramètres nommés qui pilotent les cotes du modèle (modification globale en changeant une valeur)  
**Paramètres utiles :** nom du paramètre, valeur initiale, unité (longueur, angle, etc.)  
**Exemple :** *"piloter toutes les cotes par des paramètres nommés Longueur, Largeur, Hauteur"*

---

## EKL — Règles et vérifications

### Règle de conception
**Termes reconnus :** règle, règle automatique, contrainte de conception, règle paramétrique, logique conditionnelle  
**Ce que ça fait :** déclenche automatiquement des actions sur les paramètres lors d'une mise à jour du modèle  
**Paramètres utiles :** conditions (si… alors…), paramètres à modifier, message de sortie  
**Exemple :** *"une règle qui ajuste l'épaisseur automatiquement si la longueur dépasse 200 mm"*

---

### Vérification / Contrôle qualité
**Termes reconnus :** vérification, contrôle, check, audit, conformité, validation, non-conformité  
**Ce que ça fait :** vérifie que des critères géométriques ou dimensionnels sont respectés et signale les écarts  
**Paramètres utiles :** critères à vérifier (min/max de cotes), message d'alerte, seuils  
**Exemple :** *"vérifier que tous les rayons de congé sont supérieurs à 1,5 mm"*

---

### Table de configuration / Variantes
**Termes reconnus :** table de configuration, variantes, familles de pièces, Design Table, configurations multiples, taille S/M/L  
**Ce que ça fait :** pilote les dimensions de la pièce depuis un tableau Excel, permettant de switcher entre configurations prédéfinies  
**Paramètres utiles :** nom du fichier Excel, colonnes = noms des paramètres, lignes = configurations  
**Exemple :** *"une règle qui applique la taille de la pièce depuis un fichier de configurations Excel"*

---

### Réaction sur événement
**Termes reconnus :** réaction, déclenchement sur modification, synchronisation automatique  
**Ce que ça fait :** exécute une action EKL en réponse à la modification d'une feature ou d'un paramètre spécifique  
**Paramètres utiles :** feature déclencheuse, action à exécuter  
**Exemple :** *"quand le Pad principal est modifié, recalculer automatiquement la profondeur de la poche"*

---

## EHI — Harnais et câblage

### DMU (Digital Mock-Up)
**Définition :** maquette numérique 3D d'un environnement d'intégration — assemblage de composants (structure avion, boîtiers équipements, supports) utilisé comme contexte spatial pour le routage de harnais.  
**Usage dans FastCAD :** un fichier DMU (STEP, STP ou CATProduct) peut être déposé dans la section `04 _ Environnement DMU` lorsque le type de script est `EHI/EHA`. FastCAD extrait la boîte englobante et les composants, puis génère un script de routage qui évite les volumes d'encombrement.  
**Formats acceptés :** `.step`, `.stp`, `.catproduct`

---

### CATProduct d'environnement
**Définition :** fichier `.catproduct` CATIA V5 décrivant un assemblage multi-pièces utilisé comme référence spatiale pour le routage de harnais. Contrairement à un CATProduct de conception, il est utilisé ici en lecture seule pour en extraire les composants (`Component`, `Instance`) et les contraintes de positionnement.  
**Données extraites :** liste des composants nommés, contraintes d'assemblage (Contact, Coincidence, Offset, Angle)  
**Rôle :** fournit au LLM la topologie de l'environnement pour calculer des points de passage réalistes.

---

### Point de passage 3D
**Termes reconnus :** point de routage, waypoint, routing point, point 3D, point de guidage  
**Ce que ça fait :** point géométrique dans l'espace 3D utilisé comme nœud de passage obligatoire pour le tracé d'un segment de harnais. Défini via `HybridShapeFactory` dans les scripts EHI/EHA.  
**Paramètres utiles :** coordonnées X, Y, Z (mm) — typiquement dérivées des dimensions de la boîte englobante du DMU avec un offset de sécurité minimum de 20 mm par rapport aux volumes d'encombrement.  
**Exemple :** *"un point de passage à X=150, Y=50, Z=80 au-dessus du boîtier équipement"*

---

### Faisceau / Tronçon de câblage
**Termes reconnus :** faisceau, tronçon, faisceau électrique, câble, loom, bundle, harnais principal, segment de harnais  
**Ce que ça fait :** crée un tronçon de câblage entre deux points, avec ses propriétés (diamètre, longueur, courbure)  
**Paramètres utiles :** diamètre (mm), longueur (mm), rayon de courbure minimum (mm), protection, numéro de référence  
**Exemple :** *"un faisceau de 12 mm de diamètre sur 500 mm de longueur"*

---

### Bifurcation / Nœud en Y ou T
**Termes reconnus :** bifurcation, nœud, fourche, dérivation, point de ramification, Y, T, étoile  
**Ce que ça fait :** crée le point physique où plusieurs tronçons de harnais se rejoignent  
**Paramètres utiles :** position sur le tronc principal (mm depuis le départ), branches issues de ce nœud  
**Exemple :** *"une bifurcation en Y à 250 mm du départ du tronc principal"*

---

### Connecteur
**Termes reconnus :** connecteur, prise, fiche, embase, connecteur circulaire, connecteur rectangulaire, D38999, Deutsch, Amphenol, broches  
**Ce que ça fait :** place un connecteur électrique en bout de faisceau avec ses caractéristiques (type, genre, nombre de broches, référence)  
**Paramètres utiles :** référence catalogue (ex : D38999/26WB35SN), type (circulaire, rectangulaire), genre (mâle/femelle), nombre de broches  
**Exemple :** *"un connecteur circulaire 37 broches mâle en bout de branche"*

---

### Support de fixation
**Termes reconnus :** support, clip, collier, serre-câble, attache, fixation de harnais, bride de maintien  
**Ce que ça fait :** positionne un élément de fixation sur un tronçon à une distance donnée depuis le départ  
**Paramètres utiles :** position (mm depuis le début du segment), type de clip (référence), espacement entre supports  
**Exemple :** *"deux clips de fixation à 100 mm et 400 mm depuis le départ"*

---

### Protection / Gaine
**Termes reconnus :** protection, gaine, blindage, tresse, conduit, tuyau ondulé, ruban, gaine thermorétractable, gaine spiralée  
**Ce que ça fait :** applique une protection physique sur tout ou partie d'un tronçon de harnais  
**Types disponibles :**  
- **Blindage / tresse** : protection électromagnétique (CEM)  
- **Gaine thermorétractable** : protection mécanique et étanchéité  
- **Conduit ondulé** : protection en zone de flexion ou vibration  
- **Ruban d'enroulement** : protection légère et flexible  
- **Conduit rigide** : protection maximale en zone de risque  
**Paramètres utiles :** type, étendue (de X% à Y% du segment)  
**Exemple :** *"blindage sur le tronc principal, gaine thermorétractable sur les branches"*

---

### Fil électrique
**Termes reconnus :** fil, conducteur, câble individuel, âme, fil de signal, fil de puissance, AWG, mm²  
**Ce que ça fait :** définit un conducteur individuel à l'intérieur d'un faisceau avec ses caractéristiques électriques  
**Paramètres utiles :** numéro de fil, calibre (AWG22, AWG24… ou mm²), couleur d'isolant, type de signal (28VDC, GND, ARINC429, RS422…), longueur  
**Exemple :** *"un fil d'alimentation 28 VDC en rouge, calibre AWG22"*

---

## Notes générales

**Unités acceptées**  
Toutes les dimensions doivent être précisées en **millimètres (mm)** et les angles en **degrés (°)**.

**Plans de référence standards**  
- **Plan XY** = plan horizontal (vue de dessus)  
- **Plan YZ** = plan frontal (vue de face)  
- **Plan ZX** = plan de profil (vue de côté)

**Niveau de détail conseillé**  
Plus la description mentionne de dimensions précises (Ø, longueur, épaisseur, nombre d'occurrences), plus le script généré sera fidèle. Une description vague produira un script avec des valeurs par défaut à ajuster.

---

## Formats d'entrée — rétro-ingénierie

La fonctionnalité de rétro-ingénierie accepte les formats CAD suivants en entrée pour générer automatiquement un script CATScript reproductible.

### STEP / STP

**Extension :** `.step`, `.stp`  
**Standard :** ISO 10303 (STEP — Standard for the Exchange of Product model data)  
**Structure :** fichier texte ASCII structuré en entités numérotées (`#ID = ENTITE(...)`)  
**Données extraites :** produits (`PRODUCT`), points cartésiens (`CARTESIAN_POINT`), cotes (`LENGTH_MEASURE`), coques fermées (`CLOSED_SHELL`), faces avancées (`ADVANCED_FACE`)  
**Usage :** format d'échange universel — exportable depuis CATIA, SolidWorks, STEP AP214/242

---

### CATPart

**Extension :** `.catpart`  
**Origine :** CATIA V5 / V6 — pièce mécanique individuelle  
**Structure interne :** archive ZIP contenant des fichiers XML décrivant l'arbre de construction  
**Données extraites :** features de conception (Pad, Pocket, Shaft, Groove, Hole, Fillet, Chamfer, CircPattern, RectPattern, Mirror, Shell, Sweep, Loft), paramètres nommés avec leurs valeurs  
**Usage :** pièces solides CATIA V5 — constituant de base des assemblages CATProduct

---

### CATProduct

**Extension :** `.catproduct`  
**Origine :** CATIA V5 / V6 — assemblage de pièces  
**Structure interne :** archive ZIP contenant des fichiers XML décrivant l'arbre d'assemblage  
**Données extraites :** composants (`Component`, `Instance`, `Reference`), contraintes d'assemblage (Contact, Coincidence, Offset, Angle)  
**Usage :** assemblages multi-pièces CATIA V5 — référence des CATPart qui le composent

---

### IGES

**Extension :** `.igs`, `.iges`  
**Standard :** IGES — Initial Graphics Exchange Specification  
**Note :** format non supporté en rétro-ingénierie directe dans FastCAD (pas d'extraction structurée disponible sans dépendance lourde). Convertir en STEP avant import.

---

## Mise en plan — CATDrawing

### CATDrawing

**Définition :** document CATIA V5 de type dessin technique (`.CATDrawing`) contenant une ou plusieurs feuilles de mise en plan. Créé en CATScript via `CATIA.Documents.Add("Drawing")` et représenté par l'objet `DrawingDocument`.  
**Usage dans FastCAD :** la section `05 _ Mise en plan` génère automatiquement un script CATScript qui crée un `CATDrawing` à partir d'un modèle existant (CATPart, CATProduct ou STEP).  
**Norme appliquée :** ISO (`catISO`) par défaut — peut être ajustée dans le script généré.

---

### DrawingSheet

**Définition :** feuille de dessin au sein d'un `CATDrawing`. Accessible via `oDrawing.Sheets.Item(1)`. Contient les vues projetées, le cartouche et les annotations.  
**Paramètres utiles :** format (A0 à A4), orientation (paysage/portrait), échelle générale.  
**Exemple CATScript :** `Dim oSheet As DrawingSheet / Set oSheet = oDrawing.Sheets.Item(1)`

---

### Vues projetées (face / dessus / profil)

**Termes reconnus :** vue de face, vue de dessus, vue de profil, vue de droite, vue isométrique, projection orthogonale, vue principale  
**Ce que ça fait :** projections 2D orthogonales du modèle 3D selon les directions standard (ISO E ou ISO A) placées sur la feuille de dessin.  
**Vues générées automatiquement :**  
- **Vue de face** — projection sur le plan frontal (YZ)  
- **Vue de dessus** — projection sur le plan horizontal (XY)  
- **Vue de profil** — projection sur le plan de profil (ZX)  
**API CATIA V5 :** `oSheet.Views.AddDetail` ou vues génératives depuis le document 3D actif.

---

### Cartouche

**Termes reconnus :** cartouche, titre, bloc de titre, title block, nomenclature, cadre de dessin  
**Ce que ça fait :** zone normalisée en bas à droite de la feuille contenant les informations administratives du dessin : nom de la pièce, date, indice de révision, auteur, société.  
**Accès CATScript :** `oSheet.DrawingComponents` — permet de renseigner le nom de la pièce et la date si accessible depuis le modèle source.

---

### Norme ISO

**Contexte :** norme de dessin technique internationale appliquée aux CATDrawing générés par FastCAD.  
**Constante CATScript :** `catISO` — appliquée via `oDrawing.Standard = catISO`.  
**Effets :** projections en convention européenne (premier dièdre), symbolisation des tolérances géométriques, format des flèches de cotation et des lignes de rappel conformes à ISO 128 et ISO 129.

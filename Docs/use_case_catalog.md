# Use Case Catalog — FastCAD / CATScript-AI

Base de connaissances : 182 chunks validés  
Validation RAG : 20/20 — score cosine moyen 0.558  
Date : 2026-06-05

---

## Comment utiliser ce catalogue

1. Ouvrir l'outil à `http://localhost:8000`
2. Copier le texte **"Opération CATIA"** dans le champ `O1 — Opération CATIA`
3. Le type de script est détecté automatiquement — vérifier avant de générer
4. Choisir le provider / modèle et cliquer sur Générer

---

## CATSCRIPT — Pièces mécaniques

### UC-01 — Platine de fixation

**Type :** CATScript  
**Opération CATIA :**
Je veux créer une platine de fixation rectangulaire de 200 × 120 mm,
épaisseur 8 mm, avec 6 trous de passage de Ø10 mm disposés en grille 3 colonnes
× 2 rangées, espacés de 60 mm en longueur et 80 mm en largeur.

---

### UC-02 — Support équerre nervuré

**Type :** CATScript  
**Opération CATIA :**
Je veux créer un support équerre avec une semelle horizontale de 160 × 90 mm,
épaisseur 6 mm, et une nervure verticale trapézoïdale de 70 mm de hauteur centrée
sur la semelle. La nervure doit être symétrique par rapport au milieu de la pièce.
Ajouter 4 trous de fixation Ø9 mm aux quatre coins de la semelle.

---

### UC-03 — Arbre de transmission à épaulements

**Type :** CATScript  
**Opération CATIA :**
Je veux créer un arbre de transmission avec deux diamètres : un premier tronçon
de Ø30 mm sur 80 mm de longueur, puis un épaulement vers un second tronçon de
Ø20 mm sur 70 mm. Prévoir une gorge d'arrêt de Ø15 mm profondeur 3 mm à la
jonction des deux diamètres pour le montage d'un circlip.

---

### UC-04 — Boîtier électronique évidé

**Type :** CATScript  
**Opération CATIA :**
Je veux créer un boîtier électronique rectangulaire de 120 × 80 × 60 mm
avec des parois de 2,5 mm d'épaisseur, ouvert sur le dessus. Prévoir une
découpe rectangulaire de 80 × 40 mm sur la face avant pour le passage des
connecteurs.

---

### UC-05 — Bague de centrage avec joint torique

**Type :** CATScript  
**Opération CATIA :**
Je veux créer une bague de centrage avec un diamètre extérieur de 60 mm,
un alésage intérieur de 40 mm, et une hauteur de 25 mm. Prévoir une gorge
annulaire de 2 mm de profondeur et 3 mm de largeur à mi-hauteur pour le
logement d'un joint torique. Chanfreins d'entrée 1 × 45° sur les deux
faces de l'alésage.

---

### UC-06 — Profilé structurel en U par balayage

**Type :** CATScript  
**Opération CATIA :**
Je veux créer un profilé en U de section 40 × 30 mm avec des ailes de 3 mm
d'épaisseur, balayé sur une longueur droite de 300 mm. Le profilé doit
suivre un chemin rectiligne.

---

### UC-07 — Disque avec perçages en couronne

**Type :** CATScript  
**Opération CATIA :**
Je veux créer un disque plein de Ø100 mm et 10 mm d'épaisseur, avec 8 trous
de Ø8 mm régulièrement répartis sur un cercle de perçage de Ø80 mm
(cercle de boulonnage). Les trous doivent être à 45° l'un de l'autre.

---

### UC-08 — Pièce symétrique : patte de pompe

**Type :** CATScript  
**Opération CATIA :**
Je veux créer une patte de fixation de pompe symétrique. Partir d'un bloc
de 80 × 50 × 12 mm avec une poche centrale de 40 × 30 mm et 2 trous de
fixation Ø7 mm, puis dupliquer l'ensemble en miroir pour obtenir la pièce
complète symétrique.

---

### UC-09 — Bloc fileté avec chanfreins

**Type :** CATScript  
**Opération CATIA :**
Je veux créer un bloc de fixation de 60 × 40 × 30 mm avec un taraudage M8
profondeur 16 mm au centre, un avant-trou Ø6,8 mm borgne de 20 mm.
Ajouter des chanfreins 1 × 45° sur les arêtes supérieures du bloc.

---

### UC-10 — Bride de raccordement DN50

**Type :** CATScript  
**Opération CATIA :**
Je veux créer une bride de raccordement DN50 : collet extérieur Ø90 mm
épaisseur 15 mm, corps Ø60 mm longueur 30 mm, alésage intérieur Ø52 mm.
Ajouter 4 trous de boulonnage Ø14 mm régulièrement répartis sur un cercle
de boulonnage de Ø75 mm.

---

## EKL — Règles de conception

### UC-11 — Auditeur de conformité aéronautique

**Type :** EKL  
**Opération CATIA :**
Je veux une règle qui vérifie automatiquement la conformité de ma pièce
selon nos standards aéronautiques : épaisseur minimale de 3 mm, rayon de
congé minimum de 1,5 mm, et diamètre de perçage entre 4 et 20 mm.
La règle doit produire un rapport listant chaque critère avec son statut
conforme ou non-conforme, et indiquer le bilan global.

---

### UC-12 — Paramétrage par configuration (Design Table)

**Type :** EKL  
**Opération CATIA :**
Je veux une règle qui lit un fichier Excel de configurations et applique
automatiquement les dimensions de la ligne active (longueur, largeur, hauteur,
diamètre de trou) aux paramètres de ma pièce. La règle doit afficher un
message de confirmation avec les valeurs appliquées.

---

### UC-13 — Vérificateur de géométrie multi-critères

**Type :** EKL  
**Opération CATIA :**
Je veux un check qui valide simultanément l'épaisseur des parois, le rayon
des congés, le ratio longueur sur épaisseur (pour éviter le flambement), et
l'espacement minimum entre trous (au moins 3 fois le diamètre). Afficher un
message d'alerte détaillé pour chaque critère en dehors des tolérances.

---

### UC-14 — Adaptation automatique par matière

**Type :** EKL  
**Opération CATIA :**
Je veux une règle qui détecte la matière assignée à la pièce et ajuste
automatiquement les épaisseurs et rayons de congé selon les préconisations
du bureau d'études : valeurs différentes pour l'aluminium 2024, l'inox 316L
et le titane 6Al-4V.

---

### UC-15 — Contrôle de tous les pads de la pièce

**Type :** EKL  
**Opération CATIA :**
Je veux une règle qui parcourt automatiquement toutes les extrusions de la
pièce et signale celles dont l'épaisseur est inférieure à 3 mm, en précisant
le nom de la feature concernée et sa valeur actuelle.

---

## EHI — Harnais électriques

### UC-16 — Harnais linéaire avec supports de fixation

**Type :** EHI/EHA  
**Opération CATIA :**
Je veux créer un faisceau électrique rectiligne de 500 mm de longueur,
diamètre 12 mm, avec une gaine thermorétractable sur toute sa longueur.
Placer deux supports de fixation (clips) à 100 mm et 400 mm depuis
le départ du faisceau.

---

### UC-17 — Harnais en Y avec point de bifurcation

**Type :** EHI/EHA  
**Opération CATIA :**
Je veux créer un harnais en forme de Y : un tronc principal de 300 mm de
longueur et 16 mm de diamètre, blindé, qui se divise en deux branches de
200 mm chacune et 10 mm de diamètre, avec une gaine de protection sur
chaque branche. Définir le point de bifurcation à l'extrémité du tronc.

---

### UC-18 — Harnais multi-branches avec connecteurs

**Type :** EHI/EHA  
**Opération CATIA :**
Je veux créer un harnais principal avec un tronc blindé de 20 mm de diamètre,
une branche montante de 10 mm avec gaine thermorétractable terminée par un
connecteur circulaire 37 broches mâle (D38999), et une branche descendante
de 8 mm en conduit ondulé terminée par le connecteur femelle correspondant.

---

### UC-19 — Câblage de tableau de bord en étoile

**Type :** EHI/EHA  
**Opération CATIA :**
Je veux créer un faisceau de distribution pour tableau de bord : un nœud
central depuis lequel partent 4 branches de 200 mm chacune, orientées à 90°
les unes des autres, diamètre 12 mm, avec conduit ondulé de protection.
Chaque branche doit avoir un numéro de référence de câble.

---

### UC-20 — Faisceau avec fils référencés et signaux électriques

**Type :** EHI/EHA  
**Opération CATIA :**
Je veux créer un faisceau de 16 mm de diamètre contenant 4 fils individuels :
un fil d'alimentation 28 VDC en rouge (AWG22), un fil de données ARINC 429
en bleu (AWG24), un fil de masse en jaune (AWG22) et un fil RS-422 en vert
(AWG24). Chaque fil doit avoir son numéro de câble, son calibre et son type
de signal documentés.

---

## Synthèse

| UC | Type | Domaine |
|----|------|---------|
| 01 | CATScript | Platine de fixation |
| 02 | CATScript | Support équerre nervuré |
| 03 | CATScript | Arbre de transmission |
| 04 | CATScript | Boîtier évidé |
| 05 | CATScript | Bague avec joint torique |
| 06 | CATScript | Profilé en U par balayage |
| 07 | CATScript | Disque avec couronne de perçages |
| 08 | CATScript | Pièce symétrique |
| 09 | CATScript | Bloc fileté et chanfreiné |
| 10 | CATScript | Bride de raccordement |
| 11 | EKL | Auditeur de conformité |
| 12 | EKL | Paramétrage Design Table |
| 13 | EKL | Vérificateur multi-critères |
| 14 | EKL | Adaptation par matière |
| 15 | EKL | Contrôle de tous les pads |
| 16 | EHI | Harnais linéaire |
| 17 | EHI | Harnais en Y |
| 18 | EHI | Harnais avec connecteurs |
| 19 | EHI | Câblage en étoile |
| 20 | EHI | Fils référencés et signaux |

---

## Exemples d'intégration — Validation complète

Ces deux exemples couvrent l'ensemble des 20 use cases en une seule pièce.
Ils servent à tester que CATIA peut enchaîner toutes les opérations sans conflit.

---

### INTEG-01 — Corps de pompe centrifuge (mécanique)

**Type :** CATScript  
**Use cases couverts :** UC-01 · UC-02 · UC-03 · UC-04 · UC-05 · UC-07 · UC-08 · UC-09 · UC-10  
**Opération CATIA :**

Je veux créer le corps d'une pompe centrifuge en aluminium.

**Volute (carter principal)**  
Le corps est un cylindre évidé de 180 mm de diamètre extérieur et 160 mm de
hauteur, avec des parois de 6 mm d'épaisseur, ouvert sur le dessus. L'alésage
central de 80 mm de diamètre traverse toute la hauteur pour le passage de l'arbre.

**Flasque de fermeture**  
Sur la face supérieure, ajouter un flasque annulaire plat de 180 mm de diamètre
extérieur, 120 mm de diamètre intérieur et 12 mm d'épaisseur. Répartir 8 trous
de boulonnage Ø9 mm à 45° les uns des autres sur un cercle de perçage de 155 mm
de diamètre.

**Tubulure d'aspiration**  
Sur le flanc gauche du corps, une tubulure cylindrique de 60 mm de diamètre
extérieur, 44 mm d'alésage intérieur, 80 mm de longueur, avec une bride carrée
100 × 100 mm en bout. La bride porte 4 trous de fixation Ø11 mm aux coins à
15 mm des bords.

**Tubulure de refoulement**  
Identique à la tubulure d'aspiration mais orientée vers le haut à 90°, avec une
bride ronde de 90 mm de diamètre portant 4 trous de Ø11 mm répartis en croix.
Créer la tubulure de refoulement par symétrie de la tubulure d'aspiration par
rapport au plan médian horizontal.

**Nervures de renfort**  
4 nervures trapézoïdales de 8 mm d'épaisseur et 30 mm de hauteur, disposées
en croix sur la face extérieure du cylindre, réparties à 90° les unes des autres.

**Fixations au bâti**  
4 pattes de fixation de 50 × 40 mm, épaisseur 10 mm, positionnées à 90° autour
de la base du corps. Chaque patte porte un trou de fixation Ø13 mm au centre et
un taraudage M8 profondeur 20 mm pour le câblage des capteurs de vibration.
Chanfreins 1,5 × 45° sur les arêtes supérieures de chaque patte.

**Joint et étanchéité**  
Une gorge annulaire de 4 mm de largeur et 3 mm de profondeur sur la face de
portée du flasque supérieur pour le logement du joint plat.

**Paramètres**  
Piloter les cotes principales (diamètre du corps, hauteur, épaisseur de paroi,
diamètre de l'alésage arbre) par des paramètres nommés pour permettre le
dimensionnement de la famille de pompes DN40 / DN50 / DN65.

---

### INTEG-02 — Harnais de baie avionique (câblage)

**Type :** EHI/EHA  
**Use cases couverts :** UC-16 · UC-17 · UC-18 · UC-19 · UC-20  
**Opération CATIA :**

Je veux créer le harnais de câblage complet d'une baie avionique. Le harnais
alimente et relie entre eux cinq équipements : le calculateur de navigation
(IRS), le système de gestion de vol (FMS), deux écrans de pilotage (PFD gauche
et PFD droit) et l'unité d'enregistrement de données (DAR).

**Tronc principal**  
Un tronc central de 600 mm de longueur et 25 mm de diamètre, blindé (tresse
métallique sur toute la longueur) pour la protection électromagnétique. Le
tronc part du pupitre de distribution électrique (position 0, 0, 0) et longe
le plancher de la baie jusqu'au nœud de distribution central.
Placer trois supports de fixation (clips P25) à 150 mm, 350 mm et 550 mm
depuis le départ.

**Nœud de distribution principal**  
À l'extrémité du tronc, un nœud en étoile à 5 branches. Chaque branche part
vers un équipement différent.

**Branche IRS** — 350 mm, diamètre 16 mm, blindée.  
Connecteur D38999 série III, 55 broches, mâle, référence D38999/26WJ55SN,
avec un connecteur femelle de verrouillage côté calculateur.  
Fils : 4 fils de puissance 28 VDC AWG20 rouge, 2 fils de retour GND AWG20 noir,
6 paires différentielles ARINC 429 AWG24 bleues.

**Branche FMS** — 400 mm, diamètre 16 mm, blindée.  
Connecteur D38999 série III, 37 broches, référence D38999/26WB35SN.  
Fils : 2 fils de puissance 28 VDC AWG20 rouge, 1 fil GND AWG20 noir,
4 paires ARINC 429 AWG24, 2 paires RS-422 AWG24 vertes.

**Branche PFD gauche** — 280 mm, diamètre 12 mm, gaine thermorétractable.  
Connecteur D-Sub 25 broches mâle, référence DSUB-25M-HD.  
Fils : 2 fils 28 VDC AWG22 rouge, 1 GND AWG22 noir, 3 paires vidéo
ARINC 818 AWG24 jaunes.

**Branche PFD droit** — 280 mm, diamètre 12 mm, gaine thermorétractable.  
Configuration identique au PFD gauche. Créer cette branche par symétrie
par rapport au plan axial de la baie, avec ses propres connecteurs renommés.

**Branche DAR** — 500 mm, diamètre 10 mm, conduit ondulé.  
Connecteur circulaire 19 broches, référence MIL-C-26482-19-35.  
Fils : 1 fil 28 VDC AWG22, 1 GND AWG22, 2 paires données ARINC 717 AWG24
orange, 1 fil discret AWG24 gris.

**Sous-bifurcation sur la branche IRS**  
À 200 mm depuis le nœud principal sur la branche IRS, une dérivation de 120 mm
vers le capteur de température de baie. Diamètre 6 mm, conduit ondulé.
2 fils : alimentation 5 VDC AWG28 rouge, signal analogique 0–5 V AWG28 blanc.

**Connecteur de mise à la masse de la baie**  
En bout du tronc principal (côté distribution), un connecteur de masse Faston
6,3 mm avec son fil de masse AWG12 vert-jaune de 100 mm.

**Conformité**  
Rayon de courbure minimum de 5 fois le diamètre pour chaque segment.
Espacement entre supports maximum 400 mm sur le tronc.
Chaque branche doit porter son numéro de câble en attribut (format WH-IRS-001,
WH-FMS-001, WH-PFD-L-001, WH-PFD-R-001, WH-DAR-001).

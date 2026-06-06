# tasks/todo.md — CATScript-AI PoC

**Phase active :** Phase 2 — Fonctionnalités avancées
**Dernière mise à jour :** 2026-06-06
**Statut :** Phase 1 complétée ✅ · Phase 2 en cours

---

## Légende
- `[ ]` En attente
- `[~]` En cours
- `[x]` Terminé (archiver après sprint)

---

## BLOC 0 — Scaffolding Projet

- [x] **T-001** — Initialiser la structure de répertoires du projet
  - `backend/`, `frontend/`, `data/pdf_docs/`, `data/chroma_db/`, `tests/`
  - Créer `requirements.txt` avec les dépendances Phase 1
  - Créer `dev.ps1` pour lancer backend + frontend en local
  - **Agent :** Architecte

- [x] **T-002** — Créer `ROADMAP.md` depuis Specification.md §9
  - Phases 1/2/3 avec critères de succès par phase
  - **Agent :** PM

---

## BLOC 1 — Pipeline d'Ingestion PDF (RAG)

- [x] **T-101** — Implémenter `backend/ingest.py` — chargement PDF
  - `pdfplumber` ou `PyMuPDF` pour extraction texte page par page
  - Fallback OCR via Tesseract si extraction vide (risque R-02)
  - Input : chemin vers `data/pdf_docs/` — Output : liste de pages textuelles
  - **Réf :** F-04, §7.3 étape 1

- [x] **T-102** — Implémenter chunker dans `backend/ingest.py`
  - `RecursiveCharacterTextSplitter` — 500 tokens, overlap 50
  - Métadonnées par chunk : `source_file`, `page_number`, `chunk_id` (UUID)
  - **Réf :** F-05, §8.1

- [x] **T-103** — Implémenter embedder + stockage ChromaDB
  - Modèle : `all-MiniLM-L6-v2` (local, zero data leakage) ou `text-embedding-3-small` (OpenAI)
  - Persistance fichier dans `data/chroma_db/`
  - Script CLI `python -m backend.ingest --docs data/pdf_docs/`
  - **Réf :** F-05, §7.2

- [x] **T-104** — Tests unitaires ingestion
  - Test sur PDF de 2 pages : vérifier nombre de chunks, présence métadonnées
  - Test idempotence : ré-ingérer le même doc ne crée pas de doublons
  - **Réf :** MANIFESTO §IV

---

## BLOC 2 — Backend FastAPI

- [x] **T-201** — Créer `backend/main.py` — app FastAPI + endpoint `/health`
  - CORS configuré pour `localhost`
  - **Réf :** NF-02, NF-03

- [x] **T-202** — Implémenter `backend/llm_router.py`
  - Interface `call_llm(provider, model, api_key, prompt) -> str`
  - Providers : `anthropic`, `google`, `openai`, `ollama`
  - **Réf :** F-14, §7.5

- [x] **T-203** — Implémenter `backend/rag_retriever.py`
  - `retrieve(query, top_k=5) -> list[Chunk]`
  - Embed query → ChromaDB similarity search → retourner chunks + scores
  - **Réf :** F-06, F-07, §7.3 étape 2

- [x] **T-204** — Implémenter `backend/prompt_builder.py`
  - Construire le prompt système depuis §7.4 (skeleton)
  - Injecter `retrieved_chunks`, `user_query`, `script_type`
  - Flag `low_confidence` si score max < seuil configurable
  - **Réf :** F-07, F-11

- [x] **T-205** — Implémenter endpoint `POST /generate`
  - Body : `GenerationRequest` (§8.2)
  - Response : `GenerationResponse` (§8.3) — `script`, `sources`, `confidence`
  - Validation Pydantic sur tous les champs
  - **Réf :** F-01, F-02, F-09, F-11, F-19

- [x] **T-206** — Tests unitaires backend
  - `test_llm_router.py` : mock des 4 providers
  - `test_rag_retriever.py` : ChromaDB en mémoire
  - `test_prompt_builder.py` : vérifier injection chunks
  - `test_generate_endpoint.py` : endpoint avec ChromaDB de test
  - **Réf :** MANIFESTO §IV

---

## BLOC 3 — Frontend UI

- [x] **T-301** — Scaffolding frontend (HTML + Vite ou HTML/JS pur)
  - Appliquer `STYLING_REFERENCE.html` : palette Obsidian, typographie Syne/Inter
  - Layout 2 colonnes : panneau gauche (input) / panneau droit (output)
  - **Agent :** UI/UX

- [x] **T-302** — Composant : formulaire de génération
  - Champ texte libre (F-01)
  - Sélecteur script type : `CATScript/VBA`, `EKL`, `EHI/EHA` (F-02)
  - Champs optionnels : type de pièce, système d'axes, standard harnais (F-03)
  - Indicateur provider actif (F-18)
  - **Agent :** UI/UX

- [x] **T-303** — Composant : panneau Settings (modal ou drawer)
  - Sélecteur provider (F-13, F-14)
  - Champs : API key (masqué, F-17), model name (F-15)
  - Persistance `localStorage` auto-save (F-16)
  - Guard : bloquer génération si aucun provider configuré (F-20)
  - **Agent :** UI/UX

- [x] **T-304** — Composant : preview de script
  - Coloration syntaxique du code généré (F-21)
  - Zone éditable inline avant export (F-23)
  - Bandeau sources (noms PDF + pages) (F-08)
  - Badge confidence : `HIGH` / `MEDIUM` / `LOW` (§8.3)
  - **Agent :** UI/UX

- [x] **T-305** — Composant : export script
  - Bouton "Copier" → clipboard (F-24)
  - Bouton "Télécharger" → `.CATScript` ou `.txt` selon type (F-25)
  - **Agent :** UI/UX

- [x] **T-306** — Notice données (NF-05)
  - Modal première utilisation : avertissement données confidentielles
  - Stockée en `localStorage` pour ne pas réapparaître
  - **Agent :** UI/UX

---

## BLOC 4 — Intégration & Validation E2E

- [x] **T-401** — Intégration frontend ↔ backend
  - Appel `POST /generate` depuis UI
  - Gestion états : chargement, erreur, succès
  - Timeout 30s côté client (NF-01)

- [x] **T-402** — Test E2E sur PDF réel
  - Ingérer 1 PDF de know-how CATIA (ou doc synthétique)
  - Générer 1 script CATScript, 1 EKL, 1 EHI/EHA
  - Vérifier : script non vide, sources affichées, confidence correcte

- [x] **T-403** — Audit qualité (agent Auditeur)
  - Vérifier : zéro `TODO`/`FIXME`, zéro import mort, build propre
  - Validation `✅ Audit passé` obligatoire avant clôture Phase 1
  - **Agent :** Auditeur

- [x] **T-404** — Mise à jour documentation
  - `/blueprint` → doc architecture technique Phase 1
  - `/guide` → documentation utilisateur (démarrage, ingestion, génération, export)

---

## BLOC 5 — Outillage Dev

- [x] **T-501** — Créer `.gitignore`
  - ✅ Créé le 2026-06-04
  - Exclure : `node_modules/`, `.env`, `__pycache__/`, `data/chroma_db/`, `data/pdf_docs/`, `history/`

- [x] **T-502** — Créer `tasks/lessons.md`
  - Fichier vide initialisé avec structure (lire avant chaque tâche, cf. CLAUDE.md)

---

---

## BLOC 6 — Fonctionnalités Avancées (Phase 2)

- [x] **T-601** — Corriger le 3D preview pour les harnais
  - Investiguer pourquoi le rendu `type: "harness"` ne s'affiche pas dans `frontend/index.html`
  - Vérifier le parsing JSON segments (`from`/`to`/`r`) et la création des `TubeGeometry` Three.js
  - Tester avec UC-16 (harnais linéaire) et UC-17 (harnais en Y) depuis `use_case_catalog.md`
  - Ajouter fallback visuel si geometry null (message explicite, pas un écran blanc)
  - **Agent :** UI/UX + Auditeur
  - **Réf :** `backend/prompt_builder.py::build_geometry_prompt`, `frontend/index.html` section Three.js

- [ ] **T-602** — Rétro-ingénierie de modèle CAD → script reproductible
  - Nouveau endpoint `POST /reverse-engineer` — accept `UploadFile` (`.CATPart`, `.CATProduct`, `.step`, `.stp`)
  - Parser les features géométriques du fichier : `pythonocc-core` (STEP/IGES) ou extraction XML CATPart
  - Construire un prompt de rétro-ingénierie dans `prompt_builder.py` : décrire les solides détectés → demander au LLM de générer le CATScript reproductible
  - Enrichir `Docs/glossaire.md` : ajouter section "Formats d'entrée — rétro-ingénierie" (CATPart, CATProduct, STEP, IGES)
  - Enrichir `Docs/use_case_catalog.md` : ajouter UC-21 (rétro-ingénierie CATPart simple) et UC-22 (rétro-ingénierie CATProduct assemblage)
  - UI : bouton "Importer un modèle" dans le panneau gauche, résultat affiché dans la zone script
  - **Agent :** Architecte (nouveau endpoint + parseur) + UI/UX (bouton import)
  - **Réf :** Specification.md — capacités d'analyse de l'existant

- [ ] **T-603** — Passage de harnais depuis un fichier DMU d'environnement
  - Nouveau endpoint `POST /harness-routing` — accept un fichier `.CATProduct` ou `.step` représentant l'environnement 3D
  - Extraire les surfaces, volumes et contraintes de passage (zones interdites, zones de passage) via `pythonocc-core`
  - Générer un prompt EHI/EHA qui décrit l'environnement et demande le script de routage avec points de passage 3D réels
  - Enrichir `Docs/glossaire.md` : ajouter "DMU (Digital Mock-Up)", "CATProduct d'environnement", "point de passage 3D"
  - Enrichir `Docs/use_case_catalog.md` : ajouter UC-23 (routage harnais sur DMU environnement)
  - UI : champ upload secondaire "Environnement DMU" visible uniquement quand `script_type = EHI/EHA`
  - **Agent :** Architecte + UI/UX
  - **Réf :** F-04 (ingestion), §7.3 — à étendre pour formats CAD natifs

- [ ] **T-604** — Mise en plan automatique d'un modèle chargé
  - Nouveau endpoint `POST /drawing` — accept un fichier `.CATPart` ou `.CATProduct`
  - Analyser les faces et volumes principaux (via STEP ou pythonocc) pour déterminer les vues pertinentes (dessus, face, profil, isométrique)
  - Générer un script CATScript `CATDrawing` : création du dessin, placement des vues projetées, cotation automatique des dimensions principales
  - Enrichir `Docs/glossaire.md` : ajouter section "Mise en plan — CATDrawing" (vues projetées, cartouche, normes ISO)
  - Enrichir `Docs/use_case_catalog.md` : ajouter UC-24 (mise en plan simple CATPart) et UC-25 (mise en plan CATProduct assemblage)
  - UI : bouton "Générer la mise en plan" dans le panneau options, output = script CATDrawing téléchargeable en `.CATScript`
  - **Agent :** Architecte + UI/UX + Auditeur
  - **Réf :** F-25 (export script), types de sortie à étendre

---

## Ordre d'Exécution Recommandé

```
T-001 → T-002 → T-501 → T-502
→ T-101 → T-102 → T-103 → T-104
→ T-201 → T-202 → T-203 → T-204 → T-205 → T-206
→ T-301 → T-302 → T-303 → T-304 → T-305 → T-306
→ T-401 → T-402 → T-403 → T-404
→ T-601 → T-602 → T-603 → T-604
```

# ROADMAP — CATScript-AI PoC

**Projet :** CATScript-AI | **Codename :** FastCAD
**Dernière mise à jour :** 2026-06-04

---

## Phase 1 — PoC *(scope actuel)*

**Objectif :** Démontrer la faisabilité d'une génération de scripts CATIA V5 R27 guidée par RAG sur une machine solo.

**Critères de succès :**
- [x] Pipeline d'ingestion PDF → ChromaDB opérationnel
- [x] Génération de scripts CATScript, EKL et EHI/EHA depuis l'UI
- [x] 4 providers LLM configurables via l'UI (Anthropic, Google, OpenAI, Ollama)
- [x] Preview éditable + export `.CATScript` / `.txt`
- [x] Temps de réponse < 30s sur machine locale
- [x] Zéro donnée confidentielle envoyée sans notice utilisateur
- [x] Audit Auditeur passé (`✅`)

**Stack :** FastAPI · ChromaDB · sentence-transformers · HTML/JS pur

---

## Phase 2 — Knowledge Graph Evolution

**Objectif :** Enrichir la récupération par traversée de graphe pour des requêtes complexes.

**Critères de succès :**
- [ ] Remplacement ou augmentation de ChromaDB par Neo4j ou RDFLib
- [ ] Entités CATIA (pièces, relations, contraintes) modélisées comme nœuds/arêtes
- [ ] Récupération par traversée de graphe (au-delà de la similarité vectorielle)
- [ ] Ingestion étendue : Word, Excel, Confluence, Wiki

**Prérequis :** Phase 1 livrée et validée en production interne.

---

## Phase 3 — Integration & Scale

**Objectif :** Déploiement multi-utilisateurs sur l'intranet Airbus avec exécution directe dans CATIA V5.

**Critères de succès :**
- [ ] Bridge COM CATIA V5 pour exécution one-click des scripts générés
- [ ] Déploiement web multi-utilisateurs (intranet Airbus)
- [ ] Contrôle d'accès par rôle + gouvernance documentaire
- [ ] Revue de sécurité IT et conformité Airbus
- [ ] *(Optionnel)* Preview 3D paramétrique via Three.js si bridge COM insuffisant

**Prérequis :** Phase 2 livrée · revue sécurité IT planifiée · équipe ops identifiée.

# tasks/lessons.md — Mémoire d'Erreurs Active

**Règle :** Lire ce fichier avant de démarrer toute tâche. Quand > 5 entrées actives, promouvoir dans le profil agent concerné ou MANIFESTO.md puis purger.

---

| # | Leçon | Contexte | Règle Dérivée | Promu ? |
|---|-------|----------|---------------|---------|
| L-001 | Double extraction PDF (`pdfplumber` + `PyMuPDF`) dans `requirements.txt` viole le minimalisme des dépendances | T-001 audit — Spec §7.2 dit "or" | Trancher le choix primaire dans T-101 ; documenter le fallback si les deux sont nécessaires | Non |
| L-002 | `POST /geometry` ne transmettait pas `script_type` → LLM choisissait toujours le format "part" pour les harnais ; `setFromUnitVectors` crashait silencieusement sur dir≈(0,-1,0) | T-601 | Passer `script_type` à tout endpoint LLM qui génère du contenu conditionnel ; guard anti-parallèle obligatoire sur `setFromUnitVectors` Three.js | Non |

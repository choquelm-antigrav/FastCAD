# tasks/lessons.md — Mémoire d'Erreurs Active

**Règle :** Lire ce fichier avant de démarrer toute tâche. Quand > 5 entrées actives, promouvoir dans le profil agent concerné ou MANIFESTO.md puis purger.

---

| # | Leçon | Contexte | Règle Dérivée | Promu ? |
|---|-------|----------|---------------|---------|
| L-001 | Double extraction PDF (`pdfplumber` + `PyMuPDF`) dans `requirements.txt` viole le minimalisme des dépendances | T-001 audit — Spec §7.2 dit "or" | Trancher le choix primaire dans T-101 ; documenter le fallback si les deux sont nécessaires | Non |

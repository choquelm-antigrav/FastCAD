---
name: ui-ux
description: Garant de l'esthétique et du respect des design tokens. S'active dès qu'un fichier HTML, CSS ou un composant front-end est créé ou modifié.
---

## Fichiers Requis
Lire dans cet ordre avant toute action :
1. [[design-tokens.json]] — localiser à la racine du projet courant. BLOQUER si absent.
2. [[STYLING_REFERENCE.html]] — vérité visuelle absolue

# Rôle
Perfection esthétique dans les limites du système défini. Zéro liberté créative hors des design tokens.

# Protocole
1. **Lire en premier** — avant toute modification, lire [[design-tokens.json]] pour extraire les valeurs courantes.
2. **Injection stricte** — utiliser exclusivement les codes hexa, rayons, espacements et valeurs de typographie issus de [[design-tokens.json]]. Inventer des valeurs est interdit.
3. **Audit sémantique** — vérifier que chaque élément UI correspond à l'intention décrite dans [[design-tokens.json]].
4. **Vérification référence** — recouper avec [[STYLING_REFERENCE.html]] comme vérité visuelle absolue.

# Contrainte Absolue
Si [[design-tokens.json]] n'existe pas à la racine du projet courant, bloquer et le demander avant toute action.

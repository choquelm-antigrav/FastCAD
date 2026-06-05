# Constitution du Projet

## I. Principes Fondamentaux
- **Simplicité Radicale :** Si une fonction peut s'écrire en 5 lignes plutôt qu'en 10, la version courte gagne systématiquement.
- **Zéro Dette Technique :** Aucun hack temporaire. On construit pour durer, ou on ne construit pas.
- **Transparence Sémantique :** Le code doit être auto-documenté. Les noms de variables et de fonctions doivent être explicites.

## II. Politique de Rigueur (Zéro Tolérance)
- **Complétude :** Une tâche n'est terminée que si elle est testée et documentée.
- **Interdiction du "Lendemain" :** Les commentaires `// TODO` ou `// À fixer` sont des échecs d'audit.
- **Minimalisme des Dépendances :** L'ajout d'une bibliothèque tierce doit être justifié par l'Architecte.

## III. Standards de Communication
- **Économie de Signal :** Les agents privilégient la densité d'information au volume de texte.
- **Apprentissage Continu :** Chaque erreur identifiée devient une règle dans tasks/lessons.md. Quand les leçons dépassent 5 entrées actives, les promouvoir dans le profil agent concerné ou dans ce Manifeste, puis purger le fichier.

## IV. Protocole d'Hygiène
Avant de marquer toute tâche DONE, vérifier :
1. Aucun `// TODO`, `// FIXME` ou commentaire temporaire ne subsiste.
2. Aucun code mort ou import inutilisé n'est présent.
3. Le build passe sans erreur ni avertissement.
4. L'agent Auditeur a validé avec `✅ Audit passé`.

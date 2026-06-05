# Guide Utilisateur — CATScript-AI
**Version :** 1.0 — Phase 1 PoC  
**Public cible :** Ingénieurs et concepteurs CATIA V5, sans compétences en développement logiciel

---

## Chapitre 1 — Présentation

### Pourquoi CATScript-AI existe

Écrire un script CATIA depuis zéro prend du temps : retrouver la bonne API, adapter un exemple d'un collègue, corriger les erreurs de syntaxe. CATScript-AI automatise cette étape. Vous décrivez en français ce que vous voulez faire dans CATIA, l'outil génère le script prêt à copier.

**Objectif principal :** réduire de plusieurs heures à quelques minutes la rédaction de scripts CATIA répétitifs, en s'appuyant sur les documents métier (procédures, standards, guides) déjà produits par l'équipe.

### L'analogie

Imaginez un collègue très expérimenté qui a lu tous vos documents internes et tous les manuels CATIA. Vous lui dites : « J'ai besoin d'un script qui renomme toutes les instances d'un assembly selon une règle de nommage projet ». Il comprend le contexte, cherche dans ses notes, et vous rend un script commenté en quelques secondes. CATScript-AI est ce collègue — sauf qu'il ne se fatigue pas et travaille hors ligne si besoin.

### Ce que l'outil fait (périmètre PoC)

- Accepte une description en langage naturel d'une opération CATIA
- Recherche dans les documents PDF ingérés les passages pertinents (voir Chapitre 4)
- Génère un script CATIA V5 R27 commenté, prêt à être exécuté manuellement
- Supporte trois types de scripts : CATScript/VBA, EKL, EHI/EHA (définis au Chapitre 5)
- Indique quels documents ont servi à construire la réponse
- Permet de modifier le script dans l'interface avant de le télécharger

### Ce que l'outil ne fait PAS (limites PoC)

- **Ne lance pas le script automatiquement dans CATIA.** L'exécution reste manuelle via le menu Outils > Macros de CATIA.
- Ne connaît pas l'état de votre modèle 3D ouvert dans CATIA.
- Ne supporte pas CATIA V6 ni la plateforme 3DEXPERIENCE.
- Ne dispose pas d'un système d'authentification multi-utilisateurs.
- Ne génère pas d'aperçu 3D du résultat — le script commenté est le seul retour visuel disponible à ce stade.

---

## Chapitre 2 — Démarrage

### Pré-requis système

| Composant | Version minimale |
|-----------|-----------------|
| Système d'exploitation | Windows 10 ou Windows 11 |
| Python | 3.11 ou supérieur |
| Navigateur web | Chrome, Edge ou Firefox (version récente) |
| Connexion internet | Requise pour les providers cloud (Anthropic, Google, OpenAI) — non requise pour Ollama |

Pour vérifier votre version de Python, ouvrez PowerShell et tapez :
```
python --version
```

### Installation

Ouvrez PowerShell dans le dossier du projet, puis exécutez :
```powershell
pip install -r requirements.txt
```

Cette commande installe toutes les bibliothèques nécessaires (backend FastAPI, moteur de recherche vectorielle ChromaDB, connecteurs LLM).

### Lancement

```powershell
./dev.ps1
```

Le script démarre le serveur local et ouvre automatiquement votre navigateur sur `http://localhost:8000`. Si le navigateur ne s'ouvre pas, saisissez cette adresse manuellement dans la barre d'adresse.

### Notice données confidentielles (premier démarrage)

Au premier lancement, un message d'avertissement s'affiche. Il rappelle que **les requêtes envoyées à des providers cloud (Anthropic, Google, OpenAI) transitent par internet**. Ne saisissez pas de données Airbus classifiées ou soumises à des accords de confidentialité sans autorisation préalable de votre responsable sécurité. Si la confidentialité est une contrainte, utilisez Ollama (provider local — voir Chapitre 3).

---

## Chapitre 3 — Configurer un provider LLM

Un **LLM (Large Language Model)** est le moteur de génération de texte — le « cerveau » qui rédige le script à partir de votre description et des documents récupérés. CATScript-AI supporte quatre providers (fournisseurs) au choix.

### Où se trouve le bouton Settings

Dans la barre de titre en haut à droite de l'interface, cliquez sur le bouton **⚙** (icône engrenage). Le panneau Settings s'ouvre en superposition.

### Description du panneau Settings

Le panneau affiche quatre cartes, une par provider :

| Carte | Provider | Type |
|-------|----------|------|
| **Anthropic** | Claude Sonnet / Haiku | Cloud — clé API requise |
| **Google** | Gemini 1.5 Pro / 2.0 Flash | Cloud — clé API requise |
| **OpenAI** | GPT-4o / GPT-4 Turbo | Cloud — clé API requise |
| **Ollama** | Modèles locaux (ex. llama3, mistral) | Local — aucune clé requise |

### Comment configurer un provider cloud (Anthropic, Google, OpenAI)

1. Cliquez sur la carte du provider souhaité pour la sélectionner.
2. Dans le champ **API Key**, saisissez votre clé d'accès. Le champ est masqué (comme un mot de passe) — la clé n'est jamais affichée en clair ni stockée côté serveur.
3. Dans le champ **Modèle**, saisissez le nom exact du modèle (exemples : `claude-sonnet-4-5`, `gemini-2.0-flash`, `gpt-4o`).
4. Cliquez sur **Sauvegarder**.

### Cas particulier : Ollama (modèle local)

Ollama fait tourner un LLM entièrement sur votre machine. Aucune donnée ne quitte le poste.

1. Installez Ollama depuis [https://ollama.com](https://ollama.com) et téléchargez un modèle (ex. `ollama pull llama3`).
2. Dans Settings, sélectionnez la carte **Ollama**.
3. Le champ API Key est remplacé par un champ **URL** (par défaut `http://localhost:11434`). Laissez la valeur par défaut sauf si vous avez modifié le port Ollama.
4. Renseignez le nom du modèle installé (ex. `llama3`).
5. Cliquez sur **Sauvegarder**.

### Persistance automatique

La configuration est sauvegardée dans le **localStorage** de votre navigateur (zone de stockage locale propre à chaque navigateur). Elle est rechargée automatiquement à chaque ouverture de l'application. Vider le cache du navigateur efface cette configuration.

### Indicateur provider actif

Dans la barre de titre, à droite du bouton ⚙, un badge affiche le nom du provider et du modèle actuellement actifs (ex. `ANTHROPIC — claude-sonnet-4-5`). Si aucun provider n'est configuré, le badge indique `NO PROVIDER` en grisé.

---

## Chapitre 4 — Ingérer des documents PDF

### Pourquoi ingérer avant de générer

CATScript-AI utilise une architecture **RAG (Retrieval-Augmented Generation)** : avant de générer un script, il cherche dans une base de connaissances locale les passages les plus pertinents de vos documents métier, puis les fournit au LLM comme contexte. Plus la base est riche, plus le script généré sera précis et conforme à vos standards.

Sans ingestion préalable, l'outil fonctionne mais sans contexte spécifique — il génère des scripts CATIA génériques, sans connaissance de vos procédures internes.

### Commande d'ingestion

Placez vos PDFs dans le dossier `data/pdf_docs/`, puis exécutez depuis PowerShell :

```powershell
python -m backend.ingest --docs data/pdf_docs/
```

L'opération peut durer de quelques secondes à quelques minutes selon le volume de documents.

### Ce qui se passe en coulisse

1. **Extraction** : le texte de chaque page PDF est extrait.
2. **Découpage en morceaux (chunks)** : le texte est découpé en segments d'environ 500 tokens (un token correspond approximativement à 3/4 d'un mot). Chaque segment se chevauche légèrement avec le suivant (50 tokens de recouvrement) pour ne pas couper une phrase au milieu d'une information clé.
3. **Embedding** : chaque segment est converti en un vecteur numérique (une **représentation mathématique** de son sens) par un modèle d'embedding.
4. **Stockage dans ChromaDB** : les vecteurs et le texte source sont stockés dans **ChromaDB**, une base de données vectorielle locale et sans serveur, persistée dans le dossier `data/chroma/`.

### Idempotence

Si vous relancez la commande sur les mêmes PDFs, l'outil détecte les documents déjà ingérés et ne crée pas de doublons. Vous pouvez ajouter de nouveaux PDFs dans `data/pdf_docs/` et relancer la commande : seuls les nouveaux fichiers seront traités.

### Dossier cible

```
data/
└── pdf_docs/
    ├── guide_catscript_v5.pdf
    ├── standard_nommage_2024.pdf
    └── ...
```

---

## Chapitre 5 — Générer un script

### Description visuelle de l'interface

L'interface est divisée en deux panneaux :

- **Panneau gauche (formulaire)** : saisissez votre demande et paramétrez la génération.
- **Panneau droit (résultat)** : le script généré s'affiche ici, avec les sources et le badge de confiance.

### Les trois types de scripts

Sélectionnez le type adapté à votre besoin via les boutons radio du panneau gauche :

| Type | Définition |
|------|-----------|
| **CATScript / VBA** | Langage de macro intégré à CATIA V5, similaire au Visual Basic. Permet d'automatiser les opérations de modélisation, d'assemblage, de dessin. |
| **EKL** | Engineering Knowledge Language — langage de règles et formules du module CATIA Knowledge Advisor. Sert à définir des contraintes, des règles de conception ou des paramétrisations automatiques. |
| **EHI / EHA** | Electrical Harness Installation / Electrical Harness Assembly — scripts de routage de faisceaux électriques dans les modules CATIA dédiés au câblage. |

### Champs optionnels

Ces champs affinent la génération mais ne sont pas obligatoires :

- **Type de pièce** : précisez le contexte (ex. « pièce de structure », « connecteur électrique »).
- **Système d'axes** : indiquez si un repère particulier doit être utilisé.
- **Standard harnais** : pour les scripts EHI/EHA, précisez le standard de câblage applicable.

### Bouton « Générer »

Le bouton **Générer** est **désactivé** (grisé) si aucun provider LLM n'est configuré. Configurez d'abord un provider (Chapitre 3), puis revenez au formulaire.

### États de la génération

| État | Ce que vous voyez |
|------|------------------|
| **En attente** | Le panneau droit affiche un message d'invite. |
| **Chargement** | Un spinner tourne dans le panneau droit. Durée typique : 5 à 30 secondes. |
| **Résultat** | Le script apparaît avec coloration syntaxique, accompagné des sources et du badge confidence. |

### Bandeau sources

Sous le script, un bandeau liste les documents PDF (et les numéros de page) qui ont informé la génération. Exemple :

```
Sources : guide_catscript_v5.pdf (p. 12) · standard_nommage_2024.pdf (p. 3)
```

Cela permet de retrouver le contexte original si le script mérite vérification.

### Badge confidence

Le badge indique la qualité de la récupération documentaire :

| Badge | Signification |
|-------|--------------|
| **HIGH** | Les documents ingérés contiennent des passages très proches de votre demande. Résultat fiable. |
| **MEDIUM** | Des passages partiellement pertinents ont été trouvés. Relisez le script avec attention. |
| **LOW** | Peu ou aucun passage pertinent trouvé. Le script est généré principalement depuis les connaissances générales du LLM, sans ancrage dans vos documents. Vérification approfondie recommandée. Envisagez d'ingérer des documents plus spécifiques. |

---

## Chapitre 6 — Modifier et exporter

### Zone éditable

Le script affiché dans le panneau droit est **entièrement éditable**. Cliquez directement dans la zone de code pour corriger une valeur, renommer une variable, ajuster un paramètre ou ajouter un commentaire avant d'exporter.

### Bouton « Copier »

Cliquez sur **Copier** pour placer l'intégralité du script dans le presse-papiers. Vous pouvez ensuite le coller directement dans l'éditeur de macros de CATIA.

### Bouton « Télécharger »

Cliquez sur **Télécharger** pour enregistrer le script sous forme de fichier. L'extension dépend du type :

| Type de script | Extension téléchargée |
|---------------|-----------------------|
| CATScript / VBA | `.CATScript` |
| EKL | `.txt` |
| EHI / EHA | `.txt` |

### Utiliser le fichier dans CATIA V5 R27

**Pour un fichier `.CATScript` (macro VBA) :**

1. Dans CATIA, ouvrez le menu **Outils** → **Macro** → **Macros...**.
2. Dans la boîte de dialogue, cliquez sur **Bibliothèques...** et sélectionnez le dossier contenant votre fichier.
3. Sélectionnez la macro dans la liste et cliquez sur **Exécuter**.

**Pour un script EKL :**

1. Ouvrez l'atelier **Knowledge Advisor** (menu Démarrer → Analyse et Simulation ou Infrastructure selon votre configuration).
2. Dans le **Browser de règles**, importez ou créez une règle et collez le contenu du fichier `.txt`.

**Pour un script EHI/EHA :**

1. Ouvrez l'atelier **Electrical Harness Installation** ou **Electrical Harness Assembly**.
2. Utilisez l'automatisation via l'éditeur de scripts du module ou collez dans une règle Knowledge.

> **Conseil :** Testez toujours le script sur une copie de votre modèle avant de l'appliquer à un fichier de production.

---

## Chapitre 7 — Limites et précautions

### Confidentialité des données

Les providers cloud (Anthropic, Google, OpenAI) reçoivent le texte de votre requête et des extraits de vos documents ingérés. **Ne saisissez pas de données Airbus classifiées, soumises à ITAR, ou couvertes par un accord de non-divulgation sans accord explicite de votre responsable sécurité informatique.** En cas de doute, utilisez Ollama (provider local) : aucune donnée ne quitte votre machine.

### Exécution manuelle obligatoire

CATScript-AI génère des scripts mais **ne les exécute pas automatiquement dans CATIA**. L'exécution reste entièrement sous votre contrôle. Cette contrainte est intentionnelle dans le cadre du PoC — une exécution automatisée via le pont COM de CATIA est prévue en Phase 3.

### Relecture avant exécution

Un LLM peut générer un script syntaxiquement correct mais logiquement incorrect (paramètre erroné, nom d'API mal orthographié, logique inversée). **Relisez systématiquement le script avant de l'exécuter dans CATIA**, en particulier pour les opérations destructives (suppression, remplacement, modification de références).

Les scripts générés avec un badge **LOW confidence** méritent une attention particulière : l'outil ne disposait pas de contexte documentaire suffisant pour ancrer la génération dans vos standards.

### Périmètre CATIA

L'outil cible exclusivement **CATIA V5 R27**. Les scripts générés ne sont pas garantis compatibles avec CATIA V6, 3DEXPERIENCE ou d'autres versions de V5.

---

*Fin du guide — CATScript-AI v1.0 PoC*

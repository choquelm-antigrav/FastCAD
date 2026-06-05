# CATIA Script Generator — Solution Specification
**Project codename:** CATScript-AI
**Version:** 0.2 — PoC
**Author:** Max
**Date:** 2026-06-04
**Status:** Draft

---

## 1. Executive Summary

CATScript-AI is a solo-built Proof of Concept that allows mechanical designers to generate ready-to-use CATIA V5 R27 scripts (CATScript/VBA macros, EKL scripts, EHI/EHA electrical harness routings) from natural language or structured input. The system leverages a Retrieval-Augmented Generation (RAG) architecture grounded in the team's existing know-how documents (initially PDF), with a vector search layer designed to evolve into a full Knowledge Graph in later phases.

---

## 2. Objectives

| # | Objective |
|---|-----------|
| O1 | Reduce time spent writing repetitive CATIA scripts from scratch |
| O2 | Capture and reuse team know-how embedded in documents |
| O3 | Deliver a working PoC in a solo-developer timeframe |
| O4 | Establish a foundation that can evolve to a Knowledge Graph and scale across teams |

---

## 3. Scope

### 3.1 In Scope (PoC)

- Natural language input from the designer describing the desired operation
- Retrieval of relevant know-how from PDF documents via vector search (RAG)
- Generation of CATIA V5 R27-compatible scripts:
  - CATScript / VBA macros
  - EKL scripts
  - EHI / EHA electrical harness routing scripts
- Script preview before delivery
- Script export as a `.CATScript` or `.txt` file ready for manual execution in CATIA
- UI-driven LLM configuration panel (provider, model, API key) stored in browser localStorage

### 3.2 Out of Scope (PoC)

- Direct execution of scripts inside CATIA (no COM/automation bridge in PoC)
- CATIA plugin / embedded UI
- Support for CATIA V6 or 3DEXPERIENCE
- Real-time CATIA model state awareness
- Knowledge Graph construction (deferred to Phase 2)
- Multi-user / authentication layer
- Airbus IT deployment or security review
- 3D or 2D geometric preview of generated scripts — CATIA scripts call CATIA's internal COM API and cannot be executed or meaningfully rendered in a browser; well-commented script text is the PoC substitute for visual feedback

---

## 4. Users

| Role | Description | Primary Need |
|------|-------------|--------------|
| Mechanical Designer | Daily CATIA V5 user | Generate scripts fast without writing code |
| Team Lead / Knowledge Owner | Maintains know-how documents | Ensure team practices are captured and reused |
| PoC Developer (Max) | Solo builder | Simple, maintainable stack |

---

## 5. Functional Requirements

### 5.1 Input Interface

| ID | Requirement |
|----|-------------|
| F-01 | The system SHALL accept a natural language description of the desired CATIA operation |
| F-02 | The system SHALL allow the user to specify the target script type (CATScript/VBA, EKL, EHI/EHA) |
| F-03 | The system MAY offer optional structured fields (e.g., target part type, axis system, harness standard) to refine generation |

### 5.2 Know-How Retrieval (RAG Layer)

| ID | Requirement |
|----|-------------|
| F-04 | The system SHALL ingest PDF documents and chunk them into retrievable segments |
| F-05 | The system SHALL embed document chunks using a vector embedding model |
| F-06 | The system SHALL retrieve the top-k most relevant chunks given the user's input |
| F-07 | The retrieved chunks SHALL be injected into the LLM prompt as grounding context |
| F-08 | The system SHALL display which source document(s) informed the generation (traceability) |

### 5.3 Script Generation

| ID | Requirement |
|----|-------------|
| F-09 | The system SHALL generate a syntactically valid CATIA V5 R27-compatible script |
| F-10 | The system SHALL include inline comments in the generated script explaining each major step |
| F-11 | The system SHALL warn the user if no relevant know-how chunk was found (low-confidence generation) |
| F-12 | The system SHALL support regeneration with adjusted parameters if the first result is unsatisfactory |

### 5.4 LLM Configuration (UI-driven)

| ID | Requirement |
|----|-------------|
| F-13 | The system SHALL provide a Settings panel in the UI where the user can configure the LLM provider |
| F-14 | The supported providers SHALL be: Anthropic (Claude), Google (Gemini / Vertex AI), OpenAI (GPT-4), Ollama (local) |
| F-15 | For each provider the user SHALL be able to specify: the API key (or Ollama base URL) and the model name/ID |
| F-16 | The configuration SHALL be stored in browser `localStorage` and auto-loaded on next session |
| F-17 | The API key SHALL be masked (password field) in the UI and never logged or transmitted to the backend in plain text beyond the single API call |
| F-18 | The UI SHALL display the currently active provider and model name at all times |
| F-19 | The backend SHALL expose a provider-agnostic `/generate` endpoint; the provider routing SHALL be determined by a `provider` parameter sent with each request |
| F-20 | If no configuration is set, the system SHALL prompt the user to configure a provider before allowing generation |

### 5.5 Script Preview

| ID | Requirement |
|----|-------------|
| F-21 | The system SHALL display the generated script in a syntax-highlighted code preview panel |
| F-22 | The preview SHALL be available before the user downloads or copies the script |
| F-23 | The user SHALL be able to edit the script inline in the preview before exporting |

### 5.6 Script Export

| ID | Requirement |
|----|-------------|
| F-24 | The system SHALL allow the user to copy the script to clipboard |
| F-25 | The system SHALL allow the user to download the script as a `.CATScript` or `.txt` file |

---

## 6. Non-Functional Requirements

| ID | Requirement |
|----|-------------|
| NF-01 | Response time (generation) SHALL be under 30 seconds for typical requests |
| NF-02 | The PoC SHALL run on a single developer machine (Windows 10/11) without server infrastructure |
| NF-03 | The solution SHALL be operable via a local web browser (localhost) |
| NF-04 | The codebase SHALL be maintainable by a single developer with no dedicated ops support |
| NF-05 | No confidential Airbus data SHALL be sent to external APIs without explicit user acknowledgment (data notice on first use) |

---

## 7. Architecture

### 7.1 High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        Browser UI (localhost)                     │
│   [Natural Language Input]  [Script Type Selector]               │
│   [Source References]       [Code Preview + Edit]                │
│   [Copy / Download]         [⚙ Settings: Provider / Model / Key] │
│                              (stored in localStorage)             │
└───────────────────┬──────────────────────────────────────────────┘
                    │ HTTP (localhost)
                    │ {query, script_type, provider, model, api_key}
┌───────────────────▼──────────────────────────────────────────────┐
│                    Python Backend (FastAPI)                        │
│                                                                   │
│  ┌─────────────────┐      ┌──────────────────────────────────┐   │
│  │  RAG Retriever   │      │      LLM Prompt Builder           │   │
│  │  (vector search) │─────▶│  system prompt + chunks +        │   │
│  │  ChromaDB        │      │  user query + script type        │   │
│  └────────┬────────┘      └──────────────┬───────────────────┘   │
│           │                               │                       │
│  ┌────────▼────────┐      ┌──────────────▼───────────────────┐   │
│  │  PDF Ingestion   │      │     LLM Provider Router           │   │
│  │  + Chunker       │      │  ┌──────────┐ ┌───────────────┐  │   │
│  │  + Embedder      │      │  │ Anthropic│ │ Google Gemini │  │   │
│  └─────────────────┘      │  ├──────────┤ ├───────────────┤  │   │
│                            │  │  OpenAI  │ │ Ollama(local) │  │   │
│                            │  └──────────┘ └───────────────┘  │   │
│                            └──────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
                    │
        ┌───────────▼───────────┐
        │   /data/pdf_docs/      │
        │   (team know-how PDFs) │
        └───────────────────────┘
```

### 7.2 Technology Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| UI | React (Vite) or simple HTML+JS | Lightweight, runs in browser |
| Backend | Python 3.11 + FastAPI | Solo-friendly, async, easy to extend |
| PDF ingestion | `pdfplumber` or `PyMuPDF` | Reliable text extraction from PDFs |
| Chunking | LangChain `RecursiveCharacterTextSplitter` | Battle-tested, configurable |
| Embeddings | `text-embedding-3-small` (OpenAI) or `all-MiniLM-L6-v2` (local) | Fast, cost-effective |
| Vector store | ChromaDB (local, file-based) | No server needed, persistent |
| LLM — Anthropic | `anthropic` Python SDK | Claude Sonnet / Haiku |
| LLM — Google | `google-generativeai` or `vertexai` SDK | Gemini 1.5 Pro / 2.0 Flash |
| LLM — OpenAI | `openai` Python SDK | GPT-4o / GPT-4 Turbo |
| LLM — Ollama | `ollama` Python SDK (HTTP to localhost:11434) | Local models, no data leaves machine |
| LLM router | Custom `llm_router.py` abstraction | Single interface, provider-swappable |
| LLM config storage | Browser `localStorage` | Zero-infrastructure, PoC-appropriate |
| Script output | Plain text / `.CATScript` file | Directly usable in CATIA V5 |

### 7.3 RAG Pipeline Detail

1. **Ingestion (run once per document batch)**
   - Load PDF → extract text per page → chunk (≈500 tokens, 50-token overlap)
   - Embed each chunk → store in ChromaDB with metadata (source file, page number)

2. **At generation time**
   - Embed user query → retrieve top-k chunks (k=5 default) from ChromaDB
   - Build prompt: system instructions + retrieved chunks + user query + script type
   - Call LLM API → receive generated script
   - Return script + source references to UI

### 7.4 Prompt Design (skeleton)

```
SYSTEM:
You are an expert CATIA V5 R27 automation engineer.
You generate syntactically correct {script_type} scripts.
You ONLY use the know-how context provided below.
If the context is insufficient, say so explicitly before generating.
Always add inline comments to explain each step.

KNOW-HOW CONTEXT:
{retrieved_chunks}

USER REQUEST:
{user_query}

Generate the script now.
```

### 7.5 LLM Provider Router Design

The backend exposes a single `/generate` endpoint. A `llm_router.py` module abstracts all provider differences behind a common interface:

```python
# llm_router.py — provider-agnostic interface
def call_llm(provider: str, model: str, api_key: str, prompt: str) -> str:
    if provider == "anthropic":
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(model=model, max_tokens=4096,
                       messages=[{"role": "user", "content": prompt}])
        return response.content[0].text

    elif provider == "google":
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        return genai.GenerativeModel(model).generate_content(prompt).text

    elif provider == "openai":
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        return client.chat.completions.create(model=model,
                   messages=[{"role": "user", "content": prompt}]
               ).choices[0].message.content

    elif provider == "ollama":
        import ollama
        return ollama.chat(model=model,
                   messages=[{"role": "user", "content": prompt}]
               )["message"]["content"]
```

> **Note on Vertex AI:** if Airbus uses Gemini via Google Cloud Vertex AI rather than the Google AI Studio API key, replace the `google-generativeai` SDK with the `vertexai` SDK and authenticate via a GCP service account instead of an API key. This is a one-line swap in `llm_router.py`.

---



### 8.1 Document Chunk (stored in ChromaDB)

| Field | Type | Description |
|-------|------|-------------|
| `chunk_id` | string | UUID |
| `source_file` | string | Original PDF filename |
| `page_number` | int | Page in source PDF |
| `content` | string | Raw text of the chunk |
| `embedding` | vector | Float array (model-dependent dimension) |

### 8.2 Generation Request

| Field | Type | Description |
|-------|------|-------------|
| `query` | string | Natural language description from designer |
| `script_type` | enum | `catscript`, `ekl`, `ehi_eha` |
| `top_k` | int | Number of chunks to retrieve (default: 5) |
| `provider` | enum | `anthropic`, `google`, `openai`, `ollama` |
| `model` | string | Model name/ID as specified by the user (e.g. `gemini-2.0-flash`) |
| `api_key` | string | API key for the selected provider (masked in transit, never stored server-side) |

### 8.3 Generation Response

| Field | Type | Description |
|-------|------|-------------|
| `script` | string | Generated script content |
| `sources` | list | Source file + page for each retrieved chunk |
| `confidence` | enum | `high`, `medium`, `low` (based on retrieval score) |

---

## 9. Phased Roadmap

### Phase 1 — PoC (current scope)

- PDF ingestion pipeline
- Vector search (ChromaDB)
- LLM-based script generation (CATScript, EKL, EHI/EHA)
- Local web UI with preview and export
- Manual execution of scripts in CATIA V5

### Phase 2 — Knowledge Graph Evolution

- Replace or augment vector store with a Knowledge Graph (e.g., Neo4j or RDFLib)
- Model CATIA design entities, relationships, and constraints as graph nodes/edges
- Enrich retrieval with graph traversal (not just similarity search)
- Support additional document formats: Word, Excel, Confluence, Wiki

### Phase 3 — Integration & Scale

- CATIA V5 COM automation bridge for one-click script execution
- Multi-user web deployment (Airbus intranet)
- Role-based access and document governance
- IT security review and compliance
- *(Optional)* 3D parametric preview via Three.js + LLM-generated geometry descriptor JSON, if the COM bridge proves too heavy for quick feedback

---

## 10. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| LLM generates syntactically invalid CATIA script | Medium | High | Add a script validator / linter step; include CATIA API examples in system prompt |
| PDF text extraction quality is poor (scanned docs) | Medium | Medium | Use OCR fallback (Tesseract); flag low-quality chunks |
| Retrieved chunks are irrelevant (poor embedding) | Medium | High | Tune chunk size and overlap; evaluate retrieval quality on test cases |
| Data confidentiality concern with cloud LLM API | Low (PoC) | High | Display data notice; plan on-premise LLM for Phase 3 |
| CATIA V5 R27 API coverage gaps in LLM training data | Medium | Medium | Build a curated CATIA API reference doc to include in RAG corpus |

---

## 11. Open Questions

| # | Question | Owner | Target |
|---|----------|-------|--------|
| OQ-1 | Which PDF documents are available as initial know-how corpus? | Max | Before dev start |
| OQ-2 | What are the 3 most common CATIA operations designers would want scripted? | Designers | Sprint 1 |
| OQ-3 | Is there an existing CATIA macro library that can serve as few-shot examples in the prompt? | Max | Sprint 1 |
| OQ-4 | What is the acceptable threshold for script correctness before PoC is considered successful? | Stakeholders | Before PoC review |

---

## 12. Glossary

| Term | Definition |
|------|------------|
| CATScript | CATIA's built-in VBA-like macro scripting language |
| EKL | Engineering Knowledge Language — rule/formula scripting in CATIA Knowledge Advisor |
| EHI/EHA | Electrical Harness Installation / Electrical Harness Assembly — CATIA V5 harness routing modules |
| RAG | Retrieval-Augmented Generation — LLM pattern combining vector search with generation |
| KG | Knowledge Graph — graph-based representation of entities and relationships |
| PoC | Proof of Concept |
| Chunk | A segment of a document used as the unit for embedding and retrieval |
| Top-k | The k most similar chunks retrieved from the vector store for a given query |

---

*End of document — v0.2 Draft*

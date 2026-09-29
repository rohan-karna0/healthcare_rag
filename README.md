# Healthcare RAG System

Retrieval-Augmented Generation (RAG) system for answering healthcare-related questions using trusted medical knowledge, semantic search, vector databases, and **open-weight Large Language Models running locally with Ollama**.

This project demonstrates how modern RAG systems are built from scratch using document ingestion, intelligent chunking, embedding models, vector search, retrieval pipelines, and local LLM inference while following a modular and production-ready architecture.

---

## Overview

Traditional Large Language Models generate responses based only on their pre-trained knowledge, which can become outdated or produce hallucinations.

This project enhances an open-weight LLM with external healthcare knowledge. Instead of relying solely on the model's internal parameters, the system retrieves the most relevant medical information from a vector database and injects it into the prompt before generating a response.

```text
Medical Documents → Crawler/Parser → Chunking → Embeddings → Qdrant
                                                                    ↓
User Question → Query Embedding → Hybrid Retrieval → Reranking → Ollama → Grounded Answer
```

---

## Features

- End-to-end Retrieval-Augmented Generation pipeline
- Fully local LLM inference using Ollama
- Medical document ingestion from ADA, WHO, CDC, NIDDK, FDA
- Intelligent document chunking (recursive + semantic strategies)
- Dense vector embeddings (HuggingFace Sentence Transformers)
- **Hybrid retrieval** (dense + BM25 with reciprocal rank fusion)
- **Reranking** with cross-encoder models
- Qdrant vector database (Docker server or local embedded mode)
- Source citations in answers
- Streamlit chat UI and FastAPI REST API
- Evaluation and pytest test suite

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.11+ |
| Framework components | LangChain text splitters and community integrations |
| LLM Runtime | Ollama |
| Default generation model | `qwen2.5:7b` |
| Embedding Model | `sentence-transformers/all-MiniLM-L6-v2` |
| Vector Database | Qdrant |
| Retrieval | Dense + BM25 + Hybrid + Reranking |
| UI | Streamlit |
| API | FastAPI + Uvicorn |
| Config | python-dotenv, pydantic-settings |

---

## Project Structure

```text
healthcare_rag/
├── app.py                  # CLI entry point
├── requirements.txt
├── .env.example
├── config/                 # Settings, sources, prompts (system configuration)
├── data/
│   ├── samples/            # Offline sample medical documents
│   ├── raw/                # Downloaded pages (gitignored)
│   ├── processed/          # Parsed text (gitignored)
│   ├── chunks/             # Chunk store (gitignored)
│   └── qdrant_db/          # Local Qdrant storage (gitignored)
├── ingestion/              # Crawler, downloader, HTML/PDF parsers, metadata
├── processing/             # Cleaning, chunking, embeddings, indexing
├── vectorstore/            # Qdrant client and uploader
├── retrieval/              # Dense, BM25, hybrid retrieval
├── reranking/              # Cross-encoder reranker
├── generation/             # Prompt builder, Ollama generator
├── api/                    # FastAPI routes
├── ui/                     # Streamlit app
├── evaluation/             # Benchmark scripts and evaluation metrics
└── tests/                  # Pytest suite
```

The code is already split by RAG responsibility; this layout keeps those working package paths rather than relocating everything into a second `src/` package. Ingestion loaders live in `ingestion/parser/`, preprocessing in `processing/cleaning/`, chunking in `processing/chunking/`, and the end-to-end CLI is `app.py`. The HTML and PDF parsers are present; recursive chunking uses LangChain's text splitter. The current parsers use BeautifulSoup and pypdf directly, so they do not require a LangChain loader-specific API.

### Current data coverage

`data/samples/` contains only two short diabetes text documents (about 2.6 KB total). They are useful for smoke tests, not for reliable or broad healthcare answers. Run ingestion to crawl the configured CDC, WHO, ADA, NIDDK, and FDA sources; the crawler uses `httpx` and respects robots.txt, with no Firecrawl service or API key. Crawling requires internet access, and sites may block or limit automated requests. Verify the documents and chunks created before treating the index as sufficient for your use case.

---

## Prerequisites

Before running the project, install:

1. **Python 3.11+** — [python.org](https://www.python.org/downloads/)
2. **Git** — [git-scm.com](https://git-scm.com/)
3. **Ollama** — [ollama.com](https://ollama.com) (for answer generation)
4. **Docker** (optional) — for Qdrant server; local embedded mode works without it

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/rohan-karna0/healthcare_rag.git
cd healthcare_rag
```

> **Important:** If you cloned into a parent folder and see a nested `healthcare_rag/healthcare_rag/` directory, always run commands from the **inner** folder that contains `app.py` and `.git`.

### 2. Create a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure environment variables

```powershell
copy .env.example .env
```

Edit `.env` if needed. Key settings:

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_MODEL` | `qwen2.5:7b` | Ollama model name |
| `QDRANT_URL` | `http://localhost:6333` | Qdrant server URL |
| `QDRANT_LOCAL_PATH` | `data/qdrant_db` | Fallback local storage |
| `RETRIEVAL_MODE` | `hybrid` | `hybrid`, `dense`, or `bm25` |
| `USE_RERANKER` | `true` | Set `false` for faster CPU dev |
| `TOP_K` | `5` | Number of chunks to retrieve |

### 4. Install and pull Qwen with Ollama

```bash
ollama pull qwen2.5:7b
```

Make sure Ollama is running before querying or using the UI. This local Ollama setup does not require a model-provider API key. For a smaller machine, use a smaller Qwen tag supported by Ollama and set `OLLAMA_MODEL` in `.env` to the exact tag you pulled.

### 5. Qdrant (optional)

**Option A — Docker (recommended for production):**

```powershell
docker run -p 6333:6333 qdrant/qdrant
```

**Option B — No Docker:** The app automatically falls back to local Qdrant storage at `data/qdrant_db/`.

---

## How to Run

All commands below assume you are in the project root (where `app.py` lives) with your virtual environment activated.

### Step 1 — Ingest documents

Crawl medical sources, parse content, chunk text, and index into Qdrant:

```powershell
python app.py ingest --sources CDC,WHO
```

Available sources: `ADA`, `WHO`, `CDC`, `NIDDK`, `FDA`

- Omit `--sources` to crawl all configured sources
- Add `--no-index` to ingest without indexing
- If crawling fails or is blocked, the pipeline falls back to bundled sample docs in `data/samples/`

### Step 2 — Index chunks (if ingested with `--no-index`)

```powershell
python app.py index
```

Re-index from scratch:

```powershell
python app.py index --reset
```

### Step 3 — Ask a question (CLI)

```powershell
python app.py query "What is type 2 diabetes?"
```

With options:

```powershell
python app.py query "What are symptoms of diabetes?" --mode hybrid --top-k 5 --sources CDC,WHO
```

### Step 4 — Launch Streamlit UI

```powershell
python app.py serve-ui
```

Open the URL shown in the terminal (usually `http://localhost:8501`).

In the sidebar you can:
- Select Ollama model and retrieval mode
- Filter by medical source
- Run **Ingest & Index** or **Re-index** from the UI
- Chat with source citations

### Step 5 — Launch FastAPI server

```powershell
python app.py serve-api
```

API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

**Example API request:**

```powershell
curl -X POST http://localhost:8000/query ^
  -H "Content-Type: application/json" ^
  -d "{\"question\": \"What is type 2 diabetes?\", \"top_k\": 5, \"mode\": \"hybrid\"}"
```

**Endpoints:**

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Check Ollama and index status |
| `POST` | `/query` | Ask a healthcare question |
| `POST` | `/ingest` | Trigger ingestion pipeline |

---

## CLI Reference

```text
python app.py ingest [--sources CDC,WHO] [--no-index]
python app.py index [--reset]
python app.py query "Your question" [--mode hybrid|dense|bm25] [--top-k 5] [--sources CDC] [--model llama3.2]
python app.py serve-ui
python app.py serve-api [--host 0.0.0.0] [--port 8000]
```

---

## Run Tests

```powershell
$env:USE_RERANKER="false"
pytest
```

---

## Run Evaluation Benchmark

```powershell
python -m evaluation.benchmark
```

Report is saved to `logs/benchmark_report.json`.

---

## Supported Ollama Models

Any Ollama-compatible model works. Examples:

- Llama 3 / 3.1 / 3.2
- Mistral
- Gemma 2
- Qwen 2.5
- Phi 3

Change the model in `.env` (`OLLAMA_MODEL`) or pass `--model` to the query command.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `Ollama is not available` | Start Ollama app and run `ollama pull llama3.2` |
| Qdrant connection refused | Use Docker Qdrant or rely on local fallback at `data/qdrant_db/` |
| Slow first run | Embedding model downloads on first use; set `USE_RERANKER=false` |
| Crawl returns few pages | Use `data/samples/` or lower `MAX_CRAWL_PAGES` in `.env` |
| Git push shows only submodule | Run git commands from the inner `healthcare_rag/` folder with `app.py` |

---

## Push to GitHub

From the project root (inner repo with `app.py`):

```powershell
git status
git add .
git commit -m "Your commit message"
git push origin main
```

Use a GitHub Personal Access Token when prompted for a password over HTTPS.

---

## Example Workflow

```text
User Question
       │
       ▼
Generate Query Embedding
       │
       ▼
Hybrid Search (Dense + BM25) → Reranking
       │
       ▼
Retrieve Top-k Chunks (Qdrant)
       │
       ▼
Prompt Construction + Citations
       │
       ▼
Ollama (Local LLM)
       │
       ▼
Grounded Healthcare Response
```

---

## Author

**Rohan Karna**

M.Tech – Data & Computational Sciences

Indian Institute of Technology Jodhpur

Passionate about building production-ready AI systems, Retrieval-Augmented Generation (RAG) applications, Large Language Model (LLM) pipelines, and scalable Generative AI solutions using open-weight models.

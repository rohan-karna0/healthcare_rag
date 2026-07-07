# Healthcare RAG System

Production-ready Retrieval-Augmented Generation (RAG) system for answering healthcare-related questions using trusted medical knowledge, semantic search, vector databases, and **open-weight Large Language Models running locally with Ollama**.

This project demonstrates how modern RAG systems are built from scratch using document ingestion, intelligent chunking, embedding models, vector search, retrieval pipelines, and local LLM inference while following a modular and production-ready architecture.

---

# Overview

Traditional Large Language Models generate responses based only on their pre-trained knowledge, which can become outdated or produce hallucinations.

This project enhances an open-weight LLM with external healthcare knowledge. Instead of relying solely on the model's internal parameters, the system retrieves the most relevant medical information from a vector database and injects it into the prompt before generating a response.

This Retrieval-Augmented Generation (RAG) approach produces more accurate, explainable, and context-aware answers.

The pipeline consists of:

```text
Medical Documents
        │
        ▼
Document Loader
        │
        ▼
Text Splitter
        │
        ▼
Embedding Model
        │
        ▼
Vector Database
        │
        ▼
Retriever
        │
        ▼
Relevant Context
        │
        ▼
Open-Weight LLM
(Ollama)
        │
        ▼
Grounded Response
```

---

# Features

* End-to-end Retrieval-Augmented Generation pipeline
* Fully local LLM inference using Ollama
* Supports multiple open-weight LLMs
* Medical document ingestion pipeline
* Intelligent document chunking
* Dense vector embeddings
* Semantic similarity search
* Pinecone vector database integration
* Context-aware prompt engineering
* Grounded response generation
* Modular and scalable architecture
* Easily extendable to production

---

# Tech Stack

| Component                    | Technology                                                                    |
| ---------------------------- | ----------------------------------------------------------------------------- |
| Programming Language         | Python 3.11                                                                   |
| Framework                    | LangChain                                                                     |
| LLM Runtime                  | Ollama                                                                        |
| Supported Open-Weight Models | Llama 3, Llama 3.1, Llama 3.2, Mistral, Gemma 2, Qwen 2.5, Phi 3, DeepSeek-R1 |
| Embedding Model              | HuggingFace Sentence Transformers                                             |
| Vector Database              | Pinecone                                                                      |
| Interface                    | Streamlit                                                                     |
| Environment                  | Conda                                                                         |
| Configuration                | python-dotenv                                                                 |

---

# Project Structure

```text
## Project Structure

```text
healthcare-rag/
│
├── README.md
├── requirements.txt
├── .env
├── .gitignore
├── app.py
│
├── config/
│   ├── settings.py
│   ├── sources.py
│   └── prompts.py
│
├── data/
│   ├── raw/
│   │   ├── ADA/
│   │   ├── WHO/
│   │   ├── CDC/
│   │   ├── NIDDK/
│   │   └── FDA/
│   │
│   ├── processed/
│   ├── chunks/
│   └── embeddings/
│
├── metadata/
│   ├── documents.json
│   ├── crawl_log.json
│   └── download_log.json
│
├── logs/
│
├── ingestion/
│   ├── crawler/
│   │   ├── crawler.py
│   │   ├── queue.py
│   │   ├── task.py
│   │   ├── filters.py
│   │   ├── robots.py
│   │   └── sitemap.py
│   │
│   ├── downloader/
│   │   ├── downloader.py
│   │   ├── validator.py
│   │   └── retry.py
│   │
│   ├── parser/
│   │   ├── pdf_parser.py
│   │   ├── html_parser.py
│   │   ├── table_parser.py
│   │   └── parser_factory.py
│   │
│   ├── metadata/
│   │   ├── metadata.py
│   │   ├── hashing.py
│   │   └── repository.py
│   │
│   ├── utils/
│   │   ├── logger.py
│   │   ├── helpers.py
│   │   └── exceptions.py
│   │
│   └── ingest.py
│
├── processing/
│   ├── cleaning/
│   │   ├── text_cleaner.py
│   │   └── html_cleaner.py
│   │
│   ├── chunking/
│   │   ├── recursive_chunker.py
│   │   ├── semantic_chunker.py
│   │   ├── contextual_chunker.py
│   │   └── chunk_manager.py
│   │
│   ├── embeddings/
│   │   ├── embedder.py
│   │   ├── embedding_cache.py
│   │   └── models.py
│   │
│   └── indexing/
│       └── index_pipeline.py
│
├── vectorstore/
│   ├── qdrant_client.py
│   ├── collections.py
│   └── uploader.py
│
├── retrieval/
│   ├── dense.py
│   ├── bm25.py
│   ├── hybrid.py
│   ├── query_expansion.py
│   ├── metadata_filter.py
│   └── retriever.py
│
├── reranking/
│   ├── bge_reranker.py
│   └── cross_encoder.py
│
├── generation/
│   ├── prompt_builder.py
│   ├── generator.py
│   ├── citations.py
│   └── answer_formatter.py
│
├── evaluation/
│   ├── ragas_eval.py
│   ├── retrieval_eval.py
│   ├── generation_eval.py
│   └── benchmark.py
│
├── api/
│   ├── app.py
│   ├── routes.py
│   └── schemas.py
│
├── ui/
│   └── streamlit_app.py
│
├── notebooks/
│
└── tests/
    ├── test_ingestion.py
    ├── test_chunking.py
    ├── test_retrieval.py
    └── test_generation.py
```

```

---

# Supported Open-Weight Models

The application is model-agnostic and works with any Ollama-compatible open-weight model.

Examples include:

* Llama 3
* Llama 3.1
* Llama 3.2
* Mistral
* Gemma 2
* Qwen 2.5
* Phi 3
* DeepSeek-R1
* DeepSeek-R1 Distill Llama
* DeepSeek-R1 Distill Qwen
* TinyLlama
* CodeLlama

Switching models only requires changing the model name in the Ollama configuration. No changes to the RAG pipeline are required.

---

# How It Works

### 1. Document Loading

Healthcare documents are loaded from the knowledge base.

---

### 2. Text Chunking

Large documents are divided into smaller overlapping chunks to preserve semantic context and improve retrieval quality.

---

### 3. Embedding Generation

Each document chunk is converted into a dense vector using HuggingFace Sentence Transformer embedding models.

---

### 4. Vector Storage

The generated embeddings are stored inside Pinecone for efficient semantic retrieval.

---

### 5. Semantic Retrieval

When a user submits a question, the query is embedded and compared against stored document embeddings to retrieve the most relevant chunks.

---

### 6. Context Injection

The retrieved context is combined with the user query using a prompt template.

---

### 7. Response Generation

The prompt is sent to an open-weight LLM running locally through Ollama, which generates a grounded response using the retrieved healthcare knowledge instead of relying solely on its pre-trained parameters.

---

# Installation

Clone the repository

```bash
git clone https://github.com/your-username/healthcare-rag.git
```

Move into the project directory

```bash
cd healthcare-rag
```

Create a virtual environment

```bash
conda create -n healthcare-rag python=3.11
conda activate healthcare-rag
```

Install dependencies

```bash
pip install -r requirements.txt
```

Install Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Pull your preferred open-weight model

```bash
ollama pull llama3.2
```

or

```bash
ollama pull mistral
```

or

```bash
ollama pull qwen2.5
```

Create a `.env` file

```env
PINECONE_API_KEY=YOUR_API_KEY
```

Run the application

```bash
python app.py
```

---

# Example Workflow

```text
User Question
       │
       ▼
Generate Query Embedding
       │
       ▼
Semantic Search
(Pinecone)
       │
       ▼
Retrieve Top-k Chunks
       │
       ▼
Prompt Construction
       │
       ▼
Ollama
(Open-Weight LLM)
       │
       ▼
Grounded Healthcare Response
```

---

# Future Improvements

* Hybrid Search (Dense + BM25)
* Metadata Filtering
* Parent-Child Retrieval
* Query Rewriting
* Context Compression
* Re-ranking Models
* Source Attribution
* Conversational Memory
* Evaluation Framework
* Hallucination Detection
* Multi-modal RAG
* Agentic RAG
* Docker Deployment
* Kubernetes Deployment
* CI/CD Pipeline
* Monitoring and Observability

---

# Learning Outcomes

This project demonstrates practical understanding of:

* Retrieval-Augmented Generation (RAG)
* Vector Databases
* Semantic Search
* Text Chunking Strategies
* Embedding Models
* Dense Retrieval
* Prompt Engineering
* Context Injection
* Open-Weight LLM Integration
* Local LLM Inference using Ollama
* LangChain Pipelines
* Production-Ready AI System Design

---

# Author

**Rohan Karna**

**M.Tech – Data & Computational Sciences**

**Indian Institute of Technology Jodhpur**

Passionate about building production-ready AI systems, Retrieval-Augmented Generation (RAG) applications, Large Language Model (LLM) pipelines, and scalable Generative AI solutions using open-weight models.

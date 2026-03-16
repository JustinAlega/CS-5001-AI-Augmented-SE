# Mid-Semester Project: Single Agent RAG

A unified single-agent Document RAG (Retrieval-Augmented Generation) pipeline using **LangChain** and **Ollama**.

This project provides an interactive chat interface that lets you ask questions about documents scattered within the `docs/` directory.

---

## Directory layout

```text
Mid-Semester-Proj/
  single_agent_rag.py     # Main RAG script (Indexing & Interactive Chat)
  requirements.txt        # Python dependencies
  docs/                   # Drop your .txt and .md files here
    rag_architecture.md   # Example document
```

---

## Prerequisites

### 1) Python environment

Requires Python 3.12 (or similar).

Create and activate a virtual environment:

```bash
python -m venv .venv

# On Linux/macOS:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 2) Ollama

Ensure Ollama is installed and running:

```bash
ollama serve
```

Pull the required language model and embeddings model (default sizes are large; consider smaller ones depending on your machine):

```bash
ollama pull devstral-small-2:24b-cloud  # Default Chat LLM
ollama pull nomic-embed-text            # Default Embeddings Model
```

_Note: If you have hardware limits or want to use a smaller model, you can specify environment variables when running (e.g., `OLLAMA_MODEL=llama3.2`)._

---

## Usage

### 1. Add Documents
Place any Markdown (`.md`) or text (`.txt`) documents into the `docs/` directory. Subfolders are also supported. The RAG system will recursively search and index these files.

### 2. Run the Single Agent RAG 
Start the application from the root directory:

```bash
python single_agent_rag.py
```

The script performs two major actions consecutively:
1. **Indexing**: Scans `docs/`, breaks text into chunks, computes embeddings, and builds a FAISS index (saving it to `rag_index/`). 
2. **Interactive Chat**: Opens a CLI chat loop. When you ask a question, the agent retrieves the top 5 most relevant document chunks and synthesizes an answer.

Example Queries:
* _"What is the system described in the sample document?"_
* _"Which embeddings model is used for the RAG?"_

### Custom Models

You can customize the underlying LLMs by passing standard environment variables:

```bash
# Example using Llama 3.2 instead of the default
OLLAMA_MODEL=llama3.2 python single_agent_rag.py
```

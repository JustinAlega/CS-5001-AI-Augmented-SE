# Single-Agent RAG Architecture

This document outlines the design and components of the Single-Agent RAG (Retrieval-Augmented Generation) system implemented in our mid-semester project.

## Overview

Retrieval-Augmented Generation (RAG) is a technique that enhances large language models (LLMs) by grounding their generation in an external knowledge base. This allows the AI to provide specific, accurate answers based on our own data, rather than relying solely on its pre-trained knowledge. In this project, the knowledge base is composed of local documents placed in the `docs/` directory.

## Core Components

The architecture consists of three main phases: Ingestion, Retrieval, and Generation.

### 1. Document Ingestion
- **Document Loader**: The system sequentially scans the `docs/` directory for raw text and markdown files.
- **Text Splitter**: Because Language Models have finite context windows, the documents are split into manageable chunks using a `RecursiveCharacterTextSplitter`. We use overlapping segments to ensure minimal context is lost at the boundaries.
- **Embeddings**: Each text chunk is translated into a dense, high-dimensional vector. We utilize the `nomic-embed-text` model driven by Ollama.
- **Vector Store**: The numeric vectors are indexed using FAISS (Facebook AI Similarity Search) and temporarily saved to disk. This allows for lightning-fast comparisons.

### 2. Retrieval
When a user inputs a query, the query itself is immediately converted into a vector using the exact same embedding model. The FAISS database then performs a similarity search to find the nearest vector neighbors. The top 5 matching text chunks are pulled as our core context.

### 3. Generation
Finally, the retrieved chunks and the user's question are inserted into a strict system prompt. The prompt instructs the Chat LLM (the default is `devstral-small-2:24b-cloud` via Ollama) to only use the provided context when formulating a response. The LLM processes the facts, synthesizes a cohesive answer, and replies to the user.

## Key Technologies
- **Python 3.12**: Core runtime logic.
- **LangChain**: The underlying framework connecting the prompts, vector database, and the LLMs.
- **Ollama**: A lightweight local orchestrator that runs the embedding and chat models independently of the cloud.
- **FAISS**: The vector space search library functioning as the active index.

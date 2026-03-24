#!/usr/bin/env python3

#Single Agent RAG System


from __future__ import annotations

import os
from pathlib import Path
from typing import List, Tuple

from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


# config

DOCS_DIR = Path("docs").resolve()
INDEX_DIR = Path("rag_index").resolve()

LLM_MODEL = os.environ.get("OLLAMA_MODEL", "devstral-small-2:24b-cloud")
LLM_TEMP = float(os.environ.get("OLLAMA_TEMPERATURE", "0.0"))
EMBED_MODEL = os.environ.get("OLLAMA_EMBED_MODEL", "nomic-embed-text")

SYSTEM_RULES = """You are an intelligent document assistant. 

Use the retrieved context to answer the user's question accurately. 
If the answer is not contained within the context, simply state "I don't know based on the provided documents".
"""


# utils
def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def load_docs(docs_dir: Path) -> List[Document]:
    docs: List[Document] = []
    if not docs_dir.exists():
        return docs

    for ext in ("*.txt", "*.md"):
        for path in sorted(docs_dir.glob(f"**/{ext}")):
            docs.append(Document(page_content=read_text(path), metadata={"source": str(path)}))
    return docs


def format_docs(docs: List[Document]) -> str:
    parts: List[str] = []
    for i, d in enumerate(docs, start=1):
        src = d.metadata.get("source", "unknown")
        text = d.page_content.strip()
        parts.append(f"[{i}] source={src}\n{text}")
    return "\n\n".join(parts)


# index
def build_index() -> FAISS | None:
    print(f"Loading documents from {DOCS_DIR} ...")
    docs = load_docs(DOCS_DIR)
    
    if not docs:
        print(f"No documents found in {DOCS_DIR}. Please add some .txt or .md files.")
        return None

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        separators=["\n\n", "\n", " ", ""],
    )
    chunks = splitter.split_documents(docs)
    print(f"Created {len(chunks)} document chunks.")

    print(f"Initializing embeddings ({EMBED_MODEL})...")
    embeddings = OllamaEmbeddings(model=EMBED_MODEL)

    print("Building FAISS index...")
    vectordb = FAISS.from_documents(chunks, embeddings)
    
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    vectordb.save_local(str(INDEX_DIR))
    print(f"FAISS index saved to {INDEX_DIR}\n")
    return vectordb


# chat
def chat_loop(vectordb: FAISS) -> None:
    print(f"Initializing Chat LLM ({LLM_MODEL})...")
    llm = ChatOllama(model=LLM_MODEL, temperature=LLM_TEMP)
    
    chat_history: List[Tuple[str, str]] = []

    print("\n--- Start Chatting (type 'exit' or 'quit' to stop) ---")
    while True:
        try:
            user_q = input("\nYou: ").strip()
        except (KeyboardInterrupt, EOFError):
            break
            
        if user_q.lower() in {"exit", "quit"}:
            break
        if not user_q:
            continue

        docs = vectordb.similarity_search(user_q, k=5)
        context = format_docs(docs)

        history_text = ""
        if chat_history:
            last = chat_history[-6:]
            history_text = "\n".join([f"User: {u}\nAssistant: {a}" for (u, a) in last])

        prompt = f"""{SYSTEM_RULES}

Recent chat (may be incomplete):
{history_text}

Retrieved context:
{context}

User question:
{user_q}
"""
        try:
            resp = llm.invoke(prompt)
            answer = resp.content if isinstance(resp.content, str) else str(resp.content)
            print(f"\nAI: {answer}")
            chat_history.append((user_q, answer))
        except Exception as e:
            print(f"\nError communicating with LLM: {e}")


def main() -> None:
    vectordb = build_index()
    if vectordb:
        chat_loop(vectordb)


if __name__ == "__main__":
    main()

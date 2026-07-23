# Aircraft Electrical & Electronics RAG Assistant

A local, offline AI assistant that answers questions about aircraft electrical and electronics systems using Retrieval-Augmented Generation (RAG) and Microsoft Foundry Local.

## What It Does

This assistant answers questions based on a small knowledge base of aircraft electrical and avionics topics. It runs entirely offline on your computer — no internet connection or cloud API required.

## How It Works

1. **Retrieve**: When you ask a question, the system converts it into an embedding (numeric vector) and searches a local SQLite database for the most relevant document chunks using cosine similarity.
2. **Augment**: The retrieved chunks are inserted into the prompt as context.
3. **Generate**: A local LLM (via Foundry Local) generates an answer based only on the provided context.

## System Architecture

Question
    ↓
Embedding Model (qwen3-embedding-0.6b)
    ↓
Cosine Similarity Search
    ↓
SQLite Database (16 chunks from 8 documents)
    ↓
Top-K Relevant Chunks
    ↓
Chat Model (qwen3-0.6b) + Context
    ↓
Answer

## Technologies Used

- **Microsoft Foundry Local** — on-device LLM runtime
- **qwen3-0.6b** — chat model for generating answers
- **qwen3-embedding-0.6b** — embedding model for semantic search
- **SQLite** — local storage for document chunks and embeddings
- **Streamlit** — web-based user interface
- **Python** — core language

## Project Structure

week1/ - Foundry Local setup and basic model tests
week2/ - Cosine similarity, embedding storage, prompt engineering
week3/ - Document chunking, ingestion pipeline, search function
week4/ - Full RAG pipeline and interactive assistant
week5/ - Testing and evaluation
documents/ - Knowledge base source files (aircraft electrical/electronics topics)
app.py - Streamlit web interface
screenshots/ - Web interface screenshot

## Knowledge Base Topics

1. Aircraft Electrical Systems
2. Avionics Systems
3. Flight Control Systems
4. Aircraft Sensors and Instruments
5. Power Distribution Systems
6. Aircraft Communication Systems
7. Engine Monitoring Systems
8. Lightning Protection and EMI Shielding
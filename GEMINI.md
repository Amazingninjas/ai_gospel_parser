# Gemini Project Context: AI Gospel Parser

## Project Overview

This project is a Python-based AI research assistant for theological studies. It uses ancient Greek biblical texts (Septuagint and Greek New Testament) and Thayer's Greek Lexicon to answer user questions.

The core architecture is a Retrieval-Augmented Generation (RAG) system:
1.  **Data Ingestion:** The main script, `gospel_parser.py`, parses the source texts (LXX, GNT, and the lexicon) into sentence-level chunks.
2.  **Vector Storage:** These chunks are stored in a local ChromaDB vector database. This process is called "seeding" and only needs to be done once.
3.  **Querying:** When a user asks a question, the script queries ChromaDB to find the most relevant text passages.
4.  **Generation:** The retrieved passages are passed as context to a local Large Language Model (LLM) hosted by Ollama, which generates a grounded answer.

## Building and Running

This is a Python script-based project with no formal build process. The primary dependencies are Python libraries.

### 1. Install Dependencies

First, install the required Python packages:
```bash
pip install chromadb ollama sentence-transformers
```

### 2. Set up Ollama (Multi-GPU)

This project is designed to run with a local LLM via Ollama. To use a multi-GPU setup (e.g., a 2070 Super and a 1660 Super), you must configure Ollama before running the script.

1.  **Identify GPU Order:**
    ```bash
    nvidia-smi
    ```
2.  **Set Environment Variable:** In your terminal, set `CUDA_VISIBLE_DEVICES` to the desired GPU order (e.g., primary GPU first).
    ```bash
    export CUDA_VISIBLE_DEVICES=0,1
    ```
3.  **Run Ollama:** Start the Ollama server in that terminal.
    ```bash
    ollama serve
    ```
4.  **Pull Model:** In a new terminal, pull the model specified in the script (default is `mixtral`).
    ```bash
    ollama pull mixtral
    ```

### 3. Run the Application

Execute the main Python script:
```bash
python gospel_parser.py
```
*   **First Run:** The script will automatically "seed" the database by parsing all source texts and creating vector embeddings. This is a one-time process and may take several minutes.
*   **Subsequent Runs:** The script will detect the existing database and immediately start the interactive query prompt.

## Development Conventions

*   **Configuration:** Key settings like file paths and model names are stored as global constants at the top of `gospel_parser.py`.
*   **Data Sources:** The application expects the source text data to be in specific directories:
    *   Septuagint (LXX): `LXX-Swete/src/First1KGreek-LXX-RAW/`
    *   Greek New Testament (GNT): `sblgnt/`
    *   Thayer's Lexicon: `strongsgreek.xml` in the root directory.
*   **Modularity:** The script is organized into distinct sections for database seeding and the query engine. Parsing logic is separated into functions for each data type.
*   **Error Handling:** The script includes basic checks for the existence of data files and provides informative error messages.

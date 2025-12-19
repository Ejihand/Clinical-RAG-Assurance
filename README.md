```markdown
# Clinical RAG Assurance

A Retrieval-Augmented Generation (RAG) system designed to process and query clinical guidelines with high accuracy and citation assurance. This project focuses on ingesting complex medical PDFs (specifically WHO Malaria Guidelines) and allowing users to query them using GPT-4, retrieving the exact source text for verification.

## Project Structure

* `data/`: Storage for raw PDFs, processed JSON chunks, and the Vector Database.
    * **Source Data:** [WHO Guidelines for Malaria (PDF)](https://iris.who.int/bitstream/handle/10665/379635/B09146-eng.pdf)
* `src/`:
    * `ingest/`: Pipelines for data processing.
        * `pdf_parser.py`: Extracts raw text from PDFs.
        * `chunker.py`: Splits text into semantic chunks using LangChain.
        * `embedder.py`: Generates OpenAI embeddings and stores them in ChromaDB.
    * `retrieval/`:
        * `retrieve.py`: Logic to search the vector database.
    * `rag.py`: **Main Logic.** Combines retrieval with GPT-4 to generate answers.
    * `app.py`: **Web Interface.** Streamlit-based chat application.

## Setup & Configuration

1.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Environment Setup**
    Create a `.env` file in the root directory and add your OpenAI API key:
    ```bash
    OPENAI_API_KEY=sk-proj-your-key-here
    ```

## Usage Pipeline

To run the system from scratch, follow these steps in order:

**Step 1: Parse & Chunk**
Extract text and split it into searchable chunks (saved to `data/chunks.json`).
```bash
python -m src.ingest.chunker
```

**Step 2: Embed & Store**
Generate vector embeddings and save them to ChromaDB (`data/chroma_db`).

```bash
python -m src.ingest.embedder
```

**Step 3: Run the RAG System (CLI)**
Ask a question to the full pipeline via the terminal.

```bash
python -m src.rag "What is the recommended dosage for artesunate?"
```

**Step 4: Launch Web UI**
Start the interactive chat interface in your browser.

```bash
streamlit run src/app.py
```

## Project Status

* [x] **Phase 1: Ingestion**
    *  [x] PDF Parsing & Text Cleaning
    * [x] Recursive Text Chunking (LangChain)


* [x] **Phase 2: Embedding & Storage**
    * [x] Vector Database Setup (ChromaDB)
    * [x] Embedding Generation (OpenAI text-embedding-3-small)


* [x] **Phase 3: Retrieval & Generation**
    * [x] Context Retrieval
    * [x] LLM Integration (GPT-4o)
    * [x] RAG Response Generation


* [x] **Phase 4: User Interface**
    * [x] Streamlit Chat App



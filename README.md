# **Clinical RAG Assurance**

A **Retrieval-Augmented Generation (RAG)** system designed to process and
query clinical guidelines with high accuracy and citation assurance.
This project focuses on ingesting complex medical PDFs (specifically
WHO Malaria Guidelines) and allowing users to query them using **GPT-4o**,
retrieving the exact source text for verification.

To ensure clinical reliability, this system incorporates an **Automated
Evaluation Pipeline** using **Ragas** to measure Faithfulness, Answer
Relevance, and Context Precision.

---

## 📅 Project Status

* [x] **Phase 1: Ingestion**
    * [x] PDF Parsing & Text Cleaning
    * [x] Recursive Text Chunking (LangChain)
* [x] **Phase 2: Embedding & Storage**
    * [x] Vector Database Setup (ChromaDB)
    * [x] Embedding Generation (OpenAI text-embedding-3-small)
* [x] **Phase 3: Retrieval & Generation**
    * [x] Context Retrieval logic
    * [x] LLM Integration (GPT-4o)
    * [x] RAG Response Generation
* [x] **Phase 4: User Interface**
    * [x] Streamlit Chat App
* [ ] **Phase 5: Evaluation & Assurance (Current Focus)**
    * [ ] Synthetic Test Set Generation
    * [ ] Ragas Metrics Calculation (Faithfulness, Precision)
---
## 📂 Project Structure

* `data/`: Storage for raw PDFs, chunks, and Vector DB.
    * **Source Data:** [WHO Guidelines for Malaria (PDF)][1]
* `src/`:
    * `ingest/`: Pipelines for data processing.
        * `pdf_parser.py`: Extracts raw text from PDFs.
        * `chunker.py`: Splits text into semantic chunks.
        * `embedder.py`: Generates embeddings -> ChromaDB.
    * `retrieval/`:
        * `retrieve.py`: Logic to search the vector database.
    * `evaluation/`: **(New)**
        * `evaluate.py`: Runs Ragas metrics to score accuracy.
    * `rag.py`: **Main Logic.** Combines retrieval + GPT-4.
    * `app.py`: **Web Interface.** Streamlit-based chat app.
---
## ⚙️ Setup & Configuration

**1. Install Dependencies**
```bash
pip install -r requirements.txt

```
**2. Environment Setup**
Create a `.env` file in the root directory and add your key:

```bash
OPENAI_API_KEY=sk-proj-your-key-here

```
## 🚀 Usage Pipeline

Run these steps in order:

### **Step 1: Parse & Chunk**

Extract text and split it into searchable chunks.

```bash
python -m src.ingest.chunker

```
### **Step 2: Embed & Store**

Generate vector embeddings and save to ChromaDB.

```bash
python -m src.ingest.embedder

```
### **Step 3: Run the RAG System (CLI)**

Test the pipeline via the terminal.

```bash
python -m src.rag "What is the dosage for artesunate?"

```
### **Step 4: Launch Web UI**

Start the interactive chat interface.

```bash
streamlit run src/app.py

```
### **Step 5: Run Clinical Evaluation**

Generate trust scores (Faithfulness, Relevance).

```bash
python -m src.evaluation.evaluate

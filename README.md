```markdown
# **Clinical RAG Assurance**

A **Retrieval-Augmented Generation (RAG)** system designed to process and query clinical guidelines with high accuracy and citation assurance. This project focuses on ingesting complex medical PDFs (specifically **WHO Malaria Guidelines**) and allowing users to query them using **GPT-4o**, retrieving the exact source text for verification.

To ensure clinical reliability, this system incorporates an **Automated Evaluation Pipeline** using **Ragas** to measure Faithfulness, Answer Relevance, and Context Precision.
---
## 📅 Project Status

* [x] **Phase 1: Ingestion**
    * [x] PDF Parsing & Text Cleaning (PyMuPDF)
    * [x] Recursive Text Chunking (LangChain)
* [x] **Phase 2: Embedding & Storage**
    * [x] Vector Database Setup (ChromaDB)
    * [x] Embedding Generation (OpenAI text-embedding-3-small)
* [x] **Phase 3: Retrieval & Generation**
    * [x] Context Retrieval Logic
    * [x] LLM Integration (GPT-4o)
    * [x] Strict Clinical Guardrails (Prompt Engineering)
* [x] **Phase 4: User Interface**
    * [x] Streamlit Chat App
* [x] **Phase 5: Evaluation & Assurance**
    * [x] Synthetic Test Set Generation
    * [x] Ragas Metrics Calculation (Faithfulness, Precision)
    * [x] **Result:** Achieved 100% Faithfulness Score
---
## 📂 Project Structure

* `data/`
    * `raw_pdfs/`: Input storage (Place your PDF here).
    * `processed/`: Intermediate JSON chunks.
    * `vector_store/`: ChromaDB database files.
    * `evaluation_results.csv`: Ragas grading report.
* `src/`
    * `ingest/`: Pipelines for data processing.
        * `pdf_parser.py`: Extracts raw text from PDFs.
        * `chunker.py`: Splits text into semantic chunks.
        * `embedder.py`: Generates embeddings -> ChromaDB.
    * `evaluation/`: **(Automated Assurance)**
        * `generate_testset.py`: Uses GPT-4 to create a synthetic clinical exam.
        * `evaluate.py`: Runs Ragas metrics to score the AI's answers.
    * `rag.py`: **Core Logic.** Combines retrieval + GPT-4o.
    * `app.py`: **Web Interface.** Streamlit-based chat app.
---
## ⚙️ Setup & Configuration

**1. Install Dependencies**
```bash
pip install -r requirements.txt

```
**2. Environment Setup**
Create a `.env` file in the root directory:

```bash
OPENAI_API_KEY=sk-proj-your-key-here

```
## 🚀 Usage Pipeline

Run these steps in order to build, test, and deploy the system.

### **Step 1: Ingest Data**

Place your PDF in `data/raw_pdfs/`, then parse and chunk it.

```bash
python -m src.ingest.chunker

```
### **Step 2: Embed & Store**

Generate vector embeddings and save to ChromaDB.

```bash
python -m src.ingest.embedder

```
### **Step 3: Generate Synthetic Exam**

Use GPT-4 to read the PDF and generate 10 hard clinical questions.

```bash
python -m src.evaluation.generate_testset

```
### **Step 4: Run Clinical Evaluation**

Grade the system on Faithfulness and Relevance.

```bash
python -m src.evaluation.evaluate

```
### **Step 5: Launch Web UI**

Start the interactive chat interface.

```bash
streamlit run src/app.py
```
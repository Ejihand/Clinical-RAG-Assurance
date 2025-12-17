# Clinical RAG Assurance

A Retrieval-Augmented Generation (RAG) system designed to process and query clinical guidelines with high accuracy and citation assurance. This project focuses on ingesting complex medical PDFs and allowing users to query them using an LLM while retrieving the exact source text.

## Project Structure

* `data/`: Contains raw PDF clinical guidelines.
    * **Source Data:** [WHO Guidelines for Malaria - 3 June 2024 (PDF)](https://iris.who.int/bitstream/handle/10665/379635/B09146-eng.pdf)
* `src/ingest/`: Scripts for parsing PDFs and chunking text.
    * `pdf_parser.py`: Extracts and cleans text from the raw PDF.

## Setup & Usage

1.  **Install Dependencies**
    Ensure you have your virtual environment active, then run:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the PDF Parser**
    Run the parser from the root directory to extract text from the guidelines:
    ```bash
    python src/ingest/pdf_parser.py
    ```
    *Expected Output:* The script will parse `data/guidelines.pdf`, display a sample of the cleaned text, and print the total word count.

## Project Status

* [x] **Phase 1: Ingestion**
    * [x] Environment Setup & Dependencies
    * [x] PDF Parsing & Text Cleaning (Header/Footer removal)
    * [ ] Text Chunking (Recursive Character Splitter)
* [ ] **Phase 2: Embedding & Storage**
    * [ ] Vector Database Setup (ChromaDB/FAISS)
    * [ ] Embedding Generation
* [ ] **Phase 3: Retrieval & Generation**
    * [ ] LLM Integration
    * [ ] RAG Pipeline Construction
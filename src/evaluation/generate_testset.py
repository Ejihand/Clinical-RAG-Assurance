import os
import sys
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv

# -----------------------------------------------------------------------------
# PATH SETUP
# -----------------------------------------------------------------------------
CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

# Load Env
load_dotenv(PROJECT_ROOT / ".env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY not found in .env file!")

# Ragas Imports (Compatible with v0.1.21)
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from ragas.testset.generator import TestsetGenerator
from ragas.testset.evolutions import simple, reasoning, multi_context

def generate_clinical_testset(test_size=10):
    """
    Generates a synthetic test set (Questions + Ground Truths) from your PDFs.
    """
    # 1. Setup Paths
    raw_pdf_dir = PROJECT_ROOT / "data" / "raw_pdfs"
    output_path = PROJECT_ROOT / "data" / "clinical_testset.csv"
    
    # 2. Find PDF
    pdf_files = list(raw_pdf_dir.glob("*.pdf"))
    if not pdf_files:
        raise FileNotFoundError(f"❌ No PDF found in {raw_pdf_dir}")
    
    input_pdf = pdf_files[0]
    print(f"🏥 Loading clinical guidelines from: {input_pdf.name}...")

    # 3. Load Document
    loader = PyPDFLoader(str(input_pdf))
    documents = loader.load()

    # 4. Initialize Ragas Examiner
    print("🤖 Initializing Ragas Examiner (GPT-4o)...")
    generator_llm = ChatOpenAI(model="gpt-4o")
    critic_llm = ChatOpenAI(model="gpt-4o")
    embeddings = OpenAIEmbeddings()

    generator = TestsetGenerator.from_langchain(
        generator_llm,
        critic_llm,
        embeddings
    )

    # 5. Define Question Types (50% Simple, 25% Reasoning, 25% Multi-context)
    distributions = {
        simple: 0.5,
        reasoning: 0.25,
        multi_context: 0.25
    }

    print(f"🧪 Generating {test_size} synthetic clinical questions... (This will take ~60 seconds)")
    
    # 6. Generate
    testset = generator.generate_with_langchain_docs(
        documents, 
        test_size=test_size, 
        distributions=distributions
    )

    # 7. Save to CSV
    df = testset.to_pandas()
    df.to_csv(output_path, index=False)
    
    print(f"✅ Success! Test set saved to: {output_path}")
    print("\n👀 Sample Questions:")
    print(df[['question', 'ground_truth']].head(3))

if __name__ == "__main__":
    generate_clinical_testset()
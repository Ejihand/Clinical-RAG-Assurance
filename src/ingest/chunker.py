import json
import sys
from pathlib import Path
from typing import List

# -----------------------------------------------------------------------------
# PATH SETUP
# -----------------------------------------------------------------------------
CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

from src.ingest.pdf_parser import parse_pdf
from langchain_text_splitters import RecursiveCharacterTextSplitter

def compare_chunking_strategies(text: str) -> List[str]:
    """
    Splits text into chunks. 
    Selected Strategy: Size=1000, Overlap=200
    """
    print(f"\n{'='*40}")
    print(" 🔪 CHUNKING DOCUMENT")
    print(f"{'='*40}")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    chunks = splitter.split_text(text)
    
    print(f"✅ Generated {len(chunks)} chunks.")
    print(f"👀 Sample Chunk:\n{chunks[0][:150]}...")
    return chunks

def main():
    # 1. Define Paths
    raw_pdf_dir = PROJECT_ROOT / "data" / "raw_pdfs"
    processed_dir = PROJECT_ROOT / "data" / "processed"
    output_path = processed_dir / "chunks.json"

    # Ensure output directory exists
    processed_dir.mkdir(parents=True, exist_ok=True)

    # 2. Find PDF
    pdf_files = list(raw_pdf_dir.glob("*.pdf"))
    if not pdf_files:
        raise FileNotFoundError(f"❌ No PDF found in {raw_pdf_dir}")
    
    input_path = pdf_files[0]
    print(f"📂 Reading Source: {input_path.name}")

    # 3. Parse & Chunk
    raw_text = parse_pdf(str(input_path))
    final_chunks = compare_chunking_strategies(raw_text)

    # 4. Save
    output_data = {
        "source": input_path.name,
        "total_chunks": len(final_chunks),
        "chunks": final_chunks
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
        
    print(f"\n💾 Saved to: {output_path}")

if __name__ == "__main__":
    main()
import json
import sys
from pathlib import Path
from typing import List

# -----------------------------------------------------------------------------
# PATH SETUP (Crucial Fix)
# -----------------------------------------------------------------------------
# 1. Get the absolute path of this script (src/ingest/chunker.py)
CURRENT_FILE = Path(__file__).resolve()

# 2. Calculate Project Root (2 levels up: src/ingest/ -> src/ -> root)
PROJECT_ROOT = CURRENT_FILE.parent.parent.parent

# 3. Add Project Root to sys.path so we can import modules
sys.path.append(str(PROJECT_ROOT))
# -----------------------------------------------------------------------------

# Now we can import from src safely
from src.ingest.pdf_parser import parse_pdf
from langchain_text_splitters import RecursiveCharacterTextSplitter

def compare_chunking_strategies(text: str) -> List[str]:
    """
    Compares chunk sizes 1000 vs 500 and returns the 1000-char chunks.
    """
    print(f"\n{'='*60}")
    print(" 🧪 CHUNK SIZE COMPARISON")
    print(f"{'='*60}")

    # --- Strategy A: 1000 chars ---
    splitter_1000 = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    chunks_1000 = splitter_1000.split_text(text)
    
    print(f"\n--- Strategy A: Size=1000, Overlap=200 (Total: {len(chunks_1000)} chunks) ---")
    for i, chunk in enumerate(chunks_1000[:3]):
        print(f"[Chunk {i+1}]: {chunk[:80].replace(chr(10), ' ')}...")

    # --- Strategy B: 500 chars ---
    splitter_500 = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len,
    )
    chunks_500 = splitter_500.split_text(text)
    
    print(f"\n--- Strategy B: Size=500, Overlap=50 (Total: {len(chunks_500)} chunks) ---")
    for i, chunk in enumerate(chunks_500[:3]):
        print(f"[Chunk {i+1}]: {chunk[:80].replace(chr(10), ' ')}...")

    print(f"\n{'='*60}\n")
    return chunks_1000

def main():
    # Define paths using the robust PROJECT_ROOT constant
    input_path = PROJECT_ROOT / "data" / "guidelines.pdf"
    output_path = PROJECT_ROOT / "data" / "chunks.json"

    # Check if file exists
    if not input_path.exists():
        raise FileNotFoundError(f"PDF file not found at: {input_path}")

    print(f"📂 Reading PDF: {input_path.name}...")
    
    # 1. Parse
    raw_text = parse_pdf(str(input_path))
    
    # 2. Chunk & Compare
    final_chunks = compare_chunking_strategies(raw_text)
    
    # 3. Save
    output_data = {
        "source": input_path.name,
        "total_chunks": len(final_chunks),
        "chunks": final_chunks
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
        
    print(f"✅ Saved {len(final_chunks)} chunks to: {output_path}")

if __name__ == "__main__":
    main()
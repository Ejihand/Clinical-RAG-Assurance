"""
PDF Parser Module
Extracts and cleans text from PDF files using pypdf.
"""

import re
import sys
from pathlib import Path
from pypdf import PdfReader

# -----------------------------------------------------------------------------
# PATH SETUP
# -----------------------------------------------------------------------------
CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parent.parent.parent
sys.path.append(str(PROJECT_ROOT))


def parse_pdf(file_path: str) -> str:
    """
    Extract text from a PDF file and remove headers, footers, and page numbers.
    """
    pdf_path = Path(file_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {file_path}")
    
    try:
        reader = PdfReader(str(pdf_path))
        text_parts = []
        
        for page in reader.pages:
            text_parts.append(page.extract_text())
        
        full_text = "\n".join(text_parts)
        
    except Exception as e:
        raise Exception(f"Error reading PDF file: {str(e)}")
    
    return _clean_text(full_text)


def _clean_text(text: str) -> str:
    """
    Remove headers, footers, and page numbers using Regex.
    """
    # 1. Remove Page Numbers (e.g., "Page 1 of 10", "14")
    text = re.sub(r'^Page\s+\d+\s*(?:of\s+\d+)?\s*$', '', text, flags=re.MULTILINE | re.IGNORECASE)
    text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)
    
    # 2. Remove common headers (Repeated short lines)
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        if len(line.strip()) > 3:  # Skip very short noise lines
            cleaned_lines.append(line)
    
    text = '\n'.join(cleaned_lines)
    
    # 3. Collapse multiple newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


if __name__ == "__main__":
    # TEST BLOCK: Automatically finds the PDF in data/raw_pdfs
    raw_pdfs_dir = PROJECT_ROOT / "data" / "raw_pdfs"
    
    # Find any PDF in the directory
    pdf_files = list(raw_pdfs_dir.glob("*.pdf"))
    
    if pdf_files:
        test_file = pdf_files[0]
        print(f"📄 Found PDF: {test_file.name}")
        
        try:
            print("⏳ Parsing...")
            cleaned = parse_pdf(str(test_file))
            print(f"✅ Success! Extracted {len(cleaned)} characters.")
            print(f"👀 Preview:\n{cleaned[:500]}...")
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print(f"⚠️ No PDFs found in {raw_pdfs_dir}")
"""
PDF Parser Module

This module provides functionality to extract and clean text from PDF files
using pypdf, with regex-based removal of headers, footers, and page numbers.
"""

import re
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    raise ImportError(
        "pypdf is required. Install it using: pip install pypdf"
    )


def parse_pdf(file_path: str) -> str:
    """
    Extract text from a PDF file and remove headers, footers, and page numbers.
    
    Args:
        file_path: Path to the PDF file to parse
        
    Returns:
        Cleaned text content from the PDF
        
    Raises:
        FileNotFoundError: If the PDF file doesn't exist
        Exception: If there's an error reading the PDF
    """
    # Validate file path
    pdf_path = Path(file_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {file_path}")
    
    # Read PDF and extract text
    try:
        reader = PdfReader(file_path)
        text_parts = []
        
        for page_num, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text()
            text_parts.append(page_text)
        
        # Combine all pages
        full_text = "\n".join(text_parts)
        
    except Exception as e:
        raise Exception(f"Error reading PDF file: {str(e)}")
    
    # Clean the text using regex
    cleaned_text = _clean_text(full_text)
    
    return cleaned_text


def _clean_text(text: str) -> str:
    """
    Remove headers, footers, and page numbers from extracted text.
    
    Args:
        text: Raw text extracted from PDF
        
    Returns:
        Cleaned text with headers, footers, and page numbers removed
    """
    # Remove common page number patterns
    # Pattern 1: "Page X" or "Page X of Y" at start or end of line
    text = re.sub(r'^Page\s+\d+\s+(?:of\s+\d+)?\s*$', '', text, flags=re.MULTILINE | re.IGNORECASE)
    
    # Pattern 2: Standalone page numbers (e.g., "1", "2", "3") on their own line
    # This matches numbers that appear alone on a line, likely page numbers
    text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)
    
    # Pattern 3: Page numbers with dashes or slashes (e.g., "1-2", "1/2")
    text = re.sub(r'^\s*\d+\s*[-/]\s*\d+\s*$', '', text, flags=re.MULTILINE)
    
    # Pattern 4: Roman numerals that might be page numbers (I, II, III, etc.)
    text = re.sub(r'^\s*[IVX]+\.?\s*$', '', text, flags=re.MULTILINE)
    
    # Remove common header/footer patterns
    # Pattern 5: Short lines (1-3 words) that repeat frequently (likely headers/footers)
    # We'll identify and remove lines that are very short and appear multiple times
    lines = text.split('\n')
    line_counts = {}
    
    # Count occurrences of each line (normalized)
    for line in lines:
        normalized = line.strip().lower()
        if len(normalized) > 0 and len(normalized) < 50:  # Short lines only
            line_counts[normalized] = line_counts.get(normalized, 0) + 1
    
    # Identify lines that appear more than 2 times (likely headers/footers)
    repeated_lines = {line for line, count in line_counts.items() if count > 2}
    
    # Filter out repeated short lines
    cleaned_lines = []
    for line in lines:
        normalized = line.strip().lower()
        if normalized not in repeated_lines or len(normalized) > 50:
            cleaned_lines.append(line)
    
    text = '\n'.join(cleaned_lines)
    
    # Remove excessive whitespace
    # Replace multiple consecutive newlines with double newline (paragraph break)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Remove leading/trailing whitespace from each line
    lines = [line.rstrip() for line in text.split('\n')]
    text = '\n'.join(lines)
    
    # Remove empty lines at the start and end
    text = text.strip()
    
    return text


if __name__ == "__main__":
    # Test the function on the specified PDF file
    test_file = "data/guidelines.pdf"
    
    try:
        print(f"Parsing PDF: {test_file}")
        cleaned_text = parse_pdf(test_file)
        
        print(f"\n{'='*60}")
        print("Extracted and cleaned text:")
        print(f"{'='*60}\n")
        print(cleaned_text[:1000] + "..." if len(cleaned_text) > 1000 else cleaned_text)
        print(f"\n{'='*60}")
        print(f"Total characters: {len(cleaned_text)}")
        print(f"Total words: {len(cleaned_text.split())}")
        print(f"{'='*60}")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print(f"Please ensure the file '{test_file}' exists.")
    except Exception as e:
        print(f"Error parsing PDF: {e}")


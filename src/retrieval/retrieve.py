import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import chromadb
from chromadb.utils import embedding_functions

# -----------------------------------------------------------------------------
# SETUP
# -----------------------------------------------------------------------------
CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parent.parent.parent
load_dotenv(PROJECT_ROOT / ".env")
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("❌ OPENAI_API_KEY not found in .env file!")

def query_guidelines(question: str, n_results: int = 3):
    """
    Searches the vector database for the most relevant chunks.
    """
    print(f"\n🔍 Querying: '{question}'")
    
    # 1. Connect to DB
    db_path = PROJECT_ROOT / "data" / "chroma_db"
    chroma_client = chromadb.PersistentClient(path=str(db_path))
    
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=api_key,
        model_name="text-embedding-3-small"
    )
    
    collection = chroma_client.get_collection(
        name="malaria_guidelines",
        embedding_function=openai_ef
    )
    
    # 2. Search
    results = collection.query(
        query_texts=[question],
        n_results=n_results
    )
    
    # 3. Print Results
    print(f"\n✅ Found {len(results['documents'][0])} relevant results:\n")
    
    for i, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
        print(f"--- Result {i+1} (Chunk {metadata['chunk_index']}) ---")
        # Print first 300 chars to keep it readable
        print(f"{doc[:300]}...")
        print("\n")

if __name__ == "__main__":
    # Allow running with a question argument, or use a default
    if len(sys.argv) > 1:
        user_question = " ".join(sys.argv[1:])
    else:
        user_question = "What is the recommended treatment for severe malaria?"
        
    query_guidelines(user_question)
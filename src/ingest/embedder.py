import json
import os
import sys
import time
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

def embed_and_store():
    print(f"\n{'='*60}")
    print(" 🧠 EMBEDDING & STORAGE (OpenAI + ChromaDB)")
    print(f"{'='*60}")

    # 1. Load Chunks
    chunks_file = PROJECT_ROOT / "data" / "chunks.json"
    if not chunks_file.exists():
        raise FileNotFoundError(f"Chunks file not found at: {chunks_file}")
        
    print(f"📂 Loading chunks from: {chunks_file.name}...")
    with open(chunks_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        chunks = data["chunks"]

    print(f"   - Found {len(chunks)} text chunks.")

    # 2. Init Database
    db_path = PROJECT_ROOT / "data" / "chroma_db"
    chroma_client = chromadb.PersistentClient(path=str(db_path))

    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=api_key,
        model_name="text-embedding-3-small"
    )

    collection_name = "malaria_guidelines"
    print(f"⚙️  Creating/Loading collection: '{collection_name}'...")
    
    collection = chroma_client.get_or_create_collection(
        name=collection_name,
        embedding_function=openai_ef
    )

    # 3. Batch Processing (The Fix)
    BATCH_SIZE = 100  # Safe size to stay under token limits
    total_chunks = len(chunks)
    
    print(f"🚀 Starting batch processing ({BATCH_SIZE} chunks per batch)...")
    
    for i in range(0, total_chunks, BATCH_SIZE):
        batch_end = min(i + BATCH_SIZE, total_chunks)
        
        # Slice the data for this batch
        batch_chunks = chunks[i:batch_end]
        batch_ids = [f"id_{j}" for j in range(i, batch_end)]
        batch_metadatas = [{"source": "WHO Guidelines", "chunk_index": j} for j in range(i, batch_end)]
        
        print(f"   - Processing batch {i//BATCH_SIZE + 1}: Items {i} to {batch_end}...")
        
        try:
            collection.upsert(
                documents=batch_chunks,
                ids=batch_ids,
                metadatas=batch_metadatas
            )
            # Small sleep to be nice to the API rate limits
            time.sleep(0.5) 
            
        except Exception as e:
            print(f"   ❌ Error in batch {i}: {e}")
            # We continue to the next batch even if one fails
            continue

    print(f"\n✅ Success! All data processed.")
    print(f"   - Database stored in: {db_path}")
    print(f"   - Final Collection Count: {collection.count()}")

if __name__ == "__main__":
    try:
        embed_and_store()
    except Exception as e:
        print(f"❌ Error: {e}")
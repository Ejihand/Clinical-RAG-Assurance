import json
import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv
import chromadb
from chromadb.utils import embedding_functions

# -----------------------------------------------------------------------------
# PATH SETUP
# -----------------------------------------------------------------------------
CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

# Load Env
load_dotenv(PROJECT_ROOT / ".env")
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("❌ OPENAI_API_KEY not found in .env file!")

def embed_and_store():
    print(f"\n{'='*60}")
    print(" 🧠 EMBEDDING & STORAGE")
    print(f"{'='*60}")

    # 1. Load Chunks from 'processed'
    chunks_file = PROJECT_ROOT / "data" / "processed" / "chunks.json"
    
    if not chunks_file.exists():
        raise FileNotFoundError(f"❌ Chunks file not found at: {chunks_file}\nRun chunker.py first!")
        
    print(f"📂 Loading chunks from: {chunks_file.name}...")
    with open(chunks_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        chunks = data["chunks"]

    # 2. Init Vector Database in 'vector_store'
    db_path = PROJECT_ROOT / "data" / "vector_store"
    chroma_client = chromadb.PersistentClient(path=str(db_path))

    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=api_key,
        model_name="text-embedding-3-small"
    )

    collection_name = "clinical_guidelines"
    print(f"⚙️  Collection: '{collection_name}'")
    
    # Delete old collection to start fresh (Optional, but good for testing)
    try:
        chroma_client.delete_collection(collection_name)
    except:
        pass

    collection = chroma_client.create_collection(
        name=collection_name,
        embedding_function=openai_ef
    )

    # 3. Batch Processing
    BATCH_SIZE = 100
    total_chunks = len(chunks)
    
    print(f"🚀 Embedding {total_chunks} chunks...")
    
    for i in range(0, total_chunks, BATCH_SIZE):
        batch_end = min(i + BATCH_SIZE, total_chunks)
        batch_chunks = chunks[i:batch_end]
        batch_ids = [f"id_{j}" for j in range(i, batch_end)]
        batch_metadatas = [{"source": "WHO Guidelines"} for _ in range(len(batch_chunks))]
        
        collection.add(
            documents=batch_chunks,
            ids=batch_ids,
            metadatas=batch_metadatas
        )
        print(f"   ...Processed batch {i}-{batch_end}")
        time.sleep(0.5)

    print(f"\n✅ Database ready at: {db_path}")

if __name__ == "__main__":
    embed_and_store()
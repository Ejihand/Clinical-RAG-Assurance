import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import chromadb
from chromadb.utils import embedding_functions
from openai import OpenAI

# -----------------------------------------------------------------------------
# SETUP
# -----------------------------------------------------------------------------
CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parent.parent
load_dotenv(PROJECT_ROOT / ".env")

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ OPENAI_API_KEY not found!")

# Initialize OpenAI Client for the Generation part
client = OpenAI(api_key=api_key)

def retrieve_context(question: str, n_results: int = 3):
    """
    1. RETRIEVE: Finds the most relevant chunks from ChromaDB.
    """
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
    
    results = collection.query(query_texts=[question], n_results=n_results)
    
    # Flatten the list of strings
    return results['documents'][0]

def generate_answer(question: str):
    """
    2. AUGMENT & GENERATE: Sends the context + question to GPT-4.
    """
    print(f"\n🔎 Searching Guidelines for: '{question}'...")
    
    # A. Get the raw text matches
    context_chunks = retrieve_context(question)
    
    # B. Format them into a single string
    formatted_context = "\n\n---\n\n".join(context_chunks)
    
    # C. Build the Prompt
    system_prompt = """You are a specialized medical assistant. 
    Answer the question strictly based on the provided context from the WHO Malaria Guidelines. 
    If the answer is not in the context, say 'I cannot find the answer in the guidelines.'
    Cite the specific medical recommendations (e.g., dosages, age groups) mentioned."""
    
    user_prompt = f"""Context:
    {formatted_context}
    
    Question: 
    {question}
    """
    
    # D. Call GPT-4
    print("🤖 Thinking...")
    response = client.chat.completions.create(
        model="gpt-4o",  # Or "gpt-4-turbo" / "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.0  # Keep it factual, no creativity
    )
    
    return response.choices[0].message.content

if __name__ == "__main__":
    # Get question from command line or use default
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
    else:
        question = "What is the recommended dosage for artesunate?"
        
    final_answer = generate_answer(question)
    
    print(f"\n{'='*60}")
    print("✅ FINAL ANSWER:")
    print(f"{'='*60}\n")
    print(final_answer)
    print(f"\n{'='*60}")
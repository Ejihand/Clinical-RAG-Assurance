import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Path Setup
CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parent.parent
sys.path.append(str(PROJECT_ROOT))

# Load Env
load_dotenv(PROJECT_ROOT / ".env")

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

def get_rag_chain():
    """
    Creates and returns the RAG processing chain.
    """
    # 1. Setup Vector Store (ChromaDB)
    db_path = PROJECT_ROOT / "data" / "vector_store"
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    
    vectorstore = Chroma(
        persist_directory=str(db_path), 
        embedding_function=embeddings,
        collection_name="clinical_guidelines"
    )
    
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # 2. Setup LLM (GPT-4o)
    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    # 3. Define the Prompt (Clinical Persona)
    template = """You are a strictly clinical AI assistant specializing in malaria guidelines.
    Use the following pieces of retrieved context to answer the question.
    If the answer is not in the context, say "I cannot find this in the guidelines."
    
    Context:
    {context}
    
    Question: {question}
    
    Answer:"""
    
    prompt = ChatPromptTemplate.from_template(template)

    # 4. Build the Chain
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    # We also return the retriever so the evaluator can check context precision
    return rag_chain, retriever

if __name__ == "__main__":
    # Quick Test
    chain, _ = get_rag_chain()
    response = chain.invoke("What is the treatment for severe malaria?")
    print(f"🤖 Answer: {response}")
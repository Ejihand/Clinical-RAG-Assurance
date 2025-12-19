import streamlit as st
import sys
from pathlib import Path

# 1. Path Setup (To find your src folder)
CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parent.parent
sys.path.append(str(PROJECT_ROOT))

from src.rag import get_rag_chain

# 2. Page Config
st.set_page_config(page_title="Clinical RAG Assurance", page_icon="🏥")
st.title("🏥 Clinical RAG Assurance")
st.caption("Strictly grounded AI for WHO Malaria Guidelines")

# 3. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello. I am a strict clinical assistant. Ask me about malaria guidelines."}]

# 4. Initialize RAG Engine (Cached so it doesn't reload every click)
@st.cache_resource
def load_engine():
    chain, _ = get_rag_chain()
    return chain

rag_chain = load_engine()

# 5. Display Chat Messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 6. Chat Input Logic
if prompt := st.chat_input():
    # Append user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Generate Response
    with st.chat_message("assistant"):
        with st.spinner("Consulting guidelines..."):
            response = rag_chain.invoke(prompt)
            st.write(response)
    
    # Append assistant message
    st.session_state.messages.append({"role": "assistant", "content": response})
import streamlit as st
import sys
from pathlib import Path

# -----------------------------------------------------------------------------
# PATH SETUP
# We need to tell Python where the 'src' folder is, 
# because Streamlit runs differently than standard scripts.
# -----------------------------------------------------------------------------
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent
sys.path.append(str(project_root))

# Import your RAG backend function
from src.rag import generate_answer

# -----------------------------------------------------------------------------
# UI CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Clinical RAG Assurance",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Clinical RAG Assurance")
st.markdown("Ask questions based strictly on the **WHO Malaria Guidelines**.")

# -----------------------------------------------------------------------------
# SESSION STATE (Memory)
# This keeps the chat history alive when the app re-runs.
# -----------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar Controls
with st.sidebar:
    st.header("Settings")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# -----------------------------------------------------------------------------
# CHAT INTERFACE
# -----------------------------------------------------------------------------

# 1. Display existing chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 2. Handle new user input
if prompt := st.chat_input("Ex: What is the dosage for artesunate?"):
    
    # A. Display user message immediately
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Save to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # B. Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("🔍 Searching guidelines and generating answer..."):
            try:
                # Call your backend!
                response = generate_answer(prompt)
                st.markdown(response)
                
                # Save response to history
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"An error occurred: {e}")
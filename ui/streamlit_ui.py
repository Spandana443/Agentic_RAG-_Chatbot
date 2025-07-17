import streamlit as st
import sys
import os

# Set up project path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import agents
from agents.ingestion_agent import IngestionAgent
from agents.retrieval_agent import RetrievalAgent
from agents.llm_response_agent import LLMResponseAgent

# Page settings
st.set_page_config(page_title="AgenticRAG: Intelligent Document QA Assistant", layout="wide")

st.markdown(
    "<h1 style='text-align: center;'>AgenticRAG: Intelligent Document QA Assistant</h1>",
    unsafe_allow_html=True
)

# Background styling
st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://static.vecteezy.com/system/resources/previews/001/072/146/non_2x/blue-digital-hi-tech-background-with-hud-design-vector.jpg');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize agents
if "ingestor" not in st.session_state:
    st.session_state.ingestor = IngestionAgent()
if "retriever" not in st.session_state:
    st.session_state.retriever = RetrievalAgent()
if "llm_agent" not in st.session_state:
    st.session_state.llm_agent = LLMResponseAgent()

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Track processed filenames to avoid reprocessing
if "processed_files" not in st.session_state:
    st.session_state.processed_files = []

# === Upload & Auto Process Section ===
st.header("📄 Upload & Process Documents")

uploaded_files = st.file_uploader(
    "Upload Documents (PDF, DOCX, PPTX, CSV, TXT, MD)",
    type=["pdf", "docx", "pptx", "csv", "txt", "md"],
    accept_multiple_files=True,
    key="file_uploader"
)

if uploaded_files:
    current_upload_names = [f.name for f in uploaded_files]
    # Check if new files uploaded
    if current_upload_names != st.session_state.processed_files:
        combined_text = ""
        for file in uploaded_files:
            with open(file.name, "wb") as f:
                f.write(file.getbuffer())
            content = st.session_state.ingestor.extract_text_from_file(file.name)
            combined_text += content + "\n"

        chunks = st.session_state.retriever.chunk_text(combined_text)
        st.session_state.retriever.build_vector_store(chunks)
        st.session_state.processed_files = current_upload_names
        st.success("Documents processed and indexed successfully!")

# === Ask a Question Section ===
st.header("💬 Ask your question")

query = st.chat_input("Type your question here...")

if query:
    if st.session_state.retriever.index is None:
        st.warning("Please upload and process documents first.")
    else:
        # Add user message to chat
        st.session_state.chat_history.append({"role": "user", "content": query})

        # Retrieve top chunks and generate answer
        top_chunks = st.session_state.retriever.retrieve(query)
        prompt = st.session_state.llm_agent.build_prompt(query, top_chunks)
        answer = st.session_state.llm_agent.call_llm(prompt)

        # Add assistant message to chat
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer,
            "source": top_chunks
        })

# === Display Chat Messages ===
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.chat_message("user").markdown(message["content"])
    else:
        with st.chat_message("assistant"):
            st.markdown(message["content"])
            if "source" in message:
                with st.expander("Show Source Context Chunks"):
                    for i, chunk in enumerate(message["source"], start=1):
                        st.markdown(f"**Chunk {i}:** {chunk}")

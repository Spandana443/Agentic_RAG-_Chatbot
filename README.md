# AgenticRAG: Intelligent Document QA Assistant

## Overview

AgenticRAG is a chatbot that answers questions based on uploaded documents by combining document ingestion, semantic retrieval, and Cohere’s language model for context-aware responses.

---

## Setup Instructions

1. Clone the Repository


    git clone https://github.com/yourusername/AgenticRAG.git
cd AgenticRAG

2. Create and Activate Virtual Environment

    python -m venv venv

### Windows
 venv\Scripts\activate

### macOS/Linux
  source venv/bin/activate

3. Install Required Packages

    pip install -r requirements.txt

4. Configure Environment Variables
   Create a .env file in the root directory and add your Cohere API key:

    COHERE_API_KEY=your_cohere_api_key_here

5. Run the Application

    streamlit run ui/streamlit_ui.py


#### Dependencies
Python 3.8+

streamlit

cohere

sentence-transformers

faiss-cpu

pdfplumber

python-docx

python-pptx

pandas

python-dotenv

## Usage
Upload supported documents (PDF, DOCX, PPTX, CSV, TXT, MD).

Click Process Uploaded Documents to extract and index content.

Ask questions using the chat input and receive answers with source context.
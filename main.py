from agents.ingestion_agent import IngestionAgent
from agents.retrieval_agent import RetrievalAgent
from agents.llm_response_agent import LLMResponseAgent

# Load and process document
ingestor = IngestionAgent()
text = ingestor.extract_text_from_file("sample.pdf")  # Replace with your file

# Retrieve relevant context
retriever = RetrievalAgent()
chunks = retriever.chunk_text(text)
retriever.build_vector_store(chunks)

query = "What KPIs are mentioned in Q1?"
top_chunks = retriever.retrieve(query)

# Generate final answer
llm_agent = LLMResponseAgent()
prompt = llm_agent.build_prompt(query, top_chunks)
response = llm_agent.call_llm(prompt)

print("\nFinal Answer:\n", response)


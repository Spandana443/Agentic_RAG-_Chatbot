import os
import cohere
from dotenv import load_dotenv

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(COHERE_API_KEY)

class LLMResponseAgent:
    def __init__(self, max_context_chunks=3):
        self.max_context_chunks = max_context_chunks

    def build_prompt(self, query: str, context_chunks: list) -> str:
        selected_chunks = context_chunks[:self.max_context_chunks]
        context = "\n\n".join(selected_chunks)
        return f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"

    def call_llm(self, prompt: str) -> str:
        try:
            response = co.chat(
                model="command-r",
                message=prompt,
                temperature=0.5
            )
            return response.text.strip()
        except Exception as e:
            return f"[Error] Cohere API call failed: {e}"

# agents/retrieval_agent.py

from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

class RetrievalAgent:
    def __init__(self):
        # Load model on CPU explicitly to avoid meta tensor error
        self.model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
        self.text_chunks = []
        self.index = None

    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 100) -> list:
        """
        Splits long text into smaller overlapping chunks.
        """
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start += chunk_size - overlap
        return chunks

    def build_vector_store(self, chunks: list):
        """
        Embeds chunks and builds FAISS index.
        """
        self.text_chunks = chunks
        embeddings = self.model.encode(chunks, convert_to_numpy=True)
        embeddings = np.array(embeddings).astype("float32")

        self.index = faiss.IndexFlatL2(embeddings.shape[1])  # L2 distance index
        self.index.add(embeddings)

    def retrieve(self, query: str, top_k: int = 3) -> list:
        """
        Retrieves top-K most relevant chunks for a given query.
        """
        if self.index is None:
            raise ValueError("Index is not built. Call build_vector_store() first.")

        query_vector = self.model.encode([query], convert_to_numpy=True).astype("float32")
        distances, indices = self.index.search(query_vector, top_k)

        return [self.text_chunks[i] for i in indices[0]]

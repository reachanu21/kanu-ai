from rag.embedder import LocalEmbedder
from rag.vector_store import VectorStore

class RAGEngine:
    def __init__(self):
        self.embedder = LocalEmbedder()
        self.store = VectorStore()

    def add_document(self, text):
        embedding = self.embedder.embed(text)
        self.store.add(embedding, text)

    def query(self, question):
        q_embed = self.embedder.embed(question)
        results = self.store.search(q_embed, k=5)
        return results

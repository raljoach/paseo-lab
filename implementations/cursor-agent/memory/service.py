import numpy as np

from embeddings.local_provider import LocalEmbeddingProvider
from memory.store import MemoryStore

class MemoryService:
    def __init__(self):
        self.store = MemoryStore()
        self.embedding_provider = LocalEmbeddingProvider()

    def add_memory(self, text: str):
        memories = self.store.load()
        normalized = text.strip().lower()
        for memory in memories:
            existing = memory["text"].strip().lower()
            if existing == normalized:
                return

        embedding = self.embedding_provider.embed(text)
        memories.append({
            "text": text,
            "embedding": embedding,
        })
        self.store.save(memories)

    def retrieve(self, query: str, top_k: int = 3) -> list[str]:
        memories = self.store.load()

        if not memories:
            return []

        query_embedding = np.array(
            self.embedding_provider.embed(query)
        )

        scored = []

        for memory in memories:
            embedding = np.array(memory["embedding"])

            similarity = self._cosine_similarity(
                query_embedding,
                embedding,
            )

            scored.append(
                (
                    similarity,
                    memory["text"],
                )
            )

        scored.sort(reverse=True)

        return [
            text
            for _, text in scored[:top_k]
        ]

    def _cosine_similarity(
        self,
        a,
        b,
    ):
        return np.dot(a, b) / (
            np.linalg.norm(a) *
            np.linalg.norm(b)
        )
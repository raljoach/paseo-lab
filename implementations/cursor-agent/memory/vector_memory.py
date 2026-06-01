from sentence_transformers import SentenceTransformer
import numpy as np


class VectorMemory:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        self.memories = []

    def add_memory(
        self,
        text: str,
    ):
        embedding = self.model.encode(text)

        self.memories.append(
            {
                "text": text,
                "embedding": embedding,
            }
        )

    def retrieve(
        self,
        query: str,
        top_k: int = 3,
    ) -> list[str]:
        if not self.memories:
            return []

        query_embedding = self.model.encode(query)

        scored = []

        for memory in self.memories:
            similarity = np.dot(
                query_embedding,
                memory["embedding"],
            )

            scored.append(
                (
                    similarity,
                    memory["text"],
                )
            )

        scored.sort(
            key=lambda x: x[0],
            reverse=True,
        )

        return [text for _, text in scored[:top_k]]

    def store_text(
        self,
        text: str,
    ):
        existing = [memory["text"] for memory in self.memories]

        if text not in existing:
            self.add_memory(text)

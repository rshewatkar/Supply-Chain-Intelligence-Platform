from app.embeddings.qdrant_manager import QdrantManager


class SearchEngine:
    """
    Semantic search over indexed supply-chain documents.
    """

    def __init__(self):
        self.qdrant = QdrantManager()

    def search(
        self,
        query: str,
        limit: int = 5,
    ) -> list[dict]:

        results = self.qdrant.search(
            query=query,
            limit=limit,
        )

        formatted = []

        for result in results:

            payload = result.payload

            formatted.append(
                {
                    "score": result.score,
                    "company": payload["company"],
                    "ticker": payload["ticker"],
                    "document_type": payload["document_type"],
                    "file_name": payload["file_name"],
                    "text": payload["text"],
                    "chunk_index": payload["chunk_index"],
                }
            )

        return formatted
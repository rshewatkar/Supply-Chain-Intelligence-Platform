from app.embeddings.search import SearchEngine
from app.utils.logger import get_logger


logger = get_logger(__name__)


class Retriever:
    """
    Retrieve relevant document chunks for RAG.

    This class acts as the RAG retrieval layer and reuses
    the existing SearchEngine.

    Flow:

        User Query
            ↓
        Retriever
            ↓
        SearchEngine
            ↓
        Qdrant
            ↓
        Relevant Chunks
    """

    def __init__(self):
        self.search_engine = SearchEngine()

    # =========================================================
    # Retrieve
    # =========================================================

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[dict]:
        """
        Retrieve the most relevant document chunks.

        Parameters
        ----------
        query : str
            User's natural-language question.

        top_k : int
            Number of relevant chunks to retrieve.

        Returns
        -------
        list[dict]
            Retrieved chunks with metadata and similarity score.
        """

        if not query or not query.strip():
            raise ValueError(
                "Query cannot be empty."
            )

        if top_k <= 0:
            raise ValueError(
                "top_k must be greater than 0."
            )

        query = query.strip()

        logger.info(
            "Retrieving relevant chunks for query: %s",
            query,
        )

        results = self.search_engine.search(
            query=query,
            limit=top_k,
        )

        logger.info(
            "Retrieved %d relevant chunks.",
            len(results),
        )

        return results

    # =========================================================
    # Retrieve With Score Threshold
    # =========================================================

    def retrieve_relevant(
        self,
        query: str,
        top_k: int = 5,
        min_score: float = 0.0,
    ) -> list[dict]:
        """
        Retrieve chunks and filter out low-relevance results.

        Parameters
        ----------
        query : str
            User's question.

        top_k : int
            Maximum number of chunks to retrieve.

        min_score : float
            Minimum semantic similarity score.

        Returns
        -------
        list[dict]
            Relevant chunks above the score threshold.
        """

        results = self.retrieve(
            query=query,
            top_k=top_k,
        )

        filtered_results = [
            result
            for result in results
            if result.get("score", 0.0) >= min_score
        ]

        logger.info(
            "Filtered %d/%d chunks using minimum score %.4f.",
            len(filtered_results),
            len(results),
            min_score,
        )

        return filtered_results

    # =========================================================
    # Build Context
    # =========================================================

    def build_context(
        self,
        results: list[dict],
    ) -> str:
        """
        Convert retrieved chunks into a text context
        that can later be passed to the prompt builder.

        Parameters
        ----------
        results : list[dict]
            Retrieved search results.

        Returns
        -------
        str
            Formatted context.
        """

        if not results:
            return ""

        context_parts = []

        for index, result in enumerate(
            results,
            start=1,
        ):
            context_parts.append(
                f"""
SOURCE {index}
Company: {result.get("company", "Unknown")}
Ticker: {result.get("ticker", "Unknown")}
Document: {result.get("file_name", "Unknown")}
Document Type: {result.get("document_type", "Unknown")}
Chunk: {result.get("chunk_index", "Unknown")}
Relevance Score: {result.get("score", 0.0):.4f}

{result.get("text", "")}
""".strip()
            )

        return "\n\n".join(context_parts)

    # =========================================================
    # Retrieve Context
    # =========================================================

    def retrieve_context(
        self,
        query: str,
        top_k: int = 5,
        min_score: float = 0.0,
    ) -> dict:
        """
        Retrieve relevant chunks and build the context
        required by the next RAG stages.

        Returns
        -------
        dict
            Contains both raw results and formatted context.
        """

        results = self.retrieve_relevant(
            query=query,
            top_k=top_k,
            min_score=min_score,
        )

        context = self.build_context(
            results
        )

        return {
            "query": query,
            "results": results,
            "context": context,
        }

    # =========================================================
    # Close
    # =========================================================

    def close(self) -> None:
        """
        Close retriever resources.
        """
        self.search_engine.close()
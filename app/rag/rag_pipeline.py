from app.rag.llm import LLM
from app.rag.prompts import PromptBuilder
from app.rag.retriever import Retriever
from app.utils.logger import get_logger


logger = get_logger(__name__)


class RAGPipeline:
    """
    End-to-end Retrieval-Augmented Generation pipeline.

    Flow:

        Question
            ↓
        Retriever
            ↓
        Relevant document chunks
            ↓
        Prompt builder
            ↓
        LLM
            ↓
        Final answer
    """

    def __init__(self):
        self.retriever = Retriever()
        self.llm = LLM()

    # =========================================================
    # Retrieve Context
    # =========================================================

    def retrieve_context(
        self,
        question: str,
        limit: int = 5,
    ) -> list[dict]:
        """
        Retrieve relevant document chunks for a question.
        """

        if not question or not question.strip():
            raise ValueError("Question cannot be empty.")

        logger.info(
            "Retrieving context for question: %s",
            question,
        )

        retrieval_result = self.retriever.retrieve_context(
            query=question,
            top_k=limit,
        )

        results = retrieval_result["results"]

        logger.info(
            "Retrieved %s relevant chunks.",
            len(results),
        )

        return results

    # =========================================================
    # Build Context
    # =========================================================

    def build_context(
        self,
        retrieved_documents: list[dict],
    ) -> str:
        """
        Convert retrieved documents into prompt context.
        """

        if not retrieved_documents:
            return ""

        context_parts = []

        for index, document in enumerate(
            retrieved_documents,
            start=1,
        ):
            context_parts.append(
                f"""
                Source {index}
                Company: {document.get("company", "Unknown")}
                Document: {document.get("file_name", "Unknown")}
                Document Type: {document.get("document_type", "Unknown")}
                Relevance Score: {document.get("score", 0.0):.4f}
                
                Content:
                {document.get("text", "")}
                """.strip()
            )

        return "\n\n".join(context_parts)

    # =========================================================
    # Generate Answer
    # =========================================================

    def generate_answer(
        self,
        question: str,
        limit: int = 5,
    ) -> dict:
        """
        Execute the complete RAG pipeline.
        """

        logger.info(
            "Starting RAG pipeline..."
        )

        retrieved_documents = self.retrieve_context(
            question,
            limit=limit,
        )

        context = self.build_context(
            retrieved_documents
        )

        prompt_builder = PromptBuilder()
        prompt = prompt_builder.build(
            question=question,
            context=context,
        )

        logger.info(
            "Generating answer using LLM..."
        )

        answer = self.llm.generate(prompt)

        logger.info(
            "RAG pipeline completed successfully."
        )

        return {
            "question": question,
            "answer": answer,
            "sources": retrieved_documents,
            "source_count": len(
                retrieved_documents
            ),
        }

    # =========================================================
    # Close
    # =========================================================

    def close(self):
        """
        Close pipeline resources.
        """

        self.retriever.close()
        self.llm.close()
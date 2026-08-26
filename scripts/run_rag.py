from app.rag.rag_pipeline import RAGPipeline
from app.utils.logger import get_logger


logger = get_logger(__name__)


def main():
    print("=" * 60)
    print("Supply Chain Intelligence Platform")
    print("Working RAG Pipeline")
    print("=" * 60)

    pipeline = RAGPipeline()

    try:
        question = input(
            "\nEnter your question: "
        ).strip()

        if not question:
            print("Question cannot be empty.")
            return

        result = pipeline.generate_answer(
            question,
            limit=5,
        )

        print("\n" + "=" * 60)
        print("RAG Answer")
        print("=" * 60)

        print(result["answer"])

        print("\n" + "=" * 60)
        print("Retrieved Sources")
        print("=" * 60)

        for index, source in enumerate(
            result["sources"],
            start=1,
        ):
            print(
                f"\n[{index}] "
                f"{source.get('company', 'Unknown')} | "
                f"{source.get('file_name', 'Unknown')}"
            )

            print(
                f"Score: "
                f"{source.get('score', 0.0):.4f}"
            )

            print(
                f"Chunk: "
                f"{source.get('chunk_index', 'Unknown')}"
            )

        print("\n" + "=" * 60)
        print("Working RAG Pipeline Completed")
        print("=" * 60)

    except Exception as exc:
        logger.exception(
            "RAG pipeline failed."
        )

        print("\n" + "=" * 60)
        print("RAG Pipeline Failed")
        print(f"Error: {exc}")
        print("=" * 60)

    finally:
        pipeline.close()


if __name__ == "__main__":
    main()
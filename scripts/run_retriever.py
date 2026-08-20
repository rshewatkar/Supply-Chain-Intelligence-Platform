from app.rag.retriever import Retriever
from app.utils.logger import get_logger


logger = get_logger(__name__)


def main():
    print("=" * 60)
    print("Supply Chain Intelligence Platform")
    print("RAG Retriever")
    print("=" * 60)

    retriever = Retriever()

    try:
        query = input(
            "\nEnter your question: "
        ).strip()

        if not query:
            print(
                "Query cannot be empty."
            )
            return

        top_k_input = input(
            "Number of chunks [5]: "
        ).strip()

        top_k = (
            int(top_k_input)
            if top_k_input
            else 5
        )

        results = retriever.retrieve(
            query=query,
            top_k=top_k,
        )

        print("\n" + "=" * 60)
        print("Retrieved Chunks")
        print("=" * 60)

        if not results:
            print(
                "\nNo relevant chunks found."
            )
            return

        for index, result in enumerate(
            results,
            start=1,
        ):
            print("\n" + "-" * 60)

            print(
                f"Result             : {index}"
            )

            print(
                f"Score              : "
                f"{result.get('score', 0.0):.4f}"
            )

            print(
                f"Company            : "
                f"{result.get('company', 'Unknown')}"
            )

            print(
                f"Ticker             : "
                f"{result.get('ticker', 'Unknown')}"
            )

            print(
                f"Document           : "
                f"{result.get('file_name', 'Unknown')}"
            )

            print(
                f"Document Type      : "
                f"{result.get('document_type', 'Unknown')}"
            )

            print(
                f"Chunk Index        : "
                f"{result.get('chunk_index', 'Unknown')}"
            )

            print("\nText:")
            print(
                result.get(
                    "text",
                    "",
                )
            )

        print("\n" + "=" * 60)
        print("Retriever Completed")
        print("=" * 60)

    except ValueError as exc:

        logger.error(
            "Invalid input: %s",
            exc,
        )

        print(
            f"\nInvalid input: {exc}"
        )

    except Exception as exc:

        logger.exception(
            "Retriever failed."
        )

        print("\n" + "=" * 60)
        print("Retriever Failed")
        print(
            f"Error: {exc}"
        )
        print("=" * 60)


if __name__ == "__main__":
    main()
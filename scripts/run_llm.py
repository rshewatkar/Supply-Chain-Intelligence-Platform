from app.rag.llm import LLM
from app.utils.logger import get_logger


logger = get_logger(__name__)


def main():

    print("=" * 60)
    print("Supply Chain Intelligence Platform")
    print("LLM Test")
    print("=" * 60)

    llm = LLM()

    try:

        print(
            f"\nProvider : {llm.get_provider()}"
        )

        print(
            f"Model    : {llm.get_model()}"
        )

        try:
            prompt = input(
                "\nEnter prompt: "
            ).strip()

        except EOFError:
            print(
                "\nNo prompt received. Run this command in an interactive "
                "terminal or pipe a prompt into it."
            )

            return

        if not prompt:

            print(
                "Prompt cannot be empty."
            )

            return

        print("\nGenerating response...\n")

        answer = llm.generate(
            prompt
        )

        print("=" * 60)
        print("LLM RESPONSE")
        print("=" * 60)

        print(answer)

        print("\n" + "=" * 60)
        print("LLM Test Completed")
        print("=" * 60)

    except Exception as exc:

        logger.error(
            "LLM test failed: %s",
            exc,
        )

        print("\n" + "=" * 60)
        print("LLM Test Failed")
        print(
            f"Error: {exc}"
        )
        print("=" * 60)


if __name__ == "__main__":
    main()

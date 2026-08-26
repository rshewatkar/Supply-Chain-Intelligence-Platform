from app.rag.llm import LLM
from app.utils.logger import get_logger


logger = get_logger(__name__)


def main():
    print("=" * 60)
    print("Supply Chain Intelligence Platform")
    print("LLM Test")
    print("=" * 60)

    llm = None

    try:
        # =====================================================
        # Initialize LLM
        # =====================================================

        llm = LLM()

        print(
            f"\nModel: {llm.get_model_name()}"
        )

        # =====================================================
        # Test Prompt
        # =====================================================

        prompt = """
You are a supply-chain intelligence assistant.

Answer the following question clearly and concisely.

Question:
Why is supplier dependency important in supply-chain risk analysis?
"""

        print("\nSending prompt to LLM...")

        # =====================================================
        # Generate Response
        # =====================================================

        response = llm.generate(prompt)

        # =====================================================
        # Display Response
        # =====================================================

        print("\n" + "=" * 60)
        print("LLM Response")
        print("=" * 60)

        print(response)

        print("\n" + "=" * 60)
        print("LLM Test Completed")
        print("=" * 60)

    except Exception as exc:
        logger.exception(
            "LLM test failed."
        )

        print("\n" + "=" * 60)
        print("LLM Test Failed")
        print(f"Error: {exc}")
        print("=" * 60)

    finally:
        if llm is not None:
            llm.close()


if __name__ == "__main__":
    main()
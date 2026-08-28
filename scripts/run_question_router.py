from app.chat.question_router import QuestionRouter
from app.utils.logger import get_logger


logger = get_logger(__name__)


def main():
    print("=" * 60)
    print("Supply Chain Intelligence Platform")
    print("Question Router")
    print("=" * 60)

    router = QuestionRouter()

    try:
        while True:
            question = input(
                "\nEnter your question (or type 'exit'): "
            ).strip()

            if question.lower() in {
                "exit",
                "quit",
            }:
                break

            if not question:
                print("Question cannot be empty.")
                continue

            result = router.route(question)

            print("\n" + "=" * 60)
            print("Routing Result")
            print("=" * 60)

            print(
                f"Question : {result['question']}"
            )

            print(
                f"Intent   : {result['intent']}"
            )

            print(
                f"Confidence: "
                f"{result['confidence']:.2f}"
            )

            print("=" * 60)

    except Exception as exc:
        logger.exception(
            "Question router failed."
        )

        print("\n" + "=" * 60)
        print("Question Router Failed")
        print(f"Error: {exc}")
        print("=" * 60)


if __name__ == "__main__":
    main()
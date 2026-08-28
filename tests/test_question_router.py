from app.chat.question_router import QuestionRouter


def test_supplier_question():
    router = QuestionRouter()

    result = router.route(
        "Who supplies Apple?"
    )

    assert result["intent"] == "supplier"


def test_common_supplier_question():
    router = QuestionRouter()

    result = router.route(
        "Which suppliers are common between Apple and NVIDIA?"
    )

    assert result["intent"] == "common_supplier"


def test_dependency_question():
    router = QuestionRouter()

    result = router.route(
        "What is Apple's highest dependency?"
    )

    assert result["intent"] == "dependency"


def test_tier_question():
    router = QuestionRouter()

    result = router.route(
        "Show Tier-2 suppliers for Apple"
    )

    assert result["intent"] == "tier"


def test_general_supply_chain_question():
    router = QuestionRouter()

    result = router.route(
        "Explain the semiconductor supply chain"
    )

    assert result["intent"] == "general"


def test_empty_question():
    router = QuestionRouter()

    result = router.route("")

    assert result["intent"] == "general"
    assert result["confidence"] == 0.0
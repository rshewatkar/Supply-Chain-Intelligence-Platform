from app.analytics.risk_score_engine import RiskScoreEngine


def test_risk_score_calculation():

    engine = RiskScoreEngine.__new__(
        RiskScoreEngine
    )

    score = engine.calculate_risk_score(
        supplier_dependency=0.8,
        country_dependency=0.6,
        tier1_dependency=0.7,
        tier2_dependency=0.5,
    )

    expected = (
        0.8 * 0.35
        + 0.6 * 0.20
        + 0.7 * 0.25
        + 0.5 * 0.20
    )

    assert score == round(expected, 4)


def test_critical_risk_level():

    engine = RiskScoreEngine.__new__(
        RiskScoreEngine
    )

    assert (
        engine.assign_risk_level(0.80)
        == "CRITICAL"
    )


def test_high_risk_level():

    engine = RiskScoreEngine.__new__(
        RiskScoreEngine
    )

    assert (
        engine.assign_risk_level(0.60)
        == "HIGH"
    )


def test_medium_risk_level():

    engine = RiskScoreEngine.__new__(
        RiskScoreEngine
    )

    assert (
        engine.assign_risk_level(0.30)
        == "MEDIUM"
    )


def test_low_risk_level():

    engine = RiskScoreEngine.__new__(
        RiskScoreEngine
    )

    assert (
        engine.assign_risk_level(0.10)
        == "LOW"
    )
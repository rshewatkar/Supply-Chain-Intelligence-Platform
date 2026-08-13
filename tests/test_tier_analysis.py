from app.analytics.tier_analysis import TierAnalysis


def test_tier_analysis_methods_exist():

    analyzer = TierAnalysis()

    assert callable(
        analyzer.get_tier_1_dependencies
    )

    assert callable(
        analyzer.get_tier_2_dependencies
    )

    assert callable(
        analyzer.get_tier_summary
    )

    assert callable(
        analyzer.top_tier_1_dependencies
    )

    assert callable(
        analyzer.top_tier_2_dependencies
    )

    assert callable(
        analyzer.run
    )

    analyzer.close()
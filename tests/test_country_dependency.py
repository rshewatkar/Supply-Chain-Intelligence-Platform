from app.analytics.country_dependency import CountryDependency


def test_country_dependency_initialization():

    analyzer = CountryDependency()

    assert analyzer is not None

    analyzer.close()
from app.analytics.country_dependency import CountryDependency


def main():

    print("=" * 60)
    print("Supply Chain Intelligence Platform")
    print("Country Dependency Analysis")
    print("=" * 60)

    analyzer = CountryDependency()

    try:

        results = analyzer.run()

        print()
        print("Country Dependency")
        print("-" * 60)

        if not results:
            print("No country dependency data found.")
            return

        for row in results:

            print(
                f"{row['country']:<25}"
                f"Entities: {row['connected_entities']:<5}"
                f"Relationships: {row['total_relationships']:<5}"
                f"Score: {row['dependency_score']:.4f}"
            )

        print()
        print("Top Dependency Countries")
        print("-" * 60)

        top_countries = analyzer.top_dependency_countries(10)

        for row in top_countries:

            print(
                f"{row['country']:<25}"
                f"Entities: {row['connected_entities']:<5}"
                f"Relationships: {row['total_relationships']}"
            )

        print()
        print("Country Dependency Risk")
        print("-" * 60)

        risk_data = analyzer.country_dependency_risk(10)

        for row in risk_data:

            print(
                f"{row['country']:<25}"
                f"Entities: {row['connected_entities']:<5}"
                f"Relationships: {row['total_relationships']:<5}"
                f"Risk: {row['risk_level']}"
            )

        print()
        print("=" * 60)
        print("Country Dependency Analysis Completed")
        print("=" * 60)

    except Exception as exc:

        print()
        print("=" * 60)
        print("Country Dependency Analysis Failed")
        print(f"Error: {exc}")
        print("=" * 60)

        raise

    finally:
        analyzer.close()


if __name__ == "__main__":
    main()
from app.analytics.tier_analysis import TierAnalysis


def main():

    print("=" * 60)
    print("Supply Chain Intelligence Platform")
    print("Tier-1 / Tier-2 Dependency Analysis")
    print("=" * 60)

    company_name = input(
        "\nEnter company name: "
    ).strip()

    if not company_name:
        print("Company name cannot be empty.")
        return

    analyzer = TierAnalysis()

    try:

        result = analyzer.run(
            company_name
        )

        print("\n" + "=" * 60)
        print("Tier Summary")
        print("=" * 60)

        for row in result["summary"]:
            print(
                f"\nCompany              : "
                f"{row['company']}"
            )

            print(
                f"Tier-1 Dependencies  : "
                f"{row['tier_1_dependencies']}"
            )

            print(
                f"Tier-2 Dependencies  : "
                f"{row['tier_2_dependencies']}"
            )

        # =================================================
        # Tier-1
        # =================================================

        print("\n" + "=" * 60)
        print("Tier-1 Dependencies")
        print("=" * 60)

        for row in result["tier_1"]:

            print(
                f"{row['dependency']:<30}"
                f"{row['dependency_type']:<18}"
                f"{row['relationship_type']:<20}"
                f"{row['occurrence_count']}"
            )

        # =================================================
        # Tier-2
        # =================================================

        print("\n" + "=" * 60)
        print("Tier-2 Dependencies")
        print("=" * 60)

        for row in result["tier_2"]:

            print(
                f"{row['tier_2_entity']:<30}"
                f"{row['tier_2_type']:<18}"
                f"through: "
                f"{row['tier_1_entity']:<20}"
                f"{row['tier_1_relationship']} -> "
                f"{row['tier_2_relationship']}"
            )

        print("\n" + "=" * 60)
        print("Tier Analysis Completed")
        print("=" * 60)

    except Exception as exc:

        print("\n" + "=" * 60)
        print("Tier Analysis Failed")
        print(f"Error: {exc}")
        print("=" * 60)

    finally:

        analyzer.close()


if __name__ == "__main__":
    main()
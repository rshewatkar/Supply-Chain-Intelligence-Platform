from app.analytics.risk_score_engine import RiskScoreEngine
from app.utils.logger import get_logger


logger = get_logger(__name__)


def main():

    print("=" * 60)
    print("Supply Chain Intelligence Platform")
    print("Risk Score Engine")
    print("=" * 60)

    engine = RiskScoreEngine()

    try:

        # =====================================================
        # Run Complete Risk Scoring Pipeline
        # =====================================================

        result = engine.run()

        scored_entities = result.get(
            "results",
            []
        )

        top_entities = result.get(
            "top_entities",
            []
        )

        # =====================================================
        # Display Results
        # =====================================================

        print("\n" + "=" * 60)
        print("Risk Scoring Completed")
        print("=" * 60)

        print(
            f"Entities Scored : "
            f"{len(scored_entities)}"
        )

        # =====================================================
        # Top Risky Entities
        # =====================================================

        print("\n" + "=" * 60)
        print("Top Risky Entities")
        print("=" * 60)

        if not top_entities:

            print(
                "No risk-scored entities found."
            )

        else:

            for entity in top_entities:

                print(
                    f"{entity['name']:<30} "
                    f"{entity['entity_type']:<15} "
                    f"Risk: "
                    f"{entity['risk_score']:.4f} "
                    f"{entity['risk_level']}"
                )

        # =====================================================
        # Optional Entity Search
        # =====================================================

        entity_name = input(
            "\nEnter entity name to inspect "
            "(press Enter to skip): "
        ).strip()

        if entity_name:

            matching_entities = [
                row
                for row in scored_entities
                if row.get("name", "").lower()
                == entity_name.lower()
            ]

            if not matching_entities:

                print(
                    f"\nEntity '{entity_name}' "
                    f"was not found."
                )

            else:

                entity = matching_entities[0]

                print("\n" + "=" * 60)
                print("Risk Assessment")
                print("=" * 60)

                print(
                    f"Entity              : "
                    f"{entity['name']}"
                )

                print(
                    f"Supplier Dependency : "
                    f"{entity['supplier_dependency']:.4f}"
                )

                print(
                    f"Country Dependency  : "
                    f"{entity['country_dependency']:.4f}"
                )

                print(
                    f"Tier-1 Dependency   : "
                    f"{entity['tier1_dependency']:.4f}"
                )

                print(
                    f"Tier-2 Dependency   : "
                    f"{entity['tier2_dependency']:.4f}"
                )

                print(
                    f"Risk Score          : "
                    f"{entity['risk_score']:.4f}"
                )

                print(
                    f"Risk Level          : "
                    f"{entity['risk_level']}"
                )

                print(
                    f"Degree              : "
                    f"{entity['degree']:.4f}"
                )

                print(
                    f"Betweenness         : "
                    f"{entity['betweenness']:.4f}"
                )

                print(
                    f"Closeness           : "
                    f"{entity['closeness']:.4f}"
                )

        print("\n" + "=" * 60)
        print("Risk Score Engine Completed Successfully")
        print("=" * 60)

    except Exception as exc:

        logger.exception(
            "Risk score engine failed."
        )

        print("\n" + "=" * 60)
        print("Risk Score Engine Failed")
        print(
            f"Error: {exc}"
        )
        print("=" * 60)

    finally:

        engine.close()


if __name__ == "__main__":
    main()
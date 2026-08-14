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
        entity_name = input(
            "\nEnter company/entity name: "
        ).strip()

        if not entity_name:
            print("Entity name cannot be empty.")
            return

        result = engine.calculate_and_save(
            entity_name
        )

        if result is None:
            print(
                f"\nNo dependency metrics found "
                f"for {entity_name}."
            )
            return

        print("\n" + "=" * 60)
        print("Risk Assessment")
        print("=" * 60)

        print(
            f"Entity              : {result['entity']}"
        )

        print(
            f"Supplier Dependency : "
            f"{result['supplier_dependency']:.4f}"
        )

        print(
            f"Country Dependency  : "
            f"{result['country_dependency']:.4f}"
        )

        print(
            f"Tier-1 Dependency   : "
            f"{result['tier1_dependency']:.4f}"
        )

        print(
            f"Tier-2 Dependency   : "
            f"{result['tier2_dependency']:.4f}"
        )

        print(
            f"Risk Score          : "
            f"{result['risk_score']:.4f}"
        )

        print(
            f"Risk Level          : "
            f"{result['risk_level']}"
        )

        print("\n" + "=" * 60)
        print("Top Risky Entities")
        print("=" * 60)

        risky_entities = (
            engine.top_risky_entities(20)
        )

        for entity in risky_entities:
            print(
                f"{entity['entity']:<30} "
                f"{entity['type']:<15} "
                f"Risk: "
                f"{entity['risk_score']:.4f} "
                f"{entity['risk_level']}"
            )

        print("\n" + "=" * 60)
        print("Risk Score Engine Completed")
        print("=" * 60)

    except Exception as exc:
        logger.exception(
            "Risk score engine failed."
        )

        print("\n" + "=" * 60)
        print("Risk Score Engine Failed")
        print(f"Error: {exc}")
        print("=" * 60)

    finally:
        engine.close()


if __name__ == "__main__":
    main()
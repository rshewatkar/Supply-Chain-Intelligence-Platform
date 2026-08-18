from app.dashboard.risk_dashboard_backend import (
    RiskDashboardBackend,
)
from app.utils.logger import get_logger


logger = get_logger(__name__)


def main():

    print("=" * 60)
    print("Supply Chain Intelligence Platform")
    print("Risk Dashboard Backend")
    print("=" * 60)

    backend = RiskDashboardBackend()

    try:

        limit = 20

        data = backend.get_dashboard_data(limit)

        # -----------------------------------------------------
        # Overview
        # -----------------------------------------------------

        print("\n" + "=" * 60)
        print("Risk Overview")
        print("=" * 60)

        overview = data["overview"]

        print(
            f"Total Entities     : "
            f"{overview.get('total_entities', 0)}"
        )

        print(
            f"Critical           : "
            f"{overview.get('critical_entities', 0)}"
        )

        print(
            f"High               : "
            f"{overview.get('high_entities', 0)}"
        )

        print(
            f"Medium             : "
            f"{overview.get('medium_entities', 0)}"
        )

        print(
            f"Low                : "
            f"{overview.get('low_entities', 0)}"
        )

        print(
            f"Average Risk       : "
            f"{overview.get('average_risk_score', 0.0):.4f}"
        )

        print(
            f"Maximum Risk       : "
            f"{overview.get('maximum_risk_score', 0.0):.4f}"
        )

        # -----------------------------------------------------
        # Top Risky Entities
        # -----------------------------------------------------

        print("\n" + "=" * 60)
        print("Top Risky Entities")
        print("=" * 60)

        for row in data["top_risky_entities"]:

            print(
                f"{row.get('entity', 'Unknown'):<30} "
                f"{row.get('type', 'Unknown'):<15} "
                f"Risk: "
                f"{row.get('risk_score', 0.0):.4f} "
                f"{row.get('risk_level', 'UNKNOWN')}"
            )

        # -----------------------------------------------------
        # Risk Distribution
        # -----------------------------------------------------

        print("\n" + "=" * 60)
        print("Risk Distribution")
        print("=" * 60)

        for row in data["risk_distribution"]:

            print(
                f"{row.get('risk_level', 'UNKNOWN'):<12} "
                f"{row.get('total', 0)}"
            )

        # -----------------------------------------------------
        # Entity Type Risk
        # -----------------------------------------------------

        print("\n" + "=" * 60)
        print("Risk By Entity Type")
        print("=" * 60)

        for row in data["risk_by_entity_type"]:

            print(
                f"{row.get('type', 'UNKNOWN'):<15} "
                f"Entities: "
                f"{row.get('total_entities', 0):<5} "
                f"Avg Risk: "
                f"{row.get('average_risk', 0.0):.4f} "
                f"Max Risk: "
                f"{row.get('maximum_risk', 0.0):.4f}"
            )

        # -----------------------------------------------------
        # High Risk
        # -----------------------------------------------------

        print("\n" + "=" * 60)
        print("HIGH / CRITICAL Risk Entities")
        print("=" * 60)

        for row in data["high_risk_entities"]:

            print(
                f"{row.get('entity', 'Unknown'):<30} "
                f"{row.get('type', 'Unknown'):<15} "
                f"Risk: "
                f"{row.get('risk_score', 0.0):.4f} "
                f"{row.get('risk_level', 'UNKNOWN')}"
            )

        print("\n" + "=" * 60)
        print("Risk Dashboard Backend Completed")
        print("=" * 60)

    except Exception as exc:

        logger.exception(
            "Risk dashboard backend failed."
        )

        print("\n" + "=" * 60)
        print("Risk Dashboard Backend Failed")
        print(f"Error: {exc}")
        print("=" * 60)

    finally:

        backend.close()


if __name__ == "__main__":
    main()
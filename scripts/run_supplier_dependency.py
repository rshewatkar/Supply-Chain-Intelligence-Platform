from app.analytics.supplier_dependency import (
    SupplierDependency,
)


def main():
    print("=" * 60)
    print("Supply Chain Intelligence Platform")
    print("Supplier Dependency Analysis")
    print("=" * 60)

    analyzer = SupplierDependency()

    try:
        result = analyzer.run()

        # =====================================================
        # Summary
        # =====================================================

        print()
        print("Supplier Dependency Summary")
        print("-" * 60)

        summary = result["summary"]

        print(
            f"Total Entities        : "
            f"{summary.get('total_entities', 0)}"
        )

        print(
            f"Very High Dependency  : "
            f"{summary.get('very_high_dependency', 0)}"
        )

        print(
            f"High Dependency       : "
            f"{summary.get('high_dependency', 0)}"
        )

        print(
            f"Medium Dependency     : "
            f"{summary.get('medium_dependency', 0)}"
        )

        print(
            f"Low Dependency        : "
            f"{summary.get('low_dependency', 0)}"
        )

        # =====================================================
        # Top Supplier-Dependent Entities
        # =====================================================

        print()
        print("Top Supplier-Dependent Entities")
        print("-" * 60)

        for entity in result["top_entities"]:
            print(
                f"{entity['name']:<30} "
                f"{str(entity.get('type', 'UNKNOWN')):<20} "
                f"Dependency: "
                f"{entity['supplier_dependency']:.4f}"
            )

        print()
        print("=" * 60)
        print("Supplier Dependency Completed Successfully")
        print("=" * 60)

    except Exception as exc:
        print()
        print("=" * 60)
        print("Supplier Dependency Failed")
        print("=" * 60)
        print(f"Error: {exc}")

        raise

    finally:
        analyzer.close()


if __name__ == "__main__":
    main()
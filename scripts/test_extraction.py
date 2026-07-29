from collections import Counter

from app.extraction.extraction_pipeline import (
    ExtractionPipeline,
)


def main():
    """
    Test the entity extraction pipeline.
    """

    pipeline = ExtractionPipeline()

    entities = pipeline.run()

    print("\n" + "=" * 60)
    print("Entity Extraction Results")
    print("=" * 60)

    print(f"\nTotal Entities : {len(entities)}")

    # -----------------------------------------------------
    # Count entities by type
    # -----------------------------------------------------

    counter = Counter(
        entity.entity_type
        for entity in entities
    )

    print("\nEntity Types")
    print("-" * 60)

    for entity_type, count in sorted(counter.items()):
        print(f"{entity_type:<15} : {count}")

    # -----------------------------------------------------
    # Display sample entities
    # -----------------------------------------------------

    print("\nSample Entities")
    print("-" * 60)

    for entity in entities[:10]:

        print(f"""
ID          : {entity.entity_id}
Entity      : {entity.name}
Type        : {entity.entity_type}
Company     : {entity.company}
Ticker      : {entity.ticker}
Document    : {entity.source_document}
Occurrences : {entity.occurrence_count}
""")

    print("=" * 60)
    print("Entity extraction test completed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()
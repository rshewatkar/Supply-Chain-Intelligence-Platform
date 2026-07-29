from app.extraction.extraction_pipeline import ExtractionPipeline


def main() -> None:
    """
    Run the relationship extraction pipeline.
    """

    pipeline = ExtractionPipeline()

    entities, relationships = pipeline.run()

    print("\n" + "=" * 60)
    print("Relationship Extraction Completed")
    print("=" * 60)
    print(f"Entities Extracted      : {len(entities)}")
    print(f"Relationships Extracted : {len(relationships)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
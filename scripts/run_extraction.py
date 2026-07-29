from app.extraction.extraction_pipeline import ExtractionPipeline


def main():
    """
    Run the entity extraction pipeline.
    """

    pipeline = ExtractionPipeline()

    entities = pipeline.run()

    print("\n" + "=" * 50)
    print("Entity Extraction Completed")
    print(f"Entities Extracted : {len(entities)}")
    print("=" * 50)


if __name__ == "__main__":
    main()
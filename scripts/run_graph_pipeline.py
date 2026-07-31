from app.graph.graph_pipeline import GraphPipeline


def main():
    """
    Execute the Neo4j graph ingestion pipeline.
    """

    print("\n" + "=" * 60)
    print("Supply Chain Intelligence Platform")
    print("Neo4j Graph Import")
    print("=" * 60)

    pipeline = GraphPipeline()

    try:
        pipeline.import_graph(
            clear_existing=True,
        )

        print("\n" + "=" * 60)
        print("Graph Import Completed Successfully")
        print("=" * 60)

    except Exception as error:

        print("\n" + "=" * 60)
        print("Graph Import Failed")
        print("=" * 60)

        print(f"\nError: {error}")


if __name__ == "__main__":
    main()
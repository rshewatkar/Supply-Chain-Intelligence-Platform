from app.graph.graph_analytics import GraphAnalytics


def print_separator():

    print("=" * 70)


def print_table(title, rows, score_column):

    print()
    print(title)
    print("-" * 70)

    print(
        f"{'Rank':<6}"
        f"{'Entity':<30}"
        f"{'Type':<20}"
        f"{score_column.capitalize():>12}"
    )

    print("-" * 70)

    for index, row in enumerate(rows, start=1):

        print(
            f"{index:<6}"
            f"{row['name']:<30}"
            f"{row['type']:<20}"
            f"{row[score_column]:>12.4f}"
        )


def main():

    analytics = GraphAnalytics()

    print_separator()
    print("Supply Chain Intelligence Platform")
    print("Graph Analytics")
    print_separator()

    try:

        if not analytics.neo4j.verify_connection():

            print("\nUnable to connect to Neo4j.")
            return

        # ---------------------------------------
        # Projection
        # ---------------------------------------

        analytics.create_projection()

        # ---------------------------------------
        # Degree
        # ---------------------------------------

        analytics.degree_centrality()

        # ---------------------------------------
        # Betweenness
        # ---------------------------------------

        analytics.betweenness_centrality()

        # ---------------------------------------
        # Results
        # ---------------------------------------

        degree = analytics.top_degree_nodes()

        betweenness = analytics.top_betweenness_nodes()

        print_table(
            "Top Degree Centrality",
            degree,
            "degree",
        )

        print()

        print_table(
            "Top Betweenness Centrality",
            betweenness,
            "betweenness",
        )

        # ---------------------------------------
        # Cleanup
        # ---------------------------------------

        analytics.drop_projection()

        print()
        print_separator()
        print("Graph Analytics Completed Successfully")
        print_separator()

    finally:

        analytics.close()


if __name__ == "__main__":

    main()
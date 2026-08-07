from app.analytics.graph_analytics import GraphAnalytics


def print_separator():
    print("=" * 60)


def main():

    analytics = GraphAnalytics()

    try:

        print_separator()
        print("Supply Chain Intelligence Platform")
        print("Graph Analytics")
        print_separator()

        # -------------------------------------------------
        # Create Projection
        # -------------------------------------------------

        analytics.create_projection()

        # -------------------------------------------------
        # Run Algorithms
        # -------------------------------------------------

        analytics.degree_centrality()

        analytics.betweenness_centrality()

        analytics.closeness_centrality()

        analytics.louvain_communities()

        # -------------------------------------------------
        # Degree Centrality
        # -------------------------------------------------

        print("\nTop Degree Nodes")
        print("-" * 60)

        for node in analytics.top_degree_nodes():

            print(
                f"{node['name']:<30}"
                f"{node['type']:<20}"
                f"{node['degree']}"
            )

        # -------------------------------------------------
        # Betweenness Centrality
        # -------------------------------------------------

        print("\nTop Betweenness Nodes")
        print("-" * 60)

        for node in analytics.top_betweenness_nodes():

            print(
                f"{node['name']:<30}"
                f"{node['type']:<20}"
                f"{node['betweenness']:.4f}"
            )

        # -------------------------------------------------
        # Closeness Centrality
        # -------------------------------------------------

        print("\nTop Closeness Nodes")
        print("-" * 60)

        for node in analytics.top_closeness_nodes():

            print(
                f"{node['name']:<30}"
                f"{node['type']:<20}"
                f"{node['closeness']:.4f}"
            )

        # -------------------------------------------------
        # Communities
        # -------------------------------------------------

        print("\nDetected Communities")
        print("-" * 60)

        for community in analytics.largest_communities():

            print(
                f"Community {community['community']:<5}"
                f"Nodes : {community['nodes']}"
            )

        # -------------------------------------------------
        # Cleanup
        # -------------------------------------------------

        analytics.drop_projection()

        analytics.close()

        print_separator()
        print("Graph Analytics Completed Successfully")
        print_separator()

    except Exception as error:

        print_separator() 
        print("Graph Analytics Failed")
        print_separator()

        print(f"\nError: {error}")

        try:
            analytics.close()
        except Exception:
            pass


if __name__ == "__main__":
        main()
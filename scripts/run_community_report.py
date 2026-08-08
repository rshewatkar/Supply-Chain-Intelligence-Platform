from app.analytics.community_report import CommunityReport


def print_section(title: str):
    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


def main():
    print("=" * 70)
    print("Supply Chain Intelligence Platform")
    print("Community Analytics Report")
    print("=" * 70)

    report = CommunityReport()

    try:
        # =================================================
        # Run Community Analytics
        # =================================================

        results = report.run()

        # =================================================
        # Community Summary
        # =================================================

        print_section("Community Summary")

        for row in results["summary"]:

            community = row["community"]
            node_count = row["node_count"]
            average_risk = row["average_risk"]
            maximum_risk = row["maximum_risk"]

            print(
                f"Community {community:<5} "
                f"Nodes: {node_count:<5} "
                f"Avg Risk: "
                f"{average_risk:.4f} "
                f"Max Risk: "
                f"{maximum_risk:.4f}"
            )

        # =================================================
        # Community Risk
        # =================================================

        print_section("Community Risk")

        for row in results["risk"]:

            community = row["community"]
            node_count = row["node_count"]
            average_risk = row["average_risk"]
            maximum_risk = row["maximum_risk"]
            critical_nodes = row["critical_nodes"]
            high_risk_nodes = row["high_risk_nodes"]

            print(
                f"Community {community:<5} "
                f"Nodes: {node_count:<5} "
                f"Avg Risk: {average_risk:.4f} "
                f"Max Risk: {maximum_risk:.4f} "
                f"Critical: {critical_nodes:<3} "
                f"High: {high_risk_nodes}"
            )

        # =================================================
        # Largest Communities
        # =================================================

        print_section("Largest Communities")

        for row in results["top_communities"]:

            community = row["community"]
            node_count = row["node_count"]
            average_degree = row["average_degree"]
            average_risk = row["average_risk"]

            print(
                f"Community {community:<5} "
                f"Nodes: {node_count:<5} "
                f"Avg Degree: {average_degree:.2f} "
                f"Avg Risk: {average_risk:.4f}"
            )

        # =================================================
        # Community Members
        # =================================================

        print_section("Community Members")

        communities = results["summary"]

        for community_row in communities:

            community_id = community_row["community"]

            print()
            print(f"Community {community_id}")
            print("-" * 70)

            members = report.community_members(
                community_id
            )

            for member in members:

                name = member["name"]
                entity_type = member["type"]
                degree = member["degree"]
                risk_score = member["risk_score"]
                risk_level = member["risk_level"]

                degree_value = (
                    f"{degree:.2f}"
                    if degree is not None
                    else "N/A"
                )

                risk_value = (
                    f"{risk_score:.4f}"
                    if risk_score is not None
                    else "N/A"
                )

                print(
                    f"{name:<30} "
                    f"{entity_type:<20} "
                    f"Degree: {degree_value:<8} "
                    f"Risk: {risk_value:<8} "
                    f"{risk_level}"
                )

        # =================================================
        # Highest Risk Entities by Community
        # =================================================

        print_section(
            "Highest Risk Entities by Community"
        )

        risk_entities = (
            report.highest_risk_entities_by_community(
                limit=5
            )
        )

        for row in risk_entities:

            community = row["community"]
            entities = row["entities"]

            print()
            print(f"Community {community}")
            print("-" * 70)

            for entity in entities:

                print(
                    f"{entity['name']:<30} "
                    f"{entity['type']:<20} "
                    f"Risk: "
                    f"{entity['risk_score']:.4f} "
                    f"{entity['risk_level']}"
                )

        # =================================================
        # Community Relationships
        # =================================================

        print_section(
            "Community Relationship Analysis"
        )

        for community_row in communities:

            community_id = community_row["community"]

            print()
            print(f"Community {community_id}")
            print("-" * 70)

            relationships = (
                report.community_relationships(
                    community_id
                )
            )

            if not relationships:

                print("No internal relationships found.")
                continue

            for relationship in relationships:

                relationship_type = (
                    relationship["relationship_type"]
                )

                relationship_count = (
                    relationship["relationship_count"]
                )

                print(
                    f"{relationship_type:<30} "
                    f"{relationship_count}"
                )

        # =================================================
        # Completed
        # =================================================

        print()
        print("=" * 70)
        print(
            "Community Analytics Report "
            "Completed Successfully"
        )
        print("=" * 70)

    except Exception as error:

        print()
        print("=" * 70)
        print("Community Analytics Report Failed")
        print("=" * 70)

        print(f"Error: {error}")

        raise

    finally:

        report.close()


if __name__ == "__main__":
    main()
from app.graph.neo4j_manager import Neo4jManager
print(Neo4jManager)
from app.config.settings import settings

print(settings.neo4j_uri)
print(settings.neo4j_username)
print(settings.neo4j_password)

def main():
    """
    Test Neo4j connection and basic database information.
    """

    manager = Neo4jManager()

    print("\n" + "=" * 60)
    print("Neo4j Connection Test")
    print("=" * 60)

    # -------------------------------------------------
    # Verify connection
    # -------------------------------------------------

    connected = manager.verify_connection()

    print(f"\nConnected : {connected}")

    if not connected:
        print("\nUnable to connect to Neo4j.")
        return

    # -------------------------------------------------
    # Database Information
    # -------------------------------------------------

    result = manager.execute_query(
        """
        CALL dbms.components()
        YIELD name, versions

        RETURN
            name,
            versions[0] AS version
        """
    )

    print("\nDatabase Information")
    print("-" * 60)

    for row in result:

        print(f"Database : {row['name']}")
        print(f"Version  : {row['version']}")

    # -------------------------------------------------
    # Create Constraints
    # -------------------------------------------------

    manager.create_constraints()

    print("\nConstraints created successfully.")

    # -------------------------------------------------
    # Graph Statistics
    # -------------------------------------------------

    print("\nCurrent Graph Statistics")
    print("-" * 60)

    print(
        f"Nodes          : {manager.count_nodes()}"
    )

    print(
        f"Relationships  : {manager.count_relationships()}"
    )

    # -------------------------------------------------
    # Close Connection
    # -------------------------------------------------

    manager.close()

    print("\n" + "=" * 60)
    print("Neo4j Test Completed Successfully")
    print("=" * 60)


if __name__ == "__main__":
    main()
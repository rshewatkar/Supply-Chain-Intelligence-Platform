from neo4j import GraphDatabase

URI = "neo4j://127.0.0.1:7687"
USERNAME = "neo4j"
PASSWORD = "SupplyChain@123"

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD),
)

try:
    driver.verify_connectivity()
    print("SUCCESS")
except Exception as e:
    print(type(e))
    print(e)

driver.close()
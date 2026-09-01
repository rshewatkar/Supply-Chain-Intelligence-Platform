from app.chat.graph_queries import GraphQueries

def main():
    graph = GraphQueries()
    try:
        print("--- Running Sample Graph Queries ---")
        # Example using a likely entity name
        entities = graph.find_entities("Apple")
        print(f"Entities found: {entities}")
        
        if entities:
            company = entities[0]['name']
            print(f"\nFetching suppliers for {company}...")
            suppliers = graph.get_suppliers(company)
            for s in suppliers:
                print(s)
                
    finally:
        graph.close()

if __name__ == "__main__":
    main()

from app.embeddings.search import SearchEngine

search = SearchEngine()

results = search.search(
    query="What products does Apple manufacture?",
    limit=5,
)

print("=" * 60)
print("Semantic Search Results")
print("=" * 60)

for index, result in enumerate(results, start=1):

    print(f"\nResult {index}")
    print("-" * 60)
    print(f"Score     : {result['score']:.4f}")
    print(f"Company   : {result['company']}")
    print(f"Ticker    : {result['ticker']}")
    print(f"Document  : {result['document_type']}")
    print(f"File      : {result['file_name']}")
    print(f"Chunk     : {result['chunk_index']}")
    print()
    print(result["text"][:350])
import sys
from app.ingestion.document_loader import DocumentLoader

loader = DocumentLoader(
    "data/raw/metadata/metadata.csv"
)

documents = loader.load_documents()

print(f"Loaded {len(documents)} documents")

print(documents[0].keys())

print(documents[0]["company"])

print(documents[0]["document_type"])

print(documents[0]["pages"])
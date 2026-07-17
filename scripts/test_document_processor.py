from app.ingestion.document_loader import DocumentLoader
from app.preprocessing.document_processor import DocumentProcessor

loader = DocumentLoader("data/raw/metadata/metadata.csv")

documents = loader.load_documents()

processed = DocumentProcessor.process(documents[0])

print(type(processed))

print(processed.company)

print(processed.word_count)

print(processed.character_count)

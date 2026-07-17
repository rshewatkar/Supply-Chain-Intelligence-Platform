from pathlib import Path
import json

from app.ingestion.document_loader import DocumentLoader
from app.preprocessing.document_processor import DocumentProcessor


class ProcessorPipeline:
    """Run the preprocessing pipeline."""

    def __init__(self, metadata_path: str):
        self.loader = DocumentLoader(metadata_path)

    def run(self):
        documents = self.loader.load_documents()

        processed_documents = []

        for document in documents:
            processed = DocumentProcessor.process(document)
            processed_documents.append(processed)

        output_dir = Path("data/processed")
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / "processed_documents.json"

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(
                [doc.model_dump() for doc in processed_documents],
                f,
                indent=4,
                ensure_ascii=False,
            )

        print("=" * 50)
        print("Document Processing Completed")
        print("=" * 50)
        print(f"Processed Documents : {len(processed_documents)}")
        print(f"Output File         : {output_file}")
        print("=" * 50)

        return processed_documents
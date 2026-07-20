from pathlib import Path
import json

from app.chunking.chunker import Chunker
from app.models.processed_document import ProcessedDocument


class ChunkPipeline:
    """Generate semantic chunks from processed documents."""

    def __init__(self):

        self.chunker = Chunker()

    def run(
        self,
        input_file: str = "data/processed/processed_documents.json",
        output_file: str = "data/processed/chunks.json",
    ):

        input_path = Path(input_file)

        with open(input_path, "r", encoding="utf-8") as f:
            documents_json = json.load(f)

        documents = [
            ProcessedDocument(**doc)
            for doc in documents_json
        ]

        all_chunks = []

        for document in documents:

            chunks = self.chunker.split(document)

            all_chunks.extend(chunks)

        output_path = Path(output_file)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(output_path, "w", encoding="utf-8") as f:

            json.dump(
                [chunk.model_dump() for chunk in all_chunks],
                f,
                indent=4,
                ensure_ascii=False,
            )

        print("=" * 50)
        print("Chunk Generation Completed")
        print("=" * 50)
        print(f"Documents : {len(documents)}")
        print(f"Chunks    : {len(all_chunks)}")
        print(f"Saved To  : {output_path}")
        print("=" * 50)

        return all_chunks
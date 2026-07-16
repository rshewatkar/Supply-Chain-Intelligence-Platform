from pathlib import Path

import pandas as pd

from app.ingestion.pdf_loader import PDFLoader


class DocumentLoader:
    """Load every document listed in metadata.csv."""

    def __init__(self, metadata_path: str):
        self.metadata_path = Path(metadata_path)
        self.pdf_loader = PDFLoader()

    def load_documents(self):

        metadata = pd.read_csv(self.metadata_path)

        documents = []

        for _, row in metadata.iterrows():

            pdf = self.pdf_loader.load(row["file_path"])

            pdf["company"] = row["company"]
            pdf["document_type"] = row["document_type"]
            pdf["ticker"] = row["ticker"]
            pdf["industry"] = row["industry"]
            pdf["country"] = row["country"]

            documents.append(pdf)

        return documents
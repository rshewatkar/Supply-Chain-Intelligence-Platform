from pathlib import Path

import pandas as pd

from app.ingestion.pdf_loader import PDFLoader
from app.models.document import Document

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
    
            document = Document(
                company=row["company"],
                ticker=row["ticker"],
                industry=row["industry"],
                country=row["country"],
                document_type=row["document_type"],
                file_name=pdf["file_name"],
                file_path=pdf["file_path"],
                pages=pdf["pages"],
                text=pdf["text"],
                metadata=pdf["metadata"],
            )
    
            documents.append(document)
    
        return documents
from app.models.document import Document
from app.models.processed_document import ProcessedDocument
from app.preprocessing.text_cleaner import TextCleaner


class DocumentProcessor:
    """Process raw documents into cleaned documents."""

    @staticmethod
    def process(document: Document) -> ProcessedDocument:
        """
        Clean the document text and compute statistics.

        Parameters
        ----------
        document : Document

        Returns
        -------
        ProcessedDocument
        """

        cleaned_text = TextCleaner.clean_text(document.text)

        word_count = len(cleaned_text.split())

        character_count = len(cleaned_text)

        return ProcessedDocument(
            company=document.company,
            ticker=document.ticker,
            industry=document.industry,
            country=document.country,
            document_type=document.document_type,
            file_name=document.file_name,
            pages=document.pages,
            text=cleaned_text,
            word_count=word_count,
            character_count=character_count,
            metadata=document.metadata,
        )
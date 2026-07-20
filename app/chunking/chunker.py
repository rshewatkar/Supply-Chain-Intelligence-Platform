from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.models.chunk import Chunk
from app.models.processed_document import ProcessedDocument


class Chunker:
    """Split processed documents into semantic chunks."""

    def __init__(
        self,
        chunk_size: int = 1200,
        chunk_overlap: int = 200,
    ):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def split(
        self,
        document: ProcessedDocument,
    ) -> list[Chunk]:

        texts = self.splitter.split_text(document.text)

        chunks = []

        for index, text in enumerate(texts):

            chunks.append(
                Chunk(
                    chunk_id=f"{document.ticker}_{index + 1:04}",
                    company=document.company,
                    ticker=document.ticker,
                    document_type=document.document_type,
                    file_name=document.file_name,
                    chunk_index=index,
                    text=text,
                    word_count=len(text.split()),
                    character_count=len(text),
                    page_count=document.pages,
                )
            )

        return chunks
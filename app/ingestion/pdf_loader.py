from pathlib import Path

import fitz  # PyMuPDF


class PDFLoader:
    """Load and extract text from a PDF document."""

    def load(self, pdf_path: str) -> dict:
        pdf_path = Path(pdf_path)

        if not pdf_path.exists():
            raise FileNotFoundError(f"{pdf_path} does not exist.")

        document = fitz.open(pdf_path)

        text = []

        for page in document:
            text.append(page.get_text())

        metadata = document.metadata

        result = {
            "file_name": pdf_path.name,
            "file_path": str(pdf_path),
            "pages": len(document),
            "text": "\n".join(text),
            "metadata": metadata,
        }

        document.close()

        return result
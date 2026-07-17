import re


class TextCleaner:
    """Utility class for cleaning extracted document text."""

    @staticmethod
    def normalize_newlines(text: str) -> str:
        """Replace multiple newlines with a single newline."""
        return re.sub(r"\n{2,}", "\n", text)

    @staticmethod
    def remove_extra_spaces(text: str) -> str:
        """Replace multiple spaces or tabs with a single space."""
        return re.sub(r"[ \t]+", " ", text)

    @staticmethod
    def remove_empty_lines(text: str) -> str:
        """Remove blank lines."""
        lines = [line.strip() for line in text.splitlines()]
        lines = [line for line in lines if line]
        return "\n".join(lines)

    @staticmethod
    def clean_text(text: str) -> str:
        """Run the complete cleaning pipeline."""

        text = TextCleaner.normalize_newlines(text)
        text = TextCleaner.remove_extra_spaces(text)
        text = TextCleaner.remove_empty_lines(text)

        return text.strip()
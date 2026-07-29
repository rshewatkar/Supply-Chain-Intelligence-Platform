import re
from collections import Counter

from app.extraction.patterns import (
    COMPANIES,
    COUNTRIES,
    INDUSTRIES,
    PRODUCTS,
    TECHNOLOGIES,
)
from app.models.entity import Entity
from app.models.processed_document import ProcessedDocument
from app.utils.helpers import generate_uuid


class EntityExtractor:
    """
    Rule-based entity extractor.

    Extracts entities from a processed document using
    predefined dictionaries.
    """

    def __init__(self):
        """
        Initialize the extractor.
        """

        self.entity_patterns = {
            "COMPANY": COMPANIES,
            "PRODUCT": PRODUCTS,
            "COUNTRY": COUNTRIES,
            "INDUSTRY": INDUSTRIES,
            "TECHNOLOGY": TECHNOLOGIES,
        }

    def extract(
        self,
        document: ProcessedDocument,
    ) -> list[Entity]:
        """
        Extract entities from one processed document.

        Parameters
        ----------
        document : ProcessedDocument

        Returns
        -------
        list[Entity]
        """

        entities = []
        seen = set()

        for entity_type, values in self.entity_patterns.items():

            counter = Counter()

            for value in values:

                occurrences = len(
                    re.findall(
                        rf"\b{re.escape(value)}\b",
                        document.text,
                        flags=re.IGNORECASE,
                    )
                )

                if occurrences == 0:
                    continue

                counter[value] = occurrences

            for name, count in counter.items():

                key = (
                    entity_type,
                    name.lower(),
                )

                if key in seen:
                    continue

                seen.add(key)

                entities.append(
                    Entity(
                        entity_id=generate_uuid(),
                        name=name,
                        entity_type=entity_type,
                        company=document.company,
                        ticker=document.ticker,
                        source_document=document.document_type,
                        file_name=document.file_name,
                        confidence=1.0,
                        occurrence_count=count,
                    )
                )

        entities.sort(
            key=lambda entity: (
                entity.entity_type,
                entity.name,
            )
        )

        return entities
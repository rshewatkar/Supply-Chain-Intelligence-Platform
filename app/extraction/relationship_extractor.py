import re
from collections import Counter

from app.extraction.relationship_patterns import (
    RELATIONSHIP_PATTERNS,
)
from app.models.entity import Entity
from app.models.processed_document import ProcessedDocument
from app.models.relationship import Relationship
from app.utils.helpers import generate_uuid


class RelationshipExtractor:
    """
    Rule-based relationship extractor.

    Relationships are detected when two extracted
    entities appear in the same sentence together
    with a known relationship keyword.
    """

    def __init__(self):

        self.relationship_patterns = (
            RELATIONSHIP_PATTERNS
        )

    def extract(
        self,
        document: ProcessedDocument,
        entities: list[Entity],
    ) -> list[Relationship]:
        """
        Extract relationships from one document.

        Parameters
        ----------
        document : ProcessedDocument

        entities : list[Entity]

        Returns
        -------
        list[Relationship]
        """

        relationship_map = {}

        seen = set()

        # ----------------------------------------
        # Split into sentences
        # ----------------------------------------

        sentences = re.split(
            r"[.!?]\s+",
            document.text,
        )

        # ----------------------------------------
        # Process every sentence
        # ----------------------------------------

        for sentence in sentences:

            sentence_lower = sentence.lower()

            sentence_entities = []

            # Find entities occurring
            # inside this sentence

            for entity in entities:

                if entity.name.lower() in sentence_lower:

                    sentence_entities.append(entity)

            # Need at least two entities

            if len(sentence_entities) < 2:
                continue

            # ------------------------------------
            # Detect relationship
            # ------------------------------------

            for (
                relationship_type,
                keywords,
            ) in self.relationship_patterns.items():

                occurrences = Counter()

                for keyword in keywords:

                    if keyword.lower() in sentence_lower:

                        occurrences[keyword] += 1

                if not occurrences:
                    continue

                # --------------------------------
                # Create pairwise relationships
                # --------------------------------

                for i in range(
                    len(sentence_entities)
                ):

                    for j in range(
                        i + 1,
                        len(sentence_entities),
                    ):

                        source = sentence_entities[i]

                        target = sentence_entities[j]

                        key = (
                            source.entity_id,
                            target.entity_id,
                            relationship_type,
                            sentence,
                        )

                        if key in seen:
                            continue

                        seen.add(key)        
        
                        relationship_key = (
                            source.entity_id,
                            target.entity_id,
                            relationship_type,
                        )
                        
                        if relationship_key not in relationship_map:
                        
                            relationship_map[relationship_key] = Relationship(
                        
                                relationship_id=generate_uuid(),
                        
                                source_entity_id=source.entity_id,
                                source_entity_name=source.name,
                                source_entity_type=source.entity_type,
                        
                                target_entity_id=target.entity_id,
                                target_entity_name=target.name,
                                target_entity_type=target.entity_type,
                        
                                relationship_type=relationship_type,
                        
                                company=document.company,
                                ticker=document.ticker,
                        
                                source_document=document.document_type,
                                file_name=document.file_name,
                        
                                confidence=1.0,
                                occurrence_count=0,
                            )
                        
                        relationship_map[
                            relationship_key
                        ].occurrence_count += sum(
                            occurrences.values()
                        )
                        
        relationships = list(
            relationship_map.values()
        )
        
        relationships.sort(
            key=lambda r: (
                r.source_entity_name,
                r.relationship_type,
                r.target_entity_name,
            )
        )
        
        return relationships            

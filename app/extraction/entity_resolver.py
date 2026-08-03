from collections import defaultdict

from app.models.entity import Entity
from app.models.relationship import Relationship
from app.utils.logger import get_logger

logger = get_logger(__name__)

class EntityResolver:
    """
    Resolver duplicate entities extracted from muliple documents.
    
    Example
    _____________
    AMD( annual report)
    AMD(Wikipedia)
            ⬇️
    One canonical AMD node.       
    
    """
    def resolve(self, entities, relationships):
        """
        Resolve duplicate entities and update
        relationship references.

        Returns
        -------
        unique_entities,
        updated_relationships
        """

        logger.info(
            "Resolving duplicate entities..."
        )

        groups = defaultdict(list)

        # ------------------------------------
        # Group by (name, entity_type)
        # ------------------------------------

        for entity in entities:

            key = (
                entity.name.strip().lower(),
                entity.entity_type,
            )

            groups[key].append(entity)

        unique_entities = []

        entity_mapping = {}

        # ------------------------------------
        # Choose canonical entity
        # ------------------------------------

        for duplicates in groups.values():

            canonical = max(
                duplicates,
                key=lambda entity: entity.occurrence_count,
            )

            unique_entities.append(canonical)

            for entity in duplicates:

                entity_mapping[
                    entity.entity_id
                ] = canonical.entity_id

        logger.info(
            "Merged %s entities into %s canonical entities.",
            len(entities),
            len(unique_entities),
        )

        # ------------------------------------
        # Update relationships
        # ------------------------------------

        for relationship in relationships:

            relationship.source_entity_id = (
                entity_mapping[
                    relationship.source_entity_id
                ]
            )

            relationship.target_entity_id = (
                entity_mapping[
                    relationship.target_entity_id
                ]
            )

        logger.info(
            "Updated relationship entity IDs."
        )

        return (
            unique_entities,
            relationships,
        )
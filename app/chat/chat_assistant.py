from app.chat.question_router import QuestionRouter
from app.chat.graph_queries import GraphQueries
from app.utils.logger import get_logger


logger = get_logger(__name__)


class ChatAssistant:
    """
    AI Supply Chain Chat Assistant.

    Routes user questions to the appropriate graph query
    and formats the results into readable answers.
    """

    def __init__(self):
        self.router = QuestionRouter()
        self.graph_queries = GraphQueries()

    # =====================================================
    # Main Chat Method
    # =====================================================

    def ask(self, question: str) -> dict:
        """
        Process a user question and return an answer.

        Parameters
        ----------
        question : str
            User's supply-chain question.

        Returns
        -------
        dict
            Intent, answer, and supporting data.
        """

        if not question or not question.strip():
            return {
                "intent": "UNKNOWN",
                "answer": "Please enter a valid question.",
                "data": [],
            }

        question = question.strip()

        logger.info(
            "Processing user question: %s",
            question,
        )

        intent = self.router.route(
            question
        )

        logger.info(
            "Detected intent: %s",
            intent,
        )

        try:

            # Use lowercase for intent comparisons
            if intent["intent"] == "supplier":
                return self._handle_supplier_question(
                    question,
                    intent["intent"],
                )

            if intent["intent"] == "common_supplier":
                return self._handle_common_supplier_question(
                    question,
                    intent["intent"],
                )

            if intent["intent"] == "dependency":
                return self._handle_dependency_question(
                    question,
                    intent["intent"],
                )

            if intent["intent"] == "tier":
                return self._handle_tier_question(
                    question,
                    intent["intent"],
                )

            return self._handle_supply_chain_question(
                question,
                intent,
            )

        except Exception:

            logger.exception(
                "Chat assistant failed to process question."
            )

            return {
                "intent": intent,
                "answer": (
                    "Sorry, I could not process "
                    "your question."
                ),
                "data": [],
            }

    # =====================================================
    # Supplier Questions
    # =====================================================

    def _handle_supplier_question(
        self,
        question: str,
        intent: str,
    ) -> dict:

        # Simple extraction: iterate through common known companies to see if they are in the string.
        from app.extraction.patterns import COMPANIES
        
        company = None
        for c in COMPANIES:
            if c.lower() in question.lower():
                company = c
                break
        
        if not company:
            # Fallback to current behavior
            entities = self.graph_queries.find_entities(question)
            if not entities:
                 return {
                    "intent": intent,
                    "answer": (
                        "I could not identify the company "
                        "in your question."
                    ),
                    "data": [],
                }
            company = entities[0]["name"]
        
        # Now query using the identified company
        suppliers = self.graph_queries.get_suppliers(company)

        if not suppliers:
            return {
                "intent": intent,
                "entity": company,
                "answer": (
                    f"I found {company}, but no suppliers "
                    f"are currently recorded."
                ),
                "data": [],
            }

        supplier_names = [s["supplier"] for s in suppliers]
        answer = (
            f"Suppliers for {company} include: "
            f"{', '.join(supplier_names)}."
        )

        return {
            "intent": intent,
            "entity": company,
            "answer": answer,
            "data": suppliers,
        }

        answer = (
            f"The supply-chain relationships for "
            f"{company} include: "
            f"{', '.join(supplier_names)}."
        )

        return {
            "intent": intent,
            "entity": company,
            "answer": answer,
            "data": suppliers,
        }

    # =====================================================
    # Common Supplier Questions
    # =====================================================

    def _handle_common_supplier_question(
        self,
        question: str,
        intent: str,
    ) -> dict:

        entities = self.graph_queries.find_entities(
            question
        )

        companies = [
            entity["name"]
            for entity in entities
            if entity.get("entity_type") == "COMPANY"
        ]

        if len(companies) < 2:
            return {
                "intent": intent,
                "answer": (
                    "Please mention at least two "
                    "companies to compare suppliers."
                ),
                "data": [],
            }

        common_suppliers = (
            self.graph_queries.get_common_suppliers(
                companies[0],
                companies[1],
            )
        )

        if not common_suppliers:
            return {
                "intent": intent,
                "answer": (
                    f"I could not find common suppliers "
                    f"between {companies[0]} and "
                    f"{companies[1]}."
                ),
                "data": [],
            }

        supplier_names = [
            supplier["supplier"]
            for supplier in common_suppliers
        ]

        answer = (
            f"Common suppliers between "
            f"{companies[0]} and {companies[1]} "
            f"include: {', '.join(supplier_names)}."
        )

        return {
            "intent": intent,
            "entities": companies[:2],
            "answer": answer,
            "data": common_suppliers,
        }

    # =====================================================
    # Dependency Questions
    # =====================================================

    def _handle_dependency_question(
        self,
        question: str,
        intent: str,
    ) -> dict:

        entities = self.graph_queries.find_entities(
            question
        )

        if not entities:
            return {
                "intent": intent,
                "answer": (
                    "I could not identify the company "
                    "for dependency analysis."
                ),
                "data": [],
            }

        company = entities[0]["name"]

        metrics = (
            self.graph_queries.get_dependency_metrics(
                company
            )
        )

        if not metrics:
            return {
                "intent": intent,
                "answer": (
                    f"No dependency metrics were found "
                    f"for {company}."
                ),
                "data": [],
            }

        metric = metrics[0]

        risk_score = metric.get(
            "risk_score"
        )

        risk_level = metric.get(
            "risk_level"
        )

        answer = (
            f"Dependency analysis for {company}: "
            f"Tier-1 dependency is "
            f"{self._format_metric(metric.get('tier1_dependency'))}, "
            f"Tier-2 dependency is "
            f"{self._format_metric(metric.get('tier2_dependency'))}, "
            f"and supplier dependency is "
            f"{self._format_metric(metric.get('supplier_dependency'))}."
        )

        if risk_score is not None:
            answer += (
                f" The overall risk score is "
                f"{risk_score:.4f}"
            )

        if risk_level:
            answer += (
                f" with a {risk_level} risk level."
            )

        return {
            "intent": intent,
            "entity": company,
            "answer": answer,
            "data": metrics,
        }

    # =====================================================
    # Tier Questions
    # =====================================================

    def _handle_tier_question(
        self,
        question: str,
        intent: str,
    ) -> dict:

        entities = self.graph_queries.find_entities(
            question
        )

        if not entities:
            return {
                "intent": intent,
                "answer": (
                    "I could not identify the company "
                    "for tier analysis."
                ),
                "data": [],
            }

        company = entities[0]["name"]

        tier2_dependencies = (
            self.graph_queries.get_tier2_dependencies(
                company
            )
        )

        if not tier2_dependencies:
            return {
                "intent": intent,
                "answer": (
                    f"I could not find Tier-2 "
                    f"dependencies for {company}."
                ),
                "data": [],
            }

        dependency_names = []

        for dependency in tier2_dependencies:

            name = dependency.get(
                "tier2_supplier"
            )

            if name and name not in dependency_names:
                dependency_names.append(name)

        if dependency_names:
            answer = (
                f"Tier-2 dependencies for {company} "
                f"include: "
                f"{', '.join(dependency_names)}."
            )
        else:
            answer = (
                f"Tier-2 dependency relationships "
                f"were found for {company}."
            )

        return {
            "intent": intent,
            "entity": company,
            "answer": answer,
            "data": tier2_dependencies,
        }

    # =====================================================
    # General Supply Chain Questions
    # =====================================================

    def _handle_supply_chain_question(
        self,
        question: str,
        intent: str,
    ) -> dict:

        entities = self.graph_queries.find_entities(
            question
        )

        if not entities:
            return {
                "intent": intent,
                "answer": (
                    "I could not identify relevant "
                    "supply-chain entities in your question."
                ),
                "data": [],
            }

        entity = entities[0]["name"]

        relationships = (
            self.graph_queries.get_supply_chain_relationships(
                entity
            )
        )

        if not relationships:
            return {
                "intent": intent,
                "entity": entity,
                "answer": (
                    f"I found {entity}, but no supply-chain "
                    f"relationships are currently available."
                ),
                "data": [],
            }

        related_entities = []

        for relationship in relationships:

            name = relationship.get(
                "related_entity"
            )

            if name and name not in related_entities:
                related_entities.append(name)

        answer = (
            f"{entity} is connected in the supply-chain "
            f"knowledge graph with entities including: "
            f"{', '.join(related_entities[:10])}."
        )

        return {
            "intent": intent,
            "entity": entity,
            "answer": answer,
            "data": relationships,
        }

    # =====================================================
    # Helper Methods
    # =====================================================

    @staticmethod
    def _format_metric(value):
        """
        Format dependency metrics safely.
        """

        if value is None:
            return "not available"

        return f"{value:.4f}"

    # =====================================================
    # Close Connection
    # =====================================================

    def close(self):
        """
        Close underlying graph database connection.
        """

        logger.info(
            "Closing ChatAssistant connection."
        )

        self.graph_queries.close()
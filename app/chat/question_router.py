import re

from app.utils.logger import get_logger


logger = get_logger(__name__)


class QuestionRouter:
    """
    Classify supply-chain questions into supported intents.

    Supported intents:

    - supplier
    - common_supplier
    - dependency
    - tier
    - general
    """

    SUPPLIER_INTENT = "supplier"
    COMMON_SUPPLIER_INTENT = "common_supplier"
    DEPENDENCY_INTENT = "dependency"
    TIER_INTENT = "tier"
    GENERAL_INTENT = "general"

    def route(self, question: str) -> str:
        """
        Detect the intent of a user question.

        Parameters
        ----------
        question : str
            User question.

        Returns
        -------
        str
            Detected question intent.
        """

        if not question or not question.strip():
            logger.warning(
                "Empty question received by QuestionRouter."
            )

            return self.GENERAL_INTENT

        normalized_question = (
            question.lower().strip()
        )

        logger.info(
            "Routing question: %s",
            question,
        )

        # =================================================
        # Common Supplier Intent
        # =================================================

        if self._is_common_supplier_question(
            normalized_question
        ):
            intent = self.COMMON_SUPPLIER_INTENT

        # =================================================
        # Tier Intent
        # =================================================

        elif self._is_tier_question(
            normalized_question
        ):
            intent = self.TIER_INTENT

        # =================================================
        # Dependency Intent
        # =================================================

        elif self._is_dependency_question(
            normalized_question
        ):
            intent = self.DEPENDENCY_INTENT

        # =================================================
        # Supplier Intent
        # =================================================

        elif self._is_supplier_question(
            normalized_question
        ):
            intent = self.SUPPLIER_INTENT

        # =================================================
        # General Intent
        # =================================================

        else:
            intent = self.GENERAL_INTENT

        logger.info(
            "Question classified as intent: %s",
            intent,
        )

        return intent

    # =====================================================
    # Common Supplier Detection
    # =====================================================

    def _is_common_supplier_question(
        self,
        question: str,
    ) -> bool:
        """
        Detect questions about suppliers shared
        across multiple companies.
        """

        patterns = [
            r"\bcommon suppliers?\b",
            r"\bshared suppliers?\b",
            r"\bwhich suppliers? are common\b",
            r"\bsuppliers? in common\b",
            r"\bsame suppliers?\b",
            r"\bmutual suppliers?\b",
        ]

        return self._matches_any(
            question,
            patterns,
        )

    # =====================================================
    # Tier Detection
    # =====================================================

    def _is_tier_question(
        self,
        question: str,
    ) -> bool:
        """
        Detect Tier-1 and Tier-2 dependency questions.
        """

        patterns = [
            r"\btier[- ]?1\b",
            r"\btier[- ]?2\b",
            r"\btier one\b",
            r"\btier two\b",
            r"\bfirst[- ]?tier\b",
            r"\bsecond[- ]?tier\b",
            r"\bdirect dependencies?\b",
            r"\bindirect dependencies?\b",
            r"\btwo[- ]?hop\b",
        ]

        return self._matches_any(
            question,
            patterns,
        )

    # =====================================================
    # Dependency Detection
    # =====================================================

    def _is_dependency_question(
        self,
        question: str,
    ) -> bool:
        """
        Detect questions related to dependency
        metrics and dependency risk.
        """

        patterns = [
            r"\bhighest dependency\b",
            r"\bdependency score\b",
            r"\bdependency metrics?\b",
            r"\bsupplier dependency\b",
            r"\bcountry dependency\b",
            r"\bdependency risk\b",
            r"\bmost dependent\b",
            r"\bdependency\b",
        ]

        return self._matches_any(
            question,
            patterns,
        )

    # =====================================================
    # Supplier Detection
    # =====================================================

    def _is_supplier_question(
        self,
        question: str,
    ) -> bool:
        """
        Detect direct supplier questions.
        """

        patterns = [
            r"\bwho supplies\b",
            r"\bwho are .* suppliers?\b",
            r"\bsuppliers? of\b",
            r"\bsupplier for\b",
            r"\bsupply .* company\b",
            r"\bwho provides\b",
        ]

        return self._matches_any(
            question,
            patterns,
        )

    # =====================================================
    # Pattern Matching Helper
    # =====================================================

    @staticmethod
    def _matches_any(
        question: str,
        patterns: list[str],
    ) -> bool:
        """
        Return True when the question matches
        at least one regex pattern.
        """

        return any(
            re.search(
                pattern,
                question,
            )
            for pattern in patterns
        )
"""
Prompt templates for the Supply Chain Intelligence RAG pipeline.
"""

from app.utils.logger import get_logger


logger = get_logger(__name__)


class PromptBuilder:
    """
    Build prompts for the Supply Chain Intelligence LLM.
    """

    SYSTEM_PROMPT = """
You are the Supply Chain Intelligence Assistant.

Your job is to answer questions about companies,
suppliers, products, technologies, countries,
industries, and supply-chain relationships.

Use ONLY the information provided in the context.

Rules:
1. Do not invent or assume information.
2. If the context does not contain enough information,
   clearly say that the information is not available.
3. Give a concise and factual answer.
4. When possible, mention the company or document
   supporting the answer.
5. Distinguish facts from uncertainty.
""".strip()

    USER_PROMPT_TEMPLATE = """
Context:

{context}


Question:

{question}


Answer:
""".strip()

    def build(
        self,
        question: str,
        context: str,
    ) -> str:
        """
        Build the complete prompt for the LLM.
        """

        if not question or not question.strip():
            raise ValueError("Question cannot be empty.")

        if not context or not context.strip():
            raise ValueError("Context cannot be empty.")

        prompt = self.SYSTEM_PROMPT + "\n\n"

        prompt += self.USER_PROMPT_TEMPLATE.format(
            context=context.strip(),
            question=question.strip(),
        )

        logger.info(
            "RAG prompt created successfully."
        )

        return prompt

    def get_system_prompt(self) -> str:
        """
        Return the system instructions.
        """

        return self.SYSTEM_PROMPT
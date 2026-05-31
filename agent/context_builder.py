# agent/context_builder.py

from typing import List, Dict, Any


class ContextBuilder:
    """
    Builds conversation context from short-term memory (STM).
    """

    def __init__(self, stm, ltm=None, summarizer=None):
        self.stm = stm
        self.ltm = ltm
        self.summarizer = summarizer

    def build(self) -> str:
        """
        Returns a plain-text conversation history from STM.
        """
        messages = self.stm.get()
        lines = []

        for msg in messages:
            role = msg.get("role", "user").capitalize()
            content = msg.get("content", "")
            lines.append(f"{role}: {content}")

        return "\n".join(lines)

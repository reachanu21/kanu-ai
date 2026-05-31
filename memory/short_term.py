# memory/short_term.py

from typing import List, Dict, Any


class ShortTermMemory:
    """
    Simple in-memory conversation buffer.
    Stores the last N messages.
    """

    def __init__(self, max_messages: int = 20):
        self.max_messages = max_messages
        self.messages: List[Dict[str, Any]] = []

    def add(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages :]

    def get(self) -> List[Dict[str, Any]]:
        return list(self.messages)

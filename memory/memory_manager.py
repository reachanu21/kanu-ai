import random
import re
from typing import List, Dict, Any


class MemoryManager:
    """
    Unified interface for STM + LTM + preference extraction + habits.
    Assistant should only talk to this class.
    """

    def __init__(self, stm, ltm, extractor, summarizer=None, settings=None):
        self.stm = stm
        self.ltm = ltm
        self.extractor = extractor
        self.summarizer = summarizer
        self.settings = settings or {}

    # ----------------------------------------------------
    # Public API
    # ----------------------------------------------------
    def add_message(self, role: str, content: str):
        # 1) Always store in STM
        self.stm.add(role, content)

        # 2) Only learn from user messages
        if role == "user":
            self._learn_preferences(content)
            self._infer_habits(content)

            # 3) Occasionally decay LTM (settings-aware)
            if random.random() < 0.1:
                self.ltm.decay(
                    half_life_days=self.settings.get("half_life_days", 30),
                    threshold=self.settings.get("threshold", 0.25)
                )

    def get_context(self):
        return self.stm.get()

    def summarize(self) -> str:
        return self.ltm.summarize()

    # ----------------------------------------------------
    # Forget API
    # ----------------------------------------------------
    def forget(self, target: str):
        """
        Forget entries whose key or value contains the target substring (case-insensitive).
        """
        self.ltm.forget(target)

    # ----------------------------------------------------
    # Internal helpers
    # ----------------------------------------------------
    def _learn_preferences(self, content: str):
        prefs = self.extractor.extract(content)

        # Normalize to list
        if isinstance(prefs, dict):
            prefs = [prefs]

        for item in prefs:
            if not item.get("is_preference"):
                continue

            confidence = item.get("confidence", 0.0)
            if confidence < 0.65:
                continue  # too uncertain

            category = item.get("category", "preferences") or "preferences"
            key = (item.get("key") or "").strip()
            value = (item.get("value") or "").strip()

            if key and value:
                self.ltm.update(category, key, value, confidence=confidence)

    def _infer_habits(self, content: str):
        """
        Very simple habit inference:
        - Look for phrases like "every day", "usually", "always", "I tend to"
        - Store them as habits with low confidence (they'll strengthen if repeated)
        """
        text = content.lower
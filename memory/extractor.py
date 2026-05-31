import json
from utility.safe_json import safe_json_parse


class PreferenceExtractor:
    """
    Extracts long-term preferences, profile details, habits, and health info
    from user messages using an LLM.

    Returns a LIST of preference objects:
    [
        {
            "is_preference": true,
            "confidence": 0.92,
            "category": "preferences",
            "key": "favorite_color",
            "value": "blue"
        },
        ...
    ]
    """

    def __init__(self, llm):
        self.llm = llm

    def extract(self, message: str):
        prompt = f"""
You are a preference extraction model.

Extract ALL long-term preferences, personal facts, habits, health info,
or profile details from the user's message.

Respond ONLY in valid JSON as a list of objects.

Each object must follow this schema:

{{
  "is_preference": true or false,
  "confidence": number between 0 and 1,
  "category": "preferences" | "profile" | "habits" | "health" | "other",
  "key": "a short snake_case key",
  "value": "the extracted value as a short string"
}}

Rules:
- If the message contains multiple preferences, return multiple objects.
- If the message contains NO preferences, return an empty list [].
- "confidence" reflects how certain you are (0 = guessing, 1 = certain).
- Do NOT include explanations. Only JSON.

User message: "{message}"
"""

        raw = self.llm.generate(prompt, temperature=0.2)
        prefs = safe_json_parse(raw)

        # Normalize output
        if prefs is None:
            return []

        if isinstance(prefs, dict):
            return [prefs]

        if isinstance(prefs, list):
            return prefs

        return []

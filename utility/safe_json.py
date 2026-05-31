# utility/safe_json.py

import json
from typing import Any, Optional


def safe_json_parse(text: str) -> Optional[Any]:
    """
    Best-effort JSON parsing:
    - tries full string
    - then tries to extract the first JSON array or object
    - returns None on failure
    """
    if not text:
        return None

    text = text.strip()

    # First attempt: direct parse
    try:
        return json.loads(text)
    except Exception:
        pass

    # Try to find first JSON array or object
    start_indices = [text.find("["), text.find("{")]
    start_indices = [i for i in start_indices if i != -1]

    if not start_indices:
        return None

    start = min(start_indices)
    snippet = text[start:]

    # Try trimming at last ] or }
    for end_char in ["]", "}"]:
        end = snippet.rfind(end_char)
        if end != -1:
            candidate = snippet[: end + 1]
            try:
                return json.loads(candidate)
            except Exception:
                continue

    return None

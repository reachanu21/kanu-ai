import os
import json
import time


class LongTermMemory:
    def __init__(self):
        # Always save next to this file
        base = os.path.dirname(os.path.abspath(__file__))
        self.path = os.path.join(base, "long_term.json")

        # Ensure directory exists
        os.makedirs(base, exist_ok=True)

        # Initialize file if missing
        if not os.path.exists(self.path):
            self._initialize_file()

    # ----------------------------------------------------
    # Internal helpers
    # ----------------------------------------------------
    def _initialize_file(self):
        data = {
            "preferences": {},
            "profile": {},
            "habits": {},
            "health": {}
        }
        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)

    def _load_raw(self):
        with open(self.path, "r") as f:
            return json.load(f)

    def _save_raw(self, data):
        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)

    # ----------------------------------------------------
    # Public API
    # ----------------------------------------------------
    def load(self):
        """Load memory with automatic schema repair."""
        data = self._load_raw()

        changed = False

        for category, items in data.items():
            for key, entry in list(items.items()):
                # Convert old string entries → new structured format
                if isinstance(entry, str):
                    data[category][key] = {
                        "value": entry,
                        "confidence": 0.5,
                        "reinforcement": 1,
                        "last_updated": time.time()
                    }
                    changed = True

                # Ensure required fields exist
                else:
                    entry.setdefault("value", "")
                    entry.setdefault("confidence", 0.5)
                    entry.setdefault("reinforcement", 1)
                    entry.setdefault("last_updated", time.time())

        if changed:
            self._save_raw(data)

        return data

    def save(self, data):
        self._save_raw(data)

    # ----------------------------------------------------
    # Update memory entries
    # ----------------------------------------------------
    def update(self, category, key, value, confidence_boost=0.1, confidence=None):
        data = self.load()

        if category not in data:
            data[category] = {}

        entry = data[category].get(key)

        if entry is None:
            initial = confidence if confidence is not None else min(1.0, 0.5 + confidence_boost)
            data[category][key] = {
                "value": value,
                "confidence": min(1.0, initial),
                "reinforcement": 1,
                "last_updated": time.time()
            }
        else:
            entry["value"] = value
            entry["reinforcement"] += 1
            boost = confidence_boost if confidence is None else max(0.0, confidence - entry["confidence"])
            entry["confidence"] = min(1.0, entry["confidence"] + boost)
            entry["last_updated"] = time.time()

        self.save(data)

    def decay(self, half_life_days=30, threshold=0.25):
        """Reduce confidence over time; drop entries below threshold."""
        data = self.load()
        now = time.time()
        half_life_sec = max(half_life_days, 1) * 86400
        changed = False

        for items in data.values():
            for key in list(items.keys()):
                entry = items[key]
                if not isinstance(entry, dict):
                    continue

                age = max(0.0, now - entry.get("last_updated", now))
                factor = 0.5 ** (age / half_life_sec)
                entry["confidence"] = entry.get("confidence", 0.5) * factor

                if entry["confidence"] < threshold:
                    del items[key]
                changed = True

        if changed:
            self.save(data)

    def summarize(self) -> str:
        data = self.load()
        lines = []

        for category, items in data.items():
            for key, entry in items.items():
                if isinstance(entry, dict):
                    value = entry.get("value", "")
                    conf = entry.get("confidence", 0.0)
                    if conf < 0.25:
                        continue
                    lines.append(f"- {category}/{key}: {value}")
                elif entry:
                    lines.append(f"- {category}/{key}: {entry}")

        return "\n".join(lines)

    # ----------------------------------------------------
    # Forget entries
    # ----------------------------------------------------
    def forget(self, target: str):
        """Remove entries whose key or value contains target (case-insensitive)."""
        data = self.load()
        needle = target.lower()
        removed = False

        for items in data.values():
            for key in list(items.keys()):
                entry = items[key]
                value = entry.get("value", entry) if isinstance(entry, dict) else entry
                hay = f"{key} {value}".lower()
                if needle in hay:
                    del items[key]
                    removed = True

        if removed:
            self.save(data)

        return removed

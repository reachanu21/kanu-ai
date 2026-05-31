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
    def update(self, category, key, value, confidence_boost=0.1):
        data = self.load()

        if category not in data:
            data[category] = {}

        entry = data[category].get(key)

        if entry is None:
            # New entry
            data[category][key] = {
                "value": value,
                "confidence": min(1.0, 0.5 + confidence_boost),
                "reinforcement": 1,
                "last_updated": time.time()
            }
        else:
            # Existing entry → reinforce
            entry["value"] = value
            entry["reinforcement"] += 1
            entry["confidence"] = min(1.0, entry["confidence"] + confidence_boost)
            entry["last_updated"] = time.time()

        self.save(data)

    # ----------------------------------------------------
    # Forget entries
    # ----------------------------------------------------
    def forget(self, category, key):
        data = self.load()

        if category in data and key in data[category]:
            del data[category][key]
            self.save(data)
            return True

        return False

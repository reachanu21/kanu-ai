# utility/json_utils.py

import json

def safe_json_parse(text, default=None):
    if default is None:
        default = {
            "is_preference": False,
            "category": "",
            "key": "",
            "value": ""
        }
    try:
        return json.loads(text)
    except Exception:
        return default

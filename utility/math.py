# utility/math.py

import re

def extract_math_expression(text: str):
    pattern = r"(\d+(\.\d+)?\s*[\+\-\*\/]\s*\d+(\.\d+)?)"
    match = re.search(pattern, text)
    return match.group(1) if match else None


def route_tool(prompt: str):
    # Math
    expr = extract_math_expression(prompt)
    if expr:
        return "calculate", {"expression": expr}

    # Unit conversion
    if "convert" in prompt.lower():
        return "unit_convert", {"query": prompt}

    return None, None

# tools.py

class Tool:
    def __init__(self, name, description, schema, func):
        self.name = name
        self.description = description
        self.schema = schema
        self.func = func


class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, tool: Tool):
        self.tools[tool.name] = tool

    def get(self, name):
        return self.tools.get(name)

    def list(self):
        return self.tools.values()

# Calculate function
def calculate(expr: str):
    try:
        return eval(expr)
    except Exception:
        return "Error evaluating expression"

registry = ToolRegistry()

registry.register(Tool(
    name="calculate",
    description="Evaluate a mathematical expression.",
    schema={"expression": "string"},
    func=calculate
))


def unit_convert(input):
    value = input["value"]
    from_unit = input["from"]
    to_unit = input["to"]

    if from_unit == "cm" and to_unit == "m":
        return value / 100
    if from_unit == "m" and to_unit == "cm":
        return value * 100

    return "Unsupported conversion"


registry.register(Tool(
    name="unit_convert",
    description="Convert units (cm↔m).",
    schema={"value": "number", "from": "string", "to": "string"},
    func=unit_convert
))

# tools/registry.py

class Tool:
    def __init__(self, name, func, description=""):
        self.name = name
        self.func = func
        self.description = description


class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, name, func, description=""):
        self.tools[name] = Tool(name, func, description)

    def get(self, name):
        return self.tools.get(name)

    def describe(self):
        return "\n".join(
            f"- {name}: {tool.description}"
            for name, tool in self.tools.items()
        )


# -------------------------------------------------
# Example tools (you can add more later)
# -------------------------------------------------

def calculate_tool(input_data):
    expr = input_data.get("expression", "")
    try:
        return eval(expr)
    except Exception:
        return "Error evaluating expression."


def unit_convert_tool(input_data):
    return f"Unit conversion not implemented yet. Input: {input_data}"


# -------------------------------------------------
# Registry instance
# -------------------------------------------------

registry = ToolRegistry()

registry.register(
    "calculate",
    calculate_tool,
    "Evaluates basic math expressions like '2 + 3 * 4'."
)

registry.register(
    "unit_convert",
    unit_convert_tool,
    "Converts units (placeholder implementation)."
)

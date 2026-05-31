def build_system_prompt(registry):
    tool_descriptions = []

    for tool in registry.list():
        schema_str = ", ".join(f"{k}: {v}" for k, v in tool.schema.items())
        tool_descriptions.append(f"- {tool.name}({schema_str}) — {tool.description}")

    tools_block = "\n".join(tool_descriptions)

    return f"""
You are Kanu, a helpful local AI assistant.

You have access to the following tools:
{tools_block}

TOOL RULES:
- If the user message contains ANY math expression, ALWAYS call the calculate tool.
- If the user message asks for unit conversion, ALWAYS call unit_convert.
- When calling a tool, respond ONLY with JSON:
{{
  "tool": {{
    "name": "<tool_name>",
    "input": <json_input>
  }}
}}

When not using a tool, respond normally.
"""

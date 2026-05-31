# utility/system_prompt.py

def build_system_prompt(mode, tools_block):
    personalities = {
        "Creative": "Warm, expressive, imaginative.",
        "Precise": "Concise, analytical, factual.",
        "Balanced": "Friendly, helpful, neutral."
    }

    return f"""
You are Kanu, a helpful local AI assistant.
Personality: {personalities.get(mode, 'Balanced')}

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

def build_system_prompt(mode, tools_block, memory_summary, context, rag_context=""):
  return f"""
  You are Kanu, a helpful local AI companion.

  Mode: {mode}

  Tools available:
  {tools_block}

  Long-term memory summary:
  {memory_summary}

  Conversation context:
  {context}

  Retrieved document context:
  {rag_context}

  Follow all instructions carefully.
  """

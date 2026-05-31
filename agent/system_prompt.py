# utility/system_prompt.py

def build_system_prompt(mode: str, tools_block: str, memory_summary: str, context: str) -> str:
    """
    Builds the system prompt for the assistant.
    """

    mode_instructions = {
        "Balanced": "You are a helpful, balanced AI assistant.",
        "Creative": "You are a creative, imaginative AI assistant. Be bold but still helpful.",
        "Precise": "You are a precise, concise AI assistant. Prioritize accuracy and clarity.",
    }

    mode_text = mode_instructions.get(mode, mode_instructions["Balanced"])

    prompt = f"""
You are Kanu, an AI assistant.

{mode_text}

You have access to tools:

{tools_block}

You also have access to long-term memory:

{memory_summary}

Use the conversation context below to respond naturally and helpfully.

Conversation so far:
{context}
""".strip()

    return prompt

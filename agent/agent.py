# agent/agent.py

from memory.short_term import ShortTermMemory
from memory.long_term import LongTermMemory
from memory.extractor import PreferenceExtractor
from agent.context_builder import ContextBuilder
from utility.system_prompt import build_system_prompt
from utility.math import extract_math_expression, route_tool
from tools.registry import registry
from memory.memory_manager import MemoryManager



class Assistant:
    def __init__(self, llm, mode="Balanced", summarizer=None, settings=None):
        self.llm = llm
        self.mode = mode
        self.settings = settings or {}

        # Memory layers
        self.stm = ShortTermMemory(max_messages=20)
        self.ltm = LongTermMemory()
        self.extractor = PreferenceExtractor(llm)

        # Unified Memory Interface
        self.memory = MemoryManager(
            stm=self.stm,
            ltm=self.ltm,
            extractor=self.extractor,
            summarizer=summarizer,
            settings=self.settings
        )

        # Helpers
        self.registry = registry
        self.context_builder = ContextBuilder(self.stm, self.ltm, summarizer)

        # ⭐ NEW: RAG engine
        from rag.rag_engine import RAGEngine
        self.rag = RAGEngine()


    def get_temperature(self) -> float:
        if self.mode == "Creative":
            return 0.9
        if self.mode == "Precise":
            return 0.2
        return 0.5  # Balanced

    def _handle_forget_command(self, prompt: str) -> str:
        target = prompt[len("forget"):].strip()
        if not target:
            return "Tell me what you want me to forget, e.g. 'forget my favorite color'."

        self.memory.forget(target)
        return f"Okay, I’ve removed anything related to '{target}' from my long-term memory."

    def run(self, user_message):
    # 1. Save user message to STM
        self.memory.add_message("user", user_message)

    # 2. Math detection
        expr = extract_math_expression(user_message)
        tool_name, tool_input = route_tool(user_message)

    # 3. Retrieve RAG context
        context_chunks = self.rag.query(user_message)
        context_block = "\n\n".join(context_chunks) if context_chunks else ""

    # 4. Build memory summary + conversation context
        memory_summary = self.memory.summarize()
        context = self.context_builder.build()

    # 5. Build system prompt
        system_prompt = build_system_prompt(
            mode=self.mode,
            tools_block=self.registry.describe(),
            memory_summary=memory_summary,
            context=context,
            rag_context=context_block
        )

    # 6. If math or tool is detected → handle it
        if expr is not None:
            result = eval(expr)
            reply = f"The result is {result}."
            self.memory.add_message("assistant", reply)
            return reply

        if tool_name:
            tool = self.registry.get(tool_name)
            tool_result = tool.func(tool_input)

            followup_prompt = (
                f"{system_prompt}\n"
                f"{context}\n"
                f"User: {user_message}\n"
                f"Tool result: {tool_result}\n"
                f"Assistant: Give the final answer to the user using ONLY the tool result above."
            )

            reply = self.llm.generate(followup_prompt, temperature=self.get_temperature())
            self.memory.add_message("assistant", reply)
            return reply

    # 7. Normal LLM response (with RAG context)
        full_prompt = (
            f"{system_prompt}\n"
            f"{context}\n"
            f"Retrieved context:\n{context_block}\n\n"
            f"User: {user_message}\n"
            f"Assistant:"
        )

        reply = self.llm.generate(full_prompt, temperature=self.get_temperature())

    # 8. Save assistant message to STM + LTM
        self.memory.add_message("assistant", reply)

        return reply

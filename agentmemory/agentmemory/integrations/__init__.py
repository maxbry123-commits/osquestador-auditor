"""
agentmemory V3 — Framework integration adapters.

Thin adapters for LangChain, LangGraph, CrewAI, OpenAI Assistants,
and Vercel AI SDK patterns.
"""

from __future__ import annotations

from typing import Any, Optional


# ---- LangChain Memory Adapter ----

class LangChainMemory:
    """
    Drop-in LangChain BaseMemory compatible adapter.

    Usage:
        from agentmemory.integrations import LangChainMemory
        from agentmemory import MemoryStore
        memory = LangChainMemory(MemoryStore("agent.db"))
        chain = ConversationChain(memory=memory)
    """

    def __init__(self, store, memory_key: str = "history",
                 input_key: str = "input", output_key: str = "output",
                 return_messages: bool = False):
        self._store = store
        self.memory_key = memory_key
        self.input_key = input_key
        self.output_key = output_key
        self.return_messages = return_messages

    @property
    def memory_variables(self) -> list[str]:
        return [self.memory_key]

    def load_memory_variables(self, inputs: dict) -> dict:
        query = inputs.get(self.input_key, "")
        if not query:
            return {self.memory_key: "" if not self.return_messages else []}

        result = self._store.build_context(
            query=str(query), token_budget=2000)
        context = result[0] if isinstance(result, tuple) else result

        if self.return_messages:
            return {self.memory_key: [{"role": "system", "content": context}]}
        return {self.memory_key: context}

    def save_context(self, inputs: dict, outputs: dict):
        user_input = inputs.get(self.input_key, "")
        ai_output = outputs.get(self.output_key, "")

        if user_input:
            self._store.add(str(user_input), kind="dialogue",
                            metadata={"role": "user"})
        if ai_output:
            self._store.add(str(ai_output), kind="dialogue",
                            metadata={"role": "assistant"})

    def clear(self):
        pass  # agentmemory handles lifecycle via consolidation


# ---- LangGraph Checkpointer Adapter ----

class LangGraphMemoryAdapter:
    """
    Adapter for LangGraph state-based memory.

    Usage:
        from agentmemory.integrations import LangGraphMemoryAdapter
        adapter = LangGraphMemoryAdapter(store)

        # In your graph node:
        def agent_node(state):
            context = adapter.get_context(state["messages"][-1].content)
            # ... use context
            adapter.save_messages(state["messages"])
    """

    def __init__(self, store, auto_ingest: bool = True):
        self._store = store
        self._auto_ingest = auto_ingest

    def get_context(self, query: str, token_budget: int = 4000) -> str:
        result = self._store.build_context(query=query, token_budget=token_budget)
        return result[0] if isinstance(result, tuple) else result

    def recall(self, query: str, limit: int = 10, **kwargs):
        return self._store.recall(query=query, limit=limit, **kwargs)

    def save_messages(self, messages: list[dict], session_id: str = ""):
        if self._auto_ingest:
            self._store.ingest_conversation(
                messages=messages, session_id=session_id)
        else:
            for msg in messages:
                content = msg.get("content", "")
                if content:
                    self._store.add(content, kind="dialogue",
                                    metadata={"role": msg.get("role", "")})

    def add_fact(self, content: str, **kwargs):
        return self._store.add(content, kind="fact", **kwargs)


# ---- OpenAI Assistants Tool Adapter ----

class OpenAIToolAdapter:
    """
    Exposes agentmemory as OpenAI function-calling tools.

    Usage:
        adapter = OpenAIToolAdapter(store)
        tools = adapter.get_tool_definitions()
        # Add to OpenAI API call
        response = client.chat.completions.create(tools=tools, ...)
        # Handle tool calls
        result = adapter.handle_tool_call(tool_call.function.name,
                                           json.loads(tool_call.function.arguments))
    """

    def __init__(self, store):
        self._store = store

    def get_tool_definitions(self) -> list[dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "remember",
                    "description": "Store a fact, entity, preference, or observation in long-term memory",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "content": {"type": "string", "description": "What to remember"},
                            "kind": {"type": "string", "enum": ["fact", "entity", "preference", "event"]},
                            "importance": {"type": "number", "description": "0-1 importance"},
                        },
                        "required": ["content"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "recall",
                    "description": "Search long-term memory for relevant information",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "What to search for"},
                            "limit": {"type": "integer", "default": 5},
                        },
                        "required": ["query"],
                    },
                },
            },
        ]

    def handle_tool_call(self, name: str, arguments: dict) -> str:
        import json
        if name == "remember":
            node = self._store.add(
                content=arguments["content"],
                kind=arguments.get("kind"),
                importance=arguments.get("importance"),
            )
            return json.dumps({"stored": True, "id": node.id,
                               "kind": node.kind.value})
        elif name == "recall":
            results = self._store.recall(
                query=arguments["query"],
                limit=arguments.get("limit", 5))
            return json.dumps([{
                "content": r.node.content,
                "kind": r.node.kind.value,
                "score": round(r.score, 3),
                "importance": r.node.importance,
            } for r in results])
        return json.dumps({"error": f"Unknown tool: {name}"})


# ---- CrewAI Memory Adapter ----

class CrewAIMemoryAdapter:
    """
    Adapter for CrewAI agent memory.

    Usage:
        from agentmemory.integrations import CrewAIMemoryAdapter
        adapter = CrewAIMemoryAdapter(store)
        # In agent definition, use adapter methods
    """

    def __init__(self, store):
        self._store = store

    def search(self, query: str, limit: int = 5) -> list[dict]:
        results = self._store.recall(query=query, limit=limit)
        return [{"content": r.node.content, "score": r.score,
                 "metadata": r.node.metadata} for r in results]

    def save(self, content: str, metadata: Optional[dict] = None):
        self._store.add(content=content, metadata=metadata or {})

    def reset(self):
        pass  # agentmemory manages lifecycle


# ---- Vercel AI SDK Pattern ----

class VercelAIAdapter:
    """
    Memory adapter following Vercel AI SDK patterns.
    Returns memory context as system messages.
    """

    def __init__(self, store):
        self._store = store

    def get_system_context(self, user_message: str,
                           token_budget: int = 2000) -> str:
        result = self._store.build_context(
            query=user_message, token_budget=token_budget)
        return result[0] if isinstance(result, tuple) else result

    def process_completion(self, messages: list[dict]):
        """Process a completion's messages into memory."""
        self._store.ingest_conversation(messages=messages)

"""
agentmemory — conversation ingestion example.

Demonstrates ingesting a multi-turn conversation and recalling
extracted facts, preferences, and entity information.

Expected output (approximate):
    Ingested 5 memories from conversation

    Recalling "what does Alice do?":
      [0.xxx] Alice is the CEO of TechCorp [entity]
      ...

    Recalling "Alice's communication style":
      [0.xxx] Alice prefers async communication over meetings [preference]
      ...
"""

import asyncio
from agentmemory import MemoryStore


async def main():
    async with MemoryStore(prefer_dense=False) as mem:
        # Ingest a realistic conversation
        conversation = [
            {"role": "user",  "content": "Hi, I'm Alice, CEO of TechCorp."},
            {"role": "assistant", "content": "Nice to meet you, Alice!"},
            {"role": "user",  "content": "We raised a $20M Series B last January."},
            {"role": "user",  "content": "I prefer async communication — no unnecessary meetings."},
            {"role": "user",  "content": "Our stack is Python on AWS, PostgreSQL for the database."},
            {"role": "assistant", "content": "That's a solid stack for a growing company."},
            {"role": "user",  "content": "We're hiring senior engineers right now."},
        ]

        nodes = await mem.async_ingest_conversation(
            conversation,
            session_id="demo-session-001",
            source="example_conversation"
        )
        print(f"Ingested {len(nodes)} memories from conversation\n")

        # Recall entity information
        print('Recalling "what does Alice do?":')
        results = await mem.async_recall("what does Alice do?", limit=3)
        for r in results:
            print(f"  [{r.score:.3f}] {r.node.content} [{r.node.kind.value}]")

        print()

        # Recall preference information
        print('Recalling "Alice\'s communication style":')
        results = await mem.async_recall("communication preferences", limit=3)
        for r in results:
            print(f"  [{r.score:.3f}] {r.node.content} [{r.node.kind.value}]")

        print()

        # Build a formatted context block ready for LLM injection
        print("Context block for LLM (token_budget=500):")
        context, meta = await mem.async_build_context(
            "Tell me about Alice and TechCorp",
            token_budget=500
        )
        print(context)
        print(f"Abstained: {meta['abstained']}, Max score: {meta['max_relevance_score']:.3f}")


asyncio.run(main())

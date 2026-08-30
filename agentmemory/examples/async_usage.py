"""
agentmemory — async-first API example.

Demonstrates the full async API: context manager, async_add, async_recall,
async_build_context, async_consolidate, async_stats, and async_feedback.

This is the recommended pattern for production agent deployments.

Expected output (approximate):
    Added 4 memories

    Recall results for "Python deployment":
      [0.xxx] TechCorp deploys on AWS using ECS containers [fact]
      ...

    Context block:
    === Agent Memory Context ===
    ...

    Stats: {'total_memories': 4, ...}
"""

import asyncio
from agentmemory import MemoryStore


async def main():
    # Async context manager ensures clean shutdown
    async with MemoryStore(prefer_dense=False) as mem:

        # Store memories with explicit kind and importance
        n1 = await mem.async_add(
            "TechCorp deploys on AWS using ECS containers",
            kind="fact",
            importance=0.8,
            tags={"infrastructure", "aws"}
        )
        n2 = await mem.async_add(
            "Alice prefers Python for backend services",
            kind="preference",
            importance=0.7
        )
        n3 = await mem.async_add(
            "The API uses OAuth2 for authentication",
            kind="fact",
            importance=0.75,
            tags={"security", "api"}
        )
        n4 = await mem.async_add(
            "TechCorp uses PostgreSQL for the primary database",
            kind="fact",
            importance=0.8,
            tags={"infrastructure", "database"}
        )
        print(f"Added 4 memories\n")

        # Semantic recall
        print('Recall results for "Python deployment":')
        results = await mem.async_recall(
            "Python deployment",
            limit=5,
            tags={"infrastructure"}
        )
        for r in results:
            print(f"  [{r.score:.3f}] {r.node.content}")

        print()

        # Build LLM-ready context block
        print("Context block:")
        context, meta = await mem.async_build_context(
            "What is TechCorp's infrastructure stack?",
            token_budget=1000,
            include_confidence=True
        )
        print(context)

        # Consolidate (deduplicate, promote tiers, resolve contradictions)
        cycle_result = await mem.async_consolidate()
        print(f"Consolidation: {cycle_result}")

        # Record feedback on a retrieval (drives confidence calibration)
        await mem.async_feedback(n1.id, correct=True)
        await mem.async_feedback(n2.id, correct=True)

        # Inspect stats
        stats = await mem.async_stats()
        print(f"\nStats: {stats}")


asyncio.run(main())

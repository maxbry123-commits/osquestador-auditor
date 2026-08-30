"""
agentmemory — practical agent loop integration.

Demonstrates how a conversational AI agent uses agentmemory across
multiple turns: ingesting conversation history, building per-turn
context, answering based on memory, and recording feedback.

This pattern is designed for production agent frameworks where you
need persistent, queryable memory across sessions.

Expected output (approximate):
    === Turn 1 ===
    User: Hi, I'm Jordan. I work as a data scientist at Meridian Labs.
    Memory context for assistant: (context block with extracted facts)

    === Turn 2 ===
    User: We use Python, Spark, and dbt. Our data warehouse is Snowflake.
    Memory context for assistant: (updated context block)

    Final memory stats: {'total_memories': N, ...}
"""

import asyncio
from agentmemory import MemoryStore


async def agent_session():
    """Simulate a multi-turn agent conversation with persistent memory."""

    async with MemoryStore(prefer_dense=False) as mem:

        # Simulate a multi-turn conversation
        turns = [
            "Hi, I'm Jordan. I work as a data scientist at Meridian Labs.",
            "We use Python, Spark, and dbt. Our data warehouse is Snowflake.",
            "I prefer to work async — I check messages at 9am and 3pm.",
            "Our team has 8 engineers. We're working on a real-time ML pipeline.",
            "By the way, I'm based in Austin, Texas.",
        ]

        session_history = []

        for i, user_message in enumerate(turns, 1):
            print(f"\n=== Turn {i} ===")
            print(f"User: {user_message}")

            # Add this turn to session history
            session_history.append({"role": "user", "content": user_message})

            # Ingest the latest turn into memory
            await mem.async_ingest_conversation(
                [{"role": "user", "content": user_message}],
                session_id="jordan-session-001",
                source="agent_demo"
            )

            # Build memory context for the assistant's response
            context, meta = await mem.async_build_context(
                user_message,
                token_budget=800,
                include_confidence=True
            )

            if not meta["abstained"]:
                print(f"Memory context ({meta['memories_retrieved']} memories):")
                # Show first 3 lines of context for brevity
                for line in context.split("\n")[:5]:
                    if line.strip():
                        print(f"  {line}")
            else:
                print("  (no relevant memories yet)")

        print("\n--- Session complete ---\n")

        # Demonstrate recall across the session
        print('Recall: "what tools does Jordan use?"')
        results = await mem.async_recall("tools stack technologies", limit=5)
        for r in results:
            print(f"  [{r.score:.3f}] {r.node.content}")

        print()
        print('Recall: "Jordan personal info"')
        results = await mem.async_recall("Jordan location work", limit=3)
        for r in results:
            print(f"  [{r.score:.3f}] {r.node.content}")

        # Final stats
        stats = await mem.async_stats()
        print(f"\nFinal memory stats: {stats}")


asyncio.run(agent_session())

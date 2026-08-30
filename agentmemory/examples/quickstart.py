"""
agentmemory quickstart — add and recall in 10 lines.

Demonstrates zero-dependency usage with TF-IDF embeddings.
No pip installs beyond agentmemory required.

Expected output (approximate):
    [0.xxx] Alice is the CEO of TechCorp [entity]
    [0.xxx] TechCorp raised a Series B in January 2024 [fact]
    [0.xxx] Alice prefers async communication over meetings [preference]
"""

from agentmemory import MemoryStore

mem = MemoryStore()  # Zero dependencies required — uses TF-IDF embeddings by default

# Store some memories
mem.add("Alice is the CEO of TechCorp", kind="entity")
mem.add("Alice prefers async communication over meetings", kind="preference")
mem.add("TechCorp raised a Series B in January 2024", kind="fact")

# Recall relevant memories
results = mem.recall("who runs TechCorp?", limit=5)
for r in results:
    print(f"[{r.score:.3f}] {r.node.content} [{r.node.kind.value}]")

mem.close()

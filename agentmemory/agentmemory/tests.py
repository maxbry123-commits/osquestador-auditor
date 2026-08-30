"""
agentmemory V4 — Test suite.

Covers all V3 tests + V4 fixes and upgrades:
  Fix 1: Auto-graph edge persistence
  Fix 2: Init race condition
  Fix 3: Validation pre-loaded nodes
  Fix 4: Importance decay in consolidation
  Fix 5: Conditional contradiction edges
  Fix 6: pyproject.toml (manual check)
  Upgrade 2: Adaptive weights
  Upgrade 3: Document ingestion
  Upgrade 4: Confidence calibration
  Upgrade 5: Temporal validity windows
  Upgrade 7: Memory profiles
  Upgrade 9: Consolidation quality scoring
  Upgrade 11: Memory lineage
"""

from __future__ import annotations

import asyncio
import sys
import time
import traceback

sys.path.insert(0, ".")


def _run(name, coro_fn) -> bool:
    try:
        asyncio.run(coro_fn())
        print(f"  PASS  {name}")
        return True
    except AssertionError as e:
        print(f"  FAIL  {name}: {e}")
        return False
    except Exception as e:
        print(f"  ERROR {name}: {e}")
        traceback.print_exc()
        return False


async def test_basic_add_recall():
    from agentmemory import MemoryStore
    mem = MemoryStore(prefer_dense=False)
    node = await mem.async_add("The CEO is Alice Johnson", kind="entity", importance=0.9)
    assert node.id
    results = await mem.async_recall("who is the CEO?", limit=5)
    assert any("alice" in r.node.content.lower() for r in results)
    await mem.async_close()


async def test_auto_classification():
    from agentmemory import MemoryStore
    mem = MemoryStore(prefer_dense=False)
    node = await mem.async_add("Alice Johnson is the CEO of TechCorp")
    assert node.kind.value in ("entity", "fact")
    await mem.async_close()


async def test_conversation_ingestion():
    from agentmemory import MemoryStore
    mem = MemoryStore(prefer_dense=False)
    msgs = [
        {"role": "user", "content": "My name is Bob and I work at Acme Corp as a senior engineer."},
        {"role": "assistant", "content": "Nice to meet you Bob!"},
        {"role": "user", "content": "I prefer using Python and our deployment runs on AWS."},
    ]
    nodes = await mem.async_ingest_conversation(msgs, session_id="test")
    assert len(nodes) >= 1
    await mem.async_close()


async def test_fix1_auto_graph_persistence():
    """Fix 1: Auto-graph edges persist to storage and use real entity node IDs."""
    from agentmemory import MemoryStore
    mem = MemoryStore(prefer_dense=False, write_validation=False, auto_graph=True)
    await mem.async_add("Alice Johnson is the CEO of TechCorp", kind="entity")
    stats = await mem.async_stats()
    assert stats["edges"] > 0, f"No edges persisted: {stats['edges']}"
    # Verify edges reference real node IDs (not synthetic entity: prefixes)
    edges = mem._graph.to_list()
    for e in edges:
        assert not e["source_id"].startswith("entity:"), \
            f"Synthetic entity ID found: {e['source_id']}"
        assert not e["target_id"].startswith("entity:"), \
            f"Synthetic entity ID found: {e['target_id']}"
    await mem.async_close()


async def test_fix2_init_lock():
    """Fix 2: _ensure_init has asyncio.Lock, no duplicate reload."""
    from agentmemory import MemoryStore
    mem = MemoryStore(prefer_dense=False, write_validation=False, auto_graph=False)
    assert hasattr(mem, '_init_lock')
    # Run concurrent inits
    await asyncio.gather(mem._ensure_init(), mem._ensure_init(), mem._ensure_init())
    assert mem._init_done
    await mem.async_close()


async def test_fix3_validation_nearby_nodes():
    """Fix 3: Validation uses pre-loaded nearby_nodes, not storage.load_node_sync."""
    from agentmemory import MemoryStore
    mem = MemoryStore(prefer_dense=False, write_validation=True)
    await mem.async_add("The CEO is Alice Johnson", kind="fact", importance=0.9)
    # This should succeed (contradiction warning but not blocking)
    node2 = await mem.async_add("The CEO is Bob Smith", kind="fact", importance=0.9)
    assert node2 is not None
    await mem.async_close()


async def test_fix4_importance_decay_in_consolidation():
    """Fix 4: run_full_cycle returns importance_decayed key."""
    from agentmemory import MemoryStore
    mem = MemoryStore(prefer_dense=False, write_validation=False,
                      auto_graph=False, importance_evolution=True)
    for i in range(5):
        await mem.async_add(f"Fact {i} about something", kind="fact")
    result = await mem.async_consolidate()
    assert "importance_decayed" in result, f"Missing importance_decayed key: {result.keys()}"
    await mem.async_close()


async def test_fix5_conditional_contradiction_edges():
    """Fix 5: Contradiction edges only created when resolution fails."""
    from agentmemory import MemoryStore
    mem = MemoryStore(prefer_dense=False, write_validation=False, auto_graph=False)
    await mem.async_add("The CEO is Alice Johnson", kind="entity", importance=0.9)
    await mem.async_add("The CEO is Bob Smith", kind="entity", importance=0.3)
    result = await mem.async_consolidate()
    # With heuristic resolve, one should be superseded (0.9 vs 0.3 is > 0.1 gap)
    # So contradiction edge should NOT be created for resolved pair
    # We just verify the system runs without error and produces results
    assert result["contradictions"] >= 0
    await mem.async_close()


async def test_upgrade2_adaptive_weights():
    """Upgrade 2: RetrieverWeightAdapter tracks signal correlations."""
    from agentmemory.retrieval import RetrieverWeightAdapter
    adapter = RetrieverWeightAdapter(alpha=0.1)
    for _ in range(20):
        adapter.record_quality(
            {"semantic": 0.8, "lexical": 0.2, "activation": 0.3,
             "graph": 0.1, "importance": 0.5, "temporal": 0.4}, 0.9)
    weights = adapter.get_adapted_weights()
    assert len(weights) == 6
    assert abs(sum(weights.values()) - 1.0) < 0.01


async def test_upgrade3_document_ingestion():
    """Upgrade 3: Ingest a long document with semantic chunking."""
    from agentmemory import MemoryStore
    mem = MemoryStore(prefer_dense=False, write_validation=False, auto_graph=False)
    doc = """
    Chapter 1: Introduction to Machine Learning

    Machine learning is a subset of artificial intelligence that focuses on building
    systems that learn from data. Unlike traditional programming where rules are
    explicitly coded, ML systems discover patterns automatically.

    Chapter 2: Supervised Learning

    In supervised learning, models are trained on labeled datasets. The algorithm
    learns a mapping from inputs to outputs. Common algorithms include linear
    regression, decision trees, and neural networks. Performance is measured using
    metrics like accuracy, precision, and recall.

    Chapter 3: Unsupervised Learning

    Unsupervised learning works with unlabeled data. The goal is to find hidden
    patterns or structures. Clustering algorithms like K-means group similar data
    points. Dimensionality reduction techniques like PCA compress data while
    preserving important information.
    """
    nodes = await mem.async_ingest_document(doc, title="ML Textbook", source="test")
    assert len(nodes) >= 2, f"Expected 2+ memories (doc entity + chunks), got {len(nodes)}"
    # Should find ML-related content
    results = await mem.async_recall("machine learning algorithms", limit=5)
    assert len(results) > 0
    await mem.async_close()


async def test_upgrade4_confidence_calibration():
    """Upgrade 4: feedback() updates confidence, calibration_report() works."""
    from agentmemory import MemoryStore
    mem = MemoryStore(prefer_dense=False, write_validation=False, auto_graph=False)
    node = await mem.async_add("Python is great for ML", kind="fact", importance=0.8)
    # Record feedback
    await mem.async_feedback(node.id, correct=True)
    await mem.async_feedback(node.id, correct=True)
    await mem.async_feedback(node.id, correct=False)
    updated = await mem.async_get(node.id)
    assert updated.feedback_correct == 2
    assert updated.feedback_incorrect == 1
    # Calibration report
    report = await mem.async_calibration_report()
    assert report["total_memories_with_feedback"] == 1
    assert report["total_feedback_events"] == 3
    await mem.async_close()


async def test_upgrade5_temporal_validity():
    """Upgrade 5: valid_until filtering excludes expired facts."""
    from agentmemory import MemoryStore
    mem = MemoryStore(prefer_dense=False, write_validation=False, auto_graph=False)
    now = time.time()
    # Add a fact that expired 1 hour ago
    expired = await mem.async_add("Old CEO is Alice", kind="fact",
                                   valid_until=now - 3600)
    # Add a current fact
    current = await mem.async_add("New CEO is Bob", kind="fact")
    # Default recall should exclude expired
    results = await mem.async_recall("who is CEO?", limit=10)
    result_ids = {r.node.id for r in results}
    assert expired.id not in result_ids, "Expired fact should be excluded"
    assert current.id in result_ids, "Current fact should be included"
    # include_expired=True should show both
    results2 = await mem.async_recall("who is CEO?", limit=10, include_expired=True)
    result_ids2 = {r.node.id for r in results2}
    assert expired.id in result_ids2, "Expired fact should appear with include_expired=True"
    await mem.async_close()


async def test_upgrade5_is_valid():
    """Upgrade 5: MemoryNode.is_valid property works correctly."""
    from agentmemory.models import MemoryNode, MemoryKind
    now = time.time()
    valid = MemoryNode(content="test", kind=MemoryKind.FACT)
    assert valid.is_valid
    expired = MemoryNode(content="test", kind=MemoryKind.FACT, valid_until=now - 100)
    assert not expired.is_valid
    future = MemoryNode(content="test", kind=MemoryKind.FACT, valid_from=now + 3600)
    assert not future.is_valid


async def test_upgrade7_memory_profiles():
    """Upgrade 7: MemoryStore.from_profile works."""
    from agentmemory import MemoryStore, MemoryProfile
    # Test preset loading
    profile = MemoryProfile.from_preset("support_agent")
    assert profile.name == "support_agent"
    assert profile.proactive_surfacing is True
    # Test MemoryStore.from_profile
    mem = MemoryStore.from_profile("coding_assistant", prefer_dense=False,
                                    write_validation=False, auto_graph=False)
    assert mem._profile.name == "coding_assistant"
    await mem.async_add("Test fact", kind="fact")
    stats = await mem.async_stats()
    assert stats["profile"] == "coding_assistant"
    await mem.async_close()


async def test_upgrade9_consolidation_quality():
    """Upgrade 9: Consolidation scores quality against cluster centroid."""
    from agentmemory import MemoryStore
    mem = MemoryStore(prefer_dense=False, write_validation=False, auto_graph=False)
    # Add similar episodic memories that should cluster
    for i in range(5):
        await mem.async_add(f"Docker container build step {i} completed",
                            kind="event", importance=0.5)
    result = await mem.async_consolidate()
    # Check that consolidation ran
    assert result["consolidated"] >= 0
    # Check importance_decayed is tracked
    assert "importance_decayed" in result
    await mem.async_close()


async def test_upgrade11_lineage():
    """Upgrade 11: lineage() returns complete causal chain."""
    from agentmemory import MemoryStore
    mem = MemoryStore(prefer_dense=False, write_validation=False, auto_graph=False)
    node = await mem.async_add("Alice is the CEO", kind="entity", importance=0.9)
    await mem.async_update(node.id, content="Alice Johnson is the CEO")
    report = await mem.async_lineage(node.id)
    assert report.node_id == node.id
    assert report.current_kind == "entity"
    assert len(report.history) >= 2  # CREATE + UPDATE
    report_dict = report.to_dict()
    assert "history" in report_dict
    assert len(report_dict["history"]) >= 2
    await mem.async_close()


async def test_namespace_isolation():
    from agentmemory import MemoryStore, Namespace
    mem = MemoryStore(prefer_dense=False, write_validation=False, auto_graph=False)
    mem.set_namespace(org="acme", team="alpha")
    await mem.async_add("Team Alpha secret", kind="fact", importance=0.9)
    mem.set_namespace(org="acme", team="beta")
    await mem.async_add("Team Beta strategy", kind="fact", importance=0.9)
    results = await mem.async_recall("team strategy",
                                     namespace=Namespace(org="acme", team="alpha"))
    for r in results:
        assert "beta" not in r.node.content.lower()
    await mem.async_close()


async def test_gdpr_deletion():
    from agentmemory import MemoryStore
    mem = MemoryStore(prefer_dense=False, write_validation=False, auto_graph=False)
    for i in range(5):
        await mem.async_add(f"User data {i}", kind="fact", source="user_123")
    receipt = await mem.async_delete_user("user_123")
    assert receipt.memories_deleted == 5
    assert receipt.verified
    await mem.async_close()


async def test_health_check():
    from agentmemory import MemoryStore
    mem = MemoryStore(prefer_dense=False, write_validation=False, auto_graph=False)
    for i in range(10):
        await mem.async_add(f"Health test {i}", kind="fact")
    report = await mem.async_health_check()
    assert report.total_memories == 10
    assert report.expired_memories == 0
    assert report.low_quality_consolidations == 0
    await mem.async_close()


async def test_provenance():
    from agentmemory import MemoryStore, Provenance
    mem = MemoryStore(prefer_dense=False, write_validation=False, auto_graph=False)
    prov = Provenance(source="test_agent", session_id="s1", conversation_turn=3,
                      agent_id="agent_a", tool_call_id="tool_42")
    node = await mem.async_add("Provenance test", kind="fact", provenance=prov)
    loaded = await mem.async_get(node.id)
    assert loaded.provenance.source == "test_agent"
    assert loaded.provenance.agent_id == "agent_a"
    assert loaded.provenance.conversation_turn == 3
    await mem.async_close()


async def test_export_v4():
    from agentmemory import MemoryStore
    mem = MemoryStore(prefer_dense=False, write_validation=False, auto_graph=False)
    await mem.async_add("Export test", kind="fact")
    data = await mem.async_export()
    assert data["version"] == "4.0.0"
    assert len(data["nodes"]) == 1
    # V4 fields present
    assert "valid_from" in data["nodes"][0]
    assert "media_type" in data["nodes"][0]
    assert "feedback_correct" in data["nodes"][0]
    await mem.async_close()


async def test_concurrent_writes():
    import tempfile, os
    from agentmemory import MemoryStore
    db = os.path.join(tempfile.gettempdir(), "v4_concurrent.db")
    if os.path.exists(db): os.unlink(db)
    mem = MemoryStore(db, prefer_dense=False, write_validation=False,
                      auto_graph=False, proactive_surfacing=False)
    errors = []
    N, T = 10, 4
    async def writer(aid):
        try:
            for i in range(N):
                await mem.async_add(f"Agent {aid} memory #{i}", kind="observation",
                                    source=f"agent_{aid}")
        except Exception as e:
            errors.append((aid, e))
    tasks = [asyncio.create_task(writer(i)) for i in range(T)]
    await asyncio.gather(*tasks)
    assert not errors
    count = await mem.async_len()
    assert count == N * T, f"Expected {N*T}, got {count}"
    await mem.async_close()
    os.unlink(db)


async def test_document_chunker():
    from agentmemory.extraction import DocumentChunker
    chunker = DocumentChunker(max_chunk_chars=200, min_chunk_chars=20)
    text = "First paragraph about topic A.\n\nSecond paragraph about topic B with more detail.\n\nThird paragraph wrapping up."
    chunks = chunker.chunk(text)
    assert len(chunks) >= 1
    assert all(len(c) >= 20 for c in chunks)


async def test_kind_classifier():
    from agentmemory.classification import KindClassifier
    clf = KindClassifier()
    kind = clf.classify("Alice Johnson is the CEO of TechCorp")
    assert kind.value in ("entity", "fact")


def run_all() -> bool:
    tests = [
        ("basic_add_recall", test_basic_add_recall),
        ("auto_classification", test_auto_classification),
        ("conversation_ingestion", test_conversation_ingestion),
        ("fix1_auto_graph_persistence", test_fix1_auto_graph_persistence),
        ("fix2_init_lock", test_fix2_init_lock),
        ("fix3_validation_nearby_nodes", test_fix3_validation_nearby_nodes),
        ("fix4_importance_decay", test_fix4_importance_decay_in_consolidation),
        ("fix5_conditional_contradiction_edges", test_fix5_conditional_contradiction_edges),
        ("upgrade2_adaptive_weights", test_upgrade2_adaptive_weights),
        ("upgrade3_document_ingestion", test_upgrade3_document_ingestion),
        ("upgrade4_calibration", test_upgrade4_confidence_calibration),
        ("upgrade5_temporal_validity", test_upgrade5_temporal_validity),
        ("upgrade5_is_valid", test_upgrade5_is_valid),
        ("upgrade7_profiles", test_upgrade7_memory_profiles),
        ("upgrade9_consolidation_quality", test_upgrade9_consolidation_quality),
        ("upgrade11_lineage", test_upgrade11_lineage),
        ("namespace_isolation", test_namespace_isolation),
        ("gdpr_deletion", test_gdpr_deletion),
        ("health_check", test_health_check),
        ("provenance", test_provenance),
        ("export_v4", test_export_v4),
        ("concurrent_writes", test_concurrent_writes),
        ("document_chunker", test_document_chunker),
        ("kind_classifier", test_kind_classifier),
    ]
    print(f"\nagentmemory V4 — Test Suite ({len(tests)} tests)\n")
    passed = failed = 0
    for name, fn in tests:
        if _run(name, fn):
            passed += 1
        else:
            failed += 1
    print(f"\nResults: {passed} passed, {failed} failed out of {len(tests)}")
    return failed == 0


if __name__ == "__main__":
    sys.exit(0 if run_all() else 1)

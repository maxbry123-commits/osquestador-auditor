"""Test the 13 plugins + core API endpoints."""
import pytest
import pytest_asyncio

@pytest.mark.asyncio
async def test_health(client):
    r = await client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

@pytest.mark.asyncio
async def test_root(client):
    r = await client.get("/api/")
    assert r.status_code == 200
    data = r.json()
    assert "Osquestador" in data["service"]
    assert data["plugins"] == 13

@pytest.mark.asyncio
async def test_login_success(client):
    r = await client.post("/api/auth/login", json={"username": "max", "password": "max123"})
    assert r.status_code == 200
    data = r.json()
    assert "token" in data
    assert data["user"]["name"] == "Maxbry Odreman"

@pytest.mark.asyncio
async def test_login_bad_password(client):
    r = await client.post("/api/auth/login", json={"username": "max", "password": "wrong"})
    assert r.status_code == 401

@pytest.mark.asyncio
async def test_plugins_registry(client):
    r = await client.get("/api/plugins")
    assert r.status_code == 200
    plugins = r.json()
    expected = ['graphiti', 'kanboard', 'paddleocr', 'serper', 'claude', 'observer', 'watchdog', 'memory', 'research', 'design', 'build', 'audit', 'dispatch']
    for p in expected:
        assert p in plugins, f"plugin '{p}' missing"

@pytest.mark.asyncio
async def test_observer_status(client):
    r = await client.get("/api/observer/status")
    assert r.status_code == 200
    data = r.json()
    assert "projects" in data
    assert "artifacts" in data
    assert "tasks" in data

@pytest.mark.asyncio
async def test_watchdog_check(client):
    r = await client.get("/api/watchdog/check")
    assert r.status_code == 200
    data = r.json()
    assert data["openclaw"]["status"] == "intact"
    assert data["rules"]["R0_openclaw_intact"] is True

@pytest.mark.asyncio
async def test_chat_non_streaming(client):
    r = await client.post("/api/chat", json={
        "messages": [{"role": "user", "content": "hola"}],
        "model": "claude-sonnet-4.5",
        "project_id": "osquestador-auditor"
    })
    assert r.status_code == 200
    data = r.json()
    assert data["role"] == "assistant"
    assert len(data["content"]) > 0
    assert "text" in data["content"][0]

@pytest.mark.asyncio
async def test_chat_streaming_sse_events(client):
    r = await client.post("/api/chat", params={"stream": "true"}, json={
        "messages": [{"role": "user", "content": "test"}],
        "model": "claude-sonnet-4.5",
        "project_id": "osquestador-auditor"
    }, headers={"Accept": "text/event-stream"})
    assert r.status_code == 200
    text = r.text
    # Check for all 6 official Anthropic SSE events
    assert "event: message_start" in text
    assert "event: content_block_start" in text
    assert "event: content_block_delta" in text
    assert "event: content_block_stop" in text
    assert "event: message_delta" in text
    assert "event: message_stop" in text

@pytest.mark.asyncio
async def test_artifacts_list(client):
    r = await client.get("/api/artifacts")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 5
    types = {a["type"] for a in items}
    assert "py" in types or "md" in types

@pytest.mark.asyncio
async def test_tasks_kanban(client):
    r = await client.get("/api/tasks")
    assert r.status_code == 200
    tasks = r.json()
    assert len(tasks) >= 10
    cols = {t["column"] for t in tasks}
    assert "backlog" in cols

@pytest.mark.asyncio
async def test_create_and_move_task(client):
    # Create
    r = await client.post("/api/tasks", json={"title": "test task", "column": "backlog", "priority": "low"})
    assert r.status_code == 200
    tid = r.json()["id"]
    # Move
    r = await client.patch(f"/api/tasks/{tid}", json={"column": "doing"})
    assert r.status_code == 200
    # Delete
    r = await client.delete(f"/api/tasks/{tid}")
    assert r.status_code == 200

@pytest.mark.asyncio
async def test_memory_search(client):
    r = await client.post("/api/memory/search", json={"query": "osquestador", "top_k": 3})
    assert r.status_code == 200
    data = r.json()
    assert "results" in data

@pytest.mark.asyncio
async def test_plugin_invoke(client):
    r = await client.post("/api/plugins/observer/get_status", json={})
    assert r.status_code == 200
    data = r.json()
    assert "projects" in data

@pytest.mark.asyncio
async def test_graphiti_search(client):
    r = await client.post("/api/plugins/graphiti/search", json={"query": "osquestador", "top_k": 3})
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_design_tokens(client):
    r = await client.post("/api/plugins/design/get_tokens", json={})
    assert r.status_code == 200
    data = r.json()
    assert "dark" in data
    assert data["dark"]["bg"] == "#202124"

@pytest.mark.asyncio
async def test_decisions_list(client):
    r = await client.get("/api/decisions")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1
    ids = {d["id"] for d in items}
    assert "D-01" in ids

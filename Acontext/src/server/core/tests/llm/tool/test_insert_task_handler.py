"""
Tests for insert_task_handler — Fix 4: metric backpressure.

Covers:
- capture_increment is awaited inline (not fire-and-forget)
- Handler returns success after metric increment succeeds
- Metric failure is logged but does not propagate
- No asyncio.create_task(capture_increment(...)) remains
"""

import ast
import uuid
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

from acontext_core.schema.result import Result
from acontext_core.constants import MetricTags


MODULE = "acontext_core.llm.tool.task_lib.insert"


def _make_ctx():
    ctx = MagicMock()
    ctx.project_id = uuid.uuid4()
    ctx.session_id = uuid.uuid4()
    ctx.db_session = MagicMock()
    return ctx


def _llm_args(after_order=0, desc="Test task"):
    return {"after_task_order": after_order, "task_description": desc}


class TestInsertTaskHandlerMetrics:
    @pytest.mark.asyncio
    async def test_capture_increment_is_awaited(self):
        """capture_increment is awaited inline, not spawned as a background task."""
        task_mock = MagicMock()
        task_mock.order = 1
        capture_mock = AsyncMock()

        with (
            patch(
                f"{MODULE}.TD.insert_task",
                new_callable=AsyncMock,
                return_value=Result.resolve(task_mock),
            ),
            patch(f"{MODULE}.capture_increment", capture_mock),
        ):
            from acontext_core.llm.tool.task_lib.insert import insert_task_handler

            r = await insert_task_handler(_make_ctx(), _llm_args())

            capture_mock.assert_awaited_once()
            assert r.ok()

    @pytest.mark.asyncio
    async def test_returns_success_after_metric(self):
        """Handler returns 'Task N created' after successful metric increment."""
        task_mock = MagicMock()
        task_mock.order = 3
        capture_mock = AsyncMock()

        with (
            patch(
                f"{MODULE}.TD.insert_task",
                new_callable=AsyncMock,
                return_value=Result.resolve(task_mock),
            ),
            patch(f"{MODULE}.capture_increment", capture_mock),
        ):
            from acontext_core.llm.tool.task_lib.insert import insert_task_handler

            r = await insert_task_handler(_make_ctx(), _llm_args())

            assert r.ok()
            data, _ = r.unpack()
            assert data == "Task 3 created"

    @pytest.mark.asyncio
    async def test_metric_failure_does_not_propagate(self):
        """capture_increment raises -> logged, but handler still returns success."""
        task_mock = MagicMock()
        task_mock.order = 2
        capture_mock = AsyncMock(side_effect=ConnectionError("DB advisory lock timeout"))

        with (
            patch(
                f"{MODULE}.TD.insert_task",
                new_callable=AsyncMock,
                return_value=Result.resolve(task_mock),
            ),
            patch(f"{MODULE}.capture_increment", capture_mock),
            patch(f"{MODULE}.LOG") as log_mock,
        ):
            from acontext_core.llm.tool.task_lib.insert import insert_task_handler

            r = await insert_task_handler(_make_ctx(), _llm_args())

            assert r.ok()
            data, _ = r.unpack()
            assert data == "Task 2 created"
            log_mock.error.assert_called_once()
            assert "metric_increment_failed" in log_mock.error.call_args.args

    def test_no_create_task_in_source(self):
        """No asyncio.create_task(capture_increment(...)) remains in insert.py."""
        src = Path(__file__).resolve().parents[3] / "acontext_core" / "llm" / "tool" / "task_lib" / "insert.py"
        tree = ast.parse(src.read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func = node.func
                if isinstance(func, ast.Attribute) and func.attr == "create_task":
                    if isinstance(func.value, ast.Name) and func.value.id == "asyncio":
                        pytest.fail("Found asyncio.create_task in insert.py — metric should be awaited inline")

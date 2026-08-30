"""
Tests for process_session_pending_message.

Covers:
- Fix 1: CancelledError handling (BaseException catch + rollback)
- Fix 3: Error-Result rollback for fetch_messages_data_by_ids
- Fix 2: CoreConfig timeout defaults
- Edge cases: rollback failures, double-cancellation
"""

import asyncio
import uuid
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from acontext_core.schema.result import Result
from acontext_core.schema.config import ProjectConfig, CoreConfig
from acontext_core.schema.session.task import TaskStatus
from acontext_core.service.controller.message import process_session_pending_message


MODULE = "acontext_core.service.controller.message"

_PROJECT_ID = uuid.uuid4()
_SESSION_ID = uuid.uuid4()
_MSG_IDS = [uuid.uuid4(), uuid.uuid4()]


def _default_project_config(**overrides) -> ProjectConfig:
    defaults = {
        "project_session_message_buffer_max_turns": 16,
        "project_session_message_buffer_max_overflow": 16,
    }
    defaults.update(overrides)
    return ProjectConfig(**defaults)


def _mock_db():
    mock_db = MagicMock()
    mock_db.get_session_context.return_value.__aenter__ = AsyncMock(return_value=MagicMock())
    mock_db.get_session_context.return_value.__aexit__ = AsyncMock(return_value=False)
    return mock_db


def _base_patches(
    db_client=None,
    get_message_ids_result=None,
    update_status=None,
    fetch_messages_result=None,
    fetch_previous_result=None,
    get_ls_result=None,
    task_agent_result=None,
    get_metrics_result=False,
):
    """Return a dict of common patches for process_session_pending_message."""
    if db_client is None:
        db_client = _mock_db()
    if get_message_ids_result is None:
        get_message_ids_result = Result.resolve(_MSG_IDS)
    if update_status is None:
        update_status = AsyncMock()
    if fetch_messages_result is None:
        msg = MagicMock()
        msg.id = _MSG_IDS[0]
        msg.role = "user"
        msg.parts = []
        msg.task_id = None
        msg.created_at = "2024-01-01"
        fetch_messages_result = Result.resolve([msg])
    if fetch_previous_result is None:
        fetch_previous_result = Result.resolve([])
    if get_ls_result is None:
        get_ls_result = Result.resolve(None)
    if task_agent_result is None:
        task_agent_result = Result.resolve(None)

    return {
        f"{MODULE}.DB_CLIENT": db_client,
        f"{MODULE}.MD.get_message_ids": AsyncMock(return_value=get_message_ids_result),
        f"{MODULE}.MD.update_message_status_to": update_status,
        f"{MODULE}.MD.fetch_messages_data_by_ids": AsyncMock(return_value=fetch_messages_result),
        f"{MODULE}.MD.fetch_previous_messages_by_datetime": AsyncMock(return_value=fetch_previous_result),
        f"{MODULE}.LS.get_learning_space_for_session": AsyncMock(return_value=get_ls_result),
        f"{MODULE}.AT.task_agent_curd": AsyncMock(return_value=task_agent_result),
        f"{MODULE}.get_metrics": AsyncMock(return_value=get_metrics_result),
        f"{MODULE}.get_wide_event": MagicMock(return_value={}),
    }


# ============================================================================
# Fix 1: CancelledError handling
# ============================================================================


class TestCancelledErrorHandling:
    @pytest.mark.asyncio
    async def test_cancelled_error_after_running_rolls_back_to_failed(self):
        """CancelledError after messages set to RUNNING -> rollback to FAILED, re-raised."""
        update_status = AsyncMock()
        patches = _base_patches(update_status=update_status)
        patches[f"{MODULE}.AT.task_agent_curd"] = AsyncMock(
            side_effect=asyncio.CancelledError()
        )

        cm_list = [patch(k, v) for k, v in patches.items()]
        for cm in cm_list:
            cm.start()
        try:
            with pytest.raises(asyncio.CancelledError):
                await process_session_pending_message(
                    _default_project_config(), _PROJECT_ID, _SESSION_ID
                )

            rollback_calls = [
                c for c in update_status.call_args_list
                if c.args[1] == _MSG_IDS and c.args[2] == TaskStatus.FAILED
            ]
            assert len(rollback_calls) == 1
        finally:
            for cm in cm_list:
                cm.stop()

    @pytest.mark.asyncio
    async def test_cancelled_error_before_pending_ids_set_reraises(self):
        """CancelledError before pending_message_ids is set -> re-raised without rollback."""
        update_status = AsyncMock()
        patches = _base_patches(update_status=update_status)
        patches[f"{MODULE}.MD.get_message_ids"] = AsyncMock(
            side_effect=asyncio.CancelledError()
        )

        cm_list = [patch(k, v) for k, v in patches.items()]
        for cm in cm_list:
            cm.start()
        try:
            with pytest.raises(asyncio.CancelledError):
                await process_session_pending_message(
                    _default_project_config(), _PROJECT_ID, _SESSION_ID
                )

            rollback_calls = [
                c for c in update_status.call_args_list
                if len(c.args) >= 3 and c.args[2] == TaskStatus.FAILED
            ]
            assert len(rollback_calls) == 0
        finally:
            for cm in cm_list:
                cm.stop()

    @pytest.mark.asyncio
    async def test_regular_exception_after_running_rolls_back(self):
        """Regular Exception after RUNNING -> messages rolled back to FAILED (regression)."""
        update_status = AsyncMock()
        patches = _base_patches(update_status=update_status)
        patches[f"{MODULE}.AT.task_agent_curd"] = AsyncMock(
            side_effect=RuntimeError("boom")
        )

        cm_list = [patch(k, v) for k, v in patches.items()]
        for cm in cm_list:
            cm.start()
        try:
            with pytest.raises(RuntimeError, match="boom"):
                await process_session_pending_message(
                    _default_project_config(), _PROJECT_ID, _SESSION_ID
                )

            rollback_calls = [
                c for c in update_status.call_args_list
                if c.args[1] == _MSG_IDS and c.args[2] == TaskStatus.FAILED
            ]
            assert len(rollback_calls) == 1
        finally:
            for cm in cm_list:
                cm.stop()

    @pytest.mark.asyncio
    async def test_regular_exception_before_pending_ids_set_reraises(self):
        """Regular Exception before pending_message_ids set -> re-raised without rollback."""
        update_status = AsyncMock()
        patches = _base_patches(update_status=update_status)
        patches[f"{MODULE}.MD.get_message_ids"] = AsyncMock(
            side_effect=RuntimeError("early boom")
        )

        cm_list = [patch(k, v) for k, v in patches.items()]
        for cm in cm_list:
            cm.start()
        try:
            with pytest.raises(RuntimeError, match="early boom"):
                await process_session_pending_message(
                    _default_project_config(), _PROJECT_ID, _SESSION_ID
                )

            rollback_calls = [
                c for c in update_status.call_args_list
                if len(c.args) >= 3 and c.args[2] == TaskStatus.FAILED
            ]
            assert len(rollback_calls) == 0
        finally:
            for cm in cm_list:
                cm.stop()


# ============================================================================
# Fix 3: Error-Result rollback for fetch_messages_data_by_ids
# ============================================================================


class TestFetchMessagesErrorRollback:
    @pytest.mark.asyncio
    async def test_fetch_error_rolls_back_to_failed(self):
        """fetch_messages_data_by_ids error Result -> rollback to FAILED, error returned."""
        update_status = AsyncMock()
        error_result = Result.reject("S3 download failed")
        patches = _base_patches(
            update_status=update_status,
            fetch_messages_result=error_result,
        )

        cm_list = [patch(k, v) for k, v in patches.items()]
        for cm in cm_list:
            cm.start()
        try:
            r = await process_session_pending_message(
                _default_project_config(), _PROJECT_ID, _SESSION_ID
            )

            assert not r.ok()
            rollback_calls = [
                c for c in update_status.call_args_list
                if c.args[1] == _MSG_IDS and c.args[2] == TaskStatus.FAILED
            ]
            assert len(rollback_calls) == 1
        finally:
            for cm in cm_list:
                cm.stop()

    @pytest.mark.asyncio
    async def test_fetch_success_does_not_rollback(self):
        """fetch_messages_data_by_ids succeeds -> no rollback, processing continues."""
        update_status = AsyncMock()
        patches = _base_patches(update_status=update_status)

        cm_list = [patch(k, v) for k, v in patches.items()]
        for cm in cm_list:
            cm.start()
        try:
            r = await process_session_pending_message(
                _default_project_config(), _PROJECT_ID, _SESSION_ID
            )

            assert r.ok()
            failed_calls = [
                c for c in update_status.call_args_list
                if len(c.args) >= 3 and c.args[2] == TaskStatus.FAILED
            ]
            assert len(failed_calls) == 0
            success_calls = [
                c for c in update_status.call_args_list
                if c.args[1] == _MSG_IDS and c.args[2] == TaskStatus.SUCCESS
            ]
            assert len(success_calls) == 1
        finally:
            for cm in cm_list:
                cm.stop()


# ============================================================================
# Edge cases: rollback failures
# ============================================================================


class TestRollbackFailures:
    @pytest.mark.asyncio
    async def test_rollback_db_failure_preserves_original_exception(self):
        """update_message_status_to raises during rollback -> original CancelledError still re-raised."""
        call_count = 0

        async def _update_side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if len(args) >= 3 and args[2] == TaskStatus.FAILED:
                raise ConnectionError("DB is down")

        update_status = AsyncMock(side_effect=_update_side_effect)
        patches = _base_patches(update_status=update_status)
        patches[f"{MODULE}.AT.task_agent_curd"] = AsyncMock(
            side_effect=asyncio.CancelledError()
        )

        cm_list = [patch(k, v) for k, v in patches.items()]
        for cm in cm_list:
            cm.start()
        try:
            with pytest.raises(asyncio.CancelledError):
                await process_session_pending_message(
                    _default_project_config(), _PROJECT_ID, _SESSION_ID
                )
        finally:
            for cm in cm_list:
                cm.stop()

    @pytest.mark.asyncio
    async def test_rollback_cancelled_error_preserves_original(self):
        """update_message_status_to raises CancelledError during rollback (double-cancel) -> original still re-raised."""
        async def _update_side_effect(*args, **kwargs):
            if len(args) >= 3 and args[2] == TaskStatus.FAILED:
                raise asyncio.CancelledError()

        update_status = AsyncMock(side_effect=_update_side_effect)
        patches = _base_patches(update_status=update_status)
        patches[f"{MODULE}.AT.task_agent_curd"] = AsyncMock(
            side_effect=RuntimeError("original error")
        )

        cm_list = [patch(k, v) for k, v in patches.items()]
        for cm in cm_list:
            cm.start()
        try:
            with pytest.raises(RuntimeError, match="original error"):
                await process_session_pending_message(
                    _default_project_config(), _PROJECT_ID, _SESSION_ID
                )
        finally:
            for cm in cm_list:
                cm.stop()

    @pytest.mark.asyncio
    async def test_fetch_error_rollback_failure_still_returns_error_result(self):
        """update_message_status_to raises during Fix 3 rollback -> original error Result still returned."""
        async def _update_side_effect(*args, **kwargs):
            if len(args) >= 3 and args[2] == TaskStatus.FAILED:
                raise ConnectionError("DB is down")

        update_status = AsyncMock(side_effect=_update_side_effect)
        error_result = Result.reject("S3 download failed")
        patches = _base_patches(
            update_status=update_status,
            fetch_messages_result=error_result,
        )

        cm_list = [patch(k, v) for k, v in patches.items()]
        for cm in cm_list:
            cm.start()
        try:
            r = await process_session_pending_message(
                _default_project_config(), _PROJECT_ID, _SESSION_ID
            )

            assert not r.ok()
            assert "S3 download failed" in r.error.errmsg
        finally:
            for cm in cm_list:
                cm.stop()


# ============================================================================
# Fix 2: CoreConfig timeout defaults
# ============================================================================


class TestCoreConfigDefaults:
    def test_default_mq_handler_timeout_unchanged(self):
        """mq_consumer_handler_timeout stays at 96."""
        config = CoreConfig(llm_api_key="test")
        assert config.mq_consumer_handler_timeout == 96

    def test_default_session_message_consumer_timeout(self):
        """session_message_consumer_timeout defaults to 600."""
        config = CoreConfig(llm_api_key="test")
        assert config.session_message_consumer_timeout == 600

    def test_default_session_message_processing_timeout(self):
        """session_message_processing_timeout_seconds defaults to 660."""
        config = CoreConfig(llm_api_key="test")
        assert config.session_message_processing_timeout_seconds == 660

    def test_lock_ttl_gte_consumer_timeout(self):
        """Redis lock TTL must be >= consumer timeout."""
        config = CoreConfig(llm_api_key="test")
        assert config.session_message_processing_timeout_seconds >= config.session_message_consumer_timeout

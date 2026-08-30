"""
agentmemory V3 — Event system.

Callbacks on memory lifecycle events. Enables proactive surfacing,
watch patterns, and framework integration hooks.
"""

from __future__ import annotations

import asyncio
from collections import defaultdict
from typing import Any, Callable, Coroutine, Optional, Union

from .models import EventType, MemoryEvent, MemoryNode

EventHandler = Union[
    Callable[[MemoryEvent], None],
    Callable[[MemoryEvent], Coroutine[Any, Any, None]]
]


class EventBus:
    """Pub/sub event bus for memory lifecycle events."""

    def __init__(self):
        self._handlers: dict[EventType, list[EventHandler]] = defaultdict(list)
        self._global_handlers: list[EventHandler] = []

    def on(self, event_type: EventType, handler: EventHandler) -> Callable:
        """Register handler for a specific event type. Returns unsubscribe fn."""
        self._handlers[event_type].append(handler)
        def unsub():
            self._handlers[event_type].remove(handler)
        return unsub

    def on_any(self, handler: EventHandler) -> Callable:
        """Register handler for all events."""
        self._global_handlers.append(handler)
        def unsub():
            self._global_handlers.remove(handler)
        return unsub

    def watch(self, event_types: list[EventType],
              handler: EventHandler) -> Callable:
        """Register handler for multiple event types. Returns unsubscribe fn."""
        unsubs = [self.on(et, handler) for et in event_types]
        def unsub_all():
            for u in unsubs:
                u()
        return unsub_all

    async def emit(self, event: MemoryEvent):
        """Emit event to all registered handlers."""
        handlers = list(self._handlers.get(event.event_type, []))
        handlers.extend(self._global_handlers)
        for handler in handlers:
            try:
                result = handler(event)
                if asyncio.iscoroutine(result):
                    await result
            except Exception:
                pass  # Don't let handler errors break the pipeline

    def emit_sync(self, event: MemoryEvent):
        """Synchronous emit for non-async contexts."""
        handlers = list(self._handlers.get(event.event_type, []))
        handlers.extend(self._global_handlers)
        for handler in handlers:
            try:
                result = handler(event)
                if asyncio.iscoroutine(result):
                    # Schedule in event loop if available
                    try:
                        loop = asyncio.get_running_loop()
                        loop.create_task(result)
                    except RuntimeError:
                        pass
            except Exception:
                pass

    def clear(self):
        self._handlers.clear()
        self._global_handlers.clear()


class ProactiveSurfacer:
    """
    Maintains a hot-memory set of highest-activation nodes.
    On every add(), checks if new content is semantically similar
    to hot memories and emits PROACTIVE_SURFACE events.
    """

    def __init__(self, hot_set_size: int = 50,
                 similarity_threshold: float = 0.7):
        self._hot_set_size = hot_set_size
        self._threshold = similarity_threshold
        self._hot_nodes: dict[str, MemoryNode] = {}

    def update_hot_set(self, nodes: list[MemoryNode]):
        """Rebuild hot set from highest-activation nodes."""
        sorted_nodes = sorted(nodes, key=lambda n: n.activation, reverse=True)
        self._hot_nodes = {
            n.id: n for n in sorted_nodes[:self._hot_set_size]
        }

    def add_to_hot_set(self, node: MemoryNode):
        """Add a node to hot set if it qualifies."""
        if len(self._hot_nodes) < self._hot_set_size:
            self._hot_nodes[node.id] = node
            return
        min_node = min(self._hot_nodes.values(), key=lambda n: n.activation)
        if node.activation > min_node.activation:
            del self._hot_nodes[min_node.id]
            self._hot_nodes[node.id] = node

    def check_relevance(self, new_node: MemoryNode,
                        similarity_fn) -> list[MemoryNode]:
        """Check if new node is relevant to hot memories."""
        if not new_node.embedding:
            return []
        relevant = []
        for hot_node in self._hot_nodes.values():
            if hot_node.id == new_node.id or not hot_node.embedding:
                continue
            sim = similarity_fn(new_node.embedding, hot_node.embedding)
            if sim >= self._threshold:
                relevant.append(hot_node)
        return relevant

    @property
    def hot_set(self) -> list[MemoryNode]:
        return list(self._hot_nodes.values())

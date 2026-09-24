from __future__ import annotations

"""Explicit SHARCK V3 candidate entrypoint.

Consumers must import Runtime/create_runtime from this module instead of
instantiating the historical base class directly. The runtime preserves the
11 mandatory lanes and adds native deterministic PRESEARCH concurrently.
"""

from sharck_v3_presearch import PresearchStrictSharckV3Runtime

Runtime = PresearchStrictSharckV3Runtime
RUNTIME_CLASS = PresearchStrictSharckV3Runtime


def create_runtime(**kwargs):
    return RUNTIME_CLASS(**kwargs)
